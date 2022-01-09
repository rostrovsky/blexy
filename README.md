# blexy
Simple [OpenMetrics](https://github.com/OpenObservability/OpenMetrics/blob/main/specification/OpenMetrics.md) exporter for BLE devices.

## Requirements
* device with BLE compliant transceiver (e.g. RPi 3+)
* Python 3.7+

## Running
```
pip install blexy
blexy --port 8888 --config-file ~/.blexy.yaml
```

## Endpoints
* `/` - returns list of connected devices in JSON format.
* `/metrics` - returns values read from connected BLE devices in [OpenMetrics format](https://github.com/OpenObservability/OpenMetrics/blob/main/specification/OpenMetrics.md).

## Config
* Device & server configuration is by default expected to be placed in  `./config.yaml`.
* Custom config file path can be specified via `-c / --config-file` command line option.
* `port` and `log_level` can be either specified in config file or through command line options (see `blexy -h` for exact option names). 

### Example config file
Below file will make blexy connect to two Xiaomi temperature / humidity sensors and listen on port 8080:
```yaml
port: 8080
log_level: info
ble:
  devices:
    - name: living room sensor
      model: LYWSD03MMC
      address: xx:xx:xx:xx:xx:xx
    - name: bedroom sensor
      model: LYWSD03MMC
      address: xx:xx:xx:xx:xx:xx
```

## Example output
```
$ curl localhost:8080/metrics
# TYPE battery_level_percentage gauge
# UNIT battery_level_percentage percentage
battery_level_percentage_gauge{name="living room sensor",model="LYWSD03MMC",manufacturer="Xiaomi",address="xx:xx:xx:xx:xx:xx",interface="0"} 77
battery_level_percentage_gauge{name="bedroom sensor",model="LYWSD03MMC",manufacturer="Xiaomi",address="xx:xx:xx:xx:xx:xx",interface="0"} 88
# TYPE humidity_percentage gauge
# UNIT humidity_percentage percentage
humidity_percentage_gauge{name="living room sensor",model="LYWSD03MMC",manufacturer="Xiaomi",address="xx:xx:xx:xx:xx:xx",interface="0"} 48
humidity_percentage_gauge{name="bedroom sensor",model="LYWSD03MMC",manufacturer="Xiaomi",address="xx:xx:xx:xx:xx:xx",interface="0"} 51
# TYPE temperature_celsius gauge
# UNIT temperature_celsius celsius
temperature_celsius_gauge{name="living room sensor",model="LYWSD03MMC",manufacturer="Xiaomi",address="xx:xx:xx:xx:xx:xx",interface="0"} 22.33
temperature_celsius_gauge{name="bedroom sensor",model="LYWSD03MMC",manufacturer="Xiaomi",address="xx:xx:xx:xx:xx:xx",interface="0"} 25.11
# TYPE voltage_volts gauge
# UNIT voltage_volts volts
voltage_volts_gauge{name="living room sensor",model="LYWSD03MMC",manufacturer="Xiaomi",address="xx:xx:xx:xx:xx:xx",interface="0"} 3.11
voltage_volts_gauge{name="bedroom sensor",model="LYWSD03MMC",manufacturer="Xiaomi",address="xx:xx:xx:xx:xx:xx",interface="0"} 3.03
# EOF
```

## Supported devices
* `LYWSD03MMC` (Xiaomi)