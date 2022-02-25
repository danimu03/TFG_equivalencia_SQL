import src.Rules_AR.rulesAR as rulesAR
import src.SQL_To_JSON.Sql_To_Json as sqlJSON
import src.Creates_To_JSON.Creates_Json as createsJSON

def equivalence(query_sql1,query_sql2, query_ddl=None):
    try:
        #obtenemos el json de la primera consulta
        json1 = sqlJSON.parse_Sql_To_Json(query_sql1)
        #obtenemos el json de la segunda consulta
        json2 = sqlJSON.parse_Sql_To_Json(query_sql2)

        #si tenemos una sentencia de creacion de tablas, la parseamos tambien
        if query_ddl != None:
            creates = createsJSON.create_tables_json(query_ddl)

        # TODO: llamada que calcule la equivalencia de las dos consultas
        # parametros: json1, json2, creates

        
    except Exception as e:
        print(e)


    return