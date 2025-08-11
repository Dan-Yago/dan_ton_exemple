import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage import gaussian_filter
import pickle
from mplsoccer import VerticalPitch, Pitch

# Чтение
with open('data/all_pass_rb.pkl', 'rb') as f:
    mas = pickle.load(f)
x,y=[],[]
big_x,big_y=[],[]

def is_prog(y,y2): #по умолчанию передавать X
    if y2<30:
        return False
    if y2-y>=9.5:
        return True
    return False

for m in mas:
  if m[5]=='Benjamin Sesko':
    x.append(m[2])
    y.append(m[3])

# Создание поля
pitch = VerticalPitch(
    pitch_type='opta', 
    line_zorder=2,
    pitch_color='#22312b', 
    line_color='#efefef',
    corner_arcs=True, 
    half=False, 
)

fig, ax = plt.subplots(figsize=(10, 8))
pitch.draw(ax=ax)
# хитмап
bin_statistic = pitch.bin_statistic(x, y, statistic='count', bins=(50, 35))
bin_statistic['statistic'] = gaussian_filter(bin_statistic['statistic'], 1)
pitch.heatmap(bin_statistic, ax=ax, cmap='hot', edgecolors='#22312b')

plt.savefig('Sesko_pass_rec.png', dpi=300, bbox_inches='tight')
plt.show()

print('-- FINISH --')

