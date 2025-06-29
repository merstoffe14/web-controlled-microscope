from ast import Str
from typing import Dict, Tuple
from locations import Locations
from serialBridge import SerialBridge
# from wellPlateManager import WellPlateType

class WellPlateManager:

    def __init__(self, bridge: SerialBridge):
        self.bridge = bridge
        self.locations = bridge.locations
        self.WellPlateType48 = WellPlateType(13.08, (19.2, 9.5, 0))
        self.WellPlateType96 = WellPlateType(9, (14.4, 11.2, 0))
        self.WellPlateType384 = WellPlateType(4.5, (12.13, 8.99, 0))
    
    async def moveToWell(self, plateType: Str, plateNumber: int, well: Str):
        if plateType == "WellPlateType48":
            plate = self.WellPlateType48
        elif plateType == "WellPlateType96":
            plate = self.WellPlateType96
        elif plateType == "WellPlateType384":
            plate = self.WellPlateType384
        else:
            raise Exception("PlateType not found")
    
        plateSlotStart = self.locations.locationbook["slot" + str(plateNumber)]

        try:
            plateA1 = plate.A1_offset
        except:
            print("Plate type not found")
            return

        stepsBetween = await self.getStepsBetween("A1", well)
        distanceFromA1 = (stepsBetween[0]*plate.interWellDistance, stepsBetween[1]*plate.interWellDistance, 0)
        print("Moving------------------")
        print(f"Start of plate: {plateSlotStart}")
        print(f"Plate A1: {plateA1}")
        print(f"distance between: {distanceFromA1}")
        coords = [plateSlotStart[i] + plateA1[i] + distanceFromA1[i] for i in range(len(plateSlotStart))]
        print(f"Sum: {coords}")
        print("------------------------")
        z = await self.locations.getCurrentLocation()
        print(z)
        z = z[2]
        print(z)
        await self.bridge.goto(coords[0], coords[1], z, 0)

        
    async def getStepsBetween(self, coordinate1, coordinate2):
        y1 = coordinate1[0]
        x1 = int(coordinate1[1:])

        y2 = coordinate2[0]
        x2 = int(coordinate2[1:])

        x_res = x2-x1
        y_res = ord(y2)-ord(y1)
        
        # Go x_res right, Go y_res down, down from the point of view of the user, not the coordsystem
        return (x_res, y_res, 0)

class WellPlateType:
    def __init__(self, interWellDistance, A1_offset):
        self.interWellDistance = interWellDistance
        self.A1_offset = A1_offset