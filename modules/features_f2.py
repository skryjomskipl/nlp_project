# Features #2
# This file is created by  Samantha 

import nltk
from .bigram import Bigram
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

class FeaturesF2:
    utils = None
    dataset = None
    stop_words=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
        'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
        'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
        'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
        'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
        'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
        'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
        'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here',
        'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more',
        'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
        'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']     
    
    def __init__(self, utils, dataset):
        self.utils = utils
        self.dataset = dataset
       
    
    def __first_word_after_E1(self,abstract,rel):
          #First word after the first Entity E1 but in between the entities
        
        delimeter=['.']     
        a = abstract.get_entity_ids(rel.a)
        b = abstract.get_entity_ids(rel.b)
        
        #word after Entity 1
        i = max(a)+1 
        #First word of Entity 2
        j = min(b)
         
        while i>=0:
            if abstract.obj[i].value.lower()==abstract.obj[j].value.lower():
                break
            if '.' in abstract.obj[i].value.lower():
                break 
            if abstract.obj[i].value.lower() not in FeaturesF2.stop_words:
                break   
            i=i+1  
            
        word = abstract.obj[i].value.lower()
        #print("i after--->",word)
        ps = PorterStemmer()
         
      
        #calculate bigram
        bigram = Bigram.get_abstract(self,abstract,ps.stem(word))
        if bigram:
            for x in bigram:
                bb=x[1]
        if not bigram:
                bb=0
         
        return bb
    
        
    def __first_word_before_E2(self,abstract,rel):
          #First word before the second Entity E2 but in between the entities
        
        delimeter=['.']     
        a = abstract.get_entity_ids(rel.a)
        b = abstract.get_entity_ids(rel.b)
        
        #word after Entity 1
        j = max(a)
        #First word of Entity 2
        i = min(b)-1
         
        while i>=0:
            if abstract.obj[i].value.lower()==abstract.obj[j].value.lower():
                break
            if '.' in abstract.obj[i].value.lower():
                break 
            if abstract.obj[i].value.lower() not in FeaturesF2.stop_words:
                break   
            i=i-1  
            
        word = abstract.obj[i].value.lower()
        #print("i after--->",word)
        ps = PorterStemmer()
         
      
        #calculate bigram
        bigram = Bigram.get_abstract(self,abstract,ps.stem(word))
        if bigram:
            for x in bigram:
                bb=x[1]
        if not bigram:
                bb=0
         
        return bb
    
    
    def __words_between_Entities(self,abstract,rel):
          #Other words in between the two entities
        
        delimeter=['.'] 
        a = abstract.get_entity_ids(rel.a)
        b = abstract.get_entity_ids(rel.b)
        
        ps = PorterStemmer()
        
        #word after Entity 1
        i = max(a)+1
        
        #First word of Entity 2
        j = min(b)
        words=[]
        bigram_arr=[]
        while i>=0:
            if abstract.obj[i].value.lower()==abstract.obj[j].value.lower():
                break
            if '.' in abstract.obj[i].value.lower():
                break 
            #if abstract.obj[i].value.lower() not in FeaturesF2.stop_words:
                #word = abstract.obj[i].value.lower()
                #words.append(ps.stem(word)) 
            word = abstract.obj[i].value.lower()
            words.append(ps.stem(word)) 
            i=i+1  
            
        #print (words)
        for x in words:
            bigram = Bigram.get_abstract(self,abstract,x)
            if bigram:
                for x in bigram:
                    bb=x[1]
                    bigram_arr.append(bb)
                  
            if not bigram:
                    bb=0
        #print(bigram_arr) 
        if bigram_arr:
            max_b=max(bigram_arr)
            
        if not bigram_arr:
            max_b=0
           
        return max_b
   
    def __POStypes_between_Entities(self,abstract,rel):
          # number of different POS types in between the entities
        
        delimeter=['.']
        #stop_words=[]
        #print (stop_words) 
  
        a = abstract.get_entity_ids(rel.a)
        b = abstract.get_entity_ids(rel.b)
        #print ("a:--",abstract.obj[max(a)].value.lower())
        #print ("b",abstract.obj[min(b)].value.lower())
         
        #word after Entity 1
        i = max(a)+1
        
        #First word of Entity 2
        j = min(b)
        
        #array to store the words between entities
        words=[] 
        #array to store the POS of words between entities
        postags=[]
        #POS function
        tokens = []
        
        for obj in abstract.obj:
            tokens.append(obj.value)
        
        tokens_pos = self.utils.get_pos_tags(tokens)
               
        while i>=0:
            if abstract.obj[i].value.lower()==abstract.obj[j].value.lower():
                break
            if '.' in abstract.obj[i].value.lower():
                break 
            if abstract.obj[i].value.lower() not in FeaturesF2.stop_words:
                words.append(abstract.obj[i].value.lower())
                pos=tokens_pos[i][1]
                postags.append(pos)
            
            #words.append(abstract.obj[i].value.lower())
            #pos=tokens_pos[i][1]
            #postags.append(pos)
            i=i+1      
        #count the unique POS types
        unique_POS = set(postags)
        unique_POS_count = len(unique_POS)
        #print (words)
        #print (postags)
        #print ("unique_POS_count-->",unique_POS_count)
        return unique_POS_count 
    
    def __POStypes_before_E1(self,abstract,rel):
          #number of different POS types before E1
        
        delimeter=['.']
    
        a = abstract.get_entity_ids(rel.a)
        b = abstract.get_entity_ids(rel.b)
        
        #word before Entity 1
        i = min(a)-1
         
        #array to store the words between entities
        words=[] 
        #array to store the POS of words between entities
        postags=[]
        #POS function
        tokens = []
        for obj in abstract.obj:
            tokens.append(obj.value)
        
        tokens_pos = self.utils.get_pos_tags(tokens)
               
        while i>=0:
           
            if '.' in abstract.obj[i].value.lower():
                break 
            if abstract.obj[i].value.lower() not in FeaturesF2.stop_words:
                words.append(abstract.obj[i].value.lower())
                pos=tokens_pos[i][1]
                postags.append(pos) 
            #words.append(abstract.obj[i].value.lower())
            #pos=tokens_pos[i][1]
            #postags.append(pos)
            
            i=i-1      
        #count the unique POS types
        unique_POS = set(postags)
        unique_POS_count = len(unique_POS)
        #print (words)
        #print (postags)
        #print ("unique_POS_count-->",unique_POS_count)
        return unique_POS_count 
    
    def __POStypes_after_E2(self,abstract,rel):
          #number of different POS types after E2
        
        delimeter=['.']
         
        a = abstract.get_entity_ids(rel.a)
        b = abstract.get_entity_ids(rel.b)
         
         
        #word after Entity 2
        i = max(b)+1
        
         
        #array to store the words between entities
        words=[] 
        #array to store the POS of words between entities
        postags=[]
        #POS function
        tokens = []
        for obj in abstract.obj:
            tokens.append(obj.value)
        
        tokens_pos = self.utils.get_pos_tags(tokens)
               
        while i>=0:
           
            if '.' in abstract.obj[i].value.lower():
                break 
            if abstract.obj[i].value.lower() not in FeaturesF2.stop_words:
                words.append(abstract.obj[i].value.lower())
                pos=tokens_pos[i][1]
                postags.append(pos)
            #words.append(abstract.obj[i].value.lower())
            #pos=tokens_pos[i][1]
            #postags.append(pos)
            
            i=i+1      
        #count the unique POS types
        unique_POS = set(postags)
        unique_POS_count = len(unique_POS)
        #print (words)
        #print (postags)
        #print ("unique_POS_count-->",unique_POS_count)
        return unique_POS_count 
   
    def __POStype_highest_tfidf_between_entities(self,abstract,rel):
          # POS type of the word with highest tf-idf score in between the entities
        
        delimeter=['.']
       
        a = abstract.get_entity_ids(rel.a)
        b = abstract.get_entity_ids(rel.b)
        
        #word after Entity 1
        i = max(a)+1
        
        #First word of Entity 2
        j = min(b)
        
        #array to store the words between entities
        words=[] 
        #array to store the tfidf values of the words between entities 
        tfidf=[]
         
        #POS function
        tokens = [] 
        for obj in abstract.obj:
            tokens.append(obj.value)
        
        tokens_pos = self.utils.get_pos_tags(tokens)
               
        while i>=0:
            if abstract.obj[i].value.lower()==abstract.obj[j].value.lower():
                break
            if '.' in abstract.obj[i].value.lower():
                break 
             
            if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                if abstract.tf_idf[abstract.obj[i].value.lower()]>0.02:
                  
                    tfidf.append(abstract.tf_idf[abstract.obj[i].value.lower()])
                    words.append(i)
             
            i=i+1      
         
        #print (words)  
        #print (tfidf)
        if tfidf: 
            pos=(self.utils.get_feature_from_pos_tagger(tokens_pos[tfidf.index(max(tfidf))][1]))
            #print ("POS",pos)
        if not tfidf: 
            pos= 0
         
        return pos 
    
    def __POStype_highest_tfidf_before_E1(self,abstract,rel):
          # POS type of the word with highest tf-idf score in before E1
        
        delimeter=['.']
       
        a = abstract.get_entity_ids(rel.a)
         
        #word before Entity 1
        i = min(a)+1
      
        #array to store the words between entities
        words=[] 
        #array to store the tfidf values of the words between entities 
        tfidf=[]
         
        #POS function
        tokens = [] 
        for obj in abstract.obj:
            tokens.append(obj.value)
        
        tokens_pos = self.utils.get_pos_tags(tokens)
               
        while i>=0:
        
            if '.' in abstract.obj[i].value.lower():
                break 
             
            if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                if abstract.tf_idf[abstract.obj[i].value.lower()]>0.02:
                  
                    tfidf.append(abstract.tf_idf[abstract.obj[i].value.lower()])
                    words.append(i)
             
            i=i-1      
         
        #print (words)  
        #print (tfidf)
        if tfidf: 
            pos=(self.utils.get_feature_from_pos_tagger(tokens_pos[tfidf.index(max(tfidf))][1]))
            #print ("POS",pos)
        if not tfidf:
            
            pos= 0
         
        return pos 
    
    def __POStype_highest_tfidf_after_E2(self,abstract,rel):
          # POS type of the word with highest tf-idf score after_E2
        
        delimeter=['.'] 
        b = abstract.get_entity_ids(rel.b)
        
        
        #word after Entity 2
        i = max(b)+1
        
        #array to store the words between entities
        words=[] 
        #array to store the tfidf values of the words between entities 
        tfidf=[]
         
        #POS function
        tokens = [] 
        for obj in abstract.obj:
            tokens.append(obj.value)
        
        tokens_pos = self.utils.get_pos_tags(tokens)
               
        while i>=0: 
            if '.' in abstract.obj[i].value.lower():
                break 
             
            if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                if abstract.tf_idf[abstract.obj[i].value.lower()]>0.02:
                  
                    tfidf.append(abstract.tf_idf[abstract.obj[i].value.lower()])
                    words.append(i)
             
            i=i+1      
         
        #print (words)  
        #print (tfidf)
        if tfidf: 
            pos=(self.utils.get_feature_from_pos_tagger(tokens_pos[tfidf.index(max(tfidf))][1]))
            #print ("POS",pos)
        if not tfidf: 
            pos= 0
         
        return pos 
    
    def get_features(self, rel):
        X = []
        # Prepare stuff
        abstract = self.dataset.get_abstract(rel.abstract)
         
        #first_word_after_E1=self.__first_word_after_E1(abstract,rel)
        #X.append(  first_word_after_E1)
        
        #first_word_before_E2=self.__first_word_before_E2(abstract,rel)
        #X.append(  first_word_before_E2)
        
        #words_between_Entities=self.__words_between_Entities(abstract,rel)
        #X.append(  words_between_Entities)
        
        POStypes_between_Entities=self.__POStypes_between_Entities(abstract,rel)
        X.append(  POStypes_between_Entities)
        
        POStypes_before_E1=self.__POStypes_before_E1(abstract,rel)
        #X.append(  POStypes_before_E1)
        
        POStypes_after_E2=self.__POStypes_after_E2(abstract,rel)
        #X.append(  POStypes_after_E2)
        
        POStype_highest_tfidf_between_entities=self.__POStype_highest_tfidf_between_entities(abstract,rel)
        #X.append(  POStype_highest_tfidf_between_entities)
        
        POStype_highest_tfidf_before_E1=self.__POStype_highest_tfidf_before_E1(abstract,rel)
        #X.append(  POStype_highest_tfidf_before_E1)
        
        POStype_highest_tfidf_after_E2=self.__POStype_highest_tfidf_after_E2(abstract,rel)
        #X.append(  POStype_highest_tfidf_after_E2)
       
        return X
