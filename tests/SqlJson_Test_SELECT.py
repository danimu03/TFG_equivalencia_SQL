import unittest
from src.SQL_To_JSON.Sql_To_Json import parse_Sql_To_Json as sql
from src.Creates_To_JSON.Creates_Json import create_tables_json as create

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

        res = sql("SELECT nombre FROM Persona", create(
            ["CREATE TABLE Persona(nombre VARCHAR2(30) PRIMARY KEY);"]))
        expected = {'type': 'pi',
                    'proj': ['Persona1.nombre'],
                    'rel': {'type': 'rel',
                            'table': {'type': 'rho',
                                      'ren': ['Persona', 'Persona1']
                                      }
                            }
                    }
        self.assertEqual(res, expected)

    def test_twoSELECT(self):
        """
        Test of SELECT two attributes

        Original query: SELECT Nombre, Edad FROM Persona
        """

        res = sql("SELECT nombre, edad FROM Persona", create(
            ["CREATE TABLE Persona(nombre VARCHAR2(30) PRIMARY KEY, edad INT(3));"]))
        expected = {"type": "pi",
                    "proj": ["Persona1.nombre", "Persona1.edad"],
                    "rel": {"type": "rel",
                            "table": {'type': 'rho',
                                      'ren': ['Persona', 'Persona1']
                                      }
                            }
                    }
        self.assertEqual(res, expected)

    def test_fiveSELECT(self):
        """
        Test of SELECT five attributes

        Original query: SELECT Nombre, Ap1, Ap2, Edad, Telefono FROM Persona
        """

        res = sql("SELECT nombre, ap1, ap2, edad, telefono FROM Persona", create(
            ["CREATE TABLE Persona(nombre VARCHAR2(30) PRIMARY KEY, ap1 VARCHAR(10), ap2 VARCHAR(10), edad INT(3), telefono INT(9));"]))
        expected = {"type": "pi",
                    "proj": ["Persona1.nombre", "Persona1.ap1", "Persona1.ap2", "Persona1.edad", "Persona1.telefono"],
                    "rel": {"type": "rel",
                            "table": {'type': 'rho',
                                      'ren': ['Persona', 'Persona1']
                                      }
                            }
                    }
        self.assertEqual(res, expected)

if __name__ == "__main__":
    unittest.main()