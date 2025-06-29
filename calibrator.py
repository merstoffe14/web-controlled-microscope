import cv2  # type: ignore
import numpy as np  # 
from liveCam import LiveCam
from locations import Locations
from serialBridge import SerialBridge
from skimage import filters  
import skimage as skimage  
import matplotlib.pyplot as plt

'''
If this the calibration stops the camera and the software. Then I can try working with the getCurrentFrame
logic instead of Camera.GetFrame()
'''

class Calibrator:

    def __init__(self, bridge: SerialBridge, liveCam: LiveCam, locations: Locations) -> None:
        self.bridge: SerialBridge = bridge
        self.liveCam: LiveCam = liveCam
        self.locations: Locations = locations
        self.pictureNumber: int = 0

    # Autofocus function
    # Add a bottom limit.
    # fmin optimizer?

    async def calibrate_z(self):
        currentLocation = await self.locations.getCurrentLocation()
        await self.bridge.goto(currentLocation[0], currentLocation[1], 0, 0)

        print("Focusing")
        caliArray = []
        await self.bridge.goto(0, 0, 50, 1)
        for i in range(150):
            
            # fmo = 
            fmo = np.mean(filters.sobel(image=self.liveCam.camera.GetFrame())**2)
            caliArray.append(fmo)
            
        maxVal = max(caliArray)
        index = caliArray.index(maxVal)
        print(f"Max value: {maxVal}")
        print(f"Index: {index}")

        await self.bridge.goto(0, 0, 50-index/150, 1)

        plt.plot(caliArray, color="red")
        plt.show()

    async def z_optimizer(self, location):
        currentLocation = await self.locations.getCurrentLocation()
        await self.bridge.goto(currentLocation[0], currentLocation[1], location, 0)

        fmo = np.mean(filters.sobel(image=self.liveCam.camera.GetFrame())**2)*-10000
        return fmo


        
            

        
        

   