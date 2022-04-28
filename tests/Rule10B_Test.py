import unittest
import src.Creates_To_JSON.Creates_Json as creates
import src.Rules_AR.rulesAR as rulesAR


class TestRule10B(unittest.TestCase):

    def test_simple1(self):
        jsonExample = {   "type" : "join",
                          "cond" : {  "type" : "eq",
                                      "values" : ["vuelo1.origen", "Madrid"]
                                  },
                          "lrel" : {  "type" : "sigma",
                                      "cond" : {   "type" : "eq",
                                                   "values" : ["vuelo1.destino", 'Barcelona']
                                               },
                                      "rel" : {'type': 'rel',
                                           'table': {'type': 'rho',
                                                     'ren': ['vuelo', 'vuelo1']
                                                    }
                                           }
                                    },
                          "rrel" : {  "type" : "sigma",
                                      "cond" : {   "type" : "eq",
                                                   "values" : ["avion1.nombre", "Iberia"]
                                               },
                                      "rel" : {'type': 'rel',
                                               'table': {'type': 'rho',
                                                         'ren': ['avion', 'avion1']}
                                              }
                                    }
                      }

        expected = {   "type" : "sigma",
                      "cond" : {	"type" : "and",
                                    "values" : [
                                                {	"type" : "eq",
                                                      "values" : ['Barcelona',"vuelo1.destino"]
                                                },
                                                {	"type" : "eq",
                                                      "values" : ["Iberia","avion1.nombre"]
                                                }
                                          ]
                                    },
                      "rel" : {   "type" : "join",
                                  "cond" : {   "type" : "eq",
                                        "values" : ['vuelo1.origen','Madrid']
                                    },
                                  "rrel" : {'type': 'rel',
                                               'table': {'type': 'rho',
                                                         'ren': ['avion', 'avion1']}
                                              },
                                  "lrel" : {'type': 'rel',
                                           'table': {'type': 'rho',
                                                     'ren': ['vuelo', 'vuelo1']
                                                    }
                                           }
                              }
                  }
        try:
            tablas = creates.create_tables_json([
                                                "create table vuelo(flno number(4,0) primary key, origen varchar2(20), destino varchar2(20), distancia number(6,0), salida date, llegada date, precio number(7,2));",
                                                "create table avion(aid number(9,0) primary key, nombre varchar2(30), autonomia number(6,0));"])
            res = rulesAR.rule10B(jsonExample, tablas)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple1')



if __name__ == "__main__":
    unittest.main()
