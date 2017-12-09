# Features #F2
# Written by  Samantha 

import nltk
from common import *
from .bigram import Bigram
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

class FeaturesF2:
    utils = None
    dataset = None 
    
    def __init__(self, utils, dataset):
        self.utils = utils
        self.dataset = dataset
        #define the stop words used in stop word removal
        self.stop_words=['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
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
      
    
    def __first_word_after_E1(self,abstract,rel,flag):
          #Bigram of the first word after the first Entity E1 but in between the entities
          #flag: 1- with stop words, 0 -without stop words
        delimeter=['.']     
        a = abstract.get_entity_ids(rel.a)
        b = abstract.get_entity_ids(rel.b)
        
        #word after Entity 1
        i = max(a)+1 
        #First word of Entity 2
        j = min(b)
         
        while i>=0:
            #checks whether word equals to the first word of the entity 2
            if abstract.obj[i].value.lower()==abstract.obj[j].value.lower():
                break
            #Checks whether it is the end of the sentence
            if '.' in abstract.obj[i].value.lower():
                break 
            #stop words removed
            if flag == 1:
                if abstract.obj[i].value.lower() not in self.stop_words:
                    break  
            i=i+1  
            
        word = abstract.obj[i].value.lower()
        #lemmatization
        ps = PorterStemmer()
      
        #calculate bigram
        bigram = Bigram.get_abstract(self,abstract,ps.stem(word)) 
        if bigram:
            for x in bigram:
                bb=x[1]
        if not bigram:
                bb=0
         
        return bb
    
        
    def __first_word_before_E2(self,abstract,rel,flag):
          #Bigram of the First word before the second Entity E2 but in between the entities
        
        delimeter=['.']     
        a = abstract.get_entity_ids(rel.a)
        b = abstract.get_entity_ids(rel.b)
        
        #word after Entity 1
        j = max(a)
        #First word of Entity 2
        i = min(b)-1
         
        while i>=0:
            #checks whether word equals to the first word of the entity 2
            if abstract.obj[i].value.lower()==abstract.obj[j].value.lower():
                break
            #Checks whether it is the end of the sentence
            if '.' in abstract.obj[i].value.lower():
                break 
            #stop words removed
            if flag == 1:
                if abstract.obj[i].value.lower() not in self.stop_words:
                    break
                     
            i=i-1  
            
        word = abstract.obj[i].value.lower()
        #lemmatization
        ps = PorterStemmer()
         
      
        #calculate bigram
        bigram = Bigram.get_abstract(self,abstract,ps.stem(word)) 
        if bigram:
            for x in bigram:
                bb=x[1]
        if not bigram:
                bb=0
         
        return bb
    
    
    def __words_between_Entities(self,abstract,rel,flag):
          #Highest bigram value of the words in between entities
        
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
            #stop words removed
            if flag == 1:
                if abstract.obj[i].value.lower() not in self.stop_words:
                    word = abstract.obj[i].value.lower()
                    words.append(ps.stem(word)) 
                 
            #stop words not removed
            if flag == 0:
                word = abstract.obj[i].value.lower()
                words.append(ps.stem(word)) 
                 
            i=i+1  
            
        #calculate bigram
        for x in words:
            bigram = Bigram.get_abstract(self,abstract, x)
            if bigram:
                for x in bigram:
                    bb=x[1]
                    bigram_arr.append(bb)
                  
            if not bigram:
                    bb=0
        #select the word that produces highest bigram value
        if bigram_arr:
            max_b=max(bigram_arr)
            
        if not bigram_arr:
            max_b=0
           
        return max_b
   
    def __POStypes_between_Entities(self,abstract,rel,flag):
          # number of unique POS types in between the entities
        
        delimeter=['.']
        a = abstract.get_entity_ids(rel.a)
        b = abstract.get_entity_ids(rel.b)
        
        #word after Entity 1
        i = max(a)+1
        
        #First word of Entity 2
        j = min(b)
        
        #array to store the words between entities
        words=[] 
        #array to store the POS of words between entities
        postags=[]
        #Apply POS function
        tokens = []
        
        for obj in abstract.obj:
            tokens.append(obj.value)
        
        tokens_pos = self.utils.get_pos_tags(tokens)
               
        while i>=0:
            if abstract.obj[i].value.lower()==abstract.obj[j].value.lower():
                break
          
            #stop when sentence ends
            if '.' in abstract.obj[i].value.lower():
                break 
            #stop words removed
            if flag == 1:
                if abstract.obj[i].value.lower() not in self.stop_words:
                    words.append(abstract.obj[i].value.lower())
                    pos=tokens_pos[i][1]
                    postags.append(pos)
                  
             #stop words not removed
            if flag == 0:
                words.append(abstract.obj[i].value.lower())
                pos=tokens_pos[i][1]
                postags.append(pos)
                
            i=i+1      
       
        #count the unique POS types
        unique_POS = set(postags)
        unique_POS_count = len(unique_POS)
        
        return unique_POS_count 
    
    def __POStypes_before_E1(self,abstract,rel,flag):
          #number of unique POS types before E1
        
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
            #stop when sentence ends
            if '.' in abstract.obj[i].value.lower():
                break 
             #stop words removed
            if flag == 1:
                if abstract.obj[i].value.lower() not in self.stop_words:
                    words.append(abstract.obj[i].value.lower())
                    pos=tokens_pos[i][1]
                    postags.append(pos)
                     
             #stop words not removed
            if flag == 0:
                words.append(abstract.obj[i].value.lower())
                pos=tokens_pos[i][1]
                postags.append(pos)
                 
            
            i=i-1      
       
        #count the unique POS types
        unique_POS = set(postags)
        unique_POS_count = len(unique_POS)
         
        return unique_POS_count 
    
    def __POStypes_after_E2(self,abstract,rel,flag):
          #number of unique POS types after E2
        
        delimeter=['.']
    
        a = abstract.get_entity_ids(rel.a)
        b = abstract.get_entity_ids(rel.b)
        
        #word after E2
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
            #stop when sentence ends
            if i == len(abstract.obj) or'.' == abstract.obj[i].value.lower() :
                break 
             #stop words removed
            if flag == 1:
                if abstract.obj[i].value.lower() not in self.stop_words:
                    words.append(abstract.obj[i].value.lower())
                    pos=tokens_pos[i][1]
                    postags.append(pos)
                    
             #stop words not removed
            if flag == 0:
                words.append(abstract.obj[i].value.lower())
                pos=tokens_pos[i][1]
                postags.append(pos) 
            
            i=i+1 
           
        #count the unique POS types
        unique_POS = set(postags)
        unique_POS_count = len(unique_POS)
         
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
            #stop when sentence ends
            if '.' in abstract.obj[i].value.lower():
                break 
            #select words with tfidf value higher than 0.02 
            if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                if abstract.tf_idf[abstract.obj[i].value.lower()]>0.02:
                  
                    tfidf.append(abstract.tf_idf[abstract.obj[i].value.lower()])
                    words.appenget_abstractd(i)
             
            i=i+1      
         
        if tfidf: 
            pos=(self.utils.get_feature_from_pos_tagger(tokens_pos[tfidf.index(max(tfidf))][1]))
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
            #stop when sentence ends
            if '.' in abstract.obj[i].value.lower():
                break 
            #select words with tfidf value higher than 0.02  
            if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                if abstract.tf_idf[abstract.obj[i].value.lower()]>0.02:
                  
                    tfidf.append(abstract.tf_idf[abstract.obj[i].value.lower()])
                    words.append(i)
             
            i=i-1      
     
        if tfidf: 
            pos=(self.utils.get_feature_from_pos_tagger(tokens_pos[tfidf.index(max(tfidf))][1]))
          
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
            #stop when sentence ends
            if i == len(abstract.obj) or'.' in abstract.obj[i].value.lower():
                break 
             #select words with tfidf value higher than 0.02 
            if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                if abstract.tf_idf[abstract.obj[i].value.lower()]>0.02:
                  
                    tfidf.append(abstract.tf_idf[abstract.obj[i].value.lower()])
                    words.append(i)
             
            i=i+1      
       
        if tfidf: 
            pos=(self.utils.get_feature_from_pos_tagger(tokens_pos[tfidf.index(max(tfidf))][1]))
            #print ("POS",pos)
        if not tfidf: 
            pos= 0
         
        return pos 
    
    def get_features(self, rel):
        #All features implemented are mentioned here
        X = []
        abstract = self.dataset.get_abstract(rel.abstract)
        
        #Bigram of the first word after E1 without stop words
        first_word_after_E1=self.__first_word_after_E1(abstract,rel,0)
        X.append(  first_word_after_E1)
        #Bigram of the first word after E1 with stop words
        first_word_after_E1=self.__first_word_after_E1(abstract,rel,1)
        X.append(  first_word_after_E1)
        
        #Bigram of the first word before E2 without stop words
        first_word_before_E2=self.__first_word_before_E2(abstract,rel,0)
        X.append(  first_word_before_E2)
        #Bigram of the first word before E2 with stop words
        first_word_before_E2=self.__first_word_before_E2(abstract,rel,1)
        X.append(  first_word_before_E2)
        
        #Highest bigram value of words in between entities without stop words
        words_between_Entities=self.__words_between_Entities(abstract,rel,0)
        X.append(  words_between_Entities)
        #Highest bigram value of words in between entities - with stop words
        words_between_Entities=self.__words_between_Entities(abstract,rel,1)
        X.append(  words_between_Entities)
        
        #number of unique POS types in between the entities  without stop words
        POStypes_between_Entities=self.__POStypes_between_Entities(abstract,rel,0)
        X.append(  POStypes_between_Entities)
        #number of unique POS types in between the entities - with stop words
        POStypes_between_Entities=self.__POStypes_between_Entities(abstract,rel,1)
        X.append(  POStypes_between_Entities)
        
        #number of unique POS types Entity1 (E1) without stop words
        POStypes_before_E1=self.__POStypes_before_E1(abstract,rel,0)
        X.append(  POStypes_before_E1)
        #number of unique POS types Entity1 (E1) - with stop words
        POStypes_before_E1=self.__POStypes_before_E1(abstract,rel,1)
        X.append(  POStypes_before_E1)
       
        #number of unique POS types Entity 2 (E2) - without stop words
        POStypes_after_E2=self.__POStypes_after_E2(abstract,rel,0)
        X.append(  POStypes_after_E2)
        #number of unique POS types Entity 2 (E2) - with stop words
        POStypes_after_E2=self.__POStypes_after_E2(abstract,rel,1)
        X.append(  POStypes_after_E2)
        
        #POS type of the word with highest tf-idf score in between the entities 
        POStype_highest_tfidf_between_entities=self.__POStype_highest_tfidf_between_entities(abstract,rel)
        X.append(  POStype_highest_tfidf_between_entities)
        #POS type of the word with highest tf-idf score in before Entity1 (E1) 
        POStype_highest_tfidf_before_E1=self.__POStype_highest_tfidf_before_E1(abstract,rel)
        X.append(  POStype_highest_tfidf_before_E1)
        #POS type of the word with highest tf-idf score in after Entity 2 (E2)
        POStype_highest_tfidf_after_E2=self.__POStype_highest_tfidf_after_E2(abstract,rel)
        X.append(  POStype_highest_tfidf_after_E2)
      
       
        return X
