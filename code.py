import time
import itertools
import random
import numpy as np
import math
import scipy as sc

random.seed(5)

global n,l,w,sigmaError,train,test,prior,trainLength,testLength,miu,lst,X
w = []
train = []
test = []



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
    print(prior)
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

       
        
        
def miuCal():
    global n,l,w,sigmaError,train,test,trainLength,testLength,prior,xsition,lst,miu
    #    generate all bit string of classes
    lst = list(itertools.product([0, 1], repeat=n))
    
#   calculate miu
    miu = [0] * (2 ** n)
    for i in range(0, 2**n):
        miu[i] = sum(x * y for x, y in zip(lst[i] , w))
 
def calculateX():
    global n,X,trainLength,train
    for i in range(0, trainLength):
        binary = []
        for j in range(0,n):
            binary.append(train[i+j])
        classNumber = b2d(binary)
        
    

def sigmaCal():
    print()
    
def nomal(x,mu,sigma):
    pdf = (1 / (2 * math.pi * (sigma ** 2)) ** .5) * math.exp(-((x - mu) ** 2/(2 * (sigma ** 2)))
    return pdf
    

def training():   
    print("Training")
    priorCal()
    xsitionCal()
    miuCal()
    calculateX()
    
def testing():
    print("Testing")           

def main():
    readfile()
    start = time.clock()
    training()
    print(miu)
    end = time.clock()
    print('Time :',end - start)


if __name__ == "__main__":
    main()