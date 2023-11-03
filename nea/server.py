import socket
import sqlite3
from datetime import datetime
import pickle

con = sqlite3.connect("users.db")
cur = con.cursor()
#cur.execute("CREATE TABLE Accounts(Username, Password, Date_Created,settings,highest_score)")



def check_user_pass(received_data):
    cur.execute("SELECT Username FROM Accounts WHERE Username=? AND Password=?",(received_data[1],received_data[2]))  # check if pass and user of same entity matches recirved data
    if cur.fetchone() == None:
        return False
    else:
        return True

def check_user(received_data):
    cur.execute("SELECT Username FROM Accounts WHERE Username=?",received_data[1])
    if cur.fetchone() == None:
        return False
    else:
        return True

def add_data(received_data):
        cur.execute("INSERT INTO Accounts (Username, Password, Date_Created,settings,highest_score) VALUES (?,?,?,?,?)",(received_data[1],received_data[2],datetime.now(),received_data[3],received_data[4]))  # received_data[2] is login or signup received_data[3] 456 is rest
        con.commit()


def update_config(received_data):
    cur.execute("UPDATE users SET settings = ? WHERE Username = ?", (received_data[2], received_data[1]))
    con.commit()



s = socket.socket()
print("Socket successfully created")

port = 2000  # can be anything

s.bind(("0.0.0.0", port))
print(f"socket binded to {port}")

s.listen(5)
print("socket is listening")  # max queue of 5 connections any more is rejected limited by hardware

while True:

    # Establish connection with client.
    sock, address = s.accept()
    print("Got connection from", address)



    data = sock.recv(1024)  # Receive up to 1024 bytes of data
    received_data = pickle.loads(data)

    if received_data[0] == "login":
        if check_user_pass(received_data):
            sock.send("True".encode())
            sock.close()
        else:
            sock.send("False".encode())
            sock.close()

    if received_data[0] == "signup":
        if check_user(received_data):
            sock.send("False".encode())
            sock.close()

        else:
            add_data(received_data)
            sock.send("True".encode())
            sock.close()
    if received_data[0]=="config":
        update_config(received_data)
        sock.close()




