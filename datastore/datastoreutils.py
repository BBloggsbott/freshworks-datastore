import os
import json


def write_timetolive(data, filename):
    """
    Write a timetolive entry to the file
    """
    ttl_file = open(filename, 'w+')
    json.dump(data, ttl_file)
    ttl_file.close()

def read_timetolive(filename):
    """
    Read a timetolive entry from the file
    """
    if not os.path.isfile(filename):
        return {}
    ttl_file = open(filename, 'r')
    data = json.load(ttl_file)
    ttl_file.close()
    return data

def intimetolive(key, filename):
    """
    Check if the given key has a timetolive entry
    """
    timetolivedict = read_timetolive(filename)
    return (key in timetolivedict.keys())

def isalive(key, timestamp, filename):
    """
    Check if a given key is alive or expired
    """
    timetolivedict = read_timetolive(filename)
    alive = (timestamp - timetolivedict[key][0]) < timetolivedict[key][1]
    return alive

def delete_timetolive(key, filename):
    """
    Delete a given key from the timetolive entries
    """
    if not intimetolive(key, filename):
        return False, 'Key not in time to live'
    else:
        timetolivedict = read_timetolive(filename)
        timetolivedict.pop(key)
        write_timetolive(timetolivedict, filename)
        return True, 'Key deleted'


def add_entry_to_datastore(new_key, new_value, filename):
    """
    Add entry to the datastore
    """
    old_data = {}
    if os.path.isfile(filename):
        data_file = open(filename, 'r')
        old_data = json.load(data_file)
        data_file.close()
    if new_key in old_data.keys():
        return False, 'Key exists'
    old_data[new_key] = new_value
    data_file = open(filename, 'w+')
    if len(json.dumps(old_data).encode('utf-8')) > 2**30:
        return False, 'File size greater than 1 GB'
    json.dump(old_data, data_file)
    data_file.close()
    return True, 'Entry Created'

def read_entry_from_datastore(key, filename):
    """
    Read an entry from the datastore
    """
    if not os.path.isfile(filename):
        return False, 'Datastore not Found'
    data_file = open(filename, 'r')
    data = json.load(data_file)
    data_file.close()
    if key not in data.keys():
        return False, 'Key not found'
    else:
        return True, data[key]
        

def delete_entry_from_datastore(key, filename, timetolive_filename):
    """
    Delete an entry from the datastore
    """
    success, resp = read_entry_from_datastore(key, filename)
    if success:
        data_file = open(filename, 'r')
        data = json.load(data_file)
        data_file.close()
        data.pop(key)
        data_file = open(filename, 'w')
        json.dump(data, data_file)
        data_file.close()
        delete_timetolive(key, timetolive_filename)
        return True, 'Deleted Key'
    else:
        return success, resp
