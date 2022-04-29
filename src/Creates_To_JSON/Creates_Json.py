from mo_sql_parsing import parse

class ErrorCreatesSQL(ValueError):
    """
    Own exception
    """
    def __init__(self, message, *args):         
        super(ErrorCreatesSQL, self).__init__(message, *args)

#recibe una lista de sentencias creates y devuelve una lista de sentencias hardcodeadas
#in->  ["create table..." , "create table..."]
#out -> [{name:example, columns[...]}, {name:example, columns[...]}]
def create_tables_json(creates):
    """
    Transforms the DDL creates to JSON format

    :param pre: list of DDL creates
    :return: list of dict
    """
    list_of_creates= []
    for e in creates:
        dict = parse(e)
        if "create table" in dict.keys():
            list_of_creates.append(dict["create table"])
        else:
            raise ErrorCreatesSQL("ONLY DDL CREATES SUPPORTED")
    return list_of_creates



