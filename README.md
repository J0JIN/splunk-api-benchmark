# Splunk API Benchmark

A small production-style benchmark repository for comparing Splunk Search API retrieval patterns.

This project is designed to demonstrate the performance and stability differences between:

- `jobs.create(...)+job.results(...)` — the Splunk results API workflow
- `service.jobs.export(...)` — the Splunk export streaming workflow

The goal is to show why results-based retrieval can become slow or unstable for large event volumes and high-cardinality searches, while export-based streaming is often more suitable for bulk retrieval.

## Project Overview

This repository provides:

- a clean CLI interface for running benchmarks
- separate implementation modules for results and export benchmarks
- timing helpers for repeated runs and averaged comparisons
- safe parsing of Splunk export JSON streams
- console output that highlights row counts, elapsed time, and behavioral differences

## Why this benchmark exists

In Splunk, search jobs and results retrieval are convenient for dashboard-style and interactive queries. However, when the result set becomes very large, the results API can:

- require the search job to remain alive until completion
- buffer large payloads inside Splunk
- become slower or unstable for bulk extraction

The export API is built for streaming and bulk retrieval, making it more reliable for large result sets and high-cardinality data.

## Difference between results and export

- `results`: submits a search job, polls until completion, then retrieves returned results as JSON.
- `export`: streams raw search output directly from Splunk in line-delimited JSON.

The export approach is often better for large datasets because it reduces memory pressure and avoids waiting for the full job payload to be materialized in the results endpoint.

## Setup Instructions

1. Clone the repository.
2. Copy `.env.example` to `.env`.
3. Fill in your Splunk connection details.
4. Install dependencies.

```bash
python -m pip install -r requirements.txt
```

## Example `.env`

```env
SPLUNK_HOST=localhost
SPLUNK_PORT=8089
SPLUNK_SCHEME=https
SPLUNK_USERNAME=admin
SPLUNK_PASSWORD=changeme
```

## How to run

```bash
python main.py --query "search index=_internal | head 1000" --runs 3
```

If no query is provided, the benchmark uses a safe default:

```bash
search index=_internal | head 100
```

## Example output

```text
Benchmark summary
-----------------
Method         Rows   Time (s)   Note
results        100    2.19       search job + results API retrieval
export         100    0.37       streaming export API retrieval

Averages over 3 runs
---------------------
results export 0.87 sec
export export 0.29 sec
```

## Suggested test queries

- `search index=_internal | head 1000`
- `search index=* | head 5000`
- `search index=_audit | head 2000`

> This repository is meant to compare bulk result retrieval strategies, not generic Splunk query tuning.

## Real-world relevance

Security teams, SIEM operators, and Splunk platform engineers frequently need to move large search outputs from Splunk into downstream analytics, monitoring, or incident response workflows.

This benchmark helps show why export-style streaming is often preferable for:

- forensic data extraction
- large-scale data export
- automated alert enrichment
- high-cardinality search result retrieval

## Notes

- Use search queries that produce a significant number of results to observe the performance gap.
- The benchmark is intentionally simple, focusing on method comparison rather than search optimization.
- Export returns line-delimited JSON, so parsing is designed to handle streaming safely.
- **Splunk results API limitation**: By default, the results API returns a maximum of 50,000 events per search. For queries that return more than 50,000 events, you must modify Splunk's `maxresultrows` setting in `limits.conf` or use the export API for unlimited results.
