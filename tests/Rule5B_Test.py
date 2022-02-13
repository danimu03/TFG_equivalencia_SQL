import unittest
import src.Rules_AR.rulesAR as rulesAR

class TestRule5B(unittest.TestCase):

    def test_simple1(self):

        jsonExample = { "type" : "sigma",
                        "cond" : {"type" : "eq",
                                  "values" : ["edad", 18]
                                 },
                        "rel" : {"type" : "join",
                                 "cond" :{"type" : "eq",
                                          "values" : ["nombre", "Juan"]
                                         },
                                 "lrel" : "tabla1",
                                 "rrel" : "tabla2"
                                }
                        }
        expected = {"type" : "join",
                    "cond" : {"type" : "and",
                              "values" : [{"type" : "eq","values" : ["edad", 18]},
                                          {"type" : "eq","values" : ["nombre", "Juan"]}]
                             },
                    "lrel" : "tabla1",
                    "rrel" : "tabla2"
                    }
        try:
            res = rulesAR.rule5B(jsonExample)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple1')

    def test_and(self):
        jsonExample = {"type": "sigma",
                       "cond": {"type": "eq",
                                "values": ["edad", 18]
                                },
                       "rel": {"type": "join",
                               "cond": {"type": "and",
                                        "values": [{"type": "eq", "values": ["dni", "11223344T"]},
                                                    {"type": "eq", "values": ["nombre", "Juan"]}]
                                        },
                               "lrel": "tabla1",
                               "rrel": "tabla2"
                               }
                       }
        expected = {"type": "join",
                    "cond": {"type": "and",
                             "values": [{"type": "eq", "values": ["edad", 18]},
                                        {"type": "eq", "values": ["dni", "11223344T"]},
                                        {"type": "eq", "values": ["nombre", "Juan"]}]
                             },
                    "lrel": "tabla1",
                    "rrel": "tabla2"
                    }
        try:
            res = rulesAR.rule5B(jsonExample)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_and')

    def test_or(self):
        jsonExample = {"type": "sigma",
                       "cond": {"type": "eq",
                                "values": ["edad", 18]
                                },
                       "rel": {"type": "join",
                               "cond": {"type": "or",
                                        "values": [{"type": "eq", "values": ["dni", "11223344T"]},
                                                   {"type": "eq", "values": ["nombre", "Juan"]}]
                                        },
                               "lrel": "tabla1",
                               "rrel": "tabla2"
                               }
                       }
        expected = {"type": "join",
                    "cond": {"type": "and",
                             'values': [{'type': 'eq', 'values': ['edad', 18]},
                                        {'type': 'or',
                                          'values': [{'type': 'eq', 'values': ['dni', '11223344T']},
                                                     {'type': 'eq', 'values': ['nombre', 'Juan']}]}]
                             },
                    "lrel": "tabla1",
                    "rrel": "tabla2"
                    }
        try:
            res = rulesAR.rule5B(jsonExample)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_or')

if __name__ == "__main__":
        unittest.main()