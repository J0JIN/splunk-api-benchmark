import json
from typing import Iterator


def parse_line_delimited_json(raw_text: str) -> Iterator[dict]:
    """Parse line-delimited JSON safely from Splunk export output."""
    for line_number, line in enumerate(raw_text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue

        try:
            record = json.loads(stripped)
        except json.JSONDecodeError as err:
            raise ValueError(
                f"Invalid JSON on export stream line {line_number}: {err.msg}"
            ) from err

        if not isinstance(record, dict):
            raise ValueError(
                f"Export stream line {line_number} did not parse as a JSON object."
            )

        yield record
