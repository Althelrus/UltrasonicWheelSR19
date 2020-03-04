import json

class SaveConstants:
    def saveconfig(self, data):
        with open('/home/pi/Desktop/UltrsonicWheelSR19/data.txt', 'w') as outfile:
            json.dump(data, outfile, indent=4)

    def loadconfig(self):
        print("load")
        with open('/home/pi/Desktop/UltrsonicWheelSR19/data.txt') as json_file:
            data = json.load(json_file)
        return data