from flask import Flask, request
from analytics import parseContainers,getDistance,getLocationsInRange
import json


app = Flask(__name__)

print("...")

containerData = []


    

@app.route("/get-containers",methods=['GET'])
def getConainers():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    containers = request.args.get('containers').split(',')
    for i in range(len(containers)):
        containers[i] = int(containers[i])
    containers = set(containers)
    print(containers)
    locations = getLocationsInRange((lat,lng),containerData,300,containers)
    for location in range(len(locations)):
        locations[location]['types'] = list(locations[location]['types'])
    return json.dumps(locations)

if __name__ == "__main__":
    print('parsing')
    containerData = parseContainers('data/containers.json')
    app.run()