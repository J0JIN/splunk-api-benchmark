from benchmark.metrics import AggregateBenchmarkResult


def print_benchmark_report(
    benchmark_results: list[AggregateBenchmarkResult],
    runs: int,
    query: str,
) -> None:
    print("\nSplunk API Benchmark")
    print("---------------------")
    print(f"Query: {query}")
    print(f"Runs per method: {runs}\n")

    header = f"{'Method':<12} {'Rows':>8} {'Time (s)':>12} {'Note':>32}"
    print(header)
    print("-" * len(header))

    for result in benchmark_results:
        print(
            f"{result.method:<12} {result.row_count:>8} {result.average_seconds:>12.2f} {result.note:>32}"
        )

    print("\nDetailed run results")
    print("--------------------")
    for result in benchmark_results:
        run_times = ", ".join(f"{run.elapsed_seconds:.2f}s" for run in result.all_runs)
        print(f"{result.method}: row_count={result.row_count}, runs=[{run_times}]")

    print("\nNotes")
    print("- The results path uses a search job followed by results API retrieval.")
    print("- The export path streams line-delimited JSON and is usually better for bulk retrieval.")
