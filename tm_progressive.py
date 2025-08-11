import pandas as pd
from tabulate import tabulate

def is_prog(y,y2):
    if y2<33: #исключаем передачи принятые в первой трети поля
        return False
    if y2-y>=9.5: # > +-10 метров
        return True
    return False

def is_tgpass(x, y, center_x=50, center_y=50):
    if center_x<33:
        return False
    if (49.4 <= center_x <= 50.6) and (49.4 <= center_y <= 50.6):
        return False
    # Параметры фигуры
    big_width = 23.4 * 2
    big_height = 14.3 * 2
    small_width = 7.81 * 2
    small_height = 4.76 * 2
    # Проверка попадания в прямоугольную область между полукругами
    if (abs(x - center_x) <= 23.4 and 
        abs(x - center_x) >= 7.81 and 
        abs(y - center_y) <= 0.5):  # небольшой допуск для линии
        return True
    # Проверка нижнего полукруга (красный)
    if y <= center_y:
        # Уравнение эллипса: ((x-cx)/(a))² + ((y-cy)/(b))² ≤ 1
        a = big_width / 2
        b = big_height / 2
        if ((x - center_x) / a)**2 + ((y - center_y) / b)**2 <= 1:
            return True
    # Проверка верхнего полукруга (синий)
    if y >= center_y:
        a = small_width / 2
        b = small_height / 2
        if ((x - center_x) / a)**2 + ((y - center_y) / b)**2 <= 1:
            return True
    
    return False

csv = pd.read_csv('data/forwards_bundesliga.csv', encoding='utf-8')

players = csv['Name'].tolist()
teams = csv['Team'].tolist()
minutes_p = csv['Min'].tolist()

df = pd.read_json('opt/bundesliga2425.json')
final=[]

for zxc in range(len(players)):
    myplayer=players[zxc]
    myteam=teams[zxc]
    print (myplayer,' ')
    poisk = df[(df['team'] == myteam) & (df['type'].isin(['Pass', 'Aerial', 'BallTouch']))]
    mas,pl,pl_tgpass=[],[],[]
    zz='qualifiers'
    toch,ind,allpass=0,0,0

    if not poisk.empty:
        # Вывод списка игроков и количества сыгранных минут
        for index, row in poisk.iterrows():
            typ=row['type']
            player_name = row['player']
            x=row['x']
            y=row['y']
            x2=row['end_x']
            y2=row['end_y']
            sus=row['outcome_type']
            keyp=row[zz]
            vremya=str(row['minute'])+':'+str(row['second'])
            if sus=='Successful':
                toch+=1
            allpass+=1
            mas.append([ind,player_name,x,y,x2,y2,typ,vremya,sus,row['game_id']]) #все пасы
            if (player_name==myplayer):
                if (typ=='Pass') & (sus=='Successful') & (is_tgpass(y2,x2,y,x)==True):
                    pl.append([ind,player_name,x,y,x2,y2,typ,vremya,sus,row['game_id']]) #только Тм пасс
            ind+=1 #Для лучшей навигации свой Ind вместо Index по всему файлу 
    else:
        print("Игрок не найден.")

    vsego_tg_prog=0
    tg_prog,prog_pass_after=[],[]
    for r in pl:
        time_str = r[7]
        minutes, seconds = map(float, time_str.split(':'))
        t=(minutes*60)+seconds
        index=r[0]
        for i in range(1, 11):#охватываем 10 событий после ТМ пасс
            try:
                time_team = mas[index+i][7]
                minutes, seconds = map(float, time_team.split(':'))
                t_team = (minutes * 60) + seconds
                if t_team - t > 5:# охватываем только 5 секунд
                    break
                    
                if mas[index+i][6] == 'Pass':
                    if mas[index+i][8] == 'Successful':
                        if is_prog(mas[index+i][2], mas[index+i][4]): #проверка продвигающая ли передача
                            vsego_tg_prog += 1
                            break
                            
            except (IndexError, ValueError, AttributeError) as e:
                print(f"Произошла ошибка: {e}. Прерывание цикла.") # исключаем случаи, когда нет 10 событий после передачи
                break
            except Exception as e:
                print(f"Неизвестная ошибка: {e}. Прерывание цикла.")
                break



    print ('tg_prog: ',vsego_tg_prog,'\n')

    final.append([myplayer,vsego_tg_prog,minutes_p[zxc], ((vsego_tg_prog * 90) / minutes_p[zxc])])

#######################################
# Сбор данных завершен.

print ('\n')
print (tabulate(final, tablefmt='pipe', stralign='center',headers=['Name','TmProg','Min','per 90 TmProg']))
print ('\n')
#сохранение в excel виде
df = pd.DataFrame(final, columns=['Name','TmProg','Min','per 90 TmProg']) 
df.to_excel("tmprog_bund.xlsx", index=False)
print ('- F -\n')
