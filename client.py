import socket
import threading
import random
import json

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def receive():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            print(message.decode())
        except:
            pass
t = threading.Thread(target=receive)
t.start()

#client.sendto(f"/join {name}".encode(), ("localhost", 9999))

while True:
    message = input("")
    if message.startswith("/"):
        if message.startswith("/join"):
            ipPort = message[message.index(" ")+1:]
            split = ipPort.split()
            ip = split[0]
            port = split[1]
            print(ip)
            client.bind((ip, int(port)))
            x = {"command":"join"}
            y = json.dumps(x)
            client.sendto(y.encode(), (ip, int(port)))
            #print("Connection to the Message Board Server is successful!")
            
        elif message.startswith("/leave"):
            print("Connection closed. Thank you!")
        elif message.startswith("/register"): 
            print("Welcome {name}!")
        elif message.startswith("/all"):
            print("alling")
        elif message.startswith("/msg"):
            print("msging")
        elif message.startswith("/?"):
            print("???????ing")
        else:
            print("Error: Command not found.")
    else:
        print('edi wow')
        #client.sendto(f"{name}: {message}".encode(), ("localhost", 9999))
