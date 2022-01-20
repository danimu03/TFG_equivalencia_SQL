import unittest
import rulesAR



class TestRule3(unittest.TestCase):

    def test_simple1(self):

        jsonExample = { "type" : "pi",
                        "proj" : ["edad"],
                        "rel" : {     "type" : "pi",
                                    "proj" : ["sexo"],
                                    "rel" : "Persona"
                                }       
                        }
        expected = {    "type" : "pi",
                        "proj" : ["edad"],
                        "rel" : "Persona"
                    }
        try:
            res = rulesAR.rule3(jsonExample)
            self.assertTrue(res == expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple1')

if __name__ == "__main__":
    unittest.main()