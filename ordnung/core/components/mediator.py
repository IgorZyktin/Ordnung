# -*- coding: utf-8 -*-

"""Component binding class, allows non direct linking between components.
"""
from typing import Any, Optional, Dict, TypeVar, Iterable

SomeComponent = TypeVar('SomeComponent')
Mapping = Dict[str, SomeComponent]


class Mediator:
    """Component binding class, allows non direct linking between components.

    Note that this component is supposed to exist in only one instance
    (though it is not a singleton). Main concern here is garbage collection,
    because we're using strong links here. Mediator is created only to store
    permanent objects.
    """
    MAX_NAMES_ON_STR = 3

    def __init__(self, initial: Optional[Mapping] = None,
                 allow_overwrite: bool = False):
        """Initialize instance.
        """
        self.allow_overwrite = allow_overwrite
        self._storage: Mapping = initial or {}

    def __str__(self) -> str:
        """Return textual representation.
        """
        names = sorted(self.keys())
        total = len(names)

        if total > self.MAX_NAMES_ON_STR:
            half = self.MAX_NAMES_ON_STR // 2
            string = (f'len={total}, '
                      + ', '.join(f'"{x}"' for x in names[:half])
                      + ', ..., '
                      + ', '.join(f'"{x}"' for x in names[-half:]))

        elif total > 0:
            string = ', '.join(f'"{x}"' for x in names)

        else:
            string = ''

        return f'{self.name}({string})'

    def __repr__(self) -> str:
        """Return textual representation.
        """
        return f'{self.name}(allow_overwrite={self.allow_overwrite})'

    def __contains__(self, name: str) -> bool:
        """Return True if we have something with this name inside.
        """
        return name in self._storage

    def __iter__(self) -> Iterable[str]:
        """Iterate over keys.
        """
        return iter(self._storage)

    def __getitem__(self, name: str) -> SomeComponent:
        """Get object with this name.
        """
        try:
            value = self._storage[name]
            return value
        except KeyError:
            raise KeyError(f'{self.name} does not '
                           f'have component named "{name}"')

    def __getattr__(self, name: str) -> SomeComponent:
        """Same as __getitem__.
        """
        try:
            value = self._storage[name]
            return value
        except KeyError:
            raise AttributeError(f'{self.name} does not '
                                 f'have component named "{name}"')

    def __len__(self) -> int:
        """Return amount of elements in storage.
        """
        return len(self._storage)

    @property
    def name(self) -> str:
        """Shorthand for class name.
        """
        return type(self).__name__

    def check_type(self, name: str) -> None:
        """Ensure that name is a kind of string.
        """
        if not isinstance(name, str):
            raise TypeError(f'{self.name} works only with string-like keys')

    def register(self, name: str, component: SomeComponent) -> None:
        """Add component to storage.
        """
        self.check_type(name)
        if name in self and not self.allow_overwrite:
            raise NameError(f'{self.name} already has '
                            f'registered component named "{name}"')

        self._storage[name] = component
        setattr(self, name, component)

    def unregister(self, name: str) -> None:
        """Delete component from storage.
        """
        if name not in self:
            raise NameError(f'{self.name} does not have '
                            f'registered component named "{name}"')

        self._storage.pop(name)
        delattr(self, name)

    def get(self, name: str, default: Optional[Any] = None) -> SomeComponent:
        """Get object with this name.
        """
        return self._storage.get(name, default)

    def clear(self):
        """Delete all links to components.
        """
        self._storage.clear()

    def keys(self):
        """Get keys view.
        """
        return self._storage.keys()

    def values(self):
        """Get values view.
        """
        return self._storage.values()

    def items(self):
        """Get pairs name-object.
        """
        return self._storage.items()

    def populate(self, **kwargs) -> None:
        """Same as register, but for group of components.
        """
        for name, component in kwargs.items():
            self.register(name, component)
