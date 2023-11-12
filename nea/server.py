import socket
import sqlite3

import pickle

con = sqlite3.connect("users.db")
cur = con.cursor()
try:
    cur.execute("CREATE TABLE Accounts(Username, Password, hours_played,minutes,settings,highest_score)")
except:
    pass


def check_user_pass(received_data):
    cur.execute("SELECT Username FROM Accounts WHERE Username=? AND Password=?",(received_data[1],received_data[2]))  # check if pass and user of same entity matches recirved data

    if cur.fetchone() == None:
        return False
    else:
        return True

def check_user(received_data):
    cur.execute("SELECT Username FROM Accounts WHERE Username=?",(received_data[1],))
    if cur.fetchone() == None:
        return False
    else:
        return True

def add_data(received_data):
        cur.execute("INSERT INTO Accounts (Username, Password, hours_played,minutes,settings,highest_score) VALUES (?,?,?,?,?,?)",(received_data[1],received_data[2],0,0,received_data[3],received_data[4]))  # received_data[2] is login or signup received_data[3] 456 is rest
        con.commit()
def update_config(received_data):
    cur.execute("UPDATE Accounts SET settings = ? WHERE Username = ?", (received_data[2], received_data[1]))
    con.commit()

def fetch_hours(received_data):
    cur.execute("SELECT hours_played FROM Accounts WHERE Username=?", (received_data[1],))
    hours = cur.fetchone()
    return hours[0]

def fetch_settiings(received_data):
    cur.execute("SELECT settings FROM Accounts WHERE Username=?", (received_data[1],))
    settings = cur.fetchone()
    return settings[0]
def update_hours(received_data):
    cur.execute("SELECT hours_played,minutes FROM Accounts WHERE Username=?",(received_data[1],))
    hours,minutes = cur.fetchone()
    minutes+=1
    if minutes // 60 == 1:
        hours +=minutes // 60
        minutes = 0

    cur.execute("UPDATE Accounts SET hours_played = ?,minutes=? WHERE Username = ?", (hours,minutes, received_data[1]))
    con.commit()



s = socket.socket()
print("Socket successfully created")

port = 3100  # can be anything
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
        print("login")
        if check_user_pass(received_data):
            print(fetch_settiings(received_data))
            data = pickle.dumps(["True", fetch_settiings(received_data)])
            sock.send(data)
            sock.close()
        else:
            sock.send("False".encode())
            sock.close()

    if received_data[0] == "signup":
        print("signup")
        if check_user(received_data):
            sock.send("False".encode())
            sock.close()

        else:
            add_data(received_data)
            print("added data")
            sock.send("True".encode())
            sock.close()
            print("closed")
    if received_data[0]=="config":
        print("config")
        update_config(received_data)
        sock.send("True".encode())
        sock.close()
    if received_data[0]=="hours":
        print("hours")
        update_hours(received_data)
        sock.close()
    if received_data[0]=="fetch":
        print("fetch")
        sock.send(str(fetch_hours(received_data)).encode())
        sock.close()
