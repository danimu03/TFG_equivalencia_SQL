import unittest
import src.SQL_To_JSON.Sql_To_Json as sqlJSON

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
        """
        Test of equal to Int

        Original query:  SELECT Nombre FROM Persona WHERE Telefono = 12345"
        """

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

    def test_ANDTwoEquals(self):
        """
        Test of equal AND equal

        Original query:  SELECT Nombre FROM Persona WHERE Pais = \"España\" AND Telefono = 12345
        """

        res = sqlJSON.parse_Sql_To_Json("SELECT Nombre FROM Persona WHERE Pais = \"España\" AND Telefono = 12345")
        expected = {"type": "pi",
                    "proj": ["Nombre"],
                    "rel": {"type": "sigma",
                            "cond": {"type": "and",
                                     "values": [{"type": "eq",
                                                 "values": ["Pais", "España"]},
                                                {"type": "eq",
                                                 "values": ["Telefono", 12345]}]
                                     },
                            "rel": {"type": "rel",
                                    "table": "Persona"
                                    }
                            }
                    }
        self.assertEqual(res, expected)

    def test_ANDThreeEquals(self):
        """
        Test of two AND and three equals

        Original query:  SELECT Nombre FROM Persona WHERE Pais = \"España\" AND Telefono = 12345 AND Id = \"IS1452\"
        """

        res = sqlJSON.parse_Sql_To_Json("SELECT Nombre FROM Persona WHERE Pais = \"España\" AND Telefono = 12345 AND Id = \"IS1452\"")
        expected = {"type": "pi",
                    "proj": ["Nombre"],
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

    def test_ANDandVariousSelects(self):
        """
        Test of two AND and SELECT various attributes

        Original query:  SELECT Nombre, Edad FROM Persona WHERE Pais = \"España\" AND Telefono = 12345 AND Id = \"IS1452\"
        """

        res = sqlJSON.parse_Sql_To_Json("SELECT Nombre, Edad FROM Persona WHERE Pais = \"España\" AND Telefono = 12345 AND Id = \"IS1452\"")
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