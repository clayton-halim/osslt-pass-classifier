import numpy as np
from sklearn import metrics
from random import randint
from random import shuffle

FEATURES_FILE = "oversampled_output_normalized.csv"
FEATURE_COUNT = 7
train_seed = randint(0, 1000000)

class LogisticRegression(object):
    def __init__(self, threshold=0.50, alpha=0.1, lambd=0, iterations=1000):
        self.threshold = threshold        
        self.alpha = alpha
        self.lambd = lambd
        self.iterations = iterations

    def setTheta(self, t):
        self.theta = t

    def sigmoid(self, X):
        """Compute the sigmoid function"""
        den = 1.0 + np.exp(-X)
        d = 1.0 / den
        return d

    def train(self, X, y): 
        """ Trains the classifier given example data
        
        Keyword arguments:
        X -- the training set
        y -- the target set
            
        """
        
        self.dataSize = X.shape[0]
        self.featuresAmt = X.shape[1]
        self.theta = np.zeros(self.featuresAmt)
     
        it = 1
        while it <= self.iterations:
            theta1 = self.theta # Accounts for bias term not being regularized in calculation
            theta1[0] = 0
            
            self.theta = self.theta - (self.alpha / self.dataSize) * np.sum((X.transpose() * \
            (self.sigmoid(np.sum(X * self.theta, axis=1)) - y)), axis=1) + \
            ((self.lambd/(self.dataSize)) * theta1) 
        
            it += 1

    def cost(self, X, y):
        """Calculates how 'wrong' the predictor with the current parameters on its training data"""
        theta1 = self.theta # Accounts for bias term not being regularized in calculation
        theta1[0] = 0
        
        cost = -(1.0/self.dataSize) * np.sum(((np.log10(self.sigmoid(np.sum(X * self.theta, axis=1))) * y)) + \
        ((np.log10(1 - self.sigmoid(np.sum(X * self.theta, axis=1))) * (1 - y)))) + \
        np.sum((self.lambd/(2*self.dataSize)) * np.power(theta1, 2)) 
        
        return cost

    def predict_proba(self, X):
        """Outputs probabilities of the estimates for each test data"""
        return self.sigmoid(np.sum(X * self.theta, axis=1))

    def predict(self, X):
        """Outputs the predicted class for each test data"""
        X = (self.predict_proba(X) >= self.threshold)
        
        return X.astype(int)
       

def f1_score(confuse):
    """Calculates the f1 score of a set of classifications from a confusion matrix"""
    precision = confuse[0][0] / float(confuse[0][0] + confuse[1][0])
    recall = confuse[0][0] / float(confuse[0][0] + confuse[0][1])
    
    return 2 * ((precision * recall) / (precision + recall))
    
def chunkify(lst, n):
    """Splits a list into n sub-lists"""
    return [lst[i::n] for i in range(n)]

def k_fold_cv(X, y, learner, k):
    """Calculates the preformance of the classifier by k-fold cross-validation
    
    Keyword Arguments:
    X -- train data
    y -- target data
    learner -- classfier
    k -- # of subsamples to test data on
    """
    
    X = X.tolist()
    y = y.tolist()
    
    total_data = list(zip(X, y))
     
    shuffle(total_data)
        
    unzip = list(zip(*total_data))
    
    X = chunkify(unzip[0], k)
    y = chunkify(unzip[1], k)
  
    mess_ups = 0.0
    index = 0
    for test_X, test_y in zip(X, y):
        train_X = []
        train_y = []
        for i in range(len(y)):
            if i != index:
                train_X += X[i]
                train_y += y[i]
           
        learner.train(np.array(train_X), np.array(train_y))
        y_pred = learner.predict(np.array(test_X))
        error = f1_score(metrics.confusion_matrix(test_y, y_pred))
        mess_ups += error
        index += 1
        
    mess_ups /= k
    
    return mess_ups    

def main():    
    lr = LogisticRegression()

    X = []
    y = []
    
    with open(FEATURES_FILE, "r") as data_file: 
        for line in data_file:
            line = line.strip().split(",")
            y.append(float(line[1]))
            x = []
            x.append(1) # Bias term
            for i in range(2, 2 + FEATURE_COUNT):
                x.append(float(line[i]))
            X.append(x)
            
    train_data = np.array(X)
    target_data = np.array(y)
    
    print("f-score (k-fold cross-validation):", k_fold_cv(train_data, target_data, lr, 10))
    
if __name__ == '__main__':
    main()



