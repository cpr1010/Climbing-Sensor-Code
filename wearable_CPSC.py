# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:54:03 2022

@author: coler
"""

import socket

#counter = 0

HOST = "0.0.0.0"
PORT = 9999

s = socket.socket()

s.bind((HOST, PORT))
s.listen()

dist = []

while True:
    client, addr = s.accept()
    print("Running")
    
    
    while True:
        content = client.recv(12)
        content = content.decode()
        content = str(content)
        
        if len(content) == 0:
            #counter += 1
            break
            
        else:
            #counter += 1
            dist.append(content)
            
            with open(r"C:\Users\coler\OneDrive\Desktop\wearable_climbing.txt", 'a') as f:
                f.write(content)
            
            
print(dist)
client.close()

