# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 20:02:57 2018

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
    
    futures = []
    results = []
    start = time()
    numOfWorkers = cpu_count()
    Num = 10000
    with Pool(processes = numOfWorkers) as pool:
        for i in range(numOfWorkers):
            futures.append(pool.apply_async(returnSum, args = (Num,)))
            Num+= 10000
        for f in futures:
            results.append(f.get())

    end = time()
    print("Total Time:", end-start)
    print(results)