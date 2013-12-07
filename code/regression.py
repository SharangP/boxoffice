from db.db import Database
import numpy as np
import math
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
import pylab as pl

D = Database('boxoffice.db')

###############################################################################
# Generate features from db, split into training and testing sets
F = np.array(D.GetAllFeatures())

F = np.array([x for x in F if all(x[5:] != -1)])      # remove examples with missing people
np.random.shuffle(F)    #shuffle examples
Mid = F[:,0]
S = F[:,1]
F = F[:,5:]

train_ind = int(F.shape[0]*4/5)
F_train = F[:train_ind,:]
S_train = S[:train_ind]
F_test = F[train_ind:,]
S_test = S[train_ind:]

###############################################################################
# Fit regression model

svr_rbf = SVR(kernel='rbf', C=0.001, gamma=0.1, degree=5)
model = svr_rbf.fit(F_train, S_train)
S_test_guess = model.predict(F_test)

###############################################################################
# Compute metrics
print F.shape
print np.mean(np.absolute(S_test-S_test_guess))
print np.median(np.absolute(S_test-S_test_guess))
# print np.sqrt(mean_squared_error(S_test, S_test_guess))
