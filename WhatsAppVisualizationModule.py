
from collections import Counter
import emoji
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def wordCount(msgList, numberOfmostCommon = 10, caseSensitive = False):
    wordCnt = Counter()
    for msg in msgList.msgList:
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


def emojiCount(msgList, numberOfmostCommon = 10):
    emojiCnt = Counter()
    for msg in msgList.msgList:
        if not msg.isMedia:
            for c in msg.content:
                if c in emoji.UNICODE_EMOJI:
                    emojiCnt[c] += 1
    ret = dict()
    for person, numEmojis in emojiCnt.most_common(numberOfmostCommon):
        ret[person] = numEmojis
    return ret

def messageByUserCount(msgList, isMedia = False):
    messageByUserCnt = Counter()
    for msg in msgList.msgList:
        if isMedia:
            if msg.isMedia:
                messageByUserCnt[msg.sender] += 1    
        else:
            messageByUserCnt[msg.sender] += 1
    
    return dict(messageByUserCnt)

def mostCommonwordsByUser(msgList):
    tmp = dict([(sender, Counter()) for sender in msgList.senderList])
    for msg in msgList.msgList:
        if not msg.isMedia:
            for word in msg.content.split():
                tmp[msg.sender][word.lower()] +=1

    return tmp


############################################################            
def plotMostUsed(wordDict, title, yLabel='y'):
    x = [word for word, number in wordDict][::-1]
    y = [number for word, number in wordDict][::-1]
    
    _, ax = plt.subplots()  

    width = 0.75 # the width of the bars 
    ind = np.arange(len(y))  # the x locations for the groups
    ax.barh(ind, y, width, color="blue")
    ax.set_yticks(ind+width/2)
    ax.set_yticklabels(x, minor=False)
    for i, v in enumerate(y):
        ax.text(v + 3, i + .25, str(v), color='blue', fontweight='bold')
    plt.title("Top {} {}".format(len(x), title) )
    plt.xlabel('Count', fontsize=16)
    plt.ylabel(yLabel, fontsize=16) 

    plt.tick_params(labelsize=16)

    for tick in ax.get_yticklabels():
        tick.set_fontname("Segoe UI Emoji")