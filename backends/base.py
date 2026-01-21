"""Abstract base class for model backends."""

from abc import ABC, abstractmethod


class BaseBackend(ABC):
    """Abstract base class that all backends must implement."""

    name: str  # Unique identifier for this backend

    @abstractmethod
    def start(self) -> None:
        """Start the backend service.

        Called during Modal container startup (@modal.enter).
        Should block until the service is ready to accept requests.
        """
        pass

    @abstractmethod
    def health_check(self) -> dict:
        """Return health status for this backend.

        Returns:
            dict with at least 'status' key ('healthy', 'unhealthy', or 'degraded')
        """
        pass
