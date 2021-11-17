import json

#JSON de ejemplo 1
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

#JSON de ejemplo 2
jsonPrueba3Sigmas = {"type": "sigma",
                    "cond": {"type": "eq",
                                  "values": ["edad", 18]
                             },
                    "rel": {"type": "sigma",
                             "cond": {"type": "eq",
                                  "values": ["sexo", "hombre"]
                              },
                             "rel": {"type":"sigma",
                                     "cond": {'type':'eq',
                                              'values':['nombre', 'Juan']
                                              },
                                     'rel':'Personas'
                                     }
                            }
                  }

def rule1(jsonSQL):
    jsonLeft = jsonSQL["cond"]

    valuesObtained = []
    allValues = []

    for i in jsonSQL["rel"]["cond"]['values']:
        valuesObtained.insert(0, i)
    if 'type' in valuesObtained[0]:
        rightResult = valuesObtained
        i = 0
        while i < len(rightResult):
            allValues.insert(0, rightResult[i])
            i += 1
    else:
        rightResult = {'type':'eq','values':valuesObtained}
        allValues.insert(0, rightResult)
    allValues.insert(0, jsonLeft)
    relation = jsonSQL["rel"]["rel"]
    jsonResult = {"type": "sigma", "cond": {
                                            "type": "and",
                                            "values": allValues,
                                            },
                  "rel": relation
                  }
    return jsonResult

if __name__ == '__main__':
    resultado = rule1(jsonPrueba3Sigmas["rel"])
    #resultado es el segundo y tercer, ya que la aplicación de la regla se hace por cada par de sigmas
    jsonPrueba3Sigmas["rel"] = resultado
    print(rule1(json))
    print(rule1(jsonPrueba3Sigmas))
