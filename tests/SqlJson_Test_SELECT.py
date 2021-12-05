import unittest
from src.SQL_To_JSON import Sql_To_Json as sqlJSON

class SqlJson_Test_SELECT(unittest.TestCase):

    def test_oneSELECT(self):
        res = sqlJSON.parse_Sql_To_Json("SELECT Nombre FROM Persona")
        expected = {"type": "pi",
                    "proj": ["Nombre"],
                    "rel": {"type": "rel",
                            "table": "Persona"
                            }
                    }
        self.assertEqual(res, expected)

    def test_twoSELECT(self):
        res = sqlJSON.parse_Sql_To_Json("SELECT Nombre, Edad FROM Persona")
        expected = {"type": "pi",
                    "proj": ["Nombre", "Edad"],
                    "rel": {"type": "rel",
                            "table": "Persona"
                            }
                    }
        self.assertEqual(res, expected)

    def test_fiveSELECT(self):
        res = sqlJSON.parse_Sql_To_Json("SELECT Nombre, Ap1, Ap2, Edad, Telefono FROM Persona")
        expected = {"type": "pi",
                    "proj": ["Nombre", "Ap1", "Ap2", "Edad", "Telefono"],
                    "rel": {"type": "rel",
                            "table": "Persona"
                            }
                    }
        self.assertEqual(res, expected)

if __name__ == "__main__":
    unittest.main()