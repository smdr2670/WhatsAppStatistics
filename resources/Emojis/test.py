import sys
import requests
import re
import base64
import emoji


class EmojiConverter:
    def __init__(self):

        self.data = requests.get('https://unicode.org/emoji/charts/full-emoji-list.html').text
    def to_base64_png(self, emoji, version=0):
        """For different versions, you can set version = 0 for , """
        html_search_string = r"<img alt='{}' class='imga' src='data:image/png;base64,([^']+)'>" #'
        matchlist = re.findall(html_search_string.format(emoji), self.data)
        if matchlist:
            return matchlist[version]
        else:
            return None

e = EmojiConverter()

for key in emoji.UNICODE_EMOJI:
    filename = str(emoji.UNICODE_EMOJI[key]).strip(':')
    fullName = "C:\\Users\\Daniel\\Desktop\\PythonTest\\" + filename + ".jpg"
    print(filename)
    data = e.to_base64_png(key)
    if data is not None:
        imgdata = base64.b64decode(data)
        with open(fullName, 'wb') as f:
            f.write(imgdata)
