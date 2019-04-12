#import modules
import os
import time
import serial.tools.list_ports as port_list
import serial
import socket
from bottle import route, run, template, auth_basic
import threading
ip = (((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [
    [(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
     [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]))

#global Vars:
FPS = 12
INT = 1
LR = 0
DUR = 0
IMG = (DUR * FPS) 
XY = 0
#User interface:
index_html = '''
<!DOCTYPE html>
<html> 
    <h1>StopmotionHat</h1>
        <hr>
    <p>finished action: </p>  <h4>   <strong>{{ htmlcommand }}</strong> </h4> 
         <hr>
  
   
    <form action="http://{{ ipn }}:8080/shutter">
    <input type="submit" value="manual shutter" /></form>
        
    <form action="http://{{ ipn }}:8080/autofocus">
    <input type="submit" value="Autofocus" /></form>
        <br>
    <form action="http://{{ ipn }}:8080/move/l">
    <input type="submit" value="manual move left" /></form>
        
    <form action="http://{{ ipn }}:8080/move/r">
    <input type="submit" value="manual move right" /></form>
    
     <form action="http://{{ ipn }}:8080/capture">
    <input type="submit" value="capture" /></form>
    
    <p> FPS: </p>
    <script>
            function FPS()
            {
            var url="http://{{ipn}}:8080/FPS/" + document.getElementById("fps").value + "/" + document.getElementById("it").value + "/" + document.getElementById("lr").value + "/" + document.getElementById("dur").value + "/" + document.getElementById("xy").value;
            location.href=url;
            return false;
            }
            </script>
    <form  onSubmit="return FPS();">
            <select name = "fps" id = "fps" >
   
                
                <option id='12'>12</option>
                <option id='18'>18</option>
                <option id='24'>24</option>
                
    
            </select>
        
    <p> intervall: </p>
    
    
            <select name = "it" id = "it" >
   
                <option id='1'>1</option>
                <option id='2'>2</option>
                <option id='5'>5</option>
                <option id='10'>10</option>
                
    
            </select>
    <p> direction: </p>
    
    
            <select name = "lr" id = "lr" >
   
                <option id='Left'>Left</option>
                <option id='Right'>Right</option>
                <option id='None'>None</option>
                
                
    
            </select>
        <p> active motors: </p>
    
    
            <select name = "xy" id = "xy" >
   
                <option id='X'>X</option>
                <option id='Y'>Y</option>
                <option id='X&Y'>X&Y</option>
                
                
    
            </select>
            <p> duration: </p>
    
    
            <select name = "dur" id = "dur" >
   
                <option id='1'>1</option>
                <option id='5'>5</option>
                <option id='10'>10</option>
                
                
    
            </select>
        <input type="submit" value="Set Values">
    


    
</html>
'''

@route('/shutter')
def shutter():
    pass

@route('/autofocus')
def autofocus():
    pass

@route('/move/<lr>')
def move(lr):
    pass
#sets the values for automatic mode
@route('/FPS/<fps>/<it>/<lr>/<dur>/<xy>')
def FPS(fps, it, lr, dur, xy):
    global FPS
    global INT
    global LR
    global XY
    
    FPS = fps
    INT = it
    LR = lr
    DUR =dur
    XY = xy
    return template(index_html, htmlcommand="FPS: "+ FPS + " intervall: " + INT + " Direction: "+ LR + " Duration: "+ DUR + " Move: "+ XY, ipn = ip)

@route('/capture')
def capture():
    global IMG
    global INT
    global FPS
    global LR
    global DUR
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    #GPIO list: 
    enx = 0
    stepx = 0
    dirx = 0
    eny = 0
    stepy = 0
    diry = 0
    shutter = 0
    autofocus = 0
    #set up pins
    GPIO.setup(enx, GPIO.OUT)
    GPIO.setup(stepx, GPIO.OUT)
    GPIO.setup(dirx, GPIO.OUT)
    
    GPIO.setup(eny, GPIO.OUT)
    GPIO.setup(stepy, GPIO.OUT)
    GPIO.setup(diry, GPIO.OUT)
    
    GPIO.setup(shutter, GPIO.OUT)
    GPIO.setup(autofocus, GPIO.OUT)
    #deactivate stepper drivers
    GPIO.output(enx, 1)
    GPIO.output(eny, 1)
    #start cycle:
    # # enable steppers and direction according to settings
    #enable steppers according to XY
    #
    #set direction according to LR
    # if LR == L:
    #     
    
    # # do a for loop according to number of IMG needed with wait times inbetween according to INT
    # for x in range(0, IMG):
    #     GPIO.output(shutter, 1)    
    #     GPIO.output(stepx,1)
    #     GPIO.output(stepy,1)
    #     time.sleep(0.25)
    #     GPIO.output(shutter, 0) 
    #     GPIO.output(stepx,0)
    #     GPIO.output(stepy,0)
    #     time.sleep(INT)
    pass
@route('/')
def index():
    return template(index_html, htmlcommand="startup", ipn = ip)
    
#templaet for rpi.gpio
@route('/lmio')

def lmio():
    
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    #GPIO list: ms_ =microswitch
    ms_printer_z = 38
    ms_endstop_X_min = 36
    ms_endstop_X_max = 40
    ms_emergency = 29
    ms_plates = 32
    ms_printing = 31
    
    # setup
    
    GPIO.setup(ms_printer_z, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(ms_endstop_X_min, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(ms_endstop_X_max, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(ms_emergency, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(ms_plates, GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(ms_printing, GPIO.IN, GPIO.PUD_UP)
    # read pins ; rd_ = read
    rd_printer_z = GPIO.input(ms_printer_z)
    rd_endstop_X_min = GPIO.input(ms_endstop_X_min)
    rd_endstop_X_max = GPIO.input(ms_endstop_X_max)
    rd_emergency = GPIO.input(ms_emergency)
    rd_plates = GPIO.input(ms_plates)
    rd_printing = GPIO.input(ms_printing)
    #set vars to required string value if conditions apply
    if rd_printer_z == 0:
        printer_Z = "Z homed"  # "Z homed"
    else:
        printer_Z = " Z not homed"
    if rd_endstop_X_min == 0:
        endstop_X_min = "homed"  # "homed"
    else:
        endstop_X_min = "not homed"
    if rd_endstop_X_max == 0:
        endstop_X_max = "clear" # clear
    else:
        endstop_X_max = "blocked"
    if rd_emergency == 0:
        emergency = "NONE"  # "NONE"
    else:
        emergency = "ALARM!!"
    if rd_plates == 0:
        plates = "LOADED"  # "LOADED"
    else:
        plates = "No plates left"
    if rd_printing == 0:
        printer = "Printing"  # "Printing"
    else:
        printer = "Operator needs to confirm printer is printing"
    #read gpio pins and return a list of the sates
    safety_check = [printer, printer_Z, endstop_X_min, endstop_X_max, emergency, plates]
    return safety_check
# does only work on real hardware








def foreground():
    #routine to run the webserver
    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 8080))
        run(host='0.0.0.0', port=port, debug=True)

def background():
    
    pass
        
        
daemon = threading.Thread(name='background', target=background)
htmlbus = threading.Thread(name='foreground', target=foreground)
    
htmlbus.start()
daemon.start()    




