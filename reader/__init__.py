from flask import Flask
from datetime import datetime


app = Flask(__name__)

from . import auth
app.register_blueprint(auth.bp)

app.config.from_pyfile('config.py')

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}



import reader.main
