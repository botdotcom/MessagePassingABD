import sqlite3

path = 'reg_db.sqlite'

def dbconnect(path=path):
    conn = sqlite3.connect(path)
    print("Connected")
    return conn

def dbclose(conn):
    conn.commit()
    conn.close()
    print("Disconnected")

# one-time --> uncomment the lines at the end of the program to run this method
def create_table(conn):
    cursor = conn.cursor()
    query = """CREATE TABLE abd (register TEXT PRIMARY KEY, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, value TEXT);"""
    cursor.execute(query)

def reader(conn, register):
    print("Start reader")
    cursor = conn.cursor()
    # print("1")
    query = '''SELECT * FROM abd WHERE register = "{}";'''.format(register)
    # print(query)
    cursor.execute(query)
    # print("Executed")
    row = cursor.fetchone()
    print(row)
    return row

def writer(conn, register, timestamp, value):
    print("Start writer")
    cursor = conn.cursor()
    query = '''INSERT OR REPLACE INTO abd VALUES ("{}", {}, "{}");'''.format(register, timestamp, value)
    cursor.execute(query)
    # print("Executed")
    print("Written ({}, {}) at time {}".format(register, value, timestamp))


# conn = dbconnect()
# print("DB connected...")
# create_table(conn)
# print("Query executed...")
# dbclose(conn)
# print("DB disconnected...")
