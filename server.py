from flask import Flask, render_template, request, jsonify
import subprocess
import threading
import os
import signal
import pyuac

app = Flask(__name__)

# Global variables to hold the server process and its output
minecraft_server_process = None
output_log = []


@app.route("/")
def index():
    return render_template("index.html")


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
        return jsonify(status="already_running", server_running=False)


@app.route("/stop_server", methods=["POST"])
def stop_server():
    global minecraft_server_process

    if minecraft_server_process is not None:
        os.system("taskkill /f /pid " + str(minecraft_server_process.pid))
        return jsonify(status="stopped", server_running=False)
    else:
        return jsonify(status="not_running", server_running=True)


@app.route("/send_command", methods=["POST"])
def send_command():
    global minecraft_server_process
    command = request.form["command"]

    if minecraft_server_process is not None:
        if command.find("stop") == -1:
            minecraft_server_process.stdin.write(command + "\n")
            minecraft_server_process.stdin.write("\n")
            return jsonify(status="not_running", server_running=False)
        else:
            minecraft_server_process.stdin.write(command + "\n")
            minecraft_server_process.stdin.flush()
            return jsonify(status="command_sent", server_running=True)
    else:
        return jsonify(status="not_running", server_running=False)


@app.route("/get_output", methods=["GET"])
def get_output():
    global output_log
    return jsonify(
        output=output_log, server_running=(minecraft_server_process is not None)
    )


def read_output():
    global minecraft_server_process, output_log
    while minecraft_server_process is not None:
        output = minecraft_server_process.stdout.readline()
        if output:
            output_log.append(output)
            if len(output_log) > 100:
                output_log = output_log[-100:]


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
