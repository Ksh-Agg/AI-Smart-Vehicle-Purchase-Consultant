"""ETL Execution Context."""

import logging

from app.etl.config import ETLSettings, etl_settings


class ETLContext:
    """Contains metadata, configuration, logger, and metrics for an ETL execution run."""

    def __init__(
        self,
        source_name: str,
        batch_size: int | None = None,
        config: ETLSettings | None = None,
    ):
        self.source_name = source_name
        self.config = config or etl_settings
        self.batch_size = batch_size or self.config.BATCH_SIZE

        # Set up logger for this source
        self.logger = logging.getLogger(f"etl.{source_name}")
        self.logger.setLevel(self.config.LOG_LEVEL)

        # Import metrics inside __init__ or dynamically to prevent circular imports
        from app.etl.utils.metrics import MetricsCollector

        self.metrics = MetricsCollector()

    def __repr__(self) -> str:
        return (
            f"<ETLContext(source_name={self.source_name!r}, "
            f"batch_size={self.batch_size}, "
            f"processed={self.metrics.get_processed_count()})>"
        )
