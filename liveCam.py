# from pymba import Vimba
# from pymba import Frame
import os
from time import sleep
from typing import Dict
from sys import platform
import jsonpickle
import skimage
from serialBridge import SerialBridge
from datetime import datetime
import numpy as np
import H5

'''    
    I still have this piece of code to generate a random iamge when no camera is found
    But it uses the currentframe logic, which I don't use anymore. I need to find a way
    To add this to the camera.GetFrame() logic.
'''

class LiveCam:

    def __init__(self, bridge: SerialBridge):
        
        self.bridge: SerialBridge = bridge

        self.cucurrentFrame: int = 0 
        self.isZScanning: bool = False 
        self.enabled: bool = True # Do i use this?
        self.now: datetime = datetime.now() # Do i use this?
        self.camera = None
        self.method = None
        self.save_format = "HDF5"
        self.save_path = "../wellplatemicroscope/captures"

        self.settings: Dict[str, float] = {
            "ExposureTime": 20000,  # [44.209, 1410065.398]
            "Gain": 0,  # [0,20]
            "Contrast": 0,  # [0,?]
            "Brightness": 0,  # [500,12000]
        }

    def run_main(self):
        self.openCamera()

    def openCamera(self):
        # Add some way to close the camera properly when an error happens

        try:
            from CameraModel.Pleora.PleoraCamera import PleoraCamera
            self.camera = PleoraCamera()
            self.camera.Open(0)
            self.camera.Start()
            self.method = "Pleora"
            return

        except Exception as e: 
            print(e)

        try:
            import cv2
            self.camera = cv2.VideoCapture(0)
            self.method = "Opencv"    
        except:
            pass
    
        print("No compatible camera connected.")


    def GetFrame(self):   

        if self.method == "Pleora":    
            return self.camera.GetFrame()

        elif self.method == "Opencv":
            ret, frame = self.camera.read()
            return frame[...,::-1]

    def closeCamera(self):

        if self.method == "Pleora":  
            self.camera.Close()

        elif self.method == "Opencv":
            self.camera.cap.release()

    def saveImage(self):

        if platform == "linux" or platform == "linux2":
            raise Exception("Not Linux compatible yet")

        elif platform == "darwin":  # OS X
            raise Exception("Not Mac compatible yet")

        elif platform == "win32":
            win_path = "../wellplatemicroscope/captures"

        #automatically make dir
        dt_string = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = win_path + "/" + dt_string + ".tif"
        os.makedirs(win_path, exist_ok=True)
        skimage.io.imsave(filename, np.uint8(self.GetFrame()))

    def save_scan(self, im_data, metadata=None):

        if metadata is None: metadata={}

        im_data = np.array(im_data)

        path_out = self.save_path 
        if self.save_format == "HDF5":

            if im_data.ndim == 2:          im_data = im_data[None,None,:] 
            elif im_data.ndim == 3:        im_data = im_data[None,:] 

            if im_data.shape[-1] == 3:  im_data = im_data.transpose(0,3,1,2)

            dt_string = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = path_out + "/" + dt_string + ".H5"
            os.makedirs(path_out, exist_ok=True)
            H5.write_h5(filename, im_data, metadata)


    async def setCameraSetting(self, setting, value):
        print(setting)

        if self.method == "Opencv": return

        if setting == "Brightness":
            self.settings["Brightness"] = value
            await self.bridge._send_command_agr(f"s{str(value)}")
        elif setting == "ExposureTime":
            self.settings["ExposureTime"] = value
            self.camera.SetParameterDouble("ExposureTime", value)
        elif setting == "Gain":
            self.settings["Gain"] = value
            self.camera.SetParameterDouble("Gain", value)              
        else:
            print("Setting not found")
       
    #get histogram
    #Slider for contrast
    #set exposure
    #set shutterspeed




    
