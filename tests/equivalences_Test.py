import unittest
import src.Creates_To_JSON.Creates_Json as creates
import src.equivalence as equi


class SQL_Equivalence(unittest.TestCase):

    def test_simple1(self):

        try:
            query1 = "Select persona.nombre from Personas persona"
            query2 = "Select p.nombre from Personas p"
            tablas = ["create table Personas(dni number(4,0) primary key, edad varchar2(20), nombre varchar2(20), equipo varchar2(30));",
                        "create table Ganadores(dni number(9,0) primary key, equipo varchar2(30), premio varchar2(20));"]
            res = equi.equivalence(query1, query2, tablas)
            soluciones = ['Equivalentes', 'No sabemos', 'Equivalentes salvo renombramiento']
            self.assertEqual(res, soluciones[0])
        except TypeError as e:
            print(e)

    def test_simple2(self):

        try:
            query1 = "Select persona.nombre, persona.edad from Personas persona"
            query2 = "Select p.edad, p.nombre from Personas p"
            tablas = ["create table Personas(dni number(4,0) primary key, edad varchar2(20), nombre varchar2(20), equipo varchar2(30));",
                        "create table Ganadores(dni number(9,0) primary key, equipo varchar2(30), premio varchar2(20));"]
            res = equi.equivalence(query1, query2, tablas)
            soluciones = ['Equivalentes', 'No sabemos', 'Equivalentes salvo renombramiento']
            self.assertEqual(res, soluciones[0])
        except TypeError as e:
            print(e)

    def test_simple3(self):

        try:
            query1 = "Select persona.nombre, ganador.premio from Personas persona JOIN Ganadores ganador ON persona.equipo = ganador.equipo"
            query2 = "Select ganador.premio, persona.nombre from  Ganadores ganador JOIN Personas persona ON persona.equipo = ganador.equipo"
            tablas = ["create table Personas(dni number(4,0) primary key, edad varchar2(20), nombre varchar2(20), equipo varchar2(30));",
                        "create table Ganadores(dni number(9,0) primary key, equipo varchar2(30), premio varchar2(20));"]
            res = equi.equivalence(query1, query2, tablas)
            soluciones = ['Equivalentes', 'No sabemos', 'Equivalentes salvo renombramiento']
            self.assertEqual(res, soluciones[0])
        except TypeError as e:
            print(e)

    def test_simple4(self):

        try:
            query1 = "Select p.nombre, g.premio from Personas p JOIN Ganadores g ON p.equipo = g.equipo"
            query2 = "Select ganador.premio, persona.nombre from  Ganadores ganador JOIN Personas persona ON persona.equipo = ganador.equipo"
            tablas = ["create table Personas(dni number(4,0) primary key, edad varchar2(20), nombre varchar2(20), equipo varchar2(30));",
                        "create table Ganadores(dni number(9,0) primary key, equipo varchar2(30), premio varchar2(20));"]
            res = equi.equivalence(query1, query2, tablas)
            soluciones = ['Equivalentes', 'No sabemos', 'Equivalentes salvo renombramiento']
            self.assertEqual(res, soluciones[0])
        except TypeError as e:
            print(e)

    def test_simple5(self):

        try:
            query1 = "Select p1.nombre, p2.nombre from Personas p1 JOIN Personas p2 ON p1.edad = p2.edad"
            query2 = "Select p2.nombre, p1.nombre from Personas p1 JOIN Personas p2 ON p1.edad = p2.edad"
            tablas = ["create table Personas(dni number(4,0) primary key, edad varchar2(20), nombre varchar2(20), equipo varchar2(30));",
                        "create table Ganadores(dni number(9,0) primary key, equipo varchar2(30), premio varchar2(20));"]
            res = equi.equivalence(query1, query2, tablas)
            soluciones = ['Equivalentes', 'No sabemos', 'Equivalentes salvo renombramiento']
            self.assertEqual(res, soluciones[0])
        except TypeError as e:
            print(e)

    def test_simple6(self):

        try:
            query1 = "Select p1.nombre, p2.nombre from Personas p1, Personas p2, Ganadores g1, Ganadores g2 Where p1.equipo = g1.equipo and p2.equipo = g2.equipo"
            query2 = "Select p1.nombre, p2.nombre from Personas p1, Personas p2, Ganadores g1, Ganadores g2 Where p1.equipo = g2.equipo and p2.equipo = g1.equipo"
            tablas = ["create table Personas(dni number(4,0) primary key, edad varchar2(20), nombre varchar2(20), equipo varchar2(30));",
                        "create table Ganadores(dni number(9,0) primary key, equipo varchar2(30), premio varchar2(20));"]
            res = equi.equivalence(query1, query2, tablas)
            soluciones = ["Equivalentes", "No sabemos", "Equivalentes salvo renombramiento"]
            self.assertEqual(res, soluciones[2])
        except TypeError as e:
            print(e)


    def test_simple7(self):

        try:
            query1 = "Select p1.nombre, p2.edad From Personas p1, Personas p2 Where p1.nombre = p2.nombre"
            query2 = "Select p1.nombre from Personas "
            tablas = ["create table Personas(dni number(4,0) primary key, edad varchar2(20), nombre varchar2(20), equipo varchar2(30));",
                        "create table Ganadores(dni number(9,0) primary key, equipo varchar2(30), premio varchar2(20));"]
            res = equi.equivalence(query1, query2, tablas)
            soluciones = ["Equivalentes", "No sabemos", "Equivalentes salvo renombramiento"]
            self.assertEqual(res, soluciones[1])
        except TypeError as e:
            print(e)

    def test_simple8(self):
        try:
            query1 = "Select mp.nombre From Empresas mp, Trabajadores trab Where mp.empleados = 14 and trab.oficio = 'informatico'"
            query2 = "Select e.nombre From Empresas e, Trabajadores t where 14 = e.empleados And 'informatico' = t.oficio"
            tablas = ["create table Personas(dni number(4,0) primary key, edad varchar2(20), nombre varchar2(20), equipo varchar2(30));",
                        "create table Trabajadores(dni number(9,0) primary key, puesto varchar2(30), oficio varchar2(20));",
                      "create table Empresas(nif number(8, 0) primary key, nombre varchar2(30), empleados varchar2(15));"]
            res = equi.equivalence(query1, query2, tablas)
            soluciones = ["Equivalentes", "No sabemos", "Equivalentes salvo renombramiento"]
            self.assertEqual(res, soluciones[0])
        except TypeError as e:
            print(e)

    def test_simple9(self):
        try:
            query1 = "Select mp.nombre From Empresas mp"
            query2 = "Select t.dni From Trabajadores t where 'informatico' = t.oficio"
            tablas = ["create table Personas(dni number(4,0) primary key, edad varchar2(20), nombre varchar2(20), equipo varchar2(30));",
                        "create table Trabajadores(dni number(9,0) primary key, puesto varchar2(30), oficio varchar2(20));",
                      "create table Empresas(nif number(8, 0) primary key, nombre varchar2(30), empleados varchar2(15));"]
            res = equi.equivalence(query1, query2, tablas)
            soluciones = ["Equivalentes", "No sabemos", "Equivalentes salvo renombramiento"]
            self.assertEqual(res, soluciones[1])
        except TypeError as e:
            print(e)

if __name__ == "__main__":
    unittest.main()