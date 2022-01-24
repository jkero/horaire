import sqlite3
import sys, traceback, calendar, locale
from datetime import datetime, timedelta
from sqlite3 import Error
import xlsxwriter



# pour demarrer la generation de l'horaire pour une période donnée, ça prend la saisie de valeurs de base.
# nb employes
# nb equipes
# prévisions heures/personnes pour la période v. table previsions_hpers
# self.auj= datetime.today()
# self.auj2 = "2022-01-03 01:00"
# dt_string = self.auj.strftime("%Y-%m-%d %H:%M")
# print("date = " + dt_string)
# print("semaine " + str((self.auj).isocalendar()[1]))

class horaire:
    auj = ''
    week= ''
    les_jours = []
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
    cpt_heures = 0
    valeur_repartition = 0
    nom_modele = ''
    config_modele = None

    def __init__(self, la_journee):
        self.auj = datetime.fromisoformat(la_journee)        
        self.week = str((self.auj).isocalendar()[1])
        try:
            self.create_connection(r"C:\Users\j\Documents\pythonProject\matrice_temps\letemps.db")
            self.post_init()
        except Exception as e:
            print(e)
            traceback.print_exc(file=sys.stdout)




    def post_init(self):
        try:
            if self.conn is not None:
                string_previsions_config = "select previsions_hpers.hpers, previsions_hpers.heures_par_jour, \
                    previsions_hpers.nb_max_par_eq, round(previsions_hpers.hpers / previsions_hpers.heures_par_jour,1) as nb_quart_eq," \
                                           " round(round(previsions_hpers.hpers / previsions_hpers.heures_par_jour,1)/" \
                                           "previsions_hpers.nb_max_par_eq,1) as nb_quarts from previsions_hpers  where annee = ? and semaine = ?"
                cur_previsions = self.conn.cursor()
                print("date de réf. :" + str(self.auj))
                print("sem : " + str(self.week))
                liste_prev = cur_previsions.execute(string_previsions_config, (self.auj.year, self.week)).fetchall()
                self.hpers = liste_prev[0][0]
                print("Prévisions pour " + str(self.hpers) + " h-pers")
                self.duree_quart = liste_prev[0][1]
                print("\t duree_quart: " + str(self.duree_quart))
                self.nb_quarts_indivi = liste_prev[0][3] # prev hpers/heures par quart
                print("\t nb_quart_indivi: " + str(self.nb_quarts_indivi))
                self.max_emp_par_equipe = liste_prev[0][2]
                print("\t max emp par eq: " + str(self.max_emp_par_equipe))
                self.nb_quart_en_eq = liste_prev[0][4]
                print("\t nb quarts en eq: " + str(self.nb_quart_en_eq))
                self.employes_tot = self.select_count_emp_dispo()
                print("\t employes_tot: " + str(self.select_count_emp_dispo()))

                self.les_dates_de_la_semaine = self.semaine()

                # cpt_key = 0
                # for key in self.equipes_maximales:
                #     if cpt_key < round(self.nb_quart_en_eq,1):
                #         self.equipes[key] = self.equipes_maximales[key]
                #     cpt_key = cpt_key + 1

                self.attribution_equipe()

        except Exception as e:
            print(e)
            traceback.print_exc(file=sys.stdout)


    def semaine(self):
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
        """ create a database connection to a SQLite database """
        try:
            self.conn = sqlite3.connect(db_file)
            if self.conn is not None:
                count = 0
                # for key in self.equipes_maximales:
                #     if count < round(self.employes_requis/self.max_emp_par_equipe):
                #         self.equipes[key] = self.equipes_maximales[key]
                #         count  = count + 1
    
    #            print (str(equipes))
    

    
    # la composition des equipes doit se faire par jour, à cause des non-dispos qui peuvent être une seule journée. //TODO attribution selon boucle par jour pour semaine en cours
            else:
                print("Error! cannot create the database connection.")
    
        except Error as e:
                print(e)
    

    
    def calcul_equipes(self):
        print("---------")
    
    
    def select_hpers(self):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.conn.cursor()
        res = cur.execute("SELECT hpers FROM previsions_hpers where semaine = " + self.week).fetchone()
        return res[0]
    
    def select_count_emp_dispo(self):
        """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
        """
        cur = self.conn.cursor()
        res = cur.execute("select distinct count(id) from employes order by rang").fetchone()
        return res[0]
    
    def check_conflit(self, ref, res_non_dispo, conn):
        deb = res_non_dispo[0]
        fin = res_non_dispo[1]
        le_deb = datetime.fromisoformat(deb)
        la_fin = datetime.fromisoformat(fin)

        if (str((ref <= la_fin) & (ref >= le_deb))) == 'True':
            retourne = (str((ref <= la_fin) & (ref >= le_deb)))
            print("\n conflit de " + str(ref) + " pour date de" + str(le_deb) + " à " + str(la_fin))
        else:
            retourne= "False"
        return retourne

    def attribution_equipe(self):
        all_emp = "SELECT distinct nom, prenom, debut, fin, id from employes order by rang"

        find_dispo_dates_and_type = "select emp_non_dispo.t_exact_debut,emp_non_dispo.t_exact_fin, emp_non_dispo.type_non_dispo, id_empl_fk from emp_non_dispo where id_empl_fk = '%s' order by id_empl_fk"

        curseur_emp = self.conn.cursor()

        curseur_dispo = self.conn.cursor()

        curseur_emp.execute(all_emp)
        rows = curseur_emp.fetchall()

        #    self.conn.set_trace_callback(print)

        try:
            for emp in rows:
                curseur_dispo.execute(find_dispo_dates_and_type % str(emp[4]))
                res = curseur_dispo.fetchall()

                skip_emp = 'True'
                if len(res) > 0:
                    for enr_dispo in res:
                        conflit = self.check_conflit(self.auj, enr_dispo, self.conn)
                        if conflit == 'True':
                            skip_emp = 'True'
                            print('\n ************** ' + str(emp[1]).upper() + " " + str(
                                emp[0]).upper() + " exclu " + conflit)
                            break
                        else:
                            skip_emp = 'False'

                    if skip_emp == 'False':
                        print(str(emp[4]) + " peut passer")
                        self.affecte_equipes_modele(emp)
                else:
                    self.affecte_equipes_modele(emp)

            #self.ecrire_equipes_excel()
            self.ecriture_excel2()
            print("\n" + str(self.equipes))

        except Exception:
            traceback.print_exc(file=sys.stdout)

    def affecte_equipes(self, emp):
        if self.equipes == {}:
            self.initialise_dict_equipe(0)

        if self.nb_quart_en_eq - int(self.nb_quart_en_eq) > 0.00:
            print("! valeurs reparties")
            self.valeur_repartition = int(self.nb_quarts_indivi/(self.nb_quart_en_eq + 0.5) +.5)

        for nom_eq in self.equipes:
            if (len(self.equipes[nom_eq][1]) < self.valeur_repartition) and (self.cpt_heures < self.hpers) :
                self.equipes[nom_eq][1].append(emp[1][0] + ". " + emp[0])
                self.cpt_heures = self.cpt_heures + self.duree_quart
                break
            else:
                continue
# equipes inegales si nb_quart_en_eq est fractionnaire le_nb - int(le_nb) <> 0.0000.
# alors il y a une répartition à faire 7/7/4 devient 6/6/6
# je prends nb_quart_indivi / int(nb_quart_en_eq + .5) j'ai un montant moyen par équipe, je l'arrondis à l'entier suivant.
# ça donne le chiffre qui rmeplace le nb max par equipes

    def affecte_equipes_modele(self, emp):
        sql_modele_affect = "select p.hpers, p.heures_par_jour, round(p.hpers / p.heures_par_jour,1) as presences, m.nb_eq, m.nb_emp_par_eq as nb_par_eq, \
                                round(round(p.hpers *1.0 / p.heures_par_jour,1)/m.nb_emp_par_eq,1) as nb_quarts_eq,\
                                 m.nb_eq_par_creneau, m.nb_creneau_disp , \
                                 round(round(cast(p.hpers as float) / p.heures_par_jour,2) / \
                                (m.nb_emp_par_eq * m.nb_eq_par_creneau * m.nb_creneau_disp),2) as jours, m.nom \
                                from previsions_hpers as p \
                                inner join modele_assignation_hebdo as m \
                                on p.modele = m.id \
                                where p.semaine = 11" #+ str(self.week)

        cur_modele = self.conn.cursor()
        self.config_modele = cur_modele.execute(sql_modele_affect).fetchall()
        # 1 = heures_par_jour
        # 2 = presences
        # 3 = nb_eq
        # 4 = nb_quarts-eq
        # 5 = nbeq_par_creneau
        # 6 = nb creneau
        # 7 = jours
        # 8 = nom modele

        self.nom_modele = self.config_modele[0][9]

        if self.equipes == {}:
            self.initialise_dict_equipe(self.config_modele[0][3])

        for nom_eq in self.equipes:

            if (len(self.equipes[nom_eq][1]) < self.config_modele[0][4]): # !! le nb des equipes vient du modele et initialise...
                if (self.cpt_heures < self.hpers):
                    self.equipes[nom_eq][1].append(emp[1][0] + ". " + emp[0])
                    self.cpt_heures = self.cpt_heures + self.config_modele[0][1]
                break
            else:
                continue



        # for nom_eq in self.equipes:
        #     print(str(len(self.equipes[nom_eq][1])) + " < " + str(config_modele[0][3]))
        #     if (len(self.equipes[nom_eq][1]) < config_modele[0][3]) and (self.cpt_heures < self.hpers):
        #         self.equipes[nom_eq][1].append(emp[1][0] + ". " + emp[0])
        #         self.cpt_heures = self.cpt_heures + config_modele[0][1]
        #         break
        #     else:
        #         continue

    # equipes inegales si nb_quart_en_eq est fractionnaire le_nb - int(le_nb) <> 0.0000.
    # alors il y a une répartition à faire 7/7/4 devient 6/6/6
    # je prends nb_quart_indivi / int(nb_quart_en_eq + .5) j'ai un montant moyen par équipe, je l'arrondis à l'entier suivant.
    # ça donne le chiffre qui rmeplace le nb max par equipes

    def initialise_dict_equipe(self, nb_eq):
        count = 0
        for key in self.equipes_maximales:
            if nb_eq > 0:
                if count < round(nb_eq):
                    self.equipes[key] = self.equipes_maximales[key]
                    count  = count + 1
            else:
                if count < round(self.employes_requis/self.max_emp_par_equipe):
                    self.equipes[key] = self.equipes_maximales[key]
                    count  = count + 1



    def ecrire_equipes_excel(self):
        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook('horaire_A.xlsx')
        worksheet = workbook.add_worksheet('equipes')

        bold = workbook.add_format({'bold': True})
        cell_format_red = workbook.add_format({'bold': True, 'font_color': 'red'})
        cell_format_noir = workbook.add_format({'bold': True, 'font_color': 'black'})
    
        # Widen the first column to make the text clearer.
        worksheet.set_column('A:A', 20)

        # Write some simple text.
        worksheet.write('A1', 'Equipes', cell_format_red)
        col = 0
        row = 0

        for keys in self.equipes: #A-E
            col = col + 1
            for indx_eq in range(1, len(self.equipes[keys][1])+1): #4
                worksheet.write(row, col, keys, cell_format_noir)
                worksheet.write((row + indx_eq), col, self.equipes[keys][1][indx_eq-1])
                worksheet.set_column(row, col + indx_eq, 15)

        row = row + (len(self.equipes['A'][1]) + 3)
        colo = 0

        worksheet.write_string(row, colo, 'Semaine ' + str(self.week), cell_format_red) # colo passe pas ?
        colo = colo + 2 #//TODO si les colonnes sont doublees ne pas affecter le tableau du haut
        for i in range (0, len(self.les_jours)):
            worksheet.write(row, colo + i, self.les_jours[i][0], cell_format_noir)
            worksheet.write(row + 1, colo + i, self.les_jours[i][1])
            worksheet.set_column(row, colo + i, 15)

        row = row + 2


        for j in range(0, int(self.config_modele[0][5])): # calcul quart par eq indique le nb de presences totales/nb par eq. ça saute ume colonne/journée
            for i in range(0, self.config_modele[0][6]): # je repete dans rangeee suivante si + de crenaux
                for keys in self.equipes:
                    worksheet.write(row + i, colo + j, keys)

        # logique de presentation :  les colonnes des jours sont multipliees par nb_creneau_disp
#       et écrites selon nb_eq_par_creneau (un creneau = une colonne appartenant a une journee)
#        self.config_modele
        # 1 = heures_par_jour
        # 2 = presences
        # 3 = nb_eq
        # 4 = nb_quarts-eq
        # 5 = nbeq_par_creneau
        # 6 = nb creneau
        # 7 = jours
        # 8 = nom modele


        row = row + (len(self.equipes['A'][1]) + 3) + 10

        colo = 0
        worksheet.write_string(row, colo, 'Modèle ' + str(self.nom_modele), cell_format_red)

        # Insert an image.
    #    worksheet.insert_image('B5', 'logo.png')
    
        workbook.close()
    
    def ecriture_excel2(self):
        # Create an new Excel file and add a worksheet.
        workbook = xlsxwriter.Workbook('horaire_B.xlsx')
        worksheet = workbook.add_worksheet('equipes')

        bold = workbook.add_format({'bold': True})
        cell_format_red = workbook.add_format({'bold': True, 'font_color': 'red'})
        cell_format_noir = workbook.add_format({'bold': True, 'font_color': 'black'})

        # Widen the first column to make the text clearer.
        worksheet.set_column('A:A', 20)

        # Write some simple text.
        worksheet.write('A1', 'Equipes', cell_format_red)
        col = 0
        row = 0

        for keys in self.equipes:  # A-E
            col = col + 1
            for indx_eq in range(1, len(self.equipes[keys][1]) + 1):  # 4
                worksheet.write(row, col, keys, cell_format_noir)
                worksheet.write((row + indx_eq), col, self.equipes[keys][1][indx_eq - 1])
                worksheet.set_column(row, col + indx_eq, 15)

        row = row + (len(self.equipes['A'][1]) + 3)
        colo = 0

        worksheet.write_string(row, colo, 'Semaine ' + str(self.week), cell_format_red) # colo passe pas ?
        colo = colo + 2 #//TODO si les colonnes sont doublees ne pas affecter le tableau du haut
        for i in range (0, len(self.les_jours)):
            worksheet.write(row, colo + i, self.les_jours[i][0], cell_format_noir)
            worksheet.write(row + 1, colo + i, self.les_jours[i][1])
            worksheet.set_column(row, colo + i, 15)

        row = row + 2


#        for j in range(0, int(self.config_modele[0][5])): # calcul quart par eq indique le nb de presences totales/nb par eq. ça saute ume colonne/journée
#            for i in range(0, self.config_modele[0][6]): # je repete dans rangeee suivante si + de crenaux
#                for keys in self.equipes:
#                    worksheet.write(row + i, colo + j, keys)



        # 1 = heures_par_jour
        # 2 = presences
        # 3 = nb_eq
        # 4 = nb_quarts-eq
        # 5 = nbeq_par_creneau
        # 6 = nb creneau
        # 7 = jours
        # 8 = nom modele
        print(str(self.config_modele))
        nb_cren = self.config_modele[0][6]
        nb_jour_sem = len(self.les_jours)
        nb_eq = len(self.equipes)
        eq_par_cren = int(self.config_modele[0][5]+.5)
        calc_nb_quarts_requis= int(self.config_modele[0][6] + .5)
        print("date de réf. :" + str(self.auj))
        print("sem : " + str(self.week))
        print("Modele : " + str(self.hpers) + " h-pers")
        print("\t Calcul présences totales d'équipes: " + str(self.config_modele[0][6]))
        print("\t Calcul présences individuelles: " + str(self.config_modele[0][2]))
        print("\t Créneaux par jour: " + str(self.config_modele[0][7]))
        print("\t Equipes par créneau: " + str(self.config_modele[0][6]))

        # ligne1
        eqs = list(self.equipes)
        eqs2 = eqs[:]
        tot_affec = 0
        for jour in range(0, nb_jour_sem):
            print(self.les_jours[jour][0])
            for cren in range(1, nb_cren + 1):  # cren_dispo
                print("\tcren " + str(cren))
                for eq in range(0, eq_par_cren):  ##eq par creneau #// TODO ne pas resetter equipes
                    if tot_affec <  calc_nb_quarts_requis:
                        if len(eqs) > 0:
                            worksheet.write(row + cren, colo + jour, keys)
                            print(
                                "\t\teq# " + str(eq) + " " + eqs.pop(0))  # //todo gestion des equipes deja assignees ?
                            tot_affec = tot_affec + 1
                        else:
                            eqs = eqs2[:]
                            worksheet.write_string(row + cren, colo + jour, keys)
                            print(
                                "\t\teq# " + str(eq) + " " + eqs.pop(0))  # //todo gestion des equipes deja assignees ?
                            tot_affec = tot_affec + 1
                    else:
                        break
                    row = row + cren

        workbook.close()
    # //TODO on affecte les équipes TQ hpers = hpers des prévisions - ou alors c'est une fonction "quarts" qui s'en occupe
    # par exemple : prev = 140 hpers, max_pers_eq = 4, self.duree_quart = 7.5 alors on a:
    # 140 / 7.5 = 18.7 jours/pers ; 18.7/4 = 4.7 (5) quart-équipes. À un quart par jour ça fait 5 jours. A 3 quarts pas jour
    #  ça fait 1.7 jour. La règle du nb de quarts par jour devrait être un chiffre dans la table des prévisions, puisque
    #  les chiffres sont logiquement reliés. //TODO nb_eq-quarts (prev ~ hpers), ordre assign.des créneaux-quarts, plages des créneaux-quarts
    #//TODO modelr la talbe des previsions pour refleter plusieurs regles de gestion

    #//TODO la production de l'horaire doit indiquer seulement les affectations nécessaires dans les quarts/créneaux horaires
    #  faire la différence entre quart-eq et organisaiton du nombre de quarts par jour
    #  comment répartir les équipes composées ?
    #  comment placer le nombre maximal d'équipes à composer pour ensuite assigner les quarts dans l'horaire
    # logique des répartiion hebdomadaire des heures/equipes
    # par ex: 140 hpers donne 3 équipes. le 3 a été déterminé par 140 / ( 8 h/jr * 7 par eq)
    # est-ce que je peux décider à l'avance du nombre d'équipes pour pouvoir les distribuer sur un nombre de quarts (aussi dans les prévisions).
    # une equipe a un chef, le chef se rapporte au sup. de quart. Sur un quart il pourrait y avoir plusieurs équipes ?
    # il doit y avoir une formule pour optimiser, à partir de h-pers anticipé les heures des emp, les nb eq, equipiers par eq, quarts par jour
    # //TODO créer table des journées non dispo (congés statutaires, etc) pour éviter des assignations nulles
    # la formule mentionnée ci-haut doit donner une répartition égale des heures sur la semaine ? Ou alors une concentration d'efforts,
    #   par exemple les 3 quarts de 6 personnes peuvent être le même jour, voire dans le même créneau horaire, ou bien répartis en équipes de
    # 2, ce qui ferait 9 quarts à répartir dans la semaine.
    # préparer des modèles d'horaires de quart qui peuvent correspondre à des règles de gestion.
    #    genre m1: prioriser des équipes pleines, et minimum de créneaux-quarts (eq <> quart) 140 = 3eq * 6pers * 8h sur un seul quart
    #          m2: prioriser eq minimales et maximiser jours de travail 140  = 9eq * 2pers * 8h sur ? jours (selon créneaux prévus)
    #                                                                                        9eq/5jours = ~2 eq. par jour de travail?
    #          m3: prioriser eq minimales et maximiser creneau-quart/jour 140  = 9eq * 2pers * 8h sur ? créneaux-quart (selon créneaux min et max prévus)
    #                                                                                        9eq/5jours = ~2 eq. par jour de travail?

 # la logique equipes + hpers + quarts est en partie ici.

# 50 heures personnes signifie qu'un travail a besoin de 50 heures * 1 personne
# si on a 5 personnes ça fait 5 personnes * 10 heures. ici 10 heures serait la durée d'un quart typique -- à définir dans une constante (K1)

# Définition
# Unité de mesure correspondant au travail qui peut être accompli par une personne pendant une heure,
# par deux personnes pendant une demi-heure et ainsi de suite, et qui sert, dans le budget, à répartir
# les crédits affectés à la main-d'œuvre.

# il faut déterminer le nb max d'employés dans un équipe -- une autre constante (K2).

# Pour cette semaine on a besoin de (total_hpers/self.duree_quart) 50/7.5 = 6.6 personnes de quart (de 7.5 heures).

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

#print(datetime.fromisoformat(self.auj2).isocalendar()[1])
# trouver le dimanche de la semaine sqlite SELECT date('2022-01-22','-6 day', 'weekday 0'); // 2022-01-16
# la semaine de ce dimanche SELECT strftime('%W',date('2022-01-16','-6 day', 'weekday 0')); // 02
# self.auj = datetime.today()
# self.auj.strftime('%Y-%m-%d')
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

#   //TODO autre detail: equipes ont un quart determiné et il faudra tenter de verifier quarts par defaut des employes en les placant dans les equipes
#   //TODO le nb d'equipes et le dictionnaire doivent être automatiques
#   //TODO vu les modifs à  la table previsions, modifier le traitement des nombres fondamentaux
# //TODO validation des jours du modele v. les jours dans la semaine (un modele peut prendre plus de 4 ou 5 jours)
appli = horaire('2022-04-01 12:12')

appli.conn.close()