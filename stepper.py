import RPi.GPIO as GPIO
import time
import socket
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) 
enable_pin = 12
coil_A_1_pin = 7
coil_A_2_pin = 11
coil_B_1_pin = 16
coil_B_2_pin = 18
light_L_1_pin = 22 
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
GPIO.setup(light_L_1_pin, GPIO.OUT) 
GPIO.output(enable_pin, 1)
unsigned_downflag = 6
unsigned_upflag = 0
unsigned_lightflag = 0

def forward(delay, steps): 
    for i in range(0, steps): 
        setStepF(1, 1, 1, 0) 
        time.sleep(delay) 
        setStepF(1, 1, 0, 1) 
        time.sleep(delay) 
        setStepF(1, 0, 1, 1) 
        time.sleep(delay) 
        setStepF(0, 1, 1, 1) 
        time.sleep(delay)
       # setStepF(1, 1, 1, 1) 
       # time.sleep(delay)
        
def backwards(delay, steps): 
    for i in range(0, steps): 
        setStepF(0, 1, 1, 1) 
        time.sleep(delay) 
        setStepF(1, 0, 1, 1) 
        time.sleep(delay) 
        setStepF(1, 1, 0, 1) 
        time.sleep(delay) 
        setStepF(1, 1, 1, 0) 
        time.sleep(delay)
      #  setStepF(1, 1, 1, 1) 
        #time.sleep(delay)
        
def setStepF(w1, w2, w3, w4): 
    GPIO.output(coil_A_1_pin, w1) 
    GPIO.output(coil_A_2_pin, w2) 
    GPIO.output(coil_B_1_pin, w3) 
    GPIO.output(coil_B_2_pin, w4)
    
def setStepB(w1, w2, w3, w4):
    GPIO.output(coil_B_2_pin, w4)
    GPIO.output(coil_B_1_pin, w3)
    GPIO.output(coil_A_2_pin, w2)
    GPIO.output(coil_A_1_pin, w1)
    
def setStepC(c1):
    GPIO.output(light_L_1_pin, c1)
     
     
time.sleep(30)    
sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

#print(unsigned_downflag)
sock.bind(('10.42.0.1',2233))
while True:
    setStepF(0, 0, 0, 0)
    delay = 4
    steps = 25
    data_raw,addr=sock.recvfrom(1024)
    data=data_raw.decode('utf,8')
    print(data)
    
    
    if "up" in data:
      if(unsigned_upflag < 6):  
       forward(int(delay) / 1000.0, int(steps))
       unsigned_upflag = unsigned_upflag +1
       unsigned_downflag = unsigned_downflag -1
      
    if "down" in data:
      if(unsigned_downflag < 6):  
       backwards(int(delay) / 1000.0, int(steps))
       unsigned_upflag = unsigned_upflag -1
       unsigned_downflag = unsigned_downflag +1
     
    if "lighton" in data:
        setStepC(1)
    if "lightoff" in data:
        setStepC(0)
       
    setStepF(0, 0, 0, 0) 
    #time.sleep(delay)
#     time.sleep(0.1) 
   