"""Decorator for handling errors that arise during the work of the bot"""
import sys
from typing import Callable


def input_error(func: Callable) -> Callable:
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(e)
        except IndexError as e:
            return e
        except KeyboardInterrupt:
            print("\nInterrupted by user!!! Data from this session was not saved")
            sys.exit()

    return inner
