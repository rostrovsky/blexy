# blexy
Simple [OpenMetrics](https://github.com/OpenObservability/OpenMetrics/blob/main/specification/OpenMetrics.md) exporter for BLE devices

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

## Supported devices
* `LYWSD03MMC` (Xiaomi)