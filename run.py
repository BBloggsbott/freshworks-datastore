from datastore import app
import os
import sys

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    save_directory = '.'
    if len(sys.argv) > 1:
        save_directory = sys.argv[1]
        if not os.path.isdir(save_directory):
            os.makedirs(save_directory)
        if len(sys.argv) > 2:
            save_file = sys.argv[2]
        else:
            save_file = app.config['savefile']
        app.config.update(dict(
            savefile=os.path.join(save_directory, save_file),
            timetolivefile=os.path.join(save_directory, app.config['timetolivefile'])
        ))
        
app.run(host='127.0.0.1', port=port, debug=True)