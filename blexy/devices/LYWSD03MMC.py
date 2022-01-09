from typing import List
from blexy.devices.abstract_device import AbstractDevice
from blexy.utils.openmetrics import OpenMetric, OpenMetricType


class LYWSD03MMC(AbstractDevice):
    model = "LYWSD03MMC"
    manufacturer = "Xiaomi"

    def __init__(self, name, address, interface) -> None:
        super().__init__(name, address, interface)

        self.temperature = None
        self.humidity = None
        self.voltage = None
        self.battery_level = None

    def connect(self):
        if self.is_connected:
            return self

        self.log.info("Connecting...")
        self.peripheral.connect(self.address)
        self.peripheral.writeCharacteristic(
            0x0038, b"\x01\x00", True
        )  # enable notifications of Temperature, Humidity and Battery voltage
        self.peripheral.writeCharacteristic(0x0046, b"\xf4\x01\x00", True)
        self.peripheral.withDelegate(self)
        self.log.info(f"Connected")
        self.is_connected = True
        return self

    def handleNotification(self, cHandle, data):
        try:
            self.log.info(f"received data: {data.hex()}")
            self.temperature = (
                int.from_bytes(data[0:2], byteorder="little", signed=True) / 100
            )
            self.humidity = int.from_bytes(data[2:3], byteorder="little")
            self.voltage = int.from_bytes(data[3:5], byteorder="little") / 1000.0
            self.battery_level = min(
                int(round((self.voltage - 2.1), 2) * 100), 100
            )  # 3.1 or above --> 100% 2.1 --> 0 %
        except Exception as e:
            self.log.error(e)

    @property
    def open_metrics(self) -> List[OpenMetric]:
        output = [
            OpenMetric(
                name="temperature",
                type=OpenMetricType.gauge,
                unit="celsius",
                labels=self._open_metrics_labels,
                value=self.temperature,
            ),
            OpenMetric(
                name="humidity",
                type=OpenMetricType.gauge,
                unit="percentage",
                labels=self._open_metrics_labels,
                value=self.humidity,
            ),
            OpenMetric(
                name="voltage",
                type=OpenMetricType.gauge,
                unit="volts",
                labels=self._open_metrics_labels,
                value=self.voltage,
            ),
            OpenMetric(
                name="battery_level",
                type=OpenMetricType.gauge,
                unit="percentage",
                labels=self._open_metrics_labels,
                value=self.battery_level,
            ),
        ]
        return output
