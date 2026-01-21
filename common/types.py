"""Shared types and protocols for model backends."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class HealthCheckable(Protocol):
    """Protocol for services that can report health status."""

    def health_check(self) -> dict:
        """Return health status dict with at least 'status' key."""
        ...


@runtime_checkable
class Startable(Protocol):
    """Protocol for services that need explicit startup."""

    def start(self) -> None:
        """Start the service."""
        ...
