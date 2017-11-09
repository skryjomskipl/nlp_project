# Written by: Przemyslaw Skryjomski
# Precision, recall evaluation metrics added - Samantha
# Subtask 1.1 - Split 60/40 (new)
#

from dataset import *
from common import *
from modules import *
from modules.bigram import Bigram
import code
import copy
import random

train_data = 'data/subtask11/new/1.1.text.xml'
train_rel = 'data/subtask11/new/1.1.relations.txt'

# Prepare utilities
utils = Utils()
features = FeatureExtraction(utils)
bigram = Bigram(utils)
train = Dataset(train_data, train_rel)
train.read(utils)

# Enable features in this order: Przemek, Samantha, Chathuri
features_state = [True, False, False]

# Do a 60/40 split
train, test = utils.do_split(train, 0.6, seed = 0)

# Create training set
features.set_dataset(train)
tfIdfCalculator.set_dataset(train)
s=tfIdfCalculator.calc_ifidf_data()
bigram.set_dataset(train)
b=bigram.calc_bigram()
train_X, train_Y = features.prepare_data(features_state)

# Prepare vectors
features.set_dataset(test)
tfIdfCalculator.set_dataset(test)
s=tfIdfCalculator.calc_ifidf_data()
bigram.set_dataset(test)
b=bigram.calc_bigram()
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
print("Precision:          ", round(utils.get_precision(test_key_Y, test_Y), 2), "%", sep = '')
print("Recall:         ", round(utils.get_recall(test_key_Y, test_Y), 2), "%", sep = '')