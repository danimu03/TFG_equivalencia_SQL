import unittest
from src.SQL_To_JSON import Sql_To_Json as sqlJSON

class SqlJson_Test_CONDITIONS(unittest.TestCase):

    def test_equalString (self):
        res = sqlJSON.parse_Sql_To_Json("SELECT Nombre FROM Persona WHERE Pais = \"España\"")
        expected = {"type": "pi",
                    "proj": ["Nombre"],
                    "rel": {"type": "sigma",
                            "cond": {"type": "eq",
                                     "values": ["Pais", "España"]
                                     },
                            "rel": {"type": "rel",
                                    "table": "Persona"
                                    }
                            }
                    }
        self.assertEqual(res, expected)

    def test_equalInt(self):
        res = sqlJSON.parse_Sql_To_Json("SELECT Nombre FROM Persona WHERE Telefono = 12345")
        expected = {"type": "pi",
                    "proj": ["Nombre"],
                    "rel": {"type": "sigma",
                            "cond": {"type": "eq",
                                     "values": ["Telefono", 12345]
                                     },
                            "rel": {"type": "rel",
                                    "table": "Persona"
                                    }
                            }
                    }
        self.assertEqual(res, expected)

if __name__ == "__main__":
    unittest.main()