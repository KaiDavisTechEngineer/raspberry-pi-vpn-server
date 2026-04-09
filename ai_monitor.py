"""
AI Network Anomaly Detection System
Author: Kai Davis
Description: Detects unusual network activity using anomaly detection on a Raspberry Pi.
"""
import psutil
import time
import pandas as pd
import datetime
from sklearn.ensemble import IsolationForest

# === TUNING SETTINGS ===
SPIKE_THRESHOLD = 4
HIGH_THRESHOLD = 6
MIN_TRAFFIC = 10000
WINDOW_SIZE = 20

samples = []

print("Collecting baseline traffic data...")

old = psutil.net_io_counters()

for i in range(20):
    time.sleep(5)
    new = psutil.net_io_counters()

    sent = new.bytes_sent - old.bytes_sent
    recv = new.bytes_recv - old.bytes_recv

    samples.append([sent, recv])
    print(f"Baseline sample {i+1}/20 -> Sent: {sent}, Recieved: {recv}")

    old = new

df = pd.DataFrame(samples, columns=["sent", "recv"])

model = IsolationForest(contamination=0.02, random_state=42)
model.fit(df)

mean_sent = df["sent"].mean()
mean_recv = df["recv"].mean()
std_sent = df["sent"].std()
std_recv = df["recv"].std()

# === PROTECTION AGAINST ZERO STD ===
if pd.isna(std_sent) or std_sent ==0:
    std_sent = 1
if pd.isna(std_recv) or std_recv == 0:
    std_recv = 1
print("\nAI monitoring started...\n")

while True:
    time.sleep(5)

    new = psutil.net_io_counters()

    sent = new.bytes_sent - old.bytes_sent
    recv = new.bytes_recv - old.bytes_recv

    samples.append([sent, recv])
    if len(samples) < 10:
        old = new
        continue

    if len(samples) > WINDOW_SIZE:
        samples.pop(0)

    df = pd.DataFrame(samples, columns=["sent", "recv"])

    mean_sent = df["sent"].mean()
    mean_recv = df["recv"].mean()
    std_sent = df["sent"].std()
    std_recv = df["recv"].std()

    # === PROTECTION AGAINST ZERO STD ===
    if pd.isna(std_sent) or std_sent ==0:
        std_sent = 1
    if pd.isna(std_recv) or std_recv == 0:
        std_recv = 1

    test_df = pd.DataFrame([[sent, recv]], columns=["sent", "recv"])

    prediction = model.predict(test_df)[0]

    print(f"Sent: {sent} | Received: {recv}")

    is_ai_anomaly = prediction == -1
    is_spike = (
        (
            sent > mean_sent + SPIKE_THRESHOLD* std_sent or
            recv > mean_recv + SPIKE_THRESHOLD * std_recv
        )
        and
        (
            sent > MIN_TRAFFIC or recv > MIN_TRAFFIC
        )
    )

    if is_ai_anomaly or is_spike:
        reason = []
        if is_ai_anomaly:
            reason.append("AI Anomaly")
        if is_spike:
            reason.append("Traffic Spike")
        if (
            sent > mean_sent + HIGH_THRESHOLD * std_sent or
            recv > mean_recv + HIGH_THRESHOLD * std_recv
        ):
            severity = "HIGH"
        else:
            severity = "MEDIUM"

        alert_msg = f"{datetime.datetime.now()} [{severity}] ALERT ({', '.join(reason)}): Sent={sent}, Recv={recv}"
        print(alert_msg)

        with open("/home/grettyandjeff/alerts.log", "a") as f:
            f.write(alert_msg + "\n")

    old = new
