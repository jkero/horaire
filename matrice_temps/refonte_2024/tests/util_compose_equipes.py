from tests_connection import ma_connect
from util_recup_modele import Modele
class CompositionEquipes:
    connection = ma_connect()
    modele = Modele
    # def __init__(self, an, num):
    #     self.prev_annee = an
    #     self.prev_num_semaine = num
    @staticmethod
    def getLeads():
        m = CompositionEquipes.modele
        jkcur = CompositionEquipes.connection.conn.cursor()
        nb_equipes_par_q = m.nb_equipes_par_q
        nb_quarts = m.nb_q
        nb_leads = nb_quarts * nb_equipes_par_q
        queryLeads = "select * from employe where anciennete > 55 and niveau >= 3 order by niveau desc, anciennete desc"
        # # combien d'équipes par jour = nb_quarts * nb_eq_par_quart
        jkcur.execute(queryLeads)
        l_all_leads = jkcur.fetchall(int(nb_leads))
        #
        # for row in jkcur.fetchmany(int(nb_leads)):
        # # print(row)
    @staticmethod
    def getModele(an, num):
        CompositionEquipes.modele.db_recup_modele(an,num)

        liste_leads = CompositionEquipes.getLeads()


        jkcur = la_conn.conn.cursor()
        # queryLeads = "select * from employe where anciennete > 55 and niveau >= 3 order by niveau desc, anciennete desc"
        # # combien d'équipes par jour = nb_quarts * nb_eq_par_quart
        # nb_leads = nb_quarts * nb_equipes_par_q
        # # print("nb équipes par jour = %d" % (nb_leads))
        # jkcur.execute(queryLeads)
        # # jkcur.fetchall(int(nb_leads))
        #
        # for row in jkcur.fetchmany(int(nb_leads)):
        # # print(row)
        # list_e = list([row[1], row[2], row[3]])
        # liste_leads.append(list_e)
        # # dict_leads["Team " + row[2]] = list([list_e])
        #
        # # print("\nTEST 3 ---- nb leads = tot eq du modele ? (%d = %d)" % (len(liste_leads), nb_leads))
        #
        # # creer liste equipes
        #
        # liste_emp = []
        # # print("liste employes requis = %d" % (int(nb_leads) * int(nb_emplo_par_eq - 1)))
        # # //todo l'algo écarte tous les autres leads des équipes (comme employe ordinaire), ajuster
        # queryNoLeads = "select num_emp, nom, prenom,id from employe where anciennete <= 55 and niveau < 3 order by niveau desc, anciennete desc"
        # jkcur.execute(queryNoLeads)
        # # premiere passe des no-leads: toute la liste des dispos
        #
        # les_emp_orig = list(jkcur.fetchall())
        # les_emp_to_pop = les_emp_orig
        # # on elimine les-non-dispos tout en renseignant la liste avec le nb (nb_emplo_par_eq - 1) requis
        #
        # queryNonDispo = "select emp_id, nom, prenom, creneaux from employe right join non_dispo on employe.id = non_dispo.emp_id order by creneaux"
        # jkcur2 = la_conn.conn.cursor()
        # jkcur2.execute(queryNonDispo)
        # liste_non_dispos = jkcur2.fetchall()


if __name__ == '__main__':
    CompositionEquipes.getModele(2024,6)
    #print(CompositionEquipes.modele.prev_an)
    print(CompositionEquipes.modele.prev_heures_sem)
    # print(CompositionEquipes.modele.nb_equipes_par_q)