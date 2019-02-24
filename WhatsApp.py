import re
import matplotlib.pyplot as plt
import WhatsAppVisualizationModule as statPlot

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


if __name__ == '__main__':

    filename = "F:\Downloads\_chat.txt"
    msgList = MessageList()

    with open(filename, "r", encoding="utf-8") as f:
        line = f.readline()
        while line:
            line = f.readline()
            msgList.feedMessage(line)

    print("All in all number of messages: {0}".format(len(msgList.msgList)))

    mostCommonWords = statPlot.wordCount(msgList)
    statPlot.plotMostUsed(mostCommonWords, 'used words', yLabel='Word')

    mostCommonEmojis = statPlot.emojiCount(msgList)
    statPlot.plotMostUsed(mostCommonEmojis, 'used Emojis', yLabel='Emoji')

    messageByUserCount = statPlot.messageByUserCount(msgList, isMedia=False)
    mediaByUserCount = statPlot.messageByUserCount(msgList, isMedia=True)
    statPlot.plotMostUsed(messageByUserCount, 'messages spammers', yLabel='Person')
    statPlot.plotMostUsed(mediaByUserCount, 'media spammers', yLabel='Person')

    mostQuacky = max(msgList.msgList, key=lambda x: len(x.content))
    print("{} {} {} characters".format(mostQuacky.sender,
          mostQuacky.date, len(mostQuacky.content)))

    plt.show()





