import json
from abc import ABCMeta, abstractmethod, abstractproperty
from typing import List
from bluepy import btle


class AbstractDevice(btle.DefaultDelegate, metaclass=ABCMeta):
    @abstractmethod
    def connect(self) -> "AbstractDevice":
        pass

    @abstractmethod
    def handleNotification(self, cHandle, data):
        pass

    @abstractproperty
    def open_metrics(self) -> List[str]:
        pass

    @property
    def _open_metrics_labels(self) -> str:
        return f'{{name="{self.name}",model="{self.model}",manufacturer="{self.manufacturer}",address="{self.address}",interface="{self.interface}"}}'

    @property
    def as_dict(self) -> dict:
        return json.loads(json.dumps(vars(self), default=repr))
