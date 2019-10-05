import re
import emoji

from collections import Counter
from datetime import date
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class WhatsAppMessage(object):
    def __init__(self, date, sender, content):
        self.date = date
        self.sender = sender
        self.content = content
        self.isMedia = content == '<Medien ausgeschlossen>\n'

class WhatsAppMessageParser(QObject):

    emojiSignal = pyqtSignal(dict)
    wordSignal = pyqtSignal(dict)
    messageByPersonSignal = pyqtSignal(dict)
    mediaMessageByPersonSignal = pyqtSignal(dict)

    minDateSignal = pyqtSignal(object)
    maxDateSignal = pyqtSignal(object)

    def __init__(self, parent=None):
        super(WhatsAppMessageParser, self).__init__(parent)
        self.msgList = []
        self.senderList = []

        self.minDate = date(1900, 1, 1)
        self.maxDate = date(2100, 12, 31)

        self.emojiCount = {}
        self.wordCount = {}
        self.msgByUserCount = {}
        self.mediaMsgByUserCount = {}

        self.lastRequestedPlot = ""
        self.firstLoad = True

    def appendTrailingMessage(self, content):
        self.msgList[-1].content += content

    def appendMessage(self, message):
        self.msgList.append(message)
        if message.sender not in self.senderList:
            self.senderList.append(message.sender)

    def feedMessage(self, msg):
        # dt = msg[0:15]
        m = re.match('\d{2}\.\d{2}\.\d{2},\s\d{2}:\d{2}', msg[0:15])

        if m is not None:
            splitMsg = msg[18:].split(": ", 1)
            if len(splitMsg) >= 2:
                # We have a valid message
                dt = date(2000 + int(msg[6:8]), int(msg[3:5]), int(msg[0:2]) )
                # First date
                if self.minDate == date(1900, 1, 1):
                    self.minDate = dt
                # Lazy set last date
                self.maxDate = dt
                msgSender = splitMsg[0]
                msgPayload = " ".join(splitMsg[1:])
                self.appendMessage(WhatsAppMessage(dt, msgSender, msgPayload))
            else:
                # Meta info message (group was created, user joined/left etc.)
                pass
        else:
            # trailing message of previous message
            self.appendTrailingMessage(msg)

    ###########################################################################

    def getwordCount(self, numberOfmostCommon = 10, caseSensitive = False):
        wordCnt = Counter()
        for msg in self.msgList:
            if not msg.isMedia and msg.date > self.minDate and msg.date < self.maxDate:
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
            if not msg.isMedia and msg.date > self.minDate and msg.date < self.maxDate:
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
            if not msg.isMedia and msg.date > self.minDate and msg.date < self.maxDate:
                textMessageCnt[msg.sender] += 1
        ret = dict()
        for person, numMessages in textMessageCnt.most_common(numberOfmostCommon):
            ret[person] = numMessages
        return ret

    def getMediaMessagesPerPersonCount(self, numberOfmostCommon = 10):
        mediaMessageCnt = Counter()
        for msg in self.msgList:
            if msg.isMedia and msg.date > self.minDate and msg.date < self.maxDate:
                mediaMessageCnt[msg.sender] += 1
        ret = dict()
        for person, numMessages in mediaMessageCnt.most_common(numberOfmostCommon):
            ret[person] = numMessages
        return ret

    ###########################################################################

    @pyqtSlot(str)
    def onJob(self, name):
        self.lastRequestedPlot = name
        if name == 'Emojis':
            if not self.emojiCount:
                self.emojiCount = self.getemojiCount()
            self.emojiSignal.emit(self.emojiCount)
        if name == 'Words':
            if not self.wordCount:
                self.wordCount = self.getwordCount()
            self.wordSignal.emit(self.wordCount)
        if name == 'Messages by user':
            if not self.msgByUserCount:
                self.msgByUserCount = self.getTextMessagesPerPersonCount()
            self.messageByPersonSignal.emit(self.msgByUserCount)
        if name == 'Media messages by user':
            if not self.mediaMsgByUserCount:
                self.mediaMsgByUserCount = self.getMediaMessagesPerPersonCount()
            self.mediaMessageByPersonSignal.emit(self.mediaMsgByUserCount)

    @pyqtSlot(str)
    def loadFile(self, filename):
        # clear content
        self.emojiCount = {}
        self.wordCount = {}
        self.msgByUserCount = {}
        self.mediaMsgByUserCount = {}

        self.minDate = date(1900, 1, 1)
        self.maxDate = date(2100, 12, 31)

        # read actual file
        with open(filename, "r", encoding="utf-8") as f:
            line = f.readline()
            while line:
                line = f.readline()
                self.feedMessage(line)
        
        # send minumum and max date
        self.minDateSignal.emit(self.minDate)
        self.maxDateSignal.emit(self.maxDate)

        # do not change index when new file is loaded
        if self.firstLoad:
            self.firstLoad = False
            self.onJob('Emojis')
        else:
            self.onJob(self.lastRequestedPlot)

    @pyqtSlot(object)
    def setMinDate(self, minDate):
        self.minDate = minDate
        self.emojiCount = {}
        self.wordCount = {}
        self.msgByUserCount = {}
        self.mediaMsgByUserCount = {}

        self.onJob(self.lastRequestedPlot)

    @pyqtSlot(object)
    def setMaxDate(self, maxDate):
        self.maxDate = maxDate
        self.emojiCount = {}
        self.wordCount = {}
        self.msgByUserCount = {}
        self.mediaMsgByUserCount = {}

        self.onJob(self.lastRequestedPlot)