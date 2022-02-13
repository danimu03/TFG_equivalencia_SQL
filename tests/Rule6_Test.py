import unittest
import src.Rules_AR.rulesAR as rulesAR


class TestRule6(unittest.TestCase):

    def test_simple1(self):

        jsonExample = {'type' : 'pro',
                       'lrel' : 'Personas',
                       'rrel' : 'Jugadores'}
        expected = {'type' : 'pro',
                    'lrel' : 'Jugadores',
                    'rrel' : 'Personas'}
        try:
            res = rulesAR.rule6(jsonExample)
            self.assertEqual(res, expected)
        except TypeError as e:
            print(e)
            print('He fallado yo: test_simple1')


if __name__ == "__main__":
    unittest.main()