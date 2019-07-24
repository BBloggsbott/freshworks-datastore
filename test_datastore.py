from datastore.datastoreutils import add_entry_to_datastore, read_entry_from_datastore, delete_entry_from_datastore, intimetolive, write_timetolive, read_timetolive, isalive, delete_timetolive
import unittest
import os
import json

class DataStoreTest(unittest.TestCase):
    def setUp(self):
        self.filename = 'data_test.json'
        self.ttl_filename = 'timetolive_test.json'

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

    def test_delete(self):
        success, _ = add_entry_to_datastore('key4', 'val4', self.filename)
        success, resp = read_entry_from_datastore('key4', self.filename)
        self.assertTrue(success)
        self.assertEqual(resp, 'val4')
        success, _ = delete_entry_from_datastore('key4', self.filename, self.ttl_filename)
        success, _ = read_entry_from_datastore('key0', self.filename)
        self.assertFalse(success)


class TimeToLiveTests(unittest.TestCase):
    def setUp(self):
        self.filename = 'timetolive_test.json'

    def tearDown(self):
        os.remove(self.filename)

    def test_write_time_to_live(self):
        ttl_dict = {}
        ttl_dict['key1'] = (10, 4)
        write_timetolive(ttl_dict, self.filename)
        f = open(self.filename, 'r')
        data = json.load(f)
        f.close()
        self.assertTrue('key1' in data.keys())
        self.assertEqual(data['key1'][0], 10)
        self.assertEqual(data['key1'][1], 4)

    def test_read_time_to_live(self):
        ttl_dict = {}
        ttl_dict['key1'] = (10, 4)
        write_timetolive(ttl_dict, self.filename)
        data = read_timetolive(self.filename)
        self.assertTrue('key1' in data.keys())
        self.assertEqual(data['key1'][0], ttl_dict['key1'][0])
        self.assertEqual(data['key1'][1], ttl_dict['key1'][1])

    def test_in_time_to_live(self):
        ttl_dict = {}
        ttl_dict['key1'] = (10, 4)
        write_timetolive(ttl_dict, self.filename)
        self.assertTrue(intimetolive('key1', self.filename))

    def test_is_alive(self):
        ttl_dict = {}
        ttl_dict['key1'] = (10, 4)
        write_timetolive(ttl_dict, self.filename)
        self.assertTrue(isalive('key1', 11, self.filename))
        self.assertFalse(isalive('key1', 20, self.filename))

    def test_delete_time_to_live(self):
        ttl_dict = {}
        ttl_dict['key1'] = (10, 4)
        write_timetolive(ttl_dict, self.filename)
        success, _ = delete_timetolive('key1', self.filename)
        self.assertTrue(success)
        success, _ = delete_timetolive('key1', self.filename)
        self.assertFalse(success)
        self.assertFalse(intimetolive('key1', self.filename))


if __name__ == '__main__':
    unittest.main()