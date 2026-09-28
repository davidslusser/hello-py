# app.py
import datetime
import os
import socket

from bottle import Bottle, run, template

app = Bottle()

# Record start time
process_start_time = datetime.datetime.now(datetime.UTC)
start_time: str = process_start_time.strftime("%Y-%m-%d %H:%M:%S UTC")

# Get environment variables
image_tag: str = os.getenv("IMAGE_TAG", "unknown")
hostname: str = socket.gethostname()


def get_uptime() -> str:
    """Return the elapsed process time in a human-readable format."""
    elapsed_seconds = int((datetime.datetime.now(datetime.UTC) - process_start_time).total_seconds())
    days, remainder = divmod(elapsed_seconds, 86_400)
    hours, remainder = divmod(remainder, 3_600)
    minutes, seconds = divmod(remainder, 60)

    if days:
        return f"{days}d {hours:02}h {minutes:02}m {seconds:02}s"
    return f"{hours:02}h {minutes:02}m {seconds:02}s"


@app.route("/")
def index() -> str:
    return template(
        """
        <html>
        <head>
            <style>
                body {
                    background: linear-gradient(135deg, #306998 0%, #4B8BBE 50%, #306998 100%);
                    color: #fff;
                    font-family: Arial, sans-serif;
                    min-height: 100vh;
                    margin: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
                .center-container {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                }
                ul { list-style-type: none; padding: 0; }
                li { 
                    margin-bottom: 24px; /* Increased spacing */
                    text-align: center; 
                }
                h1 { color: #fff; text-align: center; }
                strong {
                    color: #ffd43b; /* Python.org yellow */
                }
            </style>
        </head>
        <body>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.2/css/all.min.css">
        <div class="center-container">
            <div style="font-size: 64px; margin-bottom: 20px;">
                <strong><i class="fa-brands fa-python"></i></strong>
            </div>
            <h1><strong>Hello Python!</strong></h1>
            <ul>
                <li><strong>Hostname:</strong><br/> {{hostname}}</li>
                <li><strong>Start Time:</strong><br/> {{start_time}}</li>
                <li><strong>Uptime:</strong><br/> {{uptime}}</li>
                <li><strong>Image Tag:</strong><br/> {{image_tag}}</li>
            </ul>
        </div>
        </body>
        </html>
        """,
        hostname=hostname,
        start_time=start_time,
        uptime=get_uptime(),
        image_tag=image_tag,
    )


@app.route("/api")
def api() -> dict[str, str]:
    return {
        "hostname": socket.gethostname(),
        "start_time": start_time,
        "uptime": get_uptime(),
        "version": image_tag,
    }


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
