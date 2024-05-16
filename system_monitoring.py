from flask import Flask
from flask_sock import Sock
from time import sleep
import psutil
from datetime import datetime

app = Flask(__name__)
sock = Sock(app)

@sock.route('/connect')
def handle_connect(ws):
    while True:
        system_usage = {
            'cpu_usage': psutil.cpu_percent(interval=1),
            'memory_usage': psutil.virtual_memory().used / (1024 * 1024), # Memory usage in MB
            'storage_usage': psutil.disk_usage('/').used / (1024 * 1024 * 1024),  # Storage usage in GB
            'time': datetime.now().time().strftime("%H:%M:%S")
        }
        ws.send(system_usage)
        sleep(1)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080, debug=True)
