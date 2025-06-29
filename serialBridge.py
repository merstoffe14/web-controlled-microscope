from operator import truediv
from re import X
import string
import serial  # type: ignore
import time
from sys import platform
from locations import Locations
import serial.tools.list_ports as port_list


class SerialBridge:

    def __init__(self, locations: Locations) -> None:
        self.locations: Locations = locations
        self.machineLimits: tuple(int,int,int) = (0,0,0)

    async def open_bridge(self):

        # Open grbl serial port        
        if platform == "linux" or platform == "linux2":
            print("Not linux compatible yet")
            raise Exception( "Not Linux compatible yet" )
            #rasp /dev/ttyUSB0. For Pc COM

        elif platform == "darwin":  ##OS X
            print("Not Mac compatible yet")
            raise Exception( "Not Mac compatible yet" )
            
        elif platform == "win32":
            self.s = self.connect_to_ports()

        if self.s is None:  
            print("No microcontroller found") 
            return False
        # Open g-code file
        # Wake up grbl
        self.s.write(b"\r\n\r\n")
        time.sleep(2)   # Wait for grbl to initialize
        self.s.flushInput()  # Flush startup text in serial input
        return True

    async def stream_g_code_file(self, filename= 'grbl.code'):
        # Stream g-code to grbl
        f = open(filename, 'r')
        for line in f:
            await self._send_command_agr(line)


    async def _send_command_agr(self, command):

        if self.s is None: return

        if command == "$H" or command == "G28":
            self.locations.currentLocation = (0,0,0)
            

        l = command.strip()  # Strip all EOL characters for consistency
        print('Sending: ' + l)
        payload = l + '\n'
        q = bytes(payload, encoding='utf-8')
        self.s.write(q)  # Send g-code block to grbl
        grbl_out = self.s.readlines()  # Wait for grbl response with carriage return

        count = 0
        while grbl_out == []:  # Wait for grbl response with carriage return
            print("no GRBL message received, trying again")
            time.sleep(0.01)
            grbl_out = self.s.readlines()
            count += 1
            if grbl_out != [] or count > 10:
                break         

        print("response: \n")
        print(grbl_out)
        return grbl_out

    async def goto(self, x: float, y: float, z: float, sys: int):
        
        if sys == 1: # RELATIVE

            # Set machine to relative mode
            await self._send_command_agr("G91")
            # Check if move would reach limit.
            (x_now,y_now,z_now) = self.locations.currentLocation
            if (x_now + x) > self.machineLimits[0] or (x_now + x < 0):   
                print("limit x would have been reached")
                return
            if y_now + y > self.machineLimits[1] or (y_now + y < 0):
                print("limit y would have been reached")
                return
            if (z_now + z > self.machineLimits[2]) or (z_now + z < 0):
                print("limit z would have been reached")
                return


        if sys == 0: # ABSOLUTE

            # Set machine to absolute mode
            await self._send_command_agr("G90")

            # Limit the movement to the machine limits
            x_max = self.machineLimits[0]
            y_max = self.machineLimits[1]
            z_max = self.machineLimits[2]

            if x < 0:                 x = 0
            if x > x_max:             x = x_max
            if y < 0:                 y = 0
            if y > y_max:             y = y_max
            if z < 0:                 z = 0
            if z > z_max:             z = z_max

        # Construct the command  
        command = f"G0 x {str(x)} y {str(y)} z {str(z)} a {str(x)}"     

        # Send the command and check for ok, if ok, set the current location.   

        answer = await self._send_command_agr(command)
        if answer is None: return
        print(answer)
        print(len(answer))
        if answer[0] == b'ok\r\n' or answer == b'ok\r\n' or len(answer) == 0:
            if sys ==1: #RELATIVE
                move = [x,y,z]
                self.locations.currentLocation = [move[i] + self.locations.currentLocation[i] for i in range(len(move))]
            elif sys ==0: # ABSOLUTE
                self.locations.currentLocation = (x,y,z)


    
    def connect_to_ports(self):
                
        ard=None
        all_ports = list(port_list.comports())
        pos_ports = [p.device for p in all_ports  if "CH340" in p.description]
       
        if len(pos_ports)==0:       print("No Port Found"); ## You may wish to cause an error here.   
        ## Search for Suitable Port
        for port in pos_ports: 
            try:      
                ard = serial.Serial(port, 115200, timeout=0.1)
                print("Connecting to port"+ port)
            except:   
                continue
        return ard

    # the reply is a string that looks like this:
    '''
    $130=200.000
    $131=200.000
    $132=200.000
    '''
    # And these are the last 3 values of a whole list sperated by a newline
    async def getMachineLimits(self):
        settings = await self._send_command_agr("$$")
        lenght = len(settings)
        # I am not sure if this is allowed.
        x = float(str(settings[lenght-2]).split("=")[1][:6])
        y = float(str(settings[lenght-3]).split("=")[1][:6])
        z = float(str(settings[lenght-4]).split("=")[1][:6])
        self.machineLimits = (x,y,z)
        print(f"Machine limits are: {self.machineLimits}")



    
