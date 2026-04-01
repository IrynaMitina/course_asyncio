"""dummy flask (sync) server. 

install dependencies:
$ pip install flask
run server with:
$ python server_flask.py
send requests to 
runs on http://127.0.0.1:8001/

"""

from time import sleep
from flask import Flask

app = Flask(__name__)

@app.route("/")
def status():
    sleep(3)  # here can be sync call to database to obtain status 
    return {"status": "io ok"}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8001)
