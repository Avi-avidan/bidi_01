import RPi.GPIO as GPIO
from pylx16a import LX16A
import datetime
import glob
import numpy as np
import datetime

class lift():
    def __init__(self, gpio_ins=[22, 27], gpio_outs=[4, 17]):
        
        self.gpio_ins = gpio_ins #22: Down Stop, 27: Up Stop
        self.gpio_outs = gpio_outs #4: led, 17: action switch in
        self.servo_index = 1
        self.LX16A = self.initialize()
        self.servo1 = LX16A(self.servo_index)
        self.init_gpio()
        print('init complete')
        
    def get_controller(self):
        import serial
        import lewansoul_lx16a

        return lewansoul_lx16a.ServoController(
            serial.Serial(self.servo_path, 115200, timeout=1),)
        
        
    def initialize(self):
        for path in glob.glob('/dev/ttyUSB*'):
            try:
                self.servo_path = path
                LX16A.initialize(path)
                print('lx16a servo found in path:', path)
                break
            except:
                pass

    def init_gpio(self):
        # This setups the GPIO for the two limit switches
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for num in self.gpio_ins:
            GPIO.setup(num, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        for num in self.gpio_outs:
            GPIO.setup(num, GPIO.OUT)
    
    def set_gpio_out(self, val, nums=None):
        if not nums:
            nums = self.gpio_outs
        for num in nums:
            GPIO.output(num, val)
    
    def stop_lx16a(self):
        self.servo1.motorMode(0)

    def activate_lx16a(self, speed=1000):
        self.servo1.motorMode(speed)

    def wait_for_switch(self, time=None, wait_for=[22, 27]):
        # GPIO 22 is servo switch
        # GPIO 27 is far from servo
        self.set_gpio_out(1)

        if not time:
            time = 600

        t1 = datetime.datetime.now()
        i = 0
        while (np.all([not GPIO.input(num) for num in wait_for]+[(datetime.datetime.now() - t1).seconds < time])):
            i += 1
        self.set_gpio_out(0)
        return True

    def move_up(self, seconds=None, up=True, speed=1000):
        if speed < 0:
            speed = 0
        elif speed > 1000:
            speed = 1000
        speed = {0: -1*speed, 1: speed}[up]
        pin = {0: 27, 1: 22}[up]
        self.activate_lx16a(speed)
        self.wait_for_switch(time=seconds, wait_for=[pin])
        self.stop_lx16a()

    def move_down(self, seconds=None, speed=1000):
        self.move_up(seconds=seconds, up=False, speed=speed)