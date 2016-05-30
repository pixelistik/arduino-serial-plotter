# author: oskar.blom@gmail.com
#
# Make sure your gevent version is >= 1.0
import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue
from random import randint
from gevent import sleep

from flask import Flask, Response, render_template

# import time


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

# Client code consumes like this.
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/debug")
def debug():
    return "Currently %d subscriptions" % len(subscriptions)

@app.route("/publish")
def publish():
    #Dummy data - pick up from request for real data
    def notify():
        msg = str(randint(0,100))
        for sub in subscriptions[:]:
            sub.put(msg)

    gevent.spawn(notify)

    return "OK"

@app.route("/subscribe")
def subscribe():
    #Dummy data - pick up from request for real data
    def notify():
        while True:
            msg = str(randint(0,100))
            for sub in subscriptions[:]:
                sub.put(msg)
            sleep(1)

    global serialListener
    if not serialListener:
        serialListener = gevent.spawn(notify)

    def gen():
        q = Queue()
        subscriptions.append(q)
        try:
            while True:
                result = q.get()
                print "seinding"
                # sleep(1)
                # ev = ServerSentEvent(str(randint(0,100)))
                ev = ServerSentEvent(str(result))
                yield ev.encode()
        except GeneratorExit: # Or maybe use flask signals
            subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")

def main():
    app.debug = True
    server = WSGIServer(("", 5000), app)
    server.serve_forever()
    # Then visit http://localhost:5000 to subscribe
    # and send messages by visiting http://localhost:5000/publish

if __name__ == "__main__":
    main()
