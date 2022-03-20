import json
from tkinter import E


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

    valuesArriba = jsonSQL['cond']['values']
    valuesAbajo = jsonSQL['rel']['cond']['values']

    # ordenamos los valuesArriba
    tipo1 = str(type(valuesArriba[0]))
    tipo2 = str(type(valuesArriba[1]))
    if tipo1 == tipo2:
        valuesArriba.sort()
    else:
        if tipo2 < tipo1:
            aux = valuesArriba[0]
            valuesArriba[0] = valuesArriba[1]
            valuesArriba[1] = aux

    # ordenamos los valuesAbajo
    tipo1 = str(type(valuesAbajo[0]))
    tipo2 = str(type(valuesAbajo[1]))
    if tipo1 == tipo2:
        valuesAbajo.sort()
    else:
        if tipo2 < tipo1:
            aux = valuesAbajo[0]
            valuesAbajo[0] = valuesAbajo[1]
            valuesAbajo[1] = aux

    tipo1 = str(type(valuesArriba[0]))
    tipo2 = str(type(valuesAbajo[0]))
    if tipo1 == tipo2:
        if valuesAbajo[0] < valuesArriba[0]:
            jsonSQL['cond']['values'] = valuesAbajo
            jsonSQL['rel']['cond']['values'] = valuesArriba
    else:
        if tipo2 < tipo1:
            jsonSQL['cond']['values'] = valuesAbajo
            jsonSQL['rel']['cond']['values'] = valuesArriba

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
        json_right = { "type": "join",
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




if __name__ == '__main__':
    jsonSQL = {}
    rule2(jsonSQL)
