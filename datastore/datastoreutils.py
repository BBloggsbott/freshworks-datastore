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