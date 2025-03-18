import os
import urllib.parse
import subprocess
import datetime

from parse import HeartRateMeasurement


BASE_URL = os.getenv("BASE_URL", "https://gtxr-vrsa.kiyuri.ca/")


def send_data(measurement: HeartRateMeasurement):
    measured_time = datetime.datetime.now().isoformat()
    data = {"measured_time": measured_time, "heart_rate": measurement.heart_rate_measurement_value}
    data["rr_intervals"] = " ".join(map(str, measurement.rr_interval)) if measurement.rr_interval else ""
    encode = lambda s: urllib.parse.quote(s, safe="")
    data = "&".join(f"{encode(k)}={encode(str(v))}" for k, v in data.items())
    url = f"{BASE_URL}"
    cmd = ["curl", "-d", data, url]
    subprocess.run(cmd, capture_output=True, check=True)
