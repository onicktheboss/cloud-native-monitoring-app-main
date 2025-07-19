from flask import Flask, Response
import psutil
from prometheus_client import CollectorRegistry, Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

@app.route("/metrics")
def metrics():
    registry = CollectorRegistry()
    cpu = Gauge('cpu_usage_percent', 'CPU usage in percent', registry=registry)
    memory = Gauge('memory_usage_percent', 'Memory usage in percent', registry=registry)
    disk = Gauge('disk_usage_percent', 'Disk usage in percent', registry=registry)

    cpu.set(psutil.cpu_percent(interval=1))
    memory.set(psutil.virtual_memory().percent)
    disk.set(psutil.disk_usage('/').percent)

    return Response(generate_latest(registry), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)