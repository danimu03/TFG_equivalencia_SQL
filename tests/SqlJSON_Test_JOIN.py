import unittest
from src.SQL_To_JSON.Sql_To_Json import parse_Sql_To_Json as sql
from src.SQL_To_JSON.Sql_To_Json import ErrorSqlQuery as errsql
from src.Creates_To_JSON.Creates_Json import create_tables_json as create


class SqlJson_Test_JOIN(unittest.TestCase):

    def test_twoTables(self):
        res = sql("SELECT nombre FROM Persona join Jugador on id = pid", create(["create table Persona(id int(2) primary key, nombre varchar2(30));",
                                                                                                     "create table Jugador(pid int(2) primary key);"]))
        expected = {'type': 'pi',
                    'proj': ['Persona1.nombre'],
                    'rel': {'type': 'join',
                            'cond': {'type': 'eq',
                                     'values': ['Persona1.id',
                                                'Jugador1.pid']
                                     },
                            'lrel': {'type': 'rel',
                                     'table': {'type': 'rho',
                                               'ren': ['Persona',
                                                       'Persona1']
                                               }
                                     },
                            'rrel': {'type': 'rel',
                                     'table': {'type': 'rho',
                                               'ren': ['Jugador',
                                                       'Jugador1']
                                               }
                                     }
                            }
                    }

        self.assertEqual(res, expected)

    def test_threeTables(self):
        res = sql("SELECT nombre FROM Persona join Jugador on id = pid join Equipo on eid = ide", create(
            ["create table Persona(id int(2) primary key, nombre varchar2(30))",
             "create table Jugador(pid int(2) primary key, eid int(2))",
             "create table Equipo(ide int(2) primary key)"]))
        expected = {'type': 'pi',
                    'proj': ['Persona1.nombre'],
                    'rel': {'type': 'join',
                            'cond': {'type': 'eq',
                                     'values': ['Persona1.id',
                                                'Jugador1.pid']},
                            'lrel': {'type': 'rel',
                                     'table': {'type': 'rho',
                                               'ren': ['Persona',
                                                       'Persona1']}},
                            'rrel': {'type': 'join',
                                     'cond': {'type': 'eq',
                                              'values': ['Jugador1.eid',
                                                         'Equipo1.ide']},
                                     'lrel': {'type': 'rel',
                                              'table': {'type': 'rho',
                                                        'ren': ['Jugador',
                                                                'Jugador1']}},
                                     'rrel': {'type': 'rel',
                                              'table': {'type': 'rho',
                                                        'ren': ['Equipo',
                                                                'Equipo1']
                                                        }
                                              }
                                     }
                            }
                    }


        self.assertEqual(res, expected)

    def test_twoTablesAmbColumn(self):
        self.assertRaises(errsql, sql, "SELECT nombre FROM Persona join Jugador on id = id", create(
            ["create table Persona(id int(2) primary key, nombre varchar2(30));",
             "create table Jugador(id int(2) primary key);"]))

    def test_threeTablesAmbColumn(self):
        self.assertRaises(errsql, sql, "SELECT nombre FROM Persona join Jugador on id = pid join Equipo on id = id",
                          create(["create table Persona(id int(2) primary key, nombre varchar2(30))",
                                  "create table Jugador(pid int(2) primary key, id int(2))",
                                  "create table Equipo(id int(2) primary key)"]))

    def test_twoTablesAsExpected(self):
        res = sql("SELECT nombre FROM Persona join Jugador on Persona.id = Jugador.id", create(
            ["create table Persona(id int(2) primary key, nombre varchar2(30));",
             "create table Jugador(id int(2) primary key);"]))
        expected = {'type': 'pi',
                    'proj': ['Persona1.nombre'],
                    'rel': {'type': 'join',
                            'cond': {'type': 'eq',
                                     'values': ['Persona1.id',
                                                'Jugador1.id']
                                     },
                            'lrel': {'type': 'rel',
                                     'table': {'type': 'rho',
                                               'ren': ['Persona',
                                                       'Persona1']
                                               }
                                     },
                            'rrel': {'type': 'rel',
                                     'table': {'type': 'rho',
                                               'ren': ['Jugador',
                                                       'Jugador1']
                                               }
                                     }
                            }
                    }

        self.assertEqual(res, expected)

    def test_threeTablesAsExpected(self):
        res = sql("SELECT nombre FROM Persona JOIN Jugador ON Persona.id = Jugador.id JOIN Equipo ON Jugador.eid = Equipo.id",
                  create(["create table Persona(id int(2) primary key, nombre varchar2(30));",
                          "create table Jugador(id int(2) primary key, eid int(2));",
                          "create table Equipo(id int(2) primary key)"]))
        expected = {'type': 'pi',
                    'proj': ['Persona1.nombre'],
                    'rel': {'type': 'join',
                            'cond': {'type': 'eq',
                                     'values': ['Persona1.id',
                                                'Jugador1.id']
                                     },
                            'lrel': {'type': 'rel',
                                     'table': {'type': 'rho',
                                               'ren': ['Persona',
                                                       'Persona1']
                                               }
                                     },
                            'rrel': {'type': 'join',
                                     'cond': {'type': 'eq',
                                              'values': ['Jugador1.eid',
                                                         'Equipo1.id']
                                              },
                                     'lrel': {'type': 'rel',
                                              'table': {'type': 'rho',
                                                        'ren': ['Jugador',
                                                                'Jugador1']
                                                        }
                                              },
                                     'rrel': {'type': 'rel',
                                              'table': {'type': 'rho',
                                                        'ren': ['Equipo',
                                                                'Equipo1']
                                                        }
                                              }
                                     }
                            }
                    }


        self.assertEqual(res, expected)

if __name__ == "__main__":
    unittest.main()
