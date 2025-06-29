from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from router import router, bridge, locations, calibrator, liveCam
import threading
import webbrowser

app = FastAPI()
api = FastAPI()
api.include_router(router)
app.mount('/api', api)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

## Open the browser on start-up, but annoying during development 
#webbrowser.open('http://127.0.0.1:8000')


# Startup sequence
@app.on_event('startup')
async def app_startup():

    print("[---------------------- Startup: data----------------------]")
    await locations.loadData()
    print("[---------------------- Startup: Serial bridge-------------]")
    if await bridge.open_bridge():
        # Only run these things if there is a machine connected.
        # Get limits from machine
        await bridge.getMachineLimits()
        locations.machineLimits = bridge.machineLimits
        print(f"Machine limits: {bridge.machineLimits}")
    else: 
        print("No machine connected, using default limits")
        bridge.machineLimits = (265,250,58)
        locations.machineLimits = (265,250,58)

    print("[---------------------- Startup: Camera -------------------]")
    liveCam.run_main()
    
    print("[---------------------- Startup: Calibrator----------------]")

    # await bridge._send_command_agr("$H")
    # calibrator.calibrate_z()

    # program startup cycle (Find home point, go to calibration point, calibrate, set calibration)


