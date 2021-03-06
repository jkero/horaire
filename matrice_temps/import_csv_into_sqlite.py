import sqlite3
from sqlite3 import Error
import pandas
import pandas as pd
import csv

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        if conn is not None:
            # create projects table
           lire_fich(conn)
        else:
            print("Error! cannot create the database connection.")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def main():
    with open("athletes.csv", "r", encoding="UTF-8") as f:
        for line in f:
            print(f.readline())
    f.close()

    fields = ['Name']
    le_data = pandas.read_csv('athletes.csv', usecols=fields)

def lire_fich(conn):
        cpt=0
        with open('athletes.csv', encoding="UTF-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                s = (row['Name'].strip().replace('\'', ''))
                r = row['Rank']
                if " " in s:
                    a,b,*_ = s.split(" ")
                cpt = cpt+1
                print(str(cpt) + ": "+  a + " " + b)
                ajouter_employe(conn, cpt, b, a, r)

def ajouter_employe(conn, cpt, nom, prenom, rang):
    # araay qui suit : multiple, h_debut, h_fin
    criteres_affect = [[14,'5','13'],[9,'8','16'],[13,'12','20']]
    hd = '0'
    hf = '0'
    # quart par : defaut ne refere pas a table emp_non_dispo. pas de fk non-dispo
    if cpt % criteres_affect[0][0] == 0:
        hd = criteres_affect[0][1]
        hf = criteres_affect[0][2]
    elif cpt % criteres_affect[1][0] == 0:
        hd = criteres_affect[1][1]
        hf = criteres_affect[1][2]
    elif cpt % criteres_affect[2][0] == 0:
        hd = criteres_affect[2][1]
        hf = criteres_affect[2][2]

    chaine_sql = "insert into employes(\"nom\",\"prenom\",\"debut\",\"fin\",\"rang\") values ('"+ nom + "','" + prenom +"','" + hd + "' ,'" + hf + "','" + rang +"')"
    print(chaine_sql)
    c = conn.cursor()
    try:
        c.execute(chaine_sql)
    except Error:
        print(Error)
    finally:
        conn.commit()



if __name__ == '__main__':
    create_connection(r"C:\Users\j\Documents\pythonProject\matrice_temps\letemps.db")