# Utilities

from sklearn import tree
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
import sklearn.metrics as skl_metrics

class Utils:
    levels = {}

    def __init__(self):
        # Prepare levels
        self.levels["USAGE"] = 1
        self.levels["RESULT"] = 2
        self.levels["MODEL-FEATURE"] = 3
        self.levels["PART_WHOLE"] = 4
        self.levels["TOPIC"] = 5
        self.levels["COMPARE"] = 6
    
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
