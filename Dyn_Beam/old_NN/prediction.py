
from sklearn import linear_model

from sklearn.metrics import r2_score

import numpy as np

data = np.loadtxt('Simulation4_acel.txt')

n_sim = 1
timesteps = np.size(data, 0)
#window = int(timesteps / 9) # 9 refers to 9 measurements of M for each simulation i.e. after 70 timesteps
#nbr_tests = int(np.size(data, 0) / window)

#X = np.zeros((nbr_tests, window)) 
#j=0
#y = np.zeros((nbr_tests , 1))

#for i in range(0, np.size(data, 0), window): #check 70 since depends on lenght of simulation
#    X[j, :] = data[i:i+window, 0]
#    y[j] = data[i+window - 1 , 1] 
#    j = j + 1


#data = data.reshape((timesteps, 2, n_sim))

xtrain = data[0:int(.9 * n_sim * timesteps), 0]
xtrain = xtrain[:, np.newaxis]

#xtrain = X[0:int(nbr_tests / 2), :]

ytrain = data[0:int(.9 * n_sim * timesteps), 1]
ytrain = ytrain[:, np.newaxis]

#train = y[0:int(nbr_tests / 2)]

reg = linear_model.LinearRegression()

reg.fit(xtrain, ytrain)

xpredict = data[int(.9 * n_sim * timesteps + 1):n_sim * timesteps, 0]
xpredict = xpredict[:, np.newaxis]

#ypredict = X[int(nbr_tests / 2):nbr_tests, :]

ypredict = reg.predict(xpredict)

ytest = data[int(.9 * n_sim * timesteps + 1):n_sim * timesteps, 1]
ytest = ytest[:, np.newaxis]

#test = y[int(nbr_tests / 2):nbr_tests]

r2 = r2_score(ytest, ypredict)
