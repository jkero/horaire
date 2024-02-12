import mariadb

from matrice_temps.refonte_2024.dev.util_connection import MaConnect
from matrice_temps.refonte_2024.dev.util_calcul_dates_semaines import LaSemaine
class Modele:
    connection = MaConnect()
    prev_an = 0
    prev_num_sem = 0
    prev_heures_sem = 0
    nb_equipes_par_q  = 0
    nb_quarts = 0
    nb_emplo_par_eq = 0
    id_mod = 0
    duree_quart = 0
    nb_jours_sem = 0
    h_modele = 0
    excedent = 0

    @staticmethod
    def db_recup_modele(an, num):
        queryHpers = "select prevision_pers_h from previsions_par_semaine where annee =  ? and num_semaine = ? order by prevision_pers_h asc"
        jkcur = Modele.connection.conn.cursor()
        jkcur.execute(queryHpers, (an, num))
        Modele.prev_an = an
        Modele.prev_num_sem = num
        Modele.excedent = 0

        Modele.prev_heures_sem = jkcur.fetchone()[0]

        queryModeles = "select id, nb_quarts, duree_quart, nb_equipes_par_quart, nb_employe_par_equipe, jours_trav_par_semaine, (nb_quarts * duree_quart * nb_equipes_par_quart * nb_employe_par_equipe * jours_trav_par_semaine) as hp from modele_affectations order by hp asc, nb_quarts asc, nb_equipes_par_quart asc"

        try:
            jkcur.execute(queryModeles)
        except mariadb.Error as m:
            print(m)

        # # charge de la semaine / jours travaillés par semaine dans le modele
        id_modele = 0
        charge_prevue = Modele.prev_heures_sem
        if jkcur:
            for row in jkcur:
                heures_du_modele = row[6]
                Modele.nb_jours_sem = row[5]
    #            h_quot = Modele.prev_heures_sem / row[5]  # row[5] = jours travaillés dans la semaine
                if heures_du_modele < charge_prevue:  # le nb heures le plus rapproché dans le modele
                    # print("pass")
                    continue
                else:
                    query_mod_hres = row[6]  # row[6] = quarts * eq-par-quart * emp-par-eq * temps-hr-par quart
                    Modele.id_mod = row[0]
                    #       print("\nTEST 2 ---- modele trouvé ! (%d, id %d) >= que charge travail (%d)" % (
                    # query_mod_hres, id_mod, h_quot))
                    # rappel: id, nb_quarts, duree_quart, nb_equipes_par_quart, nb_employe_par_equipe, jours_trav_par_semaine
                    Modele.nb_equipes_par_q = row[3]
                    Modele.duree_quart = row[2]
                    Modele.nb_quarts = row[1]
                    Modele.nb_emplo_par_eq = row[4]
    #                print("  %d - %d" % (heures_du_modele, charge_prevue))
                    Modele.h_modele = row[6]
                    Modele.excedent = heures_du_modele - charge_prevue
    #                print("----modele : nb_equipes_par_q %d, nb_quarts %d, nb_empl_eq %d, excédent: %d " % (
    #                Modele.nb_equipes_par_q, Modele.nb_quarts, Modele.nb_emplo_par_eq, Modele.excedent))
                    # print(row)
                    # print("----modele")
                    break


if __name__ == '__main__':
#    print("a static method")
    Modele.db_recup_modele(2024, 6)
    # print(Modele.prev_an)
    # print(Modele.prev_num_sem)
    # print(Modele.prev_heures_sem)
