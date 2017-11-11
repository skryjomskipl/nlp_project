# This file is create by Chathuri 
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

class FeatureCollection:
    utils = None
    dataset = None    
    stop_words=None
    
    def __init__(self, utils, dataset):
        self.utils = utils
        self.dataset = dataset
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

    def __feature (self, abstract, rel):
        #word before E1 with lematization        
        ps = PorterStemmer()
        abstract = self.dataset.get_abstract(rel.abstract)   
        
        #print("rel.abstract-> ", rel.abstract)
        tokens = []
        tokens2 = []
        for obj in abstract.obj:
            tokens.append(obj.value)
                   
        a = abstract.get_entity_ids(rel.a) 
        
        word_list=[];
        word_count=0;
        i=min(a)-1;
        while i>=0:            
            if abstract.obj[i].value=='.':
                break 
            if '.' in abstract.obj[i].value and abstract.obj[i].value not in self.stop_words:
                word_list.append(abstract.obj[i].value)                
                word_count=+1
                break 
            #if abstract.obj[i].value in stop_words:
                #stop_word_count+=1;
            #if  abstract.obj[i].value not in stop_words:
            if abstract.obj[i].value not in self.stop_words: 
                word_list.append(abstract.obj[i].value)             
                word_count=word_count+1
            if word_count==1:
                break
            i=i-1
            
        if len(word_list)==1:
            return int.from_bytes(word_list[0].encode(), 'little')
            #print("-> ", word_list[0])
        if len(word_list)!=1:
            return 0
        
    def __noOf_words_beforeE1(self,abstract,rel,flag):
         #Number of words before E1 in the full sentance. (Feature2)
            #Calc if-idf val
        noOfWords=0;
        delimeter=['.']
        ps = PorterStemmer()       
        str_id=0
        stop_word_count=0        
        a = abstract.get_entity_ids(rel.a)         
        i=min(a)-1;
        while i>=0:
            if abstract.obj[i].value=='.':
                str_id=i+1;
                break
            if '.' in abstract.obj[i].value:                
                str_id=i;
                break 
            if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                if flag==1:
                    if abstract.tf_idf[abstract.obj[i].value.lower()]<0.02:
                        stop_word_count+=1;
                        i=i-1
                        continue
            if (abstract.obj[i].value.lower()) in self.stop_words:
                stop_word_count+=1;
            
                #break   
            i=i-1    
        return (min(a)-str_id)-stop_word_count  
    
    
    def __noOf_words_afterE2(self,abstract,rel,flag):
         #Number of words after E2 in the full sentance.(Feature3)
        #print("rel>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>");
        noOfWords=0;
        delimeter=['.']
        ps = PorterStemmer()
        stop_word_count=0
        
        b = abstract.get_entity_ids(rel.b) 
        #print("rel=",abstract.id)
        #print("rel.b=",rel.b)
        i=max(b)+1;
        str_id=max(b)+1;
        #print("i=",i)
        while i<len(abstract.obj):#??
            #print("abstract.obj[i].value=",abstract.obj[i].value)
            if abstract.obj[i].value=='.':
                str_id=i-1;
                break 
            if '.' in abstract.obj[i].value:
                str_id=i;
                break
            if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                if flag==1:
                    if abstract.tf_idf[abstract.obj[i].value.lower()]<0.02:
                        stop_word_count+=1;
                        i=i+1
                        continue
            if (abstract.obj[i].value.lower()) in self.stop_words or abstract.obj[i].value in [',',';']:
                stop_word_count+=1;                  
            i=i+1
            str_id=i 
        #print("value= ",(str_id-max(b))-stop_word_count)
        return (str_id-max(b))-stop_word_count
    
    
    def __wordBeforE1 (self, abstract, rel):
        #word before E1 (featur 6)
        a = abstract.get_word_beforeE1(rel.a) 
        ps = PorterStemmer()
        
        word_no=min(a)-1
        word=""       
        count=0
        i=min(a)-1
        word=0
        
        while i>=0:
            if abstract.obj[i].value :
                if abstract.obj[i].value=='.':                    
                    break 
                if ps.stem(abstract.obj[i].value.lower()) not in self.stop_words and abstract.obj[i].value not in [',','-',';']: #add the list
                    
                    word=ps.stem(abstract.obj[i].value.lower())
                    word=int.from_bytes(word.encode(), 'little')
                    break
                else:
                    i=i-1
       
        return word
        #return 0
    
    def __wordAfterE2(self, abstract, rel):
        #word before E1 (featur 6)
        b = abstract.get_word_beforeE1(rel.b) 
        ps = PorterStemmer()
        
        word=0
        i=max(b)+1;
        str_id=max(b)+1;
        #print("i=",i)
        while i<len(abstract.obj):#
            if abstract.obj[i].value :
                if abstract.obj[i].value=='.':                    
                    break 
                if ps.stem(abstract.obj[i].value.lower()) not in self.stop_words and abstract.obj[i].value not in [',','-',';']: #add the list
                    word=abstract.obj[i].value
                    word=int.from_bytes(word.encode(), 'little')
                    break
                else:
                    i=i+1
       
        return word  
    
    def __POS_beforeE1(self, abstract, rel,flag):
        # checking pos tag of words before E1 , window size=2
        abstract = self.dataset.get_abstract(rel.abstract)   
        ps = PorterStemmer()
        tokens = []
        for obj in abstract.obj:
            tokens.append(obj.value)
        
        tokens_pos = nltk.pos_tag(tokens)        
        noOfWords=0;
        delimeter=['.']
        
        str_id=0
        stop_word_count=0
        out = [];
        
        a = abstract.get_entity_ids(rel.a) 
        
        word_list=[];
        word_count=0;
        i=min(a)-1;
        while i>=0:            
            if abstract.obj[i].value=='.':
                break 
            if '.' in abstract.obj[i].value:
                word_list.append(i)                
                word_count=word_count+1
                break 
            if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                if flag==1:
                    if abstract.tf_idf[abstract.obj[i].value.lower()]<0.02:
                        stop_word_count+=1;
                        i=i-1
                        continue    
            word_list.append(i);            
            word_count=word_count+1
            if word_count==2:
                break
            i=i-1
        #self.utils.get_feature_from_pos_tagger(tokens_pos[word_list[0]][1])
        if len(word_list)==2:
            out.append(self.utils.get_feature_from_pos_tagger(tokens_pos[word_list[0]][1]))
            out.append(self.utils.get_feature_from_pos_tagger(tokens_pos[word_list[1]][1]))
        if len(word_list)==1:
            out.append(self.utils.get_feature_from_pos_tagger(tokens_pos[word_list[0]][1]))
            out.append(0)
        if len(word_list)==0:
            out.append(0)
            out.append(0)
        
       
       
        return out
    
    def __POS_AfterE2(self, abstract, rel,flag):
        # checking pos tag of words before E1 , window size=2
        
        abstract = self.dataset.get_abstract(rel.abstract)   
        ps = PorterStemmer()
        tokens = []
        for obj in abstract.obj:
            tokens.append(obj.value)
        
        tokens_pos = nltk.pos_tag(tokens)        
        noOfWords=0;
        delimeter=['.']
        
        str_id=0
        stop_word_count=0
        out = [];
        
        b = abstract.get_entity_ids(rel.b) 
        
        word_list=[]
        word_count=0
        i=max(b)+1
        while i<len(abstract.obj):#
            #print("bstract.obj[i].value=",abstract.obj[i].value)
            if abstract.obj[i].value=='.':                
                break 
            if '.' in abstract.obj[i].value:                    
                word_list.append(i)                
                word_count=word_count+1
                #print("added")
                break  
            if (abstract.obj[i].value.lower()) not in self.stop_words and abstract.obj[i].value not in [',','-',';']: #add the list
                if flag==1:
                    if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                        if abstract.tf_idf[abstract.obj[i].value.lower()]<0.02:
                            stop_word_count+=1;
                            i=i+1
                            continue    
                word_list.append(i)                
                word_count=word_count+1
                #print("added")
            if word_count==2:
                break
                
            i=i+1
        #self.utils.get_feature_from_pos_tagger(tokens_pos[word_list[0]][1])
        #print("loop ok")
        #print("len(word_list)=",len(word_list))
        if len(word_list)!=0:
            
            
            if len(word_list)==2:
                
                out.append(self.utils.get_feature_from_pos_tagger(tokens_pos[word_list[0]][1]))
                out.append(self.utils.get_feature_from_pos_tagger(tokens_pos[word_list[1]][1]))
                
            if len(word_list)==1:
                
                out.append(self.utils.get_feature_from_pos_tagger(tokens_pos[word_list[0]][1]))
                out.append(0)
                
        if len(word_list)==0:
            out.append(0)
            out.append(0)
            
        return out
                
    def __POS_AfterE1(self, abstract, rel,flag):
        # checking pos tag of words before E1 , window size=2
        abstract = self.dataset.get_abstract(rel.abstract)   
        ps = PorterStemmer()
        tokens = []
        for obj in abstract.obj:
            tokens.append(obj.value)
        
        tokens_pos = nltk.pos_tag(tokens)        
       
        wordIndex = 0; 
        pos=0;
        b = abstract.get_entity_ids(rel.b) 
        a = abstract.get_entity_ids(rel.a) 
       
        i=max(a)+1;
        while i<len(abstract.obj):
            
            if abstract.obj[i].value :
                if abstract.obj[i].value=='.':                    
                    break 
                if '.' in abstract.obj[i].value:                    
                    wordIndex=i 
                    break  
                if abstract.obj[i].value.lower() not in self.stop_words and abstract.obj[i].value not in [',','-',';']: #add the list                
                    if flag==1:
                        if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                            if abstract.tf_idf[abstract.obj[i].value.lower()]<0.02:                        
                                i=i+1
                                continue 
                    wordIndex=i 
                    break                  
                i=i+1
        
        if wordIndex!=0:            
            pos=(self.utils.get_feature_from_pos_tagger(tokens_pos[wordIndex][1]))
        return pos
    
    def __POS_BeforeE2(self, abstract, rel,flag):
        # checking pos tag of words before E1 , window size=2
        abstract = self.dataset.get_abstract(rel.abstract)   
        ps = PorterStemmer()
        tokens = []
        for obj in abstract.obj:
            tokens.append(obj.value)
        
        tokens_pos = nltk.pos_tag(tokens)        
       
        wordIndex = 0; 
        pos=0;
        b = abstract.get_entity_ids(rel.b) 
        a = abstract.get_entity_ids(rel.a) 
       
        i=min(b)-1;
        while i<len(abstract.obj):
            
            if abstract.obj[i].value :
                if abstract.obj[i].value=='.':                    
                    break 
                if '.' in abstract.obj[i].value:
                    #if  abstract.obj[i].value in abstract.tf_idf.keys():
                        #if abstract.tf_idf[abstract.obj[i].value]<0.02:
                            #i=i-1
                            #continue                        
                    wordIndex=i 
                    break  
                if abstract.obj[i].value.lower() not in self.stop_words and abstract.obj[i].value not in [',','-',';']: #add the list
                    if flag==1:
                        if  abstract.obj[i].value.lower() in abstract.tf_idf.keys():
                            if abstract.tf_idf[abstract.obj[i].value.lower()]<0.02:                        
                                i=i-1
                                continue
                    wordIndex=i 
                    break                  
                i=i-1
        if wordIndex!=0:            
            pos=(self.utils.get_feature_from_pos_tagger(tokens_pos[wordIndex][1]))
            
        return pos
    ####################################################################################################
    #shamek
    def __get_sentence_objects(self, abstract, a, b):
        # NOTE:  I know that it is the most lame approach ever, but who cares... ;)

        l_id = 0
        r_id = 0
        delimiters = ['.', '!', '?']

        # Find the beginning of the sentence
        i = a
        while i >= 0:
            if len([x for x in delimiters if x in abstract.obj[i].value]) > 0:
                l_id = i + 1
                break

            i = i - 1
        
        # Find the end of sentence
        i = b

        while i < len(abstract.obj):
            if len([x for x in delimiters if x in abstract.obj[i].value]) > 0:
                r_id = i
                break

            i = i + 1
        
        objs = abstract.obj[l_id : r_id]
        a_id = a - l_id
        b_id = b - l_id

        return objs, a_id, b_id

    def __get_feature_from_rule(self, utils, objects):
        sentence = ""

        i = 0
        while i < len(objects):
            val = objects[i].value
            sentence = sentence + " " + val

            i = i + 1

        if "than" in sentence:
            return utils.get_level_from_name("COMPARE")

        if "which" in sentence:
            return utils.get_level_from_name("TOPIC")

        return 0
    ################################################################################################################
    ##sam
    
    
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
            if abstract.obj[i].value.lower() not in self.stop_words:
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
            if abstract.obj[i].value.lower() not in self.stop_words:
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
            if abstract.obj[i].value.lower() not in self.stop_words:
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
            if abstract.obj[i].value.lower() not in self.stop_words:
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
            if abstract.obj[i].value.lower() not in self.stop_words:
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
        
       
        #out=self.__POS_beforeE1(abstract,rel) 
        
        noOfWordsBeforeE1=self.__noOf_words_beforeE1(abstract,rel,0)
        X.append(noOfWordsBeforeE1)
        noOfWordsBeforeE1=self.__noOf_words_beforeE1(abstract,rel,1)
        X.append(noOfWordsBeforeE1)
        noOfWordsAfterE2=self.__noOf_words_afterE2(abstract,rel,0)
        X.append(noOfWordsAfterE2) 
        noOfWordsAfterE2=self.__noOf_words_afterE2(abstract,rel,1)
        X.append(noOfWordsAfterE2)
        wordBeforeE1=self.__wordBeforE1(abstract,rel)
        X.append(wordBeforeE1) 
        wordAfterE2=self.__wordAfterE2(abstract,rel)
        X.append(wordAfterE2) 
        posAfterE2=self.__POS_AfterE2(abstract,rel,0)
        X.append(posAfterE2[0])
        X.append(posAfterE2[1])
        posAfterE2=self.__POS_AfterE2(abstract,rel,1)
        X.append(posAfterE2[0])
        X.append(posAfterE2[1])
        posBeforeE1=self.__POS_beforeE1(abstract,rel,0)
        X.append(posBeforeE1[0])
        X.append(posBeforeE1[1])
        posBeforeE1=self.__POS_beforeE1(abstract,rel,1)
        X.append(posBeforeE1[0])
        X.append(posBeforeE1[1])
        posAfterE1=self.__POS_AfterE1(abstract,rel,0)
        X.append(posAfterE1)
       
        posAfterE1=self.__POS_AfterE1(abstract,rel,1)
        X.append(posAfterE1)
        posBeforeE2=self.__POS_BeforeE2(abstract,rel,0)        
        X.append(posBeforeE2)
        posBeforeE2=self.__POS_BeforeE2(abstract,rel,1)        
        X.append(posBeforeE2)
        
        #Shamek
        
        abstract = self.dataset.get_abstract(rel.abstract)
        #a = abstract.get_entity_ids(rel.a)
        #b = abstract.get_entity_ids(rel.b)

        # Feature 1 - Word distance between tags after lowercasing and stopwords removal
        #objs_between_entities = abstract.obj[max(a):min(b)]
        #objs_processed = [obj for obj in objs_between_entities if not obj.value.lower() in self.utils.get_stopwords()]

        #distance = len(objs_processed)
        #X.append(distance)

        # Feature 2 - POS tag of the last word in the entity sequence
        #a_id = max(a)
        #b_id = max(b)
        
        #a_pos = abstract.pos_tags[a_id][1]
        #b_pos = abstract.pos_tags[b_id][1]

        #X.append(self.utils.get_feature_from_pos_tagger(a_pos))
        #X.append(self.utils.get_feature_from_pos_tagger(b_pos))

        # NOTE: Taking into account 'reverse' in any way in this task seems to hurt performance as of now.
        #       Maybe later we can do something with this...

        # Feature 3 - Rule based extraction for boosting prediction of the less represented classes
        #objects, a_id, b_id = self.__get_sentence_objects(abstract, min(a), min(b))
        #X.append(self.__get_feature_from_rule(self.utils, objects))
        
        
        ##Samantha
        
        #first_word_after_E1=self.__first_word_after_E1(abstract,rel)
        #X.append(  first_word_after_E1)
        
        #first_word_before_E2=self.__first_word_before_E2(abstract,rel)
        #X.append(  first_word_before_E2)
        
        #words_between_Entities=self.__words_between_Entities(abstract,rel)
        #X.append(  words_between_Entities)
        
        #POStypes_between_Entities=self.__POStypes_between_Entities(abstract,rel)
        #X.append(  POStypes_between_Entities)
        
        #POStypes_before_E1=self.__POStypes_before_E1(abstract,rel)
        #X.append(  POStypes_before_E1)
        
        #POStypes_after_E2=self.__POStypes_after_E2(abstract,rel)
        #X.append(  POStypes_after_E2)
        
        #POStype_highest_tfidf_between_entities=self.__POStype_highest_tfidf_between_entities(abstract,rel)
        #X.append(  POStype_highest_tfidf_between_entities)
        
        #POStype_highest_tfidf_before_E1=self.__POStype_highest_tfidf_before_E1(abstract,rel)
        #X.append(  POStype_highest_tfidf_before_E1)
        
        #POStype_highest_tfidf_after_E2=self.__POStype_highest_tfidf_after_E2(abstract,rel)
        #X.append(  POStype_highest_tfidf_after_E2)
        
        return X
