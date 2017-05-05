from flask import Flask

# Create the Flask app
app = Flask(__name__, template_folder='./static')
app.config.from_object('config')

import server
