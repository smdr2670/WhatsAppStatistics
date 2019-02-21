
import re

def parseMsg(msg):
    dateTimeUser, messagepayload = msg.split(": ")
    date = dateTimeUser.split(", ")[0]


if __name__ == '__main__':

    filename = "_chat.txt"
    msgList = []
    with open(filename, "r", encoding = "utf-8") as f:
        next(f)
        line = f.readline()
        while line:
            msgList.append(line)
            line = f.readline()
