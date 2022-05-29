# spudooli-reader
An RSS feed reader made by me, just for me. But it can be for you too, if you want.

Here is some minimal help to get you going, but you'll need to know how to install and configure Python, Flask, Mysql, nginx and do some DNS. 

Install Flask - https://flask.palletsprojects.com/en/2.1.x/installation/

I think the only additional Python things to install is...
```
pip3 install feedparser
pip3 install mysql-connector-python
pip3 install flask_mysqldb
```

There is a mysql dump in the bin directory to create your database that matches mine.

Add your feeds to the feeds table - I have no admin for that yet, possibly ever. I just use adminer.

Add a crontab entry to run update-feeds.py at an interval that suits you

Make a config.py that has something like and put it in reader/

```
from reader import app
app.config['SECRET_KEY'] = 'SecretTextGoesHere'
```

Follow some instructions somewhere on how to install and configure gunicorn - I did that in about 10 minutes o you can too.