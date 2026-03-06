from flask import Flask
from datetime import datetime, timezone
import os


app = Flask(__name__)

from . import auth
app.register_blueprint(auth.bp)

from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

app.config.from_pyfile('config.py')

@app.after_request
def add_vary_cookie(response):
    response.vary.add('Cookie')
    return response

@app.context_processor
def inject_now():
    return {'now': datetime.now(timezone.utc)}

import reader.main
