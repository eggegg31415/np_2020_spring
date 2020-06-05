#!/usr/local/bin/python3
# encoding: utf-8

import argparse
import socket
import os
import json
import multiprocessing as mp

def fun(Port):
    Host = '127.0.0.1'
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as serverfd:
        serverfd.bind((Host, Port))
        File_name, addr = serverfd.recvfrom(2048)
        rcvfile = open('rcv_'+File_name.decode(), "w")

        busy = 1
        while busy:
            pkt, addr = serverfd.recvfrom(2048)
            msg = json.loads(pkt.decode())
            if msg['fin'] == 0:
                rcvfile.write(msg['payload'])
            else:
                busy = 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("num", type=int)
    parser.add_argument("port", type=int)
    args = parser.parse_args()
    Num = args.num
    Port = args.port

    child_proc = []
    for i in range(0, Num):
        child_proc.append(mp.Process(target=fun, args=(Port+i,)))
        child_proc[i].start()

    for i in range(0, Num):
        child_proc[i].join()
