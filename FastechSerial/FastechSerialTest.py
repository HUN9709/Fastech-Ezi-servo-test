from fastechComm.fastechSerial import FastechSerial
from fastechComm.fastechEziServoPlusRmini import FastechEziServoPlusRmini
import time

if __name__ == '__main__':
    fsmi = FastechEziServoPlusRmini('COM5', 20)

    # res = fsmi.fas_moveSingleAxisIncPos(0, 200000, 100000)

    # print(res)

    res = fsmi.fas_setParameter(0, 6, 170)

    print(res)
    
    #C에서는 recv data 'ReadFile(hComm, &by, 1, &received, NULL);' 로 1바이트씩 읽어와 while, swittch 문으로 처리
    #python에서는 한번에 모두 읽어오므로 RETURN Code 수정 필요할듯





