modele = {'hpers': 140, 'hparjour':	8.0,'presences': 17.5, 'nbeq': 3, 'nb_par_eq': 6, 'calc_nbquart-eq': 2.9,'nb_eq_par_cren': 3,'nb_cen-disp':	1,'jours': 0.97, 'mod':'repartition concentre'}
sem = [['Lundi', '2022-03-28'], ['Mardi', '2022-03-29'], ['Mercredi', '2022-03-30'], ['Jeudi', '2022-03-31'], ['Vendredi', '2022-04-01'], ['Samedi', '2022-04-02'], ['dimanche', '2022-04-03']]
equipes_test = {'A': [['8-16'], ['rafon']], 'B': [['8-16'], ['grichon']], 'C': [['8-16'], ['krakoin']]}
row = 1
col = 0
inc = 3
r1 = ''
r2 = ''
r3 = ''
# ligne1
for i in range(0, len(sem)): #excl.
    r1 = r1 + '\t\t|'+ sem[i][0] +'|\t' #fusionner cols 1-2-3 row1
    col = col + inc
print(r1 + "--- r:" + str(row) + " c:" + str(col))
row = row + 1
col = 1
#ligne 2
for i in range(0, len(sem)): #excl.
    r2 = r2 + '\t|' + sem[i][1] + '|\t'  # fusionner 3 cellules row1 et 2
    col = col + inc
print(r2 + "--- r:" + str(row) + " c:" + str(col))
# ligne 3
row = row + 1
col = 1
for i in range(0, len(sem)): #excl.
    for i in range(1,4):
        r3 = r3 + '   q'+ str(i) + ' |'
    col = col + inc
print(r3 + "--- r:" + str(row) + " c:" + str(col))
row = row + 1
col = 0
# r4 col 0 : eq#
r4 = ''
for numeq in range(1, modele['nb_eq_par_cren']):
    r4 = r4 +  'eq' + str(numeq) + "\n" #equipes_test[numeq][0]
    row = row + 1
print(r4 + "--- r:" + str(row) + " c:" + str(col))
row = row - modele['nb_eq_par_cren']
col = 1
r5 = ''
templisteq = [3]
row = row + 1
for nomeq in equipes_test:
    if modele['nb_cen-disp']== 1:
        col = col + 1
        templisteq[0] = col + 1
    elif modele['nb_cen-disp'] == 2:
        templisteq[0] = col+2
        templisteq[1] = col+1
    elif modele['nb_cen-disp'] == 3:
        templisteq[0] = col + 2
        templisteq[1] = col + 1
        templisteq[2] = col + 3

    for i in range(0,len(templisteq)):
        r5 = r5 + nomeq + str(templisteq[i]) + '|'

print(r5 + "--- r:" + str(row) + " c:" + str(col))
