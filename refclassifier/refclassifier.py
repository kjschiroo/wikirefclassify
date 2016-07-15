from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC


class Error(Exception):
    pass


class NotTrainedError(Error):
    pass


def _ensure_trained(func):
    def wrapper(*args, **kwargs):
        if args[0]._vectorizer is None or args[0]._clf is None:
            raise NotTrainedError
        return func(*args, **kwargs)
    return wrapper


class RefClassifier(object):

    def __init__(self, transformer):
        self._transformer = transformer
        self._vectorizer = None
        self._clf = None

    def train(self, refs, labels):
        self._vectorizer = TfidfVectorizer(min_df=5)
        trans_refs = [self._transformer(ref) for ref in refs]
        X = self._vectorizer.fit_transform(trans_refs)
        self._clf = LinearSVC().fit(X, labels)

    @_ensure_trained
    def predict(self, refs):
        trans_refs = [self._transformer(ref) for ref in refs]
        X = self._vectorizer.transform(trans_refs)
        return self._clf.predict(X)
