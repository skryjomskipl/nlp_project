# Written by: Przemyslaw Skryjomski

from dataset import *
from .features_f1 import FeaturesF1
from .features_f2 import FeaturesF2
from .features_f3 import FeaturesF3

class FeatureExtraction:
    dataset = None
    utils = None

    def __init__(self, utils):
        self.utils = utils
    
    def set_dataset(self, dataset):
        self.dataset = dataset
    
    def get_dataset_key(self):
        Y = []

        for rel in self.dataset.relation:
            type = self.utils.get_level_from_name(rel.type)
            Y.append(type)
        
        return Y
    
    def print_results(self, pred_Y):
        count = 0

        for rel in self.dataset.relation:
            type = self.utils.get_level_from_id(pred_Y[count])
            reverse = ""

            if rel.reverse:
                reverse = ",REVERSE"

            print(type, "(", rel.abstract, ".", rel.a, ",", rel.abstract, ".", rel.b, reverse, ")", sep = '')

            count += 1

    def prepare_data(self, features_state, test_dataset = False):
        X = []
        Y = []

        # Prepare features
        f1 = None
        f2 = None
        f3 = None

        if features_state[0]:
            f1 = FeaturesF1(self.utils, self.dataset)
        
        if features_state[1]:
            f2 = FeaturesF2(self.utils, self.dataset)
        
        if features_state[2]:
            f3 = FeaturesF3(self.utils, self.dataset)

        for rel in self.dataset.relation:
            # Extract features
            features = []

            # [1] Features Przemek
            if f1:
                features += f1.get_features(rel)

            # [2] Features Samantha
            if f2:
                features += f2.get_features(rel)

            # [3] Features Chathuri
            if f3:
                features += f3.get_features(rel)
    
            # Append features
            X.append(features)

            # Append label
            if not test_dataset:
                y = self.utils.get_level_from_name(rel.type)
                Y.append(y)

        return X, Y
