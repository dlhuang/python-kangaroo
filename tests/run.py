# -*- coding: utf-8 -*-
import os
import unittest
import logging

from kangaroo.bucket import Bucket

class KangarooTest(unittest.TestCase):
    test_path = os.path.dirname(__file__)

    def tearDown(self):
        filesToDelete = ["test.kg"]
        for f in filesToDelete:
            p = os.path.join(self.test_path, f)
            if os.path.exists(p):
                os.remove(p)
    
    def test_create_bucket(self):
        bucket = Bucket()
        self.assertTrue(isinstance(bucket, Bucket))

    def test_add_table(self):
        bucket = Bucket()
        name = bucket.new_table.tbl_name 
        self.assertEquals(name, "new_table")
        self.assertEquals(len(bucket.tables), 1)
    
    def test_get_tables(self):
        bucket = Bucket()
        name = bucket.new_table.tbl_name 
        name2 = bucket.new_table2.tbl_name 
        
        tables = bucket.tables 
        self.assertEquals(len(tables), 2)
        self.assertTrue(tables[0].tbl_name in [name, name2])
        self.assertTrue(tables[1].tbl_name, [name, name2])
        self.assertNotEquals(tables[0].tbl_name, tables[1].tbl_name)
        
    def test_delete_table(self):
        bucket = Bucket()
        name = bucket.new_table.tbl_name 
        bucket.delete_table(name)
        self.assertEquals(len(bucket.tables), 0)

    def test_add_row(self):
        bucket = Bucket()
        bucket.zoo.insert(dict(animal="lion", number=2))
        bucket.zoo.insert(dict(animal="kangaroo", number=100))

        self.assertEquals(len(bucket.zoo.find_all()), 2)

    def test_table_find(self):
        bucket = Bucket()
        bucket.zoo.insert(dict(animal="lion", number=2))
        bucket.zoo.insert(dict(animal="kangaroo", number=100))

        self.assertEquals(bucket.zoo.find(animal="kangaroo")["animal"], 
            "kangaroo")

    def test_filter_row_gt(self):
        bucket = Bucket()
        bucket.zoo.insert(dict(animal="lion", number=2))
        bucket.zoo.insert(dict(animal="kangaroo", number=100))
        f = dict(number__gt=2)
        self.assertEquals(len(bucket.zoo.find_all(**f)), 1)

    def test_filter_row_gte(self):
        bucket = Bucket()
        bucket.zoo.insert(dict(animal="lion", number=2))
        bucket.zoo.insert(dict(animal="kangaroo", number=100))
        f = dict(number__gte=2)
        self.assertEquals(len(bucket.zoo.find_all(**f)), 2)

    def test_filter_row_eq(self):
        bucket = Bucket()
        bucket.zoo.insert(dict(animal="lion", number=2))
        bucket.zoo.insert(dict(animal="kangaroo", number=100))
        f = dict(number=2)
        self.assertEquals(len(bucket.zoo.find_all(**f)), 1)

    def test_storage_pickle(self):
        p = os.path.join(self.test_path, "test.kg")
        bucket = Bucket(storage_format="pickle", storage_path=p)
        bucket.zoo.insert(dict(animal="lion", number=2))
        bucket.zoo.insert(dict(animal="kangaroo", number=100))
        bucket.flush()
        self.assertTrue(os.path.exists(p))

        bucket = Bucket(storage_format="pickle", storage_path=p)
        self.assertEquals(len(bucket.zoo.find_all()), 2)        

        f = dict(number=2)
        self.assertEquals(bucket.zoo.find(**f).number, 2)

    def test_storage_json(self):
        p = os.path.join(self.test_path, "test.kg")
        bucket = Bucket(storage_format="json", storage_path=p)
        bucket.zoo.insert(dict(animal="lion", number=2))
        bucket.zoo.insert(dict(animal="kangaroo", number=100))
        bucket.flush()
        self.assertTrue(os.path.exists(p))

        bucket = Bucket(storage_format="json", storage_path=p)
        self.assertEquals(len(bucket.zoo.find_all()), 2)        

        f = dict(number=2)
        self.assertEquals(bucket.zoo.find(**f).number, 2)

if __name__ == '__main__':
    unittest.main()
