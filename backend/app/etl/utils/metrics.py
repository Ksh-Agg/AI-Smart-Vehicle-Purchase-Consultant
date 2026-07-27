"""ETL Metrics Collector Utility."""

import time
from typing import Any


class MetricsCollector:
    """Collects and calculates execution metrics for an ETL pipeline run."""

    def __init__(self) -> None:
        self.extracted: int = 0
        self.transformed: int = 0
        self.validated: int = 0
        self.rejected: int = 0
        self.loaded: int = 0
        self.start_time: float = time.perf_counter()
        self.elapsed_time: float = 0.0

    def inc_extracted(self, count: int = 1) -> None:
        """Increments the extracted record count."""
        self.extracted += count

    def inc_transformed(self, count: int = 1) -> None:
        """Increments the transformed record count."""
        self.transformed += count

    def inc_validated(self, count: int = 1) -> None:
        """Increments the validated record count."""
        self.validated += count

    def inc_rejected(self, count: int = 1) -> None:
        """Increments the rejected record count."""
        self.rejected += count

    def inc_loaded(self, count: int = 1) -> None:
        """Increments the loaded record count."""
        self.loaded += count

    def get_processed_count(self) -> int:
        """Returns the total number of records that were processed (either loaded or rejected)."""
        return self.loaded + self.rejected

    def stop_timer(self) -> None:
        """Stops the run timer and records the elapsed time."""
        self.elapsed_time = time.perf_counter() - self.start_time

    @property
    def execution_time(self) -> float:
        """Returns the total elapsed execution time in seconds."""
        if self.elapsed_time == 0.0:
            return time.perf_counter() - self.start_time
        return self.elapsed_time

    @property
    def throughput(self) -> float:
        """Returns records processed per second."""
        t = self.execution_time
        if t == 0.0:
            return 0.0
        return (self.extracted) / t

    def get_report(self) -> dict[str, Any]:
        """Generates a summary report of the run metrics."""

        return {
            "extracted": self.extracted,
            "transformed": self.transformed,
            "validated": self.validated,
            "rejected": self.rejected,
            "loaded": self.loaded,
            "execution_time_seconds": round(self.execution_time, 4),
            "throughput_records_per_second": round(self.throughput, 2),
        }
