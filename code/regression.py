from db.db import Database
import numpy as np
import math
from sklearn.svm import SVR
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_squared_error, r2_score
import matplotlib.pyplot as plt
 
# def metrics(name, truth, guess, plotParams):
def metrics(ax1, ax2, name, truth, guess, plotParams):
    # print str(name) + " results:"
    Mean = np.mean(np.absolute(truth-guess))
    Median = np.median(np.absolute(truth-guess))
    R2 = r2_score(truth, guess)

    print Mean
    print Median
    print R2

    sortedError = sorted(zip(truth, truth-guess), key=lambda pair: pair[0])
    std = np.std(truth-guess)

    X = [x[0] for x in sortedError]
    Y = [x[1] for x in sortedError]

    ax1.plot(X, Y, plotParams)
    ax1.plot([0,100],[0,0], 'k')
    ax1.plot([0,100],[std,std], 'k')
    ax1.plot([0,100],[-std,-std], 'k')

    ax1.axis([0,100,-100,100])

    # ax2.hist(guess)
    
    return Mean, Median, R2

D = Database('boxoffice.db')

###############################################################################
# Generate features from db, split into training and testing sets
F1 = np.array(D.GetAllFeatures())

F1 = np.array([x for x in F1 if all(x[5:] != -1)])      # remove examples with missing people

algorithms = [
    SVR(kernel='rbf', C=1, gamma=.002, degree=3),
    AdaBoostRegressor(DecisionTreeRegressor(max_depth=15), n_estimators=200),
    GradientBoostingRegressor(loss='huber', n_estimators=200),
    RandomForestRegressor(n_estimators=200)
    ]

niter = 5
means = np.zeros([len(algorithms),niter])
medians = np.zeros([len(algorithms),niter])
r2s = np.zeros([len(algorithms),niter])

for n in xrange(niter):
    print "Begin iteration " + str(n) + "\n"
    np.random.shuffle(F1)    #shuffle examples

    Mid = F1[:,0]
    S = F1[:,1]

    MeanCast = np.mean(F1[:,[7,9,11,13]],1)
    StdCast = np.mean(F1[:,[8,10,12,14]],1)
    MeanCast = MeanCast.reshape(len(MeanCast),1)
    StdCast = StdCast.reshape(len(StdCast),1)

    F = np.append(F1[:,[5, 6, 15, 16]], MeanCast, 1)
    F = np.append(F, StdCast, 1)
    # F=F1[:,5:]

    train_ind = int(F.shape[0]*9/10)
    F_train = F[:train_ind,:]
    S_train = S[:train_ind]
    F_test = F[train_ind:,]
    S_test = S[train_ind:]

    ###############################################################################
    # PCA

    # pca = PCA()
    # F_train = pca.fit_transform(F_train)
    # F_test = pca.transform(F_test)

    ###############################################################################
    # Fit regression models

    guess = []

    for a in algorithms:
        model = a.fit(F_train, S_train)
        guess.append(a.predict(F_test))

    ###############################################################################
    # Compute metrics

    plt.hold(True)
    p1 = plt.figure()
    p2 = plt.figure()
    p3 = plt.figure()
    p4 = plt.figure()
    p5 = plt.figure()

    ax1 = p1.add_subplot(111)
    ax2 = p2.add_subplot(111)
    ax3 = p3.add_subplot(111)
    ax4 = p4.add_subplot(111)

    ax51 = p5.add_subplot(221)
    ax52 = p5.add_subplot(222)
    ax53 = p5.add_subplot(223)
    ax54 = p5.add_subplot(224)

    means[0,n], medians[0,n], r2s[0,n] = metrics(ax1, ax51, "SVR", S_test, guess[0], 'ro')
    means[1,n], medians[1,n], r2s[1,n] = metrics(ax2, ax52, "Boosted Decision Tree", S_test, guess[1], 'bo')
    means[2,n], medians[2,n], r2s[2,n] = metrics(ax3, ax53, "Gradient Boosting Regression", S_test, guess[2], 'go')
    means[3,n], medians[3,n], r2s[3,n] = metrics(ax4, ax54, "Random Forest Regression", S_test, guess[3], 'ko')

    # means[0,n], medians[0,n], r2s[0,n] = metrics("SVR", S_test, guess[0], 'ro')
    # means[1,n], medians[1,n], r2s[1,n] = metrics("Boosted Decision Tree", S_test, guess[1], 'bo')
    # means[2,n], medians[2,n], r2s[2,n] = metrics("Gradient Boosting Regression", S_test, guess[2], 'go')
    # means[3,n], medians[3,n], r2s[3,n] = metrics("Random Forest Regression", S_test, guess[3], 'ko')

    # ax51.hist(S_test)
    # ax42.hist(boostedTreeGuess)
    # ax43.hist(S_test-boostedTreeGuess)

print np.mean(means,1)
print np.mean(medians,1)
print np.mean(r2s,1)

plt.show()
