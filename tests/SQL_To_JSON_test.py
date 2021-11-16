from unittest import TestCase
import unittest


class TestSqlJson(TestCase):

    def test_one(self):
        #res = name_function("SELECT Nombre FROM Persona WHERE Pais = \"España\"")
        res = {"type" : "example"}
        expected = {"type" : "pi", 
                    "proj" : ["Nombre"],
                    "rel" : {"type" : "sigma",
                            "cond" : {"type": "eq",	
                                    "values" : ["Pais", "España"]},
                            "rel" :	{"type" : "rel",
							        "table" : "Persona"}
                            }
                }
        self.assertTrue(res == expected)
    
    def test_two(self):
        #res = name_function("SELECT Nombre, Ap1, Ap2 FROM Empl JOIN Proyecto ON Dni = DniDir")
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
        self.assertTrue(res == expected)

    def test_three(self):
        #res = name_function("SELECT Nombre, Ap1, Ap2 FROM Empl, Dedicacion WHERE Dni=DniEmpl")
        res = {"type" : "example"}
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
        self.assertTrue(res == expected)

    def test_four(self):
        #res = name_function("SELECT p.nombre FROM curso AS c, profesor AS p WHERE p.nombre = \"Juan Carlos\" AND c.id = \"IS345\"")
        res = {"type" : "example"}
        expected = {"type" : "pi",
                    "proj" : ["Nombre", "Ap1", "Ap2"],
                    "rel" : {"type" : "sigma",
                            "cond" : {"type" : "and",	
                                    "values" : [{"type" : "eq",
                                                "values" : ["p.nombre", "Juan Carlos"]},
                                                {"type" : "eq",
                                                "values" : ["c.id", "IS345"]}]	
                                    },
                            "rel" :	{"type" : "pro",
                                    "lrel" : {"type" : "rho",
                                            "ren" : ["curso", "c"],
                                            "rel" : {"type"	: "rel",
                                                    "table" : "curso"}
                                                    },
                                    "rrel" : {"type" : "rho",
                                            "ren" : ["profesor", "p"],
                                            "rel" :	{ "type" : "rel",
                                                      "table" :	"profesor"}
                                            }
                                    }
                            }
                    }
        self.assertTrue(res == expected)
    


if __name__ == "__main__":
    unittest.main()
    