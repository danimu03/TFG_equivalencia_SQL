import unittest
import src.Rules_AR.rulesAR as rulesAR


class TestRule7(unittest.TestCase):

    def test_simple1(self):

        jsonExample = {"type" : "join",
                        "cond" : {"type" : "eq",
                                  "values" : ["nombre", "Juan"]
                                  },
                        "lrel" : {'type' : 'rel' ,
                               'table' : {'type': 'rho',
                                          'ren': ['Personas', 'Personas1']},
                               },
                        "rrel" : {'type' : 'rel' ,
                               'table' : {'type': 'rho',
                                          'ren': ['Jugadores', 'Jugadores1']},
                               }
                       }
        expected = {"type" : "join",
                    "cond" : {"type" : "eq",
                              "values" : ["nombre", "Juan"]
                              },
                    "lrel" : {'type' : 'rel' ,
                               'table' : {'type': 'rho',
                                          'ren': ['Jugadores', 'Jugadores1']},
                               },
                    "rrel" : {'type' : 'rel' ,
                               'table' : {'type': 'rho',
                                          'ren': ['Personas', 'Personas1']},
                               }
                   }
        try:
            res = rulesAR.rule7(jsonExample)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple1')


if __name__ == "__main__":
    unittest.main()
