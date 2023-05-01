# =============================================================================
#
# Title: my_flask.py
#
# Author: Aidan
#
# Description: File to host a flask web application to keep the bot online at all times
# Source: https://docs.replit.com/tutorials/python/build-basic-discord-bot-python
#
# =============================================================================

from flask import Flask
from threading import Thread

app = Flask('')


@app.route('/')
def main():
    return 'Bot is alive'


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    server = Thread(target=run)
    server.start()
