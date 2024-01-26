from util_connection import ma_connect
from util_calcul_dates_semaines import LaSemaine
class Modele:
    connection = ma_connect()
    prev_an = 0
    prev_num_sem = 0
    prev_heures_sem = 0
    nb_equipes_par_q  = 0
    nb_quarts = 0
    nb_emplo_par_eq = 0
    id_mod = 0
    duree_quart = 0
    @staticmethod
    def db_recup_modele(an, num):
        queryHpers = "select prevision_pers_h from previsions_par_semaine where annee =  ? and num_semaine = ? order by prevision_pers_h asc"
        jkcur = Modele.connection.conn.cursor()
        jkcur.execute(queryHpers, (an, num))
        Modele.prev_an = an
        Modele.prev_num_sem = num
        Modele.prev_heures_sem = jkcur.fetchone()[0]

        queryModeles = "select id, nb_quarts, duree_quart, nb_equipes_par_quart, nb_employe_par_equipe, jours_trav_par_semaine, ((nb_quarts * duree_quart * nb_equipes_par_quart * nb_employe_par_equipe)) as hp from modele_affectations order by hp asc, nb_quarts asc, nb_equipes_par_quart asc"
        jkcur.execute(queryModeles)
        # # charge de la semaine / jours travaillés par semaine dans le modele
        id_modele = 0
        for row in jkcur:
            h_quot = Modele.prev_heures_sem / row[5]  # row[5] = jours travaillés dans la semaine
            if row[6] >= h_quot:  # le nb heures le plus rapproché dans le modele
                query_mod_hres = row[6]  # row[6] = quarts * eq-par-quart * emp-par-eq * temps-hr-par quart
                Modele.id_mod = row[0]
                #       print("\nTEST 2 ---- modele trouvé ! (%d, id %d) >= que charge travail (%d)" % (
                # query_mod_hres, id_mod, h_quot))
                # rappel: id, nb_quarts, duree_quart, nb_equipes_par_quart, nb_employe_par_equipe, jours_trav_par_semaine
                Modele.nb_equipes_par_q = row[3]
                Modele.duree_quart = row[2]
                Modele.nb_quarts = row[1]
                Modele.nb_emplo_par_eq = row[4]
                print("----modele : nb_equipes_par_q %d, nb_quarts %d, nb_empl_eq %d " % (Modele.nb_equipes_par_q, Modele.nb_quarts, Modele.nb_emplo_par_eq))
                # print(row)
                # print("----modele")
                break
            else:
                # print("pass")
                continue
            #     # equipes --leads

if __name__ == '__main__':
    print("a static method")
    # Modele.db_recup_modele(2024, 6)
    # print(Modele.prev_an)
    # print(Modele.prev_num_sem)
    # print(Modele.prev_heures_sem)
