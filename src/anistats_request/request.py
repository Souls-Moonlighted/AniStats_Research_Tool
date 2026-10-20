import json
import os
from pathlib import Path

import requests

from anistats_request.config import RequestConfig, RequestConfigs

API_BASE_URL = "https://api.myanimelist.net/v2"

def create_request(
    config: RequestConfig | RequestConfigs, save: bool, output_dir: Path, timeout_seconds: float
) -> dict[str, Path]:
    """Fetch configured data from MyAnimeList and write responses as JSON if save is True.

    A single ``RequestConfig`` creates one ``<name>.json`` file. A
    ``RequestConfigs`` collection creates one file for each contained request.
    When ``output_dir`` is omitted and ``save`` is true, files are written to
    ``data/raw``. Supplying ``output_dir`` selects that directory instead.

    Args:
        config: One request configuration or a collection of named
            configurations to run.
        timeout_seconds: The timeout for the API request in seconds.
        save: Whether to use ``data/raw`` as the default output directory when
            ``output_dir`` is omitted. Responses are written to an explicitly
            supplied ``output_dir`` regardless of this value.
        output_dir: Directory in which to write the JSON response files. If
            omitted, ``save`` must be true to select ``data/raw``.

    Returns:
        A mapping from each request name to its JSON file path.

    Raises:
        ValueError: ``MAL_CLIENT_ID`` is missing or a request name cannot be
            used as a file name.
        requests.RequestException: A request to the MyAnimeList API fails.
        OSError: The output directory or a response file cannot be created or
            written.
    """
    client_id = os.environ.get("MAL_CLIENT_ID")
    if not client_id:
        raise ValueError(
            "MAL_CLIENT_ID is not set. Set it to your MyAnimeList API client ID."
        )

    if isinstance(config, RequestConfig):
        request_configs = (config,)
    else:
        request_configs = tuple(config.configs.values())

    if not request_configs:
        raise ValueError("At least one request configuration is required")

    for request_config in request_configs:
        if (
            not request_config.name
            or request_config.name in {".", ".."}
            or Path(request_config.name).name != request_config.name
        ):
            raise ValueError(
                f"Request name {request_config.name!r} is not a valid file name"
            )

    if not output_dir.exists() and save:
        output_dir = Path.cwd().absolute().parents[2]/"data/raw"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths: dict[str, Path] = {}

    for request_config in request_configs:
        params: dict[str, str | int] = {
            "limit": request_config.limit,
            "offset": request_config.offset,
            "nsfw": str(request_config.nsfw).lower(), # Request parameter for NSFW content is a string "true" or "false"
        }
        if request_config.fields:
            params["fields"] = ",".join(request_config.fields) # Request parameter for fields is a comma-separated string

        response = requests.get(
            f"{API_BASE_URL}/{request_config.endpoint.lstrip('/')}",
            headers={"X-MAL-CLIENT-ID": client_id},
            params=params,
            timeout=timeout_seconds,
        )
        response.raise_for_status()

        output_path = output_dir / f"{request_config.name}.json"
        with output_path.open("w", encoding="utf-8") as output_file:
            json.dump(response.json(), output_file, ensure_ascii=False, indent=2)
            _ = output_file.write("\n")
        output_paths[request_config.name] = output_path

    return output_paths
