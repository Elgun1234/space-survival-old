import socket
import sqlite3

con = sqlite3.connect("users.db")
cur = con.cursor()
cur.execute("CREATE TABLE Accounts(User_ID, Usernames, Passwords, Date_Created,settings,highest_score)")

def check_details(received_data):
  res = cur.execute(f"SELECT Usernames FROM Accounts WHERE {received_data}")
  return res
  
  

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

  if check_details(received_data):
    c.send('False'.encode())
  else:
    c.send('True'.encode())

  #check/add
 
  # Close the connection with the client 
  c.close()
   
  
