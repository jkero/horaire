import calendar
import locale

import sys
import traceback
from datetime import datetime, date, timedelta
from sqlite3 import Error
import xlsxwriter

@staticmethod
def ecriture_excel2():
    date_prod = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    e = datetime
    nomfich = e.today().strftime('%y_%m_%d_%H%M')
    workbook = xlsxwriter.Workbook('builds_xlsx/rev3_' + nomfich + '.xlsx')
    worksheet = workbook.add_worksheet('equipes')
    bold = workbook.add_format({'bold': True})
    cell_format_red = workbook.add_format({'bold': True, 'font_color': 'red'})
    cell_format_noir = workbook.add_format({'bold': True, 'font_color': 'black','text_wrap':'true','align':'center','valign':'top'})
    worksheet.set_column('A:A', 20)
    worksheet.write(1,0, "Émis le " + date_prod)
    worksheet.write('A1', 'Equipes', cell_format_red)
    workbook.close()
    col = 0
    # row = 0
    # for keys in self.calendrier_equipes:  # dates
    #     row = row + 1
    #     worksheet.write(row, col, keys, cell_format_noir)
    #     for indx in range(0, len(self.calendrier_equipes[keys])):  # nb eq
    #         row = row +1
    #         for j in range(0, len(self.calendrier_equipes[keys][indx])):
    #             worksheet.write(row,col,str(self.calendrier_equipes[keys][indx][0][0]),cell_format_noir) #nom eq
    #             for r in range(0, len(self.calendrier_equipes[keys][indx][1])): #nb eq
    #                 worksheet.write(row, col+ r + 1 ,str(self.calendrier_equipes[keys][indx][1][r]))
    #     worksheet.set_column(row, col, 15)
    # row = row + self.config_modele[0][5]
    # date_prod = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    # worksheet.write_string(row, col+1, "Émis le " + date_prod, cell_format_red)
    #
    # # --------------autre feuille excel -------------------------------------------------------------------------
    # row = 1
    #
    # worksheet2 = workbook.add_worksheet('calendrier')
    # colo = 0
    #
    # worksheet2.write_string(row, colo, 'Semaine ' + str(self.config_modele[0][0]), cell_format_red) # colo passe pas ?
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
    # worksheet2.write(row, colo, 'Horaire')
    #
    # for i in range(1, 4):
    #     worksheet2.write(row, colo + i, 'Q'+ str(i))
    #
    # for ix in range(0, len(self.les_jours)):
    #     row = row + 1
    #     worksheet2.write(row, colo, str(self.les_jours[ix][0]) + "\n" + str(self.les_jours[ix][1]), cell_format_noir)
    #     worksheet2.set_column(row, colo, 15)
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
    #                     worksheet2.write(row, colo, pop_string_eq.strip())
    #                     tot_affec = tot_affec + 1
    #                 else:
    #                     if len(eqs2)/eq_par_cren >=  nb_cren:
    #                         eqs = eqs2[:]
    #                         eq_courante = eqs.pop(0)
    #                         pop_string_eq = pop_string_eq + " " + eq_courante
    #                         tot_affec = tot_affec + 1
    #                         worksheet2.write_string(row, colo, pop_string_eq.strip())
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
    # worksheet2.write_string(row + 2, colo, "Modele : " + str(self.config_modele[0][10]) + " h-pers = " + str(self.config_modele[0][1]), cell_format_red)
    # row = row + 3
    # la_longue_string_modele = ""
    # la_longue_string_modele = la_longue_string_modele + " Calcul pr. équipes: " + str(calc_nb_quarts_requis) + "\n"
    # la_longue_string_modele = la_longue_string_modele + " Calcul prés individuelles: " + str(self.config_modele[0][3]) + "\n"
    # la_longue_string_modele = la_longue_string_modele + " Créneaux par jour: " + str(nb_cren) + "\n"
    # la_longue_string_modele = la_longue_string_modele + " Equipes par créneau: " + str(eq_par_cren) + "\n"
    # la_longue_string_modele = la_longue_string_modele + " Nombre d'équipes: " + str(nb_eq) + "\n"
    # la_longue_string_modele = la_longue_string_modele + " Empl. par éq.: " + str(self.config_modele[0][5]) + "\n"
    # la_longue_string_modele = la_longue_string_modele + " Durée quart.: " + str(self.config_modele[0][2]) + "\n"
    # worksheet2.write_string(row, colo, la_longue_string_modele, cell_format_noir)
    # worksheet2.set_column(row, colo, 23)
    # row = row + 2
    # date_prod = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    # worksheet2.write_string(row, colo+1, "Émis le " + date_prod, cell_format_red)
    #workbook.close()

ecriture_excel2() #juste pourverifier quelques lignes sinon ça plante pour le moment