import src.Rules_AR.rulesAR as rulesAR
import src.SQL_To_JSON.Sql_To_Json as sqlJSON
import src.Creates_To_JSON.Creates_Json as createsJSON
import copy

def equivalence(query_sql1,query_sql2, query_ddl=None):
    soluciones = ['Equivalentes', 'No sabemos']
    try:
        # si tenemos una sentencia de creacion de tablas, la parseamos tambien
        if query_ddl != None:
            creates = createsJSON.create_tables_json(query_ddl)
        else:
            creates = None


        #obtenemos el json de la primera consulta
        json1 = sqlJSON.parse_Sql_To_Json(query_sql1, creates)
        #obtenemos el json de la segunda consulta
        json2 = sqlJSON.parse_Sql_To_Json(query_sql2, creates)

        final1 = [False]
        final2 = [False]

        # TODO: llamada que calcule la equivalencia de las dos consultas
        json1rulesApplied = applyRules(json1, creates, final1)
        json2rulesApplied = applyRules(json2, creates, final2)
        # parametros: json1, json2, creates

        if json1rulesApplied.equals(json2rulesApplied):
            return True
        else:
            return False
    except Exception as e:
        print(e)


    return soluciones[0]


def applyRules(json, creates, esFinal):
    jsonResultado = {}
    if json['type'] == 'sigma':
        if 'type' in json['rel']:
            jsonCopia = copy.deepcopy(json['rel'])
            applyRules(jsonCopia, creates, esFinal)
            json['rel'] = jsonCopia
            if esFinal[0]:
                if json['rel']['type'] == 'sigma':
                    #aplicamos regla 2, 1
                    jsonResultado = rulesAR.rule2(json)
                    jsonResultado = rulesAR.rule1(jsonResultado)
                elif json['rel']['type'] == 'pro':
                    #aplicamos la regla 5a
                    jsonCopia = copy.deepcopy(json)
                    jsonResultado = rulesAR.rule5A(jsonCopia)
                    json = jsonResultado
                elif json['rel']['type'] == 'join':
                    #aplicamos la regla 5b
                    jsonCopia = copy.deepcopy(json)
                    jsonResultado = rulesAR.rule5B(jsonCopia)
                    json = jsonResultado
                else:
                    jsonResultado = json
        else:
            esFinal[0] = True
            jsonResultado = json
    elif json['type'] == 'pi':
        if 'type' in json['rel']:
            applyRules(json['rel'], creates, esFinal)
            if esFinal[0]:
                if json['rel']['type'] == 'sigma':
                    #aplicamos regla 4
                    jsonCopia = copy.deepcopy(json)
                    jsonResultado=rulesAR.rule4(jsonCopia)
                    json = jsonResultado
                    esFinal[0] = False
                elif json['rel']['type'] == 'pi':
                    #aplicamos la regla 3
                    jsonResultado=rulesAR.rule3(json)
                elif json['rel']['type'] == 'join':
                    #¿Se puede aplicar la regla 11B?
                    if json['rel']['rrel']['type'] == 'pi' and json['rel']['lrel']['type'] == 'pi':
                        jsonResultado=rulesAR.rule11B(json)
                else:
                    jsonResultado = json
        else:
            esFinal[0] = True
            jsonResultado = json
    elif json['type'] == 'pro':
        #6 8a 9a 9b
        leftJson = False
        rightJson = False
        if 'type' in json['lrel']:
            applied = applyRules(json['rel'], creates, esFinal)
            json['rel'] = applied
            leftJson = True
        if 'type' in json['rrel']:
            applied = applyRules(json['rel'], creates, esFinal)
            json['rel'] = applied
            rightJson = True

        #aplicamos las reglas
        if leftJson == False and rightJson == False:
            #regla 6
            jsonResultado=rulesAR.rule6(json)
        elif leftJson == True and rightJson == False:
            if json['type']['lrel'] == 'pro':
                #aplicamos regla 8a
                jsonResultado = rulesAR.rule8A(json)
            elif json['type']['lrel'] == 'sigma':
                #aplicamos la regla 9a
                jsonResultado = rulesAR.rule9A(json)
        elif leftJson == True and rightJson == True:
                #¿Aplicamos la regla 9b?
                if json['type']['lrel'] == 'sigma' and json['type']['rrel'] == 'sigma':
                    jsonCopia = copy.deepcopy(json)
                    jsonResultado = rulesAR.rule9b(jsonCopia)
                    json = jsonResultado
    elif json['type'] == 'join':
        #7 8b 10a 10b 11a
        leftJson = False
        rightJson = False
        if 'type' in json['lrel']:
            applied = applyRules(json['rel'], creates, esFinal)
            json['rel'] = applied
            leftJson = True
        if 'type' in json['rrel']:
            applied = applyRules(json['rel'], creates, esFinal)
            json['rel'] = applied
            rightJson = True

            # aplicamos las reglas
            if leftJson == False and rightJson == False:
                #aplicamos la regla 7
                jsonResultado=rulesAR.rule7(json)
            elif leftJson == True and rightJson == False:
                if json['lrel']['type'] == 'join':
                    #aplicamos la regla 8b
                    jsonResultado = rulesAR.rule8b(json)
                elif json['lrel']['type'] == 'sigma':
                    #aplicamos la regla 10a
                    jsonCopia = copy.deepcopy(json)
                    jsonResultado = rulesAR.rule10a(jsonCopia)
                    json = jsonResultado
            elif leftJson == True and rightJson == True:
                # ¿Aplicamos la regla 10b?
                if json['lrel']['type'] == 'sigma' and json['rrel']['type'] == 'sigma':
                    jsonCopia = copy.deepcopy(json)
                    jsonResultado = rulesAR.rule10b(jsonCopia)
                    json = jsonResultado
                # ¿Aplicamos la regla 11a?
                elif json['lrel']['type'] == 'pi' and json['rrel']['type'] == 'pi':
                    jsonCopia = copy.deepcopy(json)
                    jsonResultado = rulesAR.rule11a(jsonCopia)
                    json = jsonResultado

    if esFinal[0] == True:
        jsonResultado = json

    return jsonResultado