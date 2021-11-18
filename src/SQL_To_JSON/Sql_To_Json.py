
from mo_sql_parsing import parse

def parse_Sql_To_Json(sql):
    previousJson = parse(sql);
    return parse_Sql_Json(previousJson)


def parse_Sql_Json(previousJson):
    if "select" in  previousJson:
        return sql_select(previousJson)
    
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
    if isinstance(value, list):
        return
    else:
        json = {}
        json["type"] = "rel"
        json["table"] = value
        return json


    




print(parse("SELECT Nombre, direccion FROM usuario WHERE pais = \"España\""))
print(parse_Sql_To_Json("SELECT Nombre, direccion FROM usuario WHERE pais = \"España\""))

print(parse("SELECT Nombre FROM nombre WHERE pais = \"España\""))
