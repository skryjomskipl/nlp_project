# Written by: Przemyslaw Skryjomski

class Object:
    value = ''
    meta = None
    id = None

    def __init__(self, name, id = None):
        """ctor"""
        self.value = name
        self.meta = {}
        self.id = id

    def bind_meta(self, name, value):
        """Metadata setter"""
        self.meta[name] = value
    
    def get_meta(self, name):
        """Metadata getter"""
        if name not in self.meta:
            return None

        return self.meta[name]
