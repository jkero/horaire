modele = {'hpers': 140, 'hparjour':	8.0,'presences': 17.5, 'nbeq': 3, 'nb_par_eq': 6, 'calc_nbquart-eq': 2.9,'nb_eq_par_cren': 3,'nb_cren_disp':	1,'jours': 0.97, 'mod':'repartition concentre'}
sem = [['Lundi', '2022-03-28'], ['Mardi', '2022-03-29'], ['Mercredi', '2022-03-30'], ['Jeudi', '2022-03-31'], ['Vendredi', '2022-04-01'], ['Samedi', '2022-04-02'], ['dimanche', '2022-04-03']]
equipes_test = {'A': [['8-16'], ['rafon']], 'B': [['8-16'], ['grichon']], 'C': [['8-16'], ['krakoin']]}
row = 1
col = 0
inc = 3
r1 = ''
r2 = ''
r3 = ''
nb_cren = 3#modele['nb_cren_disp']
nb_jour_sem = len(sem)
nb_eq = len(equipes_test)
eq_par_cren = 1#modele['nb_eq_par_cren']
nb_q_eq = int(modele['calc_nbquart-eq']+ .5)
# ligne1
eqs = list(equipes_test)
eqs2 = eqs[:]
print("\ncreneaux disponibles par jour:" + str(nb_cren))
print("max equipes par creneau:" + str(eq_par_cren))
print("calc. equipes assign. total:" + str(nb_q_eq)+ "\n")
tot_affec = 0
for jour in range(0, nb_jour_sem):
    print(sem[jour][0])
    for cren in range(1, nb_cren+ 1):#cren_dispo
        print("\tcren " + str(cren))
        for eq in range(0, eq_par_cren):##eq par creneau #// TODO ne pas resetter equipes
            if tot_affec < nb_q_eq:
                if len(eqs) > 0:
                    print("\t\teq# " + str(eq) + " " + eqs.pop(0))  # //todo gestion des equipes deja assignees ?
                    tot_affec = tot_affec + 1
                else:
                    eqs = eqs2[:]
                    print("\t\teq# " + str(eq) + " " + eqs.pop(0))  # //todo gestion des equipes deja assignees ?
                    tot_affec = tot_affec + 1
            else:
                break



