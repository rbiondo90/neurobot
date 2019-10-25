import json
import os
import defaults

class DistanceInterpolator:
    FILES_DIRECTORY = os.path.join(defaults.CONFIG_DIRECTORY, os.path.basename(__file__).split(".")[0])

    def __init__(self, known_points_file):
        #try:
        with open(os.path.join(self.FILES_DIRECTORY, known_points_file)) as file:
            self.known_points = json.load(file)["known_points"]
        #except BaseException as e:
            #print(str(e))
            #print("Parameter file not exists or is not a valid JSON!")

    def get_distance(self, area):
        pass

    def get_interpolating_points(self, area):
        if area < self.known_points[0]["area"]:
            return self.known_points[0], self.known_points[1]
        for i in range(len(self.known_points) - 1):
            if area in range(self.known_points[i]["area"], self.known_points[i+1]["area"]):
                return self.known_points[i], self.known_points[i+1]
        return self.known_points[-2], self.known_points[-1]

    def interpolate(self, area):
        point1, point2 = self.get_interpolating_points(area)
        x1 = point1["area"]
        x2 = point2["area"]
        y1 = point1["distance"]
        y2 = point2["distance"]
        x = area
        deltay = y2 - y1
        deltax = x2 - x1
        y = deltay * ((x - x1) / deltax + y1 / deltay)
        return min(max(y, 0) ,1)

if __name__ == "__main__":
    points = DistanceInterpolator("person_face.json")