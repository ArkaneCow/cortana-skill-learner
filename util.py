import json

import d_time
import d_weather

def loadJSON(name):
    contents_file = open(name, "r")
    contents = contents_file.read()
    contents_file.close()
    return json.loads(contents)

def writeJSON(name, data):
    with open(name, "w") as fp:
        json.dump(data, fp)

def saveFunction(name, seq_id, seq_str):
    current = loadJSON("cmd.json")

    func = {}
    func["id"] = len(current)
    func["internal"] = False
    func["trigger"] = name
    func["s_id"] = seq_id
    func["s_str"] = seq_str

    current[name] = func
    writeJSON("cmd.json", current)
