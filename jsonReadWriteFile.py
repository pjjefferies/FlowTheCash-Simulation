import json

def load_json(fileName):    #Load Locally Saved Vehicles
    try:
        f = open(fileName, "r")
    except OSError:
        #print("In load_json, found OSError")
        raise OSError
        return
    try:
        jsonCarData = json.load(f)
        #print("In load_json, in try, type(jsonCarData): ", type(jsonCarData))
    except ValueError:
        #print("In load_json, found ValueError")
        raise ValueError
        return
    #print("Closing file")
    f.close()
    #print("Returning jsonCarData")
    return jsonCarData


def write_json(databaseFile, listOfCarData): #Write locally saved vehicles
    try:
        f = open(databaseFile, "w")
        jsonCarData = json.dumps(listOfCarData, indent="\t", sort_keys=True)
        f.write(jsonCarData)
        f.close()
        return
    except OSError:
        return
