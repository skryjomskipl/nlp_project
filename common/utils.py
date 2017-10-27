# Written by: Przemyslaw Skryjomski

from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import sklearn.metrics as skl_metrics

import nltk
from nltk.tag.perceptron import PerceptronTagger

import random
import copy

class Utils:
    levels = {}
    pos_tagger = None
    stopwords = None

    def __init__(self):
        # Prepare levels
        self.levels["USAGE"] = 1
        self.levels["RESULT"] = 2
        self.levels["MODEL-FEATURE"] = 3
        self.levels["PART_WHOLE"] = 4
        self.levels["TOPIC"] = 5
        self.levels["COMPARE"] = 6
        self.pos_tagger = PerceptronTagger()
        self.stopwords = nltk.corpus.stopwords.words('english')
    
    def get_level_from_name(self, name):
        return self.levels[name]

    def get_level_from_id(self, id):
        for i in self.levels:
            if self.levels[i] == id:
                return i

        return None

    def get_classifier(self, name):
        if name == "Decision Tree":
            return tree.DecisionTreeClassifier(criterion = "entropy", random_state = 1)
        elif name == "Naive Bayes":
            return GaussianNB()
        elif name == "SVM":
            return SVC(C = 10)
        else:
            print("Unknown classifier name provided!")
            return None
    
    def get_stopwords(self):
        return self.stopwords
    
    def get_pos_tags(self, tokens):
        tagset = None
        return nltk.tag._pos_tag(tokens, tagset, self.pos_tagger)
    
    def get_feature_from_pos_tagger(self, tag):
        tags = [
            'CC', 'CD', 'DT', 'EX', 'FW', 'IN', 'JJ', 'JJR', 'JJS', 'LS',
            'MD', 'NN', 'NNS', 'NNP', 'NNPS', 'PDT', 'POS', 'PRP', 'PRP$', 'RB',
            'RBR', 'RBS', 'RP', 'SYM', 'TO', 'UH', 'VB', 'VBD', 'VBG', 'VBN',
            'VBP', 'VBZ', 'WDT', 'WP', 'WP$', 'WRB'
        ]

        if not tag in tags:
            return 0
        else:
            return tags.index(tag) + 1
    
    def get_accuracy(self, y_true, y_pred):
        return skl_metrics.accuracy_score(y_true, y_pred)*100
    
    def get_fmeasure(self, y_true, y_pred):
        return skl_metrics.f1_score(y_true, y_pred, average = 'macro') * 100

    def do_split(self, data, train_perc, seed = 0):
        if train_perc >= 1 or train_perc <= 0:
            print("Error, train equals ", train_perc, ", must be in (0, 1) range. Bailing out.", sep = '')
            quit()

        # Randomize
        tmp_data = copy.deepcopy(data)

        random.seed(seed)
        random.shuffle(tmp_data.relation)

        # Copy training set
        train = copy.deepcopy(tmp_data)

        # Copy training set to test set
        test = copy.deepcopy(tmp_data)

        # Split
        train_start = round(len(train.relation) * train_perc)
        train_end = len(train.relation)
        del train.relation[train_start:train_end]

        test_start = 0
        test_end = round(len(test.relation) * train_perc)
        del test.relation[test_start:test_end]

        return train, test
