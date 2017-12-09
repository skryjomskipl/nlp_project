# Written by: Przemyslaw Skryjomski

from dataset.object import Object
from dataset.abstract import Abstract
from dataset.relation import Relation
import xml.etree.ElementTree

class Dataset:
    path = ''
    path_relations = ''
    abstract = None
    relation = None
    test_dataset = False

    def __init__(self, path, path_relations, test_dataset = False):
        """ctor"""
        self.path = path
        self.path_relations = path_relations
        self.abstract = []
        self.relation = []
        self.test_dataset = test_dataset
    
    def __parse_abstract_entity(self, abstract, attrib, text):
        abstract_id = attrib['id']
        abstract_id = abstract_id.split('.', 1)[1]

        for i in text.split():
            o = Object(i, abstract_id)
            abstract.append_object(o)

    def __parse_abstract_split(self, abstract, x):
        if x == None:
            return

        for i in x.split():
            o = Object(i)
            abstract.append_object(o)

    def __parse_abstract(self, abstract, c):
        self.__parse_abstract_split(abstract, c.text)

        for x in c:
            if not x.tag == 'SectionTitle':
                self.__parse_abstract_entity(abstract, x.attrib, x.text)
                self.__parse_abstract_split(abstract, x.tail)

    def __parse(self, utils):
        """PRIVATE - Parsing dataset"""
        fp = xml.etree.ElementTree.parse(self.path)
        if not fp:
            return False

        root = fp.getroot()

        for child in root:
            if len(child) == 0:
                print('WARNING: Encountered empty tag \'', child.tag, '\'.', sep = '')
                continue
            
            if child.tag != 'text':
                print('Expected child tag \'text\', got \'', child.tag, '\'.', sep = '')
                return False

            if not 'id' in child.attrib:
                print('Attribute \'id\' not found in child.')
                return False

            abstract_id = child.attrib['id']
            abstract = Abstract(abstract_id)

            #print("-> ", abstract_id)

            for c in child:
                if c.tag == 'title':
                    abstract.set_title(c.text)
                elif c.tag == 'abstract':
                    self.__parse_abstract(abstract, c)

            abstract.finalize(utils)
            self.abstract.append(abstract)

        return True

    def __parse_relations(self, utils):
        """PRIVATE: Parsing relations"""
        fp = open(self.path_relations)
        if not fp:
            return False

        for line in fp:
            # Check if line is empty
            if not line.strip():
                continue

            # Prepare data
            abstract = ""
            a = ""
            b = ""
            type = None
            reverse = False

            # Getting type
            if not self.test_dataset:
                s = line.split('(', 1)
                type = s[0]

            # Getting relations
            s = line.split('(', 1)[1].split(')', 1)[0]
            s = s.split(',')

            a = s[0].split('.', 1)
            b = s[1].split('.', 1)

            # Getting abstract
            if a[0] != b[0]:
                print("Encountered relations between different abstracts!")
                return False

            abstract = a[0]

            # Getting relations IDs
            a = a[1]
            b = b[1]

            if len(s) == 3:
                reverse = True
            elif len(s) != 2:
                print("Relations error, check if data are correct!")
                return False

            # Add them to the container
            rel = Relation(abstract, a, b, type, reverse)
            self.relation.append(rel)

            #print(rel.type, ' ', rel.abstract, ' ', rel.a, ' ', rel.b, ' ', rel.reverse, sep = '')
        
        return True

    def read(self, utils):
        """Reading dataset"""
        #print('Reading dataset from path: ', self.path, sep = '')

        if not self.__parse(utils):
            print('Failed at parsing dataset!')
            return False

        #print('Reading relations from path: ', self.path_relations, sep = '')

        if not self.__parse_relations(utils):
            print('Failed at parsing relations!')
            return False

        return True
    
    def get_abstract(self, id):
        for a in self.abstract:
            if a.id == id:
                return a

        return None
