import mysql.connector
import hashlib
import feedparser
import ssl
from datetime import datetime
from time import strftime

feedparser.USER_AGENT = "Spudooli Reader/1.0 - 1 subscribers - https://www.spudooli.com"

if hasattr(ssl, '_create_unverified_context'):
    ssl._create_default_https_context = ssl._create_unverified_context

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bobthefish",
    database="reader",
)


def processrss(url, feed_title, feedid):
    """
    Download the rss feed, break it up and stuff it into the database
    """
    try:
        feed = feedparser.parse(url)
        cursor = connection.cursor(buffered = True)
        feeditemcount = len(feed["entries"])
        for entry in feed["entries"]:
            title = entry.get("title")
            link = entry.get("link")
            urlhash = hashlib.md5(link.encode())
            description = entry.get("description")
            if entry.get("content"):
                description = entry.get("content")[0]["value"]
            # TODO Fix for my timezone
            published = entry.get("published_parsed")
            published = strftime("%Y-%m-%d %H:%M:%S", published)
            dateUpdated = datetime.now()
            print(f'       {title}')
            cursor.execute(
                "INSERT ignore INTO feed_items (title, url, urlhash, content, feed_title, date_published, date_updated, feed_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (title, link, urlhash.hexdigest(), description, feed_title, published, dateUpdated, feedid))

            connection.commit()


        # Update the feed's last updated date
        dateUpdated = datetime.now()
        mysql_insert_query = "update feeds set last_checked = %s, feed_item_count = %s where id = %s"
        values = (dateUpdated, feeditemcount, feedid)
        cursor.execute(mysql_insert_query, values)
        connection.commit()

    except Exception as e:
        print(e)
        print("Error processing feed: --------------------------------------------" + url)
        cursor.close()
        return

def cleanupfeeditems(feedid, feedItemCount):
    """
    Cleans up feed_items, removing any items older than what the RSS feed provides
    """
    cursor = connection.cursor(buffered = True)
    deletefrom = "DELETE FROM feed_items WHERE feed_id = %s and id NOT IN (select id from (SELECT id, feed_id FROM feed_items where feed_id = %s ORDER BY id DESC LIMIT %s) foo)"
    cursor.execute(deletefrom, (feedid, feedid, feedItemCount))
    connection.commit()
    cursor.close()


if __name__ == "__main__":

    # Get feeds from the database and process them
    cursor = connection.cursor(buffered = True)
    cursor.execute("SELECT id, feedurl, title FROM feeds")
    for row in cursor:
        print(row[1])
        processrss(row[1], row[2], row[0])


    #Get the feeds to cleanup old feeditems
    cursor = connection.cursor(buffered = True)
    cursor.execute("SELECT id, feed_item_count FROM feeds")

    for row in cursor:
        print(row[1])
        cleanupfeeditems(row[0], row[1])