"""Backend registry for model services."""

from typing import Type
from backends.base import BaseBackend

# Registry of available backends
_BACKENDS: dict[str, Type[BaseBackend]] = {}


def register_backend(cls: Type[BaseBackend]) -> Type[BaseBackend]:
    """Decorator to register a backend class.

    Usage:
        @register_backend
        class MyBackend(BaseBackend):
            name = "my-backend"
            ...
    """
    _BACKENDS[cls.name] = cls
    return cls


def get_backends() -> dict[str, Type[BaseBackend]]:
    """Get all registered backend classes."""
    return _BACKENDS.copy()


def get_backend(name: str) -> Type[BaseBackend] | None:
    """Get a specific backend class by name."""
    return _BACKENDS.get(name)
