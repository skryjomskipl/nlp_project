# Relation class

class Relation:
    abstract = ""
    a = ""
    b = ""
    type = None
    reverse = False

    def __init__(self, abstract = "", a = "", b = "", type = None, reverse = False):
        """ctor"""
        self.abstract = abstract
        self.a = a
        self.b = b
        self.type = type
        self.reverse = reverse
    
    def set_abstract(self, name):
        self.abstract = name

    def set_a(self, name):
        self.a = name
    
    def set_b(self, name):
        self.b = name
    
    def set_type(self, name):
        self.type = name
    
    def set_reverse(self, reverse):
        self.reverse = reverse
    