from adafruit_servokit import ServoKit
import pandas as pd
import time
import datetime
import os

last_path = '/home/pi/log/com/last.csv'
log_path = '/home/pi/log/com/log.csv'

class Motors():
    def __init__(self, ):
        self.serv_range = dict()
        self.serv_range[0] = {'mid': 75, 'min': 10, 'max': 140} # HCSR04
        self.serv_range[1] = {'mid': 55, 'min': 0, 'max': 155} # front cam pan
        self.serv_range[2] = {'mid': 70, 'min': 30, 'max': 135} # front cam tilt

        self.serv_range[9] = {'mid': 30, 'min': 0, 'max': 120} # arm grip open/close
        self.serv_range[10] = {'mid': 90, 'min': 0, 'max': 180} # arm rotate
        self.serv_range[11] = {'mid': 180, 'min': 0, 'max': 180} # wrist
        self.serv_range[12] = {'mid': 85, 'min': 82, 'max': 180} # elbow
        self.serv_range[13] = {'mid': 30, 'min': 20, 'max': 180} # sholder
        self.serv_range[14] = {'mid': 165, 'min': 130, 'max': 180} # base
        self.servos = {s: 0 for s in self.serv_range}
        
        self.kit = ServoKit(channels=16)
        
        self.init_servos()
        
        
    def init_servos(self, servos=[]):
        for s in servos:
            time.sleep(1)
            self.kit.servo[s].angle = self.serv_range[s]['mid']
            self.servos[s] = self.serv_range[s]['mid']
        if len(servos) > 0:
            print(f'servos {" ".join([str(s) for s in servos])} init complete')
        
    def move_arm(self, current, to, step=0.5):
        order_ind = [0, 1, 5, 4, 3, 2]
        while(current != to):
            print(current, to)
            for ind in order_ind:
                if to[ind] > current[ind]:
                    dif = min(step, to[ind]-current[ind])
                    current[ind] += dif
                    kit.servo[ind].angle = current[ind]
                elif to[ind] < current[ind]:
                    dif = min(step, current[ind]-to[ind])
                    current[ind] -= dif
                    kit.servo[ind].angle = current[ind]
        return current
    
    def move_servo(self, num, trg, intervals=None, pause=1):
        cur = m.servos[num]
        if not intervals:
            intervals = trg - cur
        if trg != cur:
            off = (trg - cur)//intervals
            for i in range(intervals-1):
                cur += off
                self.kit.servo[num].angle = cur
                time.sleep(pause/intervals)
                self.servos[num] = cur
            cur = trg
            self.kit.servo[num].angle = trg
            self.servos[num] = cur
        return True
    
def get_date(ret_str=True):
    date = datetime.date.today()
    if ret_str:
        return f'{date}'
    return date

def get_dt(ret_str=True):
    dt = datetime.datetime.now()
    if ret_str:
        return f'{dt}'
    return dt

def str_to_dt(dt_str):
    return datetime.datetime.fromisoformat(dt_str)

m = Motors()
m.init_servos(m.servos)

print(f'parsing from {last_path} for servos control')
print(f'logging servos control to {log_path}')

while(True):
    try:
        time.sleep(0.02)
        if os.path.exists(last_path):
            df = pd.read_csv(last_path, usecols=['motor', 'message', 'date', 'dt'])
            for i, row in df.iterrows():
                td = get_dt(ret_str=False) - str_to_dt(row['dt'])
                if td.total_seconds() < 30:
                    s = row['motor']
                    trg = row['message']
                    print(f'servo {s} cur: {m.servos[s]}, trg {trg}')
                    m.move_servo(s, trg, intervals=None, pause=0.01)
            df.to_csv(log_path, header=None, mode='a',)
            os.remove(last_path)
            print(m.servos)
    except Exception as e:
        print(e)
        time.sleep(0.02)
        pass
