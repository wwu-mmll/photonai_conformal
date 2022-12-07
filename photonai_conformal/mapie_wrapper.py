from abc import ABC
import numpy as np
import itertools
from sklearn.base import BaseEstimator, RegressorMixin, ClassifierMixin

from mapie.classification import MapieClassifier
from mapie.regression import MapieRegressor


class MapieWrapper(ABC, BaseEstimator):

    def __init__(self):
        self.clf = NotImplementedError
        self.alpha = None

    def fit(self, X, y):
        self.clf.fit(X, y)
        return self

    def predict(self, X, **kwargs):
        raise NotImplementedError()


class ConformalClassifier(MapieWrapper, ClassifierMixin):
    def __init__(self,
                 estimator=None,
                 method="score",
                 cv=None,
                 n_jobs=None,
                 random_state=None,
                 verbose=0,
                 alpha=None):
        """
        Wrapper for conformal classification.For parameter details see
        [mapie docs](https://mapie.readthedocs.io/en/latest/generated/mapie.classification.MapieClassifier.html#mapie-classification-mapieclassifier)
        Parameters
        ----------
        estimator
        method
        cv
        n_jobs
        random_state
        verbose
        alpha
        """
        super(ConformalClassifier, self).__init__()
        self.estimator = estimator
        self.method = method
        self.n_jobs = n_jobs
        self.random_state = random_state
        self.verbose = verbose
        self.alpha = alpha
        self.clf = MapieClassifier(estimator=estimator,
                                   method=method,
                                   cv=cv,
                                   n_jobs=n_jobs,
                                   random_state=random_state,
                                   verbose=verbose)

    def predict(self, X, **kwargs):
        if not self.alpha and 'alpha' not in kwargs:
            return self.clf.predict(X)
        else:
            alpha_vals = self.alpha.copy() if self.alpha else kwargs['alpha']
            preds_orig, y_pis = self.clf.predict(X, alpha=alpha_vals)
            preds = np.stack([preds_orig[:]]*y_pis.shape[1], axis=-1)[..., None]  # dims
            output = np.append(y_pis, preds, axis=-1)  # preds are at [..., -1]
            alpha_vals.append('y_pred')
            final_preds = np.array([tuple(output[row, c_ps, alpha] for alpha, c_ps in
                                          itertools.product(range(len(alpha_vals)), range(output.shape[1]))) for row in
                                    range(output.shape[0])],
                                   dtype=[(str(key) + ul, np.float64) for key, ul in
                                          itertools.product(alpha_vals, [f'_{i}_ps' for i in range(output.shape[1])])])
            # remove double y_pred entry
            pred_names = list(final_preds.dtype.names[:-2])
            final_preds = final_preds[pred_names]
            pred_names = pred_names[:-1]
            pred_names.append('y_pred')
            final_preds.dtype.names = tuple(pred_names)
            if 'return_internals_testing' in kwargs:
                return final_preds, preds_orig, y_pis
            return final_preds


class ConformalRegressor(MapieWrapper, RegressorMixin):
    def __init__(self,
                 estimator=None,
                 method="plus",
                 cv=None,
                 n_jobs=None,
                 agg_function="mean",
                 verbose=0,
                 conformity_score=None,
                 alpha=None):
        """
        Wrapper for conformal regression. For parameter details see
        [mapie docs](https://mapie.readthedocs.io/en/latest/generated/mapie.regression.MapieRegressor.html#mapie.regression.MapieRegressor)
        Parameters
        ----------
        estimator
        method
        cv
        n_jobs
        agg_function
        verbose
        conformity_score
        alpha
        """
        super(ConformalRegressor, self).__init__()
        self.estimator = estimator
        self.method = method
        self.cv = cv
        self.n_jobs = n_jobs
        self.agg_function = agg_function
        self.verbose = verbose
        self.conformity_score = conformity_score
        self.alpha = alpha
        self.clf = MapieRegressor(estimator=estimator,
                                  method=method,
                                  cv=cv,
                                  n_jobs=n_jobs,
                                  agg_function=agg_function,
                                  verbose=verbose,
                                  conformity_score=conformity_score)

    def predict(self, X, **kwargs):
        if not self.alpha and 'alpha' not in kwargs:
            return self.clf.predict(X)
        else:
            alpha_vals = self.alpha.copy() if self.alpha else kwargs['alpha']
            preds, y_pis = self.clf.predict(X, alpha=alpha_vals)
            preds = np.stack((preds[:], preds[:]), axis=-1)[..., None]  # dims
            output = np.append(y_pis, preds, axis=-1)  # preds are at [..., -1]
            alpha_vals.append('y_pred')
            final_preds = np.array([tuple(output[row, upper_lower, alpha] for alpha, upper_lower in
                            itertools.product(range(0, len(alpha_vals)), [0, 1])) for row in range(output.shape[0])],
                     dtype=[(str(key) + ul, np.float64) for key, ul in
                            itertools.product(alpha_vals, ['_lower', '_upper'])])
            # remove double y_pred entry
            pred_names = list(final_preds.dtype.names[:-1])
            final_preds = final_preds[pred_names]
            pred_names = pred_names[:-1]
            pred_names.append('y_pred')
            final_preds.dtype.names = tuple(pred_names)
            return final_preds
