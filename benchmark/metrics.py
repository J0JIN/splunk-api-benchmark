from dataclasses import dataclass
from time import perf_counter
from typing import Callable, Iterable, List


@dataclass(frozen=True)
class BenchmarkResult:
    method: str
    row_count: int
    elapsed_seconds: float
    note: str


@dataclass(frozen=True)
class AggregateBenchmarkResult:
    method: str
    row_count: int
    average_seconds: float
    note: str
    all_runs: List[BenchmarkResult]


def measure_time_seconds(func: Callable[..., BenchmarkResult], *args, **kwargs) -> BenchmarkResult:
    start = perf_counter()
    result = func(*args, **kwargs)
    elapsed = perf_counter() - start
    return BenchmarkResult(
        method=result.method,
        row_count=result.row_count,
        elapsed_seconds=elapsed,
        note=result.note,
    )


def run_benchmark_multiple_times(
    func: Callable[..., BenchmarkResult],
    runs: int,
    *args,
    **kwargs,
) -> AggregateBenchmarkResult:
    if runs <= 0:
        raise ValueError("runs must be a positive integer")

    results: List[BenchmarkResult] = []
    for _ in range(runs):
        benchmark_result = measure_time_seconds(func, *args, **kwargs)
        results.append(benchmark_result)

    average_seconds = sum(result.elapsed_seconds for result in results) / len(results)
    reference = results[0]

    return AggregateBenchmarkResult(
        method=reference.method,
        row_count=reference.row_count,
        average_seconds=average_seconds,
        note=reference.note,
        all_runs=results,
    )
