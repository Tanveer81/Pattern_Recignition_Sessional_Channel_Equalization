# -*- coding: utf-8 -*-
"""
Created on Thu Jul 12 23:25:14 2018

@author: User
"""

import numpy
import random
import math
import time

global n,l,w,sigmaError,train,test
w = []
train = []
test = []

def readfile():
    global n,l,w,sigmaError,train,test
    
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
    
    file = open("train.txt","r")
    string = file.readline()
    for i in range(0, len(string)):
        train.append(int(string[i]))
    file.close()
    
    file = open("test.txt","r")
    string = file.readline()
    for i in range(0, len(string)):
        test.append(int(string[i]))
    file.close()
    
    
    
    

def main():
    global n,l,w,sigmaError,train,test
    readfile()
#    print(n , l , sigmaError)
#    print(w)
#    print(train)
#    print(test)
    
    start = time.clock()


    end = time.clock()
    print('Time :',end - start)


if __name__ == "__main__":
    main()