import datetime
from datetime import datetime
from tests_connection import ma_connect
from matrice_temps.refonte_2024.dev.util_calcul_dates_semaines import MesSemaines
from matrice_temps.refonte_2024.dev.util_calcule_non_dispo import Check_non_dispo as ndispo

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
        dict_equipes = {} #un dictionnaire par jour k = nom lead
        dict_leads = {}
        dict_semaine = {} # un dictionnaire de dictionnaires k = jour semaine

        la_semaine = MesSemaines().renseigne_jours_semaine()
        print(la_semaine)

        # for j in range(len(liste_jours)):
        #     t = {}
        #     t[liste_jours[j]] = liste_equipes_par_jour
        #     liste_semaine.append(t)
        #print(liste_semaine)

        for jsem in range(len(la_semaine)):
            dict_equipes_par_jour = {}
            dict_equipes_par_jour[la_semaine[jsem]] = compose_equipes()
            #print("pop %d  orig %d" % (len(les_emp_to_pop),len(les_emp_orig)))
            les_emp_to_pop = list(les_emp_orig) #! copie par valeur

            for t_nondispo in liste_non_dispos:

                deb, fin = t_nondispo[3].split('@')
                jrsem = datetime.strptime(jsem[1], '%Y-%m-%d  %H:%M')
                jrdeb = datetime.strptime(deb, '%Y-%m-%d  %H:%M')
                jrfin = datetime.strptime(deb, '%Y-%m-%d  %H:%M')

                if ndispo.is_not_dispo(deb, fin, jsem[1]):
                    #print("heures non dispo jsem %s, deb %s, fin %s, empid %d" % (jrsem.date(),deb,fin, t_nondispo[0]))
                    for e in les_emp_to_pop:
                        if e[3] == t_nondispo[0]:
                            print("confirme %s" % e[3])
                            #print (les_emp_to_pop)
                            p = les_emp_to_pop.pop(les_emp_to_pop.index(e)) #retirer emp non dispo
                            print("retire %s" % str(p))
                            #print (les_emp_to_pop)

            #print("pour %s on a :" % jsem[1])
            # for i in les_emp_to_pop:
            #     print ("\t  %s" % str(i[1]))

                #2e passe
            #select_emp = list(jkcur2.fetchmany(int(nb_leads) * int(nb_emplo_par_eq - 1)))# ("-1")le lead est un memdre de l'équipe
            #            #print(row)
            select_emp = list(les_emp_to_pop)

            # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            # for s in select_emp:
            #     print(s)
            # print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            cpt = int(nb_leads) * int(nb_emplo_par_eq - 1)
            dict_equipes = {}
            for key in dict_leads:
                 dict_equipes[key]= dict_leads[key]
            #print("@@@@@@@@@@@@@@@@@@@@@@@@@ %s" % dict_equipes)
            #print("cpt %d" % cpt)
            while cpt > 0:#cet ordre répartit les forces (niveau et anc entre les equipes) #recuperer les leads
                for i in dict_equipes:
                    w = list(select_emp.pop(0))
                    dict_equipes[i].append(w)

                cpt = cpt - 2
            print("$$$$ %s" % dict_equipes[i])
            dict_equipes = {}

                #print(dict_leads)
            #print("k de dic sem = %s" % str(jsem[1][:10]))
            #dict_semaine[str(jsem[1][:10])] = dict_equipes
            #print(dict_equipes)



                #print(len(sem))


        # print("################################# %s" % jsem[1])
        # for jr in dict_semaine:
        #     print(jr)
        #     print(dict_semaine[jr])


                # les_emp_to_pop = les_emp_orig
                # if ndispo.is_not_dispo(deb, fin, jsem[1]):
                #     print("\n ******************************************")
                #     print(str(t_nondispo[1]) + "  %s,  %s " % (str(t_nondispo[3]), str(jsem[1])))
                #     print("\n *****************retire %s************************" % str(emp))
                #     les_emp_to_pop.pop(les_emp_to_pop.index(emp))
                # print("les 10 employes dispos le %s sont:" % jsem[1])
                # cpt = 0
                # for e in les_emp_to_pop:
                #     if cpt < 10:
                #         print(e)
                #     else:
                #         break



            # #print(la_semaine[0][1])
            # #print("************** %s" % type(la_semaine[0][1]))
            # deb, fin = t_nondispo[3].split('@')
            # #print("******** %s  %s" % (type(deb),type(deb)))
            # for emp in les_emp_to_pop:
            #     #print(" --------%d------ %s --------%d------ %s-------------" % (emp[3],type(emp[3]),t_nondispo[0], type(t_nondispo[0])))
            #     if emp[3] == t_nondispo[0]:
            #         #print(" -------------- %d -------------- %s-------------" % (emp[3],t_nondispo[0]) )

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



