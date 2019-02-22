import datetime
import re
from dateutil import parser

class Message(object):
    def __init__(self, date, sender, content):
        self.date = date
        self.sender = sender
        self.content = content
        self.isMedia = content == '<Medien ausgeschlossen>'

class MessageList(object):
    def __init__(self, msgList):
        self.msgList = msgList

    def appendTrailingMessage(self, content):
        self.msgList[-1].content += content

    def appendMessage(self, message):
        self.msgList.append(message)

    def feedMessage(self, msg):
        dt = msg[0:15]
        m = re.match('\d{2}\.\d{2}\.\d{2},\s\d{2}:\d{2}', dt)       
        
        if m is not None:
            splitMsg = msg[18:].split(": ", 1)
            if len(splitMsg) >= 2:
                # We have a valid message
                msgSender = splitMsg[0]
                msgPayload = splitMsg[1:]
                self.appendMessage(Message(dt, msgSender, msgPayload))
            else:
                # Meta info message (group was created, user joined/left etc.)
                pass 
        else:
            # trailing message of previous message
            self.appendTrailingMessage(msg)             

    
if __name__ == '__main__':

    filename = "F:\Downloads\_chat.txt"
    msgList = MessageList([])
    
    with open(filename, "r", encoding = "utf-8") as f:
        line = f.readline()
        while line:
            line = f.readline()
            msgList.feedMessage(line) 

    print("Total number of messages: {0}".format(len(msgList.msgList)))
