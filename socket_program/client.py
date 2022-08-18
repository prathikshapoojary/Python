import socket

c = socket.socket()
c.connect(('localhost',8088))

name = input("Enter the user name :")
c.send(bytes(name,'utf-8'))
password = input("Enter the password :")
c.send(bytes(password,'utf-8'))

print(c.recv(1024).decode())

