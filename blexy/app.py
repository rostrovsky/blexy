import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from blexy.utils.config import GlobalConfig
from blexy.utils.openmetrics import OpenMetricsAggregator


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
    oma = OpenMetricsAggregator()
    tasks = [d.asyncWaitForNotifications(5) for d in GlobalConfig.connected_devices()]
    results = await asyncio.gather(*tasks)
    for success, device in results:
        if success:
            oma.add_metrics(device.open_metrics)

    return PlainTextResponse(oma.text)


app = Starlette(
    routes=[
        Route("/", homepage),
        Route("/metrics", metrics),
    ],
)
