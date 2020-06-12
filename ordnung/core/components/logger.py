# -*- coding: utf-8 -*-

"""Класс-обёртка для управления логгированием.
"""
import logging
from typing import Optional, Any, Union, Callable

from colorama import init, Fore
from encosttools import s_type, serialize_arguments


class Logger:
    """Класс-обёртка для управления логгированием.
    """

    def __init__(self, mediator: Mediator, logger: Optional[Any] = None):
        """Инициализировать экземпляр.
        """
        self.mediator = mediator
        self._logger = logger

    def __repr__(self) -> str:
        """Вернуть текстовое представление.
        """
        return f'{s_type(self)}({self._logger})'

    def add(self, *args, **kwargs) -> None:
        """Добавить логгер.
        """
        if self._logger is not None:
            self._logger.add(*args, **kwargs)

    def info(self, *args, **kwargs) -> None:
        """Передать в logger.info.
        """
        self.log('info', *args, **kwargs)

    def warning(self, *args, **kwargs) -> None:
        """Передать в logger.warning.
        """
        self.log('warning', *args, **kwargs)

    def critical(self, *args, **kwargs) -> None:
        """Передать в logger.critical.
        """
        self.log('critical', *args, **kwargs)

    def debug(self, *args, **kwargs) -> None:
        """Передать в logger.debug.
        """
        if self.config.DEBUG:
            self.log('debug', *args, **kwargs)

    def error(self, *args, **kwargs) -> None:
        """Передать в logger.error.
        """
        self.log('error', *args, **kwargs)

    def exception(self, *args, **kwargs) -> None:
        """Передать в logger.exception.
        """
        self.log('exception', *args, **kwargs)

    def log(self, level: Union[int, str], *args,
            print_callback: Optional[Callable] = None, **kwargs) -> None:
        """Вызов методов логгера.
        """
        print_callback = print_callback or print

        if self._logger is None:
            print_callback(
                Fore.RED + f'[NO LOGGER] {level=}, args={args}, kwargs={kwargs}' + Fore.RESET
            )
            return

        if isinstance(level, str):
            message = serialize_arguments(*args, **kwargs)
            method = getattr(self._logger, level)
            method(message)
            return

    def get_actual_logger(self):
        """Получить фактический логгер.
        """
        return self._logger
