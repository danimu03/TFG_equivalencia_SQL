import unittest
from src.SQL_To_JSON.Sql_To_Json import parse_Sql_To_Json as sql
from src.SQL_To_JSON.Sql_To_Json import ErrorSqlQuery as errsql
from src.Creates_To_JSON.Creates_Json import create_tables_json as create


class SqlJson_Test_CARTESIAN(unittest.TestCase):

    def test_twoTable(self):
        res = sql("SELECT nombre, id FROM Persona, Empr", create([
            "CREATE TABLE Persona(nombre VARCHAR2(30) PRIMARY KEY,"
             "ap1 VARCHAR(10),"
             "ap2 VARCHAR(10),"
             "edad INT(3),"
             "telefono INT(9),"
             "pais VARCHAR(10));",
            "CREATE TABLE Empr (id INT(2) PRIMARY KEY);"
             ]))
        expected = {'type': 'pi',
                    'proj': ['Persona1.nombre',
                             'Empr1.id'],
                    'rel': {'type': 'pro',
                            'lrel': {'type': 'rel',
                                     'table': {'type': 'rho',
                                               'ren': ['Persona',
                                                       'Persona1']}},
                            'rrel': {'type': 'rel',
                                     'table': {'type': 'rho',
                                               'ren': ['Empr',
                                                       'Empr1']
                                               }
                                     }
                            }
                    }

        self.assertEqual(res, expected)

    def test_twoTableAmbColumn(self):
        self.assertRaises(errsql, sql, "SELECT nombre, nombre FROM Persona, Empr", create([
            "CREATE TABLE Persona(nombre VARCHAR2(30) PRIMARY KEY,"
            "ap1 VARCHAR(10),"
            "ap2 VARCHAR(10),"
            "edad INT(3),"
            "telefono INT(9),"
            "pais VARCHAR(10));",
            "CREATE TABLE Empr (nombre VARCHAR(20) PRIMARY KEY);"
        ]))

    def test_twoTableSameColumnAsExpected(self):
        res = sql("SELECT Persona.nombre, Empr.nombre FROM Persona, Empr", create([
            "CREATE TABLE Persona(nombre VARCHAR2(30) PRIMARY KEY,"
             "ap1 VARCHAR(10),"
             "ap2 VARCHAR(10),"
             "edad INT(3),"
             "telefono INT(9),"
             "pais VARCHAR(10));",
            "CREATE TABLE Empr (nombre VARCHAR(20) PRIMARY KEY);"
             ]))
        expected = {'type': 'pi',
                    'proj': ['Persona1.nombre',
                             'Empr1.nombre'],
                    'rel': {'type': 'pro',
                            'lrel': {'type': 'rel',
                                     'table': {'type': 'rho',
                                               'ren': ['Persona',
                                                       'Persona1']}},
                            'rrel': {'type': 'rel',
                                     'table': {'type': 'rho',
                                               'ren': ['Empr',
                                                       'Empr1']
                                               }
                                     }
                            }
                    }

        self.assertEqual(res, expected)

    def test_threeTable(self):
        res = sql("SELECT nombre, id, dep FROM Persona, Empr, Dep", create([
            "CREATE TABLE Persona(nombre VARCHAR2(30) PRIMARY KEY,"
             "ap1 VARCHAR(10),"
             "ap2 VARCHAR(10),"
             "edad INT(3),"
             "telefono INT(9),"
             "pais VARCHAR(10));",
            "CREATE TABLE Empr (id INT(2) PRIMARY KEY);",
            "CREATE TABLE Dep (dep INT(10) PRIMARY KEY);"
             ]))
        expected = {'type': 'pi',
                    'proj': ['Persona1.nombre',
                             'Empr1.id',
                             'Dep1.dep'],
                    'rel': {'type': 'pro',
                            'lrel': {'type': 'rel',
                                     'table': {'type': 'rho',
                                               'ren': ['Persona',
                                                       'Persona1']
                                               }
                                     },
                        'rrel': {'type': 'pro',
                                 'lrel': {'type': 'rel',
                                          'table': {'type': 'rho',
                                                    'ren': ['Empr',
                                                            'Empr1']
                                                    }
                                          },
                                 'rrel': {'type': 'rel',
                                          'table': {'type': 'rho',
                                                    'ren': ['Dep',
                                                            'Dep1']
                                                    }
                                          }
                                 }
                            }
                    }

        self.assertEqual(res, expected)

    def test_twoTableWhereAmbColumn(self):
        self.assertRaises(errsql, sql, "SELECT nombre, ap1, ap2 FROM Empl, Proyecto WHERE id=idDir", create(
            ["create table Empl(id int(2) primary key, nombre varchar(10), ap1 varchar(10), ap2 varchar(10), dni varchar(10))",
             "create table Proyecto(id int(2), nombre varchar(30), idDir int(2))"]))

    def test_twoTableWhereAmbColumn2(self):
        self.assertRaises(errsql, sql, "SELECT Empl.nombre, ap1, ap2 FROM Empl, Proyecto WHERE id=idDir", create(
            ["create table Empl(id int(2) primary key, nombre varchar(10), ap1 varchar(10), ap2 varchar(10), dni varchar(10))",
             "create table Proyecto(id int(2), nombre varchar(30), idDir int(2))"]))

    def test_twoTableWhereAmbColumn3(self):
        self.assertRaises(errsql, sql, "SELECT nombre, ap1, ap2 FROM Empl, Proyecto WHERE Empl.id=idDir", create(
            ["create table Empl(id int(2) primary key, nombre varchar(10), ap1 varchar(10), ap2 varchar(10), dni varchar(10))",
             "create table Proyecto(id int(2), nombre varchar(30), idDir int(2))"]))

    def test_twoTableWhere(self):
        res = sql("SELECT Empl.nombre, ap1, ap2 FROM Empl, Proyecto WHERE Empl.id=idDir", create(
            ["create table Empl(id int(2) primary key, nombre varchar(10), ap1 varchar(10), ap2 varchar(10), dni varchar(10))",
             "create table Proyecto(id int(2), nombre varchar(30), idDir int(2))"]))
        expected = {'type': 'pi',
                    'proj': ['Empl1.nombre',
                             'Empl1.ap1',
                             'Empl1.ap2'],
                    'rel': {'type': 'sigma',
                            'cond': {'type': 'eq',
                                     'values': ['Empl1.id',
                                                'Proyecto1.idDir']
                                     },
                            'rel': {'type': 'pro',
                                    'lrel': {'type': 'rel',
                                             'table': {'type': 'rho',
                                                       'ren': ['Empl',
                                                               'Empl1']
                                                       }
                                             },
                                    'rrel': {'type': 'rel',
                                             'table': {'type': 'rho',
                                                       'ren': ['Proyecto',
                                                               'Proyecto1']
                                                       }
                                             }
                                    }
                            }
                    }


        self.assertEqual(res, expected)


if __name__ == "__main__":
    unittest.main()
