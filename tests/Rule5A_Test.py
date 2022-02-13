import unittest
import src.Rules_AR.rulesAR as rulesAR

class TestRule5A(unittest.TestCase):

    def test_simple1(self):

        jsonExample = {"type": "sigma",
                        "cond": {"type": "eq",
                        "values": ["nombre"]
                                },
                        "rel": {"type": "pro",
                                "lrel": "tabla1",
                                "rrel": "tabla2"
                                }
                        }
        expected = {"type": "join",
                     "cond": {"type": "eq",
                              "values": ["nombre"]
                              },
                     "lrel": "tabla1",
                     "rrel": "tabla2"
                     }
        try:
            res = rulesAR.rule5A(jsonExample)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple1')

    def test_simple2(self):

        jsonExample = {"type": "sigma",
                        "cond": {"type": "eq",
                        "values": ["nombre", "Juan"]
                                },
                        "rel": {"type": "pro",
                                "lrel": "tabla1",
                                "rrel": "tabla2"
                                }
                        }
        expected = {"type": "join",
                     "cond": {"type": "eq",
                              "values": ["nombre", "Juan"]
                              },
                     "lrel": "tabla1",
                     "rrel": "tabla2"
                     }
        try:
            res = rulesAR.rule5A(jsonExample)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple2')

    def test_and(self):

        jsonExample = {"type": "sigma",
                       "cond": {"type": "and",
                                "values": [{ 'type':'eq',
                                             'values':['nombre','Juan']
                                },          {'type':'eq',
                                             'values':['edad', 18]
                                             }
                                           ]
                                },
                       "rel": {"type": "pro",
                               "lrel": "tabla1",
                               "rrel": "tabla2"
                               }
                       }
        expected = {"type": "join",
                    "cond": {"type": "and",
                                "values": [{ 'type':'eq',
                                             'values':['nombre','Juan']
                                },          {'type':'eq',
                                             'values':['edad', 18]
                                             }
                                           ]
                            },
                    "lrel": "tabla1",
                    "rrel": "tabla2"
                    }
        try:
            res = rulesAR.rule5A(jsonExample)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_and')



if __name__ == "__main__":
        unittest.main()