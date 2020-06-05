#!/usr/local/bin/python3
# encoding: utf-8

import socket
import argparse
import select
MAXLINE = 1024
user_num = 0
inputs = []
outputs = []
user_list = [-1]
user_group = [[]]

parser = argparse.ArgumentParser()
parser.add_argument('port', type=int)
args = parser.parse_args()
Host = '127.0.0.1'
Port = args.port

def sndmsg(sockfd, msg):
    msg = msg+'\n% '
    sockfd.send(msg.encode())

def list_users(sockfd):
    msg = ''
    for i in range(1, user_num+1):
        if user_list[i] != None:
            if msg != '':
                msg = msg+'\n'
            msg = msg+'user'+str(i)
    sndmsg(sockfd, msg)

def group_add(sockfd, data):
    user = user_list.index(sockfd)
    num = int(data.split('user')[1])
    if num > user_num or user_list[num] == None:
        sndmsg(sockfd, data+' does not exist.')
    else:
        user_group[user].append(user_list[num])
        sndmsg(sockfd, 'Add '+data+' successfully.')

def group_rem(sockfd, data):
    user = user_list.index(sockfd)
    num = int(data.split('user')[1])
    if num > user_num:
        sndmsg(sockfd, data+' does not exist.')
        return
    rem_user = user_list[num]
    try:
        user_group[user].remove(rem_user)
        sndmsg(sockfd, 'Remove '+data+' sucessfully.')
    except:
        sndmsg(sockfd, data+' does not exist.')

def group_snd(sockfd, data):
    user = user_list.index(sockfd)
    for fd in user_group[user]:
        sndmsg(fd, ' '.join(data))
    sockfd.send('% '.encode())

def exi(sockfd):
    for i in range (user_num+1):
        if user_list[i] == sockfd:
            print('user%d %s:%d disconnectd' % (i, sockfd.getpeername()[0], sockfd.getpeername()[1]))
            user_list[i] = None
            user_group[i] = []
            break
        try:
            user_group[i].remove(sockfd)
        except:
            continue
    inputs.remove(sockfd)
    sockfd.close()

def fun(sockfd, msg):
    data = msg.split()
    if data == []:
        sockfd.send('% '.encode())
        return
    gofun = data[0]
    del data[0]
    if gofun == 'list-users':
        list_users(sockfd)
    elif gofun == 'group-add':
        group_add(sockfd, data[0])
    elif gofun == 'group-remove':
        group_rem(sockfd, data[0])
    elif gofun == 'group-send':
        group_snd(sockfd, data)
    elif gofun == 'exit':
        exi(sockfd)
    else:
        sndmsg(sockfd, 'fuck!')

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverfd:
    serverfd.setblocking(0)
    serverfd.bind((Host, Port))
    serverfd.listen()
    inputs.append(serverfd)

    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        for sockfd in readable:
            if sockfd is serverfd:
                connfd, cliaddr = sockfd.accept()
                connfd.setblocking(0)

                # Keep field for new client
                inputs.append(connfd)
                user_list.append(connfd)
                user_group.append([])
                user_num += 1

                # Print some notifying message
                print('New connection from %s:%s user%d' % (cliaddr[0], cliaddr[1], user_num))
                connfd.send('% '.encode())
            else:
                msg = sockfd.recv(MAXLINE).decode().strip()
                fun(sockfd, msg)
