import socket
import sqlite3
from datetime import datetime, timedelta
import pickle
import hashlib

con = sqlite3.connect("users.db")
cur = con.cursor()
try:
    cur.execute("CREATE TABLE Accounts(Username, Password)")
except:
    pass
try:
    cur.execute("CREATE TABLE Information(Username,playtime,settings,highest_score,total_score,runs,bullets_shot)")
except:
    pass


def check_user_pass(received_data):
    cur.execute("SELECT Username FROM Accounts WHERE Username=? AND Password=?",(received_data[1],hashlib.sha512(received_data[2].encode(encoding = 'UTF-8', errors = 'strict')).digest())) # check if pass and user of same entity matches recirved data

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
        cur.execute("INSERT INTO Accounts (Username, Password) VALUES (?,?)",(received_data[1],hashlib.sha512(received_data[2].encode(encoding = 'UTF-8', errors = 'strict')).digest()))  # look at signup in main
        cur.execute("INSERT INTO Information (Username,playtime, settings, highest_score,total_score,runs,bullets_shot) VALUES (?,?,?,?,?,?,?)",(received_data[1],str(timedelta()),received_data[3],0,0,0,0))#0
        con.commit()
def update_config(received_data):
    cur.execute("UPDATE Information SET settings = ? WHERE Username = ?", (received_data[2], received_data[1]))
    con.commit()

def fetch_hours(received_data):
    cur.execute("SELECT playtime,total_score,runs,bullets_shot ,highest_score FROM Information WHERE Username=?", (received_data[1],))



    return cur.fetchone()

def fetch_settiings(received_data):
    cur.execute("SELECT settings FROM Information WHERE Username=?", (received_data[1],))
    settings = cur.fetchone()
    return settings[0]

def string_2_timedelta(string):
    x = string.split(":")
    return timedelta(hours=int(x[0]),minutes=int(x[1]),seconds=int(x[2]))

def update_info(received_data):## datetimme
    cur.execute("SELECT playtime,total_score,runs,bullets_shot ,highest_score FROM Information WHERE Username=?",(received_data[1],))
    info = cur.fetchone()

    new_time = string_2_timedelta(info[0]) + string_2_timedelta(received_data[2]) 

    new_total = info[1]+received_data[3]
    print(info[2])
    runs =1+info[2]
    new_bullet = info[3]+received_data[4]
    if info[4]<received_data[3]:
        cur.execute("UPDATE Information SET playtime = ?,total_score= ?,runs= ?,bullets_shot= ?,highest_score= ? WHERE Username = ?", (str(new_time), new_total, runs, new_bullet,received_data[3], received_data[1]))
    else:

        cur.execute("UPDATE Information SET playtime = ?,total_score= ?,runs= ?,bullets_shot= ? WHERE Username = ?", (str(new_time),new_total,info[2],new_bullet, received_data[1]))

    con.commit()
def leaderboard_fetch():
    cur.execute("SELECT Username,highest_score FROM Information ORDER BY highest_score DESC LIMIT 10")
    return cur.fetchall()
    



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
        update_info(received_data)
        sock.close()
    if received_data[0]=="fetch":
        print("fetch")
        sock.send(str(fetch_hours(received_data)).encode())
        sock.close()
    if received_data[0]=="leaderboard":
        print("leaderboard")
