import sqlite3

from sqlite3 import Error

from datetime import date, datetime

# pour demarrer la generation de l'horaire pour une période donnée, ça prend la saisie de valeurs de base.
# nb employes
# nb equipes
# prévisions heures/personnes pour la période v. table previsions_hpers

# auj= datetime.today()
# auj2 = "2022-01-03 01:00"
# dt_string = auj.strftime("%Y-%m-%d %H:%M")
# print("date = " + dt_string)
# print("semaine " + str((auj).isocalendar()[1]))

import sqlite3

from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        if conn is not None:
            auj = datetime.today()
            week = str((auj).isocalendar()[1])
            calcul_equipes(select_hpers(conn,week))
        else:
            print("Error! cannot create the database connection.")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def calcul_equipes(hpers):
    temps_quart = 7.5
    max_emp_par_equipe = 4
 # la logique equipes + hpers + quarts est en partie ici.

# 50 heures personnes signifie qu'un travail a besoin de 50 heures * 1 personne
# si on a 5 personnes ça fait 5 personnes * 10 heures. ici 10 heures serait la durée d'un quart typique -- à définir dans une constante (K1)

# Définition
# Unité de mesure correspondant au travail qui peut être accompli par une personne pendant une heure,
# par deux personnes pendant une demi-heure et ainsi de suite, et qui sert, dans le budget, à répartir
# les crédits affectés à la main-d'œuvre.

# il faut déterminer le nb max d'employés dans un équipe -- une autre constante (K2).

# pour cette semaine on a besoin de (total_hpers/nb_empl_dispo) equipes




def select_hpers(conn, sem):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    res = cur.execute("SELECT hpers FROM previsions_hpers where semaine = " + sem).fetchone()
    print(res[0])
    return res[0]

if __name__ == '__main__':
    create_connection(r"C:\Users\j\Documents\pythonProject\matrice_temps\letemps.db")


#print(datetime.fromisoformat(auj2).isocalendar()[1])