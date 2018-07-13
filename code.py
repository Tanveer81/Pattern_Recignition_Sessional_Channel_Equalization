import numpy
import random
import math
import time

global n,l,w,sigmaError,train,test,prior,trainLength,testLength
w = []
train = []
test = []



def readfile():
    global n,l,w,sigmaError,train,test,trainLength,testLength,xsition
    
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
    sigmaError = words[0]
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
    
    
def init():
    global n,l,w,sigmaError,train,test,trainLength,testLength,prior,xsition
    
    #calculating prior
    prior = [0] * (2 ** n)
    for i in range(0, trainLength):
        binary = []
        for j in range(0,n):
            binary.append(train[i+j])
        classNumber = b2d(binary)
        prior[classNumber] = prior[classNumber] + 1
    print(prior)
    prior = [float(i)/sum(prior) for i in prior]
    

def b2d(b):
    #convert a list of integers b of 1 and 0 to decimal number d
    str1 = ''.join(str(e) for e in b)
    d = int(str1, 2)
    return d
    

def main():
    global n,l,w,sigmaError,train,test
    readfile()
#    print(n , l , sigmaError)
#    print(w)
    print(len(train))
    print(train)
#    print(test)
    init()
    print(prior)
    
    start = time.clock()


    end = time.clock()
    print('Time :',end - start)


if __name__ == "__main__":
    main()