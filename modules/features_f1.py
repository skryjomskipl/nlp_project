# Features #1
#

import nltk

class FeaturesF1:
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

        # An example of a pathetic feature, word distance:
        distance = min(b)-max(a)
        X.append(distance)

        # Prepare data for the POS tagging
        tokens = []

        for obj in abstract.obj:
            tokens.append(obj.value)
        
        tokens_pos = nltk.pos_tag(tokens)

        # Using a POS tagger for both entities
        # Taking only into account last word of the entity sequence

        a_id = max(a)
        b_id = max(b)
        a_pos = tokens_pos[a_id][1]
        b_pos = tokens_pos[b_id][1]

        # Include POS tags into a feature vector
        X.append(self.utils.get_feature_from_pos_tagger(a_pos))
        X.append(self.utils.get_feature_from_pos_tagger(b_pos))

        # NOTE: Taking into account 'reverse' in any way in this task seems to hurt performance as of now.
        #       Maybe later we can do something with this...

        return X
