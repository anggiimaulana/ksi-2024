import cx_Oracle

def get_db_connection():
    try:
        dsn = cx_Oracle.makedsn('localhost', '1521', 'XE') 
        connection = cx_Oracle.connect('system', 'anggi1307', dsn)
        return connection
    except cx_Oracle.Error as e:
        return None  