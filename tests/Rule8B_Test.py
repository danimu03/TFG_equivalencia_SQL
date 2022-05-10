import unittest
import src.Rules_AR.rulesAR as rulesAR


class TestRule8B(unittest.TestCase):

    def test_simple1(self):
        jsonExample =   {"type" : "join",
                            "cond" : {   "type" : "eq",
                                          "values" : ["nombre", "Juan"]
                                      },
                            "lrel" : {    "type" : "join",
                                          "cond" : {	"type" : "and",
                                                        "values" : [
                                                                    {	"type" : "eq",
                                                                          "values" : ["edad", 18]
                                                                    },
                                                                    {	"type" : "eq",
                                                                          "values" : ["sexo", "hombre"]
                                                                    }
                                                              ]
                                                        },
                                          "lrel" : "Personas",
                                          "rrel" : "Jugadores"
                                      },
                            "rrel" : "Ganadores"
                        }
        expected = {  "type" : "join",
                        "cond" : {	"type" : "and",
                                        "values" : [
                                                    {	"type" : "eq",
                                                          "values" : ["nombre", "Juan"]
                                                    },
                                                    {	"type" : "eq",
                                                          "values" : ["sexo", "hombre"]
                                                    }
                                              ]
                                        },
                        "lrel" : "Personas",
                        "rrel" : {    "type" : "join",
                                      "cond" : {   "type" : "eq",
                                                  "values" : ["edad", 18]
                                              },
                                      "lrel" : "Jugadores",
                                      "rrel" : "Ganadores"
                                  }
                    }
        try:
            res = rulesAR.rule8B(jsonExample)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple1')



if __name__ == "__main__":
    unittest.main()
