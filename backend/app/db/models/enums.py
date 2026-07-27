"""Database-related Enum classes."""

from enum import Enum


class FuelType(str, Enum):
    """Supported fuel types for vehicles."""

    PETROL = "PETROL"
    DIESEL = "DIESEL"
    CNG = "CNG"
    EV = "EV"
    HYBRID = "HYBRID"
    PLUGIN_HYBRID = "PLUGIN_HYBRID"


class TransmissionType(str, Enum):
    """Supported transmission types for vehicles."""

    MANUAL = "MANUAL"
    AUTOMATIC = "AUTOMATIC"
    AMT = "AMT"
    CVT = "CVT"
    DCT = "DCT"


class BodyType(str, Enum):
    """Supported vehicle body styles."""

    HATCHBACK = "HATCHBACK"
    SEDAN = "SEDAN"
    SUV = "SUV"
    MUV = "MUV"
    COUPE = "COUPE"
    CONVERTIBLE = "CONVERTIBLE"
    PICKUP = "PICKUP"


class SegmentType(str, Enum):
    """Vehicle market segments."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    PREMIUM = "PREMIUM"
    LUXURY = "LUXURY"


class DrivetrainType(str, Enum):
    """Drivetrain configuration types."""

    FWD = "FWD"
    RWD = "RWD"
    AWD = "AWD"
    FOUR_WD = "4WD"


class VehicleStatus(str, Enum):
    """Vehicle availability status."""

    ACTIVE = "ACTIVE"
    DISCONTINUED = "DISCONTINUED"
    UPCOMING = "UPCOMING"


class EmissionStandard(str, Enum):
    """Emission compliance standards."""

    BS4 = "BS4"
    BS6 = "BS6"
    BS6_PHASE2 = "BS6_PHASE2"
