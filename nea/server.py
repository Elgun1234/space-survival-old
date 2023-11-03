import socket
import sqlite3

con = sqlite3.connect("users.db")
cur = con.cursor()
cur.execute("CREATE TABLE Accounts(User_ID, Usernames, Passwords, Date_Created,settings,highest_score)")

def check_user_pass(received_data):
  res = cur.execute(f"SELECT Usernames FROM Accounts WHERE {received_data}")# check if pass and user of same entity matches recirved data
  return res

def add_data(received_data):
  if cur.execute(f"SELECT Usernames FROM Accounts WHERE {received_data[0]}") :
    return True
  else:
    cur.execute(f"INSERT INTO Accounts ('','{received_data[0]}'))
    

s = socket.socket()         
print ("Socket successfully created")

port = 12345# can be anything

s.bind(('0.0.0.0', port))         
print ("socket binded to %s" %(port)) 

s.listen(5)     
print ("socket is listening") # max queue of 5 connections any more is rejected limited by hardware

while True: 
 
# Establish connection with client. 
  c, addr = s.accept()     
  print ('Got connection from', addr )
 
  # send a thank you message to the client. encoding to send byte type. 
  #c.send('Thank you for connecting'.encode()) 
  
  data = client_socket.recv(1024)  # Receive up to 1024 bytes of data
  received_data = data.decode('utf-8')

  if received_data[2]=="login":
    if check_user_pass(received_data):
      c.send('True'.encode())
    else:
      c.send('False'.encode())
  if received_data[2]=="signup":
    x=  add_data(received_data)
    if x:
      c.send('False'.encode())
      
  

  #check/add
 
  # Close the connection with the client 
  c.close()
   
  
