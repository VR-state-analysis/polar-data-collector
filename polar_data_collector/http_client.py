import os
import urllib.request
import urllib.parse
import datetime

from parse import HeartRateMeasurement


BASE_URL = os.getenv("BASE_URL", "https://gtxr-vrsa.kiyuri.ca/")


def send_data(measurement: HeartRateMeasurement):
    # format is "YYYY-MM-DD HH:MM:SS.SSS"
    measure_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    data = {"measure_time": measure_time, "heart_rate": measurement.heart_rate_measurement_value}
    data["rr_intervals"] = " ".join(map(str, measurement.rr_interval)) if measurement.rr_interval else ""
    encode = lambda s: urllib.parse.quote(s, safe="")
    urllib.request.urlopen(BASE_URL, data=bytes("&".join(f"{encode(k)}={encode(str(v))}" for k, v in data.items()), "utf-8"))
