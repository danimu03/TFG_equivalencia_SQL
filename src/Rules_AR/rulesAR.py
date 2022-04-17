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


    jsonSQL = { "type" : "join",
                "cond" : valuesCondSigma,
                "lrel" : valuesPro["lrel"],
                "rrel" : valuesPro["rrel"]
    }

    return jsonSQL

def rule5B(jsonSQL):

    valuesCondSigma = jsonSQL['cond']
    valuesJoin = jsonSQL['rel']
    leftRel = valuesJoin["lrel"]
    rightRel = valuesJoin["rrel"]

    if 'type' in valuesJoin['cond'] and valuesJoin['cond']['type'] == 'and':
        newCond = valuesJoin['cond']['values']
        finalValues = [valuesCondSigma]
        for i in newCond:
            finalValues.append(i)
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
    right = jsonSQL['rrel']
    left = jsonSQL['lrel']

    jsonSQL['rrel'] = left
    jsonSQL['lrel'] = right
    return jsonSQL

def rule7(jsonSQL):
    right = jsonSQL['rrel']
    left = jsonSQL['lrel']

    jsonSQL['rrel'] = left
    jsonSQL['lrel'] = right
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

#TODO
def rule8B(jsonSQL):

    left_left = jsonSQL['lrel']['lrel   ']
    left_right = jsonSQL['lrel']['rrel']
    right = jsonSQL['rrel']

    json = {"type": "join",
            "cond": {},
            "lrel": "",
            "rrel": ""
            }
    #hay un and en el primer cond (FALTA COMPROBAR EL RESTO DE CONDS)
    if 'type' in jsonSQL['cond'] and jsonSQL['cond']['type'] == 'and':
        '''cond'''
        values_cond = jsonSQL['cond']['values']
        values_left_first = jsonSQL['lrel']['cond']['values'][0]
        values_left_second = jsonSQL['lrel']['cond']['values'][1]
        values_cond.append(values_left_second)
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
                         "values": values_cond
        }
        json['lrel'] = left_left
        json['rrel'] = json_right
    else:
        cond = jsonSQL['cond']
        left_cond = jsonSQL['lrel']['cond']
        aux = jsonSQL['lrel']
        aux_values = jsonSQL['lrel']['cond']['values'][0]

        jsonSQL['cond']['values'][0] = cond
        jsonSQL['cond'] = left_cond
        jsonSQL['rrel']['cond'] = aux_values
        jsonSQL['lrel'] = left_left
        jsonSQL['rrel'] = aux
        jsonSQL['rrel']['lrel'] = left_right
        jsonSQL['rrel']['rrel'] = right
        json = jsonSQL

    return json

''''def rule8B(jsonSQL):

    cond = jsonSQL['cond']
    left_cond = jsonSQL['lrel']['cond']
    left_left = jsonSQL['lrel']['lrel']
    left_right = jsonSQL['lrel']['rrel']
    right = jsonSQL['rrel']
    aux = jsonSQL['lrel']
    aux_values = jsonSQL['lrel']['cond']['values'][0]

    if 'type' in cond and cond['type'] == 'and':
        newCond = cond['values']
        finalValues = left_cond['values']
        for i in newCond:
            finalValues.append(i)
        jsonAnd = {"type": "and",
                   "values": finalValues
                   }
    else:
        jsonSQL['cond']['values'][0] = cond
        jsonSQL['cond'] = left_cond
        jsonSQL['rrel']['cond'] = aux_values

    jsonSQL['lrel'] = left_left
    jsonSQL['rrel'] = aux
    jsonSQL['rrel']['lrel'] = left_right
    jsonSQL['rrel']['rrel'] = right
    return jsonSQL'''''

def rule9A(jsonSQL):

    valuesLeft = jsonSQL['lrel']
    valuesRigth = jsonSQL['rrel']
    tableLeft = valuesLeft['rel']

    valuesLeft['rel'] = valuesRigth
    jsonSQL['lrel'] = tableLeft
    jsonSQL['rrel'] = valuesLeft

    return jsonSQL

def compare_values(json1, json2):
    # esta función es solo para comparar diccionarios, los pares ya nos vienen ordenados

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
