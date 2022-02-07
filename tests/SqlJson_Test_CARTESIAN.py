import unittest
import src.SQL_To_JSON.Sql_To_Json as sqlJSON


class SqlJson_Test_CARTESIAN(unittest.TestCase):

    def test_twoTable(self):
        res = sqlJSON.parse_Sql_To_Json("SELECT Nombre FROM Persona, Empr")
        expected = {"type": "pi",
                    "proj": ["Nombre"],
                    "rel": {"type": "pro",
                            "lrel": {"type": "rel",
                                     "table": "Persona"},
                            "rrel": {"type": "rel",
                                     "table": "Empr"}
                            }
                    }
        self.assertEqual(res, expected)

    def test_threeTable(self):
        res = sqlJSON.parse_Sql_To_Json("SELECT Nombre FROM Persona, Empr, Dep")
        expected = {"type": "pi",
                    "proj": ["Nombre"],
                    "rel": {"type": "pro",
                            "lrel": {"type": "rel",
                                     "table": "Persona"},
                            "rrel": {"type": "pro",
                                     "lrel": {"type": "rel",
                                              "table": "Empr"},
                                     "rrel": {"type": "rel",
                                              "table": "Dep"}
                                     }
                            }
                    }
        self.assertEqual(res, expected)

    def test_fourTable(self):
        res = sqlJSON.parse_Sql_To_Json("SELECT Nombre FROM Persona, Empr, Dep, Casa")
        expected = {"type": "pi",
                    "proj": ["Nombre"],
                    "rel": {"type": "pro",
                            "lrel": {"type": "rel",
                                     "table": "Persona"},
                            "rrel": {"type": "pro",
                                     "lrel": {"type": "rel",
                                              "table": "Empr"},
                                     "rrel": {"type": "pro",
                                              "lrel": {"type": "rel",
                                                       "table": "Dep"},
                                              "rrel": {"type": "rel",
                                                       "table": "Casa"}}
                                     }
                            }
                    }
        self.assertEqual(res, expected)


if __name__ == "__main__":
    unittest.main()
