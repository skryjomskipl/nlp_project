# Written by: Chathuri
#feeding the result for feature selection
from dataset import *
import math
from textblob import TextBlob as tb
from .featureCollection import FeatureCollection


class FeatureRoot:
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
        bloblist=[]
        # Prepare features
        fc = None
        fc = FeatureCollection(self.utils, self.dataset)
        #for each relation run for all the features and send data to classifier later in feature selection file        
        for rel in self.dataset.relation:
            
            # Extract features
            features = []            
            features += fc.get_features(rel)
    
            # Append features
            X.append(features)

            # Append label
            if not test_dataset:
                y = self.utils.get_level_from_name(rel.type)
                Y.append(y)

        return X, Y
