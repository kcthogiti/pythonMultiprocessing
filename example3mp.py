# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 20:23:22 2018

@author: KRISHNACHAITANYA
"""


from time import time
from multiprocessing import Process, Queue, cpu_count

def returnSum(n, r):
    x = 0
    for i in range(n):
        if isPrimenumber(i):
            x += i
    r.put(x)
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
     
    #https://stackoverflow.com/questions/1540822/dumping-a-multiprocessing-queue-into-a-list
    def dump_queue(q):
        ls = []
        for i in iter(q.get, 'Stop'):
            ls.append(i)
        return ls
    
    jobs = []
    result = Queue()
    
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
    
    result.put("Stop")
    l = dump_queue(result)
    end = time()
    
    print("Total Time:", end-start)
    print(l)