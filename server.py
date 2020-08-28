import threading
import socket

host = "127.0.0.1"  #localhost
port = 60000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #TCP
server.bind((host, port)) #binding the IP
server.listen()   #server listening for connections

clients = []
nicknames = []

#broadcast server message to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

#try and get a message, if one is found broadcast it out to all clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = client.index(client)
            client.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f'{nickname} left the chat'.encode('ascii'))
            break



def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        #getting the nickname and the client info
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat'.encode('ascii'))
        client.send('Connected to the server'.encode('ascii'))
        #makes number of threads equal to clients
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Server is listening........")
receive()