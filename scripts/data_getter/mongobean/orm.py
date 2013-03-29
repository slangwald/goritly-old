import copy
import datetime

import pymongo
from bson.objectid import ObjectId
import bson

document_classes = {}

default_db = None

class DatabaseError(Exception):
    pass

def register(cls):
    document_classes[cls.type_name] = cls

def encode_document(document,cascade = False):
    if isinstance(document,dict):
        output_document = {}
        for (key,value) in document.items():
            output_document[key] = encode_document(value)
    elif isinstance(document,list):
        output_document = map(lambda x:encode_document(x),document)
    elif isinstance(document,tuple):
        output_document = tuple(map(lambda x:encode_document(x),document))
    elif isinstance(document,Document):
        if document.embedded:
            output_document = {'_type':document.type_name,'_attributes':encode_document(document.attributes,cascade)}
        else:
            if not document.document_id or cascade:
                document.save()
            output_document = {'_id':document.document_id,'_type':document.type_name}
    else:
        output_document = document
    return output_document

def decode_document(document):
    if isinstance(document,dict):
        if '_type' in document and document['_type'] in document_classes and ('_id' in document or '_attributes' in document):
            document_class = document_classes[document['_type']]
            output_document = document_class()
            if '_id' in document:
                output_document.document_id = document['_id']
                output_document.set_lazy()
            else:
                output_document.attributes = decode_document(document['_attributes'])
                output_document.embedded = True
        else:
            output_document = {}
            for (key,value) in document.items():
                output_document[key] = decode_document(value)
    elif isinstance(document,list) or isinstance(document,tuple):
        output_document = map(lambda x:decode_document(x),document)
    else:
        output_document = document
    return output_document

def encode_query(args):
    if isinstance(args,dict):
        output_args = {}
        for (key,value) in args.items():
            output_args[key] = encode_query(value)
    elif isinstance(args,list) or isinstance(args,tuple):
        output_args = map(lambda x:encode_query(x),args)
    elif isinstance(args,Document):
        if not args.document_id:
            output_args = args.attributes
        else:
            output_args = {'_id':args.document_id,'_type':args.type_name}
    else:
        output_args = args
    return output_args
    

class Collection(object):
    
    def __init__(self,document_class,collection):
        self.__dict__['_document_class'] = document_class
        self.__dict__['_collection'] = collection
    
    def __getattr__(self,key):

        def function_wrapper(collection,f,args,kwargs):
            result = f(*args,**kwargs)
            if isinstance(result,pymongo.cursor.Cursor):
                return Cursor(collection._document_class,result)
            if isinstance(result,pymongo.collection.Collection):
                return Collection(collection._document_class,result)
            return result

        if hasattr(self._collection,key):
            attr = getattr(self._collection,key)
            if hasattr(attr,'__call__'):
                return lambda *args,**kwargs:function_wrapper(self,attr,args,kwargs)

        raise AttributeError
    
    def __setattr__(self,key,value):
        setattr(self._collection,key,value)

    def find(self,*args,**kwargs):
        if 'spec' in kwargs:
            kwargs['spec'] = encode_query(kwargs['spec'])
        args = list(args)
        if len(args):
            args[0] = encode_query(args[0])
        cursor = self._collection.find(*args,**kwargs)
        return Cursor(self._document_class,cursor)

    def find_one(self,*args,**kwargs):
        if 'spec' in kwargs:
            kwargs['spec'] = encode_query(kwargs['spec'])
        args = list(args)
        if len(args):
            args[0] = encode_query(args[0])
        json_document = self._collection.find_one(*args,**kwargs)
	if not json_document:
	    return None
        document = self._document_class()
        document.attributes = decode_document(json_document)
        return document

class Cursor(object):
    
    def __init__(self,document_class,cursor):
        self.__dict__['_document_class'] = document_class
        self.__dict__['_cursor'] = cursor
        
    def __getattr__(self,key):

        def function_wrapper(cursor,f,args,kwargs):
            result = f(*args,**kwargs)
            if isinstance(result,pymongo.cursor.Cursor):
                return Cursor(cursor._document_class,result)
            if isinstance(result,pymongo.collection.Collection):
                return Collection(cursor._document_class,result)
            return result

        if hasattr(self._cursor,key):
            attr = getattr(self._cursor,key)
            if hasattr(attr,'__call__'):
                return lambda *args,**kwargs:function_wrapper(self,attr,args,kwargs)
            return attr

        raise AttributeError
        
    def __setattr__(self,key,value):
        setattr(self._cursor,key,value)

    def __iter__(self):
        return self

    def next(self):
        json_document = self._cursor.next()
        document = self._document_class()
        document.attributes = decode_document(json_document)
        return document

    def __getitem__(self,key):
        if isinstance(key,slice):
            return self.__class__(self._document_class,self._cursor.__getitem__(key))
        json_document = self._cursor[key]
        document = self._document_class()
        document.attributes = decode_document(json_document)
        return document

class MetaDocumentClass(type):

    def __new__(cls, clsname, bases, attrs):
        newclass = super(cls, MetaDocumentClass).__new__(cls, clsname, bases, attrs)
        register(newclass)  # here is your register function
        return newclass

class classproperty(object):

    def __init__(self, getter):
        self.getter = getter
    
    def __get__(self, instance, owner):
        return self.getter(owner)

class Document(object):

    __metaclass__ = MetaDocumentClass
    
    class Meta:
        
        collection_name = None
        type_name = None
        database = None
    
    #The name of the collection the document is stored to. Defaults to the name of the class (in lowercase).
    _collection_name = None
    
    #The type name of the document that appears in the JSON document. Defaults to the name of the class.
    _type_name = None

    #The database in which the document gets stored. Defaults to default_db().
    _database = None
    
    @classproperty
    def collection(cls):
        return Collection(cls,cls.database[cls.collection_name])
    
    @classproperty
    def collection_name(cls):
        if cls._collection_name:
            return cls._collection_name
        return cls.__name__.lower()

    @classproperty
    def type_name(cls):
        if cls._type_name:
            return cls._type_name
        return cls.__name__
    
    @classproperty
    def database(cls):
        if cls._database:
            return cls._database
        if default_db == None:
            raise DatabaseError("No default database configured!")
        return default_db

    def __init__(self,**kwargs):
        self._attributes = kwargs
        self._is_lazy = False
        self._embedded = False
                
    def __getitem__(self,key):
        return self.attributes[key]
        
    def __contains__(self,key):
        return True if key in self.attributes else False
    
    def __setitem__(self,key,value):
        self.attributes[key] = value
        
    def __delitem__(self,key):
        del self.attributes[key]
        
    def __copy__(self):
        d = self.__class__(**self.attributes.copy())
        return d

    def __deepcopy__(self,memo):
        d = self.__class__(**copy.deepcopy(self.attributes,memo))
        return d
    
    def __eq__(self,other):
        if type(self) != type(other):
            return False
        if self.document_id == other.document_id:
            return True
        if not self._is_lazy and not other._is_lazy and self.attributes == other.attributes:
            return True
        return False
        
    def __repr__(self):
        if self._is_lazy:
            return "Lazy"+self.__class__.__name__+"(**"+str(self._attributes)+")"
        else:
            return self.__class__.__name__+"(**"+str(self._attributes)+")"

    @property 
    def created_at(self):
        return self.attributes['_created_at']

    @property
    def updated_at(self):
        return self.attributes['_updated_at']

    @property
    def embedded(self):
        return self._embedded
    
    @embedded.setter
    def embedded(self,embedded):
        self._embedded = embedded
        if embedded:
            self.document_id = None
    
    @property
    def document_id(self):
        if '_id' in self._attributes:
            return self._attributes['_id']
        return None
    
    @document_id.setter
    def document_id(self,document_id):
        if document_id == None and '_id' in self._attributes:
            del self._attributes['_id']
        else:
            self._attributes['_id'] = document_id

    @property
    def attributes(self):
        if self._is_lazy:
            self._is_lazy = False
            self._attributes = self.collection.find_one({'_id':self.document_id}).attributes
        return self._attributes
    
    @attributes.setter
    def attributes(self,attributes):
        self._attributes = attributes
        self._is_lazy = False

    def keys(self):
        return self._attributes.keys()

    def set_lazy(self,is_lazy = True):
        self._is_lazy = is_lazy
        
    def save(self,cascade = False,revert_after = True):
        if self.embedded:
            raise AttributeError("Document is embedded!")
        if not self.document_id:
            document_id = bson.objectid.ObjectId()
            self.document_id = document_id
        if not '_created_at' in self.attributes:
            self.attributes['_created_at'] = datetime.datetime.now()
        self.attributes['_updated_at'] = datetime.datetime.now()
        self.collection.save(encode_document(self.attributes.copy(),cascade = cascade))
        if revert_after:
            self.revert()
    
    def revert(self):
        if self.embedded:
            raise AttributeError("Document is embedded!")
        if self.document_id:
            self.attributes = self.collection.find_one({'_id':self.document_id}).attributes
        else:
            raise AttributeError("Document not saved to collection!")
    
    def delete(self):
        if self.embedded:
            raise AttributeError("Document is embedded!")
        if not self.document_id:
            return
        self.collection.remove({'_id':self.document_id})
        del self.attributes['_id']
        if '_created_at' in self.attributes:
            del self.attributes['_created_at']
        if '_updated_at' in self.attributes:
            del self.attributes['_updated_at']
