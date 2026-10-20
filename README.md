# anistats_request

`anistats_request` is a Python project for fetching anime and manga data from the MyAnimeList (MAL) API and saving the responses as JSON files. Requests are defined in TOML configuration files, and `uv` is used to manage dependencies and the Python environment.

## Requirements

- Python 3.12 or later
- [`uv`](https://docs.astral.sh/uv/)
- A MyAnimeList API client ID

## Setup and usage

From the project root, sync the project dependencies:

```bash
uv sync
```

Alternatively, install the project and its dependencies from the generated `requirements.txt` file using pip:

```bash
python -m pip install -r requirements.txt
```

Set the `MAL_CLIENT_ID` environment variable to your MAL API client ID. On Linux/macOS:

```bash
export MAL_CLIENT_ID="your_mal_client_id"
uv run example.py
```

On PowerShell:

```powershell
$env:MAL_CLIENT_ID = "your_mal_client_id"
uv run example.py
```

The example reads requests from [configs/config_examples.toml](configs/config_examples.toml) and saves each response as a JSON file in `data/raw/`. For example, it creates `anime.json`. API requests use a 30-second timeout.

> Do not store `MAL_CLIENT_ID` in source code. The `.env` file is not loaded automatically; set the variable in your shell before running the example.

## Adding requests

Define each request as a separate table in a TOML file. The table name is used as the output JSON filename (the `anime` request creates `anime.json`).

```toml
title = "My requests"

[anime]
limit = 100
offset = 0
nsfw = false
endpoint = "anime/ranking"
fields = ["id", "title", "mean", "rank"]
```

Required fields:

- `limit`, `offset`: the number of results and the starting position
- `nsfw`: whether to include NSFW content
- `endpoint`: the MAL API endpoint
- `fields`: the list of fields to include in the response

See [configs/config_examples.toml](configs/config_examples.toml) for a complete example. For references to MAL fields and ranking types, see [docs/fields.md](docs/fields.md) and [docs/ranking.md](docs/ranking.md).

## Python API usage

`RequestConfigs.load_config()` loads all requests from a TOML file. `create_request()` sends a request to the MAL API for each configuration and returns the paths to the generated JSON files:

```python
from pathlib import Path

from anistats_request.config import RequestConfigs
from anistats_request.request import create_request

configs = RequestConfigs.load_config("configs/config_examples.toml")
output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)
paths = create_request(
    config=configs,
    save=True,
    output_dir=output_dir,
    timeout_seconds=30.0,
)
print(paths)
```

Set `MAL_CLIENT_ID` in the environment before starting the Python process. `create_request()` propagates HTTP and file-writing errors to the caller.

## Documentation

- [MAL fields reference](docs/fields.md)
- [Anime and manga ranking types](docs/ranking.md)
