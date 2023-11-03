import socket
import sqlite3

con = sqlite3.connect("users.db")
cur = con.cursor()
cur.execute("CREATE TABLE Accounts(User_ID, Usernames, Passwords, Date_Created,settings)")
