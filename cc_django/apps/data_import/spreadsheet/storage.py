from django.core.files.storage import Storage
from django.conf import settings

from pymongo import Connection
from gridfs import GridFS

class GridFSStorage(Storage):
    def __init__(self, host='localhost', port=27017, collection='fs'):
        for s in ('host', 'port', 'collection'):
            name = 'GRIDFS_' + s.upper()
            if hasattr(settings, name):
                setattr(self, s, getattr(settings, name))
        for s, v in zip(('host', 'port', 'collection'), (host, port, collection)):
            if v:
                setattr(self, s, v)
        self.db = Connection(host=self.host, port=self.port)[self.collection]
        self.fs = GridFS(self.db)

    def _save(self, name, content):
        self.fs.put(content, filename=name)
        return name

    def _open(self, name, *args, **kwars):
        return self.fs.get_last_version(filename=name)

    def delete(self, name):
        oid = fs.get_last_version(filename=name)._id
        self.fs.delete(oid)

    def exists(self, name):
        return self.fs.exists({'filename': name})

    def size(self, name):
        return self.fs.get_last_version(filename=name).length