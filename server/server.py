# author: oskar.blom@gmail.com
#
# Make sure your gevent version is >= 1.0
import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue
from random import randint
from gevent import sleep
import serial

from flask import Flask, Response, render_template

# SSE "protocol" is described here: http://mzl.la/UPFyxY
class ServerSentEvent(object):

    def __init__(self, data):
        self.data = data
        self.event = None
        self.id = None
        self.desc_map = {
            self.data : "data",
            self.event : "event",
            self.id : "id"
        }

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k)
                 for k, v in self.desc_map.iteritems() if k]

        return "%s\n\n" % "\n".join(lines)

app = Flask(__name__)
subscriptions = []
serialListener = None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/subscribe")
def subscribe():
    def notify():
        while True:
            with serial.Serial('/dev/pts/11') as ser:
                msg = ser.readline()
                for sub in subscriptions[:]:
                    sub.put(msg)
                sleep(0)

    global serialListener
    if not serialListener:
        serialListener = gevent.spawn(notify)

    def gen():
        q = Queue()
        subscriptions.append(q)
        try:
            while True:
                result = q.get()
                ev = ServerSentEvent(str(result))
                yield ev.encode()
        except GeneratorExit:
            subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")

def main():
    app.debug = True
    server = WSGIServer(("", 5000), app)
    server.serve_forever()

if __name__ == "__main__":
    main()
