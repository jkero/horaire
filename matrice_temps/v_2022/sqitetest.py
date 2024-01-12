import sqlite3

from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        if conn is not None:
            # create projects table
            select_all(conn)
        else:
            print("Error! cannot create the database connection.")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def select_all(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM employes")

    rows = cur.fetchall()

    for row in rows:
        print(row)

if __name__ == '__main__':
    create_connection(r"C:\Users\j\Documents\pythonProject\matrice_temps\letemps.db")