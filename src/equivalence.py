import Rules_AR.rulesAR as rulesAR
import SQL_To_JSON.Sql_To_Json as sqlJSON
import Creates_To_JSON.Creates_Json as createsJSON

def equivalence(query_sql1,query_sql2, query_ddl=None):
    try:
        #obtenemos el json de la primera consulta
        json1 = sqlJSON.parse_Sql_To_Json(query_sql1)
        #obtenemos el json de la segunda consulta
        json2 = sqlJSON.parse_Sql_To_Json(query_sql2)

        #si tenemos una sentencia de creacion de tablas, la parseamos tambien
        if query_ddl != None:
            creates = createsJSON.create_tables_json(query_ddl)
        else:
            creates = null

        # TODO: llamada que calcule la equivalencia de las dos consultas
        json1rulesApplied = applyRules(json1, creates, false)
        json2rulesApplied = applyRules(json2, creates, false)
        # parametros: json1, json2, creates

        if json1rulesApplied.equals(json2rulesApplied):
            return True
        else:
            return False
    except Exception as e:
        print(e)


    return soluciones[x]


def applyRules(json, creates, *esFinal):
    jsonResultado = {}
    if json['type'] == 'sigma':
        if 'type' in json['rel']:
            applyRules(json['rel'], creates, *esFinal)
            if esFinal:
                if json['rel']['type'] == 'sigma':
                    #aplicamos regla 2, 1
                    jsonResultado = rulesAR.rule2(json)
                    jsonResultado = rulesAR.rule1(jsonResultado)
                elif json['rel']['type'] == 'pro':
                    #aplicamos la regla 5a
                    jsonResultado = rulesAR.rule5a(json)
                elif json['rel']['type'] == 'join':
                    #aplicamos la regla 5b
                    jsonResultado = rulesAR.rule5b(json)
        else:
            esFinal = true
    elif json['type'] == 'pi':
        if 'type' in json['rel']:
            applyRules(json['rel'], creates, *esFinal)
            if esFinal:
                if json['rel']['type'] == 'sigma':
                    #aplicamos regla 4
                    jsonResultado=rulesAR.rule4(json)
                elif json['rel']['type'] == 'pi':
                    #aplicamos la regla 3
                    jsonResultado=rulesAR.rule3(json)
                elif json['rel']['type'] == 'join':
                    #¿Se puede aplicar la regla 11B?
                    if ['rel']['rrel']['type'] == 'pi' and ['rel']['lrel']['type'] == 'pi':
                        jsonResultado=rulesAR.rule11b(json)
        else:
            esFinal = true
    elif json['type'] == 'pro':
        #6 8a 9a 9b
        leftJson = false
        rightJson = false
        if 'type' in json['lrel']:
            applyRules(json['lrel'], creates, *esFinal)
            leftJson = true
        if 'type' in json['rrel']:
            applyRules(json['lrel'], creates, *esFinal)
            rightJson = true

        #aplicamos las reglas
        if leftJson == False and rightJson == False:
            #regla 6
            jsonResultado=rulesAR.rule6(json)
        elif leftJson == True and rightJson == False:
            if json['type']['lrel'] == 'pro':
                #aplicamos regla 8a
                jsonResultado.rulesAR.rule8a(json)
            elif json['type']['lrel'] == 'sigma':
                #aplicamos la regla 9a
                jsonResultado.rulesAR.rule9a(json)
        elif leftJson == True and rightJson == True:
                #¿Aplicamos la regla 9b?
                if json['type']['lrel'] == 'sigma' and json['type']['rrel'] == 'sigma':
                    jsonResultado.rulesAR.rule9b(json)
    elif json['type'] == 'join':
        #7 8b 10a 10b 11a
        leftJson = false
        rightJson = false
        if 'type' in json['lrel']:
            applyRules(json['lrel'], creates, *esFinal)
            leftJson = true
        if 'type' in json['rrel']:
            applyRules(json['lrel'], creates, *esFinal)
            rightJson = true

            # aplicamos las reglas
            if leftJson == False and rightJson == False:
                #aplicamos la regla 7
                jsonResultado=rulesAR.rule7(json)
            elif leftJson == True and rightJson == False:
                if json['lrel']['type'] == 'join':
                    #aplicamos la regla 8b
                    jsonResultado.rulesAr.rule8b(json)
                elif json['lrel']['type'] == 'sigma':
                    #aplicamos la regla 10a
                    jsonResultado.rulesAR.rule10a(json)
            elif leftJson == True and rightJson == True:
                # ¿Aplicamos la regla 10b?
                if json['type']['lrel'] == 'sigma' and json['type']['rrel'] == 'sigma':
                    jsonResultado.rulesAR.rule10b(json)
                # ¿Aplicamos la regla 11a?
                elif json['type']['lrel'] == 'pi' and json['type']['rrel'] == 'pi':
                    jsonResultado.rulesAR.rule11a(json)


    return jsonResultado