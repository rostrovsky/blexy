from bluepy import btle
from typing import List
from blexy.devices.abstract_device import AbstractDevice


class LYWSD03MMC(AbstractDevice):
    model = "LYWSD03MMC"
    manufacturer = "Xiaomi"

    def __init__(self, name, address, interface) -> None:
        super().__init__()

        self.name = name
        self.address = address
        self.interface = interface

        self.temperature = None
        self.humidity = None
        self.voltage = None
        self.battery_level = None

        self.peripheral = btle.Peripheral(deviceAddr=None, iface=self.interface)

    def connect(self):
        print(f"Connecting {self.name} ({self.model})")
        self.peripheral.connect(self.address)
        self.peripheral.writeCharacteristic(
            0x0038, b"\x01\x00", True
        )  # enable notifications of Temperature, Humidity and Battery voltage
        self.peripheral.writeCharacteristic(0x0046, b"\xf4\x01\x00", True)
        self.peripheral.withDelegate(self)
        print(f"Connected {self.name} ({self.model})")
        return self

    def handleNotification(self, cHandle, data):
        try:
            print(f"{self.name} ({self.model}) : received {data}")
            self.temperature = (
                int.from_bytes(data[0:2], byteorder="little", signed=True) / 100
            )
            self.humidity = int.from_bytes(data[2:3], byteorder="little")
            self.voltage = int.from_bytes(data[3:5], byteorder="little") / 1000.0
            self.battery_level = min(
                int(round((self.voltage - 2.1), 2) * 100), 100
            )  # 3.1 or above --> 100% 2.1 --> 0 %
        except Exception as e:
            print("e")

    @property
    def open_metrics(self) -> List[str]:
        output = [
            f"temperature{self._open_metrics_labels} {self.temperature}",
            f"humidity{self._open_metrics_labels} {self.humidity}",
            f"voltage{self._open_metrics_labels} {self.voltage}",
            f"battery_level{self._open_metrics_labels} {self.battery_level}",
        ]
        return output
