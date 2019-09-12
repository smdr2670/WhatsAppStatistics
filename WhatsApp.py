import re
import emoji

import matplotlib.pyplot as plt
import WhatsAppVisualizationModule as statPlot

from collections import Counter
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class Message(object):
    def __init__(self, date, sender, content):
        self.date = date
        self.sender = sender
        self.content = content
        self.isMedia = content == '<Medien ausgeschlossen>\n'

class MessageListReader(QObject):

    emojiSignal = pyqtSignal(dict)
    wordSignal = pyqtSignal(dict)
    messageByPersonSignal = pyqtSignal(dict)
    mediaMessageByPersonSignal = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(MessageListReader, self).__init__(parent)
        self.msgList = []
        self.senderList = []
        self.emojiCount = {}
        self.wordCount = {}
        self.msgByUserCount = {}
        self.mediaMsgByUserCount = {}

    
    def loadFile(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            line = f.readline()
            while line:
                line = f.readline()
                self.feedMessage(line)

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

    def getwordCount(self, numberOfmostCommon = 10, caseSensitive = False):
        wordCnt = Counter()
        for msg in self.msgList:
            if not msg.isMedia:
                for word in msg.content.split():
                    if caseSensitive:
                        wordCnt[word] +=1
                    else:
                        wordCnt[word.lower()] +=1
        ret = dict()
        for person, numWords in wordCnt.most_common(numberOfmostCommon):
            ret[person] = numWords
        return ret

    def getemojiCount(self, numberOfmostCommon = 10):
        emojiCnt = Counter()
        for msg in self.msgList:
            if not msg.isMedia:
                for c in msg.content:
                    if c in emoji.UNICODE_EMOJI:
                        emojiCnt[c] += 1
        ret = dict()
        for person, numEmojis in emojiCnt.most_common(numberOfmostCommon):
            ret[person] = numEmojis
        return ret

    def getTextMessagesPerPersonCount(self, numberOfmostCommon = 10):
        textMessageCnt = Counter()
        for msg in self.msgList:
            if not msg.isMedia:
                textMessageCnt[msg.sender] += 1
        ret = dict()
        for person, numMessages in textMessageCnt.most_common(numberOfmostCommon):
            ret[person] = numMessages
        return ret

    def getMediaMessagesPerPersonCount(self, numberOfmostCommon = 10):
        mediaMessageCnt = Counter()
        for msg in self.msgList:
            if msg.isMedia:
                mediaMessageCnt[msg.sender] += 1
        ret = dict()
        for person, numMessages in mediaMessageCnt.most_common(numberOfmostCommon):
            ret[person] = numMessages
        return ret


    @pyqtSlot(int)
    def onJob(self, indx):
        if indx == 0:
            if not self.emojiCount:
                self.emojiCount = self.getemojiCount()
            self.emojiSignal.emit(self.emojiCount)
        if indx == 1:
            if not self.wordCount:
                self.wordCount = self.getwordCount()
            self.wordSignal.emit(self.wordCount)
        if indx == 2:
            if not self.msgByUserCount:
                self.msgByUserCount = self.getTextMessagesPerPersonCount()
            self.messageByPersonSignal.emit(self.msgByUserCount)
        if indx == 3:
            if not self.mediaMsgByUserCount:
                self.mediaMsgByUserCount = self.getMediaMessagesPerPersonCount()
            self.mediaMessageByPersonSignal.emit(self.mediaMsgByUserCount)
