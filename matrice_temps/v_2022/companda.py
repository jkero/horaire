import pandas as pd
import numpy as np

kragouin = pd.DataFrame()

data_1 = {'product_1': ['computer','monitor','printer','desk'],
                   'price_1': [1200,800,200,350]
                   }
df1 = pd.DataFrame(data_1)
print(df1)

data_2 = {'product_2': ['computer','monitor','printer','desk'],
                    'price_2': [900,800,300,350]
                    }
df2 = pd.DataFrame(data_2)
print (df2)

#kragouin['prices_match'] = np.where(df1['price_1'] == df2['price_2'], 'True', 'False')

print(kragouin)

#Autre test

dispo = {'lundi': ['tache_1','tache_2','tache3','tache4'],
                   'debut': [6,8.5,12.5,15], 'fin':[15,16,19,23]}

dispo_table = pd.DataFrame(dispo)

print(dispo_table)

empl = {'nom': ['Jack','Diane','Gill','Joan'],
                   'debut': [6,10,12,16], 'fin':[16,18,20,23]}

empl_table = pd.DataFrame(empl)

print(empl_table)
a  = dispo_table['debut'] >= empl_table['debut']
b = dispo_table['fin'] <= empl_table['fin']
#kragouin['can_start'] = np.where(dispo_table['debut'] >= empl_table['debut'] & dispo_table['fin'] <= empl_table['fin'])

kragouin['can_start'] = np.where(a, dispo_table['lundi'] +"."+ empl_table['nom'] ,"")
kragouin['can_finish'] = np.where(b, dispo_table['lundi'] +"."+ empl_table['nom'] ,"")
print(kragouin)