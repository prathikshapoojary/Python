import socket
import sys
import re
import csv
import os

try:
    check_value = sys.argv[1]
    if len(check_value) < 11:
        raise Exception
except:
    print("Index error..")
    sys.exit();

if len(check_value) == 0 or check_value.strip() == "":
    print("Error found in argumenets..")
else:
    if re.search(r'\.csv$', check_value):  
        updated_values = check_value.split('|')
        table_name = updated_values[1]
        filename = updated_values[2]
        try:
            if os.path.exists(filename):
                if os.path.getsize(filename) == 0:
                    print("File is empty..")
                    exit()
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection.connect(("172.16.0.36",8056))
                print("Client >> ",check_value)
                connection.send(bytes(check_value,'utf-8'))
                with open(filename) as file_object:
                    print("Reading file..")
                    read_object = csv.reader(file_object)
                    row_value = ""
                    for line in read_object:
                        for value in line:
                            row_value += value +"|" 
                        connection.send(bytes(row_value,'utf-8'))
                        print(connection.recv(1024).decode(),"\n :",line)
                        row_value = ""
                        print("\n")
            else:
                print("File dose not exists..")            
        except IOError:
            print("Error found while reading file..")
    else:
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect(("172.16.0.36",8056))
        print("Client >> ",check_value)
        connection.send(bytes(check_value,'utf-8'))
        for index in range(3):
            print(connection.recv(1024).decode())
        for index in range(80):
            print("_", end = "");
        print("\n")


