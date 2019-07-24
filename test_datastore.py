from datastore.datastoreutils import add_entry_to_datastore, read_entry_from_datastore
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

    def test_read(self):
        success, _ = add_entry_to_datastore('key4', 'val4', self.filename)
        success, resp = read_entry_from_datastore('key4', self.filename)
        self.assertTrue(success)
        self.assertEqual(resp, 'val4')
        success, _ = read_entry_from_datastore('key0', self.filename)
        self.assertFalse(success)
        success, _ = read_entry_from_datastore('key4', 'somefile')
        self.assertFalse(success)

if __name__ == '__main__':
    unittest.main()