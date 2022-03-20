import unittest
import src.Rules_AR.rulesAR as rulesAR


class TestRule9A(unittest.TestCase):

    def test_simple1(self):
        jsonExample = {'type' :'pro',
                      'lrel' : { 'type':'sigma',
                                  'cond' : {'type' : 'eq',
                                           'values': ['nombre', 'Juan']
                                            },
                                  'rel' : 'Personas'},
                        'rrel' : 'Ganadores'}
        expected = {'type' :'pro',
                      'lrel' : 'Personas',
                        'rrel' : { 'type':'sigma',
                                  'cond' : {'type' : 'eq',
                                           'values': ['nombre', 'Juan']
                                            },
                                  'rel' : 'Ganadores'}
                    }
        try:
            res = rulesAR.rule9A(jsonExample)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple1')



if __name__ == "__main__":
    unittest.main()
