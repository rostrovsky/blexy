from setuptools import setup, find_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="blexy",
    description="Simple OpenMetrics exporter for BLE devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.2.0",
    url="https://github.com/rostrovsky/blexy",
    license="MIT",
    packages=find_packages(exclude=["*test.*","*test"]),
    include_package_data=True,
    install_requires=["click", "starlette", "pyyaml", "uvicorn", "bluepy", "twiggy"],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "blexy = blexy.main:cli",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="ble openmetrics bluetooth prometheus raspberry pi iot sensors",
)
