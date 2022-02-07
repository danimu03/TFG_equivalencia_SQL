import unittest
import src.SQL_To_JSON.Sql_To_Json as sqlJSON

class SqlJson_Test_SELECT(unittest.TestCase):
    """
    Class to test transformations from SQL to relational algebra, focusing on SELECT various attributes

    Methods
    _______
    test_oneSELECT
        Test of SELECT one attribute

    test_twoSELECT
        Test of SELECT two attributes

    test_fiveSELECT
        Test of SELECT five attributes
    """

    def test_oneSELECT(self):
        """
        Test of SELECT one attribute

        Original query: SELECT Nombre FROM Persona
        """

        res = sqlJSON.parse_Sql_To_Json("SELECT Nombre FROM Persona")
        expected = {"type": "pi",
                    "proj": ["Nombre"],
                    "rel": {"type": "rel",
                            "table": "Persona"
                            }
                    }
        self.assertEqual(res, expected)

    def test_twoSELECT(self):
        """
        Test of SELECT two attributes

        Original query: SELECT Nombre, Edad FROM Persona
        """

        res = sqlJSON.parse_Sql_To_Json("SELECT Nombre, Edad FROM Persona")
        expected = {"type": "pi",
                    "proj": ["Nombre", "Edad"],
                    "rel": {"type": "rel",
                            "table": "Persona"
                            }
                    }
        self.assertEqual(res, expected)

    def test_fiveSELECT(self):
        """
        Test of SELECT five attributes

        Original query: SELECT Nombre, Ap1, Ap2, Edad, Telefono FROM Persona
        """

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