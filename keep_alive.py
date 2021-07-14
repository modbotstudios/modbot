from threading import Thread

from flask import Flask

app = Flask('')


@app.route('/')
def main():
    return "modbot is online"


def run():
    app.run(host="0.0.0.0", port=80)


def keep_alive():
    server = Thread(target=run)
    server.start()
