# stdlib
import logging
from logging.config import dictConfig

logging_config = dict(
    version = 1,
    formatters = {
        'f': {'format':
              '%(asctime)s [%(levelname)s] %(message)s'}
        },
    handlers = {
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.INFO}
        },
    root = {
        'handlers': ['h'],
        'level': logging.INFO,
        },
)
dictConfig(logging_config)
logger = logging.getLogger()

import sys
from os import getcwd
path = getcwd()
if path not in sys.path:
    sys.path.insert(0, path)

# third-party
import pytest

# local
from classifier.train import get_classifier


@pytest.fixture()
def fixture_classifier():
    classifier = get_classifier()
    return classifier


@pytest.fixture()
def fixture_test_set():
    test_set = [
        ('Litecoin is good', 'pos'),
        ('Litecoin is bad', 'neg'),
        ('Litecoin appears to be crashing', 'neg')
    ]
    return test_set


@pytest.mark.accuracy
def test_accuracy(fixture_classifier, fixture_test_set):
    accuracy = fixture_classifier.accuracy(fixture_test_set)
    logger.info(f'Accuracy is: {accuracy}')

    assert accuracy > .8
