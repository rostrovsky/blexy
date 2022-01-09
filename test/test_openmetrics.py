import pytest
from blexy.utils.openmetrics import OpenMetric, OpenMetricType, OpenMetricsAggregator


def test_openmetric_text():
    om = OpenMetric(
        name="temperature",
        type=OpenMetricType.gauge,
        unit="celsius",
        labels={"x": 1, "y": "something", "abcde": "hello #!!", "double": 0.113},
        value=22.34,
    )

    assert (
        om.text
        == 'temperature_celsius_gauge{x="1",y="something",abcde="hello #!!",double="0.113"} 22.34'
    )


def test_openmetrics_aggregator():
    dev1_labels = {
        "name": "sensor 1",
        "model": "model 1",
        "manufacturer": "acme",
        "address": "P:Q:R:S:T",
        "interface": 0,
    }

    dev2_labels = {
        "name": "sensor 2",
        "model": "model 1",
        "manufacturer": "acme",
        "address": "A:B:C:D:E",
        "interface": 0,
    }

    dev1_metrics = [
        OpenMetric(
            name="temperature",
            type=OpenMetricType.gauge,
            unit="celsius",
            labels=dev1_labels,
            value=22.33,
        ),
        OpenMetric(
            name="humidity",
            type=OpenMetricType.gauge,
            unit="percentage",
            labels=dev1_labels,
            value=48,
        ),
        OpenMetric(
            name="voltage",
            type=OpenMetricType.gauge,
            unit="volts",
            labels=dev1_labels,
            value=3.11,
        ),
        OpenMetric(
            name="battery_level",
            type=OpenMetricType.gauge,
            unit="percentage",
            labels=dev1_labels,
            value=77,
        ),
    ]

    dev2_metrics = [
        OpenMetric(
            name="temperature",
            type=OpenMetricType.gauge,
            unit="celsius",
            labels=dev2_labels,
            value=25.11,
        ),
        OpenMetric(
            name="humidity",
            type=OpenMetricType.gauge,
            unit="percentage",
            labels=dev2_labels,
            value=51,
        ),
        OpenMetric(
            name="voltage",
            type=OpenMetricType.gauge,
            unit="volts",
            labels=dev2_labels,
            value=3.03,
        ),
        OpenMetric(
            name="battery_level",
            type=OpenMetricType.gauge,
            unit="percentage",
            labels=dev2_labels,
            value=88,
        ),
    ]

    oma = OpenMetricsAggregator()
    oma.add_metrics(dev1_metrics).add_metrics(dev2_metrics)

    print(f"\n\n{oma.text}")
