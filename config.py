from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class SplunkConfig:
    host: str
    port: int
    scheme: str
    username: str
    password: str


def load_config() -> SplunkConfig:
    def get_env(key: str, required: bool = True) -> str:
        value = os.getenv(key, "")
        if required and not value:
            raise EnvironmentError(f"Missing required environment variable: {key}")
        return value

    host = get_env("SPLUNK_HOST")
    port_value = get_env("SPLUNK_PORT")
    scheme = get_env("SPLUNK_SCHEME", required=False) or "https"
    username = get_env("SPLUNK_USERNAME")
    password = get_env("SPLUNK_PASSWORD")

    try:
        port = int(port_value)
    except ValueError as exc:
        raise ValueError("SPLUNK_PORT must be a valid integer") from exc

    return SplunkConfig(
        host=host,
        port=port,
        scheme=scheme,
        username=username,
        password=password,
    )