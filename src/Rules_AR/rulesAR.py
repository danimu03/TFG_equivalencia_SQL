import json

# JSON de ejemplo 1
from tkinter import E

json = {"type": "sigma",
        "cond": {"type": "eq",
                 "values": ["edad", 18]
                 },
        "rel": {"type": "sigma",
                "cond": {"type": "eq",
                         "values": ["sexo", "hombre"]
                         },
                "rel": "Persona"
                }
        }

# JSON de ejemplo 2
jsonPrueba3Sigmas = {"type": "sigma",
                     "cond": {"type": "eq",
                              "values": ["edad", 18]
                              },
                     "rel": {"type": "sigma",
                             "cond": {"type": "eq",
                                      "values": ["sexo", "hombre"]
                                      },
                             "rel": {"type": "sigma",
                                     "cond": {'type': 'eq',
                                              'values': ['nombre', 'Juan']
                                              },
                                     'rel': 'Personas'
                                     }
                             }
                     }

def rule1(jsonSQL):
    try:
        jsonLeft = jsonSQL["cond"]  # Guardamos el Json de 'rel'
        valuesObtained = [] #Guardaremos los values que se encuentran en el JsonLeft
        allValues = [] #Juntaremos los values de JsonLeft + jsonSQL (fuera de rel)

        # Si el segundo sigma, tiene como values un array vacío, eliminamos ese sigma
        if len(jsonSQL["rel"]["cond"]['values']) == 0:
            tieneCond = False
            allValues = jsonSQL['cond']['values']
        else:
            tieneCond = True
            for i in jsonSQL["rel"]["cond"]['values']:
                valuesObtained.insert(0, i) #Guardamos los values que se encuentra en la cond de rel
            if 'type' in valuesObtained[0]: #Si existe 'type', significa que se tienen varias condiciones guardadas
                rightResult = valuesObtained
                i = 0
                while i < len(rightResult):#insertamos en el array de valores, los valores que hemos cogido de 'rel' y los unimos a los del jsonRight
                    allValues.insert(0, rightResult[i])
                    i += 1
            else: #si no existe type, hay que crear el json con la condición (por ahora creamos siempre type:eq)
                rightResult = {'type': 'eq', 'values': valuesObtained}
                allValues.insert(0, rightResult)
            allValues.insert(0, jsonLeft)
        relation = jsonSQL["rel"]["rel"]#guardamos el 'rel' de 'rel' (la tabla)
        #creamos el json resultante
        if tieneCond: #si existía su cond, entonces tiene varias condiciones
            jsonCond = { "type": "and",
                         "values": allValues,
                     }
        else: #si no existía su cond, solo tiene la cond del json de arriba
            jsonCond = { "type": "eq",
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



if __name__ == '__main__':
    resultado = rule1(jsonPrueba3Sigmas["rel"])
    # resultado es el segundo y tercer, ya que la aplicación de la regla se hace por cada par de sigmas
    jsonPrueba3Sigmas["rel"] = resultado
    print(rule1(json))
    print(rule1(jsonPrueba3Sigmas))
