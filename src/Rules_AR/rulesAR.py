import json
from tkinter import E
import functools

def rule1(jsonSQL):
    try:
        jsonLeft = jsonSQL["cond"]  # Guardamos el Json de 'rel'
        valuesObtained = []  # Guardaremos los values que se encuentran en el JsonLeft
        allValues = []  # Juntaremos los values de JsonLeft + jsonSQL (fuera de rel)

        # Si el segundo sigma, tiene como values un array vacío, eliminamos ese sigma
        if len(jsonSQL["rel"]["cond"]['values']) == 0:
            tieneCond = False
            allValues = jsonSQL['cond']['values']
        else:
            tieneCond = True
            for i in jsonSQL["rel"]["cond"]['values']:
                valuesObtained.insert(0, i)  # Guardamos los values que se encuentra en la cond de rel
            if 'type' in valuesObtained[0]:  # Si existe 'type', significa que se tienen varias condiciones guardadas
                rightResult = valuesObtained
                i = 0
                while i < len(
                        rightResult):  # insertamos en el array de valores, los valores que hemos cogido de 'rel' y los unimos a los del jsonRight
                    allValues.insert(0, rightResult[i])
                    i += 1
            else:  # si no existe type, hay que crear el json con la condición (por ahora creamos siempre type:eq)
                rightResult = {'type': 'eq', 'values': valuesObtained}
                allValues.insert(0, rightResult)
            allValues.insert(0, jsonLeft)
        relation = jsonSQL["rel"]["rel"]  # guardamos el 'rel' de 'rel' (la tabla)
        # creamos el json resultante
        if tieneCond:  # si existía su cond, entonces tiene varias condiciones
            jsonCond = {"type": "and",
                        "values": allValues,
                        }
        else:  # si no existía su cond, solo tiene la cond del json de arriba
            jsonCond = {"type": "eq",
                        "values": allValues,
                        }
        jsonResult = {"type": "sigma",
                      "cond": jsonCond,
                      "rel": relation
                      }
        return jsonResult
    except:
        raise TypeError('No se puede aplicar esta regla porque algún campo está vacío')
        jsonResult = {}
        return jsonResult


def rule2(jsonSQL):
    # arrays necesarios para ordenar los valores alafabéticamente (primero, por separado)
    # consideramos que los valores del array values no están ordenados alfabéticamente

    valuesArriba = []
    valuesAbajo = []
    numValuesUp = 1
    numValuesDown = 1

    valuesArriba = jsonSQL['cond']['values']
    valuesAbajo = jsonSQL['rel']['cond']['values']


    if jsonSQL['cond']['type'] == 'and':
        numValuesUp = len(valuesArriba)
        for n in jsonSQL['cond']['values']:
            valuesCopia = n['values']
            sort_pair(valuesCopia)
    else:
        # ordenamos los valuesArriba
        sort_pair(valuesArriba)

    if jsonSQL['rel']['cond']['type'] == 'and':
        numValuesDown = len(valuesAbajo)
        for n in jsonSQL['rel']['cond']['values']:
            valuesCopia = n['values']
            sort_pair(valuesCopia)
    else:
    # ordenamos los valuesAbajo
        sort_pair(valuesAbajo)

    jsonSQL['cond']['values'] = valuesArriba
    jsonSQL['rel']['cond']['values'] = valuesAbajo

    valuesUpOrdenados = jsonSQL['cond']
    valuesDownOrdenados = jsonSQL['rel']['cond']

    if numValuesUp == 1 and numValuesDown == 1:
        valuesOrdenados = sorted([valuesUpOrdenados, valuesDownOrdenados], key=functools.cmp_to_key(compare_values))
        jsonSQL['cond'] = valuesOrdenados[0]
        jsonSQL['rel']['cond'] = valuesOrdenados[1]
    else:
        valuesAux = []
        if numValuesUp > 1:
            for n in valuesUpOrdenados['values']:
                valuesAux.append(n)
        else:
            valuesAux.append(valuesUpOrdenados)
        if numValuesDown > 1:
            for n in valuesDownOrdenados['values']:
                valuesAux.append(n)
        else:
            valuesAux.append(valuesDownOrdenados)
        valuesOrdenados = sorted(valuesAux, key=functools.cmp_to_key(compare_values))
        i = 0
        if numValuesUp > 1:
            jsonSQL['cond']['values'] = []
            j = 0
            while j < numValuesUp:
                jsonSQL['cond']['values'].append(valuesOrdenados[i])
                i = i+1
                j = j+1
        else:
            jsonSQL['cond'] = valuesOrdenados[0]
            i = 1
        if numValuesDown > 1:
            jsonSQL['rel']['cond']['values'] = []
            j = 0
            while j < numValuesDown:
                jsonSQL['rel']['cond']['values'].append(valuesOrdenados[i])
                i = i+1
                j = j+1


    return jsonSQL

def rule3(jsonSQL):

    relation = jsonSQL['rel']['rel']
    jsonSQL['rel'] = relation

    return jsonSQL

def rule4(jsonSQL):

    valuesPi = jsonSQL
    valuesSigma = jsonSQL['rel']
    relation = jsonSQL['rel']['rel']

    if 'values' in valuesSigma['cond']:
        valuesSigma['cond']['values'].sort()
    jsonSQL = valuesSigma
    jsonSQL['rel'] = valuesPi
    jsonSQL['rel']['rel'] = relation

    return jsonSQL

def rule5A(jsonSQL):

    valuesPro = jsonSQL['rel']
    valuesCondSigma = jsonSQL['cond']

    if 'type' in valuesCondSigma:
        for i in valuesCondSigma['values']:
            sort_pair(i['values'])
        valuesCondSigmaOrdenados = sorted(valuesCondSigma['values'], key=functools.cmp_to_key(compare_values))
        valuesCondSigma = {'type':'and',
                           'values':valuesCondSigmaOrdenados}

    jsonSQL = { "type" : "join",
                "cond" : valuesCondSigma,
                "lrel" : valuesPro["lrel"],
                "rrel" : valuesPro["rrel"]
    }

    return jsonSQL

def rule5B(jsonSQL):

    valuesCondSigma = jsonSQL['cond']
    sort_pair(valuesCondSigma['values'])
    valuesJoin = jsonSQL['rel']
    leftRel = valuesJoin["lrel"]
    rightRel = valuesJoin["rrel"]

    if 'type' in valuesJoin['cond'] and valuesJoin['cond']['type'] == 'and':
        newCond = valuesJoin['cond']['values']
        mediumValues = [valuesCondSigma]
        for i in newCond:
            mediumValues.append(i)
        finalValues = sorted(mediumValues, key=functools.cmp_to_key(compare_values))
        jsonAnd = {"type": "and",
                   "values": finalValues
                   }
    else:
        jsonAnd = {"type": "and",
                   "values": [valuesCondSigma, valuesJoin['cond']]
                   }

    jsonSQL = { "type" : "join",
                "cond" : jsonAnd,
                "lrel" : leftRel,
                "rrel" : rightRel
    }
    return jsonSQL

def rule6(jsonSQL):
    right = jsonSQL['rrel']['table']
    left = jsonSQL['lrel']['table']

    left['ren'].sort()
    right['ren'].sort()

    sortedVals = sorted([right, left], key=functools.cmp_to_key(compare_values))

    jsonSQL['rrel'] = sortedVals[0]
    jsonSQL['lrel'] = sortedVals[1]
    return jsonSQL

def rule7(jsonSQL):
    right = jsonSQL['rrel']['table']
    left = jsonSQL['lrel']['table']

    left['ren'].sort()
    right['ren'].sort()

    sortedVals = sorted([right, left], key=functools.cmp_to_key(compare_values))

    jsonSQL['rrel'] = sortedVals[0]
    jsonSQL['lrel'] = sortedVals[1]
    return jsonSQL

def rule8A(jsonSQL):

    left_left = jsonSQL['lrel']['lrel']
    left_right = jsonSQL['lrel']['rrel']
    right = jsonSQL['rrel']
    aux = jsonSQL['lrel']

    jsonSQL['lrel'] = left_left
    jsonSQL['rrel'] = aux
    jsonSQL['rrel']['lrel'] = left_right
    jsonSQL['rrel']['rrel'] = right
    return jsonSQL

def rule8B(jsonSQL):

    left_left = jsonSQL['lrel']['lrel']
    left_right = jsonSQL['lrel']['rrel']
    right = jsonSQL['rrel']

    json = {"type": "join",
            "cond": {},
            "lrel": "",
            "rrel": ""
            }
    #Comprobamos si existe algún and en la condición
    if 'type' in jsonSQL['cond'] and jsonSQL['cond']['type'] == 'and':
        '''cond'''
        values_cond = jsonSQL['cond']['values']
        values_left_first = jsonSQL['lrel']['cond']['values'][0]
        values_left_second = jsonSQL['lrel']['cond']['values'][1]
        values_cond.append(values_left_second)
        valuesOrdenados = sorted(values_cond, key=functools.cmp_to_key(compare_values))

        '''lrel = left_left'''
        '''rrel'''
        json_right = {
             "type": "join",
             "cond": {},
             "lrel": "",
             "rrel": ""
        }
        json_right['cond'] = values_left_first
        json_right['lrel'] = left_right
        json_right['rrel'] = right
        '''resultado'''
        json['cond'] = { "type": "and",
                         "values": valuesOrdenados
        }
        json['lrel'] = left_left
        json['rrel'] = json_right
    else:
        '''cond'''
        values_cond = jsonSQL['cond']
        values_left_first = jsonSQL['lrel']['cond']['values'][0]
        values_left_second = jsonSQL['lrel']['cond']['values'][1]
        values_and = []
        values_and.append(values_left_second)
        values_and.append(values_cond)
        valuesOrdenados = sorted(values_and, key=functools.cmp_to_key(compare_values))

        '''lrel = left_left'''
        '''rrel'''
        json_right = {
             "type": "join",
             "cond": {},
             "lrel": "",
             "rrel": ""
        }
        json_right['cond'] = values_left_first
        json_right['lrel'] = left_right
        json_right['rrel'] = right
        '''resultado'''
        json['cond'] = { "type": "and",
                         "values": valuesOrdenados
        }
        json['lrel'] = left_left
        json['rrel'] = json_right

    return json

def rule9A(jsonSQL):

    valuesLeft = jsonSQL['lrel']
    valuesRigth = jsonSQL['rrel']
    tableLeft = valuesLeft['rel']

    valuesLeft['rel'] = valuesRigth
    jsonSQL['lrel'] = tableLeft
    jsonSQL['rrel'] = valuesLeft

    return jsonSQL

def rule9B(jsonSQL, creates):

    #comprobamos si hay que aplicar la regla
    #los valores del sigma de los rel deben de pertenecer a distintas tablas
    tipoCadena = str(type('cadena'))
    tipo1 = str(type(jsonSQL['lrel']['cond']['values'][0]))
    tipo2 = str(type(jsonSQL['rrel']['cond']['values'][0]))

    if tipo1 == tipoCadena and '.' in jsonSQL['lrel']['cond']['values'][0]:
        value1 = jsonSQL['lrel']['cond']['values'][0].split('.')
    else:
        value1 = jsonSQL['lrel']['cond']['values'][1].split('.')

    if tipo2 == tipoCadena and '.' in jsonSQL['rrel']['cond']['values'][0]:
        value2 = jsonSQL['rrel']['cond']['values'][0].split('.')
    else:
        value2 = jsonSQL['rrel']['cond']['values'][0].split('.')

    tipo1tabla1 = False
    tipo1tabla2 = False
    tipo2tabla1 = False
    tipo2tabla2 = False

    nombreTabla1 = value1[0][:-1]
    nombreTabla2 = value2[0][:-1]

    for table in creates:
        if table['name'] == nombreTabla1:
            for column in table['columns']:
                if column['name'] == value1[1]:
                    tipo1tabla1 = True
                if column['name'] == value2[1]:
                    tipo2tabla1 = True
        if table['name'] == nombreTabla2:
            for column in table['columns']:
                if column['name'] == value1[1]:
                    tipo1tabla2 = True
                if column['name'] == value2[1]:
                    tipo2tabla2 = True

    if tipo1tabla1 == True and tipo1tabla2 == False and tipo2tabla1 == False and tipo2tabla2 == True:
        leftRel = jsonSQL['lrel']['rel']
        rightRel = jsonSQL['rrel']['rel']
        leftCond = jsonSQL['lrel']['cond']
        rightCond = jsonSQL['rrel']['cond']
        sort_pair(leftCond['values'])
        sort_pair(rightCond['values'])
        newValues = [leftCond, rightCond]
        valuesOrdenados = sorted(newValues, key=functools.cmp_to_key(compare_values))
        res = {'type' : 'sigma',
               'cond' : {'type' : 'eq',
                         'values' : valuesOrdenados
                        },
               'rel' : {'type' : 'pro',
                        'lrel' : leftRel,
                        'rrel' : rightRel
                       }
               }
        return res
    else:
        return jsonSQL


def rule10A(jsonSQL, creates):

    # comprobamos si hay que aplicar la regla
    # los valores del sigma de los rel deben de pertenecer a distintas tablas
    tipoCadena = str(type('cadena'))
    tipo1 = str(type(jsonSQL['lrel']['cond']['values'][0]))

    if tipo1 == tipoCadena and '.' in jsonSQL['lrel']['cond']['values'][0]:
        value1 = jsonSQL['lrel']['cond']['values'][0].split('.')
    else:
        value1 = jsonSQL['lrel']['cond']['values'][1].split('.')

    tipo1tabla = False
    tipo1otraTabla = False

    nombreTabla1 = value1[0][:-1]

    for table in creates:
        if table['name'] == nombreTabla1:
            for column in table['columns']:
                if column['name'] == value1[1]:
                    tipo1tabla = True
        else:
            for column in table['columns']:
                if column['name'] == value1[1]:
                    tipo1otraTabla = True

    if tipo1tabla == True and tipo1otraTabla == False:
        generalCond = jsonSQL['cond']
        sort_pair(generalCond['values'])
        leftRel = jsonSQL['lrel']
        sort_pair(leftRel['cond']['values'])
        rightRel = jsonSQL['rrel']
        lrelRel = jsonSQL['lrel']['rel']

        res = leftRel
        res['rel'] = {'type':'join',
                      'cond':generalCond,
                      'lrel':lrelRel,
                      'rrel':rightRel
                      }
        return res
    else:
        return jsonSQL

def rule10B(jsonSQL, creates):
    # comprobamos si hay que aplicar la regla
    # los valores del sigma de los rel deben de pertenecer a distintas tablas
    tipoCadena = str(type('cadena'))
    tipo1 = str(type(jsonSQL['lrel']['cond']['values'][0]))
    tipo2 = str(type(jsonSQL['rrel']['cond']['values'][0]))

    if tipo1 == tipoCadena and '.' in jsonSQL['lrel']['cond']['values'][0]:
        value1 = jsonSQL['lrel']['cond']['values'][0].split('.')
    else:
        value1 = jsonSQL['lrel']['cond']['values'][1].split('.')

    if tipo2 == tipoCadena and '.' in jsonSQL['rrel']['cond']['values'][0]:
        value2 = jsonSQL['rrel']['cond']['values'][0].split('.')
    else:
        value2 = jsonSQL['rrel']['cond']['values'][0].split('.')

    tipo1tabla1 = False
    tipo1tabla2 = False
    tipo2tabla1 = False
    tipo2tabla2 = False

    nombreTabla1 = value1[0][:-1]
    nombreTabla2 = value2[0][:-1]

    for table in creates:
        if table['name'] == nombreTabla1:
            for column in table['columns']:
                if column['name'] == value1[1]:
                    tipo1tabla1 = True
                if column['name'] == value2[1]:
                    tipo2tabla1 = True
        if table['name'] == nombreTabla2:
            for column in table['columns']:
                if column['name'] == value1[1]:
                    tipo1tabla2 = True
                if column['name'] == value2[1]:
                    tipo2tabla2 = True

    if tipo1tabla1 == True and tipo1tabla2 == False and tipo2tabla1 == False and tipo2tabla2 == True:
        condLeft = jsonSQL['lrel']['cond']
        sort_pair(condLeft['values'])
        relLeft = jsonSQL['lrel']['rel']
        condRight = jsonSQL['rrel']['cond']
        sort_pair(condRight['values'])
        relRight = jsonSQL['rrel']['rel']
        condGeneral = jsonSQL['cond']

        newValues = [condLeft, condRight]
        valuesOrdenados = sorted(newValues, key=functools.cmp_to_key(compare_values))

        res = {'type':'sigma',
               'cond': {'type':'and',
                        'values':valuesOrdenados
                        },
               'rel':{'type':'join',
                      'cond': condGeneral,
                       'lrel':relLeft,
                       'rrel':relRight
                      },
               }
        return res
    else:
        return jsonSQL


def rule11A(jsonSQL, creates):
    # comprobamos si hay que aplicar la regla
    # los valores del pi de los rel deben de pertenecer a distintas tablas
    value1 = jsonSQL['lrel']['proj'][0].split('.')
    value2 = jsonSQL['rrel']['proj'][0].split('.')


    tipo1tabla1 = False
    tipo1tabla2 = False
    tipo2tabla1 = False
    tipo2tabla2 = False

    nombreTabla1 = value1[0][:-1]
    nombreTabla2 = value2[0][:-1]

    for table in creates:
        if table['name'] == nombreTabla1:
            for column in table['columns']:
                if column['name'] == value1[1]:
                    tipo1tabla1 = True
                if column['name'] == value2[1]:
                    tipo2tabla1 = True

        if table['name'] == nombreTabla2:
            for column in table['columns']:
                if column['name'] == value1[1]:
                    tipo1tabla2 = True
                if column['name'] == value2[1]:
                    tipo2tabla2 = True

    if tipo1tabla1 == True and tipo1tabla2 == False and tipo2tabla1 == False and tipo2tabla2 == True:

        newProj = []
        newProj.append(jsonSQL['lrel']['proj'][0])
        newProj.append(jsonSQL['rrel']['proj'][0])
        jsonJoin = {'type':'join',
                    'cond': jsonSQL['cond'],
                    'lrel': jsonSQL['lrel']['rel'],
                    'rrel': jsonSQL['rrel']['rel']
                    }
        newJson = {'type': 'pi',
                   'proj': newProj,
                   'rel': jsonJoin
                   }
        return newJson
    else:
        return jsonSQL

def rule11B(jsonSQL, creates):
    # comprobamos si hay que aplicar la regla
    # los valores del pi de los rel deben de pertenecer a distintas tablas
    value1original = jsonSQL['proj'][0]
    value2original = jsonSQL['proj'][1]
    value1 = jsonSQL['proj'][0].split('.')
    value2 = jsonSQL['proj'][1].split('.')

    if value1original in jsonSQL['rel']['lrel']['proj']:
        if jsonSQL['rel']['lrel']['proj'][0] == value1original:
            value3 = jsonSQL['rel']['lrel']['proj'][1].split('.')
        else:
            value3 = jsonSQL['rel']['lrel']['proj'][0].split('.')
        if jsonSQL['rel']['rrel']['proj'][0] == value2original:
            value4 = jsonSQL['rel']['rrel']['proj'][1].split('.')
        else:
            value4 = jsonSQL['rel']['rrel']['proj'][0].split('.')
    else:
        if jsonSQL['rel']['lrel']['proj'][0] == value2original:
            value4 = jsonSQL['rel']['lrel']['proj'][1].split('.')
        else:
            value4 = jsonSQL['rel']['lrel']['proj'][0].split('.')
        if jsonSQL['rel']['rrel']['proj'][0] == value1original:
            value3 = jsonSQL['rel']['rrel']['proj'][1].split('.')
        else:
            value3 = jsonSQL['rel']['rrel']['proj'][0].split('.')

    if value1 != value3 and value2 != value4:
        tipo1tabla1 = False
        tipo1tabla2 = False
        tipo2tabla1 = False
        tipo2tabla2 = False
        tipo3tabla1 = False
        tipo3tabla2 = False
        tipo4tabla1 = False
        tipo4tabla2 = False

        nombreTabla1 = value1[0][:-1]
        nombreTabla2 = value2[0][:-1]

        for table in creates:
            if table['name'] == nombreTabla1:
                for column in table['columns']:
                    if column['name'] == value1[1]:
                        tipo1tabla1 = True
                    if column['name'] == value2[1]:
                        tipo2tabla1 = True
                    if column['name'] == value3[1]:
                        tipo3tabla1 = True
                    if column['name'] == value4[1]:
                        tipo4tabla1 = True
            if table['name'] == nombreTabla2:
                for column in table['columns']:
                    if column['name'] == value1[1]:
                        tipo1tabla2 = True
                    if column['name'] == value2[1]:
                        tipo2tabla2 = True
                    if column['name'] == value3[1]:
                        tipo3tabla2 = True
                    if column['name'] == value4[1]:
                        tipo4tabla2 = True

        if tipo1tabla1 == True and tipo1tabla2 == False and tipo2tabla1 == False and tipo2tabla2 == True and \
                tipo3tabla1 == True and tipo3tabla2 == False and tipo4tabla1 == False and tipo4tabla2 == True:

            newRel = {'type': 'join',
                      'cond': jsonSQL['rel']['cond'],
                      'lrel': jsonSQL['rel']['lrel']['rel'],
                      'rrel': jsonSQL['rel']['rrel']['rel'],
                      }
            jsonSQL['rel'] = newRel
            return jsonSQL
        else:
            return jsonSQL
    else:
        return jsonSQL

def compare_values(json1, json2):
    # esta función es solo para comparar diccionarios, los pares ya nos vienen ordenados

    if json1['type'] == 'rho':
        values1 = json1['ren']
        values2 = json2['ren']
    else:
        values1 = json1['values']
        values2 = json2['values']

    tipo1 = str(type(values1[0]))
    tipo2 = str(type(values2[0]))

    if tipo1 == tipo2:
        if values1[0] > values2[0]:
            return 1
        elif values1[0] < values2[0]:
            return -1
        else:
            tipo12 = str(type(values1[1]))
            tipo22 = str(type(values2[1]))

            if tipo12 == tipo22:
                if values1[1] > values2[1]:
                    return 1
                elif values1[1] < values2[1]:
                    return -1
                else:
                    return 0
            else:
                if tipo12 > tipo22:
                    return 1
                elif tipo12 < tipo22:
                    return -1
                else:
                    return 0
    else:
        if tipo1 > tipo2:
            return 1
        elif tipo1 < tipo2:
            return -1
        else:
            tipo12 = str(type(values1[1]))
            tipo22 = str(type(values2[1]))

            if tipo12 == tipo22:
                if values1[1] > values2[1]:
                    return 1
                elif values1[1] < values2[1]:
                    return -1
                else:
                    return 0
            else:
                if tipo12 > tipo22:
                    return 1
                elif tipo12 < tipo22:
                    return -1
                else:
                    return 0

def sort_pair(values):
    tipo1 = str(type(values[0]))
    tipo2 = str(type(values[1]))
    if tipo1 == tipo2:
        values.sort()
    else:
        if tipo2 < tipo1:
            aux = values[0]
            values[0] = values[1]
            values[1] = aux



if __name__ == '__main__':
    jsonSQL = {}
    rule2(jsonSQL)
