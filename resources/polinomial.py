import math
import numpy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing


def polinomial_treino(X_treino, Y_treino, Y_treino_normalizado, P, lbd=0):
    X_novo = X_treino
    custo = []
    W = []

    for polinomio in range(P):
        ones = np.ones(X_treino.shape[0], dtype=float)
        ones = np.array(ones).reshape((-1, 1))
        X = np.concatenate((ones, X_treino), axis=1)

        w = np.dot(np.linalg.pinv(X), Y_treino_normalizado)
        #salvar w0 da regularização
        if lbd > 0:
            w_0 = w[0]
            w = np.dot(X.T, X)
            I = np.eye(w.shape[0], w.shape[1])
            w += lbd * I
            w = np.linalg.inv(w)
            waux = np.dot(X.T, Y_treino_normalizado)
            w = np.dot(w, waux)
            w[0] = w_0

        W.append(w)
        #desnormaliza Y
        Y_previsto = np.dot(X, w)
        desnormaliza_Y = escalar_y.inverse_transform(Y_previsto)

        funcao_custo = 0.5 * (Y_treino - desnormaliza_Y).T
        funcao_custo = np.dot(funcao_custo, (Y_treino - desnormaliza_Y))
        #regularização
        if lbd > 0:
            W_mod = np.dot(w.T, w)
            funcao_custo += (lbd / 2) * W_mod

        rmse = math.sqrt(funcao_custo)
        custo.append(rmse)
        #adicionar novos x ao polinomio
        X_aux = []
        for valores in X_novo:
            X_aux.append(valores ** (polinomio + 2))
        X_treino = np.concatenate((X_treino, X_aux), axis=1)

    plt.plot(np.array(custo).reshape(-1, 1))
    plt.show()
    return W,P,lbd

def polinomial_teste(X_teste_normalizado,Y_teste,W,P,lbd=0):
    X_novo = X_teste_normalizado
    custo_teste = []
    for polinomio in range(P):
        ones = np.ones(X_teste_normalizado.shape[0], dtype=float)
        ones = np.array(ones).reshape((-1, 1))
        X = np.concatenate((ones, X_teste_normalizado), axis=1)

        Y_previsto = np.dot(X, W[polinomio])
        desnormaliza_Y = escalar_y.inverse_transform(Y_previsto)

        funcao_custo = 0.5 * (Y_teste - desnormaliza_Y).T
        funcao_custo = np.dot(funcao_custo, (Y_teste - desnormaliza_Y))

        if lbd > 0:
            W_mod = np.dot(W[polinomio].T, W[polinomio])
            funcao_custo += (lbd / 2) * W_mod

        rmse = math.sqrt(funcao_custo)
        custo_teste.append(rmse)

        X_aux = []
        for valores in X_novo:
            X_aux.append(valores ** (polinomio + 2))
        X_teste_normalizado = np.concatenate((X_teste_normalizado, X_aux), axis=1)

    plt.plot(np.array(custo_teste).reshape(-1, 1))
    plt.show()

#leitura dos dados
tabela = pd.read_csv("boston.csv", sep=",")

#iniciação da variaveis
ROWS = len(tabela)
COLS = tabela.shape[1]
P = 11
porcentagem = 0.8
#definindo numero de amostras de treino
treino = (int)(porcentagem*ROWS)
teste = ROWS-treino

#dividindo tabela entre treino e teste
divisao = numpy.vsplit(tabela, np.array([treino]))
tabela_teste = divisao[1]
tabela_treino = divisao[0]

#dividindo tabela treino em X e Y
divisao_tabela_treino = numpy.hsplit(tabela_treino,np.array([COLS-1]))
X_treino = divisao_tabela_treino[0]
Y_treino = divisao_tabela_treino[1]

#dividindo tabela teste em X e Y
divisao_tabela_teste = numpy.hsplit(tabela_teste,np.array([COLS-1]))
X_teste = divisao_tabela_teste[0]
Y_teste = divisao_tabela_teste[1]

#normalizando os X
escalar_x = preprocessing.MinMaxScaler(feature_range=(0,1))
escalar_x.fit(X_treino)
X_treino_normalizado = escalar_x.transform(X_treino)
X_teste_normalizado = escalar_x.transform(X_teste)

#normalizando os Y
escalar_y = preprocessing.MinMaxScaler(feature_range=(0,1))
escalar_y.fit(Y_treino)
Y_treino_normalizado = escalar_y.transform(Y_treino)
Y_teste_normalizado = escalar_y.transform(Y_teste)

#calculando sem regularização
W,P,lbd = polinomial_treino(X_treino_normalizado,Y_treino,Y_treino_normalizado,P)
polinomial_teste(X_teste_normalizado,Y_teste,W,P,lbd)

#calculando com regularização
W1,P1,lbd1 = polinomial_treino(X_treino_normalizado,Y_treino,Y_treino_normalizado,P,0.01)
polinomial_teste(X_teste_normalizado,Y_teste,W1,P1,lbd1)