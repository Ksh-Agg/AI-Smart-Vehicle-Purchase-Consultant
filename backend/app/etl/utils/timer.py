"""ETL execution timer utility."""

import time
from types import TracebackType
from typing import Self


class ExecutionTimer:
    """A context manager to measure the execution time of ETL stages."""

    def __init__(self, name: str = "Block"):
        self.name = name
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.elapsed: float = 0.0

    def __enter__(self) -> Self:
        self.start_time = time.perf_counter()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.end_time = time.perf_counter()
        self.elapsed = self.end_time - self.start_time

    def __str__(self) -> str:
        return f"{self.name} took {self.elapsed:.4f} seconds"
