import calendar
import locale

import sys
import traceback
from datetime import datetime, date, timedelta
from util_compose_equipes import CompositionEquipes
import xlsxwriter as xl
from xlsxwriter import format
class prod_chiffrier:
    semaine = 6
    @staticmethod
    def print_dict(le_dict):
        for j in le_dict:
            print(j)
            for v in le_dict.values():
                print(v)
    @staticmethod
    def ecriture_excel2():
        dict_semaine =  CompositionEquipes.get_emp_dispo(0,2024,prod_chiffrier.semaine)
        prod_chiffrier.print_dict(dict_semaine)
        date_prod = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        e = datetime
        nomfich = e.today().strftime('%y_%m_%d_%H%M')
        wb = xl.Workbook('.\\builds_xlsx\\rev3_' + nomfich + '.xlsx')
        ws = wb.add_worksheet('Équipes')

        bold = wb.add_format({'bold': True})
        cell_format_red = wb.add_format({'bold': True, 'font_color': 'red', 'font_size': '20','align': 'center','valign':'vcenter' })
        cell_format_noir = wb.add_format({'bold': True, 'font_color': 'black','text_wrap':'true','align':'center','valign':'vcenter'})
        ws.set_column('A:A', 20)
        ws.write(1,0, "Émis le :")
        ws.set_row(2, 20)
        ws.write(2, 0,date_prod, cell_format_noir)
        ws.set_row(0, 44)
        ws.write('A1', 'Equipes', cell_format_red)
        col = 2
        row = 3
        s_jour_date = CompositionEquipes.semaine
        #print(s_jour_date)
        for jour in s_jour_date:  # dates
            ws.set_column(col, col, 18)
            ws.write_string(row, col, jour[0], cell_format_noir)
            col = col + 1
            ws.set_column(col,col, 18)
            ws.write_string(row, col, jour[1][:10], cell_format_noir)
            col = col -1
            row = row + 1
        ###############
        ws = wb.add_worksheet('Modèle')
        le_modele = CompositionEquipes.modele
        une_string = "Semaine # " + str(le_modele.prev_num_sem) + ", Nb quarts: " + str(le_modele.nb_quarts) + ", Nb équipes par quart: " + str(le_modele.nb_equipes_par_q) +", Nb employés par équipes: " + str(le_modele.nb_emplo_par_eq)
        #cell_format = wb.add_format({'bold': True, 'font_color': 'red'})

        ws.merge_range(1,1,3,15, '')
        ws.write_string(1,1, str(une_string),cell_format_red)
        #################
        #         for j in range(0, len(self.calendrier_equipes[keys][indx])):
        #             ws.write(row,col,str(self.calendrier_equipes[keys][indx][0][0]),cell_format_noir) #nom eq
        #             for r in range(0, len(self.calendrier_equipes[keys][indx][1])): #nb eq
        #                 ws.write(row, col+ r + 1 ,str(self.calendrier_equipes[keys][indx][1][r]))
        #     ws.set_column(row, col, 15)
        # row = row + self.config_modele[0][5]
        # date_prod = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        # ws.write_string(row, col+1, "Émis le " + date_prod, cell_format_red)
        #
        # # --------------autre feuille excel -------------------------------------------------------------------------
        # row = 1
        #
        # ws2 = wb.add_ws('calendrier')
        # colo = 0
        #
        # ws2.write_string(row, colo, 'Semaine ' + str(self.config_modele[0][0]), cell_format_red) # colo passe pas ?
        # colo = colo + 1
        #
        # print(str(self.config_modele))
        # mod_hpers = self.config_modele[0][1]
        # nb_cren = self.config_modele[0][8]
        # nb_jour_sem = len(self.les_jours)
        # nb_eq = self.config_modele[0][4]
        # eq_par_cren = int(self.config_modele[0][7]+.5)
        # calc_nb_quarts_requis= round(self.config_modele[0][6])
        # empl_par_eq = self.config_modele[0][5]
        # print("date de réf. :" + str(self.auj))
        # print("sem : " + str(self.config_modele[0][0]))
        # print("Modele : " + str(self.config_modele[0][10]) + " h-pers = " + str(mod_hpers))
        # print("\t Calcul présences totales d'équipes: " + str(calc_nb_quarts_requis))
        # print("\t Calcul présences individuelles: " + str(self.config_modele[0][3]))
        # print("\t Créneaux par jour: " + str(nb_cren))
        # print("\t Equipes par créneau: " + str(eq_par_cren))
        # print("\t Nombre d'équipes: " + str(nb_eq))
        # print("\t Empl. par éq.: " + str(empl_par_eq))
        # print("\t Durée quart: " + str(self.config_modele[0][2]))
        #
        # # ligne1
        # eqs = self.les_cles
        # eqs2 = eqs[:]
        # tot_affec = 0
        # tot_h_affec = 0
        # ws2.write(row, colo, 'Horaire')
        #
        # for i in range(1, 4):
        #     ws2.write(row, colo + i, 'Q'+ str(i))
        #
        # for ix in range(0, len(self.les_jours)):
        #     row = row + 1
        #     ws2.write(row, colo, str(self.les_jours[ix][0]) + "\n" + str(self.les_jours[ix][1]), cell_format_noir)
        #     ws2.set_column(row, colo, 15)
        # row = row - 6
        # pop_string_eq = ""
        #
        # eq_courante = ''
        # for jour in range(0, nb_jour_sem):                  #--- Pour chaque jour
        #     cpt_cren = 0                                    # suivi de la position pour grille
        #     for cren in range(1, nb_cren + 1):              #--- Pour chaque creneau
        #         cpt_cren = cpt_cren + 1
        #         colo = colo +1# cren_dispo
        #         pop_string_eq = ""                          #chaine pour concat equipes dans un seul creneau (c=1 epc>1)
        #         for eq in range(0, eq_par_cren):            # Pour chaque equipe
        #             if tot_affec <  calc_nb_quarts_requis: # and tot_h_affec < mod_hpers:  # on interrompt si le nb equipes arrive au nb_calculé
        #                 if len(eqs) > 0:
        #                     eq_courante = eqs.pop(0)  # liste eq non vide on affecte et retire une equipe
        #                     pop_string_eq = pop_string_eq + " " + eq_courante
        #                     ws2.write(row, colo, pop_string_eq.strip())
        #                     tot_affec = tot_affec + 1
        #                 else:
        #                     if len(eqs2)/eq_par_cren >=  nb_cren:
        #                         eqs = eqs2[:]
        #                         eq_courante = eqs.pop(0)
        #                         pop_string_eq = pop_string_eq + " " + eq_courante
        #                         tot_affec = tot_affec + 1
        #                         ws2.write_string(row, colo, pop_string_eq.strip())
        #                     else:
        #                         eqs = eqs2[:]
        #                         break
        #
        #             else:
        #                 break
        #     colo = colo - cpt_cren
        #     row = row + 1
        #
        # colo = colo - 1
        # ws2.write_string(row + 2, colo, "Modele : " + str(self.config_modele[0][10]) + " h-pers = " + str(self.config_modele[0][1]), cell_format_red)
        # row = row + 3
        # la_longue_string_modele = ""
        # la_longue_string_modele = la_longue_string_modele + " Calcul pr. équipes: " + str(calc_nb_quarts_requis) + "\n"
        # la_longue_string_modele = la_longue_string_modele + " Calcul prés individuelles: " + str(self.config_modele[0][3]) + "\n"
        # la_longue_string_modele = la_longue_string_modele + " Créneaux par jour: " + str(nb_cren) + "\n"
        # la_longue_string_modele = la_longue_string_modele + " Equipes par créneau: " + str(eq_par_cren) + "\n"
        # la_longue_string_modele = la_longue_string_modele + " Nombre d'équipes: " + str(nb_eq) + "\n"
        # la_longue_string_modele = la_longue_string_modele + " Empl. par éq.: " + str(self.config_modele[0][5]) + "\n"
        # la_longue_string_modele = la_longue_string_modele + " Durée quart.: " + str(self.config_modele[0][2]) + "\n"
        # ws2.write_string(row, colo, la_longue_string_modele, cell_format_noir)
        # ws2.set_column(row, colo, 23)
        # row = row + 2
        # date_prod = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        # ws2.write_string(row, colo+1, "Émis le " + date_prod, cell_format_red)
        wb.close()

prod_chiffrier.ecriture_excel2() #juste pourverifier quelques lignes sinon ça plante pour le moment