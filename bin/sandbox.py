import hashlib
import feedparser
import ssl
from datetime import datetime
from time import strftime



def processrss(url, feed_title, feedid):
    # try:
    print("ping")
    feed = feedparser.parse(url)
    for entry in feed["entries"]:
        title = entry.get("title")
        link = entry.get("link")
        urlhash = hashlib.md5(link.encode())
        description = entry.get("description")
        #print(description)
        if entry.get("content"):
            description = entry.get("content")[0]["value"]
        #description = entry.get('content', [{}])[0].get('value', '')
        published = entry.get("published_parsed")
        print(description)
        #published = datetime.strptime(str(published), '%a, %d %b %Y %H:%M:%S %z')
        published = strftime("%Y-%m-%d %H:%M:%S", published)
        print(published)
        dateUpdated = datetime.now()
        print(title)

processrss("https://www.raspberrypi.org/feed/", "Raspberry Pi", 1)
