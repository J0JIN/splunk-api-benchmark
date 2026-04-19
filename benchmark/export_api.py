import json
from typing import Any

from splunklib.client import Service

from benchmark.metrics import BenchmarkResult
from utils.parsers import parse_line_delimited_json


def benchmark_export_api(service: Service, query: str) -> BenchmarkResult:
    try:
        response = service.jobs.export(query, output_mode="json")
        payload = response.read().decode("utf-8", errors="replace")
        row_count = sum(1 for _ in parse_line_delimited_json(payload))
    except ValueError as err:
        raise ValueError("Could not parse JSON from export API stream.") from err
    except Exception as err:
        raise RuntimeError("Error while retrieving data from the Splunk export API.") from err

    return BenchmarkResult(
        method="export",
        row_count=row_count,
        elapsed_seconds=0.0,
        note="streaming export API retrieval",
    )
