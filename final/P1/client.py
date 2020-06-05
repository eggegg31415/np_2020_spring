#!/usr/local/bin/python3
# encoding: utf-8

import argparse
import socket
import os
import sys
import json

def sndmsg(sockfd, msg):
    sockfd.sendto(msg.encode(), (Host, Port))

parser = argparse.ArgumentParser()
parser.add_argument("ip", type=str)
parser.add_argument("port", type=int)
parser.add_argument("file_name", type=str)
args = parser.parse_args()
Host = args.ip
Port = args.port
File_name = args.file_name

sndfile = open(File_name, "r")
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as clientfd:
    sndmsg(clientfd, File_name)
    for line in sndfile:
        data = {'fin': 0, 'payload': line}
        pkt = json.dumps(data)
        sndmsg(clientfd, pkt)
    data = {'fin': 1, 'payload': ""}
    pkt = json.dumps(data)
    sndmsg(clientfd, pkt)
