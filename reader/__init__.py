from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

import reader.main
