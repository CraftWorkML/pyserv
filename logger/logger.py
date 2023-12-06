"""Module with class logging"""
import logging
import os
import sys
from typing import Optional, Mapping


class BaseLogger:
    """Base class,: accessible log levels

        - urgent;
        - error;
        - warning;
        - info;
        - critical;
        - debug;
        Switch between are now calling the above method
    Args:
        app_name:
        level:
        stacktrace_from: ...

    """
    URGENT = logging.CRITICAL + 10

    def __init__(self, app_name: str, level: Optional[int] = None,
                 stacktrace_from: Optional[int] = None):
        if not hasattr(logging, 'URGENT'):
            logging.addLevelName(self.URGENT, 'URGENT')
            logging.URGENT = self.URGENT

        if level is None:
            level = int(os.getenv('LOG_LEVEL', logging.INFO))

        self.stacktrace_from = stacktrace_from
        self.app_name = app_name

        self.logger = logging.getLogger(app_name)
        self.set_level(level)

    def set_level(self, level=logging.INFO):
        self.logger.setLevel(level)

    def getEffectiveLevel(self) -> int:
        return self.logger.getEffectiveLevel()

    def _log(self, msg, args, props=None, level=logging.DEBUG):
        args_str = ' '.join(map(str, args))
        msg = str(msg)
        msg += args_str if args_str else ''

        exc_info = True if self.stacktrace_from and level >= self.stacktrace_from else None
        if props:
            exc_info = props.pop('exc_info', exc_info)
            for k, v in props.items():
                props[k] = str(v)
            props_str = ', '.join(f'{k}: {v}' for k, v in props.items())
            msg += '; ' + props_str

        self.logger.log(level, msg, extra={'props': props or {}}, exc_info=exc_info)

    def log(self, msg, *args, level=logging.INFO, **props):
        self._log(msg, args, props, level=level)

    def __call__(self, msg, *args, **props):
        self._log(msg, args, props, level=logging.INFO)

    def urgent(self, msg, *args, **props):
        self.log(msg, args, props, level=self.URGENT)

    def critical(self, msg, *args, **props):
        self._log(msg, args, props, level=logging.CRITICAL)

    def error(self, msg, *args, **props):
        self._log(msg, args, props, level=logging.ERROR)

    def warning(self, msg, *args, **props):
        self._log(msg, args, props, level=logging.WARNING)

    def info(self, msg, *args, **props):
        self._log(msg, args, props, level=logging.INFO)

    def debug(self, msg, *args, **props):
        self._log(msg, args, props, level=logging.DEBUG)


class Logger(BaseLogger):
    """Accessible log levels:

            - urgent;
            - error;
            - warning;
            - info;
            - critical;
            - debug;
        To switch between just call above method
        Creates handler with info:
        '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
    Args:
        app_name:
        level:
        stacktrace_from: ...

    """
    def __init__(self, app_name: str, level: int = None, stacktrace_from: int = None):
        super(Logger, self).__init__(app_name, level, stacktrace_from)

        if not self.logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
                                          datefmt='%Y-%m-%d %H:%M:%S')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
