# Вариант 9. Теплякова Юлия 6403
import pandas as pd
import numpy as np

# Загрузка данных
data = pd.read_csv('config.csv')
info = list()

# Инициализация значений
n0 = data['n0'][0]
h = data['h'][0]
nk = data['nk'][0]
a = data['a'][0]
b = data['b'][0]
c = data['c'][0]

# Вычисление уравнения 𝑦(𝑥) = sin^2(𝑎𝑥 + 𝑏) + cos^2(𝑐𝑥) 
for x in range(n0, nk):
    print(np.sin(a*x + b)**2 + np.cos(c*x)**2)
