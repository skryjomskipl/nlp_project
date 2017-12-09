# Uberscript for SemEval 2018 Project
# Written by Przemyslaw Skryjomski (skryjomskipl)
#

from dataset import *
from common import *
from modules import *
import argparse
import copy
import random

class Uberclass:
    # Private
    __args = {}
    __train_xml = ''
    __train_txt = ''
    __fp_output = None
    __fp_results = None
    __features_state = [True, False, False]
    __train_perc = 0.6
    __kcv = 5
    __classifier = "SVM"
    __data = None
    __utils = None
    __features = None

    # Private
    def __log(self, *arg):
        if self.__args.verbose:
            print(*arg, sep = '', end = '\n')
    
    def __print_o(self, fmt, *arg):
        str = fmt.format(*arg) + "\n"

        if self.__fp_output:
            self.__fp_output.write(str)
        else:
            print(str, sep = '', end = '')

    def __print_r(self, fmt, *arg):
        str = fmt.format(*arg) + "\n"

        if self.__fp_results:
            self.__fp_results.write(str)
        else:
            print(str, sep = '', end = '')

    def __load_dataset(self):
        self.__log("Dataset:   ", self.__train_xml)
        self.__log("Relations: ", self.__train_txt)

        self.__utils = Utils()
        self.__features = FeatureExtraction(self.__utils)

        self.__data = Dataset(self.__train_xml, self.__train_txt)
        self.__data.read(self.__utils)

    def __subtask11_pre(self):
        self.__train_xml = 'data/subtask11/new/1.1.text.xml'
        self.__train_txt = 'data/subtask11/new/1.1.relations.txt'

    def __subtask2_pre(self):
        self.__train_xml = 'data/subtask11/new/1.1.text.xml'
        self.__train_txt = 'data/subtask11/new/1.1.relations.txt'
    
    def __subtask11_post(self):
        # k-Fold Cross Validation for Subtask 1.1
        accuracy = 0
        fmeasure = 0
        accuracy_directionality = 0
        sensitivity_directionality = 0
        specificity_directionality = 0
        gmean_directionality = 0

        for i in range(self.__kcv):
            self.__log("-> ", i + 1, " / ", self.__kcv, " Fold")

            # [1] Relation classification task

            # Do a 60/40 split
            train, test = self.__utils.do_split(self.__data, self.__train_perc, seed = i)

            # Create training set
            self.__features.set_dataset(train)
            train_X, train_Y = self.__features.prepare_data(self.__features_state)

            # Prepare vectors
            self.__features.set_dataset(test)
            test_X, test_Y = self.__features.prepare_data(self.__features_state, test_dataset = True)

            # Classify
            clf = self.__utils.get_classifier(self.__classifier)
            clf = clf.fit(train_X, train_Y)
            test_Y = clf.predict(test_X)

            # Check if we are calculating baseline
            if self.__args.baseline:
                test_Y = [1] * len(test_Y)
            
            # Compute accuracy
            self.__features.set_dataset(test)
            test_key_Y = self.__features.get_dataset_key()

            # Get results
            accuracy += self.__utils.get_accuracy(test_key_Y, test_Y)
            fmeasure += self.__utils.get_fmeasure(test_key_Y, test_Y)

            # [2] Directionality classification task

            # Create training set
            self.__features.set_dataset(train)
            train_X, train_Y = self.__features.prepare_data(self.__features_state, test_dataset = False, directionality = True)

            # Prepare vectors
            self.__features.set_dataset(test)
            test_X, test_directionality_Y = self.__features.prepare_data(self.__features_state, test_dataset = True, directionality = True)

            # Classify
            clf = self.__utils.get_classifier(self.__classifier)
            clf = clf.fit(train_X, train_Y)
            test_directionality_Y = clf.predict(test_X)

            # Check if we are calculating baseline
            if self.__args.baseline:
                test_directionality_Y = [0] * len(test_directionality_Y)
            
            # Compute accuracy
            test_key_Y = []
            for rel in test.relation:
                if rel.reverse:
                    test_key_Y.append(1)
                else:
                    test_key_Y.append(0)

            # Get results
            accuracy_directionality += self.__utils.get_accuracy(test_key_Y, test_directionality_Y)
            sensitivity_directionality += self.__utils.get_sensitivity_tc(test_key_Y, test_directionality_Y)
            specificity_directionality += self.__utils.get_specificity_tc(test_key_Y, test_directionality_Y)
            gmean_directionality += self.__utils.get_gmean_tc(test_key_Y, test_directionality_Y)

            # [3] Print SemEval output
            count = 0
            for rel in test.relation:
                type = self.__utils.get_level_from_id(test_Y[count])
                reverse = ""

                if test_directionality_Y[count]:
                    reverse = ",REVERSE"

                self.__print_o("{:s}({:s}.{:s},{:s}.{:s}{:s})", type, rel.abstract, rel.a, rel.abstract, rel.b, reverse)
                count += 1

            self.__print_o("")
            
        # Average results
        accuracy /= self.__kcv
        fmeasure /= self.__kcv
        accuracy_directionality /= self.__kcv
        sensitivity_directionality /= self.__kcv
        specificity_directionality /= self.__kcv
        gmean_directionality /= self.__kcv

        # Print them!
        self.__print_r("Classification task:")
        self.__print_r("Accuracy:    {:f}", accuracy)
        self.__print_r("F-Measure:   {:f}", fmeasure)
        self.__print_r("")
        self.__print_r("Directionality task:")
        self.__print_r("Accuracy:    {:f}", accuracy_directionality)
        self.__print_r("Sensitivity: {:f}", sensitivity_directionality)
        self.__print_r("Specificity: {:f}", specificity_directionality)
        self.__print_r("GMean:       {:f}", gmean_directionality)
    
    def __subtask2_post(self):
        print("Subtask 2 is not implemented yet in this front-end.")

    def __private_call(self, name):
        mangled_name = "_" + self.__class__.__name__ + "__" + name
        getattr(self, mangled_name)()

    # Public
    def subtask(self):
        self.__private_call(self.__args.subtask + "_pre")
        
        # Custom training set
        if self.__args.input:
            self.__train_xml = self.__args.input[0]
            self.__train_txt = self.__args.input[1]

        if self.__args.output:
            self.__fp_output = open(self.__args.output, mode = 'w')
        
        if self.__args.output_results:
            self.__fp_results = open(self.__args.output_results, mode = 'w')

        if self.__args.features:
            if not self.__args.przemek:
                self.__features_state[0] = False

            if not self.__args.chathuri:
                self.__features_state[1] = False
            
            if not self.__args.samantha:
                self.__features_state[2] = False
        
        if self.__args.kcv:
            self.__kcv = int(self.__args.kcv)
            if self.__kcv <= 0:
                print("Wrong kCV value provided!")
                return
        
        if self.__args.classifier:
            classifier = self.__args.classifier

            if classifier == "decision_tree":
                classifier = "Decision Tree"
            elif classifier == "svm":
                classifier = "SVM"
            elif classifier == "naive_bayes":
                classifier = "Naive Bayes"
            
            self.__classifier = classifier

        if self.__args.train_perc:
            self.__train_perc = float(self.__args.train_perc)
        
        if self.__train_perc >= 1:
            print("Wrong training or test subset value provided for kCV.")
            return

        self.__load_dataset()
        self.__private_call(self.__args.subtask + "_post")

        if self.__fp_output:
            self.__fp_output.close()
        
        if self.__fp_results:
            self.__fp_results.close()

    def __init__(self):
        parser = argparse.ArgumentParser(description = 'SemEval 2018 Task 7: Semantic Relation Extraction and Classification in Scientific Papers')
        parser.add_argument('subtask', help = 'Subtask to be processed', choices = ['subtask11', 'subtask2'], action = 'store')
        parser.add_argument('-l', '--classifier', help = 'Selects classifier', choices = ['decision_tree', 'svm', 'naive_bayes'], action = 'store')
        parser.add_argument('-b', '--baseline', help = 'Enable calculating baseline', action = 'store_true')
        parser.add_argument('-k', '--kcv', help = 'Number of folds for kCV', metavar = '5')
        parser.add_argument('-n', '--train-perc', help = 'Percentage of train subset (must be lower than 1.0)', metavar = '0.6')
        parser.add_argument('-f', '--features', help = 'Enable custom feature extractor selection', action = 'store_true')
        parser.add_argument('-p', '--przemek', help = 'Enable feature extractor 1', action = 'store_true')
        parser.add_argument('-s', '--samantha', help = 'Enable feature extractor 2', action = 'store_true')
        parser.add_argument('-c', '--chathuri', help = 'Enable feature extractor 3', action = 'store_true')
        parser.add_argument('-i', '--input', help = 'Custom dataset for building model', nargs = 2, metavar = ('dataset.xml', 'relations.txt'))
        parser.add_argument('-o', '--output', help = 'Output file for storing predictions', metavar = 'predict.txt')
        parser.add_argument('-r', '--output-results', help = 'Output file for storing results (calculated metrics)', metavar = 'results.txt')
        parser.add_argument('-v', '--verbose', help = 'Enables verbose mode for debugging', action = 'store_true')
        self.__args = parser.parse_args()

uberclass = Uberclass()
uberclass.subtask()
