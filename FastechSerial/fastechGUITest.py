import sys
import time
from threading import Thread

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *

from fastechComm.fastechEziServoPlusRmini import FastechEziServoPlusRmini
from fastechComm.fastechCommError import FMM_Error
from fastechComm.fastechStatusFlag import FastechStatusFlagBit
from fastechComm.fastechParameter import FastechParameterNum as fpn
from fastechComm.fastechCommError import FMM_Error

#Get motion status thread#############################
class StatusThread(QtCore.QThread):
    threadEvent = QtCore.pyqtSignal(tuple)

    def __init__(self,fsmi,parent=None):
        super().__init__()
        self.fsmi = fsmi
        self.isRun = False


    def run(self):
        while self.isRun:
            res = self.fsmi.fas_getMotionStatus(0)
            #res = (0, 1, 1, 1, 1)
            time.sleep(0.2)

            self.threadEvent.emit(res)
#######################################################

class FastechGUI(QWidget):
    def __init__(self, comPort):
        super().__init__()
        self.fsmi = FastechEziServoPlusRmini(comPort, 20)
        self.dic_paramText = {}
        
        self.initUI()

        #Get all Parameter & Set text all
        self.setTextAllParameter()
        
        #Connect Event QlineEditer
        for i in self.dic_paramText:
            self.dic_paramText[i].textChanged.connect(self.setParameter(i))

        # self.searchSpd_lineEdit.textChanged.connect(self.setParameter(18))
        # self.orgSpd_lineEdit.textChanged.connect(self.setParameter(17))
        # self.orgAD_lineEdit.textChanged.connect(self.setParameter(19))

        self.ms_qthread = StatusThread(self.fsmi, self)
        self.ms_qthread.threadEvent.connect(self.setTextStatus)
        self.ms_qthread.isRun = True
        self.ms_qthread.start()
        
    def closeEvent(self, event):
        self.ms_qthread.isRun = False
    
    def initUI(self):
        self.setWindowTitle('Fastech GUI')
        self.move(300, 300)
        self.setFixedSize(450, 300)
        
        #Buttons
        on_btn = QPushButton("Servo ON", self)
        on_btn.move(25, 225)
        on_btn.resize(80, 50)
        on_btn.clicked.connect(self.servoON)

        off_btn = QPushButton("Servo OFF", self)
        off_btn.move(115, 225)
        off_btn.resize(80, 50)
        off_btn.clicked.connect(self.servoOFF)

        stop_btn = QPushButton("Stop", self)
        stop_btn.move(255, 225)
        stop_btn.resize(80, 50)
        stop_btn.clicked.connect(self.moveStop)

        em_btn = QPushButton("Emer Stop", self)
        em_btn.move(345, 225)
        em_btn.resize(80, 50)
        em_btn.clicked.connect(self.emergencyStop)
        ################################################
        
        #Motion status##################################
        gb_motionStatus = QGroupBox("Motion status", self)
        gb_motionStatus.move(10, 10)
        gb_motionStatus.resize(150, 200)

        
        self.cmdPos_lineEdit = QLineEdit("", self)
        cmdPos_label = QLabel(self.tr("Cmd Pos:"))
        cmdPos_label.setBuddy(self.cmdPos_lineEdit)
        self.cmdPos_lineEdit.setReadOnly(True)

        self.actPos_lineEdit = QLineEdit("", self)
        actPos_label = QLabel(self.tr("Act Pos:"))
        actPos_label.setBuddy(self.actPos_lineEdit)
        self.actPos_lineEdit.setReadOnly(True)

        self.actVel_lineEdit = QLineEdit("", self)
        actVel_label = QLabel(self.tr("Act Vel:"))
        actVel_label.setBuddy(self.actVel_lineEdit)
        self.actVel_lineEdit.setReadOnly(True)
        
        self.posErr_lineEdit = QLineEdit("", self)
        posErr_label = QLabel(self.tr("Pos Err:"))
        posErr_label.setBuddy(self.posErr_lineEdit)
        self.posErr_lineEdit.setReadOnly(True)

        cp_btn = QPushButton("Clear Position", self)
        cp_btn.clicked.connect(self.clearPositionEvent)

        
        ms_gl = QGridLayout()
        ms_gl.addWidget(cmdPos_label, 0, 0)
        ms_gl.addWidget(self.cmdPos_lineEdit, 0, 1)
        ms_gl.addWidget(actPos_label, 1, 0)
        ms_gl.addWidget(self.actPos_lineEdit, 1, 1)
        ms_gl.addWidget(actVel_label, 2, 0)
        ms_gl.addWidget(self.actVel_lineEdit, 2, 1)
        ms_gl.addWidget(posErr_label, 3, 0)
        ms_gl.addWidget(self.posErr_lineEdit, 3, 1)
        ms_gl.addWidget(cp_btn, 4, 0, 1, 2)
        gb_motionStatus.setLayout(ms_gl)
        ###################################################


        #Home Tab##########################################
        home_tab = QWidget()

        self.searchSpd_lineEdit = QLineEdit("", self)
        searchSpd_label = QLabel(self.tr("Search Spd:"))
        searchSpd_label.setBuddy(self.searchSpd_lineEdit)
        self.searchSpd_lineEdit.setValidator(QtGui.QIntValidator(1,500000,self))#Set Range
        self.dic_paramText[fpn.ORG_SEARCH_SPEED] = self.searchSpd_lineEdit

        self.orgSpd_lineEdit = QLineEdit("", self)
        orgSpd_label = QLabel(self.tr("Org Spd:"))
        orgSpd_label.setBuddy(self.orgSpd_lineEdit)
        self.orgSpd_lineEdit.setValidator(QtGui.QIntValidator(1,500000,self))
        self.dic_paramText[fpn.ORG_SPEED] = self.orgSpd_lineEdit

        self.orgAD_lineEdit = QLineEdit("", self)
        orgAD_label = QLabel(self.tr("Acc/Dec:"))
        orgAD_label.setBuddy(self.orgAD_lineEdit)
        self.orgAD_lineEdit.setValidator(QtGui.QIntValidator(1,9999,self))
        self.dic_paramText[fpn.ORG_ACC_DEC_TIME] = self.orgAD_lineEdit

        mo_btn = QPushButton("Move to Origin", self)
        mo_btn.clicked.connect(self.moveToOrigin)

        ht_gl = QGridLayout()
        ht_gl.addWidget(searchSpd_label, 0, 0)
        ht_gl.addWidget(self.searchSpd_lineEdit, 0, 1)
        ht_gl.addWidget(orgSpd_label, 1, 0)
        ht_gl.addWidget(self.orgSpd_lineEdit, 1, 1)
        ht_gl.addWidget(orgAD_label, 2, 0)
        ht_gl.addWidget(self.orgAD_lineEdit, 2, 1)
        ht_gl.addWidget(mo_btn, 3, 0, 1, 2)
        home_tab.setLayout(ht_gl)
        ###################################################


        #Move Tab##########################################
        move_tab = QWidget()

        self.mCmdPos_lineEdit = QLineEdit("1000", self)
        mCmdPos_label = QLabel(self.tr("Cmd Pos:"))
        self.mCmdPos_lineEdit.setValidator(QtGui.QIntValidator(-134217727,134217727,self))
        mCmdPos_label.setBuddy(self.mCmdPos_lineEdit)

        self.mStartSpd_lineEdit = QLineEdit("", self)
        mStartSpd_label = QLabel(self.tr("Start Spd:"))
        mStartSpd_label.setBuddy(self.mStartSpd_lineEdit)
        self.mStartSpd_lineEdit.setValidator(QtGui.QIntValidator(1,35000,self))
        self.dic_paramText[fpn.AXIS_START_SPEED] = self.mStartSpd_lineEdit

        self.mMoveSpd_lineEdit = QLineEdit("1000", self)
        mMoveSpd_label = QLabel(self.tr("Move Spd:"))
        self.mMoveSpd_lineEdit.setValidator(QtGui.QIntValidator(0,500000,self))
        mMoveSpd_label.setBuddy(self.mMoveSpd_lineEdit)

        self.mAccTime_lineEdit = QLineEdit("", self)
        mAccTime_label = QLabel(self.tr("Acc Time:"))
        mAccTime_label.setBuddy(self.mStartSpd_lineEdit)
        self.mAccTime_lineEdit.setValidator(QtGui.QIntValidator(1,9999,self))
        self.dic_paramText[fpn.AXIS_ACC_TIME] = self.mAccTime_lineEdit

        self.mDecTime_lineEdit = QLineEdit("", self)
        mDecTime_label = QLabel(self.tr("Dec Time:"))
        mDecTime_label.setBuddy(self.mStartSpd_lineEdit)
        self.mDecTime_lineEdit.setValidator(QtGui.QIntValidator(1,9999,self))
        self.dic_paramText[fpn.AXIS_DEC_TIME] = self.mDecTime_lineEdit

        mAbs_btn = QPushButton("ABS Move", self)
        mAbs_btn.clicked.connect(self.moveAbs)
        
        mInc_btn = QPushButton("INC Move", self)
        mInc_btn.clicked.connect(self.moveInc)


        mt_gl = QGridLayout()
        mt_gl.addWidget(mCmdPos_label, 0, 0)
        mt_gl.addWidget(self.mCmdPos_lineEdit, 0, 1)
        mt_gl.addWidget(mStartSpd_label, 1, 0)
        mt_gl.addWidget(self.mStartSpd_lineEdit, 1, 1)
        mt_gl.addWidget(mMoveSpd_label, 2, 0)
        mt_gl.addWidget(self.mMoveSpd_lineEdit, 2, 1)
        mt_gl.addWidget(mAccTime_label, 3, 0)
        mt_gl.addWidget(self.mAccTime_lineEdit, 3, 1)
        mt_gl.addWidget(mDecTime_label, 4, 0)
        mt_gl.addWidget(self.mDecTime_lineEdit, 4, 1)
        mt_gl.addWidget(mAbs_btn, 5, 0)
        mt_gl.addWidget(mInc_btn, 5, 1)
        move_tab.setLayout(mt_gl)
        ###################################################

        #Jog Tab###########################################
        jog_tab = QWidget()

        self.jMaxSpd_lineEdit = QLineEdit("", self)
        jMaxSpd_label = QLabel(self.tr("Max Spd:"))
        jMaxSpd_label.setBuddy(self.jMaxSpd_lineEdit)
        self.jMaxSpd_lineEdit.setValidator(QtGui.QIntValidator(1,500000,self))
        self.dic_paramText[fpn.JOG_SPEED] = self.jMaxSpd_lineEdit

        self.jAD_lineEdit = QLineEdit("", self)
        jAD_label = QLabel(self.tr("Acc/Dec:"))
        jAD_label.setBuddy(self.jAD_lineEdit)
        self.jAD_lineEdit.setValidator(QtGui.QIntValidator(1,9999,self))
        self.dic_paramText[fpn.JOG_ACC_DEC_TIME] = self.jAD_lineEdit

        jog0_btn = QPushButton("-Jog", self)
        jog0_btn.pressed.connect(self.moveJog0)
        jog0_btn.released.connect(self.moveStop)

        jog1_btn = QPushButton("+Jog", self)
        jog1_btn.pressed.connect(self.moveJog1)
        jog1_btn.released.connect(self.moveStop)

        jt_gl = QGridLayout()
        jt_gl.addWidget(jMaxSpd_label, 0, 0)
        jt_gl.addWidget(self.jMaxSpd_lineEdit, 0, 1)
        jt_gl.addWidget(jAD_label, 1, 0)
        jt_gl.addWidget(self.jAD_lineEdit, 1, 1)
        jt_gl.addWidget(jog0_btn, 5, 0)
        jt_gl.addWidget(jog1_btn, 5, 1)
        jog_tab.setLayout(jt_gl)
        ###################################################

        #Tab Widget
        tabs = QTabWidget(self)
        tabs.addTab(home_tab, "Home")
        tabs.addTab(move_tab, "Move")
        tabs.addTab(jog_tab, "Jog")
        tabs.move(210, 10)
        tabs.resize(230, 200)
        ###################################################
        

        self.show()

    def setTextStatus(self, res):
        if res[0] == FMM_Error.FMM_OK:
            self.cmdPos_lineEdit.setText(f"{res[1]}")
            self.actPos_lineEdit.setText(f"{res[2]}")
            self.actVel_lineEdit.setText(f"{res[4]}")
            self.posErr_lineEdit.setText(f"{res[3]}")

    def setTextParameter(self, paramNo):
        res = self.fsmi.fas_getParameter(0, paramNo)
        if res[0] == FMM_Error.FMM_OK:
            self.dic_paramText[paramNo].setText(f"{res[1]}")
        else:
            self.StatusMessage(res[0])

    def setTextAllParameter(self):
        for i in self.dic_paramText:
            self.setTextParameter(i)

    def setParameter(self, paramNo):
        def setParam():
            paramValue = self.dic_paramText[paramNo].text()
            if paramValue != "":
                res = self.fsmi.fas_setParameter(0, paramNo, int(paramValue))
                if res[0] == FMM_Error.FMM_OK:
                    self.setTextParameter(paramNo)
                else:
                    #FailEvent
                    self.StatusMessage(res[0])

        return setParam

    def moveAbs(self):
        cmdPos = self.mCmdPos_lineEdit.text()
        moveSpd = self.mMoveSpd_lineEdit.text()
        if cmdPos != "" or moveSpd != "":
            res = self.fsmi.fas_moveSingleAxisAbsPos(0, int(cmdPos), int(moveSpd))
            if res[0] == FMM_Error.FMM_OK:
                #Success Event
                self.StatusMessage(res[0])
            else:
                #Fail Event
                self.StatusMessage(res[0])

    def moveInc(self):
        cmdPos = self.mCmdPos_lineEdit.text()
        moveSpd = self.mMoveSpd_lineEdit.text()
        if cmdPos != "" or moveSpd != "":
            res = self.fsmi.fas_moveSingleAxisIncPos(0, int(cmdPos), int(moveSpd))
            if res[0] == FMM_Error.FMM_OK:
                #Success Event
                self.StatusMessage(res[0])
            else:
                #Fail Event
                self.StatusMessage(res[0])

    def moveJog0(self):
        spd = self.jMaxSpd_lineEdit.text()
        if spd != "":
            res = self.fsmi.fas_moveVelocity(0, int(spd), 0)
            if res[0] == FMM_Error.FMM_OK:
                print("OK")

    def moveJog1(self):
        spd = self.jMaxSpd_lineEdit.text()
        if spd != "":
            res = self.fsmi.fas_moveVelocity(0, int(spd), 1)
            if res[0] == FMM_Error.FMM_OK:
                print("OK")

    def moveStop(self):
        res = self.fsmi.fas_moveStop(0)
        if res[0] == FMM_Error.FMM_OK:
                #Success Event
                self.StatusMessage(res[0])
        else:
            #Fail Event
            self.StatusMessage(res[0])

    def emergencyStop(self):
        res = self.fsmi.fas_emergencyStop(0)
        if res[0] == FMM_Error.FMM_OK:
                #Success Event
                self.StatusMessage(res[0])
        else:
            #Fail Event
            self.StatusMessage(res[0])


    def clearPositionEvent(self):
        res = self.fsmi.fas_clearPosition(0)
        if res[0] == FMM_Error.FMM_OK:
                #Success Event
                self.StatusMessage(res[0])
        else:
            #Fail Event
            self.StatusMessage(res[0])

    def moveToOrigin(self):
        res = self.fsmi.fas_moveOriginSingleAxis(0)
        
        if res[0] == FMM_Error.FMM_OK:
            #Success Event
            self.StatusMessage(res[0])
        else:
            #Fail Event
            self.StatusMessage(res[0])

    def isServoOn(self):
        res = self.fsmi.fas_getAxisStatus(0)
        servoON = 0

        if res[0] == FMM_Error.FMM_OK:
            servoON = (res[1] & FastechStatusFlagBit.FFLAG_SERVOON) >> 20
        
        return servoON

    def servoON(self):
        if not self.isServoOn():
            res = self.fsmi.fas_servoEnable(0, 1)
            if res[0] == FMM_Error.FMM_OK:
                #Success Event
                self.StatusMessage(res[0])
            else:
                #Fail Event
                self.StatusMessage(res[0])

    def servoOFF(self):
        if self.isServoOn():
            res = self.fsmi.fas_servoEnable(0, 0)
            if res[0] == FMM_Error.FMM_OK:
                #Success Event
                self.StatusMessage(res[0])
            else:
                #Fail Event
                self.StatusMessage(res[0])

    def StatusMessage(self, res_code):
        msg = QMessageBox()
        msg.setWindowTitle("STATUS WARNING")
        msg.setIcon(QMessageBox.Warning)

        text = ""

        if res_code == FMM_Error.FMM_OK:
            msg.setIcon(QMessageBox.Information)
            text = "FMM_OK"
        elif res_code == FMM_Error.FMM_NOT_OPEN:
            text = "FMM_NOT_OPEN"
        elif res_code == FMM_Error.FMM_INVALID_PORT_NUM:
            text = "FMM_INVALID_PORT_NUM"
        elif res_code == FMM_Error.FMM_INVALID_SLAVE_NUM:
            text = "FMM_INVALID_SLAVE_NUM"
        elif res_code == FMM_Error.FMC_DISCONNECTED:
            text = "FMC_DISCONNECTED"
        elif res_code == FMM_Error.FMC_TIMEOUT_ERROR:
            text = "FMC_TIMEOUT_ERROR"
        elif res_code == FMM_Error.FMC_CRCFAILED_ERROR:
            text = "FMC_CRCFAILED_ERROR"
        elif res_code == FMM_Error.FMC_RECVPACKET_ERROR:
            text = "FMC_RECVPACKET_ERROR"
        elif res_code == FMM_Error.FMM_POSTABLE_ERROR:
            text = "FMM_POSTABLE_ERROR"
        elif res_code == FMM_Error.FMP_FRAMETYPEERROR:
            text = "FMP_FRAMETYPEERROR"
        elif res_code == FMM_Error.FMP_DATAERROR:
            text = "FMP_DATAERROR"
        elif res_code == FMM_Error.FMP_PACKETERROR:
            text = "FMP_PACKETERROR"
        elif res_code == FMM_Error.FMP_RUNFAIL:
            text = "FMP_RUNFAIL"
        elif res_code == FMM_Error.FMP_RESETFAIL:
            text = "FMP_RESETFAIL"
        elif res_code == FMM_Error.FMP_SERVOONFAIL1:
            text = "FMP_SERVOONFAIL1"
        elif res_code == FMM_Error.FMP_SERVOONFAIL2:
            text = "FMP_SERVOONFAIL2"
        elif res_code == FMM_Error.FMP_SERVOONFAIL3:
            text = "FMP_SERVOONFAIL3"
        elif res_code == FMM_Error.FMP_PACKETCRCERROR:
            text = "FMP_PACKETCRCERROR"
        elif res_code == FMM_Error.FMM_SENDPACKET_ERROR:
            text = "FMM_SENDPACKET_ERROR"
        elif res_code == FMM_Error.FMM_UNKNOWN_ERROR:
            text = "FMM_UNKNOWN_ERROR"

        msg.setInformativeText(text)
        msg.exec_()
        


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FastechGUI(sys.argv[1])
    sys.exit(app.exec_())