from mo_sql_parsing import parse
from Creates_To_JSON.Creates_Json import create_tables_json


class ErrorRenameSQL(ValueError):
    def __init__(self, message, *args):         
        super(ErrorRenameSQL, self).__init__(message, *args)

def rename_json(json, creates):
    #objengo una lista con las tablas de la proyeccion
    tables_from = rename_from(json, creates) 

    #renombro las columnas del select
    json = rename_select(json, tables_from, creates)

    return json

def check_tables(tables, name, prerename=None):
    ret = 0
    for e in tables:
        if name == e[0]:
            ret += 1
        if prerename and prerename == e[1]:
            raise ErrorRenameSQL('ERROR: mismo renombramiento para dos tablas')
    return ret

def rename_from(json, tables):
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



#json -> json sin parsear
#tables -> tables del from
#create -> sentencias de creacion de tablas
def rename_select(json, tables, creates):
    select = json['select']

    if isinstance(select, list):
        None
    else:
        json['select'] = {'value': check_colum(select['value'], tables, creates)}
    return json


#recibo el nombre de una columna y lo renombro
def check_colum(colum, tables, creates):
    ret = ''
    if colum.find('.') != -1:
        colum_re = check_rename(colum[0:colum.find('.')], tables)
        if len(colum_re) > 0 and len(colum_re) <2:
            ret = (colum_re[0][2]+colum[colum.find('.'):])
        else:
            raise ErrorRenameSQL('ERROR: no concuerda con el renombramiento de ninguna tabla')
    else:
        None
    return ret

#si tiene parseo -> chequeo que concuerde y lo cambio (si no concuerda expecion)
#si no tiene parseo -> compruebo los creates (si devuelve mas de uno en list excepcion- > si devuelve uno pero hay mas de dos tablas en tables excepcion)


#Chequeo si concuerda el renombramiento con los existentes en las tablas de FROM
def check_rename(prerename, tables):
    ret = []
    for e in tables:
        if prerename == e[1]:
            ret.append(e)
    return ret







#print(create_tables_json(["create table vuelo(flno number(4,0) primary key, origen varchar2(20), destino varchar2(20), distancia number(6,0), salida date, llegada date, precio number(7,2));", "create table avion(aid number(9,0) primary key, nombre varchar2(30), autonomia number(6,0));"]))
#print(parse("SELECT nombre FROM Jugador j join pepe p  WHERE nombre = aid and nombre = 'pepe'"))

print(parse("SELECT nombre FROM Jugador j join persona p"))

print(rename_json(parse("SELECT p.nombre FROM Jugador j join persona p"), create_tables_json(["create table Jugador(nombre varchar2(30) primary key);", "create table Persona(nombre varchar2(30) primary key);" ])))
#print(rename_from(parse("SELECT nombre FROM Jugador j join persona p"), None))


#Debe lanzar una excepcion por utilizar el mismo renoombramiento para dos tablas
#print(rename_from(parse("SELECT nombre FROM Jugador j join persona p"), None))