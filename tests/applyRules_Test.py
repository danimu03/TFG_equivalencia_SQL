import unittest
import src.equivalence as equi


class TestRule1(unittest.TestCase):

    def test1(self):
        query1 = {"type" : "pi",
                    "proj" : ["Nombre"],
                     "rel" : {"type" : "sigma",
                             "cond" : {"type": "eq",
                                     "values" : ["Pais", "España"]},
                             "rel" : "Persona"}
                             }
        query2 = {"type" : "pi",
                    "proj" : ["Nombre"],
                     "rel" : {"type" : "sigma",
                             "cond" : {"type": "eq",
                                     "values" : ["España", "Pais"]},
                             "rel" : "Persona"}
                             }
        final1 = [False]
        final2 = [False]

        res1 = equi.applyRules(query1, None, final1)
        res2 = equi.applyRules(query2, None, final2)

        self.assertEqual(res1, res2)




    '''def test2(self):
        query1 = {"type" : "pi",
	                "proj" : ["Nombre"],
	                "rel" : {"type" : "join",
                            "cond" : {"type" : "eq",
                                    "values" : ["Dni", "DniDir"]},
                            "lrel" : {"type" : "rel",
                                    "table"	: "Empleado"},
                            "rrel" : {"type" : "rel",
                                    "table"	:	"Proyecto"}
			                }
                    }
        query2 = {"type" : "pi",
	                "proj" : ["Nombre"],
	                "rel" : {"type" : "join",
                            "cond" : {"type" : "eq",
                                    "values" : ["Dni", "DniDir"]},
                            "lrel" : {"type" : "rel",
                                    "table"	: "Proyecto"},
                            "rrel" : {"type" : "rel",
                                    "table"	:	"Empleado"}
			                }
                    }
        final1 = [False]
        final2 = [False]

        res1 = equi.applyRules(query1, None, final1)
        res2 = equi.applyRules(query2, None, final2)

        self.assertEqual(res1, res2)'''

    def test3(self):
        query1 = {"type": "sigma",
                   "cond": {"type": "eq",
                            "values": ["edad", 18]},
                   "rel": {'type': 'sigma',
                           'cond': {'type': 'and',
                                    'values': [{'type': 'eq', 'values': ['sexo', 'hombre']},
                                               {'type': 'eq', 'values': ['Juan', 'nombre']}
                                               ]
                                    },
                           'rel': 'Personas'}
                   }
        query2 = {"type": "sigma",
                   "cond": {"type": "eq",
                            "values": ['sexo','hombre']},
                   "rel": {'type': 'sigma',
                           'cond': {'type': 'and',
                                    'values': [{'type': 'eq', 'values': ["edad", 18]},
                                               {'type': 'eq', 'values': ['Juan', 'nombre']}
                                               ]
                                    },
                           'rel': 'Personas'}
                   }
        final1 = [False]
        final2 = [False]

        res1 = equi.applyRules(query1, None, final1)
        res2 = equi.applyRules(query2, None, final2)

        self.assertEqual(res1, res2)


    def test4(self):

        query1 = {"type": "pi",
                       "proj": ["edad"],
                       "rel": {"type": "pi",
                               "proj": ["sexo"],
                               "rel": {"type" : "sigma",
                                         "cond" : {"type": "eq",
                                                 "values" : ["Pais", "España"]},
                                         "rel" : "Persona"}
                                         }
                       }
        query2 = {"type": "pi",
                       "proj": ["edad"],
                       "rel": {"type": "pi",
                               "proj": ["sexo"],
                               "rel": {"type" : "sigma",
                                         "cond" : {"type": "eq",
                                                 "values" : ["España", "Pais"]},
                                         "rel" : "Persona"}
                                         }
                       }
        final1 = [False]
        final2 = [False]

        res1 = equi.applyRules(query1, None, final1)
        res2 = equi.applyRules(query2, None, final2)

        while final1[0] == False:
            res1 = equi.applyRules(res1, None, final1)

        while final2[0] == False:
            res2 = equi.applyRules(res2, None, final2)

        self.assertEqual(res1, res2)



if __name__ == "__main__":
    unittest.main()