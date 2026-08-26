# Data Source Onboarding Guide

This guide explains how to integrate a new vehicle data source into the SVPC ETL framework. By using a decoupled, registry-based architecture, adding a new source does not require writing custom pipelines, scrapers, or database logic. It only requires defining a mapping configuration.

---

## Step 1: Analyze the Data Source
Identify the columns/fields present in your raw data (CSV, JSON, or Excel) and locate their corresponding canonical targets in the [Master Dataset Field Dictionary](master-dataset-field-dictionary.md).

*Example: Raw CSV Columns*
- `Car_Name` -> Maps to `vehicle.model`
- `Variant_Name` -> Maps to `vehicle.variant`
- `Year_Of_Mfg` -> Maps to `vehicle.year`
- `ExShowroomPrice` -> Maps to `vehicle.price_ex_showroom`
- `Engine_Displacement` -> Maps to `engine_spec.engine_cc`

---

## Step 2: Define a Source Mapping Configuration
Create a new configuration file under `app/etl/mapping/mappings/` (e.g., `app/etl/mapping/mappings/cardekho.py`) and declare the mapping config:

```python
from app.etl.mapping.schema import SourceMappingConfig

cardekho_mapping = SourceMappingConfig(
    source_name="cardekho",
    field_map={
        "Car_Name": "vehicle.model",
        "Variant_Name": "vehicle.variant",
        "Year_Of_Mfg": "vehicle.year",
        "ExShowroomPrice": "vehicle.price_ex_showroom",
        "Engine_Displacement": "engine_spec.engine_cc",
        "Body_Style": "vehicle.body_type",
        "Fuel": "vehicle.fuel_type",
        "Gearbox": "vehicle.transmission",
        "Seating": "vehicle.seating_capacity",
    },
    defaults={
        "brand.name": "Unknown",  # Default if brand name is not in CSV
        "brand.country": "India",
        "environmental_spec.emission_standard": "BS6_PHASE2",
    }
)
```

---

## Step 3: Register the Mapping Configuration
Register the source mapping in the mapping registry so the pipeline can discover it.
Update `app/etl/mapping/mappings/__init__.py` to import and register the mapping:

```python
from app.etl.mapping.registry import mapping_registry
from app.etl.mapping.mappings.cardekho import cardekho_mapping

mapping_registry.register(cardekho_mapping)
```

---

## Step 4: Run the ETL Pipeline
With the mapping registered, you can now instantiate the pipeline and pass your raw file. The pipeline automatically extracts, standardizes, validates, and loads the data:

```python
from app.etl import ETLPipeline
from app.etl.extract import CSVExtractor

# Initialize the pipeline for the registered source 'cardekho'
pipeline = ETLPipeline(source_name="cardekho", extractor=CSVExtractor())

# Execute the pipeline with a path to your raw file
report = pipeline.run("data/raw/cardekho_raw.csv")

print(f"ETL Execution Summary: {report}")
```
---

## Key Customizations

### 1. Custom Extractor
If the raw source data is in a format not supported by the default extractors (CSV, JSON, Excel), you can implement a custom extractor by subclassing `BaseExtractor` and implementing its `extract()` method:

```python
from app.etl.extract import BaseExtractor
from typing import Any, Iterable

class XMLExtractor(BaseExtractor):
    def extract(self, file_path: str) -> Iterable[dict[str, Any]]:
        # Implement custom XML extraction logic here
        # Yield dictionary rows
        pass
```

### 2. Custom Transformer
If the default transformer (`DefaultTransformer`) cannot handle unique parsing rules for this specific source, subclass it to override specific fields:

```python
from app.etl.transform import DefaultTransformer
from typing import Any

class CarDekhoTransformer(DefaultTransformer):
    def transform(self, mapped_record: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
        # Call super().transform() to get base normalization
        normalized = super().transform(mapped_record)
        
        # Add custom rules here
        # e.g., custom mapping of model name strings
        return normalized
```
Pass your custom transformer when subclassing or run it explicitly before validation.

---

## Related Documentation
- [ETL Architecture Specification](../architecture/etl-architecture.md)
- [Master Dataset Field Dictionary](master-dataset-field-dictionary.md)
