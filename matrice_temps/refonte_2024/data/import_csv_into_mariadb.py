from operator import itemgetter

import mariadb
import csv
import sys
import random

class trafic_mariadb:
    conn = None
    dict_transfert = {}
    list_transfert = []
    liste_unique = []
    def __init__(self):
        self.lire_fich_csv()
        self.ecrire_fich_pour_load()
        self.ajouter_employe_dans_db()
    def create_connection(self):
        """ create a database connection to a SQLite database """
        # Connect to MariaDB Platform
        try:
            self.conn = mariadb.connect(
                user="jack",
                password="yoyo",
                host="localhost",
                port=3306,
                database="horaire"
            )
        except mariadb.Error as e:
            print(f"Error connecting to MariaDB Platform: {e}")
            sys.exit(1)

    def lire_fich_csv(self):
        with open('rev2_forbes.csv', newline='\n') as csvfile:
            readr = csv.reader(csvfile, delimiter=',', quotechar='"',skipinitialspace=True)
            i = 0
            for row in readr:
             #renseigner selon les colonnes de la table mariadb + constructions adhoc
                self.list_transfert.append([row[0][:1].upper() + row[1][:1].upper()  + str(row[4]).zfill(3),row[1],row[0],row[7], '2025-1-1 07:00','2025-1-1 15:00',random.randrange(1, 5)])
        print(self.list_transfert)
        self.list_transfert = sorted(self.list_transfert, key=itemgetter(3),reverse=True)
        print(self.list_transfert)

    def ecrire_fich_pour_load(self):
        liste_unique = []
        liste_transfert = []
        f = open("tri_employes.csv", "w+")
        with open(f.name, "a", newline='\n') as csvfile:
            wrtr = csv.writer(csvfile, delimiter=',', quotechar='"')
            i = 0
            for row  in self.list_transfert:
                if row[1] not in liste_unique:
                    #pas de doublons dans les noms -source hétéroclite
                    liste_unique.append(row[1])
                    liste_transfert.append(row)
                    wrtr.writerow(row)
        print(liste_unique)
        self.liste_transfert = liste_transfert

    def ajouter_employe_dans_db(self):
        """ plus simple de le faire via mariadb command line load infile"""
        self.create_connection()
        le_curseur = self.conn.cursor()
        print(type(le_curseur))
        string_insert = "insert into employe_kill_me (num_emp, nom, prenom,anciennete,pref_creneau_deb,pref_creneau_fin,niveau) values (?,?,?,?,?,?,?)"
        try:
            for emp in self.liste_transfert:
                le_curseur.execute(string_insert, (emp[0],emp[1],emp[2],emp[3],emp[4],emp[5],emp[6]))
        except Exception as e:
            print(e)
        finally:
            self.conn.commit()
            self.conn.close()


if __name__ == '__main__':
    appli = trafic_mariadb();
