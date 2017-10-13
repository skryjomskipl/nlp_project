# Subtask 1.1 - Test set (old)
#

from dataset import *
from common import *
from modules import *

# Subtask 1.1
train_data = 'data/subtask11/1.1.train.text.xml'
train_rel = 'data/subtask11/1.1.train.relations.txt'

test_data = 'data/subtask11/1.1.test.text.xml'
test_rel = 'data/subtask11/1.1.test.relations.txt'
test_key = 'data/subtask11/1.1.test.key.txt'

train = Dataset(train_data, train_rel)
train.read()

test = Dataset(test_data, test_rel, test_dataset = True)
test.read()

test_key = Dataset(test_data, test_key)
test_key.read()

# Prepare utilities
utils = Utils()
features = FeatureExtraction(utils)

# Enable features in this order: Przemek, Samantha, Chathuri
features_state = [True, False, False]

# Create training set
features.set_dataset(train)
train_X, train_Y = features.prepare_data(features_state)

# Create test set
features.set_dataset(test)
test_X, test_Y = features.prepare_data(features_state, test_dataset = True)

# TODO: You can provide development set by randomizing/shuffling training set.
#       Then you need to alter of course code below.

# Classify
clf = utils.get_classifier("Decision Tree")
clf = clf.fit(train_X, train_Y)
test_Y = clf.predict(test_X)

print("\n=> Training set")
print(" -> X")
print(train_X)
print(" -> Y")
print(train_Y)
print("\n=> Testing set")
print(" -> X")
print(test_X)
print(" -> Y")
print(test_Y)

# Preparing results
print("\n=> Results")
features.set_dataset(test)
features.print_results(test_Y)

# Compute accuracy
features.set_dataset(test_key)
test_key_Y = features.get_dataset_key()

print("\n=> Metrics")
print("Accuracy:          ", round(utils.get_accuracy(test_key_Y, test_Y), 2), "%", sep = '')
print("F-Measure:         ", round(utils.get_fmeasure(test_key_Y, test_Y), 2), "%", sep = '')