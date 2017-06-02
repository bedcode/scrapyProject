import html2text
import json
import os
import requests

for filename in os.listdir(os.getcwd()):
    if (filename == 'htmlParser.py'):
        continue
    f = open(filename, 'r')
    data = json.load(f)
    url = 'https://twitter.com' + data['url']
    user_agent = {'user-agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:53.0) Gecko/20100101 Firefox/53.0'}
    r = requests.get(url, headers = user_agent)
    text = r.text
    start = text.find('<p class="TweetTextSize TweetTextSize--jumbo js-tweet-text tweet-text"')
    t = text[start:]
    end = t.find('</p>')
    t = t[:end]
    parseText = html2text.html2text(t)
    print(parseText)
