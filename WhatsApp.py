
import re

def parseMsg(msg):
    dateTimeUsername, messagepayload = msg.split(": ")
    msgDate, msgTime, username = re.split(", | - ", dateTimeUsername)


if __name__ == '__main__':

    filename = "_chat.txt"
    msgList = []
    with open(filename, "r", encoding = "utf-8") as f:
        next(f)
        line = f.readline()
        while line:
            msgList.append(line)
            line = f.readline()
