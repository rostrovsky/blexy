import json
from abc import ABCMeta, abstractmethod
from typing import List, Tuple
from bluepy import btle
from twiggy import log

from blexy.utils.concurrency import run_in_executor


class AbstractDevice(btle.DefaultDelegate, metaclass=ABCMeta):
    def __init__(self, name, address, interface):
        super().__init__()
        self.name = name
        self.address = address
        self.interface = interface
        self.peripheral = btle.Peripheral(deviceAddr=None, iface=self.interface)
        self.is_connected = False

    @property
    def log(self):
        return log.name(f"{self.name}@{self.address}")

    @abstractmethod
    def connect(self) -> "AbstractDevice":
        pass

    @abstractmethod
    def handleNotification(self, cHandle, data):
        pass

    @run_in_executor
    def __asyncWaitForNotifications(self, timeout) -> Tuple[bool, "AbstractDevice"]:
        return self.peripheral.waitForNotifications(timeout), self

    async def asyncWaitForNotifications(self, timeout) -> Tuple[bool, "AbstractDevice"]:
        self.log.debug(f"waiting for notification with timeout {timeout}s")
        return await self.__asyncWaitForNotifications(timeout), self

    @property
    @abstractmethod
    def open_metrics(self) -> List[str]:
        pass

    @property
    def _open_metrics_labels(self) -> dict:
        # return f'{{name="{self.name}",model="{self.model}",manufacturer="{self.manufacturer}",address="{self.address}",interface="{self.interface}"}}'
        return {
            "name": self.name,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "address": self.address,
            "interface": self.interface,
        }

    @property
    def as_dict(self) -> dict:
        return json.loads(json.dumps(vars(self), default=repr))
