"""Custom exceptions for the SVPC ETL framework."""


class ETLError(Exception):
    """Base exception for all ETL errors."""

    pass


class ExtractionError(ETLError):
    """Raised when data extraction fails."""

    pass


class MappingError(ETLError):
    """Raised when field mapping fails or configuration is invalid."""

    pass


class TransformationError(ETLError):
    """Raised when data transformation or normalization fails."""

    pass


class ValidationError(ETLError):
    """Raised when business or type validation fails."""

    pass


class LoadingError(ETLError):
    """Raised when database loading fails."""

    pass
