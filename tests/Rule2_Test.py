import unittest
import rulesAR

class TestRule2(unittest.TestCase):

    def test_numeros(self):
        jsonExample = {'type': 'sigma',
                       'cond': {'type': 'eq',
                                'values': [100, 1]},
                       'rel': {'type': 'sigma',
                               'cond': {'type': 'eq',
                                        'values': [30, 40]},
                               'rel': 'Persona'}
                       }
        expected = {'type': 'sigma',
                    'cond': {'type': 'eq',
                             'values': [1, 100]
                             },
                    'rel': {'type': 'sigma',
                            'cond': {'type': 'eq',
                                     'values': [30, 40]},
                            'rel': 'Persona'
                            }
                    }
        res = rulesAR.rule2(jsonExample)
        self.assertTrue(res == expected)

    def test_numeros_reves(self):
        jsonExample = {'type': 'sigma',
                       'cond': {'type': 'eq',
                                'values': [30, 40]},
                       'rel': {'type': 'sigma',
                               'cond': {'type': 'eq',
                                        'values': [100, 1]},
                               'rel': 'Persona'}
                       }
        expected = {'type': 'sigma',
                    'cond': {'type': 'eq',
                             'values': [1, 100]
                             },
                    'rel': {'type': 'sigma',
                            'cond': {'type': 'eq',
                                     'values': [30, 40]},
                            'rel': 'Persona'
                            }
                    }
        res = rulesAR.rule2(jsonExample)
        self.assertTrue(res == expected)

    def test_palabras(self):
        jsonExample = {'type': 'sigma',
                       'cond': {'type': 'eq',
                                'values': ['nombre', 'juan']},
                       'rel': {'type': 'sigma',
                               'cond': {'type': 'eq',
                                        'values': ['hombre', 'sexo']},
                               'rel': 'Persona'}
                       }
        expected = {'type': 'sigma',
                    'cond': {'type': 'eq',
                             'values': ['hombre', 'sexo']
                             },
                    'rel': {'type': 'sigma',
                            'cond': {'type': 'eq',
                                     'values': ['juan', 'nombre']},
                            'rel': 'Persona'
                            }
                    }
        res = rulesAR.rule2(jsonExample)
        self.assertTrue(res == expected)

    def test_palabras_mayuscula(self):
        jsonExample = {'type': 'sigma',
                       'cond': {'type': 'eq',
                                'values': ['nombre', 'Juan']},
                       'rel': {'type': 'sigma',
                               'cond': {'type': 'eq',
                                        'values': ['hombre', 'sexo']},
                               'rel': 'Persona'}
                       }
        expected = {'type': 'sigma',
                    'cond': {'type': 'eq',
                             'values': ['hombre', 'sexo']
                             },
                    'rel': {'type': 'sigma',
                            'cond': {'type': 'eq',
                                     'values': ['juan', 'nombre']},
                            'rel': 'Persona'
                            }
                    }
        res = rulesAR.rule2(jsonExample)
        self.assertTrue(res == expected)

    def test_palabras_numeros(self):
        jsonExample = {'type': 'sigma',
                       'cond': {'type': 'eq',
                                'values': ['edad', 18]},
                       'rel': {'type': 'sigma',
                               'cond': {'type': 'eq',
                                        'values': ['hombre', 'sexo']},
                               'rel': 'Persona'}
                       }
        expected = {'type': 'sigma',
                    'cond': {'type': 'eq',
                             'values': [18, 'edad']
                             },
                    'rel': {'type': 'sigma',
                            'cond': {'type': 'eq',
                                     'values': ['hombre', 'sexo']},
                            'rel': 'Persona'
                            }
                    }
        res = rulesAR.rule2(jsonExample)
        self.assertTrue(res == expected)

    def test_completo(self):
        jsonExample = {'type': 'sigma',
                       'cond': {'type': 'eq',
                                'values': ['EdAd', 18]},
                       'rel': {'type': 'sigma',
                               'cond': {'type': 'eq',
                                        'values': ['sexo', 'Hombre']},
                               'rel': 'Persona'}
                       }
        expected = {'type': 'sigma',
                    'cond': {'type': 'eq',
                             'values': [18, 'edad']
                             },
                    'rel': {'type': 'sigma',
                            'cond': {'type': 'eq',
                                     'values': ['hombre', 'sexo']},
                            'rel': 'Persona'
                            }
                    }
        res = rulesAR.rule2(jsonExample)
        self.assertTrue(res == expected)

    def test_parecidos(self):
        jsonExample = {'type': 'sigma',
                       'cond': {'type': 'eq',
                                'values': ['apellido2', 'Fernandez']},
                       'rel': {'type': 'sigma',
                               'cond': {'type': 'eq',
                                        'values': ['apellido1', 'Gonzalez']},
                               'rel': 'Persona'}
                       }
        expected = {'type': 'sigma',
                    'cond': {'type': 'eq',
                             'values': ['apellido1', 'gonzalez']
                             },
                    'rel': {'type': 'sigma',
                            'cond': {'type': 'eq',
                                     'values': ['apellido2', 'fernandez']},
                            'rel': 'Persona'
                            }
                    }
        res = rulesAR.rule2(jsonExample)
        self.assertTrue(res == expected)

if __name__ == "__main__":
    unittest.main()