from mo_sql_parsing import parse
from Creates_To_JSON.Creates_Json import create_tables_json


def check_tables(tables, name):
    ret = 0
    for e in tables:
        if name == e[0]:
            ret += 1
    return ret

def rename_from(json, tables):
    frm = json['from']
    tables = []
    if isinstance(frm, dict):
        aux = []
        aux.append(frm['value'])
        aux.append(frm['name'])
        aux.append(frm['value']+str(check_tables(tables, frm['value'])+1))
        tables.append(aux)
    elif isinstance(frm, list):
        for e in frm:
            if isinstance(e,dict):
                if 'value' in e.keys():
                    aux1 = []
                    aux1.append(e['value'])
                    aux1.append(e['name'])
                    aux1.append(e['value']+str(check_tables(tables, e['value'])+1))
                    tables.append(aux1)
                elif 'join' in e.keys() and isinstance(e['join'], dict):
                    j = e['join']
                    aux1 = []
                    aux1.append(j['value'])
                    aux1.append(j['name'])
                    aux1.append(j['value']+str(check_tables(tables, j['value'])+1))
                    tables.append(aux1)
                else:
                    aux1 = []
                    aux1.append(e['join'])
                    aux1.append('')
                    aux1.append(e['join']+str(check_tables(tables, e['join'])+1))
                    tables.append(aux1)
            else:
                aux2=[]
                aux2.append(e)
                aux2.append("")
                aux2.append(e+str(check_tables(tables, e)+1))
                tables.append(aux2)
    else:
        aux = []
        aux.append(frm)
        aux.append("")
        aux.append(frm+str(check_tables(tables, frm)+1))
        tables.append(aux)

    return tables




def rename_select(json, tables):
    select = json['select']

    if isinstance(select, list):
        None
    else:
        None
    return json




#print(create_tables_json(["create table vuelo(flno number(4,0) primary key, origen varchar2(20), destino varchar2(20), distancia number(6,0), salida date, llegada date, precio number(7,2));", "create table avion(aid number(9,0) primary key, nombre varchar2(30), autonomia number(6,0));"]))
#print(parse("SELECT nombre FROM Jugador j join pepe p  WHERE nombre = aid and nombre = 'pepe'"))

print(parse("SELECT nombre FROM Jugador j join persona p"))
print(rename_from(parse("SELECT nombre FROM Jugador j join persona p"), None))

