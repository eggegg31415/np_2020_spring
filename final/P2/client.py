#!/usr/bin/python3
# encoding: utf-8

import socket
import argparse
import select
import sys
MAXLINE = 1024

inputs = []
parser = argparse.ArgumentParser()
parser.add_argument('host', type=str)
parser.add_argument('port', type=int)
args = parser.parse_args()
Host = args.host
Port = args.port

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clifd:
    clifd.connect((Host, Port))
    inputs.append(sys.stdin)
    inputs.append(clifd)

    while inputs:
        readable, writable, exceptional = select.select(inputs, [], [])
        for sockfd in readable:
            if sockfd is clifd:
                msg = sockfd.recv(MAXLINE).decode()
                if len(msg) == 0:
                    sockfd.close()
                    exit(0)
                print(msg, end='')
            else:
                msg = input()
                clifd.send(msg.encode())
