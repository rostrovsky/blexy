from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from blexy.utils.config import GlobalConfig


async def homepage(request):
    """
    Returns JSON with list of connected devices
    """
    devices = [d.as_dict for d in GlobalConfig.connected_devices()]
    return JSONResponse(devices)


async def metrics(request):
    """
    Returns device readouts in OpenMetrics format
    """
    out = []
    for d in GlobalConfig.connected_devices():
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
