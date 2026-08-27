"""Catalogue database models."""

from app.db.models.catalogue import Brand, Variant, VehicleModel
from app.db.models.comfort import VariantComfortSpec
from app.db.models.connected import VariantConnectedSpec
from app.db.models.consultation import Consultation, ConsultationShortlistItem
from app.db.models.infotainment import VariantInfotainmentSpec
from app.db.models.lighting import VariantLightingSpec
from app.db.models.physical import VariantPhysicalSpec
from app.db.models.powertrain import (
    VariantChargingOption,
    VariantPowertrainSpec,
    VariantTerrainMode,
)
from app.db.models.pricing import VariantPrice
from app.db.models.safety import VariantSafetySpec

__all__ = [
    "Brand",
    "VehicleModel",
    "Variant",
    "VariantPrice",
    "VariantPowertrainSpec",
    "VariantChargingOption",
    "VariantTerrainMode",
    "VariantPhysicalSpec",
    "VariantSafetySpec",
    "VariantComfortSpec",
    "VariantInfotainmentSpec",
    "VariantLightingSpec",
    "VariantConnectedSpec",
    "Consultation",
    "ConsultationShortlistItem",
]
