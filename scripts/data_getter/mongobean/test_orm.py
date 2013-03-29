import unittest
import copy

import mongobean.orm as orm
import pymongo

def test_connection():
    return pymongo.MongoClient()

class TestDocument1(orm.Document):
    
    collection_name = "test_document1"

class TestDocument2(orm.Document):
    
    collection_name = "test_document2"
    
class CustomDocument(orm.Document):
    
    _database = test_connection().test_database_2
    _type_name = "wiki_wiki"
    _collection_name = "hulu_hulu"

class TestDocuments(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.connection = test_connection()
        cls.connection.drop_database('test_database_1')
        cls.connection.drop_database('test_database_2')
        cls.test_database_1 = cls.connection.test_database_1
        cls.test_database_2 = cls.connection.test_database_2
        orm.default_db = cls.test_database_1
    
    @classmethod
    def tearDownClass(cls):
        cls.connection.drop_database('test_database_1')
        cls.connection.drop_database('test_database_2')
        
    def test_comparison(self):
        doc1 = orm.Document(hallo = 'welt')
        doc2 = orm.Document(hallo = 'welt')
        
        assert doc1 == doc2
        
        doc1.save()
        doc2.save()
        
        assert doc1 != doc2
    
    def test_custom_document(self):
        attributes = {'test' : "test"}
        custom_doc = CustomDocument(**attributes)
        custom_doc.save()

        self.assertEqual(self.test_database_1[custom_doc.collection_name].find({'_id':custom_doc.document_id}).count(),0)
        self.assertEqual(self.test_database_2[custom_doc.collection_name].find({'_id':custom_doc.document_id}).count(),1)
        self.assertEqual(self.test_database_2[custom_doc.collection_name].find({'_id':custom_doc.document_id})[0],custom_doc.attributes)
        self.assertEqual(custom_doc,CustomDocument.collection.find_one({'_id':custom_doc.document_id}))

    def test_embedded_document(self):
        attributes = {'test' : "test"}
        custom_doc = CustomDocument(**attributes)
        
        subdoc = TestDocument2(test = 1243,father = custom_doc,hashvalue = {'test':123,'foo':'bar'})
        subdoc.embedded = True
        custom_doc['subdoc'] = subdoc
        custom_doc.save()
        
        loaded_doc = CustomDocument.collection.find_one({'_id':orm.ObjectId(custom_doc.document_id)})
        
        self.assertEqual(loaded_doc,custom_doc)
        self.assertEqual(loaded_doc['subdoc'],subdoc)
        self.assertEqual(subdoc.document_id,None)
        self.assertRaises(AttributeError,subdoc.save)
        self.assertRaises(AttributeError,subdoc.revert)
        
    
    def test_document_copying(self):
        doc = orm.Document(hallo = 'welt')
        subdoc1 = TestDocument1(name = 'subdoc1',testvalue = 24)
        subdoc2 = TestDocument2(name = 'subdoc2',testvalue =454)
        doc['subdocs'] = [subdoc1,subdoc2]
        doc.save()
        doc_copy = copy.copy(doc)
        doc_deepcopy = copy.deepcopy(doc)

        assert doc_copy == doc
        assert doc_deepcopy == doc
        assert doc_copy == doc_deepcopy

    
    def test_nested_document(self):
        doc = orm.Document(hallo = 'welt')
        subdoc1 = TestDocument1(name = 'subdoc1',testvalue = 24)
        subdoc2 = TestDocument2(name = 'subdoc2',testvalue =454)
        doc['subdocs'] = [subdoc1,subdoc2]
        doc['subdoc1'] = subdoc1
        doc.save()
        restored_doc = doc.collection.find_one({'_id':doc['_id']})

        assert isinstance(restored_doc['subdocs'],list)
        assert isinstance(restored_doc['subdocs'][0],TestDocument1)
        assert isinstance(restored_doc['subdocs'][1],TestDocument2)
        assert restored_doc['subdocs'][0] == restored_doc['subdoc1']
        assert restored_doc['subdocs'][0] == subdoc1
        assert restored_doc['subdocs'][1] == subdoc2

    def test_circular_nested_document(self):
        doc = orm.Document(attributes = {'hallo' : 'welt','dict':{'5':4,'test':[1,2,3]}})
        doc1 = TestDocument1(attributes = {'param' : 3433322})
        doc2 = TestDocument2(attributes = {'param' : 34322})
        doc['subdoc'] = doc1
        doc1['subdoc'] = doc2
        doc2['subdoc'] = doc
        
        doc.save()

        doc = doc.collection.find_one({'_id':doc.document_id})
        
        assert doc['subdoc'] == doc1
        assert doc['subdoc'].attributes == doc1.attributes
        assert doc['subdoc']['subdoc'] == doc2
        assert doc['subdoc']['subdoc']['subdoc'] == doc


if __name__ == '__main__':
    unittest.main()