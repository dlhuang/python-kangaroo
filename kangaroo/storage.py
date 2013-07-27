import json
import pickle
import time 
from kangaroo.table import Table

class Storage(object):

    def __init__(self, path, bucket):
        self.path = path
        self.bucket = bucket

    def dump(self, bucket):
        raise NotImplementedError()

    def load(self, bucket):
        raise NotImplementedError()

    def get_data_to_save(self):
        data = {
            "tables": self.bucket.tables,
            "time": time.time()
        }
        return data

    def load_into_memory(self, data):
        for t in data["tables"]:
            self.bucket.add_table(t)

class StorageCPickle(Storage):
    
    def load(self):
        with open(self.path, 'rb') as f:
            data = pickle.load(f)
        self.load_into_memory(data)

    def dump(self):
        data = self.get_data_to_save()

        with open(self.path, 'wb') as f:
            pickle.dump(data, f)

class StorageJson(Storage):
    
    def load(self):
        with open(self.path, 'rb') as f:
            database = json.loads(f.read())
        data = dict(tables=[], time=database["time"])
        for t in database["tables"]:
            table = Table(tbl_name=t["tbl_name"])
            for row in t["rows"]:
                table.insert(row)
            data["tables"].append(table)
        self.load_into_memory(data)

    def dump(self):
        data = self.get_data_to_save()
        tables = []
        for table in self.bucket.tables:
            d = {
                "tbl_name": table.tbl_name,
                "index": [],
                "rows": table.find_all(),
            }
            tables.append(d)
        
        database = dict(time=time.time(), tables=tables)

        with open(self.path, 'wb') as f:
            f.write(json.dumps(database))