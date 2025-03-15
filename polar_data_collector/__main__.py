import sys

from PySide6.QtCore import QCoreApplication
from PySide6.QtBluetooth import QBluetoothLocalDevice

from main import discover
import database


if __name__ == "__main__":
    database.setup()
    app = QCoreApplication(sys.argv)
    local_device = QBluetoothLocalDevice()
    assert local_device.isValid(), "Bluetooth device is not valid"
    local_device.powerOn()
    print("Bluetooth device powered on")
    local_device.setHostMode(QBluetoothLocalDevice.HostMode.HostDiscoverable)
    print("Bluetooth device set to discoverable mode")
    print(f"my name is '{local_device.name()}'")
    print(f"my address is '{local_device.address().toString()}'")
    discover()
    sys.exit(app.exec())
