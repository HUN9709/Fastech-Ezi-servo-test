import zmq
import json
import time

class FastechClient:
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:5555")

    def getAllStatus(self):
        req_data = {
            "cmd" : 'getAllStatus',
        }

        self.socket.send_json(req_data)

        res = self.socket.recv()
        res = json.loads(res)

        return res

    def moveToOrigin(self):
        req_data = {
            "cmd" : 'moveToOrigin',
        }

        self.socket.send_json(req_data)

        res = self.socket.recv()
        res = json.loads(res)

        return res

    def moveStop(self):
        req_data = req_data = {
            "cmd" : 'moveStop',
        }

        self.socket.send_json(req_data)

        res = self.socket.recv()
        res = json.loads(res)

        return res

    def emergencyStop(self):
        req_data = {
            "cmd" : 'emergencyStop',
        }

        self.socket.send_json(req_data)

        res = self.socket.recv()
        res = json.loads(res)

        return res


if __name__ == "__main__":
    fas_client = FastechClient()
    for i in range(1, 100):
        time.sleep(0.01)

        start_time = time.time()

        if i % 10 == 0:
            if (i / 10) % 2 == 1:
                result = fas_client.moveToOrigin()
            else:
                result = fas_client.emergencyStop()
        else:
            result = fas_client.getAllStatus()

        print(i, result, time.time() - start_time)
