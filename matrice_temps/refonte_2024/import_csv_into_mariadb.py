from operator import itemgetter

import mariadb
from mariadb import Error
import pandas as pd
import csv
import sys
import random

class trafic_mariadb:
    conn = None
    dict_transfert_forbes = {'num_emp': None, 'nom': None, 'prenom': None, 'anciennete':None,'pref_creneau_deb':None,'pref_creneau_fin':None,'niveau':None}
    dict_transfert = {}
    list_transfert = []
    def __init__(self):
        self.create_connection()
        self.lire_fich()
        self.ecrire_fich()
        self.ajouter_employe()
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



    def lire_fich(self):
        with open('rev2_forbes.csv', newline='\n') as csvfile:
            readr = csv.reader(csvfile, delimiter=',', quotechar='"',skipinitialspace=True)
            i = 0
            for row in readr:
             #renseigner selon les colonnes de la table mariadb + constructions adhoc
                self.list_transfert.append([row[0][:1].upper() + row[1][:1].upper()  + str(row[4]).zfill(3),row[1],row[0],row[7], '2025-1-1 07:00','2025-1-1 15:00',random.randrange(1, 5)])
        print(self.list_transfert)
        self.list_transfert = sorted(self.list_transfert, key=itemgetter(3),reverse=True)
        print(self.list_transfert)

    def ecrire_fich(self):
        liste_unique = []
        f = open("tri_employes.csv", "w+")
        with open(f.name, "a", newline='\n') as csvfile:
            wrtr = csv.writer(csvfile, delimiter=',', quotechar='"')
            i = 0
            for row  in self.list_transfert:
                if row[1] not in liste_unique:
                    liste_unique.append(row[1])
                    wrtr.writerow(row)
        print(liste_unique)

    def ajouter_employe(self):
        # araay qui suit : multiple, h_debut, h_fin

        #chaine_sql = "insert into employes(\"nom\",\"prenom\",\"debut\",\"fin\",\"rang\") values ('"+ nom + "','" + prenom +"','" + hd + "' ,'" + hf + "','" + rang +"')"
#        to_mariadb_req = "insert into employe(num_emp, nom, prenom, anciennete, pref_creneau_deb, pref_creneau_fin, niveau)
#        values('jk_001', 'Kéroack', 'Jacques', 30, '2024-1-1 07:00', '2024-1-1 15:00', 4)";
        c = self.conn.cursor()
        data = pd.read_csv("dict_file.csv", sep=',', encoding="UTF-8")
        # df = pd.DataFrame(data)
        # df.columns = ["num_emp", "nom", "prenom", "anciennete", "pref_creneau_deb", "pref_creneau_fin", "niveau"]
        # for row in df.iterrows():
        #     print (row)
        #
        #     stringExec = "insert into employe(num_emp, nom, prenom, anciennete, pref_creneau_deb, pref_creneau_fin, niveau";
        #     listParams = row
        # try:
        #     c.execute(chaine_sql)
        # except Error:
        #     print(Error)
        # finally:
        #     conn.commit()



if __name__ == '__main__':
    appli = trafic_mariadb();
