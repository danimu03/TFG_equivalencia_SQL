import unittest
import src.SQL_To_JSON.Sql_To_Json as sqlJSON


class SqlJson_Test_CARTESIAN(unittest.TestCase):

    def test_twoTable(self):
        res = sqlJSON.parse_Sql_To_Json("SELECT nombre FROM user JOIN empleado ON dni = dniempleado")
        expected = {'type': 'pi',
                    'proj': ['nombre'],
                    'rel': {'type': 'join',
                            'cond': {'type': 'eq',
                                     'values': ['dni', 'dniempleado']},
                            'lrel': {'type': 'rel',
                                     'table': 'user'},
                            'rrel': {'type': 'rel',
                                     'table': 'empleado'}
                            }
                    }

        self.assertEqual(res, expected)


if __name__ == "__main__":
    unittest.main()
