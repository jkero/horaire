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
        #self.lire_fich_csv()
        #self.ecrire_fich_pour_load()
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
        import random

        ze_liste = list([
['TL099', 'Tremblay', 'Léo', 99, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['GG083', 'Gagnon', 'Gabriel', 83, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['RR089', 'Roy', 'Raphaël', 89, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['CA008', 'Côté', 'Arthur', 8, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['BL039', 'Bouchard', 'Louis', 39, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['GJ066', 'Gauthier', 'Jules', 66, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['MA025', 'Morin', 'Adam', 25, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['LM073', 'Lavoie', 'Maël', 73, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['FL087', 'Fortin', 'Lucas', 87, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['GH008', 'Gagné', 'Hugo', 8, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['ON011', 'Ouellet', 'Noah', 11, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['PL090', 'Pelletier', 'Liam', 90, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['BG027', 'Bélanger', 'Gabin', 27, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['LS067', 'Lévesque', 'Sacha', 67, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['BP027', 'Bergeron', 'Paul', 27, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['LN085', 'Leblanc', 'Nathan', 85, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['PA004', 'Paquette', 'Aaron', 4, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['GM048', 'Girard', 'Mohamed', 48, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['SE014', 'Simard', 'Ethan', 14, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['BE053', 'Boucher', 'Eden', 53, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['CT057', 'Caron', 'Tom', 57, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['BL008', 'Beaulieu', 'Léon', 8, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['CN067', 'Cloutier', 'Noé', 67, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['DT027', 'Dubé', 'Tiago', 27, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['PT083', 'Poirier', 'Théo', 83, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['FI066', 'Fournier', 'Isaac', 66, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['LM064', 'Lapointe', 'Marius', 64, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['LV098', 'Leclerc', 'Victor', 98, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['LA097', 'Lefebvre', 'Ayden', 97, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['PM019', 'Poulin', 'Martin', 19, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['TN094', 'Thibault', 'Naël', 94, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['SM026', 'St-Pierre', 'Mathis', 26, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['NA069', 'Nadeau', 'Axel', 69, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['MR047', 'Martin', 'Robin', 47, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['LT077', 'Landry', 'Timéo', 77, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['ME089', 'Martel', 'Enzo', 89, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['BM033', 'Bédard', 'Marceau', 33, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['GE054', 'Grenier', 'Eliott', 54, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['LN032', 'Lessard', 'Nino', 32, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['BV081', 'Bernier', 'Valentin', 81, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['RN094', 'Richard', 'Nolan', 94, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['MM079', 'Michaud', 'Malo', 79, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['HM041', 'Hébert', 'Milo', 41, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['DA080', 'Desjardins', 'Antoine', 80, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['CS094', 'Couture', 'Samuel', 94, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['TA093', 'Turcotte', 'Augustin', 93, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['LA044', 'Lachance', 'Amir', 44, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['PL034', 'Parent', 'Lyam', 34, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['BR063', 'Blais', 'Rayan', 63, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['GY068', 'Gosselin', 'Yanis', 68, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['SI024', 'Savard', 'Ibrahim', 24, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['PG042', 'Proulx', 'Gaspard', 42, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['BS084', 'Beaudoin', 'Sohan', 84, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['DC030', 'Demers', 'Clément', 30, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['PM033', 'Perreault', 'Mathéo', 33, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['BB085', 'Boudreau', 'Baptiste', 85, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['LS061', 'Lemieux', 'Simon', 61, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['CM040', 'Cyr', 'Maxence', 40, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['PI009', 'Perron', 'Imran', 9, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['DK089', 'Dufour', 'Kaïs', 89, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['DC002', 'Dion', 'Côme', 2, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['MS060', 'Mercier', 'Soan', 60, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['BE058', 'Bolduc', 'Evan', 58, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['BM007', 'Bérubé', 'Maxime', 7, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['BC054', 'Boisvert', 'Camille', 54, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['LA025', 'Langlois', 'Alexandre', 25, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['MO008', 'Ménard', 'Owen', 8, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['TI086', 'Therrien', 'Ismaël', 86, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['BL060', 'Bilodeau', 'Lenny', 60, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['PP094', 'Plante', 'Pablo', 94, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['BL072', 'Blanchette', 'Léandre', 72, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['DN065', 'Dubois', 'Naïm', 65, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['CI022', 'Champagne', 'Ilyan', 22, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['PT014', 'Paradis', 'Thomas', 14, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['FJ033', 'Fortier', 'Joseph', 33, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['AO055', 'Arsenault', 'Oscar', 55, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['DE029', 'Dupuis', 'Elio', 29, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['GM099', 'Gaudreault', 'Malone', 99, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['HN085', 'Hamel', 'Noa', 85, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['HD050', 'Houle', 'Diego', 50, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['VN022', 'Villeneuve', 'Noam', 22, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['RL075', 'Rousseau', 'Livio', 75, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['GC061', 'Gravel', 'Charlie', 61, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['TC027', 'Thériault', 'Charly', 27, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['LB084', 'Lemay', 'Basile', 84, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['RM065', 'Robert', 'Milan', 65, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2],
['AI008', 'Allard', 'Ilyes', 8, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['DA036', 'Deschênes', 'Ali', 36, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['GA035', 'Giroux', 'Anas', 35, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['GL017', 'Guay', 'Logan', 17, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['LM092', 'Leduc', 'Mathys', 92, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['BA055', 'Boivin', 'Alessio', 55, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['CW060', 'Charbonneau', 'William', 60, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['LT054', 'Lambert', 'Timothée', 54, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['RA028', 'Raymond', 'Auguste', 28, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['VA071', 'Vachon', 'Adem', 71, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['GA050', 'Gilbert', 'Ayoub', 50, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['AW059', 'Audet', 'Wassim', 59, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 1],
['JM076', 'Jean', 'Marin', 76, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 3],
['LY056', 'Larouche', 'Youssef', 56, '2099-01-01 07:00:00 ', '2099-01-01 07:00:00', 2]
])
            #print(to_go)
        """ plus simple de le faire via mariadb command line load infile"""
        self.create_connection()
        le_curseur = self.conn.cursor()
        print(type(le_curseur))
        string_insert = "insert into employe (num_emp, nom, prenom,anciennete,pref_creneau_deb,pref_creneau_fin,niveau) values (?,?,?,?,?,?,?)"
        try:
            for emp in ze_liste:
                print(emp)
                le_curseur.execute(string_insert, (emp[0],emp[1],emp[2],emp[3],emp[4],emp[5],emp[6]))
        except Exception as e:
            print(e)
        finally:
            self.conn.commit()
            self.conn.close()


if __name__ == '__main__':
    appli = trafic_mariadb();
