import pandas as pd
import numpy as np
from matplotlib import pyplot as plt 

chutes = pd.read_excel('chutes.xlsx')
besoins = pd.read_excel('Besoin.xlsx')
procede_besoin = pd.read_excel('procédé-besoin.xlsx')
procedes = pd.read_excel('procédés.xlsx')
rendu_procede = pd.read_excel('rendu-procédé.xlsx')
rendu = pd.read_excel('rendu.xlsx')
num = pd.read_excel('num.xlsx')

d={}
for i in range (len(procedes['Nom'])):
    d[i]=procede_besoin[procede_besoin['id procédé'] == i]['id besoin'].tolist()
print(d)

q={}
for i in range (len(procedes['Nom'])):
    q[i]=[]
    g={}
    for j in d[i]:
        g[j]=[]
        if not (besoins.loc[j,'Colonne de la table chute'] == 'composition'):
            borne_inf = float(besoins.loc[j,'Borne_inf'])
            borne_sup = float(besoins.loc[j,'Borne_sup'])
            print(borne_inf, borne_sup)
            a = chutes[(chutes[besoins.loc[j,'Colonne de la table chute']] > borne_inf ) & ( chutes[besoins.loc[j,'Colonne de la table chute']] < borne_sup)]['numéro'].tolist()
            g[j] += a
        else:
            a = chutes[ chutes[besoins.loc[j,'Colonne de la table chute']] == besoins.loc[j,'Valeur']]['numéro'].tolist()
            g[j] += a
    éléments_communs = g[d[i][0]]
    for j in d[i]:
        éléments_communs = set(éléments_communs) & set(g[j])
    q[i] += list( éléments_communs )
print(q)

id_procédé = []
numéro_chute = []
for i in q.keys():
    id_procédé += [i]*len(q[i])
    numéro_chute += q[i]


assemblage = pd.DataFrame({'id_procédé': id_procédé, 'numéro_chute': numéro_chute})
print(assemblage)