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
INT = 1.0
LR = "l"
DUR = 1
IMG = (DUR * FPS) 
XY = "X"

#User interface:
index_html = '''
<!DOCTYPE html>
<html> 
    <h1>StopmotionHat</h1>
        <hr>
    <p>finished action: </p>  <h4>   <strong>{{ htmlcommand }}</strong> </h4> 
         <hr>
  <form action="http://{{ ipn }}:8080/shutdown">
    <input type="submit" value="shutdown system" /></form>
   
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
                <option id='20'>20</option>
    
            </select>
    <p> direction: </p>
    
    
            <select name = "lr" id = "lr" >
   
                <option id='Left'>Left</option>
                <option id='Right'>Right</option>
                
                
                
    
            </select>
        <p> active motors: </p>
    
    
            <select name = "xy" id = "xy" >
   
                <option id='X'>X</option>
                <option id='Y'>Y</option>
                <option id='X&Y'>X&Y</option>
                <option id='None'>None</option>
                
    
            </select>
            <p> duration: </p>
    
    
            <select name = "dur" id = "dur" >
   
                <option id='1'>1</option>
                <option id='5'>5</option>
                <option id='10'>10</option>
                <option id='15'>15</option>
                <option id='20'>20</option>
                <option id='25'>25</option>
                <option id='30'>30</option>
    
            </select>
        <input type="submit" value="Set Values">
        <br><hr>
     


    
</html>
'''
@route('/shutdown')
def shutdown():
    os.system("sudo shutdown -h now")

@route('/shutter')
def shutter():
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    shutter = 8
    autofocus = 10
    GPIO.setup(autofocus, GPIO.OUT)
    GPIO.setup(shutter, GPIO.OUT)
    GPIO.output(autofocus,1)
    time.sleep(2.5)
    GPIO.output(shutter,1)
    time.sleep(2.5)
    GPIO.output(shutter,0)
    GPIO.output(autofocus,0)
    return template(index_html, htmlcommand= "manual capture", ipn = ip)

@route('/autofocus')
def autofocus():
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    autofocus = 10
    GPIO.setup(autofocus, GPIO.OUT)
    GPIO.output(autofocus,1)
    time.sleep(2.5)
    GPIO.output(autofocus,0)
    return template(index_html, htmlcommand= "autofocus", ipn = ip)

@route('/move/<lr>')
def move(lr):
    global IMG
    global INT
    global FPS
    global LR
    global DUR
    
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    #GPIO list: 
    enx = 26
    stepx = 18
    dirx = 16
    eny = 32
    stepy = 24
    diry = 22
    
    #set up pins
    GPIO.setup(enx, GPIO.OUT)
    GPIO.setup(stepx, GPIO.OUT)
    GPIO.setup(dirx, GPIO.OUT)
    
    GPIO.setup(eny, GPIO.OUT)
    GPIO.setup(stepy, GPIO.OUT)
    GPIO.setup(diry, GPIO.OUT)
    
    #deactivate stepper drivers
    GPIO.output(enx, 0)
    GPIO.output(eny, 0)
    if lr == "l":
        
        GPIO.output(diry, 0)
        GPIO.output(dirx, 0)
        for x in range(0,200):
            GPIO.output(stepx,1)
            GPIO.output(stepy,1)
            time.sleep(0.01)
            GPIO.output(stepx,0)
            GPIO.output(stepy,0)
            time.sleep(0.01)
            print("did step " + str(x))
        return template(index_html, htmlcommand= "step left", ipn = ip)
    elif lr == "r":
        GPIO.output(diry, 1)
        GPIO.output(dirx, 1)
        for x in range(0,200):
            GPIO.output(stepx, 1)
            GPIO.output(stepy, 1)
            time.sleep(0.01)
            GPIO.output(stepx, 0)
            GPIO.output(stepy, 0)
            time.sleep(0.01)
        return template(index_html, htmlcommand= "step right", ipn = ip)
    else:
        return template(index_html, htmlcommand= "ERROR", ipn = ip)
    
    
#sets the values for automatic mode
@route('/FPS/<fps>/<it>/<lr>/<dur>/<xy>')
def FPS(fps, it, lr, dur, xy):
    global FPS
    global INT
    global LR
    global XY
    global DUR
    
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
    IMG = int(DUR) * int(FPS)
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BOARD)
    #GPIO list: 
    enx = 26
    stepx = 18
    dirx = 16
    eny = 32
    stepy = 24
    diry = 22
    shutter = 8
    autofocus = 10
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
    #enable steppers and direction according to settings
    #enable steppers according to XY
    if XY == "X":
        GPIO.output(enx,0)
        GPIO.output(eny,1)
    elif XY == "Y":
        GPIO.output(enx,1)
        GPIO.output(eny,0)
    elif XY == "X&Y":
	    GPIO.output(enx,0)
	    GPIO.output(eny,0)
    else:
        GPIO.output(enx,1)
        GPIO.output(eny,1)
    #set direction according to LR
    if LR == "Left":
	    GPIO.output(dirx,1)
	    GPIO.output(diry,1)
    else:
	    GPIO.output(dirx,0)
	    GPIO.output(diry,0)
    #     
    
    # # do a for loop according to number of IMG needed with wait times inbetween according to INT
    for x in range(0, IMG):
        GPIO.output(autofocus,1)
        time.sleep(2.5)
        GPIO.output(shutter,1)
        time.sleep(2.5)
        GPIO.output(shutter,0)
        GPIO.output(autofocus,0)    
        for y in range(0,200):
            GPIO.output(stepx,1)
            GPIO.output(stepy,1)
            time.sleep(0.01)
            GPIO.output(stepx,0)
            GPIO.output(stepy,0)
            time.sleep(0.01)
        time.sleep(float(INT))
        print("image # "+ str(x + 1) + " taken")
        
    return template(index_html, htmlcommand= str(IMG) + " Sequence finished", ipn = ip)


@route('/')
def index():
    return template(index_html, htmlcommand="startup", ipn = ip)
    








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



