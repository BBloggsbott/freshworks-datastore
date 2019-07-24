from datastore.datastoreutils import add_entry_to_datastore
import unittest
import os
import json

class DataStoreTest(unittest.TestCase):
    def setUp(self):
        self.filename = 'data_test.json'

    def tearDown(self):
        os.remove(self.filename)

    def test_add(self):
        success, _ = add_entry_to_datastore('key1', 'val1', self.filename)
        self.assertTrue(success)
        success, _ = add_entry_to_datastore('key1', 'val2', self.filename)
        self.assertFalse(success)
    
    def test_saved_content(self):
        success, _ = add_entry_to_datastore('key3', 'val3', self.filename)
        f = open(self.filename, 'r')
        data = json.load(f)
        f.close()
        assert data['key3'] == 'val3'

if __name__ == '__main__':
    unittest.main()