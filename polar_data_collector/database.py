import sqlite3


conn = sqlite3.connect("polar_data_collector.db")


def setup():
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS polar_data (
                    time TEXT, -- "YYYY-MM-DD HH:MM:SS" format
                    heart_rate INTEGER, -- in bpm
                    rr_intervals TEXT -- space-separated 64-bit floats
                    )"""
    )
    conn.commit()


def add_entry(HeartRateMeasurement):
    cur = conn.cursor()
    rr_intervals = (
        " ".join(map(str, HeartRateMeasurement.rr_interval))
        if HeartRateMeasurement.rr_interval
        else None
    )
    cur.execute(
        """INSERT INTO polar_data (time, heart_rate, rr_intervals) 
                   VALUES (datetime('now'), ?, ?)""",
        (HeartRateMeasurement.heart_rate_measurement_value, rr_intervals),
    )
    conn.commit()
