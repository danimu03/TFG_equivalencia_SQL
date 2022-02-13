import unittest
import src.Rules_AR.rulesAR as rulesAR


class TestRule3(unittest.TestCase):

    def test_simple1(self):

        jsonExample = {"type": "pi",
                       "proj": ["edad"],
                       "rel": {"type": "pi",
                               "proj": ["sexo"],
                               "rel": "Persona"
                               }
                       }
        expected = {"type": "pi",
                    "proj": ["edad"],
                    "rel": "Persona"
                    }
        try:
            res = rulesAR.rule3(jsonExample)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple1')

    def test_simple2(self):
        jsonExample = {"type": "pi",
                       "proj": ["nombre", "edad"],
                       "rel": {"type": "pi",
                               "proj": ["apellidos", "dni"],
                               "rel": "Persona"
                               }
                       }
        expected = {"type": "pi",
                    "proj": ["nombre", "edad"],
                    "rel": "Persona"
                    }
        try:
            res = rulesAR.rule3(jsonExample)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple2')


if __name__ == "__main__":
    unittest.main()
