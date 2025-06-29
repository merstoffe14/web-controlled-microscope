# WebsiteControlledMicroscope
## To run the website:

You need to install the requirements.txt using: 
```
pip install -r requirements.txt
```

You will also need to pip install uvicorn (is not in the requirements.txt) and install the vimba sdk from their website (when prompted, select: for application development).

Make sure both cables (Mako camera and microcontroller) are plugged in.
The automatic com port finder code has not been implemented yet, so look up the comport (in device manager) and change it at the top of serialBridge.py
Then browse to the folder which contains main.py and run this command:

```
uvicorn main:app --reload   
```

If it starts with no errors, then the website should be running at localhost:8000.

To avoid a couple of issues, please press the calibrate home button before you do anything else.

## Known issues:

* You need to reload the website sometimes for the liveview to start working

* When you use joggin, you can accidentaly soft lock the system by trying to go out of bounds (this issue has been resolved for moving based on a given coordinate)
 There is not yet a way to reset the system using the website, so you need to restart the code (ctrl + c in terminal) 

* The autofocus button is still called "run file" and the enpoint that it calls to still has a placeholder name.

# 
Send me a message anytime that you have a problem with this.
merlijn.stoffels@student.uantwerpen.be
