from tests_connection import ma_connect
from util_recup_modele import Modele
from util_calcule_non_dispo import Check_non_dispo
from util_calcul_dates_semaines import LaSemaine
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
        nb_quarts = m.nb_quarts
        nb_leads = nb_quarts * nb_equipes_par_q
        queryLeads = "select * from employe where anciennete > 55 and niveau >= 3 order by niveau desc, anciennete desc"
        # # combien d'équipes par jour = nb_quarts * nb_eq_par_quart
        jkcur.execute(queryLeads)
        l_all_leads = jkcur.fetchall()
        #
        return list(l_all_leads)
    @staticmethod
    def getUnderLeads():
        m = CompositionEquipes.modele
        jkcur = CompositionEquipes.connection.conn.cursor()
        nb_equipes_par_q = m.nb_equipes_par_q
        nb_quarts = m.nb_quarts
        nb_under_leads = (nb_quarts * nb_equipes_par_q) - 1
        queryUnderLeads = "select * from employe where anciennete <= 55 and niveau < 3 order by niveau desc, anciennete desc"
        # # combien d'équipes par jour = nb_quarts * nb_eq_par_quart
        jkcur.execute(queryUnderLeads)
        l_all_under_leads = jkcur.fetchall()
        #
        return list(l_all_under_leads)

    @staticmethod



    def get_all_non_dispos():
        jkcur = CompositionEquipes.connection.conn.cursor()
        queryNonDispo = "select emp_id, nom, prenom, creneaux from employe right join non_dispo on employe.id = non_dispo.emp_id order by creneaux"
        jkcur.execute(queryNonDispo)
        liste_non_dispos = list(jkcur.fetchall())

        return liste_non_dispos

    @staticmethod
    def get_emp_dispo(premier_jour_sem, an, semaine):
        liste_all_leads = CompositionEquipes.getLeads()
        liste_all_under_leads = CompositionEquipes.getUnderLeads()
        liste_all_non_dispos = CompositionEquipes.get_all_non_dispos()
        modele_previsions = CompositionEquipes.modele
        modele_previsions.db_recup_modele(an, semaine)
        #print(modele_previsions.prev_an)
        # +----------+--------------------
        # | id_dispo | creneaux | emp_id |
        # +----------+--------------------
        liste_all_lead_pop = liste_all_leads.copy()
        liste_all_under_leads_pop = liste_all_under_leads.copy()
        # +----+---------+-----------+--------+------------+---------------------+---------------------+
        # | id | num_emp | nom | prenom | anciennete | pref_creneau_deb | pref_creneau_fin | niveau |
        # +----+---------+-----------+--------+------------+---------------------+---------------------+
        liste_jours_semaine = LaSemaine.renseigne_jours_semaine(premier_jour_sem,an,semaine)# \\todo hard code here for tests ;1st day must be 0 (Monday) to 6 (Sunday)
        print (liste_jours_semaine)

        for jour in liste_jours_semaine:
            liste_all_lead_pop = liste_all_leads.copy()
            liste_all_under_leads_pop = liste_all_under_leads.copy()
            for pot_lead in liste_all_lead_pop:
                #print(pot_lead[0])
                for non_dispo in liste_all_non_dispos:
#                    print(non_dispo[0])
                    if Check_non_dispo.is_not_dispo(non_dispo[3],jour[1]):
                        if(pot_lead[0] == non_dispo[0]):
                            print (" %s  %s" % (str(jour[1]),str(pot_lead[2])))
                            liste_all_lead_pop.pop(liste_all_lead_pop.index(pot_lead))

            for pot_under_lead in liste_all_under_leads_pop:
                # print(pot_lead[0])
                for non_dispo in liste_all_non_dispos:
                    #                    print(non_dispo[0])
                    if Check_non_dispo.is_not_dispo(non_dispo[3], jour[1]):
                        if (pot_under_lead[0] == non_dispo[0]):
                            print(" %s  %s" % (str(jour[1]), str(pot_under_lead[2])))
                            liste_all_under_leads_pop.pop(liste_all_under_leads_pop.index(pot_under_lead))


        #ltot = liste_all_lead_pop


        jkcur = CompositionEquipes.connection.conn.cursor()
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
    CompositionEquipes.get_emp_dispo(0,2024,6)