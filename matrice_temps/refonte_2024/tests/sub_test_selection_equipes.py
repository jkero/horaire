import datetime
import locale
import calendar
from tests_connection import ma_connect
import unittest
import tests_connection
from util_calcul_dates_semaines import MesSemaines
from util_calcule_non_dispo import Check_non_dispo as ndispo

class sub_test_equipes:
    @staticmethod
    def liste_equipes():
        an = 2024
        num_semaine = 6
        la_conn = ma_connect()
        jkcur = la_conn.conn.cursor()
        query_mod_hres = sem_hpers = 0
        nb_quarts = 0
        nb_emplo_par_eq = 0
        dict_equipes = {}
        queryHpers = "select prevision_pers_h from previsions_par_semaine where annee =  ? and num_semaine = ? order by prevision_pers_h asc"
        jkcur.execute(queryHpers,(an,num_semaine))
        sem_hpers = jkcur.fetchone()[0]
        queryModeles = "select id, nb_quarts, duree_quart, nb_equipes_par_quart, nb_employe_par_equipe, jours_trav_par_semaine, ((nb_quarts * duree_quart * nb_equipes_par_quart * nb_employe_par_equipe)) as hp from modele_affectations order by hp asc, nb_quarts asc, nb_equipes_par_quart asc"
        jkcur.execute(queryModeles)
        #charge de la semaine / jours travaillés par semaine dans le modele
        id_modele = 0
        for row in jkcur:
            h_quot = sem_hpers / row[5]# row[5] = jours travaillés dans la semaine
            if row[6] >= h_quot:  # le nb heures le plus rapproché dans le modele
                query_mod_hres = row[6]# row[6] = quarts * eq-par-quart * emp-par-eq * temps-hr-par quart
                id_mod = row[0]
         #       print("\nTEST 2 ---- modele trouvé ! (%d, id %d) >= que charge travail (%d)" % (
                #query_mod_hres, id_mod, h_quot))
                # rappel: id, nb_quarts, duree_quart, nb_equipes_par_quart, nb_employe_par_equipe, jours_trav_par_semaine
                nb_equipes_par_q = row[3]
                nb_quarts = row[1]
                nb_emplo_par_eq = row[4]
                #print("----modele : nb_equipes_par_q %d, nb_quarts %d, nb_empl_eq %d " % ( row[3],row[1],row[4]))
                #print(row)
                #print("----modele")
                break
            else:
                # print("pass")
                continue
                #equipes --leads
        liste_leads = []
        jkcur = la_conn.conn.cursor()
        queryLeads = "select * from employe where anciennete > 55 and niveau >= 3 order by niveau desc, anciennete desc"
        # combien d'équipes par jour = nb_quarts * nb_eq_par_quart
        nb_leads = nb_quarts * nb_equipes_par_q
        #print("nb équipes par jour = %d" % (nb_leads))
        jkcur.execute(queryLeads)
        # jkcur.fetchall(int(nb_leads))

        for row in jkcur.fetchmany(int(nb_leads)):
            #print(row)
            list_e = list([row[1],row[2],row[3]])
            liste_leads.append(list_e)
            dict_equipes["Team " + row[2]] = list([list_e])
        #print(" le dico ")
        #print(dict_equipes)

        #print("\nTEST 3 ---- nb leads = tot eq du modele ? (%d = %d)" % (len(liste_leads), nb_leads))

        #creer liste equipes

        liste_emp = []
        #print("liste employes requis = %d" % (int(nb_leads) * int(nb_emplo_par_eq - 1)))
        # //todo l'algo écarte tous les autres leads des équipes (comme employe ordinaire), ajuster
        queryNoLeads = "select num_emp, nom, prenom,id from employe where anciennete <= 55 and niveau <= 2 order by niveau desc, anciennete desc"
        jkcur.execute(queryNoLeads)
        #premiere passe des no-leads: toute la liste des dispos

        les_emp_orig = list(jkcur.fetchall())
        les_emp_to_pop = les_emp_orig
        # on elimine les-non-dispos tout en renseignant la liste avec le nb (nb_emplo_par_eq - 1) requis

        queryNonDispo = "select emp_id, nom, prenom, creneaux from employe right join non_dispo on employe.id = non_dispo.emp_id order by creneaux"
        jkcur2 = la_conn.conn.cursor()
        jkcur2.execute(queryNonDispo)
        liste_non_dispos = jkcur2.fetchall()

        for t_nondispo in liste_non_dispos:
            la_semaine = MesSemaines().renseigne_jours_semaine()
            #print(la_semaine[0][1])
            #print("************** %s" % type(la_semaine[0][1]))
            deb, fin = t_nondispo[3].split('@')
            #print("******** %s  %s" % (type(deb),type(deb)))
            for emp in les_emp_to_pop:
                #print(" --------%d------ %s --------%d------ %s-------------" % (emp[3],type(emp[3]),t_nondispo[0], type(t_nondispo[0])))
                if emp[3] == t_nondispo[0]:
                    #print(" -------------- %d -------------- %s-------------" % (emp[3],t_nondispo[0]) )
                    for sem in la_semaine:# si le debut ou la fin entrent dans l'intervalle ... préciser algo pour heures
                        #print("pour le jour %s " % str(sem[1]))
                        les_emp_to_pop = les_emp_orig
                        if  ndispo.is_not_dispo(deb, fin,sem[1]):
                            print("\n ******************************************")
                            print(str(t_nondispo[1]) + "  %s,  %s " % (str(t_nondispo[3]),str(sem[1])) )
                            print("\n *****************retire %s************************" % str(emp))
                            les_emp_to_pop.pop(les_emp_to_pop.index(emp))
                        print("les 10 employes dispos le %s sont:" % sem[1])
                        cpt = 0
                        for e in les_emp_to_pop:
                            if cpt < 10:
                                print(e)
                            else:
                                break
                         #remettre la liste des dispos à zero pour la prochaine journée
# quelque part ici je dois ajouter la fin de la journée traitée (+ 23h59) OK

# //todo inverser la logique et balayer la liste d'employes en même temps
        #pour chaq jour sem
            #copier liste orig empl
            #pour chq emp dans lis_copi
                #si emp_id est dans non-dispo
                    #pour chaque non-dispo de cet emp
                        #si deb >= jd et fin < jf
                          #lis_copi.pop(emp)
                          #break
                        #sinon continue

            #utiliser list_copi pour aaffecter ce jour
            # .....


        # for sem in la_semaine:
        #     for nondispo in liste_non_dispos:


        #2e passe
        # les_emp = list(jkcur.fetchmany(int(nb_leads) * int(nb_emplo_par_eq - 1)))# ("-1")le lead est un memdre de l'équipe
        # #            #print(row)
        # while les_emp:#cet ordre répartit les forces (niveau et anc entre les equipes)
        #     for i in dict_equipes:
        #         dict_equipes[i].append(list(les_emp.pop()))
        #
        # for k in dict_equipes:
        #     for j in dict_equipes[k]:
        #         print(str(j))

if __name__ == '__main__':
    sub_test_equipes.liste_equipes()



