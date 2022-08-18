import socket

s = socket.socket() #type of network working with IPV4 or IPV6 (BY defualt it is IPV4)
                    # type of network UDP ot TCP (by defualt TCP)

print('Socket Created')
s.bind(('localhost',8088)) # last port number 0 to 65535

s.listen(3)
print('Waiting for connections..')

while True:
    c, address = s.accept()
    name = c.recv(1024).decode()
    password = c.recv(1024).decode()
    if name =="Prathiksha" and password == "abc@123" :
        print("Connected with ", name," and address is ", address)
        c.send(bytes("Logged in..",'utf-8')) #utf is a format
        c.close()
    else:
        c.send(bytes("Login faild..", "utf-8"))
        c.close()
