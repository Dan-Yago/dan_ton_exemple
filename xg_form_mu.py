import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from scipy.interpolate import make_interp_spline
from numpy.polynomial import Polynomial
import statsmodels.api as sm

#два варианта сглаживания. экспоненциальное и lowless
def sgl_exp(mas,y):

    alpha = 0.3  # Коэффициент сглаживания (от 0 до 1)
    smoothed_data = np.zeros_like(mas)
    smoothed_data[0] = mas[0]
    for i in range(1, len(mas)):
        smoothed_data[i] = alpha * mas[i] + (1 - alpha) * smoothed_data[i - 1]
    return smoothed_data
def sgl_low(mas,y):
    lowess = sm.nonparametric.lowess(mas, y, frac=0.25) #frac коэфицент. можно "играться"
    data = lowess[:, 1]
    return data

data = pd.read_json('data/xg_epl.json')

for team in data['teams']:
    xg_list = [match['xG'] for match in team['matches']]
    xga_list = [match['xGA'] for match in team['matches']]
    team=team['name']

    fig = plt.figure(figsize=(10,6))
    ax = plt.axes()

    xg=np.array(xg_list)
    xga=np.array(xga_list)

    y=[]
    for i in range(5,len(xga)+1):
        y.append(i)

    xg1,xga1=[],[]
    xgsum,gsum=0,0
    for i in range(4,len(xg)):
        xga1.append((xga[i]+xga[i-1]+xga[i-2]+xga[i-3]+xga[i-4])/5)
    for i in range(4,len(xg)):
        xg1.append((xg[i]+xg[i-1]+xg[i-2]+xg[i-3]+xg[i-4])/5)

    xg_s=sgl_low(xg1,y)
    g_s=sgl_low(xga1,y)

    fig.text(
        0.515, 0.93, team+' в АПЛ', size=21,
        ha="center", color="black"
    )
    fig.text(
        0.515, 0.89, 'форма за 5 матчей', size=10,
        ha="center", color='black'
    )
    CREDIT_1 = "Данные: FBref (Opta)"
    CREDIT_2 = "НеВеликий Dan`Тон"
    CREDIT_4 = "t.me/ne_dan_ton"
    fig.text(
        0.999, 0.01, f"{CREDIT_4}", size=9,
        ##fontproperties=font_italic.prop, color="#F2F2F2",
        color="black",
        ha="right",
        linespacing=1.7
    )

    fig.text(
        0.01, 0.03, f"{CREDIT_1}", size=10,
        ##fontproperties=font_italic.prop, color="#F2F2F2",
        color="black",
        ha="left"
    )

    fig.text(
        0.01, 0.005, f"Сглаживание LOWESS со степенью 0.25", size=6,
        ##fontproperties=font_italic.prop, color="#F2F2F2",
        color="black",
        ha="left"
    )






    for spine in ax.spines.values():
        spine.set_color('black')  # цвет границ
    plt.plot(y,xg_s, label='xG',color='#f19026')           
    plt.plot(y,g_s, label='xGA',color='#0b7deb')
    plt.xlim(left=5,right=38) 
    plt.xlabel("Матчи", color='black')
    plt.ylabel("Голы", color='black')
    
    plt.grid(True,alpha=0.2, color='black')
    ax.tick_params(axis='x', color='black')  # метки по X
    ax.tick_params(axis='y', color='black')  #метки по Y
    plt.axvline(x=9,ls="--",c='black',alpha=0.7)
    plt.axvline(x=11,ls="--",c='black',alpha=0.7)
    plt.axvline(x=7,ls="dotted",c='green',alpha=0.35)
    plt.axvline(x=10,ls="dotted",c='green',alpha=0.3)
    plt.axvline(x=29,ls="dotted",c='green',alpha=0.35)
    plt.axvline(x=34,ls="dotted",c='blue',alpha=0.2)
    plt.axvline(x=24,ls="dotted",c='y',alpha=0.3)
    plt.legend()

    fig.text(
        0.15, 0.2, f"ten Hag", size=10,
        color="black",
        ha="left"
    )

    fig.text(
        0.23, 0.2, f"RvN", size=10,
        color="black",
        ha="left"
    )

    fig.text(
        0.28, 0.2, f"Ruben Amorim", size=10,
        color="black",
        ha="left"
    )

    fm=os.path.basename(__file__)
    plt.savefig(team+'_'+fm+'.png', dpi=300, bbox_inches = "tight")
    plt.show()

    if team=='Manchester United':
        break

print ('F')

