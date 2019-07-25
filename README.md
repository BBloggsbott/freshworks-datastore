# freshworks-datastore
Repository with code for freshworks campus recruitment drive

## Installation
Clone this  and `cd` to the cloned directory
```bash
$ git clone https://github.com/BBloggsbott/freshworks-datastore
$ cd freshworks-datastore
```

Install required packages
```bash
$ pip install -r requirements
```

## Run the server
### Run with defaults
To run the server with default file names and save directories run the following command
```bash
$ python3 run.py
```

### Run with custom directory
To run the server with custom save directory, use the following syntax
```bash
$ python3 run.py <save_dir>
```
Example:
```bash
$ python3 run.py data
```

### Run with custom save directory and save file
To run the server with custom save directory and save file, use the following syntax
```bash
$ python3 run.py <save_dir> <save_file>
```
Example:
```bash
$ python3 run.py data data_saves.json
```

## HTTP Endpoint
### Create data
Use the below syntax to add data to the datastore
```
http://localhost:5000/create?key=<key>&value=<value>&timetolive=<tiletolive>
```
*The `timetolive` parameter is optional*

### Read Data
Use the below syntax to read data from the datastore
```
http://localhost:5000/read?key=<key>
```

### Delete Data
Use the below syntax to delete data from the datastore
```
http://localhost:5000/delete?key=<key>
```

**When a request is processed, the response is returned with the appropriate status code.**
