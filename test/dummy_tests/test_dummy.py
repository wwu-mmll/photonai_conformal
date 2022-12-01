from unittest import TestCase
import numpy as np

from project_name.dummy.DummyTransformer import DummyTransformer


class DummyTest(TestCase):

    def setUp(self) -> None:
        # do setup stuff
        pass

    def test_fit(self):
        dt = DummyTransformer()
        X = np.random.rand(10, 10)
        dt.fit(X)
        X_t = dt.transform(X)
        self.assertTrue(np.array_equal(X, X_t))
