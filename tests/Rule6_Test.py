import unittest
import src.Rules_AR.rulesAR as rulesAR


class TestRule6(unittest.TestCase):

    def test_simple1(self):

        jsonExample = {'type' : 'pro',
                       'lrel' : {'type': 'rho', 'ren': ['Personas', 'Personas1']},
                       'rrel' : {'type': 'rho', 'ren': ['Jugadores', 'Jugadores1']}}
        expected = {'type' : 'pro',
                    'lrel' : {'type': 'rho', 'ren': ['Jugadores', 'Jugadores1']},
                    'rrel' : {'type': 'rho', 'ren': ['Personas', 'Personas1']}}
        try:
            res = rulesAR.rule6(jsonExample)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple1')


if __name__ == "__main__":
    unittest.main()