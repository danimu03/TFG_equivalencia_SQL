import unittest
from src.SQL_To_JSON.Sql_To_Json import parse_Sql_To_Json as sql
from src.Creates_To_JSON.Creates_Json import create_tables_json as create

class SqlJson_Test_CONDITIONS(unittest.TestCase):
    """
    Class to test transformations from SQL to relational algebra, focusing on conditions

    Methods
    _______
    test_equalString
        Test of equal to String

    test_equalInt
        Test of equal to Int

    test_ANDTwoEquals
        Test of equal AND equal

    test_ANDThreeEquals
        Test of two AND and three equals

    test_ANDandVariousSelects
        Test of two AND and SELECT various attributes
    """

    def test_equalString(self):
        """
        Test of equal to String

        Original query:  SELECT Nombre FROM Persona WHERE Pais = \"España\"
        """

        res = sql("SELECT nombre FROM Persona WHERE pais = 'España'", create(
            ["CREATE TABLE Persona(nombre VARCHAR2(30) PRIMARY KEY,"
             "ap1 VARCHAR(10),"
             "ap2 VARCHAR(10),"
             "edad INT(3),"
             "telefono INT(9),"
             "pais VARCHAR(10));"
             ]))
        expected = {'type': 'pi',
                    'proj': ['Persona1.nombre'],
                    'rel': {'type': 'sigma',
                            'cond': {'type': 'eq',
                                     'values': ['Persona1.pais', 'España']
                                     },
                            'rel': {'type': 'rel',
                                    'table': {'type': 'rho',
                                              'ren': ['Persona', 'Persona1']
                                              }
                                    }
                            }
                    }
        self.assertEqual(res, expected)

    def test_equalInt(self):
        """
        Test of equal to Int

        Original query:  SELECT Nombre FROM Persona WHERE Telefono = 12345"
        """

        res = sql("SELECT nombre FROM Persona WHERE telefono = 12345", create(
            ["CREATE TABLE Persona(nombre VARCHAR2(30) PRIMARY KEY,"
             "ap1 VARCHAR(10),"
             "ap2 VARCHAR(10),"
             "edad INT(3),"
             "telefono INT(9),"
             "pais VARCHAR(10));"
             ]))
        expected = {'type': 'pi',
                    'proj': ['Persona1.nombre'],
                    'rel': {'type': 'sigma',
                            'cond': {'type': 'eq',
                                     'values': ['Persona1.telefono', 12345]},
                            'rel': {'type': 'rel',
                                    'table': {'type': 'rho',
                                              'ren': ['Persona', 'Persona1']
                                              }
                                    }
                            }
                    }
        self.assertEqual(res, expected)

    def test_ANDTwoEquals(self):
        """
        Test of equal AND equal

        Original query:  SELECT Nombre FROM Persona WHERE Pais = \"España\" AND Telefono = 12345
        """

        res = sql("SELECT nombre FROM Persona WHERE pais = 'España' AND telefono = 12345", create(
            ["CREATE TABLE Persona(nombre VARCHAR2(30) PRIMARY KEY,"
             "ap1 VARCHAR(10),"
             "ap2 VARCHAR(10),"
             "edad INT(3),"
             "telefono INT(9),"
             "pais VARCHAR(10));"
             ]))
        expected = {'type': 'pi',
                    'proj': ['Persona1.nombre'],
                    'rel': {'type': 'sigma',
                            'cond': {'type': 'and',
                                     'values': [{'type': 'eq',
                                                 'values': ['Persona1.pais', 'España']
                                                 },
                                                {'type': 'eq',
                                                 'values': ['Persona1.telefono', 12345]
                                                 }]
                                     },
                            'rel': {'type': 'rel',
                                    'table': {'type': 'rho',
                                              'ren': ['Persona', 'Persona1']
                                              }
                                    }
                            }
                    }

        self.assertEqual(res, expected)

    def test_ANDThreeEquals(self):
        """
        Test of two AND and three equals

        Original query:  SELECT Nombre FROM Persona WHERE Pais = \"España\" AND Telefono = 12345 AND Id = \"IS1452\"
        """

        res = sql("SELECT nombre FROM Persona WHERE pais = 'España' AND telefono = 12345 AND edad = 26", create(
            ["CREATE TABLE Persona(nombre VARCHAR2(30) PRIMARY KEY,"
             "ap1 VARCHAR(10),"
             "ap2 VARCHAR(10),"
             "edad INT(3),"
             "telefono INT(9),"
             "pais VARCHAR(10));"
             ]))
        expected = {'type': 'pi',
                    'proj': ['Persona1.nombre'],
                    'rel': {'type': 'sigma',
                            'cond': {'type': 'and',
                                     'values': [{'type': 'eq',
                                                 'values': ['Persona1.pais', 'España']
                                                 },
                                                {'type': 'eq',
                                                 'values': ['Persona1.telefono', 12345]
                                                 },
                                                {'type': 'eq',
                                                 'values': ['Persona1.edad', 26]
                                                 }]
                                     },
                            'rel': {'type': 'rel',
                                    'table': {'type': 'rho',
                                              'ren': ['Persona', 'Persona1']
                                              }
                                    }
                            }
                    }

        self.assertEqual(res, expected)

    def test_ANDandVariousSelects(self):
        """
        Test of two AND and SELECT various attributes

        Original query:  SELECT Nombre, Edad FROM Persona WHERE Pais = \"España\" AND Telefono = 12345 AND Id = \"IS1452\"
        """

        res = sql("SELECT nombre, edad FROM Persona WHERE pais = 'España' AND telefono = 12345 AND edad = 26", create(
            ["CREATE TABLE Persona(nombre VARCHAR2(30) PRIMARY KEY,"
             "ap1 VARCHAR(10),"
             "ap2 VARCHAR(10),"
             "edad INT(3),"
             "telefono INT(9),"
             "pais VARCHAR(10));"
             ]))
        expected = {'type': 'pi',
                    'proj': ['Persona1.nombre',
                             'Persona1.edad'],
                    'rel': {'type': 'sigma',
                            'cond': {'type': 'and',
                                     'values': [{'type': 'eq',
                                                 'values': ['Persona1.pais', 'España']
                                                 }, {'type': 'eq',
                                                     'values': ['Persona1.telefono', 12345]
                                                     },
                                                {'type': 'eq',
                                                 'values': ['Persona1.edad', 26]
                                                 }]
                                     },
                            'rel': {'type': 'rel',
                                    'table': {'type': 'rho',
                                              'ren': ['Persona', 'Persona1']
                                              }
                                    }
                            }
                    }

        self.assertEqual(res, expected)

if __name__ == "__main__":
    unittest.main()