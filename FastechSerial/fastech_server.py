import sys
import zmq
import time
import json
from fastechComm.fastechEziServoPlusRmini import FastechEziServoPlusRmini

class FastechZmqServer:
    def __init__(self):
        #Get Zmq Response Socket
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.bind("tcp://*:5555")

        #Get Object that Serial Comm with Fastech Driver 
        self.fsmi = FastechEziServoPlusRmini('COM5', 20)

    def run(self):
        while True:
            msg_recv = self.socket.recv()
            
            msg_recv = json.loads(msg_recv)


            if msg_recv['cmd'] == "getAllStatus":
                start = time.time()
                res = self.fsmi.fas_getAllStatus(0)#0.01
                print(f'getAllStatus:{time.time() - start}')
                send_data = {
                    'status' : res[0],
                    'fas_status' : int.from_bytes(res[3], 'little'),
                    'cmd_pos' : res[4],
                    'act_pos' : res[5],
                    'act_vel' : res[6],
                    'pos_err' : res[7],
                }

                self.socket.send_json(send_data)

            elif msg_recv['cmd'] == "moveToOrigin":
                start = time.time()
                res = self.fsmi.fas_moveOriginSingleAxis(0)
                print(f'moveToOrigin:{time.time() - start}')
                
                send_data = {
                    'status' : res[0],
                }

                self.socket.send_json(send_data)

            elif msg_recv['cmd'] == "moveStop":
                start = time.time()
                res = self.fsmi.fas_moveStop(0)
                print(f'moveStop:{time.time() - start}')

                send_data = {
                    'status' : res[0],
                }

                self.socket.send_json(send_data)

            elif msg_recv['cmd'] == "emergencyStop":
                start = time.time()
                res = self.fsmi.fas_emergencyStop(0)
                print(f'moveStop:{time.time() - start}')

                send_data = {
                    'status' : res[0],
                }

                self.socket.send_json(send_data)

if __name__ == '__main__':
    fas_server = FastechZmqServer()

    fas_server.run()