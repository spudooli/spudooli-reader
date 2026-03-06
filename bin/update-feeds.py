import mysql.connector
import hashlib
import feedparser
import logging
import requests
from datetime import datetime
import pytz


logging.basicConfig(filename='/tmp/update-feeds.log', encoding='utf-8', level=logging.DEBUG)

feedparser.USER_AGENT = "Spudooli Reader/1.0 - 1 subscribers - https://reader.spudooli.com/about"


connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bobthefish",
    database="reader",
)

def get_bluesky_embed_code(bluesky_post_url):
    # This function fetches the embed code for a Bluesky post
    api_url = f"https://embed.bsky.app/oembed?url={bluesky_post_url}"
    session = requests.Session()
    session.trust_env = False
    response = session.get(api_url)
    if response.status_code == 200:
        embed_code = response.json().get('html')
        return embed_code
    else:
        raise Exception(f"Failed to fetch embed code: {response.status_code}")

def processrss(url, feed_title, feedid):
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
            published_parsed = entry.get("published_parsed")
            updated_parsed = entry.get("updated_parsed")
            if updated_parsed:
                published_parsed = updated_parsed

            if published_parsed:
                dt_utc = datetime(*published_parsed[:6], tzinfo=pytz.utc)
                nz_tz = pytz.timezone('Pacific/Auckland')
                dt_nz = dt_utc.astimezone(nz_tz)
                published = dt_nz.strftime("%Y-%m-%d %H:%M:%S")
            else:
                 nz_tz = pytz.timezone('Pacific/Auckland')
                 published = datetime.now(nz_tz).strftime("%Y-%m-%d %H:%M:%S")
            dateUpdated = datetime.now()
            print(f'       {title}')
            # if the link includes bluesky url, get the embed code
            if 'bsky.app' in link:
                # first check if the post is already in the database so that we don't fetch the embed code again
                cursor.execute("SELECT id FROM feed_items WHERE url = %s", (link,))
                if cursor.rowcount > 0:
                    # skip this item if it's already in the database
                    continue
                else:
                    embed_code = get_bluesky_embed_code(link)
                    description = f"{embed_code}"
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
    # Cleans up feed_items, removing any items older than what the RSS feed provides
    """
    # multiply the feeditem count to give some overhead, just in case
    feedItemCount = int(feedItemCount) * 5
    logging.debug(f"feedid - {feedid},  feeditemcount - {feedItemCount}")
    cursor = connection.cursor(buffered = True)
    deletefrom = "DELETE fi FROM feed_items fi LEFT JOIN (SELECT id FROM feed_items WHERE feed_id = %s AND star IS NULL ORDER BY id DESC LIMIT %s) AS to_keep ON fi.id = to_keep.id WHERE fi.feed_id = %s AND fi.star IS NULL AND to_keep.id IS NULL;"
    cursor.execute(deletefrom, (feedid, feedItemCount, feedid))
    connection.commit()
    cursor.close()


def deleteboingboingads():
    cursor = connection.cursor(buffered = True)
    cursor.execute("UPDATE `feed_items` SET `haveread` = '1' WHERE `feed_id` = '86' and content like '%<strong>TL;DR%'")
    connection.commit()
    cursor.close()


if __name__ == "__main__":
    # Get feeds from the database and process them
    cursor = connection.cursor(buffered = True)
    cursor.execute("SELECT id, feedurl, title FROM feeds where blue_processor IS NULL")
    for row in cursor:
        print(row[1])
        processrss(row[1], row[2], row[0])

    #Get the feeds to cleanup old feeditems
    cursor = connection.cursor(buffered = True)
    cursor.execute("SELECT id, feed_item_count FROM feeds")
    for row in cursor:
        print(row[1])
        logging.debug(row)
        if int(row[1]) > 0:
            cleanupfeeditems(row[0], row[1])
    
    # Delete Boing Boing ads
    deleteboingboingads()

    
