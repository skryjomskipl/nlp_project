#written by Samantha
#used in class Features F2 word features
import nltk.collocations
import nltk.corpus
import collections

class Bigram:
    
    def get_abstract(self,text,word):
        
        for abstr in self.dataset.abstract:
           
            
            bgm    = nltk.collocations.BigramAssocMeasures()
            finder = nltk.collocations.BigramCollocationFinder.from_words(abstr.text.lower().split())
            scored = finder.score_ngrams( bgm.likelihood_ratio  )
           
        
         # Group bigrams by first word in bigram.                                        
        prefix_keys = collections.defaultdict(list)
        for key, scores in scored:
            prefix_keys[key[0]].append((key[1], scores))

        # Sort keyed bigrams by strongest association.                                  
        for key in prefix_keys:
            prefix_keys[key].sort(key = lambda x: -x[1])
           
        val = prefix_keys[word][:1]
     
        return val
     