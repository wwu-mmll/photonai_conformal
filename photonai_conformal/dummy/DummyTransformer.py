from sklearn.base import BaseEstimator, TransformerMixin


class DummyTransformer(BaseEstimator, TransformerMixin):

    def __init__(self, dummy_hp: int = None):
        """Dummy Transformer, based on Dummy et al. 2022

        Please give examples!

        Parameters
        ----------
        dummy_hp: int,default=None
            Explanation of the dummy hyperparameter

        Examples
        --------
        Usage with PHOTONAI Now
        ```python
            import stuff

            hp = Hyperpipe()
            hp += PipelineElement("DummyTransformer", dummy)
        ```

        Notes
        -----
        This is only a dummy classifier!
        """
        self.dummy_hp = dummy_hp

    def fit(self, X=None, y=None):
        return self

    def transform(self, X):
        # this function woul normally handle the transformation...
        return X
