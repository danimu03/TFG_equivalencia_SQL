import unittest
import src.Creates_To_JSON.Creates_Json as creates
import src.Rules_AR.rulesAR as rulesAR


class TestRule11B(unittest.TestCase):

    def test_simple1(self):
        jsonExample = {   "type" : "pi",
                            "proj" : ['Personas1.edad', 'Ganadores1.premio'],
                            "rel" : { "type" : "join",
                                      "cond" : {      "type" : "eq",
                                                      "values" : ["Personas1.nombre", "Juan"]
                                                },
                                      "lrel" :  {   "type" : "pi",
                                                    "proj" : ["Personas1.edad", "Personas1.sexo"],
                                                    "rel" : "Personas"
                                                },
                                      "rrel" : {    "type" : "pi",
                                                    "proj" : ["Ganadores1.premio", "Ganadores1.nacionalidad"],
                                                    "rel" : "Ganadores"
                                                }
                                    }
                        }

        expected = {   "type" : "pi",
                        "proj" : ['Personas1.edad', 'Ganadores1.premio'],
                        "rel" :{    "type" : "join",
                                    "cond" :{     "type" : "eq",
                                                  "values" : ["Personas1.nombre", "Juan"]
                                              },
                                    "lrel" : "Personas",
                                    "rrel" : "Ganadores"
                                }
                     }
        try:
            tablas = creates.create_tables_json([
                                                "create table Personas(dni number(4,0) primary key, edad varchar2(20), nombre varchar2(20), sexo varchar2(20));",
                                                "create table Ganadores(dni number(9,0) primary key, nacionalidad varchar2(30), premio varchar2(20));"])
            res = rulesAR.rule11B(jsonExample, tablas)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple1')



if __name__ == "__main__":
    unittest.main()
