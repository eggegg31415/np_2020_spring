#!/usr/local/bin/python3.6
# encoding: utf-8
import argparse
import socket
import select
import sqlite3
MAXLINE = 1024
inputs = []
outputs = []
name = {}

def sndmsg(sockfd, msg):
    msg = msg + "\n% "
    sockfd.send(msg.encode())

def register(sockfd, data):
    if not len(data) is 3:
        sndmsg(sockfd, "Usage: register <username> <email> <password>")
        return
    username = data[0]
    email = data[1]
    password = data[2]

    #check if user name is unique
    cur.execute("SELECT Username FROM USERS")
    users = cur.fetchall()
    for user in users:
        if user[0] == username:
            sndmsg(sockfd, "Username is already used.")
            return
    cur.execute("INSERT INTO USERS (Username, Email, Password) \
            values (?, ?, ?)", (username, email, password))
    sqlfd.commit()
    sndmsg(sockfd, "Register successfully.")

def login(sockfd, data):
    if not len(data) is 2:
        sndmsg(sockfd, "Usage: login <username> <password>")
        return
    username = data[0]
    passwd = data[1]

    if sockfd in name:
        sndmsg(sockfd, "Please logout first.")
        return

    cur.execute("SELECT Username,Password FROM USERS")
    users = cur.fetchall()
    for user in users:
        if user[0] == username:
            if user[1] != passwd:
                sndmsg(sockfd, "Login failed.")
                return
            else:
                name[sockfd] = username
                sndmsg(sockfd, "Welcome, " + username)
                return
    sndmsg(sockfd, "Login failed.")


def whoami(sockfd):
    if sockfd in name:
        sndmsg(sockfd, name[sockfd])
    else:
        sndmsg(sockfd, "Please login first.")

def logout(sockfd):
    if sockfd in name:
        sndmsg(sockfd, "Bye, " + name[sockfd])
        del name[sockfd]
    else:
        sndmsg(sockfd, "Please login first.")

def exi(sockfd):
    if sockfd in outputs:
        outputs.remove(sockfd)
    inputs.remove(sockfd)
    sockfd.close()

def print_motd(sockfd):
    motd = "\
********************************\n\
** Welcome to the BBS server. **\n\
********************************"
    sndmsg(sockfd, motd)


def fun(sockfd, msg):
    data = msg.split()
    gofun = data[0]
    del data[0]
    if gofun == 'register':
        register(sockfd, data)
    elif gofun == 'login':
        login(sockfd, data)
    elif gofun == 'whoami':
        whoami(sockfd)
    elif gofun == 'logout':
        logout(sockfd)
    elif gofun ==  'exit':
        exi(sockfd)
    else:
        sndmsg(sockfd, "fuck!")

# get port information
parser = argparse.ArgumentParser()
parser.add_argument("port", type=int)
args = parser.parse_args()
Host = '127.0.0.1'
Port = args.port

# build a user database
sqlfd = sqlite3.connect('user.db')
print("open db sucess")
cur = sqlfd.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS USERS(
    UID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL UNIQUE,
    Email TEXT NOT NULL,
    Password TEXT NOT NULL
    );''')
print("create db success")
sqlfd.commit()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as serverfd:
    serverfd.setblocking(0)
    serverfd.bind((Host, Port))
    serverfd.listen()
    inputs.append(serverfd)

    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        for sockfd in readable:
            if sockfd is serverfd:  # new client enters
                connfd, cliaddr = sockfd.accept()
                connfd.setblocking(0)
                inputs.append(connfd)
                print_motd(connfd)
                print("New connection.")
            else:
                msg = sockfd.recv(MAXLINE).decode().strip()
                fun(sockfd, msg)

