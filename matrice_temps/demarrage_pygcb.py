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
    nb_quarts_par_jour = 3
 # la logique equipes + hpers + quarts est en partie ici.

# 50 heures personnes signifie qu'un travail a besoin de 50 heures * 1 personne
# si on a 5 personnes ça fait 5 personnes * 10 heures. ici 10 heures serait la durée d'un quart typique -- à définir dans une constante (K1)

# Définition
# Unité de mesure correspondant au travail qui peut être accompli par une personne pendant une heure,
# par deux personnes pendant une demi-heure et ainsi de suite, et qui sert, dans le budget, à répartir
# les crédits affectés à la main-d'œuvre.

# il faut déterminer le nb max d'employés dans un équipe -- une autre constante (K2).

# Pour cette semaine on a besoin de (total_hpers/temps_quart) 50/7.5 = 6.6 personnes de quart (de 7.5 heures).

# Exemple plus nombreux avec 1000 hpers. On a 1000/7.5 = 133 quarts pour la semaine; on peut diviser par 5 jours = 26.6 personnes par jour.

# Prenons 27 pour arrondir et on divise par le nb_max par equipe : on a alors 27/4 = 7 equipes de 4 par jour pendant 5 jours.

# donc 7 * 4 * 5 * 7.5   = les ~1000 heures/pers requises.

#il faut déterminer le nb de quarts, s'il y a lieu, une autre constante (K3)

# si on a 3 quarts ça fait 2 quarts de 2 et un quart de 3 équipes, on peut les remplir  jour -> matin -> soir ??

# Réalité : ça prendrait 27 personnes ([1000/7.5h] sans backup) sur le payroll pendant cette période.

# il faut assigner les employés aux équipes selon les règles de gestion des non_dispo.

# types de non dispo: 1 = quart pour non-dispo (selon la struc de cette table : le quart par défaut)
#                     2  = vacances
#                     3  = autres cas de non-dispo

# Pour le moment ce sont des créneaux à interpréter selon le type de dispo.


#  -- a) choisir les employés soit dans l'ordre d'ancienneté ou alors au hasard ?? (les plus anciens sur les equipes de jour, par exemple)
#  -- b) pour chaque équipe et cpt < nb_emplo requis,
#         cpt_eq = 0
#         si cpt_eq < max
#           si liste(emp.non_dispo) <> date pour cette affectation (#semaine = dates à comparer pour les 3 types de non-dispo).
#                ajouter cet employé dans equipe.
#                 cpt++
#                 cpt_eq++
# la rotation des équipes est prédéterminée entre chaque semaine (ou non, c'est fixe, car c'est au moment des validations des non-dispos que la justice s'applique). Selon le nb, il faut permuter logiquement à travers les quarts.
# ça pourrait être une sequence générée. Logique à étudier: comment permuter si les valeurs changent ? Concept de
# quart prioritaire (y ajouter des equipes, etc.)

#           s           d           l           m           m           j           v
#q   matin/jour/soir
#eq      y/w,x/z      y/w,x/z     c/ab/d     c/ab/d     c/ab/d       c/ab/d      y/w,x/z

# bref, quand un employe est intégré, il faut lui appliquer une grille de non dispos et de quarts, selon la période (on lui assigne un quart + les vacances + les autres non-dispos.).

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