# Written by: Przemyslaw Skryjomski
# Precision, recall evaluation metrics added - Samantha
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

# Prepare utilities
utils = Utils()
features = FeatureExtraction(utils)

data = Dataset(train_data, train_rel)
data.read(utils)

# Enable features in this order: Przemek, Samantha, Chathuri
features_state = [True, False, False]

m_accuracy = 0
m_fmeasure = 0

for i in range(kCV):
    print("-> ", i + 1, " / ", kCV, " Fold", sep = '')

    # Do a 60/40 split
    train, test = utils.do_split(data, 0.6, seed = i)

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
print("Precision:          ", round(utils.get_precision(test_key_Y, test_Y), 2), "%", sep = '')
print("Recall:         ", round(utils.get_recall(test_key_Y, test_Y), 2), "%", sep = '')