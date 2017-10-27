# Written by: Przemyslaw Skryjomski

class FeaturesF1:
    utils = None
    dataset = None

    def __init__(self, utils, dataset):
        self.utils = utils
        self.dataset = dataset
    
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
    
    def get_features(self, rel):
        X = []

        # Prepare stuff
        abstract = self.dataset.get_abstract(rel.abstract)
        a = abstract.get_entity_ids(rel.a)
        b = abstract.get_entity_ids(rel.b)

        # Feature 1 - Word distance between tags after lowercasing and stopwords removal
        objs_between_entities = abstract.obj[max(a):min(b)]
        objs_processed = [obj for obj in objs_between_entities if not obj.value.lower() in self.utils.get_stopwords()]

        distance = len(objs_processed)
        X.append(distance)

        # Feature 2 - POS tag of the last word in the entity sequence
        a_id = max(a)
        b_id = max(b)
        
        a_pos = abstract.pos_tags[a_id][1]
        b_pos = abstract.pos_tags[b_id][1]

        X.append(self.utils.get_feature_from_pos_tagger(a_pos))
        X.append(self.utils.get_feature_from_pos_tagger(b_pos))

        # NOTE: Taking into account 'reverse' in any way in this task seems to hurt performance as of now.
        #       Maybe later we can do something with this...

        # Feature 3 - Rule based extraction for boosting prediction of the less represented classes
        objects, a_id, b_id = self.__get_sentence_objects(abstract, min(a), min(b))
        X.append(self.__get_feature_from_rule(self.utils, objects))

        return X
