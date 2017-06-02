import html2text
import json
import os
import requests

for filename in os.listdir(os.getcwd()):
    if (filename == 'htmlParser.py'):
        continue
    # open all files in current directory except the parser
    f = open(filename, 'r')
    data = json.load(f)
    f.close()

    # complete url
    url = 'https://twitter.com' + data['url']
    # fake user agent = Mozilla Firefox on Linux machine
    user_agent = {'user-agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'}
    r = requests.get(url, headers = user_agent)
    # transform HTML page in text
    text = r.text

    # search for the text of the tweet
    start = text.find('<p class="TweetTextSize TweetTextSize--jumbo js-tweet-text tweet-text"')
    t = text[start:]
    if t == 1:
        continue
    end = t.find('</p>')
    t = t[:end]
    if t == 1:
        continue
    parseText = html2text.html2text(t)
    print(parseText)
