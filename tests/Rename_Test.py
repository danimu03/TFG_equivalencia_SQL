import unittest
from mo_sql_parsing import parse
from src.SQL_To_JSON.Sql_To_Json import parse_Sql_To_Json as sql
import src.SQL_To_JSON.renameSQL as ren
from src.Creates_To_JSON.Creates_Json import create_tables_json as create


class Rename_Test(unittest.TestCase):

    def test_addId(self):
        #res = ren.rename_json(parse("SELECT nombre FROM Persona"), create.create_tables_json(["create table Persona(nombre varchar2(30) primary key);"]))
        res = sql("SELECT nombre from Persona", create(
            ["create table Persona(nombre varchar2(30) primary key);"]
        ))
        # formato parse
        # expected = {'select': {'value': 'Persona1.nombre'},'from': {'value': 'Persona','name': 'Persona1'}}
        # formato sql_to_json
        expected = {'type': 'pi', 'proj': ['Persona1.nombre'], 'rel': {'type': 'rel', 'table': {'type': 'rho', 'ren': ['Persona', 'Persona1']}}}

        self.assertEqual(res, expected)

    def test_Persona(self):
        #res = ren.rename_json(parse("SELECT Persona.nombre FROM Persona"), create.create_tables_json(["create table Persona(nombre varchar2(30) primary key);"]))
        res = sql("SELECT Persona.nombre FROM Persona", create(
            ["create table Persona(nombre varchar2(30) primary key);"]
        ))
        # formato parse
        # expected = {'select': {'value': 'Persona1.nombre'},'from': {'value': 'Persona','name': 'Persona1'}}
        # formato sql_to_json
        expected = {'type': 'pi', 'proj': ['Persona1.nombre'], 'rel': {'type': 'rel', 'table': {'type': 'rho', 'ren': ['Persona', 'Persona1']}}}

        self.assertEqual(res, expected)

    def test_p(self):
        res = sql("SELECT p.nombre FROM Persona p", create(
            ["create table Persona(nombre varchar2(30) primary key);"]
        ))

        expected = {'type': 'pi', 'proj': ['Persona1.nombre'], 'rel': {'type': 'rel', 'table': {'type': 'rho', 'ren': ['Persona', 'Persona1']}}}

        self.assertEqual(res, expected)

    def test_pj(self): #falla el renombramiento del JOIN
        res = sql("SELECT p.nombre FROM Jugador j join Persona p on nombre = nombre", create(
            ["create table Jugador(nombre varchar2(30) primary key);",
             "create table Persona(nombre varchar2(30) primary key);"]
        ))

        expected = ""

        self.assertEqual(res, expected)

    def test_sameRename(self):
        self.assertRaises(ren.ErrorRenameSQL, ren.rename_json, parse("SELECT p.nombre FROM Jugador p join persona p"), create(["create table Jugador(nombre varchar2(30) primary key);", "create table Persona(nombre varchar2(30) primary key);" ]))

    def test_ambColumn(self): #esta realmente no es de renombramiento
        self.assertRaises(ren.ErrorRenameSQL, ren.rename_json, parse("SELECT nombre, dni FROM Jugador  join persona "), create(["create table Jugador(nombre varchar2(30) primary key);", "create table persona(nombre varchar2(30),dni varchar2(30) primary key);" ]))



if __name__ == "__main__":
    unittest.main()