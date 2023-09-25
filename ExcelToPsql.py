#Requires pandas, xlrd, openpyxl

import pandas as pd
import psycopg2

#Mejoras 
#Obtener el orden de las columnas en el Excel
#Obtener las columnas de la base de datos
#Cambiar el orden de los campos a ingresar 
#Hacerlo en PyQt6 y generar el ejecutable una vez este listo
#Opcional: Permitir Crear la base de datos en caso que no este creada.



# # print(df.__len__())
# # for rows in df.itertuples():
# #     print(type(rows))
# # print(type(df))


# print(df_to_dict)
# # print(f'Dict len: {len(df_to_dict)}')
# # print(f'List of COlumn Headers: {df_to_dict.keys()}')


# #Obtener los Headers de la tabla
# for head in df_to_dict.keys():
#     print(head)
#     print(df_to_dict[head])
#     print("------------------")


# print(type(conductores_list))

#Iterate on the Excel table
def getData(filename):
    file_name = filename + '.xlsx'
    df = pd.read_excel(filename)
    df_to_dict = df.to_dict('list')
    headers = [header for header in df_to_dict.keys()]
    first_head  = headers[0]
    last_head = headers[len(headers)-1]
    n_values = len(df_to_dict[headers[0]])
    str_insert = ''
    str_els = ''
    str_final = ''
    for n in range(n_values):
        str_els = ''
        for head in headers:
            if head == last_head:
                str_el = f"'{df_to_dict[head][n]}'"
            else:
                str_el = f"'{df_to_dict[head][n]}'" + ','
            str_els = str_els + str_el
        if n == n_values-1:
        
            str_insert = "("+str_els + ");"
        else:
            str_insert = "("+str_els + "),"
        str_final = str_final + str_insert 
    print(str_final)
    context = {
        'str-db': str_final,
        'headers':headers
    }
    return context



#Connect to the Database
def connect ():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="camionera",
            user="postgres",
            password="Marcelomanda2020"
        )
        global conn 
        conn = connection
        print("Conectado")
    except:
        print("Can not connect to db")

#Insert the data on the Table
def InsertConductor(nombre):
    cursor = conn.cursor()
    Q = f"INSERT INTO camiones (placa,marca) VALUES {nombre}"
    try:
        if cursor.execute(Q) is None:
            conn.commit()
    except:
        print("Error with the insert")
        
def getTableInfo(TableName):
    cursor = conn.cursor()
    Q = f"SELECT column_name, data_type, character_maximum_length,column_default FROM information_schema.columns WHERE table_name = '{TableName}';"
    try:
        cursor.execute(Q)
        data = cursor.fetchall()
        print(data)
    except:
        print('Error with \d')
# connect()
# getTableInfo('drivers')
# getData()
# flota_vehicular = getData()
# print(flota_vehicular)
# InsertConductor(flota_vehicular)
#All the data that we can get from the DB 
#table_catalog | table_schema | table_name | column_name | ordinal_position | column_default | is_nullable |     data_type     | character_maximum_length | character_octet_length | numeric_precision | numeric_precision_radix | numeric_scale | datetime_precision | interval_type | interval_precision | character_set_catalog | character_set_schema | character_set_name | collation_catalog | collation_schema | collation_name | domain_catalog | domain_schema | domain_name | udt_catalog | udt_schema | udt_name | scope_catalog | scope_schema | scope_name | maximum_cardinality | dtd_identifier | is_self_referencing | is_identity | identity_generation | identity_start | identity_increment | identity_maximum | identity_minimum | identity_cycle | is_generated | generation_expression | is_updatable 