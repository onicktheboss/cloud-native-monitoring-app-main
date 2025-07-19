import subprocess
import time
import webbrowser

def run(cmd, show_output=True):
    print(f"🛠️  Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if show_output:
        print(result.stdout)
    if result.stderr:
        print(f"⚠️  Error: {result.stderr}")
    return result

def wait_for_pod(label):
    print(f"⏳ Waiting for {label} pod to be ready...")
    run(f"kubectl wait --for=condition=ready pod -l app={label} --timeout=90s")

def open_service(name):
    print(f"🌐 Opening {name}...")
    url = subprocess.getoutput(f"minikube service {name} --url")
    webbrowser.open(url)

# ---- Execution ----
print("🚀 Starting Full Monitor Setup")
run("minikube start")

print("📦 Applying all manifests...")
manifests = [
    "k8s/deployment.yaml",
    "k8s/service.yaml",
    "k8s/prometheus-config.yaml",
    "k8s/prometheus-deployment.yaml",
    "k8s/prometheus-service.yaml",
    "k8s/grafana-deployment.yaml",
    "k8s/grafana-service.yaml"
]
for file in manifests:
    run(f"kubectl apply -f {file}")

wait_for_pod("resource-monitor")
wait_for_pod("prometheus")
wait_for_pod("grafana")

open_service("prometheus-service")
open_service("grafana-service")

print("✅ All systems go! Enjoy your dashboard.")