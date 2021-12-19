# blexy
Simple [OpenMetrics](https://github.com/OpenObservability/OpenMetrics/blob/main/specification/OpenMetrics.md) exporter for BLE devices

## Running
```
pip install -r requirements.txt
python main.py
```

## Endpoints
* `/` - returns JSON list of connected devices.
* `/metrics` - returns values read from connected BLE devices.

## Config
Device & server configuration is stored in `config.yaml`.