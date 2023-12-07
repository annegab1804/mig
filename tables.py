import pandas as pd
import numpy as np
from matplotlib import pyplot as plt 

#on convertit tous les fichiers excels en dataframe
chutes = pd.read_excel('chutes.xlsx', index_col='numéro')
besoins = pd.read_excel('Besoin.xlsx')
procede_besoin = pd.read_excel('procédé-besoin.xlsx')
procedes = pd.read_excel('procédés.xlsx')
rendu_procede = pd.read_excel('rendu-procédé.xlsx')
rendu = pd.read_excel('rendu.xlsx')
num = pd.read_excel('num.xlsx')


#on récupère le numéro des besoins que chaque procédé à besoin
d={}
for i in range (len(procedes['Nom'])):
    d[i]=procede_besoin[procede_besoin['id procédé'] == i]['id besoin'].tolist()


#à chaque procédé on associe des chutes compatibles
q={}
for i in range (len(procedes['Nom'])):
    q[i]=[]
    g={}
    for j in d[i]:
        g[j]=[]
        if not (besoins.loc[j,'Colonne de la table chute'] == 'composition'):
            borne_inf = float(besoins.loc[j,'Borne_inf'])
            borne_sup = float(besoins.loc[j,'Borne_sup'])
            a = chutes[(chutes[besoins.loc[j,'Colonne de la table chute']] > borne_inf ) & ( chutes[besoins.loc[j,'Colonne de la table chute']] < borne_sup)].index.tolist()
            g[j] += a
        else:
            a = chutes[ chutes[besoins.loc[j,'Colonne de la table chute']] == besoins.loc[j,'Valeur']].index.tolist()
            g[j] += a
    éléments_communs = g[d[i][0]]
    for j in d[i]:
        éléments_communs = set(éléments_communs) & set(g[j])
    q[i] += list( éléments_communs )

id_procédé = []
numéro_chute = []
for i in q.keys():
    id_procédé += [i]*len(q[i])
    numéro_chute += q[i]

#on crée la table assemblage qui relie un procédé et une chute
assemblage = pd.DataFrame({'id_procédé': id_procédé, 'numéro_chute': numéro_chute})

#on ajoute à la table assemblage leur rendu
temps = []
for i in range(len(assemblage)):
    temps += [procedes.loc[assemblage.loc[i, "id_procédé"], "Temps"]]
assemblage['Temps'] = temps


prix = []
for i in range(len(assemblage)):
    prix += [procedes.loc[assemblage.loc[i, "id_procédé"], "Prix"]]
assemblage['Prix'] = prix

modifie_la_chute = []
for i in range(len(assemblage)):
    modifie_la_chute += [procedes.loc[assemblage.loc[i, "id_procédé"], "Modifie la chute"]]
assemblage['Modifie la chute'] = modifie_la_chute

mosaïque_possible = []
for i in range(len(assemblage)):
    mosaïque_possible += [procedes.loc[assemblage.loc[i, "id_procédé"], "Mosaïque possible"]]
assemblage["Mosaïque possoble"] = mosaïque_possible

déparayé = []
for i in range(len(assemblage)):
    déparayé += [procedes.loc[assemblage.loc[i, "id_procédé"], "Déparayé"]]
assemblage['Déparayé'] = déparayé

tout_type_de_forme = []
for i in range(len(assemblage)):
    tout_type_de_forme += [procedes.loc[assemblage.loc[i, "id_procédé"], "Tout type de forme"]]
assemblage['Tout type de forme'] = tout_type_de_forme

rigide = []
for i in range(len(assemblage)):
    rigide += [procedes.loc[assemblage.loc[i, "id_procédé"], "Rigide"]]
assemblage['Rigide'] = rigide

épais = []
for i in range(len(assemblage)):
    épais+= [procedes.loc[assemblage.loc[i, "id_procédé"], "Épais"]]
assemblage['Épais'] = épais

#on doit remplir les cases de la colonne épais dont le rendu dépend de la chute et non du procédé

for i in range(len(assemblage)):
    if assemblage.loc[i, 'Épais'] == '?' :
        if chutes.loc[assemblage.loc[i,'numéro_chute'], 'épaisseur (mm)' ] > 0.9:
            assemblage.loc[i, 'Épais'] = 'oui'
        else:
            assemblage.loc[i, 'Épais'] = 'non'

print(assemblage)  

assemblage.to_excel('assemblage.xlsx')
