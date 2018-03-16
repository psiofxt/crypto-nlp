# stdlib
import json

# third-party
from textblob.classifiers import NaiveBayesClassifier

# local
from logs import logger


def get_classifier():
    """
    TODO: Docstring
    """
    with open('classifier/classifier.json', 'r') as data:
        classifier = NaiveBayesClassifier(data, format="json")

    return classifier


def update_classifier(data, classifier):
    """
    TODO: Docstring
    """
    classifier.update(data)

    return classifier


def process_data(data):
    """
    TODO: Docstring
    """
    for counter, entry in enumerate(data):
        data[counter] = entry.replace('\n', '')

    current = json.load(open('classifier/classifier.json'))

    write = {}
    for entry in data:
        logger.info(entry)

        while True:
            value = input()
            if value in ['pos', 'neg']:
                break
            logger.error('Enter either "pos" or "neg"')

        write.update(
            {
                "text": entry,
                "label": value
            }
        )

    logger.info(write)
    if len(write):
        write_data(write)


def write_data(update_data):
    """
    TODO: Docstring
    """
    with open('classifier/classifier.json', 'a') as data:
        data.write(json.dumps(update_data))
        data.close()
