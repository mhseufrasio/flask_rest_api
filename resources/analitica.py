import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing

#leitura e normalização dos dados
tabela = pd.read_csv("data.csv", sep=",")
N = len(tabela)

scaler = preprocessing.MinMaxScaler(feature_range=(0,1))

X = np.array(tabela["x"])
X = np.array(X).reshape((-1,1))
X = scaler.fit_transform(X)
ones = np.ones(N,dtype=float)
ones = np.array(ones).reshape((-1,1))
X = np.concatenate((ones,X),axis=1)

Y = np.array(tabela["y"])
Y = np.array(Y).reshape((-1,1))
Y = scaler.fit_transform(Y)

Xt = X.T
X = np.dot(X,Xt)
w = np.dot(np.linalg.pinv(X),Y)
espaco = np.linspace(0,1)
plt.plot(np.dot(X,w))
plt.plot(Y)
plt.show()
print(w.shape)
print(w)