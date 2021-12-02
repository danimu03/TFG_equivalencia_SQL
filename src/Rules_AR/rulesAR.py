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

if __name__ == '__main__':
    jsonSQL = {}
    rule2(jsonSQL)
