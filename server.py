# Student ID:220084
# Student Name:Roshani Shrestha
# Module: ST5062CEM Programming and Algorithms 2
# Hamro Secure Chatting System

import socket
import threading

HOST = '127.0.0.1'
PORT = 3030

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

users = []
chatname = []

def logfile(msg):
    try:
        with open("log.txt", "a+") as fw:
            fw.write(msg)
    except:
        print("Error occured while handeling the file.")


def broad(msg):
    for usr in users:
        usr.send(msg)


def usr_connection(usr):
    while True:
        try:
            msg = usr.recv(1024)
            sender_name = f"{chatname[users.index(usr)].decode()} says {msg.decode()}"
            print(f"{chatname[users.index(usr)]} says {msg}")
            broad(msg)
            writer = threading.Thread(target=logfile, args=(sender_name,))
            writer.start()
        except:
            index = users.index(usr)
            users.remove(usr)
            usr.close()
            usrname = chatname[index]
            chatname.remove(usrname)
            break


def main():
    while True:
        try:
            usr, address = server.accept()
            print(f"Connected with {str(address)}!")

            usr.send("CHAT".encode('utf-8'))
            usrname = usr.recv(1024)

            chatname.append(usrname)
            users.append(usr)

            print(f"Chatname of the usr is {usrname}")
            broad(f"{usrname} connected to the server!\n".encode('utf-8'))
            usr.send("Connected to the server".encode('utf-8'))

            thread = threading.Thread(target=usr_connection, args=(usr,))
            thread.start()
        except:
            print("Error had occured!")
            break


with open("info.txt", "r") as f:
    mainn = f.readlines()
    for detail in mainn:
        print(detail, end="")
print("\n\nServer running...")
main()
