"""Schema mapping configuration model."""

from typing import Any
from pydantic import BaseModel, Field


class SourceMappingConfig(BaseModel):
    """Configuration mapping raw source fields to canonical schema attributes."""

    source_name: str
    # Map raw field name -> target path (e.g. "brand.name", "vehicle.model", "engine_spec.engine_cc")
    field_map: dict[str, str] = Field(default_factory=dict)
    # Default values for fields that are missing in raw source (e.g. "environmental_spec.emission_standard": "BS6")
    defaults: dict[str, Any] = Field(default_factory=dict)

    def map_record(self, raw_record: dict[str, Any]) -> dict[str, dict[str, Any]]:
        """Maps a raw flat dictionary into structured category dictionaries.

        Returns:
            A dictionary with keys: 'brand', 'vehicle', 'engine_spec', etc.
            each containing mapped key-value pairs ready to be normalized/validated.
        """
        # Initialize the categories exactly matching the canonical model fields
        mapped: dict[str, dict[str, Any]] = {
            "brand": {},
            "vehicle": {},
            "engine_spec": {},
            "dimension_spec": {},
            "safety_spec": {},
            "feature_spec": {},
            "ownership_spec": {},
            "availability_spec": {},
            "environmental_spec": {},
        }

        # Apply mapped values
        for raw_key, value in raw_record.items():
            if raw_key in self.field_map:
                target_path = self.field_map[raw_key]
                if "." in target_path:
                    category, field = target_path.split(".", 1)
                    if category in mapped:
                        mapped[category][field] = value
                else:
                    # Default fallback: attribute of vehicle
                    mapped["vehicle"][target_path] = value

        # Apply defaults for any missing keys in mapped categories
        for target_path, default_val in self.defaults.items():
            if "." in target_path:
                category, field = target_path.split(".", 1)
                if category in mapped and field not in mapped[category]:
                    mapped[category][field] = default_val

        return mapped
