from flask import *
from threading import Thread

flask = Flask(__name__)


@flask.route("/")
def index():
    return "Hi!"


def run():
    flask.run()


def keep_alive():
    t = Thread(target=run)
    t.start()
