from typing import Any, List
from dataclasses import dataclass


class OpenMetricType:
    gauge = "gauge"
    counter = "counter"
    state_set = "state_set"
    info = "info"
    histogram = "histogram"
    gauge_histogram = "gauge_histogram"
    summary = "summary"
    unknown = "unknown"


@dataclass
class OpenMetric:
    name: str
    type: str
    unit: str
    labels: dict
    value: Any

    @property
    def labels_text(self):
        out = []
        for k, v in self.labels.items():
            out.append(f'{k}="{v}"')
        return ",".join(out)

    @property
    def text(self):
        return f"{self.name}_{self.unit}_{self.type}{{{self.labels_text}}} {self.value}"


class OpenMetricsAggregator:
    def __init__(self):
        self.metrics = []

    def add_metric(self, metric: OpenMetric) -> "OpenMetricsAggregator":
        self.metrics.append(metric)
        return self

    def add_metrics(self, metrics: List[OpenMetric]) -> "OpenMetricsAggregator":
        self.metrics.extend(metrics)
        return self

    @property
    def text(self):
        return "TODO"
