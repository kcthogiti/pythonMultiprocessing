# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 20:11:30 2018

@author: KRISHNACHAITANYA
"""


from time import time
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import cpu_count

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
    
    futures = []
    result = []

    start = time()
    numOfWorkers = cpu_count()
    Num = 10000
    with ProcessPoolExecutor(max_workers = numOfWorkers) as executor:
        for i in range(numOfWorkers):
            futures.append(executor.submit(returnSum, Num))
            Num+= 10000
    
    for f in futures:
        result.append(f.result())
    
    end = time()
    print("Total Time:", end-start)
    print(result)