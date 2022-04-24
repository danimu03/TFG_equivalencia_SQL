import unittest
import src.Creates_To_JSON.Creates_Json as creates
import src.Rules_AR.rulesAR as rulesAR


class TestRule9B(unittest.TestCase):

    def test_simple1(self):
        jsonExample = {  "type" : "join",
                          "cond" : {  "type" : "eq",
                                      "values" : ['vuelo1.distancia', 18]
                                  },
                          "lrel" : {  "type" : "sigma",
                                      "cond" : {   "type" : "eq",
                                                   "values" : ['avion1.nombre', 'Iberia']
                                               },
                                      "rel" : {'type': 'rel',
                                               'table': {'type': 'rho',
                                                         'ren': ['avion', 'avion1']}
                                              }
                                    },
                          "rrel" : {'type': 'rel',
                                   'table': {'type': 'rho',
                                             'ren': ['vuelo', 'vuelo1']
                                            }
                                   }
                      }

        expected = {   "type" : "sigma",
                          "cond" : {  "type" : "eq",
                                      "values" : ['Iberia','avion1.nombre' ]
                                   },
                          "rel" : {   "type" : "join",
                                      "cond" : {   "type" : "eq",
                                                   "values" : [18,'vuelo1.distancia']
                                               },
                                      "lrel" : {'type': 'rel',
                                               'table': {'type': 'rho',
                                                         'ren': ['avion', 'avion1']}
                                              },
                                      "rrel" : {'type': 'rel',
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
            res = rulesAR.rule10A(jsonExample, tablas)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple1')



if __name__ == "__main__":
    unittest.main()
