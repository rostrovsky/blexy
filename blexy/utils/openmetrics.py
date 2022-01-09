from typing import Any, List
from dataclasses import dataclass
from itertools import groupby


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

    @property
    def type_metadata(self):
        return f"# TYPE {self.name}_{self.unit} {self.type}"

    @property
    def unit_metadata(self):
        return f"# UNIT {self.name}_{self.unit} {self.unit}"


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
    def grouped_metrics(self):
        sorted_metrics = sorted(
            self.metrics, key=lambda m: f"{m.name}_{m.unit}_{m.type}"
        )
        return groupby(sorted_metrics, lambda m: m.name)

    @property
    def text(self):
        out = []
        for metric_name, group in self.grouped_metrics:
            # out.append(f"{group}: {metric_name}")
            for metric in group:
                if metric.type_metadata not in out:
                    out.append(metric.type_metadata)
                if metric.unit_metadata not in out:
                    out.append(metric.unit_metadata)
                out.append(str(metric.text))
        out.append("# EOF")
        return "\n".join(out)
