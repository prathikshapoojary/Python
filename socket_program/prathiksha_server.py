#Name:Prathiksha
#Date of creation: 29 August 2022

import logging
import mysql.connector
import socket
logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
try:
    mydb = mysql.connector.connect(
        host="localhost", user="prathiksha", password="Mypassword1!"
    )
    print("Connected to mysql..")
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE IF NOT EXISTS Student;")
    mycursor.execute("USE Student")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Student (ID INT NOT NULL, Name VARCHAR(255), Age INT, EmailID VARCHAR(255), Branch VARCHAR(6),PRIMARY KEY(ID) )")
    mycursor.execute("CREATE TABLE IF NOT EXISTS Marks (ID INT, Semester INT, Subject1 INT, Subject2 INT, Subject3 INT, Subject4 INT, Subject5 INT, Subject6 INT, FOREIGN KEY(ID) REFERENCES Student(ID));")
    print("Created Student database with 'Student' and 'Marks' tables..")
except:
    print("Error found..")
    logging.warning("Error found..")

server = socket.socket() #type of network working with IPV4 or IPV6 (BY defualt it is IPV4) # type of network UDP ot TCP (by defualt TCP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print('Socket Created')
server.bind(('172.16.0.36',8056)) # last port number 0 to 65535
server.listen(1)
print('Waiting for connections..')

#For select operation:
def actionSelect(table_name,record_id):    
    query = f"SELECT * FROM {table_name} WHERE ID = {record_id}" 
    mycursor.execute(query)
    records = mycursor.fetchall()
    print("\nSending response to client..")
    return records

#For insert operation:
def actionInsert(table_name,recv_line_lst): 
    updated_values = recv_line_lst.split('|')
    if table_name == 'Student':
        query = f'INSERT INTO {table_name} VALUES ({updated_values[0]},"{updated_values[1]}",{updated_values[2]},"{updated_values[3]}","{updated_values[4]}")'
        mycursor.execute(query)
    elif table_name == 'Marks':
        query = f'INSERT INTO {table_name} VALUES ({updated_values[0]},{updated_values[1]},{updated_values[2]},{updated_values[3]},{updated_values[4]},{updated_values[5]},{updated_values[6]},{updated_values[7]})'
        mycursor.execute(query)
    mydb.commit()

#For delete operation:
def actionDelete(table_name,record_id):
    try:
        query = f"DELETE FROM {table_name} WHERE ID = {record_id}"
        mycursor.execute(query)
        mydb.commit()
    except:
        return 0

while True:
    connection, address = server.accept()
    values = connection.recv(1024).decode()
    print("Connected with ", address)
    updated_values = values.split('|')
    print("Recevied from client :",updated_values)
    ser_str = "Server >>  "
    connection.send(bytes(ser_str,'utf-8')) #utf is a format
    
    #For choice : select, insert and delete
    if int(updated_values[0]) == 1:
        print("\nSELECT OPERATION :");
        try:
            table_name = updated_values[1]
            record_id = updated_values[2]
            sel_records = actionSelect(table_name,int(record_id))
            formated_output =str(sel_records).strip(")][(").split(', ')
            student = ["ID = ", "Name = ", "Age  = ","EmailID  = ","Branch =" ]
            marks = ["ID = ", "Semester = ", "Subject1  = ","Subject2  = ","Subject3 =", "Subject4  = ","Subject5  = ","Subject6 =" ]
            if table_name == "Student":
                if len(sel_records) == 0:
                    connection.send(bytes(f"Data not found in '{table_name}' table for given ID..",'utf-8'))
                    logging.warning(f"Data not found in '{table_name}' table for given ID..")
                else:
                    values = updated_values[0] +"|"+table_name+"| "
                    for (i,j) in zip(student, formated_output):
                        values += i+j +", "
                    connection.send(bytes(str(values),'utf-8'))
                    print(values[:-1])
            elif table_name == "Marks":
                if len(sel_records) == 0:
                    connection.send(bytes(f"Data not found in '{table_name}' table for given ID..",'utf-8'))
                    logging.warning(f"Data not found in '{table_name}' table for given ID..")
                else:
                    values = updated_values[0] +"|"+table_name+"| "
                    for (i,j) in zip(marks, formated_output):
                        values += i+j +", "
                    connection.send(bytes(str(values),'utf-8'))
                    print(values[:-1])
            else:
                connection.send(bytes("Table name not found in database..",'utf-8'))
                logging.warning("Table name not found in database..")
        except:
            connection.send(bytes("Invalid input..",'utf-8'))
            logging.warning("Invalid input..")

    elif int(updated_values[0]) == 2:
        table_name = updated_values[1]
        record_id = updated_values[2]
        print("\nINSERT OPERATION :");
        recv_line = []
        try:
            while 1:
                recv_line = connection.recv(1024).decode()
                if recv_line == "":
                    break
                print(f"Inserting to {table_name} table :",recv_line)
                if table_name == "Student":
                    actionInsert(table_name,str(recv_line))
                    connection.send(bytes("Record inserted..\n",'utf-8'))
                elif table_name == "Marks":
                    actionInsert(table_name,recv_line)
                    connection.send(bytes("Record inserted..",'utf-8'))
        except:
            connection.send(bytes("Error found while inserting records..",'utf-8'))
            logging.warning("Error found while inserting records..")

    elif int(updated_values[0]) == 3:
        print("\nDELETE OPERATION :");
        try:
            table_name = updated_values[1]
            record_id = updated_values[2]
            if table_name == "Student" or table_name == "Marks":
                sel_records = actionSelect(table_name,int(record_id))
                if len(sel_records) == 0:#before deleting
                    connection.send(bytes("Data not found for given ID..",'utf-8'))
                    logging.warning("Data not found for given ID..")
                else:
                    actionDelete(table_name,record_id)
                    del_records = actionSelect(table_name,record_id)
                    if len(del_records) == 0:#after deleteing
                        connection.send(bytes("Successfully deleted..",'utf-8'))
                    else:
                        connection.send(bytes("Record can not be deleted..",'utf-8'))
                        logging.warning("Record can not be deleted..")
            else:
                connection.send(bytes("Table not found..",'utf-8'))
                logging.warning("Table not found..")
        except:
            connection.send(bytes("Invalid input..",'utf-8'))
            logging.warning("Invalid input..")
            
    else:
        connection.send(bytes("Invalid choice..",'utf-8'))
        logging.warning("Invalid choice..")
    connection.close()
