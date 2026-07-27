"""ETL Schema Mapping Package."""

from app.etl.mapping.registry import mapping_registry
from app.etl.mapping.schema import SourceMappingConfig

__all__ = ["SourceMappingConfig", "mapping_registry"]
