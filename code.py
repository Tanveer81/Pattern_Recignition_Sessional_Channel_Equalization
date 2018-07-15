import time
import itertools
import random
import math
import numpy as np
random.seed(1)

global n,l,w,sigmaError,sigmaError2,train,test,prior,trainLength,testLength,miu,lst,X,var,xk,graph,result
w = []
train = []
test = []
sigmaError2 = .225

def readfile():
    global n,l,w,sigmaError,train,test,trainLength,testLength,xsition,lst,miu
    
    file = open("config.txt", "r")
    string = file.readline()
    words = string.split(' ')
    n = int(words[0])
    l = int(words[1])
    string = file.readline()
    words = string.split(' ')
    for i in range(0,n):
        w.append(float(words[i]))
    string = file.readline()
    words = string.split(' ')
    sigmaError = float(words[0])
#    sigmaError = np.random.normal(0, sigmaError, 1)[0]
    file.close()
    
    #padding train and test with n-1 0's at start
    for i in range (0, n-1):
        train.append(0)
        test.append(0)
    
    file = open("train.txt","r")
    string = file.readline()
    for i in range(0, len(string)):
        train.append(int(string[i]))
    trainLength = len(train) - n + 1
    file.close()
    
    
    file = open("test.txt","r")
    string = file.readline()
    for i in range(0, len(string)):
        test.append(int(string[i]))
    testLength = len(test) - n + 1
    file.close()
    
    
def b2d(b):
    #convert a list of integers b of 1 and 0 to decimal number d
    str1 = ''.join(str(e) for e in b)
    d = int(str1, 2)
    return d    
    

def normpdf(x, mean, sd):
    var = float(sd)**2
    pi = 3.1415926
    denom = (2*pi*var)**.5
    num = math.exp(-(float(x)-float(mean))**2/(2*var))
    return num/denom


def priorCal():   
    global n,l,w,sigmaError,train,test,trainLength,testLength,prior,xsition,lst,miu
    #calculating prior
    prior = [0] * (2 ** n)
    for i in range(0, trainLength):
        binary = []
        for j in range(0,n):
            binary.append(train[i+j])
        classNumber = b2d(binary)
        prior[classNumber] = prior[classNumber] + 1
#    print(prior)
    prior = [float(i)/sum(prior) for i in prior]#normalize
   
    
    
    
def xsitionCal():
    global n,l,w,sigmaError,train,test,trainLength,testLength,prior,xsition,lst,miu
    #calculatiing xsition
    xsition = []
    for i in range(0,2**n):
        a = [0] * (2 ** n)
        xsition.append(a)
    
    for i in range(0, trainLength - 1):
        binary1 = []
        binary2 = []
        for j in range(0,n):
            binary1.append(train[i+j])
            binary2.append(train[i+j+1])
        currentState = b2d(binary1)
        nextState = b2d(binary2)
        xsition[currentState][nextState] = xsition[currentState][nextState] + 1
        
    for j in range(0,2**n):
        if sum(xsition[j]) != 0: 
            xsition[j] = [float(i)/sum(xsition[j]) for i in xsition[j]]#normalize

       
        
def calculateX():
    global n,X,trainLength,train,lst,sigmaError2
    lst = list(itertools.product([0, 1], repeat=n))
    X=[]
    for i in range(0,2**n):
        a = []
        X.append(a)
    
    for i in range(0, trainLength):
        binary = []
        for j in range(0,n):
            binary.append(train[i+j])
        classNumber = b2d(binary)        
        X[classNumber].append(sum(x * y for x, y in zip(lst[classNumber] , w))+np.random.normal(0, sigmaError, 1)[0])
        
        
        
def miuCal():
    global n,X,miu

    miu = [0] * (2 ** n)
    for i in range(0, 2**n):
        if len(X[i]) !=0:
            miu[i] = sum(X[i]) / float(len(X[i]))

 

def sigmaCal():
    var = []
    for i in range(0, 2**n):
        var.append(np.var(X[i]))


def getX():
    global n,xk,test,testLength,lst,sigmaError
    xk = []
    
    for i in range(0, testLength):
        binary = []
        for j in range(0,n):
            binary.append(test[i+j])
        classNumber = b2d(binary)        
        xk.append(sum(x * y for x, y in zip(lst[classNumber] , w))+np.random.normal(0, sigmaError, 1)[0])
    


    
def createGraph():
    global graph,n,testLength,prior,miu,sigmaerror,xk
    graph = []    
    for i in range(0, testLength):
        a = []
        for j in range(0, 2**n):
            if i == 0:
                a.append([-1, prior[j]*normpdf(xk[i], miu[j], np.random.normal(0, sigmaError, 1)[0])])
            else:
                a.append([-1, normpdf(xk[i], miu[j], np.random.normal(0, sigmaError, 1)[0])])
        graph.append(a)
    
def parents(classNumber):
    return math.floor((classNumber/2)) + 2**( n-1) , math.floor((classNumber/2))   
    
def children(classNumber):
    return (classNumber * 2) % (2**n) , ((classNumber * 2) % (2**n)) + 1

def viterbi():
    global graph,n,testLength,prior,miu,sigmaerror,xk,xsition
    
    for i in range(1, testLength):
        for j in range(0, 2**n):
            p1,p2 = parents(j)
            if graph[i-1][p1][1]*xsition[p1][j] >  graph[i-1][p2][1]*xsition[p2][j]:
                graph[i][j][0] = p1
                graph[i][j][1] = graph[i][j][1] * graph[i-1][p1][1]*xsition[p1][j]
            else:
                graph[i][j][0] = p2
                graph[i][j][1] = graph[i][j][1] * graph[i-1][p2][1]*xsition[p2][j]
    
def backProp():
    global graph,n,testLength,prior,miu,sigmaerror,xk,xsition,result
    max = 0
    lastClass = 0
    for i in range(0,2** n):
        if graph[testLength - 1][i][1] > max:
            max = graph[testLength - 1][i][1]
            lastClass = i
    
    result = []
    result.append(lastClass%2)
    
    xx = lastClass
    
    for i in range(testLength - 1 , 0, -1):
        mp = graph[i][xx][0]
        result.append(mp % 2)
        xx = mp 
    result.reverse()
  
    print(result)
  
def training():   
    print("Training")
    priorCal()
    xsitionCal()
    calculateX()
    miuCal()
    sigmaCal()    
    
def testing():
    print("Testing")           
    getX()
    createGraph()
    viterbi()
    backProp()
    
def accuracy():
    global test,result,testLength
    a = np.array(test[2:])
    b = np.array(result)
    accurate = np.sum(a == b)
    print(accurate/testLength)    

    
def main():
    readfile()
    start = time.clock()
    training()
    testing()
    accuracy()
    end = time.clock()
    print('Time :',end - start)


if __name__ == "__main__":
    main()