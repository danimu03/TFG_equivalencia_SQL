from mo_sql_parsing import parse
from src.Creates_To_JSON.Creates_Json import *

class ErrorRenameSQL(ValueError):
    def __init__(self, message, *args):         
        super(ErrorRenameSQL, self).__init__(message, *args)

def rename_json(json, creates):
    #objengo una lista con las tablas de la proyeccion
    tables_from = extract_from(json, creates) 

    #renombro las columnas del select
    json = rename_select(json, tables_from, creates)

    #renombro las columnas de where
    json = rename_where(json, tables_from, creates)

    #renombro el from

    json = rename_from(json, tables_from)

    return json

def check_tables(tables, name, prerename=None):
    ret = 0
    for e in tables:
        if name == e[0]:
            ret += 1
        if prerename and prerename == e[1]:
            raise ErrorRenameSQL('ERROR: mismo renombramiento para dos tablas')
    return ret


#e[0] -> nombre de la tabla
#e[1] -> pre-renombramiento
#e[2] -> nuestro renombramiento     
def extract_from(json, tables):
    frm = json['from']
    tables = []
    if isinstance(frm, dict):
        aux = []
        aux.append(frm['value'])
        aux.append(frm['name'])
        aux.append(frm['value']+str(check_tables(tables, frm['value'], frm['name'])+1))
        tables.append(aux)
    elif isinstance(frm, list):
        for e in frm:
            if isinstance(e,dict):
                if 'value' in e.keys():
                    aux1 = []
                    aux1.append(e['value'])
                    aux1.append(e['name'])
                    aux1.append(e['value']+str(check_tables(tables, e['value'], e['name'])+1))
                    tables.append(aux1)
                elif 'join' in e.keys() and isinstance(e['join'], dict):
                    j = e['join']
                    aux1 = []
                    aux1.append(j['value'])
                    aux1.append(j['name'])
                    aux1.append(j['value']+str(check_tables(tables, j['value'], j['name'])+1))
                    tables.append(aux1)
                else:
                    aux1 = []
                    aux1.append(e['join'])
                    aux1.append('')
                    aux1.append(e['join']+str(check_tables(tables, e['join'])+1))
                    tables.append(aux1)
            else:
                aux2=[]
                aux2.append(e)
                aux2.append('')
                aux2.append(e+str(check_tables(tables, e)+1))
                tables.append(aux2)
    else:
        aux = []
        aux.append(frm)
        aux.append("")
        aux.append(frm+str(check_tables(tables, frm)+1))
        tables.append(aux)

    return tables



def rename_from(json, tables):
    if isinstance(json['from'], str):
        aux = {}
        aux['value'] = json['from']
        aux['name'] = tables[0][2]
        json['from'] = aux
    elif isinstance(json['from'], dict):
        json['from']['name'] = tables[0][2]
    elif isinstance(json['from'], list):
        for i in range(len(json['from'])):
            if isinstance(json['from'][i], str):
                aux = {}
                aux['value'] = json['from'][i]
                aux['name'] = tables[i][2]
                json['from'][i] = aux
            elif isinstance(json['from'][i], dict) and 'join' in json['from'][i].keys():
                if isinstance(json['from'][i]['join'],dict):
                    aux = {}
                    aux['value'] = json['from'][i]['join']['value']
                    aux['name'] = tables[i][2]
                    json['from'][i]['join'] = aux
                else:
                    aux = {}
                    aux['value'] = json['from'][i]['join']
                    aux['name'] = tables[i][2]
                    json['from'][i]['join'] = aux
            elif isinstance(json['from'][i], dict) and 'value' in json['from'][i].keys():
                aux = {}
                aux['value'] = json['from'][i]['value']
                aux['name'] = tables[i][2]
                json['from'][i] = aux
    return json



#json -> json sin parsear
#tables -> tables del from
#create -> sentencias de creacion de tablas
def rename_select(json, tables, creates):
    select = json['select']

    if isinstance(select, list):
        aux = []
        for e in select:
            aux.append({'value': check_colum(e['value'], tables, creates)})
        json['select'] = aux

    else:
        json['select'] = {'value': check_colum(select['value'], tables, creates)}
    return json


def rename_where(json, tables, creates):
    if 'where' in json.keys():
        whe = json['where']

        if 'and' in whe.keys():
            an = whe['and']
            aux1=[]
            for e in an:
                aux = []
                for i in e['eq']:
                    if isinstance(i,str): 
                        aux.append(check_colum(i, tables, creates))
                    else:
                        aux.append(i)
                aux1.append({'eq': aux})
            json['where']['and'] = aux1
        else:
            eq = whe['eq']
            aux = []
            for e in eq:
                if isinstance(e,str): 
                    aux.append(check_colum(e, tables, creates))
                else:
                    aux.append(e)
            json['where'] = {'eq': aux}
    return json

#recibo el nombre de una columna y lo renombro
def check_colum(colum, tables, creates):
    ret = ''
    if colum.find('.') != -1:
        #está renombrada
        colum_re = check_pre_rename(tables,colum[0:colum.find('.')], None)
        if len(colum_re) > 0 and len(colum_re) <2:
            ret = (colum_re[0][2]+colum[colum.find('.'):])
        else:
            raise ErrorRenameSQL('ERROR: no concuerda con el renombramiento de ninguna tabla')
    else:
        #no está renombrada
        colums_creates = check_creates(colum, creates)
        #chequeo la columna con los crates
        if len(colums_creates) == 0:
            #no coincide con ninguna
            raise ErrorRenameSQL('ERROR: no coincide la columna a proyectar con ninguna de las tablas de From')
        elif len(colums_creates) > 1:
            #coincide con mas de una
            raise ErrorRenameSQL('ERROR: consulta ambigua')
        else:
            colum_re = check_pre_rename(tables, None, colums_creates[0])
            #compruebo si la tabla con la que coincide aparece mas de una vez en el join     
            if len(colum_re) != 1:
                raise ErrorRenameSQL('ERROR: consulta ambigua')
            else:
                #correcto
                ret = (colum_re[0][2]+'.'+colum)
    return ret

#si tiene parseo -> chequeo que concuerde y lo cambio (si no concuerda expecion)
#si no tiene parseo -> compruebo los creates (si devuelve mas de uno en list excepcion- > si devuelve uno pero hay mas de dos tablas en tables excepcion)


#Chequeo si concuerda el renombramiento con los existentes en las tablas de FROM o el nombre de la tabla coincidente
def check_pre_rename(tables, prerename= None, prename=None):
    ret = []
    if prerename:
        for e in tables:
            if prerename == e[1] or prerename == e[0] :
                ret.append(e)
              

    if prename:
        for e in tables:
            if prename == e[0]:
                ret.append(e)
    return ret


#compruebo las columnas con las setencias creates
def check_creates(colum, creates):
    ret = []
    for e in creates:
        columns_e = e['columns']
        if isinstance(columns_e, list):
            for i in columns_e:
                if colum == i['name']:
                    ret.append(e['name'])
                    break
        else:
            if colum == columns_e['name']:
                ret.append(e['name'])
    return ret



#print(create_tables_json(["create table Jugador(nombre varchar2(30) primary key, dni varchar(10));", "create table Persona(nom varchar2(30) primary key, dni varchar(10));" ]))

#print(check_creates('nombre', create_tables_json(["create table Jugador(nombre varchar2(30) primary key, dni varchar(10));", "create table Persona(nom varchar2(30) primary key, dni varchar(10));" ])))







#print(create_tables_json(["create table vuelo(flno number(4,0) primary key, origen varchar2(20), destino varchar2(20), distancia number(6,0), salida date, llegada date, precio number(7,2));", "create table avion(aid number(9,0) primary key, nombre varchar2(30), autonomia number(6,0));"]))
#print(parse("SELECT nombre FROM Jugador j join pepe p  WHERE nombre = aid and nombre = 'pepe'"))

#print(parse("SELECT p.nombre, j.nombre FROM Jugador j join persona p"))
#print(rename_json(parse("SELECT p.nombre,j.nombre FROM Jugador j join persona p"), create_tables_json(["create table Jugador(nombre varchar2(30) primary key);", "create table Persona(nombre varchar2(30) primary key);" ])))



# TEST CASES:

#Debe lanzar una excepcion por utilizar el mismo renoombramiento para dos tablas
#print(extract_from(parse("SELECT nombre FROM Jugador j join persona p"), None))

#print(rename_json(parse("SELECT Persona.nombre FROM Persona, Jugador"), create_tables_json(["create table Persona(nombre varchar2(30) primary key);","create table Jugador(nombre varchar2(30) primary key);"])))

#OK
#print(parse("SELECT p.nombre FROM Jugador j join persona p"))
#print(rename_json(parse("SELECT p.nombre FROM Jugador p join persona p"), create_tables_json(["create table Jugador(nombre varchar2(30) primary key);", "create table Persona(nombre varchar2(30) primary key);" ])))


#OK
#print(parse("SELECT p.nombre, j.nombre FROM Jugador j join persona p"))
#print(rename_json(parse("SELECT p.nombre,j.nombre FROM Jugador j join persona p"), create_tables_json(["create table Jugador(nombre varchar2(30) primary key);", "create table Persona(nombre varchar2(30) primary key);" ])))



#OK
#print(parse("SELECT nombre FROM Jugador  join persona "))
#print(rename_json(parse("SELECT nombre FROM Jugador  join persona "), create_tables_json(["create table Jugador(nombre varchar2(30) primary key);", "create table Persona(dni varchar2(30) primary key);" ])))


#OK
#print(parse("SELECT nombre FROM Jugador  join persona "))
#print(rename_json(parse("SELECT nombre, dni FROM Jugador  join persona "), create_tables_json(["create table Jugador(nombre varchar2(30) primary key);", "create table persona(dni varchar2(30) primary key);" ])))


#excepcion consulta ambigua
#print(parse("SELECT nombre FROM Jugador  join persona "))
#print(rename_json(parse("SELECT nombre, dni FROM Jugador  join persona "), create_tables_json(["create table Jugador(nombre varchar2(30) primary key);", "create table persona(nombre varchar2(30),dni varchar2(30) primary key);" ])))


#ok
#print(parse("SELECT j.nombre FROM Jugador j  join persona p Where j.nombre = p.nombre"))
#print(rename_json(parse("SELECT j.nombre FROM Jugador j  join persona p Where j.nombre = p.nombre"), create_tables_json(["create table Jugador(nombre varchar2(30) primary key);", "create table persona(nombre varchar2(30),dni varchar2(30) primary key);" ])))


#ok
#print(parse("SELECT Jugador.nombre FROM Jugador   join persona Where Jugador.nombre = persona.nombre and Jugador.nombre = 'pepe'"))
#print(rename_json(parse("SELECT Jugador.nombre FROM Jugador  join persona  Where nombre = namee and nombre = 'pepe'"), create_tables_json(["create table Jugador(nombre varchar2(30) primary key);", "create table persona(namee varchar2(30),dni varchar2(30) primary key);" ])))
