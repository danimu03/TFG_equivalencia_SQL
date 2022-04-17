import unittest
import src.Creates_To_JSON.Creates_Json as create


class CreateTables_Test(unittest.TestCase):

    def test_oneTable(self):
        res = create.create_tables_json(["create table vuelo(flno number(4,0) primary key, origen varchar2(20), destino varchar2(20), distancia number(6,0), salida date, llegada date, precio number(7,2));"])
        expected = [{'name': 'vuelo',
                    'columns': [{'name': 'flno', 'type': {'number': [4,0]}, 'primary_key': True},
                                {'name': 'origen', 'type': {'varchar2': 20}},
                                {'name': 'destino', 'type': {'varchar2': 20}},
                                {'name': 'distancia', 'type': {'number': [6, 0]}},
                                {'name': 'salida', 'type': {'date': {}}},
                                {'name': 'llegada', 'type': {'date': {}}},
                                {'name': 'precio', 'type': {'number': [7, 2]}}
                                ]
                    }]

        self.assertEqual(res, expected)

    def test_twoTables(self):
        res = create.create_tables_json(["create table vuelo(flno number(4,0) primary key, origen varchar2(20), destino varchar2(20), distancia number(6,0), salida date, llegada date, precio number(7,2));", "create table avion(aid number(9,0) primary key, nombre varchar2(30), autonomia number(6,0));"])
        expected = [{'name': 'vuelo',
                    'columns': [{'name': 'flno', 'type': {'number': [4,0]}, 'primary_key': True},
                                {'name': 'origen', 'type': {'varchar2': 20}},
                                {'name': 'destino', 'type': {'varchar2': 20}},
                                {'name': 'distancia', 'type': {'number': [6, 0]}},
                                {'name': 'salida', 'type': {'date': {}}},
                                {'name': 'llegada', 'type': {'date': {}}},
                                {'name': 'precio', 'type': {'number': [7, 2]}}]
                     },
                    {'name': 'avion',
                     'columns': [{'name': 'aid', 'type': {'number': [9, 0]}, 'primary_key': True},
                                 {'name': 'nombre', 'type': {'varchar2': 30}},
                                 {'name': 'autonomia', 'type': {'number': [6, 0]}}]
                     }
                    ]

        self.assertEqual(res, expected)

    def test_threeTables(self):
        res = create.create_tables_json(["create table vuelo(flno number(4,0) primary key, origen varchar2(20), destino varchar2(20), distancia number(6,0), salida date, llegada date, precio number(7,2));",
                                         "create table avion(aid number(9,0) primary key, nombre varchar2(30), autonomia number(6,0));",
                                         "create table pasajero(pid number(2,0) primary key, nombre varchar2(30), flno number(4,0));"])
        expected = [{'name': 'vuelo',
                    'columns': [{'name': 'flno', 'type': {'number': [4,0]}, 'primary_key': True},
                                {'name': 'origen', 'type': {'varchar2': 20}},
                                {'name': 'destino', 'type': {'varchar2': 20}},
                                {'name': 'distancia', 'type': {'number': [6, 0]}},
                                {'name': 'salida', 'type': {'date': {}}},
                                {'name': 'llegada', 'type': {'date': {}}},
                                {'name': 'precio', 'type': {'number': [7, 2]}}]
                     },
                    {'name': 'avion',
                     'columns': [{'name': 'aid', 'type': {'number': [9, 0]}, 'primary_key': True},
                                 {'name': 'nombre', 'type': {'varchar2': 30}},
                                 {'name': 'autonomia', 'type': {'number': [6, 0]}}]
                     },
                    {'name': 'pasajero',
                     'columns': [{'name': 'pid', 'type': {'number': [2, 0]}, 'primary_key': True},
                                 {'name': 'nombre', 'type': {'varchar2': 30}},
                                 {'name': 'flno', 'type': {'number': [4, 0]}}]
                     }
                    ]

        self.assertEqual(res, expected)

if __name__ == "__main__":
    unittest.main()