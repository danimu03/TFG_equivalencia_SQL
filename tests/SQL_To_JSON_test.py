import unittest
from src.SQL_To_JSON import Sql_To_Json as sqlJSON

class TestSqlJson(unittest.TestCase):

    # def test_one(self):
    #     res = sqlJSON.parse_Sql_To_Json("SELECT Nombre FROM Persona WHERE Pais = \"España\"")
    #     #res = {'type': 'pi', 'proj': ['Nombre'], 'rel': {'type': 'sigma', 'cond': {'type': 'eq', 'values': ['Pais', 'España']}, 'rel': {'type': 'rel', 'table': 'Persona'}}}
    #     expected = {"type" : "pi",
    #                 "proj" : ["Nombre"],
    #                 "rel" : {"type" : "sigma",
    #                         "cond" : {"type": "eq",
    #                                 "values" : ["Pais", "España"]},
    #                         "rel" :	{"type" : "rel",
	# 						        "table" : "Persona"}
    #                         }
    #             }
    #     self.assertEqual(res, expected)

    def test_two(self):
        #res = parse_Sql_To_Json("SELECT Nombre, Ap1, Ap2 FROM Empl JOIN Proyecto ON Dni = DniDir")
        res = {"type" : "example"}
        expected = {"type" : "pi",
	                "proj" : ["Nombre", "Ap1", "Ap2"],
	                "rel" : {"type" : "join",
                            "cond" : {"type" : "eq",
                                    "values" : ["Dni", "DniDir"]},
                            "lrel" : {"type" : "rel",
                                    "table"	: "Empl"},
                            "rrel" : {"type" : "rel",
                                    "table"	:	"Proyecto"}
			                }
                    }
        self.assertEqual(res, expected)

    def test_three(self):
        res = sqlJSON.parse_Sql_To_Json("SELECT Nombre, Ap1, Ap2 FROM Empl, Dedicacion WHERE Dni=DniEmpl")
        #res = {'type': 'pi', 'proj': ['Nombre', 'Ap1', 'Ap2'], 'rel': {'type': 'sigma', 'cond': {'type': 'eq', 'values': ['Dni', 'DniEmpl']}, 'rel': {'type': 'pro', 'lrel': {'type': 'rel', 'table': 'Empl'}, 'rrel': {'type': 'rel', 'table': 'Dedicacion'}}}}
        expected = {"type" : "pi",
	                "proj" : ["Nombre", "Ap1", "Ap2"],
	                "rel" :	{"type" : "sigma",
                            "cond" : {"type" : "eq",
                                    "values" : ["Dni", "DniEmpl"]},
                            "rel" : {"type" : "pro",
                                    "lrel" : {"type" : "rel",
                                            "table"	:	"Empl"},
                                    "rrel" : {"type" :	"rel",
                                            "table"	: "Dedicacion"}
						            }
			                }
                    }
        self.assertEqual(res, expected)

    # def test_four(self):
    #     #res = parse_Sql_To_Json("SELECT p.nombre FROM curso AS c, profesor AS p WHERE p.nombre = \"Juan Carlos\" AND c.id = \"IS345\"")
    #     res = {"type" : "example"}
    #     expected = {"type" : "pi",
    #                 "proj" : ["Nombre", "Ap1", "Ap2"],
    #                 "rel" : {"type" : "sigma",
    #                         "cond" : {"type" : "and",
    #                                 "values" : [{"type" : "eq",
    #                                             "values" : ["p.nombre", "Juan Carlos"]},
    #                                             {"type" : "eq",
    #                                             "values" : ["c.id", "IS345"]}]
    #                                 },
    #                         "rel" :	{"type" : "pro",
    #                                 "lrel" : {"type" : "rho",
    #                                         "ren" : ["curso", "c"],
    #                                         "rel" : {"type"	: "rel",
    #                                                 "table" : "curso"}
    #                                                 },
    #                                 "rrel" : {"type" : "rho",
    #                                         "ren" : ["profesor", "p"],
    #                                         "rel" :	{ "type" : "rel",
    #                                                   "table" :	"profesor"}
    #                                         }
    #                                 }
    #                         }
    #                 }
    #     self.assertEqual(res, expected)

    # def test_five(self):
    #     res = sqlJSON.parse_Sql_To_Json("SELECT Nombre, Edad FROM Persona WHERE Pais = \"España\"")
    #     #res = {'type': 'pi', 'proj': ['Nombre', 'Edad'], 'rel': {'type': 'sigma', 'cond': {'type': 'eq', 'values': ['Pais', 'España']}, 'rel': {'type': 'rel', 'table': 'Persona'}}}
    #     expected = {"type": "pi",
    #                 "proj": ["Nombre", "Edad"],
    #                 "rel": {"type": "sigma",
    #                         "cond": {"type": "eq",
    #                                  "values": ["Pais", "España"]
    #                                  },
    #                         "rel": {"type": "rel",
    #                                 "table": "Persona"
    #                                 }
    #                         }
    #                 }
    #     self.assertEqual(res, expected)

    # def test_six(self):
    #     res = sqlJSON.parse_Sql_To_Json("SELECT Nombre, Edad, Telefono FROM Persona WHERE Pais = \"España\"")
    #     #res = {'type': 'pi', 'proj': ['Nombre', 'Edad', 'Telefono'], 'rel': {'type': 'sigma', 'cond': {'type': 'eq', 'values': ['Pais', 'España']}, 'rel': {'type': 'rel', 'table': 'Persona'}}}
    #     expected = {"type": "pi",
    #                 "proj": ["Nombre", "Edad", "Telefono"],
    #                 "rel": {"type": "sigma",
    #                         "cond": {"type": "eq",
    #                                  "values": ["Pais", "España"]
    #                                  },
    #                         "rel": {"type": "rel",
    #                                 "table": "Persona"
    #                                 }
    #                         }
    #                 }
    #     self.assertEqual(res, expected)

    # def test_seven(self):
    #     res = sqlJSON.parse_Sql_To_Json("SELECT Nombre, Edad FROM Persona WHERE Telefono = 12345")
    #     #res = {'type': 'pi', 'proj': ['Nombre', 'Edad'], 'rel': {'type': 'sigma', 'cond': {'type': 'eq', 'values': ['Telefono', 12345]}, 'rel': {'type': 'rel', 'table': 'Persona'}}}
    #     expected = {"type": "pi",
    #                 "proj": ["Nombre", "Edad"],
    #                 "rel": {"type": "sigma",
    #                         "cond": {"type": "eq",
    #                                  "values": ["Telefono", 12345]
    #                                  },
    #                         "rel": {"type": "rel",
    #                                 "table": "Persona"
    #                                 }
    #                         }
    #                 }
    #     self.assertEqual(res, expected)

    def test_eight(self):
        res = sqlJSON.parse_Sql_To_Json("SELECT Nombre, Ap1, Ap2 FROM Empl, Dedicacion, Persona WHERE Dni=DniEmpl")
        #res = {'type': 'pi', 'proj': ['Nombre', 'Ap1', 'Ap2'], 'rel': {'type': 'sigma', 'cond': {'type': 'eq', 'values': ['Dni', 'DniEmpl']}, 'rel': {'type': 'pro', 'lrel': {'type': 'rel', 'table': 'Empl'}, 'rrel': {'type': 'pro', 'lrel': {'type': 'rel', 'table': 'Dedicacion'}, 'rrel': {'type': 'rel', 'table': 'Persona'}}}}}

        expected = {"type": "pi",
                    "proj": ["Nombre", "Ap1", "Ap2"],
                    "rel": {"type": "sigma",
                            "cond": {"type": "eq",
                                     "values": ["Dni", "DniEmpl"]},
                            "rel": {"type": "pro",
                                    "lrel": {"type": "rel",
                                             "table": "Empl"},
                                    "rrel": {"type": "pro",
                                             "lrel": {"type": "rel",
                                                      "table": "Dedicacion"},
                                             "rrel": {"type": "rel",
                                                      "table": "Persona"
                                                      }
                                             }
                                    }
                            }
                    }
        self.assertEqual(res, expected)

    def test_nine(self):
        res = sqlJSON.parse_Sql_To_Json("SELECT Nombre, Ap1, Ap2 FROM Empl, Dedicacion, Persona, Sector, Jefe WHERE Dni=DniEmpl")
        #res = {'type': 'pi', 'proj': ['Nombre', 'Ap1', 'Ap2'], 'rel': {'type': 'sigma', 'cond': {'type': 'eq', 'values': ['Dni', 'DniEmpl']}, 'rel': {'type': 'pro', 'lrel': {'type': 'rel', 'table': 'Empl'}, 'rrel': {'type': 'pro', 'lrel': {'type': 'rel', 'table': 'Dedicacion'}, 'rrel': {'type': 'pro', 'lrel': {'type': 'rel', 'table': 'Persona'}, 'rrel': {'type': 'pro', 'lrel': {'type': 'rel', 'table': 'Sector'}, 'rrel': {'type': 'rel', 'table': 'Jefe'}}}}}}}

        expected = {"type": "pi",
                    "proj": ["Nombre", "Ap1", "Ap2"],
                    "rel": {"type": "sigma",
                            "cond": {"type": "eq",
                                     "values": ["Dni", "DniEmpl"]},
                            "rel": {"type": "pro",
                                    "lrel": {"type": "rel",
                                             "table": "Empl"},
                                    "rrel": {"type": "pro",
                                             "lrel": {"type": "rel",
                                                      "table": "Dedicacion"},
                                             "rrel": {"type": "pro",
                                                      "lrel": {"type": "rel",
                                                               "table": "Persona"},
                                                      "rrel": {"type": "pro",
                                                               "lrel": {"type": "rel",
                                                                        "table": "Sector"},
                                                               "rrel": {"type": "rel",
                                                                        "table": "Jefe"}
                                                               }
                                                      }
                                             }
                                    }
                            }
                    }
        self.assertEqual(res, expected)

    # def test_ten(self):
    #     res = sqlJSON.parse_Sql_To_Json("SELECT Nombre, Edad FROM Persona WHERE Pais = \"España\" AND Telefono = 12345")
    #     #res = {'type': 'pi', 'proj': ['Nombre', 'Edad'], 'rel': {'type': 'sigma', 'cond': {'type': 'and', 'values': [{'type': 'eq', 'values': ['Pais', 'España']}, {'type': 'eq', 'values': ['Telefono', 12345]}]}, 'rel': {'type': 'rel', 'table': 'Persona'}}}
    #
    #     expected = {"type": "pi",
    #                 "proj": ["Nombre", "Edad"],
    #                 "rel": {"type": "sigma",
    #                         "cond": {"type": "and",
    #                                  "values": [{"type": "eq",
    #                                              "values": ["Pais", "España"]},
    #                                             {"type": "eq",
    #                                              "values": ["Telefono", 12345]}]
    #                                  },
    #                         "rel": {"type": "rel",
    #                                 "table": "Persona"
    #                                 }
    #                         }
    #                 }
    #     self.assertEqual(res, expected)

    def test_eleven(self):
        res = sqlJSON.parse_Sql_To_Json("SELECT Nombre, Edad FROM Persona WHERE Pais = \"España\" AND Telefono = 12345 AND Id = \"IS1452\"")
        #res = {'type': 'pi', 'proj': ['Nombre', 'Edad'], 'rel': {'type': 'sigma', 'cond': {'type': 'and', 'values': [{'type': 'eq', 'values': ['Pais', 'España']}, {'type': 'eq', 'values': ['Telefono', 12345]}, {'type': 'eq', 'values': ['Id', 'IS1452']}]}, 'rel': {'type': 'rel', 'table': 'Persona'}}}

        expected = {"type": "pi",
                    "proj": ["Nombre", "Edad"],
                    "rel": {"type": "sigma",
                            "cond": {"type": "and",
                                     "values": [{"type": "eq",
                                                 "values": ["Pais", "España"]},
                                                {"type": "eq",
                                                 "values": ["Telefono", 12345]},
                                                 {"type": "eq",
                                                  "values": ["Id", "IS1452"]}]
                                     },
                            "rel": {"type": "rel",
                                    "table": "Persona"
                                    }
                            }
                    }
        self.assertEqual(res, expected)



if __name__ == "__main__":
    unittest.main()
    
