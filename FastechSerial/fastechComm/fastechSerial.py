import serial
import time

# from utill.CalcCRC import calcCRC
from fastechComm.util.CalcCRC import calcCRC
from fastechComm.fastechCommError import FMM_Error

ASCII_NODE          = 0xAA
ASCII_NODE_START    = 0xCC
ASCII_NODE_END      = 0xEE

PACKET_SIZE_PREFIXED = 5    #Slave No.(1) + Command (1) + ReturnCode (1) + Checksum (2) 
FRAME_HEADER_TAIL_SIZE = 4


MAX_SEND_BUFFER_SIZE = 512
MAX_RECV_BUFFER_SIZE = 256

class FastechReceivingStatus:
    RETURN_OK               = 0#
    RETURN_TIMEOUT          = 1#
    RETURN_RECV_NOT_ENOUGH  = 2#
    #RETURN_INCORRECTTARGET = 3
    RETURN_RECV_NO_DATA     = 4#
    RETURN_DATA_OVERFLOW    = 5#
    RETURN_CORRUPT_SENT_DATA = 6#
    RETURN_CORRUPT_RECV_DATA = 7#
    RETURN_NOT_SUPPORTED    = 8#


class FastechSerial:
    def __init__(self, port_name, time_out):
        
        self.fs = serial.Serial(port= port_name,
                                baudrate=115200,
                                parity=serial.PARITY_NONE,
                                stopbits=serial.STOPBITS_ONE,
                                bytesize=serial.EIGHTBITS,
                                timeout=10)

        self.res_queue = []
        self.count = 0
        
    def _sendPacket(self, slaveNo, cmd, data=b''):
        packet = []
    
        #Add Header
        packet.append(ASCII_NODE)
        packet.append(ASCII_NODE_START)

        ################
        #ADD Frame Data#
        ################
        packet.append(slaveNo)#Add Slave ID
        packet.append(cmd)#Add Frame type
        
        for byte in data:
            packet.append(byte)
        
        #Get CRC (Slave ID, Frame Type, Data)
        crc = calcCRC(bytes(packet[2:]))

        #Add CRC Low, High
        packet.append(crc & 0xFF)
        packet.append((crc >> 8) & 0xFF)

        addNum = 0
        for idx, byte in enumerate(packet[2:]):
            #Byte stuffing(Add '0xAA' behind real data)
            if byte == ASCII_NODE:
                packet.insert(idx + 2 + addNum, byte)
                addNum += 1
        ################################

        #Add Tail
        packet.append(ASCII_NODE)
        packet.append(ASCII_NODE_END)
        
        #Send packet
        try:
            write_len = self.fs.write(bytes(packet))
        except:
            print('except write')
            return -1

        #check write bytes length
        if write_len != len(packet):
            return 0

        return write_len


    def _recvPacket(self, slaveNo, cmd):
        #Recive Packet##############################
        res = self.fs.read(self.fs.inWaiting())
        ############################################

        #Check Receive no data#######################
        if len(res) < PACKET_SIZE_PREFIXED + FRAME_HEADER_TAIL_SIZE:#Header(2) + Recv Frame Data(5) + Tail(2) 
            '''
                ERROR: Recived Packet too small
            '''
            print(f"ERROR: Recived Packet too small {res}")
            return (FastechReceivingStatus.RETURN_RECV_NOT_ENOUGH, res)#2
        ############################################

        #Check header and tail######################
        if (res[0] != ASCII_NODE or
            res[1] != ASCII_NODE_START or
            res[-2] != ASCII_NODE or
            res[-1] != ASCII_NODE_END) :
            '''
                ERORR: Header or Tail
            '''
            print(f"ERR: Invalid Header or Tail {res}")
            #I think it should be fix....  [comm.c line:174]
            return (FastechReceivingStatus.RETURN_TIMEOUT, res)#1
        ############################################

        #Unstuffing bytes###########################
        frame_data = b''
        b_pre = 0x00
    
        for b in res[2:-2]:
            if b == 0xaa and b_pre == 0xaa:
                b_pre = 0x00
            else:
                frame_data = frame_data + bytes([b])
                b_pre = b

        result = res[:2] + frame_data + res[-2:]
        ############################################

        #Check data overflow########################
        if len(frame_data) >= MAX_RECV_BUFFER_SIZE:
            '''
                ERROR: DATAOVERFLOW
            '''
            print(f"ERR: Data overflow{res}")
            return (FastechReceivingStatus.RETURN_DATA_OVERFLOW, result)#5
        ############################################

        #Check CRC#################################
        if calcCRC(result[2:-2]) != 0x00:
            
            '''
                ERORR: CRC
            '''
            print(f"ERR: Invalid CRC {result}")
            return (FastechReceivingStatus.RETURN_CORRUPT_RECV_DATA, result)#7
        ###########################################

        #check slaveNo, cmd########################
        if frame_data[0] != slaveNo or frame_data[1] != cmd:
            '''
                ERORR: CRC
            '''
            #different from Comm.c
            return (FastechReceivingStatus.RETURN_CORRUPT_RECV_DATA, result)#7
        ###########################################

        #check CommStatus##########################
        if frame_data[2] == FMM_Error.FMP_FRAMETYPEERROR:#128
            return (FastechReceivingStatus.RETURN_OK, result)
        elif frame_data[2] == FMM_Error.FMP_PACKETCRCERROR:#170
            return (FastechReceivingStatus.RETURN_CORRUPT_SENT_DATA, result)
        ###########################################
        
        
        #return result
        return (FastechReceivingStatus.RETURN_OK, result)
        

    def doSendCommand(self, slaveNo, cmd, data=b'', timeout=5):
        time_limit = timeout
        start_time = time.time()
        nReturn = -1
        res, res_data = (-1, b'')

        self.count += 1

        while(res != FastechReceivingStatus.RETURN_OK):
            
            if time.time() - start_time > time_limit:# time out default 5sec
                nReturn = FastechReceivingStatus.RETURN_TIMEOUT
                break

            if self._sendPacket(slaveNo, cmd, data) <= 0:
                return (FMM_Error.FMM_SENDPACKET_ERROR, res_data)
            
            time.sleep(0.01)

            res, res_data = self._recvPacket(slaveNo, cmd)

            if res == FastechReceivingStatus.RETURN_DATA_OVERFLOW:
                nReturn = FMM_Error.FMC_RECVPACKET_ERROR
            elif res == FastechReceivingStatus.RETURN_CORRUPT_RECV_DATA:
                nReturn = FMM_Error.FMC_CRCFAILED_ERROR

        if nReturn == FastechReceivingStatus.RETURN_TIMEOUT:
            nReturn = FMM_Error.FMC_TIMEOUT_ERROR
        elif (nReturn == FastechReceivingStatus.RETURN_RECV_NOT_ENOUGH 
            or nReturn == FastechReceivingStatus.RETURN_RECV_NO_DATA 
            or nReturn == FastechReceivingStatus.RETURN_DATA_OVERFLOW):
            nReturn = FMM_Error.FMC_RECVPACKET_ERROR
        elif nReturn == FastechReceivingStatus.RETURN_CORRUPT_SENT_DATA:
            nReturn = FMM_Error.FMP_PACKETERROR
        else:
            nReturn = res_data[4]

        return (nReturn, res_data[2:-2])

    def doSendCommandNoRes(self, slaveNo, cmd, data=b''):
        self._sendPacket(slaveNo, cmd, data)

        



        

        

            
            