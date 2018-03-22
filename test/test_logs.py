import sys
from os import getcwd
path = getcwd()
if path not in sys.path:
    sys.path.insert(0, path)
from logs import logger
import pytest


def test_log_rotation():
    logger.info("In test log rotation")
    assert True
