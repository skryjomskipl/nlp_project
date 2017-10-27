# Written by: Przemyslaw Skryjomski
# The get_word_beforeE1 function written by Chathuri and Samantha

from dataset.object import Object

class Abstract:
    id = ''
    title = ''
    obj = None
    text = ''
    pos_tags = None

    def __init__(self, id):
        """ctor"""
        self.id = id
        self.obj = []

    def set_title(self, title):
        """Sets title"""
        self.title = title

    def get_object(self, name):
        """Object getter, returns None if not found"""
        for i in self.obj:
            if i.value == name:
                return i

        return None

    def get_entity(self, id):
        """Entity getter, returns None if not found"""
        for o in self.obj:
            if o.id == id:
                return o

        return None

    def get_entity_ids(self, id):
        """Entity ids getter, returns empty array if not found"""
        a = []
        count = 0

        for o in self.obj:
            if o.id == str(id):
                a.append(count)
            
            count += 1

        return a


    def append_object(self, obj):
        """Appends object, returns False if one already exist"""
        self.obj.append(obj)
        self.text = self.text + obj.value + ' '

        return True
    
    def finalize(self, utils):
        """Do some postprocessing stuff with abstract"""

        # Remove space from the last object appended in abstract raw text
        text_length = len(self.text)

        if text_length > 0:
            self.text = self.text[:text_length - 1]

        # Apply POS tagging on abstract
        tokens = []
        for obj in self.obj:
            tokens.append(obj.value)
        
        self.pos_tags = utils.get_pos_tags(tokens)
    
    def get_word_beforeE1(self, id):
        """Retuen the fisrt word befor the first entity"""
        a=self.get_entity_ids(id);

        return a
