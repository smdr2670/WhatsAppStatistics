import re

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Message(object):
    def __init__(self, date, sender, content):
        self.date = date
        self.sender = sender
        self.content = content
        self.isMedia = content == '<Medien ausgeschlossen>\n'


class MessageList(object):
    def __init__(self):
        self.msgList = []
        self.senderList = []

    def appendTrailingMessage(self, content):
        self.msgList[-1].content += content

    def appendMessage(self, message):
        self.msgList.append(message)
        if message.sender not in self.senderList:
            self.senderList.append(message.sender)

    def feedMessage(self, msg):
        dt = msg[0:15]
        m = re.match('\d{2}\.\d{2}\.\d{2},\s\d{2}:\d{2}', dt)

        if m is not None:
            splitMsg = msg[18:].split(": ", 1)
            if len(splitMsg) >= 2:
                # We have a valid message
                msgSender = splitMsg[0]
                msgPayload = " ".join(splitMsg[1:])
                self.appendMessage(Message(dt, msgSender, msgPayload))
            else:
                # Meta info message (group was created, user joined/left etc.)
                pass
        else:
            # trailing message of previous message
            self.appendTrailingMessage(msg)



def plotTotalNumberOfMessages(msgList):
    numberOfMessagesSentDict = {}
    for sender in msgList.senderList:
        numberOfMessagesSentDict[sender] = [0, 0]

    for message in msgList.msgList:
        if message.isMedia:
            numberOfMessagesSentDict[message.sender][1] = numberOfMessagesSentDict[message.sender][1] + 1
        else:
            numberOfMessagesSentDict[message.sender][0] = numberOfMessagesSentDict[message.sender][0] + 1

    for sender in numberOfMessagesSentDict:
        print("{0} : {1} text messages, {2} media messages".format(
            sender, numberOfMessagesSentDict[sender][0], numberOfMessagesSentDict[sender][1]))

    listOfSenders = []
    listOfTotalMessages = []
    listOfMediaMessages = []

    # labels for bars

    for key, value in numberOfMessagesSentDict.items():
        listOfSenders.append(key)
        listOfTotalMessages.append(value[0])
        listOfMediaMessages.append(value[1])

    ind = np.arange(len(listOfSenders))

    width = 0.35  # the width of the bars

    _, ax = plt.subplots()
    rects1 = ax.bar(ind - width/2, listOfTotalMessages, width,
                    color='SkyBlue', label='Text messages')
    rects2 = ax.bar(ind + width/2, listOfMediaMessages, width,
                    color='IndianRed', label='Media Messages')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Number of messages')
    ax.set_title('Group chat ...')
    ax.set_xticks(ind)
    ax.set_xticklabels(listOfSenders)
    ax.legend()

    def autolabel(rects, xpos='center'):
        """
        Attach a text label above each bar in *rects*, displaying its height.

        *xpos* indicates which side to place the text w.r.t. the center of
        the bar. It can be one of the following {'center', 'right', 'left'}.
        """
        xpos = xpos.lower()  # normalize the case of the parameter
        ha = {'center': 'center', 'right': 'left', 'left': 'right'}
        offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.01*height,
                    '{}'.format(height), ha=ha[xpos], va='bottom')

    autolabel(rects1, "left")
    autolabel(rects2, "right")
    plt.show()

if __name__ == '__main__':

    filename = "F:\Downloads\_chat.txt"
    msgList = MessageList()

    with open(filename, "r", encoding="utf-8") as f:
        line = f.readline()
        while line:
            line = f.readline()
            msgList.feedMessage(line)

    print("All in all number of messages: {0}".format(len(msgList.msgList)))

    plotTotalNumberOfMessages(msgList)

    mostQuacky = max(msgList.msgList, key=lambda x: len(x.content))
    print("{} {} {} characters".format(mostQuacky.sender,
          mostQuacky.date, len(mostQuacky.content)))





