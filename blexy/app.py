from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from importlib import import_module


connected_devices = []

async def homepage(request):
    """
    Returns JSON with list of connected devices
    """
    devices = [d.as_dict for d in connected_devices]
    return JSONResponse(devices)


async def metrics(request):
    """
    Returns device readouts in OpenMetrics format
    """
    out = []
    for d in connected_devices:
        if d.peripheral.waitForNotifications(2000):
            out.extend(d.open_metrics)
    return PlainTextResponse("\n".join(out))


app = Starlette(
    debug=True,
    routes=[
        Route("/", homepage),
        Route("/metrics", metrics),
    ],
)

# connect devices
for dev in config_devices:
    dev_name = dev.get("name")
    dev_model = dev.get("model")
    dev_addr = dev.get("address")
    dev_iface = dev.get("interface", 0)
    try:
        device_module = import_module(f"devices.{dev_model}")
        device_class = getattr(device_module, dev_model)
        device_obj = device_class(name=dev_name, address=dev_addr, interface=dev_iface)
        connected_devices.append(device_obj.connect())
    except Exception as e:
        print(f'could not import device "{dev_name}" ({dev_model})')
        print(e)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=port, log_level=log_level)
