

#I'm not yet sure how  I will do this. I think i'm going to use 1 big dictionary with all the locations. You will be able to save, edit and remove 
#Locations. Because the coordinate system is not constant (various factors..) you will be able to set a "calibrate tuple" and that value will be addded
#To every coordinate when the coordinate is pulled from this class. The calibration tuple should be set everytime the machine starts.
#(X,Y,Z)
#This whole file is filled with functions that return a status report, i'm not sure if I will use this later so I might remove them (the status reports)
from tokenize import String
from typing import Dict, Tuple
import os
import shutil
import jsonpickle

class Locations:

    def __init__(self):

        self.locationbook: Dict[str, Tuple[float, float, float]] = {
            "calibrationlocation": (100, 100, 0),
            "slot1": (0, 0, 0),
            "slot2": (137, 0, 0),
            "slot3": (0, 86, 0),
            "slot4": (137, 86, 0),
            "slot5": (0, 172, 0),
            "slot6": (136, 172, 0),
            "home": (0, 0, 0),  #Why another home when you have G28? because when you call this home, it will be calibrated. Nice to have.
            "interestingZFocus": (0, 0, 33.5),
        }
 

        #The values below will not be saved, because the are machine constants/Should be edited every time the system starts
        #Machine constant, no need to able to change this.
        #The z Value will change when the microscope changes!
        #Will be accesed by calibration function.
        self.calibration = (0, 0, 0)
        self.currentLocation = (0, 0, 0)
        self.machineLimits = (0, 0, 0)
        

    #You will be able to add a location by being at the location and saving it, or manually by giving XYZ but that will be coded somewhere else,
    #In this class you will just be able to give xyz, and it will save it.
    async def addLocation(self,x:float, y:float, z:float, name: str):
        if (x > self.machineLimits[0]) or (y > self.machineLimits[1]) or (z > self.machineLimits[2]):
            statrep = "Coords are out of bounds, location has not been added"
        else:
            x = x - self.calibration[0]
            y = y - self.calibration[1]
            z = z - self.calibration[2]
            self.locationbook[name] = (x, y, z)
            statrep = "ok"
        await self.saveData()
        return statrep

    #You will probably be able to select from a list, but again this will be coded somewhere else.
    async def removeLocation(self, name):
        check = self.checkLocation(name)
        if check[0]:
            del self.locationbook[name]
            statrep = "ok"
        else:
            statrep = check[1]
        await self.saveData()
        return statrep

    async def editLocation(self, x:float, y:float, z:float, name):
        check = self.checkLocation(name)
        if check[0]:
            self.locationbook[name] = (float(x), float(y), float(z))
            statrep = "ok"
        else:
            statrep = check[1]
        await self.saveData()
        return statrep

    #You could just access the dict if you import this class, but I use this function to be able to calibrate every coord.
    async def getLocation(self, name):
        check = self.checkLocation(name)
        print(check)
        if check[0]:
            x = self.locationbook[0] + self.calibration[0]
            y = self.locationbook[1] + self.calibration[1]
            z = self.locationbook[2] + self.calibration[2]
            statrep = "ok"
        else:
            statrep = check[1]
        response = (x,y,z,statrep)
        return response

    async def setCalibration(self, x, y, z):
        self.calibration = (float(x), float(y), float(z))
        statrep = "ok"
        await self.saveData()
        return statrep

    # I want this function to be async, but then it returns a coroutine? h2fix pls
    #Only used inside of this class, checks if a location exsists.
    #Returns a tup with a bool of the status and a string with the actual status.
    def checkLocation(self, name) -> Tuple[bool, str]:
        if name in self.locationbook:
            ok = True
            statrep = "ok"
        else:
            ok = False
            statrep = "Location does not exist"
        return (ok, statrep)

    #Function to save the location dictionary every time something has been edited, to make it failsafe.
    async def saveData(self):
        print("Saving data")
        with open('data.json', 'w') as json_file:
            json_file.write(jsonpickle.encode(self.locationbook))

    #I'm thinking to only load on startup? This is failsafe (this is what currently happens)
    async def loadData(self):
        print("Loading location data")

        # Check if data.json exists, if not copy from hardcoded initial template.
        try:
            if not os.path.exists('data.json'):
                shutil.copyfile('init_data.json', 'data.json')
        except Exception as e:
            raise Exception("Initial data json is missing!") from e

        # Read database in memory.
        with open('data.json', 'r') as json_file:
            json_data = json_file.read()
            self.locationbook = jsonpickle.decode(json_data)

    async def getCurrentLocation(self):
        return self.currentLocation

    
   