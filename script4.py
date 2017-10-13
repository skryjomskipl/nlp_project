# Subtask 1.1 - kCV (new)
#

from dataset import *
from common import *
from modules import *
import code
import copy
import random

train_data = 'data/subtask11/new/1.1.text.xml'
train_rel = 'data/subtask11/new/1.1.relations.txt'
kCV = 5

data = Dataset(train_data, train_rel)
data.read()

# Prepare utilities
utils = Utils()
features = FeatureExtraction(utils)

# Enable features in this order: Przemek, Samantha, Chathuri
features_state = [True, False, False]

m_accuracy = 0
m_fmeasure = 0

for i in range(kCV):
    print("-> ", i + 1, " / ", kCV, " Fold", sep = '')

    # Copy dataset
    train = copy.deepcopy(data)
    test = copy.deepcopy(data)

    # Randomize
    random.seed(i)
    random.shuffle(train.relation)
    test.relation = copy.deepcopy(train.relation)

    # Do a 60/40 split
    train_start = round(len(train.relation) * 0.6)
    train_end = len(train.relation)
    del train.relation[train_start:train_end]

    test_start = round(len(test.relation) * 0.4)
    test_end = len(test.relation)
    del test.relation[test_start:test_end]

    # Create training set
    features.set_dataset(train)
    train_X, train_Y = features.prepare_data(features_state)

    # Prepare vectors
    features.set_dataset(test)
    test_X, test_Y = features.prepare_data(features_state, test_dataset = True)

    # Classify
    clf = utils.get_classifier("Decision Tree")
    clf = clf.fit(train_X, train_Y)
    test_Y = clf.predict(test_X)

    # Compute accuracy
    features.set_dataset(test)
    test_key_Y = features.get_dataset_key()

    # Get results
    m_accuracy += utils.get_accuracy(test_key_Y, test_Y)
    m_fmeasure += utils.get_fmeasure(test_key_Y, test_Y)

# Get results
m_accuracy = round(m_accuracy/kCV, 2)
m_fmeasure = round(m_fmeasure/kCV, 2)

print("\n=> Metrics")
print("Accuracy:          ", m_accuracy, "%", sep = '')
print("F-Measure:         ", m_fmeasure, "%", sep = '')
