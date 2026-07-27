"""Registry-based mapping configurations storage."""

from app.etl.exceptions import MappingError
from app.etl.mapping.schema import SourceMappingConfig


class MappingRegistry:
    """Registry managing source field mapping configurations."""

    def __init__(self) -> None:
        self._registry: dict[str, SourceMappingConfig] = {}

    def register(self, config: SourceMappingConfig) -> None:
        """Registers a new source mapping configuration."""
        if config.source_name in self._registry:
            raise MappingError(
                f"Mapping configuration for source '{config.source_name}' is already registered."
            )
        self._registry[config.source_name] = config

    def get(self, source_name: str) -> SourceMappingConfig:
        """Retrieves a registered source mapping configuration."""
        if source_name not in self._registry:
            raise MappingError(
                f"No mapping configuration registered for source '{source_name}'."
            )
        return self._registry[source_name]

    def clear(self) -> None:
        """Clears all registrations."""
        self._registry.clear()


mapping_registry = MappingRegistry()
