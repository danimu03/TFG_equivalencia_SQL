
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
        return sql_pro(value)
    else:
        json = {}
        json["type"] = "rel"
        json["table"] = value
        return json

def sql_pro(value):
    json = {}
    json["type"] = "pro"

    lreljson = {}
    lreljson["type"] = "rel"
    lreljson["table"] = value[0]
    json["lrel"] = lreljson
    del value[0]


    if len(value) > 1:
        json["rrel"] = sql_pro(value)
    else:
        rreljson = {}
        rreljson["type"] = "rel"
        rreljson["table"] = value[0]
        del value[0]
        json["rrel"] = rreljson



    return json



    




#print(parse("SELECT Nombre, direccion FROM usuario WHERE pais = \"España\" and num = 1"))

#print(parse_Sql_To_Json("SELECT Nombre, Edad FROM Persona"))

#print(parse("SELECT Nombre FROM nombre WHERE pais = \"España\""))

