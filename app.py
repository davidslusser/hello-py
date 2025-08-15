# app.py
import datetime
import os
import socket

from bottle import Bottle, run, template

app = Bottle()

# Record start time
start_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

# Get environment variables
image_tag = os.getenv("IMAGE_TAG", "unknown")
hostname = socket.gethostname()


@app.route("/")
def index():
    return template(
        """
        <h1>App Info</h1>
        <ul>
            <li><strong>Hostname:</strong> {{hostname}}</li>
            <li><strong>Start Time:</strong> {{start_time}}</li>
            <li><strong>Image Tag:</strong> {{image_tag}}</li>
        </ul>
    """,
        hostname=hostname,
        start_time=start_time,
        image_tag=image_tag,
    )


@app.route("/api")
def api():
    return {
        "hostname": socket.gethostname(),
        "start_time": start_time,
        "version": image_tag,
    }


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
