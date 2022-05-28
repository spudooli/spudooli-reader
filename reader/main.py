from reader import app, db
from flask import render_template, redirect, url_for, request, flash
from datetime import date


@app.route("/")
def index():
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT `id`, `title`, `url`, `content`, `haveread`, `feed_title`, `date_published` FROM `feed_items` WHERE `haveread` IS NULL ORDER BY `date_published` DESC",)
    newsitems = cursor.fetchall()
    cursor.close()

    # Get a count of the items that have not been read grouped by feed title
    cursor = db.mysql.connection.cursor()
    cursor.execute(
        "SELECT `feed_title`, COUNT(id) id FROM `feed_items` WHERE `haveread` IS NULL GROUP BY `feed_title`")
    unreadcounts = cursor.fetchall()

    return render_template('index.html', newsitems=newsitems, unreadcounts=unreadcounts)


@app.route("/read", methods=['POST'])
def read():
    request_data = request.get_json()
    print(request_data)
    itemid = request_data['feedid']
    print(itemid)
    cursor = db.mysql.connection.cursor()
    cursor.execute(
        "UPDATE `feed_items` SET `haveread` = '1' WHERE `id` = %s", (itemid,))
    db.mysql.connection.commit()
    cursor.close()
    return "ok"


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
