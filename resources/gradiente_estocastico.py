import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing

#leitura e normalização dos dados
tabela = pd.read_csv("data.csv", sep=",")
tabela = preprocessing.normalize(tabela, axis=0)
for ponto in tabela:
    plt.plot(ponto[0],ponto[1],'o')

#iniciação da variaveis
N = len(tabela)
T = 100
w0 = [1]
w1 = [1]
erro_quadratico = []
alfa = 0.5
t=1
erro_sum = []
errox = 0.0
funcao_custo = []
custo = 0.0

#plot da reta inicial
espaco = np.linspace(-1,1)
linha = w1[t-1]*espaco + w0[t-1]
plt.plot(espaco,linha)

#calculando regressão
while t <= T:
    random.shuffle(tabela)
    for valor in tabela:
        y = valor[1]
        x = valor[0]
        y_previsto = w0[t-1] + w1[t-1]*x
        erro_quadratico.append(y - y_previsto)
        custo += erro_quadratico[t-1]**2
        w0t = w0[t-1] + alfa*(erro_quadratico[t-1])
        w1t = w1[t-1] + alfa*(erro_quadratico[t-1])*x
        w0.append(w0t)
        w1.append(w1t)
    funcao_custo.append(custo)
    custo = 0.0
    t += 1

#plot reta alterada
linha_prevista = w1[t-1]*espaco + w0[t-1]
plt.plot(espaco,linha_prevista)
"plt.savefig(f'imagens/{(t-1):004}',dpi=72, facecolor='white')"

plt.show()
plt.plot(funcao_custo)
plt.show()
print(f"w0 = {w0[t-1]} e w1 = {w1[t-1]}")