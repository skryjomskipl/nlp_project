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
            return tree.DecisionTreeClassifier()
        elif name == "Naive Bayes":
            return GaussianNB()
        elif name == "SVM":
            return SVC()
        else:
            print("Unknown classifier name provided!")
            return None
    
    def get_accuracy(self, y_true, y_pred):
        return skl_metrics.accuracy_score(y_true, y_pred)*100
    
    def get_fmeasure(self, y_true, y_pred):
        return skl_metrics.f1_score(y_true, y_pred, average = 'macro')
