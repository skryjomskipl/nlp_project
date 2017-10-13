class FeaturesF2:
    utils = None
    dataset = None

    def __init__(self, utils, dataset):
        self.utils = utils
        self.dataset = dataset
    
    def get_features(self, rel):
        X = []

        # Prepare stuff
        abstract = self.dataset.get_abstract(rel.abstract)
        a = abstract.get_entity_ids(rel.a)
        b = abstract.get_entity_ids(rel.b)

        # TODO

        return X
