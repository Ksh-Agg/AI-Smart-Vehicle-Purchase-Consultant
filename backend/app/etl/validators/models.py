"""ETL Validation Report models."""

from pydantic import BaseModel, Field


class ValidationErrorDetail(BaseModel):
    """Represents a single validation error on a specific record and field."""

    row_index: int
    field: str
    error_type: str
    message: str


class ValidationReport(BaseModel):
    """Holds all validation failures accumulated during a run."""

    errors: list[ValidationErrorDetail] = Field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        """Returns True if no errors were found."""
        return len(self.errors) == 0

    def add_error(
        self, row_index: int, field: str, error_type: str, message: str
    ) -> None:
        """Helper to append a new validation error detail."""
        self.errors.append(
            ValidationErrorDetail(
                row_index=row_index,
                field=field,
                error_type=error_type,
                message=message,
            )
        )
