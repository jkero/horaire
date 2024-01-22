import datetime
import locale
import calendar
from tests_connection import ma_connect
import unittest
import tests_connection
from util_calcul_dates_semaines import MesSemaines

class test_affect_equipes(unittest.TestCase):
    dummy_dico_staff ={}
    la_conn = None
    an = 2024
    num_semaine = 6
    hpers = 0.0
    def test_1etablir_conn(self):
        self.la_conn = ma_connect()
        print("TEST ---- connection != None")
        self.assertNotEqual(self.la_conn.conn,None)
        #self.getLeads()

    def test_2getLeads(self):
        self.la_conn = ma_connect()
        jkcur = self.la_conn.conn.cursor()
        queryLeads = "select * from employe where anciennete > 55 and niveau >= 3 order by niveau desc"
        jkcur.execute(queryLeads)
        print("TEST ---- query niveau des employes != None")
        self.assertNotEqual(jkcur, None)
        # for emp in jkcur:
        #     print(" %s, %s, n = %d" % (emp[2],emp[3],emp[7]))

    def test_3get_hpers(self):
        an = self.an
        num_semaine = self.num_semaine
        self.la_conn = ma_connect()
        jkcur = self.la_conn.conn.cursor()
        queryHpers = "select prevision_pers_h from previsions_par_semaine where annee =  ? and num_semaine = ?"
        jkcur.execute(queryHpers,(an,num_semaine))
        print("TEST ---- querysemaine != None")
        self.assertNotEqual(jkcur, None)
        if jkcur is not None:
            h = jkcur.fetchone()
            self.hpers = h[0]

    def test_4ventile_hpers_v_modeles(self):
        """ pour un nombre d'heures prévues hprevues, pour chaque modele hmod disponible
            par ordre asc de hmod resource disponible,
                si hmod < hprevues(le modele prevoit ou non une config pour ce nombre)
                    passe au modele suivant
                sinon
                    utiliser le modele (le modele accomode la charge, ou plus).
        """
        an = self.an
        num_semaine = self.num_semaine
        self.la_conn = ma_connect()
        jkcur = self.la_conn.conn.cursor()
        query_mod_hres = sem_hpers = 0
        queryHpers = "select prevision_pers_h from previsions_par_semaine where annee =  ? and num_semaine = ? order by prevision_pers_h asc"
        jkcur.execute(queryHpers,(an,num_semaine))
        print("TEST ---- curseur != None (la charge de la semmaine)")
        self.assertNotEqual(jkcur, None)
        sem_hpers = jkcur.fetchone()[0]
        print( "hpers " + str(sem_hpers))
        queryModeles = "select id, nb_quarts, duree_quart, nb_equipes_par_quart, nb_employe_par_equipe, jours_trav_par_semaine, ((nb_quarts * duree_quart * nb_equipes_par_quart * nb_employe_par_equipe)) as hp from modele_affectations order by hp asc, nb_quarts asc, nb_equipes_par_quart asc"
        #la requête ordonne en préférant le nb heures , le nb de quarts et le nb equipes minimaux (si h est pareil), dans cet ordre.
        jkcur.execute(queryModeles)
        id_mod = 0
        for row in jkcur.fetchall():
            #print(row)
            h_quot = sem_hpers / row[5]# ça donne les heures quotidiennes et de là on dérive le modèle compatible via affectations eq et q par jour
            #print("la charge hebdo. de %d implique  %d heures par jour (%d) " % (sem_hpers, h_quot, row[5] ))
            #print(str(row))
            #print(" query modele %d >= hquot %d ?" % (row[6],h_quot))
            if row[6] >= h_quot : #le nb heures le plus rapproché dans le modele
                query_mod_hres = row[6]
                id_mod = row[0]
                print("\nTEST 1 ---- modele trouvé ! (%d, id %d) >= que charge travail (%d)" % (
                    query_mod_hres, id_mod, h_quot))
                break
            else:
                # print("pass")
                continue
        # le modele
                self.assertGreaterEqual(query_mod_hres,h_quot)

    def test_5liste_equipes(self):
        """
        Avec les param de modele trouvé plut tôt, on a le nb équipes et emp par equipes et nb de quarts.
        Donc, nb_eq * nb_quarts = nb_leads à affecter (liste equipes) (emp_reste = nb_emp_par_eq - 1);
        S'en suit l'affectation des equipes avec les niveaux autres que leads tq emp_reste < query.
        #soit une charge de 150 heures pour une semaine donnée
        # prédéfini: 5 jours semaine, même modele chaque jour (répétition equipe sauf non-dispo)
        #1- répartir cette charge sur une semaine (5 jours)
        #2- 150/5 = 30 h par jour
        #3- diviser 30 par h_par_quart (7.5) = 4 personnes
        #4- trouver le modele qui supporte la charge prévue (total des heures accomplissables en une semaine)

        """
        an = self.an
        num_semaine = self.num_semaine
        self.la_conn = ma_connect()
        jkcur = self.la_conn.conn.cursor()
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
                print("\nTEST 2 ---- modele trouvé ! (%d, id %d) >= que charge travail (%d)" % (
                    query_mod_hres, id_mod, h_quot))
                # rappel: id, nb_quarts, duree_quart, nb_equipes_par_quart, nb_employe_par_equipe, jours_trav_par_semaine
                nb_equipes_par_q = row[3]
                nb_quarts = row[1]
                nb_emplo_par_eq = row[4]
                print("----modele : nb_equipes_par_q %d, nb_quarts %d, nb_empl_eq %d " % ( row[3],row[1],row[4]))
                print(row)
                print("----modele")
                break
            else:
                # print("pass")
                continue
                #equipes --leads
        liste_leads = []
        jkcur = self.la_conn.conn.cursor()
        queryLeads = "select * from employe where anciennete > 55 and niveau >= 3 order by niveau desc, anciennete desc"
        # combien d'équipes par jour = nb_quarts * nb_eq_par_quart
        nb_leads = nb_quarts * nb_equipes_par_q
        print("nb équipes par jour = %d" % (nb_leads))
        jkcur.execute(queryLeads)
        # jkcur.fetchall(int(nb_leads))

        for row in jkcur.fetchmany(int(nb_leads)):
            print(row)
            list_e = list([row[1],row[2],row[3]])
            liste_leads.append(list_e)
            dict_equipes["Team " + row[2]] = list([list_e])
        print(" le dico ")
        print(dict_equipes)

        print("\nTEST 3 ---- nb leads = tot eq du modele ? (%d = %d)" % (len(liste_leads), nb_leads))
        self.assertEqual(len(liste_leads), nb_leads)
        #creer liste equipes

        liste_emp = []
        print("liste employes requis = %d" % (int(nb_leads) * int(nb_emplo_par_eq - 1)))
        # //todo l'algo écarte tous les autres leads des équipes (comme employe ordinaire), ajuster
        queryNoLeads = "select num_emp, nom, prenom from employe where anciennete <= 55 and niveau <= 2 order by niveau desc, anciennete desc"
        jkcur.execute(queryNoLeads)
        #premiere passe des no-leads: toute la liste des dispos

        les_emp = list(jkcur.fetchall())
        # on elimine les-non-dispos tout en renseignant la liste avec le nb (nb_emplo_par_eq - 1) requis

        queryNonDispo = "select num_emp, nom, prenom, creneaux from employe right join non_dispo on employe.id = non_dispo.emp_id order by creneaux"
        jkcur2 = self.la_conn.conn.cursor()
        jkcur2.execute(queryNonDispo)
        liste_non_dispos = jkcur2.fetchall()
        for nondispo in liste_non_dispos:
            la_semaine = MesSemaines().renseigne_jours_semaine()
            print(la_semaine[0][1])
            print("************** %s" % type(la_semaine[0][1]))
            deb, fin = nondispo[3].split('@')
            print("******** %s  %s" % (type(deb),type(deb)))
            for sem in la_semaine:# si le debut ou la fin entrent dans l'intervalle ... préciser algo pour heures
                if datetime.datetime.strptime(deb,'%Y-%m-%d %H:%M') >= datetime.datetime.strptime(sem[1],'%Y-%m-%d %H:%M'):
                    if datetime.datetime.strptime(fin,'%Y-%m-%d %H:%M') > datetime.datetime.strptime(sem[1],'%Y-%m-%d %H:%M') + datetime.timedelta(hours=23.99):
                        print("deb %s fin %s jour d %s jour f %s" % (str(deb), str(fin), str(sem[1]), str(datetime.datetime.strptime(sem[1],'%Y-%m-%d %H:%M') + datetime.timedelta(hours=23.99))) )
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
        les_emp = list(jkcur.fetchmany(int(nb_leads) * int(nb_emplo_par_eq - 1)))# ("-1")le lead est un memdre de l'équipe
        #            #print(row)
        while les_emp:#cet ordre répartit les forces (niveau et anc entre les equipes)
            for i in dict_equipes:
                dict_equipes[i].append(list(les_emp.pop()))

        for k in dict_equipes:
            print("\n************")
            for j in dict_equipes[k]:
                print(str(j))



