# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 20:58:58 2018

@author: KRISHNACHAITANYA
"""


from time import time
from multiprocessing import Process, Manager, cpu_count

def returnSum(n, r):
    x = 0
    for i in range(n):
        if isPrimenumber(i):
            x += i
    r.append(x)
    return x

def isPrimenumber(n):   
    x = True
    if n == 1:
        x = False
    else:
        for i in range(2,n):
            if n%i == 0:
                x = False
    return x


if __name__ == "__main__":
    
    jobs = []
    result = Manager().list()
    
    start = time()
    numOfWorkers = cpu_count()
    Num = 10000
    for i in range(numOfWorkers):
        p = Process(target = returnSum, args = (Num,result,))
        Num+= 10000
        jobs.append(p)
        p.start()
        
    for j in jobs:
        j.join()

    end = time()
    
    print("Total Time:", end-start)
    print(result)