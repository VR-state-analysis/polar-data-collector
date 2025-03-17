import functools

from PySide6.QtBluetooth import (
    QBluetoothDeviceInfo,
    QLowEnergyController,
    QBluetoothUuid,
    QBluetoothDeviceDiscoveryAgent,
    QLowEnergyService,
    QLowEnergyCharacteristic,
)
from PySide6.QtCore import QByteArray

import database
import http_client
import parse


def on_discovered(device):
    print(f"Discovered device: {device.name()}")
    if device.name().startswith("Polar"):
        print(
            f"Polar device found: {device.name()} with address {device.address().toString()}"
        )
        assert (
            device.coreConfigurations()
            & QBluetoothDeviceInfo.CoreConfiguration.LowEnergyCoreConfiguration
        ), "Polar must be BLE"
        controller = QLowEnergyController.createCentral(device)
        controller.connected.connect(lambda: on_connect_polar(controller, device))
        controller.disconnected.connect(
            lambda: print(f"[{device.name()}] Disconnected from {device.name()}")
        )
        controller.errorOccurred.connect(
            lambda error: print(f"[{device.name()}] Controller error: {error}")
        )
        controller.serviceDiscovered.connect(
            functools.partial(on_service_discovered, controller, device)
        )
        controller.connectToDevice()


def on_service_discovered(
    controller: QLowEnergyController,
    device: QBluetoothDeviceInfo,
    service: QBluetoothUuid,
):
    print(f"[{device.name()}] Service discovered: {service}")
    if service == QBluetoothUuid(QBluetoothUuid.ServiceClassUuid.HeartRate):
        print(f"[{device.name()}] Heart Rate service discovered")
        heart_rate_service = controller.createServiceObject(service)
        assert heart_rate_service is not None, "???"
        heart_rate_service.stateChanged.connect(
            functools.partial(on_hr_state_changed, device, heart_rate_service)
        )
        heart_rate_service.characteristicChanged.connect(
            lambda characteristic, value: on_heart_rate_changed(
                characteristic, device, value
            )
        )
        heart_rate_service.errorOccurred.connect(
            lambda error: print(f"[{device.name()}] Heart Rate service error: {error}")
        )
        heart_rate_service.discoverDetails()


def on_hr_state_changed(
    device: QBluetoothDeviceInfo,
    heart_rate_service: QLowEnergyService,
    state: QLowEnergyService.ServiceState,
):
    print(f"[{device.name()}] Heart Rate service state changed: {state}")
    if state == QLowEnergyService.ServiceState.ServiceDiscovered:
        print(f"[{device.name()}] Heart Rate service is ready")
        hr_char = heart_rate_service.characteristic(
            QBluetoothUuid(QBluetoothUuid.CharacteristicType.HeartRateMeasurement)
        )
        assert hr_char.isValid()
        descriptor = hr_char.descriptor(
            QBluetoothUuid(
                QBluetoothUuid.DescriptorType.ClientCharacteristicConfiguration
            )
        )
        assert descriptor.isValid()
        heart_rate_service.writeDescriptor(descriptor, QByteArray.fromHex(b"0100"))


def on_connect_polar(controller: QLowEnergyController, device: QBluetoothDeviceInfo):
    print(
        f"[{device.name()}] Connected to Polar device: {device.name()}; discovering services..."
    )
    controller.discoverServices()


def on_heart_rate_changed(
    characteristic: QLowEnergyCharacteristic,
    device: QBluetoothDeviceInfo,
    value: QByteArray,
):
    if characteristic.uuid() == QBluetoothUuid(
        QBluetoothUuid.CharacteristicType.HeartRateMeasurement
    ):
        print(f"data: {value}")
        measurement, flags = parse.read_stuff(value.data())
        print(
            f"[{device.name()}] Heart Rate Measurement: {measurement.heart_rate_measurement_value} bpm; RR Interval: {measurement.rr_interval}; Flags: {flags}"
        )
        database.add_entry(measurement)
        http_client.send_data(measurement)


def discover():
    agent = QBluetoothDeviceDiscoveryAgent()
    agent.setLowEnergyDiscoveryTimeout(5000)
    agent.deviceDiscovered.connect(on_discovered)
    agent.errorOccurred.connect(lambda error: print(f"Discovery error: {error}"))
    agent.finished.connect(lambda: print("Discovery finished"))
    agent.canceled.connect(lambda: print("Discovery canceled"))
    agent.start(QBluetoothDeviceDiscoveryAgent.DiscoveryMethod.LowEnergyMethod)
