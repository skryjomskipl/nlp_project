# Written by: Przemyslaw Skryjomski

# Subtask 1.1 - Split 60/40 of Development set (old)
#

from dataset import *
from common import *
from modules import *
import code
import copy
import random

# Subtask 1.1
train_data = 'data/subtask11/1.1.train.text.xml'
train_rel = 'data/subtask11/1.1.train.relations.txt'

train = Dataset(train_data, train_rel)
train.read()

# Prepare utilities
utils = Utils()
features = FeatureExtraction(utils)

# Enable features in this order: Przemek, Samantha, Chathuri
features_state = [True, False, False]

# Create training set
features.set_dataset(train)
train_X, train_Y = features.prepare_data(features_state)

# Create development set
test = copy.deepcopy(train)

# Randomize
random.seed(0)
random.shuffle(test.relation)

# Do a 60/40 split
train_start = round(len(train.relation) * 0.6)
train_end = len(train.relation)
del train.relation[train_start:train_end]

test_start = round(len(test.relation) * 0.4)
test_end = len(test.relation)
del test.relation[test_start:test_end]

# Prepare vectors
features.set_dataset(test)
test_X, test_Y = features.prepare_data(features_state, test_dataset = True)

# Classify
clf = utils.get_classifier("Decision Tree")
clf = clf.fit(train_X, train_Y)
test_Y = clf.predict(test_X)

print("\n=> Training set")
print(" -> X")
print(train_X)
print(" -> Y")
print(train_Y)
print("\n=> Development set")
print(" -> X")
print(test_X)
print(" -> Y")
print(test_Y)

# Preparing results
print("\n=> Results")
features.set_dataset(test)
features.print_results(test_Y)

# Compute accuracy
features.set_dataset(test)
test_key_Y = features.get_dataset_key()

# Get results
print("\n=> Metrics")
print("Accuracy:          ", round(utils.get_accuracy(test_key_Y, test_Y), 2), "%", sep = '')
print("F-Measure:         ", round(utils.get_fmeasure(test_key_Y, test_Y), 2), "%", sep = '')