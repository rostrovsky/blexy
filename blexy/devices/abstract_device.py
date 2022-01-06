import json
from abc import ABCMeta, abstractmethod
from typing import List
from bluepy import btle


class AbstractDevice(btle.DefaultDelegate, metaclass=ABCMeta):
    def __init__(self, name, address, interface):
        super().__init__()
        self.name = name
        self.address = address
        self.interface = interface
        self.peripheral = btle.Peripheral(deviceAddr=None, iface=self.interface)
        self.is_connected = False

    @abstractmethod
    def connect(self) -> "AbstractDevice":
        pass

    @abstractmethod
    def handleNotification(self, cHandle, data):
        pass

    async def asyncWaitForNotifications(self, timeout) -> bool:
        raise NotImplementedError("TODO!")

    @abstractmethod
    @property
    def open_metrics(self) -> List[str]:
        pass

    @property
    def _open_metrics_labels(self) -> str:
        return f'{{name="{self.name}",model="{self.model}",manufacturer="{self.manufacturer}",address="{self.address}",interface="{self.interface}"}}'

    @property
    def as_dict(self) -> dict:
        return json.loads(json.dumps(vars(self), default=repr))
