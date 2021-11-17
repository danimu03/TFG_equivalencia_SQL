
from mo_sql_parsing import parse

def parse_Sql_To_Json(sql):
    previusJson = parse(sql);
    return parse_Sql_Json(previusJson)


def parse_Sql_Json(previusJson):
    if "select" in  previusJson:
        return sql_select(previusJson)
    
    elif "eq" in previusJson:
       return sql_eq(previusJson)

    elif "where" in previusJson:
        return sql_where(previusJson)


    elif "from" in previusJson:
        #si devuelve mas de uno es producto cartesiano
        return sql_from(previusJson)
        


def sql_select(previusJson):
    json = {}
    listAux = previusJson["select"]
    values = []
    for i in listAux:
        values.append( i["value"])
    json["type"] = "pi"
    json["proj"] = values
    del previusJson["select"]
    json["rel"] =  parse_Sql_Json(previusJson)
    return json

def sql_eq(previusJson):
    json = {}
    json["type"] = "eq"
    json["values"] = previusJson["eq"]
    return json

def sql_where(previusJson):
    json={}
    json["type"] = "sigma"
    auxJson = previusJson["where"]
    json["cond"] = parse_Sql_Json(auxJson)
    del previusJson["where"]
    json["rel"] = parse_Sql_Json(previusJson)
    return json


def sql_from(previusJson):
    value = previusJson["from"]
    if isinstance(value, list):
        return
    else:
        json = {}
        json["type"] = "rel"
        json["table"] = value
        return json


    




print(parse("SELECT Nombre, casa FROM nombre WHERE pais = \"España\""))
print(parse_Sql_To_Json("SELECT Nombre, casa FROM nombre WHERE pais = \"España\""))







