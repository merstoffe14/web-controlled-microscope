from wellPlateManager import WellPlateManager
from serialBridge import SerialBridge
from liveCam import LiveCam
from locations import Locations
import time
import datetime
import cv2
import numpy as np


class RoutineManager:

    # Make 3 standard routines
    def __init__(self, bridge: SerialBridge, liveCam: LiveCam, locations: Locations):
        print("Routine Manager Init")
        self.bridge = bridge
        self.liveCam = liveCam
        self.locations = locations


    # This should be a routine object.
    async def do_z_scan(self, start, end, step):
        currentLocation = await self.locations.getCurrentLocation()

        if currentLocation is None:            print("Warning: No device attached")
        imgarray = []


        await self.bridge.goto(currentLocation[0], currentLocation[1], float(start), 0)
        time.sleep(5)
        zpos = list(np.arange(float(start), float(end), float(step)))
        for i in zpos:
            print(i)
            await self.bridge.goto(currentLocation[0], currentLocation[1], i, 0)
            time.sleep(1.5)
            # UINT16 is not permanent, see github issue.
            im = np.uint16(self.liveCam.GetFrame())
            print(im.dtype)

            #TODO make the livefeed work while scanning?
            #_, im = cv2.imencode('.png', im[...,::-1])
            #img_bytes = im.tobytes()
            #await socket.send_bytes(img_bytes)
            imgarray.append(im)

        
        ## Assign metadata
        if imgarray[0].ndim == 2:                 channels = ["brightfield"]
        elif imgarray[0].shape[-1] == 1:          channels = ["brightfield"]
        elif imgarray[0].shape[-1] == 3:          channels = ["red","blue","green"]
        else:                                     channels = []

        ## TODO get camera settings and load them too
        metadata = {
            "dimension_names":["z","c","x","y"],
            "channel_names": channels,
            "xposition": [currentLocation[0]],
            "yposition": [currentLocation[1]],
            "zpositions":[zpos]
        }

        self.liveCam.save_scan(imgarray, metadata) 
       

    # This should be a routine object.
    async def do_time_scan(self, delay, repeats):
        
        currentLocation = await self.locations.getCurrentLocation()

        if currentLocation is None:            print("Warning: No device attached")
        imgarray = []
        timestamps = []

        for i in range(repeats):
            
            await self.bridge.goto(currentLocation[0], currentLocation[1], i, 0)
            im = self.liveCam.GetFrame()

            #TODO make the livefeed work while scanning?
            #_, im = cv2.imencode('.png', im[...,::-1])
            #img_bytes = im.tobytes()
            #await socket.send_bytes(img_bytes)
            timestamps.append(datetime.now().strftime("%Y%m%d_%H%M%S"))
            imgarray.append(im)
            time.sleep(delay) ##async ?
            print("took picture")

        
        ## Assign metadata
        if imgarray[0].ndim == 2:                 channels = ["brightfield"]
        elif imgarray[0].shape[-1] == 1:          channels = ["brightfield"]
        elif imgarray[0].shape[-1] == 3:          channels = ["red","blue","green"]
        else:                                     channels = []

        ## TODO get camera settings and load them too
        metadata = {
            "dimension_names":["t","c","x","y"],
            "channel_names": channels,
            "xposition": [currentLocation[0]],
            "yposition": [currentLocation[1]],
            "zposition":[currentLocation[2]],
            "timestamp":[timestamps]
        }

        self.liveCam.save_scan(imgarray, metadata)        

class Routine:

    wellPlateManager = WellPlateManager
    def __init__(self, name, description, steps):
        pass
        # self.wellPlateType = 