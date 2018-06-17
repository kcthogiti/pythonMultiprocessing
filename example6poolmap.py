# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 19:58:10 2018

@author: KRISHNACHAITANYA
"""


from time import time
from multiprocessing import Pool, cpu_count

def returnSum(n):
    x = 0
    for i in range(n):
        if isPrimenumber(i):
            x += i
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
    
    
    start = time() 
    numOfWorkers = cpu_count()
    Num = 10000
        
    with Pool(processes = numOfWorkers) as pool:
        results = pool.map(returnSum, [Num*x for x in range(1,numOfWorkers+1)])

    end = time()
    print("Total Time:", end-start)
    print(results)