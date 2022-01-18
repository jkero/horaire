import sqlite3
import traceback,sys, math

from sqlite3 import Error

from datetime import date, datetime, timedelta

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
    temps_quart = 7.5
    max_emp_par_equipe = 4
    nb_quarts_par_jour = 3
    equipes = {}
    equipes_maximales = {'A': [['8-16'],[]],'B': [['8-16'],[]],'C': [['8-16'],[]], \
                         'D': [['5-13'],[]],'E': [['5-13'],[]],'F': [['5-13'],[]], \
                         'G': [['12-20'],[]],'H': [['12-20'],[]],'I': [['12-20'],[]]}
    try:
        conn = sqlite3.connect(db_file)
        if conn is not None:
            auj = datetime.fromisoformat("2022-04-01 12:12")
            week = str((auj).isocalendar()[1])
            hpers_req = select_hpers(conn,week)
            employes_dispos = select_count_emp_dispo(conn, week)
            calcul_equipes(select_hpers(conn,week))
            employes_requis = hpers_req/temps_quart
            print("auj :" + str(auj))
            print("sem : " + str(week))
            print("employes requis ("+ str(hpers_req) + "/" + str(temps_quart) + ") =  " + str(hpers_req/temps_quart))
            print("nb. equipes = emp_requis/max_par_eqp = " + str(employes_requis) + "/" + str(max_emp_par_equipe) + " = " + str("%2.2f") % (employes_requis/max_emp_par_equipe))
#   //TODO autre detail: equipes ont un quart determiné et il faudra tenter de verifier quarts par defaut des employes en les placant dans les equipes
#   //TODO le nb d'equipes et le dictionnaire doivent être automatiques
            count = 0
            for key in equipes_maximales:
                if count < round(employes_requis/max_emp_par_equipe):
                    equipes[key] = equipes_maximales[key]
                    count  = count + 1

            print (str(equipes))

            attribution_equipe(conn, equipes, auj)
# la composition des equipes doit se faire par jour, à cause des non-dispos qui peuvent être une seule journée. //TODO attribution selon boucle par jour pour semaine en cours
        else:
            print("Error! cannot create the database connection.")

    except Error as e:
            print(e)

    finally:
        if conn:
            conn.close()

def calcul_equipes(hpers):
    print("---------")


def select_hpers(conn, sem):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    res = cur.execute("SELECT hpers FROM previsions_hpers where semaine = " + sem).fetchone()
    return res[0]

def select_count_emp_dispo(conn, sem):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    res = cur.execute("select distinct count(id) from employes order by rang").fetchone()
    return res[0]

def check_inclusion(ref, res_non_dispo, conn):
#    print("res non dispo deb = " + str(res_non_dispo[0]) + "res non dispo fin = " + str(res_non_dispo[1]))
    req_non_dispo_employe = "select t_exact_debut, t_exact_fin, type_non_dispo from emp_non_dispo where id_empl_fk = ?"
    deb = res_non_dispo[0]
    fin = res_non_dispo[1]

#    print(str(type(ref)) + str(ref))
#    print(str(type(deb) )+ str(deb))
#    print(str(type(fin)) + str(fin))
    le_deb = datetime.fromisoformat(deb)
    la_fin = datetime.fromisoformat(fin)
    # for n in range(int((la_fin - le_deb).days) + 1):
    #     print(le_deb + timedelta(n))
    #
    print(str((ref <= la_fin) & (ref >= le_deb)))
    return (str((ref <= la_fin) & (ref >= le_deb)))


def attribution_equipe(conn, les_equipes, date):
    all_full_dispos = "SELECT distinct nom, prenom, debut, fin, id from employes order by rang"

    find_dispo_dates_and_type = "select emp_non_dispo.t_exact_debut,emp_non_dispo.t_exact_fin, emp_non_dispo.type_non_dispo, id_empl_fk from emp_non_dispo where id_empl_fk = '%s' order by id_empl_fk"

    # Attention ici la fk sur dispo ne parche pas. ça prend plutot un fk de l'id emplo dasn la tables des non_dispos, car un emplo peut avoir plusieurs non_dispos.
    #  De plus quand on valide la dispo, il faut corriger car la req retourne n non-dispos, on fait pas ça ici, TODO revoir tables

    curseur = conn.cursor()
    curseur2 = conn.cursor()
    curseur.execute(all_full_dispos)

    rows = curseur.fetchall()
#    print(type(rows))
#    print(len(rows))
    #conn.set_trace_callback(print)

    try:
        for emp in rows:
 #           print(str(emp[4]))
 #           print(type(emp[4]))
            curseur2.execute(find_dispo_dates_and_type % str(emp[4]))
            res = curseur2.fetchall()
            marqueur_non_dispo = 0
 #           print("resu pour employe " + str(emp[4])  + " " + str(len(res)))
            if len(res) > 0:
                print(str(res))
                for enr_dispo in res:
                    invalide = check_inclusion(date, enr_dispo, conn)
                    if invalide == 'True':
                         print('************** ' + str(emp[1]).upper() + " " + str(emp[0]).upper() + " exclu " + invalide)
                         marqueur_non_dispo = 1
                         break
                    else:
                          affecte_equipes(les_equipes, emp)

            else:
                affecte_equipes(les_equipes, emp)



    except Exception:
        traceback.print_exc(file=sys.stdout)


    print(les_equipes.items())


def affecte_equipes(les_equipes, emp):
    for nom_eq in les_equipes:
#        print(str(nom_eq))
        if len(les_equipes[nom_eq][1]) < 4:
            les_equipes[nom_eq][1].append(emp[1][0] + ". " + emp[0])
            break
        else:
            continue


if __name__ == '__main__':
    create_connection(r"C:\Users\j\Documents\pythonProject\matrice_temps\letemps.db")

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

# types de non dispo: 1 = quart pour non-dispo (temps/date précis où il y a non-dispo)
#                     2  = vacances (temps/date précis où il y a non-dispo)
#                     3  = autres cas de non-dispo (temps/date précis où il y a non-dispo)
#                     4  = quart assigné (seules les heures sont importantes)

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

#print(datetime.fromisoformat(auj2).isocalendar()[1])
# trouver le dimanche de la semaine sqlite SELECT date('2022-01-22','-6 day', 'weekday 0'); // 2022-01-16
# la semaine de ce dimanche SELECT strftime('%W',date('2022-01-16','-6 day', 'weekday 0')); // 02
# auj = datetime.today()
# auj.strftime('%Y-%m-%d')
# '2022-01-16' --> avoir la date seulement

# si un jour des non_dispos de l'emp == journée de constitution de l'équipe, alors rejeter l'emp.

# logique constituer les equipes
#
#creer equipe_courante(index)
#
# shuffle employés? Liste par rang ancienneté?
#
# pour chaque employé disponible ET non-assigné (R.16.) #employé est dispo (fk_dispo = null ou alors scan(date non_dispo) != ce jour-ci)
#       si eq.courante.nb_equipiers < max_par_equipe
#           inserer_employe
#       sinon
#           creer equipe_courante(index+1)
#           inserer_employe

#import datetime
#
# #def weeknum_to_dates(weeknum): mmouais
#
# #    return [datetime.strptime("2022-W"+ str(weeknum) + str(x), "%Y-W%W-%w").strftime('%d.%m.%Y') for x in range(-6,0)]
#
# #weeknum_to_dates(37)
#
# def verifier_dispo_employe(conn, date):
# # premier type: non_dispo_fk is null   //CORRIGE CETTE CLE EST ENLEVEE
#     cur = conn.cursor()
#     res = cur.execute("SELECT count('nom') from employes where non_dispo_fk is NULL order by rang").fetchone()
#     print("dispos type 4 verifiées pour " + str(res[0]))
#     res2 = conn.cursor()
#     res2 = cur.execute("SELECT count('nom') from employes where non_dispo_fk NOT NULL order by rang").fetchone()
#     print("dispos type 1-3 a valider  pour " + str(res2[0]))
#
#     all_full_dispos = "SELECT dictinct * from employes where non_dispo_fk is NULL order by rang"
#     all_cond_dispos = "SELECT distinct * from employes where non_dispo_fk not NULL order by rang"
#
#     res_les_non_disp = cur.execute(all_cond_dispos).fetchall()
#     for enr in res_les_non_disp:
#         print(enr[5])
#         cur2 = conn.cursor()
#         the_q = "select distinct * from emp_non_dispo where id = " + str(enr[5]) # TODO il faut débrouiller les comparaisons de dates
#         print("la query : " + the_q)
#         res3 = cur2.execute(the_q).fetchall()
#         check_inclusion(date, res3[0][2],res3[0][3])
#  #       print(res3[2] + " - " + res3[3])
# #        resdispo = cur.execute("select '" + date + "' between date('') from emp_non_dispo where non_dispo_fk is NULL").fetchone()
#
#     res = cur.execute("SELECT distinct count('nom') from employes where non_dispo_fk is NULL").fetchone()
#     print("dispos type 4 verifiées pour " + str(res[0]))