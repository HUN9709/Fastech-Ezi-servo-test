import sys
import time


from fastechComm.fastechSerial import FastechSerial
from fastechComm.fastechFrame import FastechFrame
from fastechComm.fastechCommError import FMM_Error


SLAVE_ALL_COMMAND = 99

class FastechEziServoPlusRmini:
    def __init__(self, port_name, time_out):

        self.fsm = FastechSerial(port_name, time_out)

    #############################
    #No-Motion Command Functions#
    #############################
    def fas_getSlaveInfo(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo, FastechFrame.FRAME_GETSLAVEINFO)

        if nRtn == FMM_Error.FMM_OK:
            rtn_slave = res[3]
            rtn_str = res[4:-3].decode('ascii')

            return nRtn, rtn_slave, rtn_str

        return (nRtn, )
        

    def fas_getMotorInfo(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo, FastechFrame.FRAME_GETMOTORINFO)

        if nRtn == FMM_Error.FMM_OK:
            rtn_motor = res[3]
            rtn_str = res[4:-3].decode('ascii')

            return nRtn, rtn_motor, rtn_str

        return (nRtn, )

    def fas_ACK(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo, FastechFrame.FRAME_FAS_GETCMDPOS)

        rtn_cmdPos = int.from_bytes(res[3:7], 'little', signed=True)

        return nRtn, rtn_cmdPos
    ###########################################################################
    
    #####################
    #Parameter Functions#
    #####################
    def fas_saveAllParameter(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo, FastechFrame.FRAME_FAS_SAVEALLPARAM)

        #need sleep 1sec

        return (nRtn, )

    def fas_setParameter(self, slaveNo, paramNo, paramValue):
        

        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_SETPARAMETER,
                                    data= (paramNo).to_bytes(1, 'little')
                                            + (paramValue).to_bytes(4, 'little', signed=True))

        return (nRtn, )

    def fas_getParameter(self, slaveNo, paramNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_GETPARAMETER,
                                    data=(paramNo).to_bytes(1, "little"))
        if nRtn == FMM_Error.FMM_OK:
            rtn_param = int.from_bytes(res[3:7], 'little', signed=True)
            return nRtn, rtn_param

        return (nRtn, )

    def fas_getROMParameter(self, slaveNo, paramNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_GETPARAMETER,
                                    data=(paramNo).to_bytes(1, "little"))
        if nRtn == FMM_Error.FMM_OK:
            rtn_param = int.from_bytes(res[3:7], 'little', signed=True)
            return nRtn, rtn_param

        return (nRtn, )
    ###########################################################################

    ##############
    #IO Functions#
    ##############
    def fas_setIOInput(self, slaveNo, IOSetMask, IoClearMask):#Not Tested
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_SETIO_INPUT,
                                    data= (IOSetMask).to_bytes(4, 'little')
                                            + (IoClearMask).to_bytes(4, 'little'))

        return (nRtn, )

    def fas_getIOInput(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_GETIO_INPUT)

        if nRtn == FMM_Error.FMM_OK:
            rtn_inputStatus = int.from_bytes(res[3:7], 'little', signed=False)
            return (nRtn, rtn_inputStatus)

        return (nRtn, ) 

        

    def fas_setIOOutput(self, slaveNo, IOSetMask, IoClearMask):#Not Tested
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_SETIO_OUTPUT,
                                    data= (IOSetMask).to_bytes(4, 'little')
                                            + (IoClearMask).to_bytes(4, 'little'))

        return (nRtn, )

    def fas_getIOOutput(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_GETIO_OUTPUT)

        if nRtn == FMM_Error.FMM_OK:
            rtn_outputSatus = int.from_bytes(res[3:7], 'little')
            return (nRtn, rtn_outputSatus)

        return (nRtn, )

    def fas_getIOAssignMap(self, slaveNo, IOPinNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_GET_IO_ASSGN_MAP,
                                    data = (IOPinNo).to_bytes(1, 'little'))

        if nRtn == FMM_Error.FMM_OK:
            rtn_pinStatus = int.from_bytes(res[3:7], 'little')
            rtn_levStatus = res[7]
            return (nRtn, rtn_pinStatus, rtn_levStatus)

        return (nRtn, )

    def fas_setIOAssignMap(self, slaveNo, IOPinNo, IOLogicMask, level):#Not tested
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_SET_IO_ASSGN_MAP,
                                    data= (IOPinNo).to_bytes(1, 'little') + (IOLogicMask).to_bytes(4, 'little') + (level).to_bytes(1, 'little'))

        return (nRtn, )

    def fas_IOAssignMapReadROM(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_IO_ASSGN_MAP_READROM)

        if nRtn == FMM_Error.FMM_OK:
            rtn_execution = res[3]
            return (nRtn, rtn_execution)

        return (nRtn, )
    ###########################################################################

    ################################
    #Servo Driver Control Functions#
    ################################
    def fas_servoEnable(self, slaveNo, onOff):

        value = 0x01 if onOff else 0x00

        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_SERVOENABLE,
                                    data= (value).to_bytes(1, 'little'))

        return (nRtn, )

    def fas_servoAlarmReset(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_ALARMRESET)

        return (nRtn, )

    # def fas_stepAlarmReset(self, slaveNo, reset):

    #     value = 0x01 if reset else 0x00

    #     res = self.fsm.doSendCommand(slaveNo,
    #                                 FastechFrame.FRAME_FAS_STEPALARMRESET,
    #                                 data=(value).to_bytes(1, 'little'))

    #     return res
    ###########################################################################

    ##########################
    #Read Status and Position#
    ##########################
    def fas_getAxisStatus(self, slaveNo):#to be test
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_GETAXISSTATUS)

        if nRtn == FMM_Error.FMM_OK:
            rtn_axisStatus = int.from_bytes(res[3:7], 'little')
            return (nRtn, rtn_axisStatus)
        
        return (nRtn, )

    def fas_getIOAxisStatus(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_GETIOAXISSTATUS)

        if nRtn == FMM_Error.FMM_OK:
            rtn_inStatus = res[3:7]
            rtn_outSatus = res[7:11]
            rtn_axisStatus = res[11:15]
            return (nRtn, rtn_inStatus, rtn_outSatus, rtn_axisStatus)

        return (nRtn, )

    def fas_getMotionStatus(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_GETMOTIONSTATUS)

        if nRtn == FMM_Error.FMM_OK:
            rtn_cmdPos = int.from_bytes(res[3:7], 'little', signed=True)
            rtn_actPos = int.from_bytes(res[7:11], 'little', signed=True)
            rtn_posErr = int.from_bytes(res[11:15], 'little', signed=True)
            rtn_actVel = int.from_bytes(res[15:19], 'little', signed=True)
            rtn_posItemNo = int.from_bytes(res[19:23], 'little')
            return (nRtn, rtn_cmdPos, rtn_actPos, rtn_posErr, rtn_actVel, rtn_posItemNo)

        return (nRtn, )

    def fas_getAllStatus(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_GETALLSTATUS)

        if nRtn == FMM_Error.FMM_OK:
            rtn_inStatus = res[3:7]
            rtn_outSatus = res[7:11]
            rtn_axisStatus = res[11:15]
            rtn_cmdPos = int.from_bytes(res[15:19], 'little', signed=True)
            rtn_actPos = int.from_bytes(res[19:23], 'little', signed=True)
            rtn_posErr = int.from_bytes(res[23:27], 'little', signed=True)
            rtn_actVel = int.from_bytes(res[27:31], 'little', signed=True)
            rtn_posItemNo = int.from_bytes(res[31:35], 'little')
        
            return (nRtn, rtn_inStatus, rtn_outSatus, rtn_axisStatus, rtn_cmdPos, rtn_actPos, rtn_posErr, rtn_actVel, rtn_posItemNo)

        return (nRtn, )

    def fas_setCommandPos(self, slaveNo, cmdPos):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_SETCMDPOS,
                                    (cmdPos).to_bytes(4, 'little', signed=True))

        return (nRtn, )

    def fas_setActualPos(self, slaveNo, actPos):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_SETACTPOS,
                                    (actPos).to_bytes(4, 'little', signed=True))

        return (nRtn, )

    def fas_clearPosition(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_CLEARPOS)
        
        return (nRtn, )

    def fas_getCommandPos(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_GETCMDPOS)
        if nRtn == FMM_Error.FMM_OK:
            rtn_cmdPos = int.from_bytes(res[3:7], 'little', signed=True)
            return (nRtn, rtn_cmdPos)

        return (nRtn, )

    def fas_getActualPos(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_GETACTPOS)
        
        if nRtn == FMM_Error.FMM_OK:
            rtn_actPos = int.from_bytes(res[3:7], 'little', signed=True)
            return (nRtn, rtn_actPos)

        return (nRtn, )

    def fas_getPosError(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_GETPOSERR)

        if nRtn == FMM_Error.FMM_OK:
            rtn_posErr = int.from_bytes(res[3:7], 'little', signed=True)
            return (nRtn, rtn_posErr)

        return (nRtn, )

    def fas_getActualVel(self, slaveNo):#to be test
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_GETACTVEL)

        if nRtn == FMM_Error.FMM_OK:
            rtn_actVel = int.from_bytes(res[3:7], 'little', signed=True)
            return (rtn_status, rtn_actVel)

        return (nRtn, )

    def fas_getAlarmType(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_GETALARMTYPE)

        if nRtn == FMM_Error.FMM_OK:
            rtn_alarmType = res[3]
            return (nRtn, rtn_alarmType)

        return (nRtn, )
    ###########################################################################

    ##################
    #Motion Functions#
    ##################
    def fas_moveStop(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_MOVESTOP)

        return (nRtn, )

    def fas_emergencyStop(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_MOVESTOP)

        return (nRtn, )

    def fas_moveOriginSingleAxis(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_MOVEORIGIN)

        return (nRtn, )

    def fas_moveSingleAxisAbsPos(self, slaveNo, absPos, velocity):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_MOVESINGLEABS,
                                    data=(absPos).to_bytes(4, 'little', signed=True)
                                            + (velocity).to_bytes(4, 'little'))

        return (nRtn, )

    def fas_moveSingleAxisIncPos(self, slaveNo, incPos, velocity):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_MOVESINGLEINC,
                                    data=(incPos).to_bytes(4, 'little', signed=True)
                                            + (velocity).to_bytes(4, 'little'))

        return (nRtn, )

    def fas_moveToLimit(self, slaveNo, velocity, limitDir):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_MOVETOLIMIT,
                                    data=(velocity).to_bytes(4, 'little') + (limitDir).to_bytes(1, 'little'))

        return (nRtn, )

    def fas_moveVelocity(self, slaveNo, velocity, velDir):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_MOVEVELOCITY,
                                    data=(velocity).to_bytes(4, 'little') + (velDir).to_bytes(1, 'little'))

        return (nRtn, )

    def fas_positionAbsOverride(self, slaveNo, overridePos):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_POSABSOVERRIDE,
                                    data=(overridePos).to_bytes(4, 'little', signed=True))

        return (nRtn, )

    def fas_positionIncOverride(self, slaveNo, overridePos):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_POSINCOVERRIDE,
                                    data=(overridePos).to_bytes(4, 'little', signed=True))

        return (nRtn, )

    def fas_velocityOverride(self, slaveNo, velocity):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_VELOVERRIDE,
                                    data=(velocity).to_bytes(4, 'little'))

        return (nRtn, )

    def fas_triggerPulseOutput(self, slaveNo, startTrigger, startPos, period, pulseTime, outputPin, reserved):#Not tested

        stValue = 0x01 if startTrigger else 0x00

        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_TRIGGER_OUTPUT,
                                    data= (stValue).to_bytes(1, 'little')
                                            + (startPos).to_bytes(4, 'little', signed=True)
                                            + (period).to_bytes(4, 'little')
                                            + (pulseTime).to_bytes(4, 'little')
                                            + (outputPin).to_bytes(1, 'little')
                                            + (reserved).to_bytes(4, 'little'))

        if nRtn == FMM_Error.FMM_OK:
            rtn_cmdStatus = res[3]
            return (nRtn, rtn_cmdStatus)

        return (nRtn, )
        
    def fas_triggerPulseStatus(self, slaveNo):#Not tested
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_TRIGGER_STATUS)

        if nRtn == FMM_Error.FMM_OK:
            rtn_triggerStatus = res[3]

        return (nRtn, rtn_triggerStatus)

    def fas_movePush(self, slaveNo, startSpd, moveSpd, position, accel, decel, pushRate, pushSpd, endPosition):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_MOVEPUSH,
                                    data= (startSpd).to_bytes(4, 'little')
                                            + (moveSpd).to_bytes(4, 'little')
                                            + (position).to_bytes(4, 'little', signed=True)
                                            + (accel).to_bytes(2, 'little')
                                            + (decel).to_bytes(2, 'little')
                                            + (pushRate).to_bytes(2, 'little')
                                            + (pushSpd).to_bytes(4, 'little')
                                            + (endPosition).to_bytes(4, 'little', signed=True)
                                            + (1).to_bytes(2, 'little'))

        return (nRtn, )

    def fas_getPushStatus(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_GETPUSHSTATUS)

        if nRtn == FMM_Error.FMM_OK:
            rtn_pushStatus = res[3]
            return (nRtn, rtn_pushStatus)

        return (nRtn, )
    ###########################################################################

    #######################
    #All-Motion Functions.#
    #######################
    def fas_allMoveStop(self):
        self.fsm.doSendCommandNoRes(SLAVE_ALL_COMMAND,
                                    FastechFrame.FRAME_FAS_ALLMOVESTOP)

    def fas_allEmergencyStop(self):
        self.fsm.doSendCommandNoRes(SLAVE_ALL_COMMAND,
                                    FastechFrame.FRAME_FAS_ALLEMERGENCYSTOP)

    def fas_allMoveOriginSingleAxis(self):
        self.fsm.doSendCommandNoRes(SLAVE_ALL_COMMAND,
                                    FastechFrame.FRAME_FAS_ALLMOVEORIGIN)

    def fas_allMoveSingleAxisAbsPos(self, absPos, velocity):
        self.fsm.doSendCommandNoRes(SLAVE_ALL_COMMAND,
                                    FastechFrame.FRAME_FAS_ALLMOVESINGLEABS,
                                    data=(absPos).to_bytes(4, 'little') + (velocity).to_bytes(4, 'little'))

    def fas_allMoveSingleAxisIncPos(self, incPos, velocity):
        self.fsm.doSendCommandNoRes(SLAVE_ALL_COMMAND,
                                    FastechFrame.FRAME_FAS_ALLMOVESINGLEINC,
                                    data=(incPos).to_bytes(4, 'little') + (velocity).to_bytes(4, 'little'))
    ###########################################################################

    ###########################
    #Position Table Functions.#
    ###########################

    def fas_posTableReadItem(self, slaveNo, itemNo):#Something weird
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_POSTAB_READ_ITEM,
                                    data=(itemNo).to_bytes(2, 'little'))

        rtn_status = res[2]
        rtn_pushStatus = res[3:67]

        return (rtn_status, rtn_pushStatus)

    def fas_posTableWriteItem(self, slaveNo, writeNo, item):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_POSTAB_WRITE_ITEM,
                                    data=(writeNo).to_bytes(2, 'little') + (item).to_bytes(64, 'little'))
        
        return res

    def fas_posTableWriteROM(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_POSTAB_WRITE_ROM)
        
        return res

    def fas_PosTableReadROM(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_POSTAB_READ_ROM)
        
        return res

    def fas_posTableRunItem(self, slaveNo, itemNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_POSTAB_RUN_ITEM,
                                    data= (itemNo).to_bytes(2, 'little'))
        
        return res

    # Frame Type ‘0x65 ~ 0x69’, ‘0x90 ~ 0x92’는 내부 사용 목적으로 할당되어 있습니다.
    def fas_posTableIsData(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_POSTAB_IS_DATA)

        return res

    def fas_posTableIsDataEx(self, slaveNo, sectionNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_POSTAB_IS_DATA_EX,
                                    data= (sectionNo).to_bytes(4, 'little'))

        return res

    def fas_posTableRunOneItem(self, slaveNo, nextMove, itemNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_POSTAB_RUN_ONEITEM,
                                    data= (nextMove).to_bytes(1, 'little') + (itemNo).to_bytes(2, 'little'))

        return res

    def fas_posTableCheckStopMode(self, slaveNo):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_POSTAB_CHECK_STOPMODE)

        return res

    def fas_posTableReadOneItem(self, slaveNo, itemNo, offSet):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_POSTAB_READ_ONEITEM,
                                    data= (itemNo).to_bytes(2, 'little') + (offSet).to_bytes(2, 'little'))

        return res

    def fas_posTableWriteOneItem(self, slaveNo, itemNo, offSet, posItemVal):
        nRtn, res = self.fsm.doSendCommand(slaveNo,
                                    FastechFrame.FRAME_FAS_POSTAB_READ_ONEITEM,
                                    data= (itemNo).to_bytes(2, 'little')
                                            + (offSet).to_bytes(2, 'little')
                                            + (posItemVal).to_bytes(4, 'little'))

        return res

    ###########################################################################

    

