"""Fetch the requests defined in configs/config_examples.toml."""

from pathlib import Path

from anistats_request.config import RequestConfigs
from anistats_request.request import create_request

PROJECT_DIR = Path(__file__).resolve().parent
CONFIG_PATH = PROJECT_DIR / "configs" / "config_examples.toml"
OUTPUT_DIR = PROJECT_DIR / "data" / "raw"


def main() -> None:
    """Load the example requests and save their responses as JSON."""
    configs = RequestConfigs.load_config(CONFIG_PATH)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_paths = create_request(
        config=configs,
        save=True,
        output_dir=OUTPUT_DIR,
        timeout_seconds=30.0,
    )

    for name, path in output_paths.items():
        print(f"Saved {name} response to {path}")


if __name__ == "__main__":
    main()
