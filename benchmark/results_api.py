import json
from time import sleep
from typing import Any

from splunklib.client import Service

from benchmark.metrics import BenchmarkResult


def benchmark_results_api(service: Service, query: str) -> BenchmarkResult:
    try:
        job = service.jobs.create(query, exec_mode="normal")
    except Exception as err:
        raise RuntimeError("Failed to create a Splunk search job.") from err

    try:
        while True:
            job.refresh()
            if job["isDone"] == "1":
                break
            sleep(1)

        response = job.results(output_mode="json", count=0)
        payload = response.read().decode("utf-8")
        document = json.loads(payload)
        results = document.get("results", [])
        row_count = len(results)
    except json.JSONDecodeError as err:
        raise ValueError("Could not parse JSON response from results API.") from err
    except Exception as err:
        raise RuntimeError("Error while retrieving results from the Splunk results API.") from err

    return BenchmarkResult(
        method="results",
        row_count=row_count,
        elapsed_seconds=0.0,
        note="search job + results API retrieval",
    )
