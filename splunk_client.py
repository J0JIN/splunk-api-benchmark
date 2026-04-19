from splunklib import client
from splunklib.binding import HTTPError

from config import SplunkConfig, load_config


def create_splunk_service(config: SplunkConfig | None = None) -> client.Service:
    if config is None:
        config = load_config()

    try:
        service = client.Service(
            host=config.host,
            port=config.port,
            scheme=config.scheme,
            username=config.username,
            password=config.password,
            verify=False,
            timeout=30,
        )
        service.login()
        return service
    except HTTPError as err:
        print(f"[ERROR] HTTP Error: {err}")
        raise ConnectionError(
            "Failed to connect to Splunk. Verify host, port, scheme, and credentials."
        ) from err
    except Exception as err:
        print(f"[ERROR] Unexpected error type: {type(err).__name__}")
        print(f"[ERROR] Error message: {err}")
        import traceback
        traceback.print_exc()
        raise ConnectionError(f"Unexpected error during Splunk authentication: {err}") from err
