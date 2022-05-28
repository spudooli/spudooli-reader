from reader import app
from flask_mysqldb import MySQL

mysql = MySQL()

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'bobthefish'
app.config['MYSQL_DB'] = 'reader'

mysql = MySQL(app)