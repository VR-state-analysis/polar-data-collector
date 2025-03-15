import struct
from dataclasses import dataclass
from typing import List


@dataclass
class HeartRateFlags:
    heart_rate_value_format: int
    sensor_contact_status: int
    energy_expended_status: int
    rr_interval_status: int

@dataclass
class HeartRateMeasurement:
    heart_rate_measurement_value: int | None = None
    """Heart rate measurement value in beats per minute (bpm)"""
    rr_interval: List[int] | None = None
    """RR interval in milliseconds (if present)"""


def read_flags(raw_data: bytes) -> HeartRateFlags:
    data = struct.unpack('>B', raw_data[:1])[0]
    return HeartRateFlags(
        heart_rate_value_format=data & 0b00000001,
        sensor_contact_status=(data & 0b00000110) >> 1,
        energy_expended_status=(data & 0b00001000) >> 3,
        rr_interval_status=(data & 0b00010000) >> 4,
    )

def read_stuff(raw_data: bytes):
    flags = read_flags(raw_data)
    offset = 1
    assert flags.heart_rate_value_format == 0, "only 8-bit format is supported rn"
    heart_rate_measurement_value = int(raw_data[offset])
    offset += 1
    if flags.energy_expended_status:
        offset += 2
    rr_interval = None
    if flags.rr_interval_status:
        rr_interval = []
        for i in range(offset, len(raw_data), 2):
            value = int.from_bytes(raw_data[i:i+2], byteorder='little')
            rr_interval.append(float(value) / 1024)
    return HeartRateMeasurement(
        heart_rate_measurement_value=heart_rate_measurement_value,
        rr_interval=rr_interval
    ), flags
