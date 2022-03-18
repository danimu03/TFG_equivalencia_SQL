from mo_sql_parsing import parse


#recibe una lista de sentencias creates y devuelve una lista de sentencias hardcodeadas
#in->  ["create table..." , "create table..."]
#out -> [{name:example, columns[...]}, {name:example, columns[...]}]
def create_tables_json(creates):
    list_of_creates= []
    for e in creates:
        dict = parse(e)
        list_of_creates.append(dict["create table"])
    return list_of_creates

#es necesario controlar que el parametro de entrada unicamente tenga creates. Excepcion

#print(create_tables_json(["create table vuelo(flno number(4,0) primary key, origen varchar2(20), destino varchar2(20), distancia number(6,0), salida date, llegada date, precio number(7,2));", "create table avion(aid number(9,0) primary key, nombre varchar2(30), autonomia number(6,0));"]))