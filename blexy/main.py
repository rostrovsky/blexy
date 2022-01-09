import click
import uvicorn
import blexy.app
from blexy.utils.config import GlobalConfig
from twiggy import quick_setup, levels


@click.command()
@click.help_option("-h", "--help")
@click.option("-p", "--port", type=click.INT)
@click.option("-c", "--config-file", default="./config.yaml", show_default=True)
@click.option("--log-level")
def cli(port, config_file, log_level):
    """
    Simple OpenMetrics exporter for BLE devices.
    """
    GlobalConfig.load_from_file(config_file)
    app_port = port if port else GlobalConfig.port
    app_log_level = log_level if log_level else GlobalConfig.log_level
    quick_setup(min_level=getattr(levels, app_log_level.upper()))
    GlobalConfig.connect_all_devices()
    uvicorn.run(blexy.app.app, host="0.0.0.0", port=app_port, log_level=app_log_level)


if __name__ == "__main__":
    cli()
