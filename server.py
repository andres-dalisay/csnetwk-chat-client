import socket
import threading
import queue
import random
import json

DISCONNECTION_ERROR = "Error: Disconnection failed. Please connect to the server first."
REGISTRATION_ERROR = "Error: Registration failed. Handle or alias already exists."
DIRECT_MESSAGE_ERROR = "Error: Handle or alias not found."
COMMAND_ERROR = "Error: Command not found."
PARAMETER_ERROR = "Error: Command parameters do not match or is not allowed."

messages = queue.Queue()
clients = []
users = dict()

serverIP = socket.gethostbyname(socket.gethostname())
serverPort = 9999

print("Server IP: ", serverIP)
print("Server Port: ", serverPort)

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((serverIP, serverPort))

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            messages.put((message, addr))
        except:
            pass

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()

            msg = json.loads(message.decode())
            
            if addr not in clients:
                clients.append(addr)
            
            client = clients[clients.index(addr)]

            try:
                if msg["command"] == "join":
                    print(message.decode())
                    commandDict = {"command":"success", "message":"Connection to the Message Board Server is successful!"}
                    commandJSON = json.dumps(commandDict)
                    server.sendto(commandJSON.encode(), client)
                
                elif msg["command"] == "leave":
                    print(message.decode())
                
                elif msg["command"] == "register":
                    name = msg["handle"]
                    if name in users.keys():
                        commandDict = {"command":"error", "message":REGISTRATION_ERROR}
                        print(commandDict)
                        commandJSON = json.dumps(commandDict)
                        server.sendto(commandJSON.encode(), client)
                    else:
                        print(message.decode())
                        users[name] = client[1]
                        commandDict = {"command":"success", "message":f"Welcome {name}!"}
                        commandJSON = json.dumps(commandDict)
                        server.sendto(commandJSON.encode(), client)
                
                elif msg["command"] == "all":
                    print(message.decode())
                    text = msg["message"]
                    key = {i for i in users if users[i] == client[1]}
                    commandDict = {"command":"success", "message":f"{key}: {text}"}
                    commandJSON = json.dumps(commandDict)
                    for n in clients:
                        server.sendto(commandJSON.encode(), n)
                    
                else:
                    server.sendto(message, client)
            except:
                clients.remove(client)


t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()
