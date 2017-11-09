from dataset import *
import nltk.collocations
import nltk.corpus
import collections


class Bigram:
    dataset = None
    utils = None

    def __init__(self, utils):
        self.utils = utils
        self.prefix_keys = []
        self.bigrams=[]
    def set_dataset(self, dataset):
        self.dataset = dataset
    
   
    def calc_bigram(self, test_dataset = False):
        
        for abstr in self.dataset.abstract:
            #print("Abstract---->", abstr.text)
            
            bgm    = nltk.collocations.BigramAssocMeasures()
            finder = nltk.collocations.BigramCollocationFinder.from_words(abstr.text.lower().split())
            scored = finder.score_ngrams( bgm.likelihood_ratio  )
            # Group bigrams by first word in bigram.                                        
        self.prefix_keys = collections.defaultdict(list)
        for key, scores in scored:
            self.prefix_keys[key[0]].append((key[1], scores))
        
       
        return self.prefix_keys
    
    def get_bigram(self, word):
         
        # Sort keyed bigrams by strongest association.                                  
        print ("array  ",self.prefix_keys)
        
        for key in self.prefix_keys:
            self.prefix_keys[key].sort(key = lambda x: -x[1])
        
        val = self.prefix_keys[word][:1]
       
        return val