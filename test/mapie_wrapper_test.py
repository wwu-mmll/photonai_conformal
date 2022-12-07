from photonai_conformal.mapie_wrapper import ConformalClassifier, ConformalRegressor
from sklearn.gaussian_process import GaussianProcessRegressor, GaussianProcessClassifier
from sklearn.datasets import load_diabetes, load_iris
import numpy as np
from mapie.classification import MapieClassifier
from mapie.regression import MapieRegressor
from unittest import TestCase


class ConformalTests(TestCase):

    def test_regressor_basic(self):
        X, y = load_diabetes(return_X_y=True)
        reg = ConformalRegressor(estimator=GaussianProcessRegressor()).fit(X, y)
        baseline = MapieRegressor(estimator=GaussianProcessRegressor()).fit(X, y)

        reg_preds = reg.predict(X)
        baseline_preds = baseline.predict(X)
        self.assertTrue(np.array_equal(reg_preds, baseline_preds))

    def test_regressor_advanced_nonequal(self):
        X, y = load_diabetes(return_X_y=True)
        reg = ConformalRegressor(estimator=GaussianProcessRegressor(), alpha=[.5]).fit(X, y)
        baseline = MapieRegressor(estimator=GaussianProcessRegressor()).fit(X, y)

        reg_preds = reg.predict(X)
        baseline_preds = baseline.predict(X, alpha=[.5])
        self.assertTrue(np.array_equal(reg_preds['y_pred'], baseline_preds[0]))
        self.assertTrue(np.array_equal(reg_preds['0.5_lower'], baseline_preds[1][:, 0, 0]))
        self.assertTrue(np.array_equal(reg_preds['0.5_upper'], baseline_preds[1][:, 1, 0]))

    def test_classifier_basic(self):
        X, y = load_iris(return_X_y=True)
        novel = ConformalClassifier(estimator=GaussianProcessClassifier()).fit(X, y)
        baseline = MapieClassifier(estimator=GaussianProcessClassifier()).fit(X, y)

        novel_preds = novel.predict(X)
        baseline_preds = baseline.predict(X)
        self.assertTrue(np.array_equal(novel_preds, baseline_preds))

    def test_classifier_advanced_nonequal(self):
        X, y = load_iris(return_X_y=True)
        novel = ConformalClassifier(estimator=GaussianProcessClassifier(),
                                    alpha=[.2, .3, .5, .9],
                                    random_state=43,
                                    method='naive').fit(X, y)

        novel_preds, y_pred, y_pis = novel.predict(X, return_internals_testing=True)
        self.assertTrue(np.array_equal(novel_preds['y_pred'], y_pred))
        self.assertTrue(np.array_equal(novel_preds['0.2_0_ps'], y_pis[:, 0, 0]))
        self.assertTrue(np.array_equal(novel_preds['0.2_1_ps'], y_pis[:, 1, 0]))
