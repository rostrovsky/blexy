import asyncio
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
    tasks = [d.asyncWaitForNotifications(5) for d in GlobalConfig.connected_devices()]
    results = await asyncio.gather(*tasks)
    for success, device in results:
        if success:
            out.extend(device.open_metrics)
    out.append("# EOF")

    return PlainTextResponse("\n".join(out))


app = Starlette(
    debug=True,
    routes=[
        Route("/", homepage),
        Route("/metrics", metrics),
    ],
)
