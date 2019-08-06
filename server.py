# Made with help from tutorials at Sentdex youtube channel


import socket
import time
import pickle



HEADERSIZE = 10




s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((socket.gethostname(),1236))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection with {address} has been established!")

    # Random test object: arbitary
    d = {1: 'alec is good', 2: 56, 'this': 'very'}
    
    msg = pickle.dumps(d)
    msg = bytes(f"{len(msg):<{HEADERSIZE}}",'utf-8')+msg

    clientsocket.send(msg)
    
