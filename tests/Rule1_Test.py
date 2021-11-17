import unittest


class TestRule1(unittest.TestCase):

    def test_one(self):
        jsonExample = {'type': 'sigma',
                       'cond': {'type': 'eq',
                                'values': ['edad', 18]},
                       'rel': {'type': 'sigma',
                               'cond': {'type': 'eq',
                                        'values': ['sexo', 'hombre']},
                               'rel': 'Persona'}
                       }
        # res = rule1(jsonExample)
        expected = {'type': 'sigma',
                    'cond': {'type': 'and',
                             'values': [{'type': 'eq',
                                         'values': ['edad', 18]},
                                        {'type': 'eq',
                                         'values': ['hombre', 'sexo']
                                         }]
                             },
                    'rel': 'Persona'}
        self.assertTrue(res == expected)

    def test_two(self):
        jsonExample = {'type': 'sigma',
                       'cond': {'type': 'eq',
                                'values': ['sexo', 'hombre']},
                       'rel': {'type': 'sigma',
                               'cond': {'type': 'eq',
                                        'values': ['nombre', 'Juan']},
                               'rel': 'Personas'
                               }
                       }
        # res = rule1(jsonExample)
        res = {}
        expected = {'type': 'sigma',
                    'cond': {'type': 'and',
                             'values': [{'type': 'eq', 'values': ['sexo', 'hombre']},
                                        {'type': 'eq', 'values': ['Juan', 'nombre']}
                                        ]
                             },
                    'rel': 'Personas'}
        self.assertTrue(res == expected)

    def test_three(self):
        jsonExample = {"type": "sigma",
                       "cond": {"type": "eq",
                                "values": ["edad", 18]},
                       "rel": {{'type': 'sigma',
                                'cond': {'type': 'and',
                                         'values': [{'type': 'eq', 'values': ['sexo', 'hombre']},
                                                    {'type': 'eq', 'values': ['Juan', 'nombre']}
                                                    ]
                                         },
                                'rel': 'Personas'}
                               }
                       }
        # res = rule1(jsonExample)
        res = {}
        expected = {'type': 'sigma',
                    'cond': {'type': 'and',
                             'values': [{'type': 'eq', 'values': ['edad', 18]},
                                        {'type': 'eq', 'values': ['sexo', 'hombre']},
                                        {'type': 'eq', 'values': ['Juan', 'nombre']}
                                        ]
                             },
                    'rel': 'Personas'}
        self.assertTrue(res == expected)


if __name__ == "__main__":
    unittest.main()
