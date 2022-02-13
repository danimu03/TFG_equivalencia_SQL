import unittest
import src.Rules_AR.rulesAR as rulesAR

class TestRule4(unittest.TestCase):

    def test_simple1(self):

        jsonExample = {'type': 'pi',
                        'proj': ['nombre'],
                        'rel': {'type': 'sigma',
                                'cond': {"type": "eq",
                                        "values": ["sexo"]
                                        },
                                'rel': 'Persona'}
                       }
        expected = {'type': 'sigma',
                    'cond': {"type": "eq",
                             "values": ["sexo"]
                            },
                    'rel': {'type': 'pi',
                            'proj': ['nombre'],
                            'rel': 'Persona'}
                    }
        try:
            res = rulesAR.rule4(jsonExample)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple2')

    def test_simple2(self):

        jsonExample = {'type': 'pi',
                        'proj': ['nombre', 'edad', 'sexo'],
                        'rel': {'type': 'sigma',
                                'cond': {"type": "eq",
                                        "values": ["sexo", "hombre"]
                                        },
                                'rel': 'Persona'}
                       }
        expected = {'type': 'sigma',
                    'cond': {"type": "eq",
                             "values": ["sexo", "hombre"]
                            },
                    'rel': {'type': 'pi',
                            'proj': ['nombre', 'edad', 'sexo'],
                            'rel': 'Persona'}
                    }
        try:
            res = rulesAR.rule4(jsonExample)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple2')


if __name__ == "__main__":
        unittest.main()