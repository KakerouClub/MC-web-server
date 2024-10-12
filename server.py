from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    session,
    flash,
    redirect,
    url_for,
)
import subprocess
import threading
import os
import json
from time import strftime
import logging
from logging.handlers import RotatingFileHandler
from flask_session import Session
from pymongo import MongoClient
from flask import Response
import time
from flask_pymongo import PyMongo

app = Flask(__name__)
app.secret_key = """
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠛⠛⠋⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠙⠛⠛⠛⠿⠻⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⠀⠀⠀⡀⠠⠤⠒⢂⣉⣉⣉⣑⣒⣒⠒⠒⠒⠒⠒⠒⠒⠀⠀⠐⠒⠚⠻⠿⠿⣿⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⡠⠔⠉⣀⠔⠒⠉⣀⣀⠀⠀⠀⣀⡀⠈⠉⠑⠒⠒⠒⠒⠒⠈⠉⠉⠉⠁⠂⠀⠈⠙⢿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠇⠀⠀⠀⠔⠁⠠⠖⠡⠔⠊⠀⠀⠀⠀⠀⠀⠀⠐⡄⠀⠀⠀⠀⠀⠀⡄⠀⠀⠀⠀⠉⠲⢄⠀⠀⠀⠈⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⠋⠀⠀⠀⠀⠀⠀⠀⠊⠀⢀⣀⣤⣤⣤⣤⣀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠜⠀⠀⠀⠀⣀⡀⠀⠈⠃⠀⠀⠀⠸⣿⣿⣿⣿
⣿⣿⣿⣿⡿⠥⠐⠂⠀⠀⠀⠀⡄⠀⠰⢺⣿⣿⣿⣿⣿⣟⠀⠈⠐⢤⠀⠀⠀⠀⠀⠀⢀⣠⣶⣾⣯⠀⠀⠉⠂⠀⠠⠤⢄⣀⠙⢿⣿⣿
⣿⡿⠋⠡⠐⠈⣉⠭⠤⠤⢄⡀⠈⠀⠈⠁⠉⠁⡠⠀⠀⠀⠉⠐⠠⠔⠀⠀⠀⠀⠀⠲⣿⠿⠛⠛⠓⠒⠂⠀⠀⠀⠀⠀⠀⠠⡉⢢⠙⣿
⣿⠀⢀⠁⠀⠊⠀⠀⠀⠀⠀⠈⠁⠒⠂⠀⠒⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠀⢀⣀⡠⠔⠒⠒⠂⠀⠈⠀⡇⣿
⣿⠀⢸⠀⠀⠀⢀⣀⡠⠋⠓⠤⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠀⠀⠀⠀⠀⠀⠈⠢⠤⡀⠀⠀⠀⠀⠀⠀⢠⠀⠀⠀⡠⠀⡇⣿
⣿⡀⠘⠀⠀⠀⠀⠀⠘⡄⠀⠀⠀⠈⠑⡦⢄⣀⠀⠀⠐⠒⠁⢸⠀⠀⠠⠒⠄⠀⠀⠀⠀⠀⢀⠇⠀⣀⡀⠀⠀⢀⢾⡆⠀⠈⡀⠎⣸⣿
⣿⣿⣄⡈⠢⠀⠀⠀⠀⠘⣶⣄⡀⠀⠀⡇⠀⠀⠈⠉⠒⠢⡤⣀⡀⠀⠀⠀⠀⠀⠐⠦⠤⠒⠁⠀⠀⠀⠀⣀⢴⠁⠀⢷⠀⠀⠀⢰⣿⣿
⣿⣿⣿⣿⣇⠂⠀⠀⠀⠀⠈⢂⠀⠈⠹⡧⣀⠀⠀⠀⠀⠀⡇⠀⠀⠉⠉⠉⢱⠒⠒⠒⠒⢖⠒⠒⠂⠙⠏⠀⠘⡀⠀⢸⠀⠀⠀⣿⣿⣿
⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠑⠄⠰⠀⠀⠁⠐⠲⣤⣴⣄⡀⠀⠀⠀⠀⢸⠀⠀⠀⠀⢸⠀⠀⠀⠀⢠⠀⣠⣷⣶⣿⠀⠀⢰⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠁⢀⠀⠀⠀⠀⠀⡙⠋⠙⠓⠲⢤⣤⣷⣤⣤⣤⣤⣾⣦⣤⣤⣶⣿⣿⣿⣿⡟⢹⠀⠀⢸⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣧⡀⠀⠀⠀⠀⠀⠀⠀⠑⠀⢄⠀⡰⠁⠀⠀⠀⠀⠀⠈⠉⠁⠈⠉⠻⠋⠉⠛⢛⠉⠉⢹⠁⢀⢇⠎⠀⠀⢸⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣀⠈⠢⢄⡉⠂⠄⡀⠀⠈⠒⠢⠄⠀⢀⣀⣀⣰⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⢀⣎⠀⠼⠊⠀⠀⠀⠘⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⡀⠉⠢⢄⡈⠑⠢⢄⡀⠀⠀⠀⠀⠀⠀⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠁⠀⠀⢀⠀⠀⠀⠀⠀⢻⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣀⡈⠑⠢⢄⡀⠈⠑⠒⠤⠄⣀⣀⠀⠉⠉⠉⠉⠀⠀⠀⣀⡀⠤⠂⠁⠀⢀⠆⠀⠀⢸⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄⡀⠁⠉⠒⠂⠤⠤⣀⣀⣉⡉⠉⠉⠉⠉⢀⣀⣀⡠⠤⠒⠈⠀⠀⠀⠀⣸⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⣄⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣰⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣶⣶⣤⣤⣤⣤⣀⣀⣤⣤⣤⣶⣾⣿⣿⣿⣿⣿
"""
app.config["SESSION_TYPE"] = "mongodb"
app.config["SESSION_MONGODB"] = MongoClient(
    "mongodb+srv://test:pSvJpf5T51CJJWk2@mc-web-server.ags8p.mongodb.net/"
)
app.config["SESSION_MONGODB_DB"] = "web-server"
app.config["SESSION_MONGODB_COLLECT"] = "sessions"
Session(app)

app.config["MONGO_URI"] = (
    "mongodb+srv://test:pSvJpf5T51CJJWk2@mc-web-server.ags8p.mongodb.net/web-server"
)
mongo = PyMongo(app)

admin_pass = open("password.txt", "r")


minecraft_server_process = None
output_log = []
default_players = [
    {"name": "Radu", "wins": 3, "winrate": 0},
    {"name": "Sandu", "wins": 1, "winrate": 0},
    {"name": "George", "wins": 0, "winrate": 0},
]
log_lock = threading.Lock()


logger = logging.getLogger(__name__)
handler = RotatingFileHandler(
    "G:/MC servers/Divine Journey/web server/MC-web-server/logs/app.log",
    maxBytes=100000,
    backupCount=3,
)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


@app.route("/")
def index():
    if "logged_in" in session and session["logged_in"]:
        return redirect(url_for("control_panel"))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    password = request.form["password"]

    if password == admin_pass:
        session["logged_in"] = True
        return redirect(url_for("control_panel"))
    else:
        flash("Incorrect password dumbfuck. Try again or get out")
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("index"))


@app.route("/control_panel", methods=["GET"])
def control_panel():
    if "logged_in" in session and session["logged_in"]:
        return render_template("index.html")
    return redirect(url_for("index"))


@app.route("/start_server", methods=["POST"])
def start_server():
    global minecraft_server_process

    if minecraft_server_process is None:
        minecraft_server_process = subprocess.Popen(
            ["launch.bat"],
            cwd="G:\\MC servers\\Divine Journey\\",
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            stdin=subprocess.PIPE,
            shell=True,
            text=True,
        )
        threading.Thread(target=read_output).start()
        return jsonify(status="started", server_running=True)
    else:
        return jsonify(status="already_running", server_running=True)


@app.route("/stop_server", methods=["POST"])
def stop_server():
    global minecraft_server_process

    if minecraft_server_process is not None:
        os.system("taskkill /f /pid " + str(minecraft_server_process.pid))
        minecraft_server_process = None
        return jsonify(status="stopped", server_running=False)
    else:
        return jsonify(status="not_running", server_running=False)


@app.route("/send_command", methods=["POST"])
def send_command():
    global minecraft_server_process
    command = request.form["command"]

    if minecraft_server_process is not None:
        minecraft_server_process.stdin.write(command + "\n")
        minecraft_server_process.stdin.flush()

        if command.lower().find("stop") != -1 and command.lower().find("debug") == -1:
            minecraft_server_process.communicate("SERVER CLOSED")[0]
            minecraft_server_process = None

        return jsonify(status="command_sent", server_running=True)
    else:
        return jsonify(status="not_running", server_running=False)


@app.route("/get_output", methods=["GET"])
def get_output():
    global output_log
    with log_lock:
        output_copy = output_log[-100:]
    return jsonify(
        output=output_copy, server_running=(minecraft_server_process is not None)
    )


@app.after_request
def after_request(response):
    timestamp = strftime("[%Y-%b-%d %H:%M]")
    logger.info(
        "%s %s %s %s %s %s",
        timestamp,
        request.remote_addr,
        request.method,
        request.scheme,
        request.full_path,
        response.status,
    )
    return response


def read_output():
    global minecraft_server_process, output_log
    while minecraft_server_process is not None:
        output = minecraft_server_process.stdout.readline()
        if output:
            with log_lock:
                if "get_output" not in output:
                    output_log.append(output.strip())
                    if len(output_log) > 100:
                        output_log = output_log[-100:]
        if minecraft_server_process.poll() is not None:
            break
    minecraft_server_process = None


@app.route("/stream_output")
def stream_output():
    def event_stream():
        while True:
            time.sleep(1)
            with log_lock:
                output_copy = output_log[-100:]
            yield f"data: {json.dumps({'output': output_copy, 'server_running': minecraft_server_process is not None})}\n\n"

    return Response(event_stream(), content_type="text/event-stream")


@app.route("/get_player_data", methods=["GET"])
def get_player_data():
    player_collection = mongo.db.players
    players = list(player_collection.find())

    if not players:
        player_collection.insert_many(default_players)
        players = list(player_collection.find())

    totalGames = sum(player["wins"] for player in players)

    for player in players:
        player["_id"] = str(player["_id"])
        if totalGames > 0:
            player["winrate"] = (player["wins"] / totalGames) * 100
        else:
            player["winrate"] = 0

    return jsonify(players)


@app.route("/save_player_data", methods=["POST"])
def save_player_data():
    player_collection = mongo.db.players
    data = request.json

    for player in data:
        player_collection.update_one(
            {"name": player["name"]}, {"$set": {"wins": player["wins"]}}
        )

    return jsonify({"status": "success"})


@app.route("/stats")
def stats():
    return render_template("stats.html")
