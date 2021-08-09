from pathlib import Path
import os
import sys
from threading import Thread

from PyQt5.QtGui import QTextCursor, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

import resource
import Ui_aml_debug
import aml_debug_audio
import aml_common

class AmlDebugUi(Ui_aml_debug.Ui_MainWindow):
    def __init__(self, Dialog):
        super().setupUi(Dialog)
        self.__m_amlDebugAudioDebugUi = AmlDebugAudioDebugUi(self)
        self.__m_amlDebugSystemOperationUi = AmlDebugSystemOperationUi(self)

    def terminalLog(self, someInfo):
        self.AmlAudioTerminalLog_textBrowser.append(someInfo)
        self.AmlAudioTerminalLog_textBrowser.moveCursor(QTextCursor.End)

    def remount(self):
        aml_common.exe_adb_cmd('adb root', True, self.terminalLog)
        return aml_common.exe_adb_cmd('adb remount', True, self.terminalLog)

    def reboot(self):
        aml_common.exe_adb_cmd('adb reboot', True, self.terminalLog)

########################################################################################################
# Table 1: "Audio Debug"
class AmlDebugAudioDebugUi():
    def __init__(self, aml_ui):
        self.__m_amlUi = aml_ui
        self.audioDebug = aml_debug_audio.AmlAudioDebug()
        self.audioDebugcfg = aml_debug_audio.AudioDebugCfg()

        self.__m_amlUi.AmlAudioDebugModeAuto_radioButton.clicked.connect(self.__click_auto_mode)
        self.__m_amlUi.AmlAudioDebugModeManual_radioButton.clicked.connect(self.__click_manual_mode)
        self.__m_amlUi.AmlAudioDebugStart_pushButton.clicked.connect(self.__click_start_capture)
        self.__m_amlUi.AmlAudioDebugStop_pushButton.clicked.connect(self.__click_stop_capture)
        self.__init_audio_debug_default_config()
        if self.audioDebugcfg.m_captureMode == aml_debug_audio.DEBUG_CAPTURE_MODE_AUTO:
            self.__m_amlUi.AmlAudioDebugModeAuto_radioButton.setChecked(True)
        elif self.audioDebugcfg.m_captureMode == aml_debug_audio.DEBUG_CAPTURE_MODE_MUNUAL:
            self.__m_amlUi.AmlAudioDebugModeManual_radioButton.setChecked(True)
        else:
            self.__m_amlUi.terminalLog('E refresh_capture_mode_ui: Not supported capture mode!!!')
        self.__m_amlUi.AmlAudioDebugOptionsDebug_checkBox.setChecked(self.audioDebugcfg.m_debugInfoEnable)
        self.__m_amlUi.AmlAudioDebugOptionsDump_checkBox.setChecked(self.audioDebugcfg.m_dumpDataEnable)
        self.__m_amlUi.AmlAudioDebugOptionsLogcat_checkBox.setChecked(self.audioDebugcfg.m_logcatEnable)
        self.__m_amlUi.AmlAudioPrintDebugEnable_checkBox.setChecked(self.audioDebugcfg.m_printDebugEnable)
        self.__m_amlUi.AmlAudioCaptureTime_spinBox.setValue(self.audioDebugcfg.m_autoDebugTimeS)
        self.__m_amlUi.AmlAudioCreateZipEnable_checkBox.setChecked(self.audioDebugcfg.m_createZipFile)

    def __init_audio_debug_default_config(self):
        self.audioDebugcfg.m_captureMode = aml_debug_audio.DEFAULT_CAPTURE_MODE
        self.audioDebugcfg.m_debugInfoEnable = True
        self.audioDebugcfg.m_dumpDataEnable = True
        self.audioDebugcfg.m_logcatEnable = True
        self.audioDebugcfg.m_printDebugEnable = False
        self.audioDebugcfg.m_autoDebugTimeS = aml_debug_audio.DEFAULT_AUTO_MODE_DUMP_TIME_S
        self.audioDebugcfg.m_createZipFile = False

    def __click_auto_mode(self):
        self.__m_amlUi.AmlAudioDebugCaptureTime_groupBox.setEnabled(True)

    def __click_manual_mode(self):
        self.__m_amlUi.AmlAudioDebugCaptureTime_groupBox.setEnabled(False)

    def __click_start_capture(self):
        self.__m_amlUi.AmlAudioDebugMode_groupBox.setEnabled(False)
        self.__m_amlUi.AmlAudioDebugOptions_groupBox.setEnabled(False)
        self.__m_amlUi.AmlAudioDebugCaptureTime_groupBox.setEnabled(False)
        self.__m_amlUi.AmlAudioDebugPrintDebug_groupBox.setEnabled(False)
        self.__m_amlUi.AmlAudioCreateZipEnable_checkBox.setEnabled(False)
        self.__m_amlUi.AmlAudioDebugStart_pushButton.setEnabled(False)
  
        self.__pre_audio_debug_config()
        self.__m_amlUi.terminalLog('')
        self.audioDebug.setAudioDebugCfg(self.audioDebugcfg)
        self.audioDebug.setShowStatusCallback(self.__m_amlUi.terminalLog)
        thr = Thread(target = self.__startCaptureInfo)
        thr.start()

    def __click_stop_capture(self):
        self.__m_amlUi.AmlAudioDebugStop_pushButton.setEnabled(False)
        thr = Thread(target = self.__stopCaptureInfo)
        thr.start()

    def __pre_audio_debug_config(self):
        if self.__m_amlUi.AmlAudioDebugModeAuto_radioButton.isChecked() == True:
            self.audioDebugcfg.m_captureMode = aml_debug_audio.DEBUG_CAPTURE_MODE_AUTO
        elif self.__m_amlUi.AmlAudioDebugModeManual_radioButton.isChecked() == True:
            self.audioDebugcfg.m_captureMode = aml_debug_audio.DEBUG_CAPTURE_MODE_MUNUAL
        else:
            self.__m_amlUi.terminalLog('E __pre_audio_debug_config: Not supported capture mode!!!')
        self.audioDebugcfg.m_debugInfoEnable = self.__m_amlUi.AmlAudioDebugOptionsDebug_checkBox.isChecked()
        self.audioDebugcfg.m_dumpDataEnable = self.__m_amlUi.AmlAudioDebugOptionsDump_checkBox.isChecked()
        self.audioDebugcfg.m_logcatEnable = self.__m_amlUi.AmlAudioDebugOptionsLogcat_checkBox.isChecked()
        self.audioDebugcfg.m_printDebugEnable = self.__m_amlUi.AmlAudioPrintDebugEnable_checkBox.isChecked()
        self.audioDebugcfg.m_autoDebugTimeS = self.__m_amlUi.AmlAudioCaptureTime_spinBox.value()
        self.audioDebugcfg.m_createZipFile = self.__m_amlUi.AmlAudioCreateZipEnable_checkBox.isChecked()
        if self.audioDebugcfg.m_printDebugEnable:
            self.__m_amlUi.terminalLog('m_captureMode:' + str(self.audioDebugcfg.m_captureMode))
            self.__m_amlUi.terminalLog('m_debugInfoEnable:' + str(self.audioDebugcfg.m_debugInfoEnable))
            self.__m_amlUi.terminalLog('m_dumpDataEnable:' + str(self.audioDebugcfg.m_dumpDataEnable))
            self.__m_amlUi.terminalLog('m_logcatEnable:' + str(self.audioDebugcfg.m_logcatEnable))
            self.__m_amlUi.terminalLog('m_printDebugEnable:' + str(self.audioDebugcfg.m_printDebugEnable))
            self.__m_amlUi.terminalLog('m_autoDebugTimeS:' + str(self.audioDebugcfg.m_autoDebugTimeS))
            self.__m_amlUi.terminalLog('m_createZipFile:' + str(self.audioDebugcfg.m_createZipFile))

    def __callback_startCaptureFinish(self):       
        if self.audioDebugcfg.m_captureMode == aml_debug_audio.DEBUG_CAPTURE_MODE_AUTO:
            self.__m_amlUi.AmlAudioDebugMode_groupBox.setEnabled(True)
            self.__m_amlUi.AmlAudioDebugOptions_groupBox.setEnabled(True)
            self.__m_amlUi.AmlAudioDebugCaptureTime_groupBox.setEnabled(True)
            self.__m_amlUi.AmlAudioDebugPrintDebug_groupBox.setEnabled(True)
            self.__m_amlUi.AmlAudioCreateZipEnable_checkBox.setEnabled(True)
            self.__m_amlUi.AmlAudioDebugStart_pushButton.setEnabled(True)
            self.__m_amlUi.terminalLog('######## Auto mode capture Finish !!! ############')
        elif self.audioDebugcfg.m_captureMode == aml_debug_audio.DEBUG_CAPTURE_MODE_MUNUAL:
            self.__m_amlUi.AmlAudioDebugStop_pushButton.setEnabled(True)
            self.__m_amlUi.terminalLog('Manual mode Start capture finish')

    def __startCaptureInfo(self):
        self.__m_amlUi.remount()
        self.audioDebug.start_capture(self.__callback_startCaptureFinish)

    def __callback_stopCaptureFinish(self):
        self.__m_amlUi.terminalLog('######## Manual mode capture Finish !!! ############')
        self.__m_amlUi.AmlAudioDebugMode_groupBox.setEnabled(True)
        self.__m_amlUi.AmlAudioDebugOptions_groupBox.setEnabled(True)
        self.__m_amlUi.AmlAudioDebugPrintDebug_groupBox.setEnabled(True)
        self.__m_amlUi.AmlAudioCreateZipEnable_checkBox.setEnabled(True)
        self.__m_amlUi.AmlAudioDebugStart_pushButton.setEnabled(True)

    def __stopCaptureInfo(self):
        self.audioDebug.stop_capture(self.__callback_stopCaptureFinish)

########################################################################################################
# Table 2: "System Operation"
class AmlDebugSystemOperationUi():
    def __init__(self, aml_ui):
        self.__m_amlUi = aml_ui

        self.__m_amlUi.AmlSystemPushDolbyDtsPush_pushButton.clicked.connect(self.__pushDstDolby)
        self.__m_amlUi.AmlSystemPushMs12Push_pushButton.clicked.connect(self.__pushMs12)
        self.__m_amlUi.AmlSystemPushCustomPush_pushButton.clicked.connect(self.__pushCustom)
        self.__m_amlUi.AmlSystemPushAllPush_pushButton.clicked.connect(self.__pushAll)
        self.__m_amlUi.AmlSystemRemount_pushButton.clicked.connect(self.__m_amlUi.remount)
        self.__m_amlUi.AmlSystemReboot_pushButton.clicked.connect(self.__m_amlUi.reboot)
        self.__m_amlUi.AmlSystemPullCustom1Pull__pushButton.clicked.connect(self.____pullCustom1)
        self.__m_amlUi.AmlSystemPullCustom2Pull2__pushButton.clicked.connect(self.__pullCustom2)

        self.__m_amlUi.AmlSystemPushDolbySrc_lineEdit.setText('')
        self.__m_amlUi.AmlSystemPushDtsSrc_lineEdit.setText('')
        self.__m_amlUi.AmlSystemPushMs12Src_lineEdit.setText('')
        self.__m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.setText('/odm/lib/')
        self.__m_amlUi.AmlSystemPushMs12Dst_lineEdit.setText('/odm/etc/ms12/')

    def __pushFilesToSoc(self, src, dst):
        aml_common.exe_adb_cmd('adb push "' + src + '" "' + dst + '"', True, self.__m_amlUi.terminalLog)
    def __pullFilesToSoc(self, src, dst):
        aml_common.exe_adb_cmd('adb pull "' + src + '" "' + dst + '"', True, self.__m_amlUi.terminalLog)
        self.__m_amlUi.AmlSystemPushDolbySrc_lineEdit.text()
    
    def __pushDstDolby(self):
        self.__pushFilesToSoc(self.__m_amlUi.AmlSystemPushDolbySrc_lineEdit.text() + '\\libHwAudio_dcvdec.so', self.__m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.text())
        self.__pushFilesToSoc(self.__m_amlUi.AmlSystemPushDtsSrc_lineEdit.text() + '\\libHwAudio_dtshd.so', self.__m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.text())
    def __pushMs12(self):
        self.__pushFilesToSoc(self.__m_amlUi.AmlSystemPushMs12Src_lineEdit.text() + '\\libdolbyms12.so', self.__m_amlUi.AmlSystemPushMs12Dst_lineEdit.text())
    def __pushCustom(self):
        self.__pushFilesToSoc(self.__m_amlUi.AmlSystemPushCustomSrc_lineEdit.text(), self.__m_amlUi.AmlSystemPushCustomDst_lineEdit.text())
    def __pushAll(self):
        self.__pushDstDolby()
        self.__pushMs12()
        self.__pushCustom()
    def ____pullCustom1(self):
        self.__pullFilesToSoc(self.__m_amlUi.AmlSystemPullCustom1Src_lineEdit.text(), self.__m_amlUi.AmlSystemPullCustom1Dst_lineEdit.text())
    def __pullCustom2(self):
        self.__pullFilesToSoc(self.__m_amlUi.AmlSystemPullCustom2Src_lineEdit.text(), self.__m_amlUi.AmlSystemPullCustom2Dst_lineEdit.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    MainWindow.setWindowIcon(QIcon(':/debug.ico'))
    ui = AmlDebugUi(MainWindow)
    MainWindow.setWindowTitle("Amlogic Debug Tool")

    if not Path(aml_common.AML_DEBUG_DIRECOTRY_CONFIG).exists():
        if not Path(aml_common.AML_DEBUG_DIRECOTRY_ROOT).exists():
            ui.terminalLog(aml_common.AML_DEBUG_DIRECOTRY_ROOT + " folder does not exist, create it.")
            os.makedirs(aml_common.AML_DEBUG_DIRECOTRY_ROOT, 777)
        ui.terminalLog('First start, ' + aml_common.AML_DEBUG_DIRECOTRY_CONFIG + " file does not exist, create it.")
        file = open(aml_common.AML_DEBUG_DIRECOTRY_CONFIG, 'w')
        file.close()

    MainWindow.show()
    sys.exit(app.exec_())
