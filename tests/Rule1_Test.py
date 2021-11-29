import unittest
import rulesAR


class TestRule1(unittest.TestCase):

    def test_simple1(self):
        jsonExample = {'type': 'sigma',
                       'cond': {'type': 'eq',
                                'values': ['edad', 18]},
                       'rel': {'type': 'sigma',
                               'cond': {'type': 'eq',
                                        'values': ['sexo', 'hombre']},
                               'rel': 'Persona'}
                       }
        expected = {'type': 'sigma',
                    'cond': {'type': 'and',
                             'values': [{'type': 'eq', 'values': ['edad', 18]},
                                        {'type': 'eq', 'values': ['hombre', 'sexo']
                                         }]
                             },
                    'rel': 'Persona'}
        try:
            res = rulesAR.rule1(jsonExample)
            self.assertTrue(res == expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple1')

    def test_simple2(self):
        jsonExample = {'type': 'sigma',
                       'cond': {'type': 'eq',
                                'values': ['sexo', 'hombre']},
                       'rel': {'type': 'sigma',
                               'cond': {'type': 'eq',
                                        'values': ['nombre', 'Juan']},
                               'rel': 'Personas'
                               }
                       }
        expected = {'type': 'sigma',
                    'cond': {'type': 'and',
                             'values': [{'type': 'eq', 'values': ['sexo', 'hombre']},
                                        {'type': 'eq', 'values': ['Juan', 'nombre']}
                                        ]
                             },
                    'rel': 'Personas'}
        try:
            res = rulesAR.rule1(jsonExample)
            self.assertTrue(res == expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple2')

    def test_tres_sigmas(self):
        jsonExample = {"type": "sigma",
                       "cond": {"type": "eq",
                                "values": ["edad", 18]},
                       "rel": {'type': 'sigma',
                               'cond': {'type': 'and',
                                        'values': [{'type': 'eq', 'values': ['sexo', 'hombre']},
                                                   {'type': 'eq', 'values': ['Juan', 'nombre']}
                                                   ]
                                        },
                               'rel': 'Personas'}
                       }
        expected = {'type': 'sigma',
                    'cond': {'type': 'and',
                             'values': [{'type': 'eq', 'values': ['edad', 18]},
                                        {'type': 'eq', 'values': ['sexo', 'hombre']},
                                        {'type': 'eq', 'values': ['Juan', 'nombre']}
                                        ]
                             },
                    'rel': 'Personas'}
        try:
            res = rulesAR.rule1(jsonExample)
            self.assertTrue(res == expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_tres_sigmas')

    def test_no_cond(self):
        #Este test es de prueba, pero falla siempre porque cond esta vacío (probamos que salga la excepción)
        jsonExample = {"type": "sigma",
                       "cond": {},
                       "rel": {'type': 'sigma',
                               'cond': {},
                               'rel': 'Personas'}
                       }
        expected = {'type': 'sigma',
                    'cond': {},
                    'rel': 'Personas'}
        try:
            res = rulesAR.rule1(jsonExample)
            self.assertTrue(res == expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_no_cond')

    def test_values_vacio(self):
        jsonExample = {'type': 'sigma',
                       'cond': {'type': 'eq',
                                'values': ['edad', 18]},
                       'rel': {'type': 'sigma',
                               'cond': {'type': 'eq',
                                        'values': []},
                               'rel': 'Persona'}
                       }
        expected = {'type': 'sigma',
                    'cond': {'type': 'eq',
                             'values': ['edad', 18]},
                     'rel': 'Persona'}
        try:
            res = rulesAR.rule1(jsonExample)
            self.assertTrue(res == expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_values_vacio')


if __name__ == "__main__":
    unittest.main()
