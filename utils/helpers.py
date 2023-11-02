import json, os,sys

def load_json(filename):
    file_path = os.path.join(sys.path[0], filename)
    if os.path.exists(file_path):
        with open(file_path) as json_file:
            json_data = json.load(json_file)
        return json_data
    else:
        print("File not found: " + filename + "")
        return None


def save_json(filename, data):
    with open(os.path[0] + '/' + filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)

