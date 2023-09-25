import psycopg2

def ConnectDb(dbname):
    try: 
        connection = psycopg2.connect(
                host="localhost",
                database=dbname,
                user="postgres",
                password="Marcelomanda2020"
            )
        global conn 
        conn = connection
        print("Conectado")
        return True
    except:
        print("Can not connect to db")
        return False

def GetTableInfo(tableName):
    cursor = conn.cursor()
    Q = f"SELECT column_name, data_type, character_maximum_length,column_default FROM information_schema.columns WHERE table_name = '{tableName}';"
    # Q = """SELECT column_name, data_type, is_nullable, column_default,
    #        CASE
    #            WHEN tc.constraint_type = 'PRIMARY KEY' THEN true
    #            ELSE false
    #        END AS is_primary_key
    # FROM information_schema.columns AS c
    # LEFT JOIN information_schema.key_column_usage AS kcu
    # ON c.column_name = kcu.column_name
    # LEFT JOIN information_schema.table_constraints AS tc
    # ON kcu.constraint_name = tc.constraint_name
    # WHERE c.table_name = %s;"""
    try:
        cursor.execute(Q)
        data = cursor.fetchall()
        # print(data[2])
        cols = []
        for i in data:
            cols.append(i)
        return cols
        # return context
        # for field in data:

            # for car in field:
            # print(f'Column Name {field[0]}, data-type: {field[1]}, character_max: {field[2]}, default_value = {field[3]}')

    except Exception as e:
        print('Error getting data info: ',str(e))

def InsertRegisters(query,DBName):
    if ConnectDb(DBName):
        cursor = conn.cursor()

        try:    
            cursor.execute(query)
            conn.commit()
            print("Executed Successfully")
        except Exception as e:
            print("Error : ", str(e))

# ConnectDb('camionera')
# GetTableInfo('drivers')