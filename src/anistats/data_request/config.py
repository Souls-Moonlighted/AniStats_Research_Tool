import os
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path
from typing import ClassVar, cast

import tomli_w

try:
    CLIENT_ID = os.environ["MAL_CLIENT_ID"]
except KeyError:
    print(
        "Error: API key not found. Please set the MAL_CLIENT_ID environment variable with your MyAnimeList API key"
    )
    sys.exit(1)

DEFAULT_CONFIG_PATH = Path(__file__).parents[2] / "configs" / "request.toml"


@dataclass(slots=True, frozen=True)
class RequestConfig:
    """
    Configuration for one request.

    The ``name`` is the TOML table name when stored in a multi-config file.

    Attributes:
        name: Name of this request and its TOML table.
        limit: Maximum number of results to return.
        offset: Number of results to skip.
        nsfw: Whether NSFW results are included.
        source: Source or ranking used for the request.
        fields: Response fields to include.

    Examples:
        >>> anime = RequestConfig(
        ...     name="anime",
        ...     limit=100,
        ...     offset=0,
        ...     nsfw=False,
        ...     source="popular",
        ...     fields=["id", "title"],
        ... )
        >>> anime.write_request_config("configs/request.toml")
        >>> loaded = RequestConfig.load_config(
        ...     "configs/request.toml", config_name="anime"
        ... )
        >>> loaded.name
        'anime'
    """

    name: str
    limit: int
    offset: int
    nsfw: bool
    source: str
    fields: list[str]

    @classmethod
    def load_config(
        cls,
        config_path: Path | str = DEFAULT_CONFIG_PATH,
        config_name: str | None = None,
    ) -> "RequestConfig":
        """Load one request from a named table in a TOML config file.

        When a file contains one request table, ``config_name`` can be omitted.

        Args:
            config_path: TOML file to read.
            config_name: Name of the request table to load. Required when the
                file contains multiple request configurations.

        Returns:
            The selected request configuration.

        Raises:
            FileNotFoundError: The TOML file does not exist.
            TypeError: The file contains an invalid configuration value.
            ValueError: The request name is missing, ambiguous, or not found.

        Examples:
            Load one request from a file containing multiple tables:

                anime = RequestConfig.load_config(
                    "configs/request.toml", config_name="anime"
                )

            Load from a file containing one request table:

                request = RequestConfig.load_config(
                    "configs/single_request.toml"
                )
        """
        request_configs = RequestConfigs.load_config(config_path)
        if config_name is None:
            if len(request_configs.configs) != 1:
                raise ValueError(
                    "config_name is required when the TOML file contains multiple request tables"
                )
            return next(iter(request_configs.configs.values()))

        try:
            return request_configs.configs[config_name]
        except KeyError:
            raise ValueError(
                f"Configuration {config_name!r} not found in {config_path}"
            ) from None

    def write_request_config(
        self, config_path: Path | str = DEFAULT_CONFIG_PATH
    ) -> None:
        """Write this request as a named table, merging it into an existing file.

        Other request tables are preserved; a table with the same name is
        replaced. A new file is created when the path does not exist.

        Args:
            config_path: Destination TOML file. Created with parent directories
                if it does not already exist.

        Raises:
            FileNotFoundError: An existing configuration file cannot be read.
            TypeError: The existing configuration file has invalid values.
            ValueError: The existing configuration file has no request tables.

        Returns:
            ``None``.

        Examples:
            >>> request = RequestConfig(
            ...     name="manga",
            ...     limit=50,
            ...     offset=0,
            ...     nsfw=False,
            ...     source="top",
            ...     fields=["id", "title"],
            ... )
            >>> request.write_request_config("configs/request.toml")
        """
        config_path = Path(config_path)
        existing = (
            RequestConfigs.load_config(config_path)
            if config_path.exists()
            else RequestConfigs(RequestConfigs.DEFAULT_TITLE, {})
        )
        configs = dict(existing.configs)
        configs[self.name] = self
        RequestConfigs(existing.title, configs).write_config(config_path, merge=False)


@dataclass(slots=True, frozen=True)
class RequestConfigs:
    """A collection of named request configurations stored in one TOML file.

    Attributes:
        title: Human-readable title written at the top of the TOML file.
        configs: Mapping from each request name to its configuration.
        DEFAULT_TITLE: Default title used when loading files without a title.

    Examples:
        >>> configs = RequestConfigs(
        ...     title="Request configs",
        ...     configs={
        ...         "anime": RequestConfig(
        ...             "anime", 100, 0, False, "popular", ["id", "title"]
        ...         ),
        ...         "manga": RequestConfig(
        ...             "manga", 50, 0, False, "top", ["id", "title"]
        ...         ),
        ...     },
        ... )
        >>> configs.write_config("configs/request.toml")
        >>> loaded = RequestConfigs.load_config("configs/request.toml")
        >>> anime = loaded.configs["anime"]
    """

    title: str
    configs: dict[str, RequestConfig]

    DEFAULT_TITLE: ClassVar[str] = "Request configs"

    def __post_init__(self) -> None:
        """Validate that each mapping key matches the request's name.

        Raises:
            ValueError: A config is stored under a key different from its name.
        """
        if any(name != config.name for name, config in self.configs.items()):
            raise ValueError("Each request config must be stored under its own name")

    @classmethod
    def load_config(
        cls, config_path: Path | str = DEFAULT_CONFIG_PATH
    ) -> "RequestConfigs":
        """Load all named requests from a TOML config file.

        Args:
            config_path: TOML file to read.

        Returns:
            The collection of request configurations in the file.

        Raises:
            FileNotFoundError: The TOML file does not exist.
            TypeError: The file contains an invalid title or request value.
            ValueError: The file does not contain any request tables.

        Examples:
            >>> configs = RequestConfigs.load_config("configs/request.toml")
            >>> for name, request in configs.configs.items():
            ...     print(name, request.source)
        """
        config_path = Path(config_path)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")

        with config_path.open("rb") as config_file:
            document = cast(dict[str, object], tomllib.load(config_file))

        title_value = document.get("title", cls.DEFAULT_TITLE)
        if not isinstance(title_value, str):
            raise TypeError("Configuration title must be a string")

        requests: dict[str, RequestConfig] = {}
        for name, table in document.items():
            if name == "title":
                continue
            requests[name] = _request_config_from_table(name, table)

        if not requests:
            raise ValueError(f"No request tables found in {config_path}")

        return cls(title_value, requests)

    def write_config(
        self,
        config_path: Path | str = DEFAULT_CONFIG_PATH,
        *,
        merge: bool = True,
    ) -> None:
        """Write this collection, optionally merging with an existing TOML file.

        Existing tables with matching names are replaced when merging. Pass
        ``merge=False`` to replace the file's contents with this collection.

        Args:
            config_path: Destination TOML file.
            merge: If ``True``, preserve existing request tables and replace
                entries that have names matching this collection. If ``False``,
                replace the file with this collection.

        Raises:
            FileNotFoundError: An existing configuration file cannot be read.
            TypeError: The existing configuration file has invalid values.
            ValueError: The existing configuration file has no request tables.

        Returns:
            ``None``.

        Examples:
            >>> configs.write_config("configs/request.toml")
            >>> configs.write_config("configs/request.toml", merge=False)
        """
        config_path = Path(config_path)
        requests = (
            dict(RequestConfigs.load_config(config_path).configs)
            if merge and config_path.exists()
            else {}
        )
        requests.update(self.configs)

        output: dict[str, object] = {"title": self.title}
        output.update(
            {name: _request_parameters(config) for name, config in requests.items()}
        )
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with config_path.open("wb") as config_file:
            tomli_w.dump(output, config_file)


def _request_parameters(config: RequestConfig) -> dict[str, object]:
    return {
        "limit": config.limit,
        "offset": config.offset,
        "nsfw": config.nsfw,
        "source": config.source,
        "fields": config.fields,
    }


def _request_config_from_table(name: str, table: object) -> RequestConfig:
    if not isinstance(table, dict):
        raise TypeError(f"Configuration table {name!r} must contain a TOML table")
    table = cast(dict[str, object], table)

    limit = table.get("limit")
    offset = table.get("offset")
    nsfw = table.get("nsfw")
    source = table.get("source")
    fields_value = table.get("fields")

    if type(limit) is not int:
        raise TypeError(f"Configuration {name!r} must define an integer limit")
    if type(offset) is not int:
        raise TypeError(f"Configuration {name!r} must define an integer offset")
    if not isinstance(nsfw, bool):
        raise TypeError(f"Configuration {name!r} must define a boolean nsfw")
    if not isinstance(source, str):
        raise TypeError(f"Configuration {name!r} must define a string source")
    if not isinstance(fields_value, list):
        raise TypeError(f"Configuration {name!r} must define a list of string fields")
    fields: list[str] = []
    for field in cast(list[object], fields_value):
        if not isinstance(field, str):
            raise TypeError(
                f"Configuration {name!r} must define a list of string fields"
            )
        fields.append(field)

    return RequestConfig(name, limit, offset, nsfw, source, fields)
