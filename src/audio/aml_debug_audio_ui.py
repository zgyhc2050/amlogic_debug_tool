import os
from threading import Thread

from PyQt5 import QtWidgets
from src.audio.aml_debug_audio import AmlAudioDebug, AudioDebugCfg
from src.audio.aml_ini_parser_audio import AmlParserIniAudio
from src.common.aml_debug_base_ui import AmlDebugBaseUi
from src.common.aml_common_utils import AmlCommonUtils

def instance(aml_ui):
    return AmlDebugAudioDebugUi(aml_ui)

########################################################################################################
# Table: "Audio Debug"
class AmlDebugAudioDebugUi(AmlDebugBaseUi):
    def __init__(self, aml_ui):
        super(AmlDebugAudioDebugUi, self).__init__(aml_ui, AmlCommonUtils.AML_DEBUG_MODULE_AUDIO)
        self.audioDebug = AmlAudioDebug(self.log)
        self.audioDebugcfg = AudioDebugCfg()
        self.__homeCallbackStartFinish = print
        self.__homeCallbackStopFinish = print
        self.__homeStartClick = False
        self.__homeStopClick = False

    def init_display_ui(self):
        mode = self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CAPTRUE_MODE)
        if mode == AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL:
            self.m_mainUi.AmlDebugAudioModeManual_radioButton.setChecked(True)
            self.m_mainUi.AmlDebugAudioCaptureTime_groupBox.setEnabled(False)
        elif mode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            self.m_mainUi.AmlDebugAudioModeAuto_radioButton.setChecked(True)
            self.m_mainUi.AmlDebugAudioCaptureTime_groupBox.setEnabled(True)
        else:
            self.log.e('E init_display_ui: Not supported capture mode:' + str(mode) + ' !!!')
        self.m_mainUi.AmlDebugAudioOptionsDebug_checkBox.setChecked(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_DEBUG_INFO))
        self.m_mainUi.AmlDebugAudioOptionsDump_checkBox.setChecked(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_DUMP_DATA))
        self.m_mainUi.AmlDebugAudioOptionsLogcat_checkBox.setChecked(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_LOGCAT))
        self.m_mainUi.AmlDebugAudioPrintDebugEnable_checkBox.setChecked(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PRINT_DEBUG))
        self.m_mainUi.AmlAudioCaptureTime_spinBox.setValue(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CAPTURE_TIME))
        self.m_mainUi.AmlDebugAudioCreateZipEnable_checkBox.setChecked(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CREATE_ZIP))
        support_channel_array = ['1', '2', '4', '6', '8']
        support_byte_array = ['1', '2', '4']
        support_rate_array = ['8000', '16000', '32000', '44100', '48000', '64000', '88200', '96000', '192000']
        self.m_mainUi.AmlAudioDebugPlayAudioChannel_comboBox.addItems(support_channel_array)
        self.m_mainUi.AmlAudioDebugPlayAudioChannel_comboBox.setCurrentText(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_CHANNEL))
        self.m_mainUi.AmlAudioDebugPlayAudioByte_comboBox.addItems(support_byte_array)
        self.m_mainUi.AmlAudioDebugPlayAudioByte_comboBox.setCurrentText(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_BYTE))
        self.m_mainUi.AmlAudioDebugPlayAudioRate_comboBox.addItems(support_rate_array)
        self.m_mainUi.AmlAudioDebugPlayAudioRate_comboBox.setCurrentText(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_RATE))
        self.__refresh_PlayAudioSelectChannelUi()
        self.m_mainUi.AmlAudioDebugPlayAudioPath_lineEdit.setText(self.m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_PATH))

    def signals_connect_slots(self):
        self.m_mainUi.AmlDebugAudioModeAuto_radioButton.clicked.connect(self.__click_auto_mode)
        self.m_mainUi.AmlDebugAudioModeManual_radioButton.clicked.connect(self.__click_manual_mode)
        self.m_mainUi.AmlDebugAudioStart_pushButton.clicked.connect(self.start_capture)
        self.m_mainUi.AmlDebugAudioStop_pushButton.clicked.connect(self.stop_capture)
        self.m_mainUi.AmlDebugAudioOptionsDebug_checkBox.clicked[bool].connect(self.__click_Debug)
        self.m_mainUi.AmlDebugAudioOptionsDump_checkBox.clicked[bool].connect(self.__click_Dump)
        self.m_mainUi.AmlDebugAudioOptionsLogcat_checkBox.clicked[bool].connect(self.__click_Logcat)
        self.m_mainUi.AmlAudioCaptureTime_spinBox.valueChanged[int].connect(self.__changed_CaptureTime)
        self.m_mainUi.AmlDebugAudioPrintDebugEnable_checkBox.clicked[bool].connect(self.__click_PrintDebugEnable)
        self.m_mainUi.AmlDebugAudioCreateZipEnable_checkBox.clicked[bool].connect(self.__click_CreateZipEnable)
        self.m_mainUi.AmlAudioDebugPlayAudio_Button.clicked.connect(self.__click_play_toggle)
        self.m_mainUi.AmlAudioDebugPlayAudioChannel_comboBox.currentTextChanged.connect(self.__textChanged_PlayAudioChannel)
        self.m_mainUi.AmlAudioDebugPlayAudioByte_comboBox.currentTextChanged.connect(self.__textChanged_PlayAudioByte)
        self.m_mainUi.AmlAudioDebugPlayAudioRate_comboBox.currentTextChanged.connect(self.__textChanged_PlayAudioRate)
        self.m_mainUi.AmlAudioDebugPlayAudioPath_lineEdit.editingFinished.connect(self.__editing_PlayAudioPath)
        self.m_mainUi.AmlAudioDebugPlayAudioOpenFile_Button.clicked.connect(self.__click_playAudioRateFileOpen)
        self.m_mainUi.AmlDebugAudioOpenOutput_pushButton.clicked.connect(self.__click_open_output)

    def __click_auto_mode(self):
        self.m_mainUi.AmlDebugAudioCaptureTime_groupBox.setEnabled(True)
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CAPTRUE_MODE, AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO)

    def __click_manual_mode(self):
        self.m_mainUi.AmlDebugAudioCaptureTime_groupBox.setEnabled(False)
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CAPTRUE_MODE, AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL)

    def start_capture(self, curTimeName='', homeCallbackFinish=print, homeClick=False):
        self.log.i('start_capture')
        self.__homeCallbackStartFinish = homeCallbackFinish
        self.__homeStartClick = homeClick
        self.m_mainUi.AmlDebugAudioMode_groupBox.setEnabled(False)
        self.m_mainUi.AmlDebugAudioOptions_groupBox.setEnabled(False)
        self.m_mainUi.AmlDebugAudioCaptureTime_groupBox.setEnabled(False)
        self.m_mainUi.AmlDebugAudioPrintDebug_groupBox.setEnabled(False)
        self.m_mainUi.AmlDebugAudioCreateZipEnable_checkBox.setEnabled(False)
        self.m_mainUi.AmlDebugAudioStart_pushButton.setEnabled(False)
        self.__pre_audio_debug_config()
        self.audioDebugcfg.m_homeClick = homeClick;
        self.audioDebug.setAudioDebugCfg(self.audioDebugcfg)
        thread = Thread(target = self.__startCaptureInfo, args = (curTimeName,))
        thread.start()

    def stop_capture(self, homeCallbackFinish=print, homeClick=False):
        self.log.i('stop_capture')
        self.__homeCallbackStopFinish = homeCallbackFinish
        self.__homeStopClick = homeClick
        if self.audioDebugcfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            self.log.i('stop_capture: auto mode not need stop.')
            if self.__homeStopClick == True:
                self.__homeCallbackStopFinish(self.m_moduleId)
            return
        self.m_mainUi.AmlDebugAudioStop_pushButton.setEnabled(False)
        thread = Thread(target = self.__stopCaptureInfo)
        thread.start()

    def __click_Debug(self, enable):
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_DEBUG_INFO, enable)
    def __click_Dump(self, enable):
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_DUMP_DATA, enable)
    def __click_Logcat(self, enable):
        if enable:
            self.m_mainUi.AmlDebugHomeOptionsLogcat_checkBox.setChecked(True)
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_LOGCAT, enable)
    def __changed_CaptureTime(self, value):
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CAPTURE_TIME, value)
    def __click_PrintDebugEnable(self, enable):
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PRINT_DEBUG, enable)
    def __click_CreateZipEnable(self, enable):
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CREATE_ZIP, enable)
    def __textChanged_PlayAudioChannel(self, value):
        self.__refresh_PlayAudioSelectChannelUi()
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_CHANNEL, value)
    def __textChanged_PlayAudioByte(self, value):
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_BYTE, value)
    def __textChanged_PlayAudioRate(self, value):
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_RATE, value)
    def __editing_PlayAudioPath(self):
        self.m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_PATH, self.m_mainUi.AmlAudioDebugPlayAudioPath_lineEdit.text())

    def __click_playAudioRateFileOpen(self):
        curPath = self.audioDebug.getCurDebugPath()
        openPath = self.check_output_path(curPath)
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self.m_mainUi, "Open File", openPath, "All Files(*);;Text Files(*.txt)")
        if not fileName == '':
            self.m_mainUi.AmlAudioDebugPlayAudioPath_lineEdit.setText(fileName)
            self.__editing_PlayAudioPath()

    def __click_play_toggle(self):
        channel = int(self.m_mainUi.AmlAudioDebugPlayAudioChannel_comboBox.currentText())
        selChn = self.m_mainUi.AmlAudioDebugPlayAudiSelChannel_comboBox.currentIndex()
        byte = int(self.m_mainUi.AmlAudioDebugPlayAudioByte_comboBox.currentText())
        rate = int(self.m_mainUi.AmlAudioDebugPlayAudioRate_comboBox.currentText())
        fileName = self.m_mainUi.AmlAudioDebugPlayAudioPath_lineEdit.text()
        isPlaying = self.audioDebug.start_play_toggle(fileName, channel, byte, rate, selChn, self.__callback_audioPlayFinish)
        if isPlaying == True:
            self.m_mainUi.AmlAudioDebugPlayAudio_Button.setText('Stop(playing)')
        else:
            self.m_mainUi.AmlAudioDebugPlayAudio_Button.setText('Play')

    def __click_open_output(self):
        curPath = self.audioDebug.getCurDebugPath()
        os.startfile(self.check_output_path(curPath))

    def get_logcat_enable(self):
        return self.m_mainUi.AmlDebugAudioOptionsLogcat_checkBox.isChecked()

    def open_logcat(self):
        self.__pre_audio_debug_config()
        self.audioDebugcfg.m_homeClick = True;
        self.audioDebug.setAudioDebugCfg(self.audioDebugcfg)
        self.audioDebug.open_logcat()

    def close_logcat(self):
        self.audioDebug.close_logcat()

    def __startCaptureInfo(self, curTimeName):
        if self.__homeStartClick == False:
            AmlCommonUtils.adb_root()
            AmlCommonUtils.adb_remount()
        self.audioDebug.start_capture(curTimeName, self.__callback_startCaptureFinish)

    def __callback_startCaptureFinish(self):       
        if self.audioDebugcfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            self.m_mainUi.AmlDebugAudioMode_groupBox.setEnabled(True)
            self.m_mainUi.AmlDebugAudioOptions_groupBox.setEnabled(True)
            self.m_mainUi.AmlDebugAudioCaptureTime_groupBox.setEnabled(True)
            self.m_mainUi.AmlDebugAudioPrintDebug_groupBox.setEnabled(True)
            self.m_mainUi.AmlDebugAudioCreateZipEnable_checkBox.setEnabled(True)
            self.m_mainUi.AmlDebugAudioStart_pushButton.setEnabled(True)
            self.log.i('------ Auto mode capture Finish !!! ------')
        elif self.audioDebugcfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL:
            self.m_mainUi.AmlDebugAudioStop_pushButton.setEnabled(True)
            self.log.i('Manual mode Start capture finish')
        if self.__homeStartClick == True:
            self.__homeCallbackStartFinish(self.m_moduleId)

    def __stopCaptureInfo(self):
        self.audioDebug.stop_capture(self.__callback_stopCaptureFinish)
        if self.__homeStopClick == True:
            self.__homeCallbackStopFinish(self.m_moduleId)

    def __callback_stopCaptureFinish(self):
        self.log.i('------ Manual mode capture Finish !!! ------')
        self.m_mainUi.AmlDebugAudioMode_groupBox.setEnabled(True)
        self.m_mainUi.AmlDebugAudioOptions_groupBox.setEnabled(True)
        self.m_mainUi.AmlDebugAudioPrintDebug_groupBox.setEnabled(True)
        self.m_mainUi.AmlDebugAudioCreateZipEnable_checkBox.setEnabled(True)
        self.m_mainUi.AmlDebugAudioStart_pushButton.setEnabled(True)

    def closeEvent(self):
        pass

    def __pre_audio_debug_config(self):
        if self.m_mainUi.AmlDebugAudioModeAuto_radioButton.isChecked() == True:
            self.audioDebugcfg.m_captureMode = AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO
        elif self.m_mainUi.AmlDebugAudioModeManual_radioButton.isChecked() == True:
            self.audioDebugcfg.m_captureMode = AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL
        else:
            self.log.w('__pre_audio_debug_config: Not supported capture mode!!!')
        self.audioDebugcfg.m_debugInfoEnable = self.m_mainUi.AmlDebugAudioOptionsDebug_checkBox.isChecked()
        self.audioDebugcfg.m_dumpDataEnable = self.m_mainUi.AmlDebugAudioOptionsDump_checkBox.isChecked()
        self.audioDebugcfg.m_logcatEnable = self.m_mainUi.AmlDebugAudioOptionsLogcat_checkBox.isChecked()
        self.audioDebugcfg.m_autoDebugTimeS = self.m_mainUi.AmlAudioCaptureTime_spinBox.value()
        self.audioDebugcfg.m_printDebugEnable = self.m_mainUi.AmlDebugAudioPrintDebugEnable_checkBox.isChecked()
        self.audioDebugcfg.m_createZipFile = self.m_mainUi.AmlDebugAudioCreateZipEnable_checkBox.isChecked()

    def __callback_audioPlayFinish(self):
        self.m_mainUi.AmlAudioDebugPlayAudio_Button.setText('Play')

    def __refresh_PlayAudioSelectChannelUi(self):
        support_sel_ch_array = ['1_2', '3_4', '5_6', '7_8']
        self.m_mainUi.AmlAudioDebugPlayAudiSelChannel_comboBox.clear()
        channels = int(self.m_mainUi.AmlAudioDebugPlayAudioChannel_comboBox.currentText())
        self.m_mainUi.AmlAudioDebugPlayAudiSelChannel_comboBox.addItem(support_sel_ch_array[0])
        if channels >= 4:
            self.m_mainUi.AmlAudioDebugPlayAudiSelChannel_comboBox.addItem(support_sel_ch_array[1])
        if channels >= 6:
            self.m_mainUi.AmlAudioDebugPlayAudiSelChannel_comboBox.addItem(support_sel_ch_array[2])
        if channels == 8:
            self.m_mainUi.AmlAudioDebugPlayAudiSelChannel_comboBox.addItem(support_sel_ch_array[3])

