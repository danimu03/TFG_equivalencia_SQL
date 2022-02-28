import unittest
import src.SQL_To_JSON.Sql_To_Json as sqlJSON


class SqlJson_Test_Exceptions(unittest.TestCase):

    def test_neqException2(self):
        self.assertRaises(sqlJSON.ErrorSqlQuery, sqlJSON.parse_Sql_To_Json, "SELECT Nombre, direccion FROM usuario WHERE pais != \"España\"")

    def test_neqException(self):
        self.assertRaises(sqlJSON.ErrorSqlQuery, sqlJSON.parse_Sql_To_Json, "SELECT Nombre, direccion FROM usuario WHERE pais != \"España\"")

    def test_ltException(self):
        self.assertRaises(sqlJSON.ErrorSqlQuery, sqlJSON.parse_Sql_To_Json, "SELECT Nombre, direccion FROM usuario WHERE id < 3456")

    def test_gtException(self):
        self.assertRaises(sqlJSON.ErrorSqlQuery, sqlJSON.parse_Sql_To_Json, "SELECT Nombre, direccion FROM usuario WHERE id < 3456")

    def test_lteException(self):
        self.assertRaises(sqlJSON.ErrorSqlQuery, sqlJSON.parse_Sql_To_Json, "SELECT Nombre, direccion FROM usuario WHERE id <= 3456")

    def test_gteException(self):
        self.assertRaises(sqlJSON.ErrorSqlQuery, sqlJSON.parse_Sql_To_Json, "SELECT Nombre, direccion FROM usuario WHERE pais >= \"España\"")

    def test_orException(self):
        self.assertRaises(sqlJSON.ErrorSqlQuery, sqlJSON.parse_Sql_To_Json, "SELECT Nombre, direccion FROM usuario WHERE pais = \"España\" OR id = 1")

    def test_groupbyException(self):
        self.assertRaises(sqlJSON.ErrorSqlQuery, sqlJSON.parse_Sql_To_Json, "SELECT Nombre, direccion FROM usuario, persona, movil WHERE pais = \"España\" and num = 1 GROUP BY name")





if __name__ == "__main__":
    unittest.main()