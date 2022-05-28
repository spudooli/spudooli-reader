import mysql.connector
import hashlib
import feedparser
import ssl
from datetime import datetime
from time import strftime

feedparser.USER_AGENT = "Spudooli Reader/1.0 - 1 subscribers - https:/www.spudooli.com"

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bobthefish",
    database="reader",
)


def processrss(url, feed_title, feedid):
    # try:
    feed = feedparser.parse(url)
    cursor = connection.cursor(buffered = True)
    for entry in feed["entries"]:
        title = entry.get("title")
        link = entry.get("link")
        urlhash = hashlib.md5(link.encode())
        description = entry.get("description")
        published = entry.get("published_parsed")

        #published = datetime.strptime(str(published), '%a, %d %b %Y %H:%M:%S %z')
        published = strftime("%Y-%m-%d %H:%M:%S", published)
        print(published)
        dateUpdated = datetime.now()
        print(title)
        cursor.execute(
            "INSERT INTO feed_items (title, url, urlhash, content, feed_title, date_published, date_updated, feed_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (title, link, urlhash.hexdigest(), description, feed_title, published, dateUpdated, feedid))

        connection.commit()
    

    # Update the feed's last updated date
    dateUpdated = datetime.now()
    mysql_insert_query = "update feeds set last_checked = %s where id = %s"
    values = (dateUpdated, feedid)
    cursor.execute(mysql_insert_query, values)
    connection.commit()

    # except Exception as e:
    #     print(e)
    #     pass

# Get feeds from the database and process them
cursor = connection.cursor(buffered = True)
cursor.execute("SELECT id, feedurl, title FROM feeds")

for row in cursor:
    print(f'Processing feed {row[1]}')
    processrss(row[1], row[2], row[0])
