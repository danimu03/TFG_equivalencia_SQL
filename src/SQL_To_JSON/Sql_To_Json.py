
from mo_sql_parsing import parse

def parse_Sql_To_Json(sql):
    """
    Parses a SQL query to JSON

    :param sql: SQL query
    :return: dict with the query transformed to relational algebra according to the definitions created
    """

    previousJson = parse(sql);
    return parse_Sql_Json(previousJson)


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
        #si devuelve mas de uno es producto cartesiano
        return sql_from(previousJson)
        


def sql_select(previousJson):
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
    json["rel"] =  parse_Sql_Json(previousJson)
    return json

def sql_and(previousJson):
    json = {}
    json["type"] = "and"
    aux = previousJson["and"]
    values = []
    for i in aux:
        values.append(parse_Sql_Json(i))
    json["values"] = values
    return json

def sql_eq(previousJson):
    json = {}
    json["type"] = "eq"
    json["values"] = previousJson["eq"]
    return json



def sql_where(previousJson):
    json={}
    json["type"] = "sigma"
    auxJson = previousJson["where"]
    json["cond"] = parse_Sql_Json(auxJson)
    del previousJson["where"]
    json["rel"] = parse_Sql_Json(previousJson)
    return json


def sql_from(previousJson):
    value = previousJson["from"]
    del previousJson["from"]
    if isinstance(value, list):
        return sql_pro_or_join(value)
    else:
        json = {}
        json["type"] = "rel"
        json["table"] = value
        return json

def sql_pro_or_join(values):
    for i in values:
        if isinstance(i, dict):
            if "join" in i.keys():
                return sql_join(values)
            else:
                return sql_pro(values)
    return sql_pro(values)

def sql_join(value):
    json = {}
    json["type"] = "join"
    valueJoin = value[1]
    json["cond"] = sql_eq(valueJoin["on"])

    lreljson = {}
    lreljson["type"] = "rel"
    lreljson["table"] = sql_join_dict(value[0])
    json["lrel"] = lreljson
    del value[0]

    if len(value) > 1:
        json["rrel"] = sql_join(value)
    else:
        rreljson = {}
        rreljson["type"] = "rel"
        rreljson["table"] = sql_join_dict(value[0])
        del value[0]
        json["rrel"] = rreljson
    return json

def sql_join_dict(value):
    if isinstance(value, dict):
        return value["join"]
    else:
        return value
    

def sql_pro(value):
    json = {}
    json["type"] = "pro"

    lreljson = {}
    lreljson["type"] = "rel"
    lreljson["table"] = sql_crossJoin(value[0])
    json["lrel"] = lreljson
    del value[0]


    if len(value) > 1:
        json["rrel"] = sql_pro(value)
    else:
        rreljson = {}
        rreljson["type"] = "rel"
        rreljson["table"] = sql_crossJoin(value[0])
        del value[0]
        json["rrel"] = rreljson
    return json


def sql_crossJoin(pre):
    if isinstance(pre, dict):
        return pre["cross join"]
    else:
        return pre 




    




#print(parse("SELECT Nombre, direccion FROM usuario CROSS JOIN persona CROSS JOIN movil WHERE pais = \"España\" and num = 1"))
#print(parse("SELECT Nombre, direccion FROM usuario, persona, movil WHERE pais = \"España\" and num = 1"))
#print(parse_Sql_To_Json("SELECT Nombre, direccion FROM usuario CROSS JOIN persona CROSS JOIN movil WHERE pais = \"España\" and num = 1"))
#print(parse_Sql_To_Json("SELECT Nombre, direccion FROM usuario, persona, movil WHERE pais = \"España\" and num = 1"))

#print(parse_Sql_To_Json("SELECT Nombre, Edad FROM Persona"))

#print(parse("SELECT Nombre FROM nombre WHERE pais = \"España\""))

#print(parse("SELECT nombre FROM user JOIN empleado ON dni = dniempleado"))
print(parse_Sql_To_Json("SELECT Nombre, Ap1, Ap2 FROM Empl JOIN Proyecto ON Dni = DniDir"))

