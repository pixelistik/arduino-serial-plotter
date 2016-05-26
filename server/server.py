from flask import Flask, Response
from random import randint
from time import sleep

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'hello world!'


@app.route("/stream")
def stream():
    def eventStream():
        while True:
            result = randint(0, 99)
            sleep(1)
            #yield "data: %d\n\n" % result
            yield "data: some%s\n\n" % result
    return Response(eventStream(), mimetype="text/event-stream")

def main():
    app.debug = True
    app.run()

if __name__ == "__main__":
    main()
