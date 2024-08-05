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

@sock.route('/system-status')
def handle_connect2(ws):
    while True:
        system_usage = {}

        memory = psutil.virtual_memory()
        network = psutil.net_io_counters()
        disk = psutil.disk_usage('/')
        time_ = datetime.now().time().strftime("%H:%M:%S")

        total_memory = memory.total / (1024 ** 2) ##MB
        memory_usage = memory.used / (1024 ** 2)

        network_sent = network.bytes_sent / (1024 ** 2)  ##MB
        network_recev = network.bytes_recv / (1024 ** 2) 

        total_disk = disk.total / (1024 ** 3)  #GB
        disk_usage = disk.used / (1024 ** 3)    # 

        system_usage['cpu'] = {
            'used': psutil.cpu_percent(interval=1), 
            'total': 100, 
            'unit': '%'}
        
        system_usage['memory'] = {
            'used': memory_usage,
            'total':total_memory,
            'unit': 'MB'
        }
        system_usage['network'] = {
            'send' : network_sent, 
            'received':network_recev,
            'unit': 'MB'

        }
        system_usage['disk'] = {
            'used': disk_usage,
            'total':total_disk,
            'unit': 'GB'
        }

        system_usage['time'] = time_

        
        ws.send(system_usage)
        sleep(5)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080, debug=True)
