from flask import Flask
from flask import render_template
from flask_cors import CORS
from flask_mongoengine import MongoEngine
import logging, logging.config
import os
import config

__author__ = 'jacobgilsaa'

logging.config.fileConfig(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logging.conf'))
logger = logging.getLogger(__name__)

# Init app w. config
app = Flask(__name__)
for key, val in config.__CONFIGURATIONS__.iteritems():
    app.config[key] = val

# Enable Cross-relam requests
CORS(app)

# Init database client
db_client = MongoEngine(app)

# For deployment - Should only be used there..
@app.route("/")
def index():
    return render_template("index.html")

# Add the Blueprints
from app.user.UserView import mod_user as user_module
from app.task.TaskView import mod_task as task_module

app.register_blueprint(user_module)
app.register_blueprint(task_module)