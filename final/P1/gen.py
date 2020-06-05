#!/usr/bin/env python3
# encoding: utf-8

import random
for i in range(100000):
    print(random.randrange(10),end="")
    if i%10 == 0:
        print("")

