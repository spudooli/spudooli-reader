from reader import app, db
from flask import render_template, request, send_from_directory
from datetime import date
from reader.auth import login_required


@app.route("/")
@login_required
def index():
    cursor = db.mysql.connection.cursor()
    cursor.execute("SELECT `id`, `title`, `url`, `content`, `haveread`, `feed_title`, `date_published`, feed_id FROM `feed_items` WHERE `haveread` IS NULL ORDER BY `date_published` ASC",)
    newsitems = cursor.fetchall()
    cursor.close()

    # Get a count of the items that have not been read grouped by feed title
    cursor = db.mysql.connection.cursor()
    cursor.execute(
        "SELECT `feed_title`, COUNT(id) id, feed_id FROM `feed_items` WHERE `haveread` IS NULL GROUP BY `feed_title`, feed_id ")
    unreadcounts = cursor.fetchall()

    return render_template('index.html', newsitems=newsitems, unreadcounts=unreadcounts)


@app.route("/read", methods=['POST'])
def read():
    request_data = request.get_json()
    itemid = request_data['feed']
    cursor = db.mysql.connection.cursor()
    cursor.execute(
        "UPDATE `feed_items` SET `haveread` = '1' WHERE `id` = %s", (itemid,))
    db.mysql.connection.commit()
    cursor.close()

    return "ok"


@app.route("/unreadcount")
def unreadcount():
    cursor = db.mysql.connection.cursor()
    cursor.execute(
        "SELECT COUNT(id) id FROM `feed_items` WHERE haveread IS NULL")
    unreadcount = cursor.fetchone()
    if unreadcount[0] == 0:
        unreadcount = " "
    else:
        unreadcount = str(unreadcount[0])
    cursor.close()

    return unreadcount


@app.route("/readinglist")
def readinglist():
    cursor = db.mysql.connection.cursor()
    cursor.execute(
        "SELECT `id`, `title`, `websiteurl`FROM `feeds`ORDER BY `id` ASC",)
    readinglist = cursor.fetchall()
    cursor.close()

    return render_template('readinglist.html', readinglist=readinglist)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500
