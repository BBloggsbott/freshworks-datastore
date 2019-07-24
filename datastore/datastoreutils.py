import os
import json
def add_entry_to_datastore(new_key, new_value, filename):
    old_data = {}
    if os.path.isfile(filename):
        data_file = open(filename, 'r')
        old_data = json.load(data_file)
        data_file.close()
    if new_key in old_data.keys():
        return False, 'Key exists'
    old_data[new_key] = new_value
    data_file = open(filename, 'w+')
    json.dump(old_data, data_file)
    data_file.close()
    return True, 'Entry Created'

def read_entry_from_datastore(key, filename):
    if not os.path.isfile(filename):
        return False, 'Datastore not Found'
    data_file = open(filename, 'r')
    data = json.load(data_file)
    data_file.close()
    if key not in data.keys():
        return False, 'Key not found'
    else:
        return True, str(data[key])
        

def delete_entry_from_datastore(key, filename):
    success, resp = read_entry_from_datastore(key, filename)
    if success:
        data_file = open(filename, 'r')
        data = json.load(data_file)
        data_file.close()
        data.pop(key)
        data_file = open(filename, 'w')
        json.dump(data, data_file)
        data_file.close()
        return True, 'Deleted Key'
    else:
        return success, resp
        