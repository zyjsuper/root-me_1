import socket
import sys
import string
import math
import base64
import codecs
import zlib

#connection info
host = "irc.root-me.org"
port = 6667
channel = "#root-me_challenge"
bot = "Candy"

#needed
readbuffer = ""
listening = 1

#not know
servername = "foo"

botname = "p1ng_bot"
nick = botname
ident = botname
realname = botname
master = "p1ng"

s = socket.socket()
s.connect((host, port))
s.send(bytes("NICK %s\r\n" % nick, "UTF-8"))
s.send(bytes("USER %s %s %s :%s\r\n" % (ident, host, servername, realname), "UTF-8"))
s.send(bytes("Join %s\r\n" % channel, "UTF-8"))
s.send(bytes("PRIVMSG %s : Hello Master\r\n" % master, "UTF-8"))

while 1:
    readbuffer+=s.recv(1024).decode("UTF-8")
    temp = str.split(readbuffer, "\n")
    readbuffer = temp.pop()

    for line in temp:
        #for debugging
        print(line.encode("UTF-8"))
        
        line = str.rstrip(line)
        line = str.split(line)

        #automatic respond to PING/PONG IRC requests
        if (line[0] == "PING"):
            s.send(bytes("PONG %s\r\n" % line[1], "UTF-8"))
        
        if(line[1] == "PRIVMSG"):
            sender = ""
            for char in line[0]:
                if(char == "!"):
                    break
                if(char != ":"):
                    sender += char
            size = len(line)
            i = 3
            message = ""
            while (i < size):
                message += line[i] + " "
                i += 1
            message = message.lstrip(":")

            #here we compute the message from Candy
            print("\r\n" + sender + ":\r\n" + message + "\r\n")

            #we start with a PRIVMSG "go"
            if sender == "p1ng":
                s.send(bytes("PRIVMSG p1ng starting!\r\n", "UTF-8")) 
                s.send(bytes("PRIVMSG Candy !ep4\r\n", "UTF-8"))
            
            #if candy responds
            if (sender == "Candy"):
                if listening:
                    if message.split(" ")[0] == "You":
                        s.send(bytes(("PRIVMSG p1ng " + str(message) + "\r\n"), "UTF-8"))
                        listening = 0

                    #1 decode the base64 format
                    decoded = base64.standard_b64decode(str.encode(message))                              
                    #2 unzip
                    unzip = zlib.decompress(decoded)
                    #3 byte -> string
                    response = unzip.decode("UTF-8")

                    s.send(bytes(("PRIVMSG p1ng !ep4 -rep " + response + "\r\n"), "UTF-8"))
                    s.send(bytes(("PRIVMSG Candy !ep4 -rep " + response + "\r\n"), "UTF-8"))
                
                