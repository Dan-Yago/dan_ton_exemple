import pandas as pd
import matplotlib.pyplot as plt
import os
from tabulate import tabulate
from collections import Counter

fig = plt.figure(figsize=(10,8))
ax = plt.axes()

file_path = 'data/final_ucl/table_1.csv'  # Путь к вашему файлу
df = pd.read_csv(file_path)
file_path = 'data/final_ucl/table_8.csv'  # Путь к вашему файлу
df2 = pd.read_csv(file_path)

mas=[]
if not df.empty:
    for index, row in df.iterrows():
        player_name = row['Player']  # Замените на название колонки с именем игрока
        if player_name=='Fabián Ruiz Peña':
            player_name = 'A Fabián Ruiz'
        pas=row['PrgP']
        car=row['PrgC']
        mas.append([player_name,pas,car])
        
else:
    print("Игрок не найден.")
kol_vs=mas[len(mas)-1][0]
kol_vs=kol_vs[0]+kol_vs[1]
kol_vs=int(kol_vs)
mas.pop()

if not df2.empty:
    for index, row in df2.iterrows():
        player_name = row['Player'] 
        if player_name=='Fabián Ruiz Peña':
            player_name = 'Fabián Ruiz'
        pas=row['PrgP']
        car=row['PrgC']
        mas.append([player_name,pas,car])
        
else:
    print("Игрок не найден.")
mas.pop()

print ('\n')
print(tabulate(mas, tablefmt='pipe', stralign='center'))
print ('\n')

point_counts = Counter((m[2], m[1]) for m in mas)
if (0, 0) in point_counts:
    del point_counts[(0, 0)]  # исключаем игроков с показателями 0 0
vsp=kol_vs
fam=[]
for i in range(len(mas)):
    fam.append(mas[i][0])

new_fam = []
for name in fam: 
    if name=='Rodrigo Gomes': #исправление фамилии вручную
        new_fam.append('R. Gomes') 
    elif name=='Toti Gomes':
        new_fam.append('T. Gomes')
    else:
        words = name.split()  # разбиваем строку на слова
        if len(words) > 1:  #если слов больше 1
            new_name = ' '.join(words[1:])  # del перво слово
            new_fam.append(new_name)
        else:
            new_fam.append(name)  
max_с = max(m[2] for m in mas)

def odinakovie_tochki(mas,z): #проверка одинаковых точек и
    pod=0
    for i in range(z):
        if mas[i][1] == mas[z][1] and mas[i][2] == mas[z][2]:
            pod=pod+1
    return pod

def tochka_2cveta(mas,z): #совпадающие точки делаем двухцветными
    for i in range(z):
        if mas[i][1] == mas[z][1] and mas[i][2] == mas[z][2]:
            if z<vsp and i>=vsp:
                return 1
            if i<vsp and z>=vsp:
                return 1
    return 2
for i in range(len(mas)):
    cal_x=0.05 #позиции фамилий относительно точек
    cal_y=0.15
    cal_s=30
    ha='left'
    od_t=0
    if mas[i][2]==max_с:
        ha='right'
        cal_x=-0.05
    if tochka_2cveta(mas,i)==1:
        cal_s=15
    point_to_check = (mas[i][2], mas[i][1])
    if point_counts[point_to_check]>1: #если совпадений больше 1
        if odinakovie_tochki(mas,i)==1: #если прошлая точка уже была
            cal_y=-0.25
        if odinakovie_tochki(mas,i)==2: #если уже было 2 точки
            ha='right'
            cal_x=-0.05
        if odinakovie_tochki(mas,i)==3:
            ha='right'
            cal_y=-0.25
            cal_x=-0.05
        if odinakovie_tochki(mas,i)>=4: # если игроков слишком много, то 5й ниже, под первым
            cal_y=-0.25*(point_counts[point_to_check]-2)

    if mas[i][1]>0 or mas[i][2]>0:
        if i>=vsp:
            fc='red'
        else:
            fc='blue'

    if mas[i][1]>0 or mas[i][2]>0:
        plt.text(mas[i][2]+cal_x, mas[i][1]+cal_y, new_fam[i],ha=ha,color=fc,bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.1'))
        plt.scatter(mas[i][2], mas[i][1], facecolor=fc,alpha=1,s=cal_s)

plt.ylabel("Progressive Passes",size=15)
plt.xlabel("Progressive Carries",size=15)
fig.text(
    0.515, 0.89, 'UEFA Champions League. Final', size=13,
    ha="center", color="black"
)
fig.text(
    0.515, 0.93, 'PSG vs. Inter. Progressive Actions', size=15,
    ha="center", color="black"
)
fig.text(
    0.255, 0.89, f"t.me/ne_dan_ton", size=10,
    ##fontproperties=font_italic.prop, color="#F2F2F2",
    color="black",
    ha="right",
    linespacing=1.7
)
fig.text(
    0.84, 0.89, f"Data: FBref (Opta)", size=9,
    ##fontproperties=font_italic.prop, color="#F2F2F2",
    color="black",
    ha="center"
)
fm=os.path.basename(__file__)
plt.savefig(fm+'.png', dpi=400, bbox_inches = "tight")
print ('F')
plt.show()

