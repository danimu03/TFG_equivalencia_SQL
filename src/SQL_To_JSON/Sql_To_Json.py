from mo_sql_parsing import parse
from src.SQL_To_JSON.renameSQL import rename_json
from src.Creates_To_JSON.Creates_Json import create_tables_json as create

class ErrorSqlQuery(ValueError):
    def __init__(self, message, *args):         
        super(ErrorSqlQuery, self).__init__(message, *args)

def checkKeys(json, support):
    """
    check if all SQL operations are supported, if not, throw an exception

    :param json: dict with operations, support: dict with supported operations
    :return:
    """
    for k in json.keys():
        if k not in support:
            raise ErrorSqlQuery("SQL QUERY NOT SUPPORTED: "+ k)
        if isinstance(json[k], dict):
            checkKeys(json[k], support)
        elif isinstance(json[k], list):
            for e in json[k]:
                if isinstance(e, dict):
                    checkKeys(e, support)

    return True

# DEBE RECIBIR:
# JSON A PARSEAR
# Sentencia de creacion de tablas PARSEADAS -> create_tables_json(creates)
def parse_Sql_To_Json(sql, creates):
    """
    Parses a SQL query to JSON

    :param sql: SQL query
    :return: dict with the query transformed to relational algebra according to the definitions created
    """
    supportSQL = ("select", "from", "join", "on", "eq", "where", "and", "value", "cross join", "name", "literal")
    try:
        previousJson = parse(sql);
        checkKeys(previousJson, supportSQL)
        previousJson = rename_json(previousJson,creates)
        return parse_Sql_Json(previousJson)
    except Exception as e:
        # print(e) #para pruebas locales
        raise ErrorSqlQuery(e) #para uso final


def parse_Sql_Json(previousJson):
    """
    Transforms the dict created with mo_sql_parsing to a dict according to the definitions created

    :param previousJson: dict to transform
    :return:
    """
    if "select" in previousJson:
        return sql_select(previousJson)

    elif "and" in previousJson:
        return sql_and(previousJson)
    
    elif "eq" in previousJson:
        return sql_eq(previousJson)

    elif "where" in previousJson:
        return sql_where(previousJson)

    elif "from" in previousJson:
        #si devuelve mas de uno es producto cartesiano o join
        return sql_from(previousJson)
        


def sql_select(previousJson):
    """
    Transforms the SELECT key-value pair, modifies the previousJson and recursively calls the function parse_Sql_Json()

    :param previousJson: dict to transform
    :return: dict with the query transformed to relational algebra according to the definitions created
    """
    json = {}
    listAux = previousJson["select"]
    values = []
    if isinstance(listAux, list):
        for i in listAux:
            values.append(i["value"])
    else: 
        values.append(listAux["value"])
    json["type"] = "pi"
    json["proj"] = values
    del previousJson["select"]
    json["rel"] = parse_Sql_Json(previousJson)
    return json

def sql_and(previousJson):
    """
    Transforms the AND key-value pair, modifies the previousJson and recursively calls the function parse_Sql_Json()

    :param previousJson: dict to transform
    :return: dict with the query transformed to relational algebra according to the definitions created
    """
    json = {}
    json["type"] = "and"
    aux = previousJson["and"]
    values = []
    for i in aux:
        values.append(parse_Sql_Json(i))
    json["values"] = values
    return json

def sql_eq(previousJson):
    """
    Transforms the EQ key-value pair, modifies the previousJson and recursively calls the function parse_Sql_Json()

    :param previousJson: dict to transform
    :return: dict with the query transformed to relational algebra according to the definitions created
    """
    json = {}
    json["type"] = "eq"
    values = []
    for i in previousJson["eq"]:
        if isinstance(i,dict):
            values.append(i['literal'])
        else:
            values.append(i)    
    json["values"] = values
    return json



def sql_where(previousJson):
    """
    Transforms the WHERE key-value pair, modifies the previousJson and recursively calls the function parse_Sql_Json()

    :param previousJson: dict to transform
    :return: dict with the query transformed to relational algebra according to the definitions created
    """
    json={}
    json["type"] = "sigma"
    auxJson = previousJson["where"]
    json["cond"] = parse_Sql_Json(auxJson)
    del previousJson["where"]
    json["rel"] = parse_Sql_Json(previousJson)
    return json


def sql_from(previousJson):
    """
    Transforms the FROM key-value pair, modifies the previousJson and recursively calls the function parse_Sql_Json()

    :param previousJson: dict to transform
    :return: dict with the query transformed to relational algebra according to the definitions created
    """
    value = previousJson["from"]
    del previousJson["from"]
    if isinstance(value, list):
        return sql_pro_or_join(value)
    else:
        json = {}
        json["type"] = "rel"
        if isinstance(value, dict):
            aux = {}
            aux['type'] = "rho"
            aux['ren'] = [value['value'], value['name']]
            json["table"] = aux #check
        else: 
            json["table"] = value #check
        return json

def sql_pro_or_join(values):
    """
    Checks if the list of received elements contains a Join or a projection and calls the corresponding functions to transform them

    :param values: list of elements to transform
    :return: dict with the query transformed to relational algebra according to the definitions created
    """
    for i in values:
        if isinstance(i, dict):
            if "join" in i.keys():
                return sql_join(values)
            #else:
                #return sql_pro(values)
    return sql_pro(values)

def sql_join(value):
    """
    Transforms the JOIN key-value pair with the list of values received.

    :param value: list of elements to transform
    :return: dict with the query transformed to relational algebra according to the definitions created
    """
    json = {}
    json["type"] = "join"
    valueJoin = value[1]
    json["cond"] = sql_eq(valueJoin["on"])

    lreljson = {}
    lreljson["type"] = "rel"
    lreljson["table"] = sql_join_dict(value[0]) #check
    json["lrel"] = lreljson
    del value[0]

    if len(value) > 1:
        json["rrel"] = sql_join(value)
    else:
        rreljson = {}
        rreljson["type"] = "rel"
        rreljson["table"] = sql_join_dict(value[0]) #check
        del value[0]
        json["rrel"] = rreljson
    return json

def sql_join_dict(value):
    """
    Auxiliary function when we do not know if we have transformed all the joins of the query

    :param value: list of elements to transform or a single element
    :return: a single element if we are done or the next Join
    """
    
    if isinstance(value, dict) and "join" in value.keys():
        if isinstance(value["join"], dict):
            ret = {}
            ret['type'] = "rho"
            ret['ren'] = [value["join"]['value'], value["join"]['name']]
        else:
            ret = value["join"]
    elif isinstance(value, dict):
        ret = {}
        ret['type'] = "rho"
        ret['ren'] = [value['value'], value['name']]
    else:
        ret = value
    
    return ret
    

def sql_pro(value):
    """
    Transforms the CARTESIAN PRODUCT key-value pair, modifies the previousJson and recursively calls the function parse_Sql_Json()

    :param value: list of elements to transform or a single element
    :return: dict with the query transformed to relational algebra according to the definitions created
    """
    json = {}
    json["type"] = "pro"

    lreljson = {}
    lreljson["type"] = "rel"
    lreljson["table"] = sql_crossJoin(value[0]) #check
    json["lrel"] = lreljson
    del value[0]


    if len(value) > 1:
        json["rrel"] = sql_pro(value)
    else:
        rreljson = {}
        rreljson["type"] = "rel"
        rreljson["table"] = sql_crossJoin(value[0]) #check
        del value[0]
        json["rrel"] = rreljson
    return json


def sql_crossJoin(pre):
    """
    Auxiliary function when we do not know if we have transformed all the cartesian products of the query

    :param pre: list of elements to transform or a single element
    :return: a single element if we are done or the next cartesian product
    """
    if isinstance(pre, dict) and "cross join" in pre.keys():
        if isinstance(pre["cross join"], dict):
            ret = {}
            ret['type'] = "rho"
            ret['ren'] = [pre["cross join"]['value'], pre["cross join"]['name']]
        else:
            ret = pre["cross join"]
    elif isinstance(pre, dict):
            ret = {}
            ret['type'] = "rho"
            ret['ren'] = [pre['value'], pre['name']]
    else:
        ret = pre
    
    return ret









                    




#print(parse("SELECT Nombre, direccion FROM usuario CROSS JOIN persona CROSS JOIN movil WHERE pais = \"España\" and num = 1"))
#print(parse("SELECT Nombre, direccion FROM usuario, persona, movil WHERE pais = \"España\" and num = 1"))
#print(parse_Sql_To_Json("SELECT Nombre, direccion FROM usuario as u CROSS JOIN persona as p  CROSS JOIN movil WHERE pais = \"España\" and num = 1"))
#print(parse("SELECT Nombre, direccion FROM usuario as u  CROSS JOIN persona as p CROSS JOIN movil WHERE pais = \"España\" and num = 1"))
#print(parse_Sql_To_Json("SELECT Nombre, direccion FROM usuario, persona, movil WHERE pais = \"España\" and num = 1"))
#print(parse_Sql_To_Json("SELECT Nombre, direccion FROM usuario, persona, movil WHERE pais = \"España\" and num = 1 GROUP BY name"))
#print(parse_Sql_To_Json("SELECT Nombre, Edad FROM Persona"))

#print(parse("SELECT Nombre FROM nombre WHERE pais = \"España\""))

#print(parse("SELECT nombre FROM user JOIN empleado ON dni = dniempleado"))

#print(parse_Sql_To_Json("SELECT u.flno, u.origen FROM vuelo as u where flno = '4658'", create(["create table vuelo(flno number(4,0) primary key, origen varchar2(20), destino varchar2(20), distancia number(6,0), salida date, llegada date, precio number(7,2));"])))
#print(parse("SELECT Nombre, direccion FROM usuario as u where Nombre = 'pepe'"))

#print(parse_Sql_To_Json("SELECT p.nombre FROM Jugador j join Persona p on nombre = nombre", create(["create table Jugador(nombre varchar2(30) primary key);", "create table Persona(nombre varchar2(30) primary key);"])))

#supportSQL = ("select", "from", "join", "on", "eq")
#json = parse("SELECT Nombre, Ap1, Ap2 FROM Empl, Empl2 JOIN Proyecto ON Dni = DniDir")
#print(checkKeys(json, supportSQL))

#print(parse("SELECT nombre FROM jugador as j join pepe as jose"))
#print(parse("CREATE TABLE Jugador (DNI INT PRIMARY KEY,Nombre VARCHAR(25),CIF INT REFERENCES Club(CIF))"))


#print(parse("SELECT nombre FROM Persona, Jugador"))
#print(parse("SELECT nombre FROM Persona join Jugador on nombre = nombre"))
#print(parse_Sql_Json(parse("SELECT nombre FROM Persona join Jugador on nombre = nombre")))
#print(rename_json(parse("SELECT p.nombre FROM Jugador j join Persona p on nombre = nombre"), create(["create table Jugador(nombre varchar2(30) primary key);", "create table Persona(nombre varchar2(30) primary key);" ])))
#print(parse_Sql_Json(rename_json(parse("SELECT p.nombre FROM Jugador j join Persona p on p.nombre = j.nombre"), create(["create table Jugador(nombre varchar2(30) primary key);", "create table Persona(nombre varchar2(30) primary key);" ]))))

#print(parse("SELECT nombre FROM Persona where id = '1'"))
#print(parse("SELECT nombre FROM Persona join Jugador on nombre = nombre where id ='1'"))

#d = {'from': ['Persona', {'join': 'Jugador', 'on': {'eq': ['nombre', 'nombre']}}]}
#for i in range(len(d['from'])):
#   print(d['from'][i])
#   if isinstance(d['from'][i], str):
#       print("string")
#   elif isinstance(d['from'][i], dict):
#       print("dict")

#print(create(["CREATE TABLE Persona(nombre VARCHAR2(30) PRIMARY KEY,"
#            "ap1 VARCHAR(10),"
#           "ap2 VARCHAR(10),"
#          "edad INT(3),"
#         "telefono INT(9),"
#        "pais VARCHAR(10));",
#      "CREATE TABLE Empr (nombre VARCHAR(20) PRIMARY KEY);"]))

#print(parse("SELECT nombre FROM Persona WHERE pais = \"España\" AND nombre = \"A\""))
print(parse_Sql_To_Json("SELECT nombre, id, dep FROM Persona, Empr, Dep", create([
            "CREATE TABLE Persona(nombre VARCHAR2(30) PRIMARY KEY,"
             "ap1 VARCHAR(10),"
             "ap2 VARCHAR(10),"
             "edad INT(3),"
             "telefono INT(9),"
             "pais VARCHAR(10));",
            "CREATE TABLE Empr (id INT(2) PRIMARY KEY);",
            "CREATE TABLE Dep (dep INT(10) PRIMARY KEY);"
             ])))