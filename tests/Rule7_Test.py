import unittest
import src.Rules_AR.rulesAR as rulesAR


class TestRule6(unittest.TestCase):

    def test_simple1(self):

        jsonExample = {"type" : "join",
                        "cond" : {"type" : "eq",
                                  "values" : ["nombre", "Juan"]
                                  },
                        "lrel" : "Personas",
                        "rrel" : "Jugadores"
                       }
        expected = {"type" : "join",
                    "cond" : {"type" : "eq",
                              "values" : ["nombre", "Juan"]
                              },
                    "lrel" : "Jugadores",
                    "rrel" : "Personas"
                   }
        try:
            res = rulesAR.rule7(jsonExample)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple1')


if __name__ == "__main__":
    unittest.main()