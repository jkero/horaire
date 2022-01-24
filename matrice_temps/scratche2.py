modele = {'hpers': 140, 'hparjour':	8.0,'presences': 17.5, 'nbeq': 3, 'nb_par_eq': 6, 'calc_nbquart-eq': 2.9,'nb_eq_par_cren': 3,'nb_cren_disp':	1,'jours': 0.97, 'mod':'repartition concentre'}
sem = [['Lundi', '2022-03-28'], ['Mardi', '2022-03-29'], ['Mercredi', '2022-03-30'], ['Jeudi', '2022-03-31'], ['Vendredi', '2022-04-01'], ['Samedi', '2022-04-02'], ['dimanche', '2022-04-03']]
equipes_test = {'A': [['8-16'], ['rafon']], 'B': [['8-16'], ['grichon']], 'C': [['8-16'], ['krakoin']]}
row = 1
col = 0
inc = 3
r1 = ''
r2 = ''
r3 = ''
nb_cren = 2#modele['nb_cren_disp']
nb_jour_sem = len(sem)
nb_eq = len(equipes_test)
ep_par_cren = modele['nb_eq_par_cren']
# ligne1
eqs = list(equipes_test)
for k in range(0, nb_jour_sem):
    if k < nb_eq:
    #    print( 'cren ' + str(cren))
        for cren in range(0, nb_cren):
    #        print('sem ' + str(key))
            if cren < nb_cren:
                for j in range(0, nb_eq):
        #            print('eq' + str(j))
                    if j < ep_par_cren:
                       print('cren ' + str(cren) + " j sem " + str(sem[k]) + ' eq ' + str(eqs[j]))
                    else:
                        break
            else:
                break
    else:
        break