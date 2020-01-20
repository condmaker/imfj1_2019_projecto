import json
from vector3 import *

#Get list of list of points from json file
def retrieve_points(object, scale):

    
    polygon = []
    

    with open('objects.json') as f:
        fileDict = json.load(f)
    try:
        fileDict[object]
    except:
        print(f"There's no object with the name '{object}'.")
        exit(0)

    pointList = fileDict[object]["points"]
    faceList = fileDict[object]["faces"]


    for i in range(len(faceList)):
        poly = []
        for j in faceList[i]:
            aux = vector3(pointList[j][0],pointList[j][1],pointList[j][2])
            aux -= vector3(-scale/2, -scale/2, scale/2)
            poly.append(aux)
        polygon.append(poly)

    return polygon

retrieve_points("cube", 1)