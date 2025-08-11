import pandas as pd
from tabulate import tabulate

# загрузка данных
data=[]
file_path = 'data/old/players_data-2024_2025_28_04.csv'
df = pd.read_csv(file_path)

file_path = 'data/2324/denormalized/Goalkeeping_adv.csv'
df1 = pd.read_csv(file_path)

#file_path = 'data/ex2022-2023_top5.xlsx'
#df2 = pd.read_excel(file_path)

#фильтр
poisk = df[(df['Min'] > 900) & (df['PSxG+/-']>=0) & (df['Stp%']>=7)]

mas=[]
head=['Name','PSxG', 'PSxG +','Cr.Stp%','%усп.длин.передач']
z=0
# Проверка, найдены ли записи
if not poisk.empty:
    for index, row in poisk.iterrows():
        player_name = row['Player']
        psxg=row['PSxG']
        age=row['Age']
        pm=row['PSxG+/-']
        #team=row['Squad']
        cross=row['Stp%']
        vper=row['Cmp%_stats_keeper_adv']
        mas.append([player_name,psxg,pm,cross,vper])
        z=z+1
        
else:
    print("Игрок не найден.")

fam=[]
for i in range(len(mas)):
    fam.append(mas[i][0])

#фильтр другие ключи
poisk1 = df1[(df1['minutes_90s'] > 9) & (df1['psxg_net']>=0) & (df1['crosses_stopped_pct']>=7)]
mas1=[]

if not poisk1.empty:
    for index, row in poisk1.iterrows():
        player_name = row['player']
        psxg=row['psxg']
        pm=row['psxg_net']
        #team=row['Squad']
        cross=row['crosses_stopped_pct']
        vper=row['launched_pct']
        mas1.append([player_name,psxg,pm,cross,vper])
else:
    print("Игрок не найден.")
"""
poisk2 = df1[(df1['minutes_90s'] > 4) & (df1['psxg_net']>=0) & (df1['crosses_stopped_pct']>=6)]
mas2=[]

if not poisk2.empty:
    for index, row in poisk2.iterrows():
        player_name = row['player']
        psxg=row['psxg']
        pm=row['psxg_net']
        #team=row['Squad']
        cross=row['crosses_stopped_pct']
        vper=row['launched_pct']
        mas1.append([player_name,psxg,pm,cross,vper])
else:
    print("Игрок не найден.")
"""

final=[]
### кусок фикса данных
sez22=[['22/23 1 match','-','-','-','-'],
['Yahia Fofana 22/23',16.4 ,-1.6,11.9, 26.4],
['22/23 1 match','-','-','-','-'],
['Mathew Ryan 22/23',17.9,-0.1,9.9,37.3],
['Brice Samba 22/23',32.4,5.4,8.9,40.0],
['Robin Zentner 22/23',35.4,-3.6,13.4,40.0]
]


fix=0
for i in mas:
    for f in mas1:
        if i[0] == f[0]:
            if fix<len(sez22):
                final.append(i)
                final.append(f)
                final.append(sez22[fix])
                final.append([' ',' ',' ',' ',' ']) #"пустая" строка между игроками
            fix=fix+1

for i in range(1,len(final),4):
    if final[i][0]=='Yahia Fofana' or final[i][0]=='Joan García':
        final[i][0]=final[i][0]+' 23/24 (2div)'
    else:
        final[i][0]=final[i][0]+' 23/24'

final[0][0]=final[0][0]+' (OGC Nice)'
final[16]=['Brice Samba (2club)',38.8,3.8,9,41.8]
final.pop()
### конец фикса

print ('\n')
print(tabulate(final, tablefmt='pipe', stralign='center',headers=head))
print ('\n')