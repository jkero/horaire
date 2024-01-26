from util_connection import ma_connect
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
        queryLeads = "select id, num_emp, nom, prenom from employe where anciennete > 55 and niveau >= 3 order by niveau desc, anciennete desc"
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
        queryUnderLeads = "select id, num_emp, nom, prenom from employe where  niveau < 3 order by anciennete desc, niveau desc"
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

        return list(liste_non_dispos)

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

        dict_equipes_semaine = {}

        for jour in liste_jours_semaine:
            dict__jour = {}# une version par jour (contient les dicos equipes)

            # // ici je réinitialise les listes des employés diponibles (vérif par jour)
            liste_all_lead_pop = liste_all_leads.copy()
            liste_all_under_leads_pop = liste_all_under_leads.copy()

            # // ici: 2 boucles pour vérifier les non_dispos et valider les listes
            for pot_lead in liste_all_lead_pop:
                for non_dispo in liste_all_non_dispos:
                    if Check_non_dispo.is_not_dispo(non_dispo[3],jour[1]):
                        if(pot_lead[0] == non_dispo[0]):
                            liste_all_lead_pop.pop(liste_all_lead_pop.index(pot_lead))

            for pot_under_lead in liste_all_under_leads_pop:
                for non_dispo in liste_all_non_dispos:
                    if Check_non_dispo.is_not_dispo(non_dispo[3], jour[1]):
                        if (pot_under_lead[0] == non_dispo[0]):
                            liste_all_under_leads_pop.pop(liste_all_under_leads_pop.index(pot_under_lead))

            dict_equipe = {} # une version par jour

            # // ici je renseigne le dico equipe (chaque équipe) avec les leaders disponibles
            for i in range(modele_previsions.nb_quarts * modele_previsions.nb_equipes_par_q):# = le nb equipes total
                dict_equipe[liste_all_lead_pop[i][2]] = list(liste_all_lead_pop[i])


            # // ici je récupère ce qu'il faut d'employés disponibles (triés par ancienneté, niveau) et les ajoute aux dicos equipes
            for i in range(((modele_previsions.nb_emplo_par_eq - 1))):
                #print(i)
                for j in dict_equipe:
                    dict_equipe[j].append(list(liste_all_under_leads_pop.pop(0)))


            # // finalement la semaine est structurée dans un dictionnaire de jours et d'équipes
            dict_equipes_semaine[jour[1][:10]] = dict_equipe

        #vérif la semaine
        for j in dict_equipes_semaine:
            print(j)
            for v in dict_equipes_semaine[j].values():
                print(v)
            # for e in j:
            #     print("\n\t %s" % str(e))
        #ltot = liste_all_lead_pop

if __name__ == '__main__':
    CompositionEquipes.get_emp_dispo(0,2024,6)