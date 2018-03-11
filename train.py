# stdlib

# third-party
from textblob.classifiers import NaiveBayesClassifier

# local


def get_classifier():
    """
    TODO: Docstring
    """
    with open('classifier.json', 'r') as data:
        classifier = NaiveBayesClassifier(data, format="json")

    return classifier


def update_classifier(data, classifier):
    """
    TODO: Docstring
    """
    classifier.update(data)

    return classifier
