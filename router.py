from datetime import datetime
from fastapi import APIRouter, WebSocket
from serialBridge import SerialBridge
from liveCam import LiveCam
from locations import Locations
from calibrator import Calibrator
from wellPlateManager import WellPlateManager
from routinemanager import RoutineManager
import asyncio


import skimage as skimage 
from fastapi.responses import FileResponse
import cv2

router = APIRouter()
locations = Locations()
bridge = SerialBridge(locations)
liveCam = LiveCam(bridge)
calibrator = Calibrator(bridge, liveCam, locations)
# I am confused about this. Wellplate manager needs locations, but right now, it gets locations from bridge, because bridge also has locations. 
# But calibrator alos needs bridge and locations, but calibrator gets them both as an argument, 
# but if i do this for wellplate manager, it will be a circular dependency?
wellPlateManager = WellPlateManager(bridge)
routinemanager = RoutineManager(bridge, liveCam, locations)


@router.get("/takePicture")
async def take_picture():
    liveCam.saveImage()
    
@router.get("/goto")
async def goto(x: float, y: float, z: float, sys: int):
    await bridge.goto(x, y, z, sys)

# Add limits.. and should be in livecam class
@router.get("/setcamerasetting")
async def setCameraSetting(setting: str, value: float):
    await liveCam.setCameraSetting(setting, value)
    
@router.get("/sendcommand")
async def sendcommand(command):
    await bridge._send_command_agr(command)

@router.get("/getdata")
async def read_getdata():
    return locations.locationbook


@router.get("/autofocus")
async def autofocus():
    # await bridge.stream_g_code_file("gcode/96.gcode")
    await calibrator.calibrate_z()

@router.get("/updatelocationlist")
async def updatelocationlist(x, y, z, name):
    await locations.editLocation(x, y, z, name)

@router.get("/getposition")
async def getposition():
    x = await locations.getCurrentLocation()
    print(x)
    return x


@router.get("/captureimage")
async def captureImage():
    liveCam.saveImage()

@router.get("/movetowell")
async def moveToWell(plateType, plateNumber, coordinate):
    await wellPlateManager.moveToWell(plateType, plateNumber, coordinate)

@router.get("/getmachinelimits")
async def getMachineLimits():
    return bridge.machineLimits

@router.get("/dozscan")
async def dozscan(start, end, step):
    await routinemanager.do_z_scan(start, end, step)

@router.websocket('/livefeed')
async def stream_video(socket: WebSocket):
    print("Client connected from: " + socket.client.host)

    # Standard value, later we will fetch these values from a file
    if liveCam.method == "Pleora":
        liveCam.camera.SetParameterDouble("ExposureTime", 100000)
    
    await socket.accept()

    try:
        while True:
            image = liveCam.GetFrame()[...,::-1]
            _, im = cv2.imencode('.png', image)
            img_bytes = im.tobytes()
            await socket.send_bytes(img_bytes)
            await asyncio.sleep(0.04)
    except:
        print("Client disconnected: " + socket.client.host)


