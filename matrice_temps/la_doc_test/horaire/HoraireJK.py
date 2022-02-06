import calendar
import locale
import sqlite3
import sys
import traceback
from datetime import datetime, timedelta
from sqlite3 import Error

import xlsxwriter

class horaire:
    '''
    C'est une application qui veut aider à la décision pour composer des équipes et des quarts

    '''
    auj = ''
    week= ''
    les_jours = []
    """Utile pour les initialisations futures et le fichier excel."""
    conn = None
    hpers_req = 0
    employes_requis = 0
    employes_tot = 0
    duree_quart  = 0
    max_emp_par_equipe = 4
    nb_quarts_indivi = 3
    nb_quart_en_eq = 0
    equipes = dict()
    equipes_maximales = {'A': [['8-16'], []], 'B': [['8-16'], []], 'C': [['8-16'], []], \
                         'D': [['5-13'], []], 'E': [['5-13'], []], 'F': [['5-13'], []], \
                         'G': [['12-20'], []], 'H': [['12-20'], []], 'I': [['12-20'], []]}
    """Besoin de ce dirctionnaire codé en dur pour les initialisations futures"""
    calendrier_equipes = dict() #pour inscrire toutes les equipes par dates
    #                              = par exemple {
    #le_dico = {
    #    'A': [['2022-04-01', ['momo', 'famo', 'Bozo']], ['2022-04-02', ['momo', 'flamo', 'Bozo']]],
    #    'B': [['2022-04-01', ['koko', 'klamo', 'kozo']], ['2022-04-02', ['koko', 'klamo', 'lozo']]]
    #}
    #ETC.                               aussi if le_dico['A'][0][1] == le_dico['A'][1][1], etc
    les_cles = list()
    liste_emp_a_assigner = list()
    """Cette liste est utile pour 'popper' les employés assignés et continuer à utiliser la même liste"""
    liste_emp_assignes = list()
    cpt_heures = 0
    valeur_repartition = 0
    nom_modele = ''
    config_modele = None

    def __init__(self, la_journee):
        """Créer la connection sur la BD et lancer les initialisations"""
        self.auj = datetime.fromisoformat(la_journee)        
        self.week = str(self.auj.isocalendar()[1])
        try:
            self.create_connection(r".\letemps.db")
            self.post_init()
        except Exception as e:
            print(e)
            traceback.print_exc(file=sys.stdout)


    def post_init(self):
        '''
        Initialiser les données stockées dans sqlite
        '''

        try:
            if self.conn is not None:
                string_previsions_config = "select previsions_hpers.hpers, previsions_hpers.heures_par_jour, \
                    previsions_hpers.nb_max_par_eq, round(previsions_hpers.hpers / previsions_hpers.heures_par_jour,1) as nb_quart_eq," \
                                           " round(round(previsions_hpers.hpers / previsions_hpers.heures_par_jour,1)/" \
                                           "previsions_hpers.nb_max_par_eq,1) as nb_quarts from previsions_hpers  where annee = ? and semaine = ?"
                cur_previsions = self.conn.cursor()

                self.les_dates_de_la_semaine = self.semaine()

                self.init_valeurs_modele()

                nb_eq = self.config_modele[0][4]

                self.initialise_calendrier_equipes(nb_eq)

                self.liste_emp_a_assigner = self.get_employes()

                self.liste_emp_assignes

                self.ajout_valide_dans_eq()

                self.ecriture_excel2()

        except Exception as e:
            print(e)
            traceback.print_exc(file=sys.stdout)

    def init_valeurs_modele(self):
        """Au lieu de renseigner manuellement les paramètres de l'application, offrir des modèles pré-configurés. Il y en a quelques uns dans la BD et ils sont associés à des semaines de travail. Un gestionnaire pourrait regarder les heures-personnes prévues pour une semaine donnée et décider du modèle ou même ajouter un modèle à la DB et l'associer à une semaine en particulier."""
        sql_modele_affect = "select p.semaine, p.hpers, p.heures_par_jour, round(p.hpers / p.heures_par_jour,1) as presences, m.nb_eq, m.nb_emp_par_eq as nb_par_eq, \
                                        round(round(p.hpers *1.0 / p.heures_par_jour,1)/m.nb_emp_par_eq,1) as nb_quarts_eq,\
                                         m.nb_eq_par_creneau, m.nb_creneau_disp , \
                                         round(round(cast(p.hpers as float) / p.heures_par_jour,2) / \
                                        (m.nb_emp_par_eq * m.nb_eq_par_creneau * m.nb_creneau_disp),2) as jours, m.nom \
                                        from previsions_hpers as p \
                                        inner join modele_assignation_hebdo as m \
                                        on p.modele = m.id \
                                        where p.semaine = " + str(self.week)

        cur_modele = self.conn.cursor()
        self.config_modele = cur_modele.execute(sql_modele_affect).fetchall()

    def semaine(self):
        """Créer une liste de jours et de dates pour la semaine à générer, selon la date fournier à l'app."""
        calendar.setfirstweekday(6)
        locale.setlocale(locale.LC_ALL, 'FR_ca')
        self.les_jours = [['Lundi', ''], ['Mardi', ''], ['Mercredi', ''], ['Jeudi', ''], ['Vendredi', ''], ['Samedi', ''],['dimanche', '']]
        lundi = self.auj + timedelta(days=-self.auj.weekday())
        incr = self.auj.weekday()
        for jours in self.les_jours:
            jours[1] = (self.auj + timedelta(days=-incr)).strftime('%Y-%m-%d')
            incr = incr - 1
        print("\n" + str(self.les_jours))
    
    def create_connection(self, db_file): #//TODO reorganiser le code sasn rapport avec la connection (sortir de cette methode)
        """Connecter avec DB sqlite (7 tables)."""
        try:
            self.conn = sqlite3.connect(db_file)
            if self.conn is not None:
                count = 0
            else:
               print("Error! cannot create the database connection.")
    
        except Error as e:
                print(e)


    def check_conflit(self, ref, les_non_dispo):
        """Vérifie les conflits de dates dans la table des non-dispo et journée courante."""
        retourne = bool()
        for enr in les_non_dispo:
            deb = enr[0]
            fin = enr[1]
            le_deb = datetime.fromisoformat(deb)
            la_fin = datetime.fromisoformat(fin)
            boule = (le_deb <= ref) and (la_fin >= ref)
            if boule:
                retourne = boule
                break
            else:
                retourne = boule
        return retourne

    def get_employes(self):
        """Obtenir la liste complète des employés (table sqlite) avant de les valider """
        all_emp = "SELECT distinct nom, prenom, debut, fin, id from employes order by rang"
        curseur_emp = self.conn.cursor()
        curseur_emp.execute(all_emp)
        les_emp  = curseur_emp.fetchall()
        return les_emp

    def get_dispos(self,emp):
        """Obtenir une liste des non-dipos (table sqlite) pour un employé donné"""
        find_dispo_dates_and_type = "select emp_non_dispo.t_exact_debut,emp_non_dispo.t_exact_fin, emp_non_dispo.type_non_dispo, id_empl_fk from emp_non_dispo where id_empl_fk = '%s' order by id_empl_fk"
        curseur_dispo = self.conn.cursor()
        curseur_dispo.execute(find_dispo_dates_and_type % emp)
        d = curseur_dispo.fetchall()
        return d

    def ajout_valide_dans_eq(self):  # cette fonction
        """
        Ajoute les membres aux équipes définies précédemment. Évite les répétitions et vérifie les non-dispos. Maintient les équipes d'un jour à l'autre.

        """
        conflit = bool()
        res = None
        emp_courant = ''
        dateiso = ''
        try:
            for key in self.calendrier_equipes:                         # par date
                for ix in range(0, len(self.calendrier_equipes[key])):  # par eq

                    while len(self.calendrier_equipes[key][ix][1]) < self.config_modele[0][5]:
                        emp_courant = self.liste_emp_a_assigner.pop(0)
                        res = self.get_dispos(emp_courant[4])
                        conflit = self.check_conflit(datetime.fromisoformat(key), res)
                        if conflit:
                            print("bobo avec" + str(emp_courant[4]) + " "  + str(datetime.fromisoformat(key)))
                            continue
                        else:
                            self.calendrier_equipes[key][ix][1].append(
                                emp_courant[1][0] + ". " + emp_courant[0] + " (" + str(emp_courant[4]) + ")")
                            print("Ok avec" + str(emp_courant[4])+ " "  + str(datetime.fromisoformat(key)))

                self.liste_emp_a_assigner = self.get_employes()
        except Exception:
            traceback.print_exc(file=sys.stdout)


    def assigne_empl_eq_jour(self, la_date, nom_eq):
        """Appelle fonction d,ajout des emp dasn les equipes et leur validation"""
        self.ajout_valide_dans_eq()

    def initialise_calendrier_equipes(self, nb_eq):
        """Initialiser le calendrier pour pouvoir le renseigner plus tard avec les références sur les clés"""
        self.les_cles = list(self.equipes_maximales.keys())[:nb_eq]
        lesdates = [self.les_jours[i][1] for i in range(0, len(self.les_jours))] # obtenir juste les dates

        self.calendrier_equipes = dict.fromkeys(lesdates)

        for k in self.calendrier_equipes:
            self.calendrier_equipes[k] =[]
            for i in range(0, len(self.les_cles)):

                self.calendrier_equipes[k].append([[self.les_cles[i]],[]])

    def ecriture_excel2(self):
        """Écriture dans fichier excel via xlsxwriter. 2 worksheets: une pour le calendrier des équipes, l'autre pour les membres des équipes. Gère les répétitions pour les jours, créneaux, nb d'équipes, etc."""
        workbook = xlsxwriter.Workbook('../horaire_B.xlsx')
        worksheet = workbook.add_worksheet('equipes')

        bold = workbook.add_format({'bold': True})
        cell_format_red = workbook.add_format({'bold': True, 'font_color': 'red'})
        cell_format_noir = workbook.add_format({'bold': True, 'font_color': 'black','text_wrap':'true','align':'center','valign':'top'})
        cell_format_vert = workbook.add_format({'bold': True, 'font_color': 'green','align':'center','valign':'center'})
        worksheet.set_column('A:A', 20)

        worksheet.write('A1', 'Equipes', cell_format_red)
        col = 0
        row = 0
        cpt_eq = 0
        for keys in self.calendrier_equipes:  # dates
            row = row + 1
            worksheet.write(row, col, keys, cell_format_noir)
            if cpt_eq < round(self.config_modele[0][6]):
                for indx in range(0, len(self.calendrier_equipes[keys])):  # nb eq
                    row = row +1
                    for j in range(0, len(self.calendrier_equipes[keys][indx])):
                        worksheet.write(row,col,str(self.calendrier_equipes[keys][indx][0][0]),cell_format_noir) #nom eq
                        for r in range(0, len(self.calendrier_equipes[keys][indx][1])): #nb eq
                            worksheet.write(row, col+ r + 1 ,str(self.calendrier_equipes[keys][indx][1][r]))
                    cpt_eq = cpt_eq + 1
                worksheet.set_column(row, col, 15)
        row = row + self.config_modele[0][5]
        date_prod = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        worksheet.write_string(row, col+1, "Émis le " + date_prod, cell_format_red)

# --------------autre feuille excel -------------------------------------------------------------------------
        row = 1

        worksheet2 = workbook.add_worksheet('calendrier')
        colo = 0

        worksheet2.write_string(row, colo, 'Semaine ' + str(self.config_modele[0][0]), cell_format_red) # colo passe pas ?
        colo = colo + 1

        print(str(self.config_modele))
        mod_hpers = self.config_modele[0][1]
        nb_cren = self.config_modele[0][8]
        nb_jour_sem = len(self.les_jours)
        nb_eq = self.config_modele[0][4]
        eq_par_cren = int(self.config_modele[0][7]+.5)
        calc_nb_quarts_requis= round(self.config_modele[0][6])
        empl_par_eq = self.config_modele[0][5]
        print("date de réf. :" + str(self.auj))
        print("sem : " + str(self.config_modele[0][0]))
        print("Modele : " + str(self.config_modele[0][10]) + " h-pers = " + str(mod_hpers))
        print("\t Calcul présences totales d'équipes: " + str(calc_nb_quarts_requis))
        print("\t Calcul présences individuelles: " + str(self.config_modele[0][3]))
        print("\t Créneaux par jour: " + str(nb_cren))
        print("\t Equipes par créneau: " + str(eq_par_cren))
        print("\t Nombre d'équipes: " + str(nb_eq))
        print("\t Empl. par éq.: " + str(empl_par_eq))
        print("\t Durée quart: " + str(self.config_modele[0][2]))

        eqs = self.les_cles
        eqs2 = eqs[:]
        tot_affec = 0 #suivi du nb eq affectées
        tot_h_affec = 0
        worksheet2.write(row, colo, 'Horaire')

        for i in range(1, 4):
            worksheet2.write(row, colo + i, 'Q'+ str(i), cell_format_noir)

        for ix in range(0, len(self.les_jours)):
            row = row + 1
            worksheet2.write(row, colo, str(self.les_jours[ix][0]) + "\n" + str(self.les_jours[ix][1]), cell_format_noir)
            worksheet2.set_column(row, colo, 15)
        row = row - 6
        pop_string_eq = ""
        eq_courante = ''
        for jour in range(0, nb_jour_sem):  # --- Pour chaque jour
            cpt_cren = 0  # suivi de la position pour grille
            for cren in range(1, nb_cren + 1):  # --- Pour chaque creneau
                cpt_cren = cpt_cren + 1
                colo = colo + 1  # cren_dispo
                pop_string_eq = ""  # chaine pour concat equipes dans un seul creneau (c=1 epc>1)
                for eq in range(0, eq_par_cren):  # Pour chaque equipe
                    if tot_affec < calc_nb_quarts_requis:  # and tot_h_affec < mod_hpers:  # on interrompt si le nb equipes arrive au nb_calculé
                        if len(eqs) > 0:
                            eq_courante = eqs.pop(0)  # liste eq non vide on affecte et retire une equipe
                            pop_string_eq = pop_string_eq + " " + eq_courante
                            worksheet2.write(row, colo, pop_string_eq.strip(),cell_format_vert)
                            tot_affec = tot_affec + 1
                            print(str(tot_affec))
                        else:
                            if len(eqs2) / eq_par_cren >= nb_cren:
                                eqs = eqs2[:]
                                eq_courante = eqs.pop(0)
                                pop_string_eq = pop_string_eq + " " + eq_courante
                                tot_affec = tot_affec + 1
                                print(str(tot_affec))
                                worksheet2.write_string(row, colo, pop_string_eq.strip(), cell_format_vert)
                            else:
                                eqs = eqs2[:]
                                break
                    else:
                        break

            colo = colo - cpt_cren
            row = row + 1



        colo = colo - 1
        worksheet2.write_string(row + 2, colo, "Modele : " + str(self.config_modele[0][10]) + " h-pers = " + str(self.config_modele[0][1]), cell_format_red)
        row = row + 3
        la_longue_string_modele = ""
        la_longue_string_modele = la_longue_string_modele + " Calcul pr. équipes: " + str(calc_nb_quarts_requis) + "\n"
        la_longue_string_modele = la_longue_string_modele + " Calcul prés individuelles: " + str(self.config_modele[0][3]) + "\n"
        la_longue_string_modele = la_longue_string_modele + " Créneaux par jour: " + str(nb_cren) + "\n"
        la_longue_string_modele = la_longue_string_modele + " Equipes par créneau: " + str(eq_par_cren) + "\n"
        la_longue_string_modele = la_longue_string_modele + " Nombre d'équipes: " + str(nb_eq) + "\n"
        la_longue_string_modele = la_longue_string_modele + " Empl. par éq.: " + str(self.config_modele[0][5]) + "\n"
        la_longue_string_modele = la_longue_string_modele + " Durée quart.: " + str(self.config_modele[0][2]) + "\n"
        worksheet2.write_string(row, colo, la_longue_string_modele, cell_format_noir)
        worksheet2.set_column(row, colo, 23)
        row = row + 2
        date_prod = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        worksheet2.write_string(row, colo+1, "Émis le " + date_prod, cell_format_red)
        workbook.close()

if __name__ == '__main__':
    appli = horaire('2022-04-01 12:12')
    print(str(appli.calendrier_equipes))
    appli.conn.close()

#  config_modele [0][v. liste suivante]
# 0 = num de semaine
# 1 = heures-personnes prévues
# 2 = durée d'une journée/quart de travail
# 3 = nb presences indivisuelles calculé
# 4 = nb équipes
# 5 = nb employés pas équipe
# 6 =  calcul du nb prévu de quarts en équipe
# 7 = nb équipes par créneau/quart
# 8 = nb de créneaux par jour
# 9 = calcul nb de jours requis
# 10 = nom du modèlle
