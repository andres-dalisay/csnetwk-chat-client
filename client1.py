import socket
import json
import random

CONNECTION_ERROR = "Error: Connection to the Message Board Server has failed! Please check IP Address and Port Number."
PARAMETER_ERROR = "Error: Command parameters do not match or is not allowed."
DISCONNECTION_ERROR = "Error: Disconnection failed. Please connect to the server first."
COMMAND_ERROR = "Error: Command not found."


connected = False
registered = False
handle = ""

clientIP = socket.gethostbyname(socket.gethostname())
clientPort = random.randint(8000, 9000)

while True:
    while not connected:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        message = input()

        if (message.startswith("/")):
            commandBody = message[1:]
            splitBody = commandBody.split(" ")
            
            if (splitBody[0] == "leave"):
                print(DISCONNECTION_ERROR)
            elif (splitBody[0] == "?"):
                print("help")
            elif (splitBody[0] == "register" or splitBody[0] == "all" or splitBody[0] == "msg"):
                print("Error: In order to use this command, please connect to a server first.")
            elif (splitBody[0] == "join"):
                if (len(splitBody) != 3):
                    print(PARAMETER_ERROR)
                else:
                    connectionIP = splitBody[1]
                    connectionPort = int(splitBody[2])
                    commandDict = {"command":"join"}
                    commandJSON = json.dumps(commandDict)
                    try:
                        client.bind((clientIP, clientPort))
                        client.sendto(commandJSON.encode(), (connectionIP, connectionPort))
                        response, server = client.recvfrom(1024)
                    except:
                        print(CONNECTION_ERROR)
                    else:
                        res = json.loads(response.decode())
                        print(res["message"])
                        connected = True
            else:
                print(COMMAND_ERROR)
        else:
            print(COMMAND_ERROR)


    message = input()

    if (message.startswith("/")):
        commandBody = message[1:]
        splitBody = commandBody.split(" ", 1)

        if (splitBody[0] == "leave"):
            if (len(splitBody) == 1):
                commandDict = {"command":"leave"}
                commandJSON = json.dumps(commandDict)
                try:
                    client.sendto(commandJSON.encode(), (connectionIP, connectionPort))
                    client.close()
                except:
                    print("Error: Disconnection failed.")
                else:
                    print("Connection closed. Thank you!")
                    connected = False
                    registered = False
            else:
                print(PARAMETER_ERROR)
        
        if (splitBody[0] == "register" and registered == False): 
            if (len(splitBody) == 2 and len(splitBody[1].split(" ")) == 1):
                commandDict = {"command":"register", "handle":splitBody[1]}
                commandJSON = json.dumps(commandDict)
                try:
                    client.sendto(commandJSON.encode(), (connectionIP, connectionPort))
                    response, server = client.recvfrom(1024)
                except:
                    print("Client Error")
                    ##TODO: check if needed pa
                else:
                    res = json.loads(response.decode())
                    
                    if res["command"] == "error":
                        print(res["message"])
                    else:
                        registered = True
                        print(res["message"])
                        
            else:
                print(PARAMETER_ERROR)
        elif (splitBody[0] == "register" and registered == True):
            print("Error: You are already registered!")

        if (splitBody[0] == "all"):
            if (len(splitBody) == 2):
                msg = splitBody[1]
                
                commandDict = {"command":"all", "message":msg}
                commandJSON = json.dumps(commandDict)

                try:
                    client.sendto(commandJSON.encode(), (connectionIP, connectionPort))
                    response, server = client.recvfrom(1024)
                except:
                    print("error")
                else:
                    print(response.decode())        
            else:
                print(PARAMETER_ERROR)
            
        
        if (splitBody[0] == "msg"):
            params = splitBody[1].split(" ", 1)
            if (len(params) == 2):
                commandDict = {"command":"register", "handle": params[0], "message": params[1]}
                commandJSON = json.dumps(commandDict)

                try:
                    client.sendto(commandJSON.encode(), (connectionIP, connectionPort))
                    response, server = client.recvfrom(1024)
                except:
                    print("error")
                else:
                    print(response.decode())
            else:
                print(PARAMETER_ERROR)
    else:
        print(COMMAND_ERROR)
    
