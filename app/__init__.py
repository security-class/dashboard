from flask import Flask

# Create the Flask app
app = Flask(__name__)
app.config.from_object('config')

import server
