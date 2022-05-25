import src.Rules_AR.rulesAR as rulesAR
import src.SQL_To_JSON.Sql_To_Json as sqlJSON
import src.Creates_To_JSON.Creates_Json as createsJSON
import copy
import itertools
import functools

def equivalence(query_sql1,query_sql2, query_ddl):
    soluciones = ['Equivalentes', 'No sabemos', 'Equivalentes salvo renombramiento']
    try:

        # si tenemos una sentencia de creacion de tablas, la parseamos tambien
        creates = createsJSON.create_tables_json(query_ddl)

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

        while final1[0] == False:
            json1rulesApplied = applyRules(json1rulesApplied, None, final1)

        while final2[0] == False:
            json2rulesApplied = applyRules(json2rulesApplied, None, final2)

        if json1rulesApplied == json2rulesApplied:
            return soluciones[0]
        else:
            if permuteRenames(json1rulesApplied, json2rulesApplied):
                return soluciones[2]
            else:
                return soluciones[1]
    except Exception as e:
        print(e)


    return soluciones[1]


def applyRules(json, creates, esFinal):
    jsonResultado = {}
    if json['type'] == 'sigma':
        if 'type' in json['rel']:
            jsonCopia = copy.deepcopy(json['rel'])
            json['rel'] = applyRules(jsonCopia, creates, esFinal)
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
            jsonCopia = copy.deepcopy(json['rel'])
            json['rel'] = applyRules(jsonCopia, creates, esFinal)
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
                        jsonResultado=rulesAR.rule11B(json, creates)
                else:
                    jsonResultado = json
                json['proj'].sort()
        else:
            esFinal[0] = True
            jsonResultado = json
    elif json['type'] == 'pro':
        #6 8a 9a 9b
        leftJson = False
        rightJson = False
        if 'type' in json['lrel']:
            jsonCopia = copy.deepcopy(json['lrel'])
            json['lrel'] = applyRules(jsonCopia, creates, esFinal)
            leftJson = True
        if 'type' in json['rrel']:
            jsonCopia = copy.deepcopy(json['rrel'])
            json['rrel'] = applyRules(jsonCopia, creates, esFinal)
            rightJson = True

        #aplicamos las reglas
        if leftJson == True and rightJson == True:
            #¿Aplicamos la regla 9b?
            if json['lrel'] ['type']== 'sigma' and json['rrel']['type'] == 'sigma':
                jsonCopia = copy.deepcopy(json)
                jsonResultado = rulesAR.rule9B(jsonCopia, creates)
                json = jsonResultado
            elif json['lrel'] ['type'] == 'rel' and json['rrel']['type'] == 'rel':
                # regla 6
                jsonResultado = rulesAR.rule6(json)
            elif json['lrel'] ['type'] == 'pro' and json['rrel']['type'] == 'rel':
                #aplicamos regla 8a
                jsonResultado = rulesAR.rule8A(json)
            elif json['lrel']['type'] == 'sigma' and json['rrel']['type'] == 'rel':
                #aplicamos la regla 9a
                jsonResultado = rulesAR.rule9A(json, creates)
    elif json['type'] == 'join':
        #7 8b 10a 10b 11a
        json['cond']['values'].sort()
        leftJson = False
        rightJson = False
        if 'type' in json['lrel']:
            jsonCopia = copy.deepcopy(json['lrel'])
            json['lrel'] = applyRules(jsonCopia, creates, esFinal)
            leftJson = True
        if 'type' in json['rrel']:
            jsonCopia = copy.deepcopy(json['rrel'])
            json['rrel'] = applyRules(jsonCopia, creates, esFinal)
            rightJson = True

        # aplicamos las reglas
        if leftJson == True and rightJson == True:
            # ¿Aplicamos la regla 10b?
            if json['lrel']['type'] == 'sigma' and json['rrel']['type'] == 'sigma':
                jsonCopia = copy.deepcopy(json)
                jsonResultado = rulesAR.rule10B(jsonCopia, creates)
                json = jsonResultado
            # ¿Aplicamos la regla 11a?
            elif json['lrel']['type'] == 'pi' and json['rrel']['type'] == 'pi':
                jsonCopia = copy.deepcopy(json)
                jsonResultado = rulesAR.rule11A(jsonCopia, creates)
                json = jsonResultado
            elif json['lrel']['type'] == 'rel' and json['rrel']['type'] == 'rel':
                # regla 6
                jsonResultado = rulesAR.rule7(json)
            elif json['lrel']['type'] == 'join' and json['rrel']['type'] == 'rel':
                # aplicamos la regla 8b
                jsonResultado = rulesAR.rule8B(json)
            elif json['lrel']['type'] == 'sigma' and json['rrel']['type'] == 'rel':
                # aplicamos la regla 10a
                jsonCopia = copy.deepcopy(json)
                jsonResultado = rulesAR.rule10A(jsonCopia, creates)
                json = jsonResultado

    elif json['type'] == 'rho' or (json['type'] == 'rel' and 'table' in json):
        esFinal[0] = True

    if not jsonResultado:
        jsonResultado = json

    return jsonResultado

def getRenames(json, renames):
    if json['type'] == 'sigma':
        if 'type' in json['rel'] or json['rel']['type'] != 'rel':
            getRenames(json['rel'], renames)
        else:
            renames.append(json['rel']['table']['ren'])
    elif json['type'] == 'pi':
        if 'type' in json['rel'] or json['rel']['type'] != 'rel':
            getRenames(json['rel'], renames)
        else:
            renames.append(json['rel']['table']['ren'])
    elif json['type'] == 'pro':
        if 'type' in json['lrel'] or json['lrel']['type'] != 'rel':
            getRenames(json['lrel'], renames)
        else:
            renames.append(json['lrel']['table']['ren'])
        if 'type' in json['rrel'] or json['rrel']['type'] != 'rel':
            getRenames(json['rrel'], renames)
        else:
            renames.append(json['rrel']['table']['ren'])
    elif json['type'] == 'join':
        if 'type' in json['lrel'] or json['lrel']['type'] != 'rel':
            getRenames(json['lrel'], renames)
        else:
            renames.append(json['lrel']['table']['ren'])
        if 'type' in json['rrel'] or json['rrel']['type'] != 'rel':
            getRenames(json['rrel'], renames)
        else:
            renames.append(json['rrel']['table']['ren'])
    elif json['type'] == 'rel':
        renames.append(json['table']['ren'])
    elif json['type'] == 'rho':
        renames.append(json['ren'])


def getPermutations(renames):
    return list(itertools.permutations(renames))

def groupRenames(renames, renamesFound):
    possibleRenames = []
    for i in renames:
        actualRenames = []
        for j in renames:
            if i != j:
                if i[0] == j[0] and i[0] not in renamesFound:
                    if i[1] not in actualRenames:
                        actualRenames.append(i[1])
                    if j[1] not in actualRenames:
                        actualRenames.append(j[1])
        if len(actualRenames) > 0:
            renamesFound.append(i[0])
            possibleRenames.append(actualRenames)
    return possibleRenames


#auion2, avion1 -- avion1, avion2    TABLA AVION
#vuelo1, vuelo2 -- vuelo2, vuelo1    TABLA VUELO
#Hay que ir haciendo el rename de cada tabla con cada posible combinación
#Deberíamos hacer el rename de la tabla0, en la posición 0, y luego por debajo, el rename 0 de la tabla 1, y el rename 1 de la tabla1
#si no coincide, volvemos a la tabla 0, y hacemos su rename 1, y luego por debajo, el rename 0 de la tabla 1, y el rename 1 de la tabla 1
def recorrerDiccionario(json, jsonEquivalence, allRenames, tablesFound, permuted, tablaActual, posicionActual, equivalentes):
    if equivalentes[0] == False:
        for (key, val) in json.items():
            if type(val) is dict:
                recorrerDiccionario(val, jsonEquivalence, allRenames, tablesFound, permuted, tablaActual, posicionActual, equivalentes)
            elif type(val) is list:
                if type(val[0]) is dict:
                    for i in val:
                        recorrerDiccionario(i, jsonEquivalence, allRenames, tablesFound, permuted, tablaActual, posicionActual, equivalentes)
                else:
                    if posicionActual != 0 or tablaActual != 0:
                        if val[0].find('.') != -1:
                            aux = val[0].split('.')
                            thisRename = aux[0]
                            pos = 0
                            for r in allRenames[tablaActual]:
                                if r == thisRename:
                                    finalRename = permuted[tablaActual][posicionActual][pos]
                                    finalRename += '.' + aux[1]
                                    val[0] = finalRename
                                pos = pos + 1
                        if val[1].find('.') != -1:
                            aux = val[1].split('.')
                            thisRename = aux[0]
                            pos = 0
                            for r in allRenames[tablaActual]:
                                if r == thisRename:
                                    finalRename = permuted[tablaActual][posicionActual][pos]
                                    finalRename += '.' + aux[1]
                                    val[1] = finalRename
                                pos = pos + 1
                        if val[0] == tablesFound[tablaActual]:
                            thisRename = val[1]
                            pos = 0
                            for r in allRenames[tablaActual]:
                                if r == thisRename:
                                    finalRename = permuted[tablaActual][posicionActual][pos]
                                    val[1] = finalRename
                                pos = pos + 1
                        if val[1] == tablesFound[tablaActual]:
                            thisRename = val[0]
                            pos = 0
                            for r in allRenames[tablaActual]:
                                if r == thisRename:
                                    finalRename = permuted[tablaActual][posicionActual][pos]
                                    val[0] = finalRename
                                pos = pos + 1
        tablaActual = tablaActual + 1
        if tablaActual < len(tablesFound):
            posicionActual = 0
            while posicionActual < len(allRenames[tablaActual]) and equivalentes[0] == False:
                recorrerDiccionario(json, jsonEquivalence, allRenames, tablesFound, permuted, tablaActual, posicionActual, equivalentes)
                posicionActual = posicionActual + 1
        if json == jsonEquivalence:
            equivalentes[0] = True



def permuteRenames(jsonToPermute, jsonEquivalente):
    renames = []
    getRenames(jsonToPermute, renames)
    permuted = []
    tablesFound = []
    allRenames = groupRenames(renames, tablesFound)
    for i in allRenames:
        permuted.append(getPermutations(i))
    jsonCopia = copy.deepcopy(jsonToPermute)
    equivalentes = [False]
    posicionActual = 0
    tablaActual = 0

    while posicionActual < len(allRenames[tablaActual]) and equivalentes[0] == False:
        recorrerDiccionario(jsonCopia, jsonEquivalente, allRenames, tablesFound, permuted, tablaActual, posicionActual,
                                     equivalentes)
        posicionActual = posicionActual + 1

    if equivalentes[0]:
        return True
    else:
        return False


