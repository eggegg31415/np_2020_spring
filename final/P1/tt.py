#!/usr/bin/env python
# encoding: utf-8

import multiprocessing as mp
import time

def oddf(odd_num):
    time.sleep(20)
    print("odd", odd_num)

def evenf(even_num):
    time.sleep(20)
    print("even", even_num)

if __name__ == '__main__':
    ap = mp.Process(target=oddf, args=(1,))
    jk = mp.Process(target=evenf, args=(2,))

    ap.start()
    jk.start()

    ap.join()
    jk.join()
