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
#        [0][v. liste suivante]
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
        #10 = nom du modèlle

        self.nom_modele = self.config_modele[0][10]

        if self.equipes == {}:
            self.initialise_dict_equipe(self.config_modele[0][4])

        for nom_eq in self.equipes:

            if (len(self.equipes[nom_eq][1]) < self.config_modele[0][5]): # !! le nb des equipes vient du modele et initialise...
                if (self.cpt_heures < self.hpers): # pour les fractions d'équipe (il y a répartition plus loin)
                    self.equipes[nom_eq][1].append(emp[1][0] + ". " + emp[0])
                    self.cpt_heures = self.cpt_heures + self.config_modele[0][2]
                break
            else:
                continue



        # for nom_eq in self.equipes:
        #     print(str(len(self.equipes[nom_eq][1])) + " < " + str(config_modele[0][4]))
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


        for j in range(0, int(self.config_modele[0][6])): # calcul quart par eq indique le nb de presences totales/nb par eq. ça saute ume colonne/journée
            for i in range(0, self.config_modele[0][7]): # je repete dans rangeee suivante si + de crenaux
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
        cell_format_noir = workbook.add_format({'bold': True, 'font_color': 'black','text_wrap':'true','align':'center'})

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

        worksheet.write_string(row, colo, 'Semaine ' + str(self.config_modele[0][0]), cell_format_red) # colo passe pas ?
        colo = colo + 1

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

        print(str(self.config_modele))
        nb_cren = self.config_modele[0][8]
        nb_jour_sem = len(self.les_jours)
        nb_eq = len(self.equipes)
        eq_par_cren = int(self.config_modele[0][7]+.5)
        calc_nb_quarts_requis= int(self.config_modele[0][6] + .5)
        print("date de réf. :" + str(self.auj))
        print("sem : " + str(self.config_modele[0][0]))
        print("Modele : " + str(self.config_modele[0][10]) + " h-pers = " + str(self.config_modele[0][1]))
        print("\t Calcul présences totales d'équipes: " + str(calc_nb_quarts_requis))
        print("\t Calcul présences individuelles: " + str(self.config_modele[0][3]))
        print("\t Créneaux par jour: " + str(nb_cren))
        print("\t Equipes par créneau: " + str(eq_par_cren))
        print("\t Empl. par éq.: " + str(self.config_modele[0][5]))

        # ligne1
        eqs = list(self.equipes)
        eqs2 = eqs[:]
        tot_affec = 0
        worksheet.write(row, colo, 'Horaire')
        for i in range(1, 4):
            worksheet.write(row, colo + i, 'Q'+ str(i))

        for ix in range(0, len(self.les_jours)):
            row = row + 1
            worksheet.write(row, colo, str(self.les_jours[ix][0]) + "\n" + str(self.les_jours[ix][1]), cell_format_noir)

            worksheet.set_column(row, colo, 15)

        row = row - 6
        pop_string_eq =""
# // todo : algo qui répète une seule fois les equipes pour une journée donnée, et qui passe toutes les equipes
#   avant de recommencer la liste

        for jour in range(0, nb_jour_sem):
            print(self.les_jours[jour][0])
            cpt_cren = 0
            for cren in range(1, nb_cren + 1):
                cpt_cren = cpt_cren + 1
                colo = colo +1# cren_dispo
                print("\tcren " + str(cren))
                pop_string_eq = ""
                for eq in range(0, eq_par_cren):
                                       ##eq par creneau #// TODO ne pas resetter equipes
                    if tot_affec <  calc_nb_quarts_requis:
#                        print('check ' + str(tot_affec) + " nb " + str(calc_nb_quarts_requis))
                        if len(eqs) > 0:
                            pop_string_eq = pop_string_eq + " " + eqs.pop(0)
                            worksheet.write(row, colo, pop_string_eq.strip())
                            print(
                                "\t\teq# " + str(eq) + " " + pop_string_eq)  # //todo gestion des equipes deja assignees ?
                            tot_affec = tot_affec + 1
                        else:
                            eqs = eqs2[:]
                            pop_string_eq = pop_string_eq + " " + eqs.pop(0)
                            if cren == nb_cren and len(eqs) == 0:
                                print(
                                    "\t\teq# " + str(eq) + " " + pop_string_eq)
                                tot_affec = tot_affec + 1

                                # si je suis au dernier creneau de la journee et len(eqp = 0)
                        #         print('FFF')

                            # else:
                            #     pop_string_eq = pop_string_eq + " " + eqs.pop(0)
                            #     worksheet.write_string(row, colo, pop_string_eq.strip())
                            #     print(
                            #      "\t\teq# " + str(eq) + " " + pop_string_eq.strip())  # //todo gestion des equipes deja assignees ?
                            #     tot_affec = tot_affec + 1
                    else:
                        break
            colo = colo - cpt_cren
            row = row + 1
            col = col -1
        worksheet.write_string(row + 2, colo, "Modele : " + str(self.config_modele[0][10]) + " h-pers = " + str(self.config_modele[0][1]), cell_format_red)

        workbook.close()

appli = horaire('2022-04-01 12:12')
#appli = horaire('2022-01-14 12:12')

appli.conn.close()

#// TODO