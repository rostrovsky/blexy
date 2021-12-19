from abc import abstractproperty
from pathlib import Path
from importlib import import_module
from typing import List
import yaml

from blexy.devices.abstract_device import AbstractDevice

with open("config.yaml", "r") as cf:
    config = yaml.load(cf, yaml.SafeLoader)
    port = config.get("port")
    log_level = config.get("log_level")
    config_devices = config.get("ble").get("devices")


class GlobalConfig:
    port = None
    log_level = None
    devices = None
    _device_objects = None

    @staticmethod
    def load_from_file(file_path: str) -> "GlobalConfig":
        fp = Path(file_path)
        with open(fp, "r") as cf:
            config = yaml.load(cf, yaml.SafeLoader)
            GlobalConfig.port = config.get("port")
            GlobalConfig.log_level = config.get("log_level")
            GlobalConfig.devices = config.get("ble").get("devices")

        if GlobalConfig.devices:
            GlobalConfig._device_objects = []

        for dev in GlobalConfig.devices:
            dev_name = dev.get("name")
            dev_model = dev.get("model")
            dev_addr = dev.get("address")
            dev_iface = dev.get("interface", 0)
            try:
                device_module = import_module(f"blexy.devices.{dev_model}")
                device_class = getattr(device_module, dev_model)
                device_obj = device_class(
                    name=dev_name, address=dev_addr, interface=dev_iface
                )
                GlobalConfig._device_objects.append(device_obj)
            except Exception as e:
                print(f'could not import device "{dev_name}" ({dev_model})')
                print(e)

    @staticmethod
    def connected_devices() -> List[AbstractDevice]:
        return [d for d in GlobalConfig._device_objects if d.is_connected]

    @staticmethod
    def connect_all_devices():
        for d in GlobalConfig._device_objects:
            d.connect()
