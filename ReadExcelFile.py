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
def getData():
    df = pd.read_excel('LibroPrueba.xlsx',sheet_name='Hoja2')
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
    return str_final



#Connect to the Database
def connect ():
    try:
        connection = psycopg2.connect(
            host="localhost",
            database="test",
            user="postgres",
            password="Admin4"
        )
        global conn 
        conn = connection
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
        
connect()
getData()
flota_vehicular = getData()
# InsertConductor(flota_vehicular)