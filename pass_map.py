import pandas as pd
from mplsoccer import VerticalPitch, Pitch
from scipy.stats import gaussian_kde
import matplotlib.pyplot as plt
from tabulate import tabulate
import numpy as np

def is_prog(y,y2):
    if y2-y>=14:
        return True
    return False
def is_deep(x, y):
    """
    Проверяет, находится ли точка (x,y) внутри фигуры с жестко заданными параметрами.
    Фигура определена точками (21,83), (79,83), (50,78) и квадратичной кривой между ними.
    
    Параметры:
    x, y - координаты проверяемой точки
    
    Возвращает:
    True, если точка внутри фигуры, False в противном случае
    """
    # Жестко заданные точки (как в исходном коде)
    points = np.array([[21, 83], [79, 83], [50, 78]])
    points = points[np.argsort(points[:, 0])]  # Сортировка по X
    
    # Коэффициенты квадратичной кривой (ax² + bx + c)
    coeffs = np.polyfit(points[:, 0], points[:, 1], 2)
    
    # 1. Проверка границ
    if x < 21 or x > 79 or y > 100:
        return False
    
    # 2. Проверка вертикальных областей
    if x <= 21:
        return y >= 83  # Левая вертикальная область
    elif x >= 79:
        return y >= 83  # Правая вертикальная область
    
    # 3. Проверка под кривой (дугой)
    y_curve = coeffs[0]*x**2 + coeffs[1]*x + coeffs[2]
    return y >= y_curve
def has_cross(qualifiers):
    for qualifier in qualifiers:
        if qualifier['type']['displayName'] == 'Cross':
            return True
    return False
def has_corner(qualifiers):
    for qualifier in qualifiers:
        if qualifier['type']['displayName'] == 'CornerTaken':
            return True
    return False

players =['Bryan Mbeumo']
teamvs='epl'

df = pd.read_json('E:/prog/scrape/whs/all_epl_matches.json')
df = df[(df['type'] == 'Pass')&(df['team']=='Brentford')&(df['y']<50)]

for names in players:
    myplayer=names
    poisk=df[(df['player']==myplayer)]
    poisk  = poisk[~poisk['qualifiers'].apply(has_corner)]
    mas=[]
    zz='qualifiers'
    toch=0
    allpass=0
    if not poisk.empty:
        for index, row in poisk.iterrows():
            player_name = row['player']
            x=row['x']
            y=row['y']
            x2=row['end_x']
            y2=row['end_y']
            sus=row['outcome_type']
            deep=is_deep(y2,x2)
            if is_deep(y2,x2):
                if sus=='Successful':
                    toch+=1
                allpass+=1
                mas.append([player_name,x,y,x2,y2,sus,deep])         
    else:
        print("Игрок не найден.")

    #стрелки
    pitch = VerticalPitch(pad_bottom=0.5, 
                          half=True, 
                          goal_type='box',
                          goal_alpha=0.8,
                          pitch_type='opta',
                          pitch_length=100,  
        pitch_width=100)    
    fig, ax = pitch.draw(figsize=(10, 8))
    ax.set_xlim(100, 0)
    ax.set_ylim(0, 100)
    start=[]
    end=[]
    for i in range(len(mas)):
        start.append((mas[i][2],mas[i][1]))
        end.append((mas[i][4],mas[i][3]))
    #print (tabulate(mas, tablefmt='pipe', stralign='center',headers='keys'))
    for i in range(len(start)):
        start_point=start[i]
        end_point=end[i]
        if mas[i][5]=='Successful':
            cl='#1E90FF'
            ga=1
        else:
            cl='#DC143C'
            ga=0 #без неудачных передач

        dx = end_point[0] - start_point[0]
        dy = end_point[1] - start_point[1]
        plt.arrow(
        x=start_point[0], y=start_point[1],  # Начало
        dx=dx, dy=dy,
        width=0.1,       # Толщина основания
        head_width=0.5,  # Ширина "головы" стрелки
        head_length=0.5, # Длина "головы"
        fc=cl,      # Цвет заполнения
        ec=cl,
        alpha=ga,
        )
    plt.savefig(
        'strelki.png',          # имя файла (позиционный аргумент)
        dpi=300,           # именованный аргумент
        bbox_inches="tight" # именованный аргумент
    )
    plt.show()

    # тепловая карта 
    pitch = VerticalPitch(pad_bottom=0.5, 
                          half=True, 
                          goal_type='box',
                          goal_alpha=0.8,
                          pitch_type='opta',
                          pitch_length=100,  
        pitch_width=100)    
    fig, ax = pitch.draw(figsize=(10, 8))
    ax.set_xlim(100, 0)
    ax.set_ylim(0, 100)   
    x = np.array([point[0] for point in end])
    y = np.array([point[1] for point in end])

    # KDE (ядровая оценка плотности). Куда были направлены передачи
    kde = gaussian_kde(np.vstack([x, y]))
    x_grid, y_grid = np.mgrid[0:100:100j, 0:100:100j]
    z = kde(np.vstack([x_grid.flatten(), y_grid.flatten()]))
    z = z.reshape(x_grid.shape)
    heatmap = ax.contourf(
        x_grid, y_grid, z,
        levels=1000,
        cmap='inferno',  # гуд варианты 'viridis', 'magma', 'coolwarm', 'hot', 'inferno'
        alpha=0.8,
        zorder=0,
        bw_method=0.8
    )
    plt.savefig(
        'hm.png',          # имя файла (позиционный аргумент)
        dpi=300,           # именованный аргумент
        bbox_inches="tight" # именованный аргумент
    )
    plt.show()

print ('- - - Finish! - - - ')