import socket
import threading
import queue

messages = queue.Queue()
clients = []

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("127.0.0.1", 9999))

def receive():
    while True:
        try:
            message, addr = server.recvfrom(1024)
            print(message.decode(), 1)
            messages.put((message, addr))
        except:
            pass

def broadcast():
    while True:
        while not messages.empty():
            message, addr = messages.get()
            print(message.decode(), 24) # messages are printed in the server terminal
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                try:
                    if message.decode().startswith("/join "):
                        name = message.decode()[message.decode().index(" ")+1:]
                        print(name, 3)
                        server.sendto(f"Welcome {name}!".encode(), client)
                    else:
                        server.sendto(message, client)
                except:
                    clients.remove(client)


t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()

{
    # localIP     = "127.0.0.1"
# localPort   = 20001
# bufferSize  = 1024

# msgFromServer       = "Hello UDP Client"
# bytesToSend         = str.encode(msgFromServer)

# # Create a datagram socket
# UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# # Bind to address and ip
# UDPServerSocket.bind((localIP, localPort))

# print("UDP server up and listening")

# # Listen for incoming datagrams
# while(True):
#     bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
#     message = bytesAddressPair[0]
#     address = bytesAddressPair[1]
#     clientMsg = "Message from Client:{}".format(message)
#     clientIP  = "Client IP Address:{}".format(address)
#     print(clientMsg)
#     print(clientIP)

#     # Sending a reply to client
#     UDPServerSocket.sendto(bytesToSend, address)
}
