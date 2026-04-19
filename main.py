import argparse
import sys

from benchmark.export_api import benchmark_export_api
from benchmark.metrics import run_benchmark_multiple_times
from benchmark.results_api import benchmark_results_api
from splunk_client import create_splunk_service
from config import load_config
from utils.printer import print_benchmark_report


DEFAULT_QUERY = "search index=_internal | head 100"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare Splunk results API and export API retrieval performance."
    )
    parser.add_argument(
        "--query",
        "-q",
        type=str,
        default=DEFAULT_QUERY,
        help="Splunk search query to benchmark.",
    )
    parser.add_argument(
        "--runs",
        "-r",
        type=int,
        default=1,
        help="Number of repeated benchmark runs to average.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_arguments()

    try:
        config = load_config()
        service = create_splunk_service(config)
    except Exception as err:
        print(f"Error initializing Splunk client: {err}")
        return 1

    try:
        results_summary = run_benchmark_multiple_times(
            benchmark_results_api, args.runs, service, args.query
        )
        export_summary = run_benchmark_multiple_times(
            benchmark_export_api, args.runs, service, args.query
        )
    except Exception as err:
        print(f"Benchmark failed: {err}")
        return 1

    print_benchmark_report([results_summary, export_summary], args.runs, args.query)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
