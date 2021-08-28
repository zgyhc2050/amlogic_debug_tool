import os
from threading import Thread
from pathlib import Path

from PyQt5 import QtWidgets
from src.audio.aml_debug_audio import AmlAudioDebug, AudioDebugCfg
from src.audio.aml_ini_parser_audio import AmlParserIniAudio
from src.common.aml_debug_base_ui import AmlDebugBaseUi
from src.common.aml_ini_parser import amlParserIniContainer, AmlParserIniManager
from src.common.aml_common import AmlCommon

def instance(aml_ui):
    return AmlDebugAudioDebugUi(aml_ui)

########################################################################################################
# Table: "Audio Debug"
class AmlDebugAudioDebugUi(AmlDebugBaseUi):
    def __init__(self, aml_ui):
        self.__m_iniPaser = amlParserIniContainer.getParserById(AmlParserIniManager.AML_PARSER_SECTION_AUDIO)
        self.audioDebug = AmlAudioDebug(aml_ui.terminalLogSignal.emit)
        self.audioDebugcfg = AudioDebugCfg()
        super(AmlDebugAudioDebugUi, self).__init__(aml_ui)

    def init_display_ui(self):
        self.__init_default_config()
        if self.audioDebugcfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL:
            self.m_amlUi.AmlAudioDebugModeManual_radioButton.setChecked(True)
            self.m_amlUi.AmlAudioDebugCaptureTime_groupBox.setEnabled(False)
        elif self.audioDebugcfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            self.m_amlUi.AmlAudioDebugModeAuto_radioButton.setChecked(True)
            self.m_amlUi.AmlAudioDebugCaptureTime_groupBox.setEnabled(True)
        else:
            self.log_fuc('E refresh_capture_mode_ui: Not supported capture mode:' + str(self.audioDebugcfg.m_captureMode) + ' !!!')
        self.m_amlUi.AmlAudioDebugOptionsDebug_checkBox.setChecked(self.audioDebugcfg.m_debugInfoEnable)
        self.m_amlUi.AmlAudioDebugOptionsDump_checkBox.setChecked(self.audioDebugcfg.m_dumpDataEnable)
        self.m_amlUi.AmlAudioDebugOptionsLogcat_checkBox.setChecked(self.audioDebugcfg.m_logcatEnable)
        self.m_amlUi.AmlAudioPrintDebugEnable_checkBox.setChecked(self.audioDebugcfg.m_printDebugEnable)
        self.m_amlUi.AmlAudioCaptureTime_spinBox.setValue(self.audioDebugcfg.m_autoDebugTimeS)
        self.m_amlUi.AmlAudioCreateZipEnable_checkBox.setChecked(self.audioDebugcfg.m_createZipFile)
        self.m_amlUi.AmlAudioDebugPlayAudioOpenFile_Button.clicked.connect(self.__click_playAudioRateFileOpen)
        support_channel_array = ['1', '2', '4', '6', '8']
        support_byte_array = ['1', '2', '3', '4']
        support_rate_array = ['8000', '16000', '32000', '44100', '48000', '64000', '88200', '96000', '192000']
        self.m_amlUi.AmlAudioDebugPlayAudioChannel_comboBox.addItems(support_channel_array)
        self.m_amlUi.AmlAudioDebugPlayAudioChannel_comboBox.setCurrentText(self.__m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_CHANNEL))
        self.m_amlUi.AmlAudioDebugPlayAudioByte_comboBox.addItems(support_byte_array)
        self.m_amlUi.AmlAudioDebugPlayAudioByte_comboBox.setCurrentText(self.__m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_BYTE))
        self.m_amlUi.AmlAudioDebugPlayAudioRate_comboBox.addItems(support_rate_array)
        self.m_amlUi.AmlAudioDebugPlayAudioRate_comboBox.setCurrentText(self.__m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_RATE))
        self.m_amlUi.AmlAudioDebugPlayAudioPath_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_PATH))

    def signals_connect_slots(self):
        self.m_amlUi.AmlAudioDebugModeAuto_radioButton.clicked.connect(self.__click_auto_mode)
        self.m_amlUi.AmlAudioDebugModeManual_radioButton.clicked.connect(self.__click_manual_mode)
        self.m_amlUi.AmlAudioDebugStart_pushButton.clicked.connect(self.__click_start_capture)
        self.m_amlUi.AmlAudioDebugStop_pushButton.clicked.connect(self.__click_stop_capture)
        self.m_amlUi.AmlAudioDebugOptionsDebug_checkBox.clicked.connect(self.__click_Debug)
        self.m_amlUi.AmlAudioDebugOptionsDump_checkBox.clicked.connect(self.__click_Dump)
        self.m_amlUi.AmlAudioDebugOptionsLogcat_checkBox.clicked.connect(self.__click_Logcat)
        self.m_amlUi.AmlAudioCaptureTime_spinBox.editingFinished.connect(self.__finished_CaptureTime)
        self.m_amlUi.AmlAudioPrintDebugEnable_checkBox.clicked.connect(self.__click_PrintDebugEnable)
        self.m_amlUi.AmlAudioCreateZipEnable_checkBox.clicked.connect(self.__click_CreateZipEnable)
        self.m_amlUi.AmlAudioDebugPlayAudio_Button.clicked.connect(self.__click_play_toggle)
        self.m_amlUi.AmlAudioDebugPlayAudioChannel_comboBox.currentTextChanged .connect(self.__finished_PlayAudioChannel)
        self.m_amlUi.AmlAudioDebugPlayAudioByte_comboBox.currentTextChanged.connect(self.__finished_PlayAudioByte)
        self.m_amlUi.AmlAudioDebugPlayAudioRate_comboBox.currentTextChanged.connect(self.__finished_PlayAudioRate)
        self.m_amlUi.AmlAudioDebugPlayAudioPath_lineEdit.editingFinished.connect(self.__finished_PlayAudioPath)

    def __init_default_config(self):
        self.audioDebugcfg.m_captureMode = self.__m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CAPTRUE_MODE)
        self.audioDebugcfg.m_debugInfoEnable = self.__m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_DEBUG_INFO)
        self.audioDebugcfg.m_dumpDataEnable = self.__m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_DUMP_DATA)
        self.audioDebugcfg.m_autoDebugTimeS = self.__m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CAPTURE_TIME)
        self.audioDebugcfg.m_logcatEnable = self.__m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_LOGCAT)
        self.audioDebugcfg.m_printDebugEnable = self.__m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PRINT_DEBUG)
        self.audioDebugcfg.m_createZipFile = self.__m_iniPaser.getValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CREATE_ZIP)

    def closeEvent(self):
        pass

    def __click_auto_mode(self):
        self.m_amlUi.AmlAudioDebugCaptureTime_groupBox.setEnabled(True)
        self.__m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CAPTRUE_MODE, AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO)

    def __click_manual_mode(self):
        self.m_amlUi.AmlAudioDebugCaptureTime_groupBox.setEnabled(False)
        self.__m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CAPTRUE_MODE, AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL)

    def __click_start_capture(self):
        self.m_amlUi.AmlAudioDebugMode_groupBox.setEnabled(False)
        self.m_amlUi.AmlAudioDebugOptions_groupBox.setEnabled(False)
        self.m_amlUi.AmlAudioDebugCaptureTime_groupBox.setEnabled(False)
        self.m_amlUi.AmlAudioDebugPrintDebug_groupBox.setEnabled(False)
        self.m_amlUi.AmlAudioCreateZipEnable_checkBox.setEnabled(False)
        self.m_amlUi.AmlAudioDebugStart_pushButton.setEnabled(False)
        self.__pre_audio_debug_config()
        self.audioDebug.setAudioDebugCfg(self.audioDebugcfg)
        thread = Thread(target = self.__startCaptureInfo)
        thread.start()

    def __click_Debug(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_DEBUG_INFO, self.m_amlUi.AmlAudioDebugOptionsDebug_checkBox.isChecked())
    def __click_Dump(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_DUMP_DATA, self.m_amlUi.AmlAudioDebugOptionsDump_checkBox.isChecked())
    def __click_Logcat(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_LOGCAT, self.m_amlUi.AmlAudioDebugOptionsLogcat_checkBox.isChecked())
    def __finished_CaptureTime(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CAPTURE_TIME, self.m_amlUi.AmlAudioCaptureTime_spinBox.value())
    def __click_PrintDebugEnable(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PRINT_DEBUG, self.m_amlUi.AmlAudioPrintDebugEnable_checkBox.isChecked())
    def __click_CreateZipEnable(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_CREATE_ZIP, self.m_amlUi.AmlAudioCreateZipEnable_checkBox.isChecked())
    def __finished_PlayAudioChannel(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_CHANNEL, self.m_amlUi.AmlAudioDebugPlayAudioChannel_comboBox.currentText())
    def __finished_PlayAudioByte(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_BYTE, self.m_amlUi.AmlAudioDebugPlayAudioByte_comboBox.currentText())
    def __finished_PlayAudioRate(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_RATE, self.m_amlUi.AmlAudioDebugPlayAudioRate_comboBox.currentText())
    def __finished_PlayAudioPath(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_PATH, self.m_amlUi.AmlAudioDebugPlayAudioPath_lineEdit.text())

    def __click_stop_capture(self):
        self.m_amlUi.AmlAudioDebugStop_pushButton.setEnabled(False)
        thread = Thread(target = self.__stopCaptureInfo)
        thread.start()

    def __click_playAudioRateFileOpen(self):
        openPath = self.audioDebug.getCurDebugPath()
        if not Path(openPath).exists() or openPath == '':
            print('I [__click_playAudioRateFileOpen]: audio debug path:' + openPath + ' not exist')
            openPath = AmlCommon.AML_DEBUG_DIRECOTRY_ROOT
        else:
            print('I [__click_playAudioRateFileOpen]: audio debug path:' + openPath + ' exist')
        if not Path(openPath).exists() or openPath == '':
            print('I [__click_playAudioRateFileOpen]: root path:' + openPath + ' not exist')
            openPath = os.getcwd()
        fileName, fileType = QtWidgets.QFileDialog.getOpenFileName(self.m_amlUi, "Open File", openPath, "All Files(*);;Text Files(*.txt)")
        if not fileName == '':
            self.m_amlUi.AmlAudioDebugPlayAudioPath_lineEdit.setText(fileName)
            self.__finished_PlayAudioPath()

    def __click_play_toggle(self):
        channel = int(self.m_amlUi.AmlAudioDebugPlayAudioChannel_comboBox.currentText())
        byte = int(self.m_amlUi.AmlAudioDebugPlayAudioByte_comboBox.currentText())
        rate = int(self.m_amlUi.AmlAudioDebugPlayAudioRate_comboBox.currentText())
        fileName = self.m_amlUi.AmlAudioDebugPlayAudioPath_lineEdit.text()
        isPlaying = self.audioDebug.start_play_toggle(fileName, channel, byte, rate, self.__callback_audioPlayFinish)
        if isPlaying == True:
            self.m_amlUi.AmlAudioDebugPlayAudio_Button.setText('Stop(playing)')
        else:
            self.m_amlUi.AmlAudioDebugPlayAudio_Button.setText('Play')

    def __pre_audio_debug_config(self):
        if self.m_amlUi.AmlAudioDebugModeAuto_radioButton.isChecked() == True:
            self.audioDebugcfg.m_captureMode = AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO
        elif self.m_amlUi.AmlAudioDebugModeManual_radioButton.isChecked() == True:
            self.audioDebugcfg.m_captureMode = AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL
        else:
            self.log_fuc('E __pre_audio_debug_config: Not supported capture mode!!!')
        self.audioDebugcfg.m_debugInfoEnable = self.m_amlUi.AmlAudioDebugOptionsDebug_checkBox.isChecked()
        self.audioDebugcfg.m_dumpDataEnable = self.m_amlUi.AmlAudioDebugOptionsDump_checkBox.isChecked()
        self.audioDebugcfg.m_logcatEnable = self.m_amlUi.AmlAudioDebugOptionsLogcat_checkBox.isChecked()
        self.audioDebugcfg.m_autoDebugTimeS = self.m_amlUi.AmlAudioCaptureTime_spinBox.value()
        self.audioDebugcfg.m_printDebugEnable = self.m_amlUi.AmlAudioPrintDebugEnable_checkBox.isChecked()
        self.audioDebugcfg.m_createZipFile = self.m_amlUi.AmlAudioCreateZipEnable_checkBox.isChecked()

    def __callback_startCaptureFinish(self):       
        if self.audioDebugcfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            self.m_amlUi.AmlAudioDebugMode_groupBox.setEnabled(True)
            self.m_amlUi.AmlAudioDebugOptions_groupBox.setEnabled(True)
            self.m_amlUi.AmlAudioDebugCaptureTime_groupBox.setEnabled(True)
            self.m_amlUi.AmlAudioDebugPrintDebug_groupBox.setEnabled(True)
            self.m_amlUi.AmlAudioCreateZipEnable_checkBox.setEnabled(True)
            self.m_amlUi.AmlAudioDebugStart_pushButton.setEnabled(True)
            self.log_fuc('######## Auto mode capture Finish !!! ############')
        elif self.audioDebugcfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL:
            self.m_amlUi.AmlAudioDebugStop_pushButton.setEnabled(True)
            self.log_fuc('Manual mode Start capture finish')

    def __startCaptureInfo(self):
        self.m_amlUi.remount()
        self.audioDebug.start_capture(self.__callback_startCaptureFinish)

    def __callback_stopCaptureFinish(self):
        self.log_fuc('######## Manual mode capture Finish !!! ############')
        self.m_amlUi.AmlAudioDebugMode_groupBox.setEnabled(True)
        self.m_amlUi.AmlAudioDebugOptions_groupBox.setEnabled(True)
        self.m_amlUi.AmlAudioDebugPrintDebug_groupBox.setEnabled(True)
        self.m_amlUi.AmlAudioCreateZipEnable_checkBox.setEnabled(True)
        self.m_amlUi.AmlAudioDebugStart_pushButton.setEnabled(True)

    def __stopCaptureInfo(self):
        self.audioDebug.stop_capture(self.__callback_stopCaptureFinish)

    def __callback_audioPlayFinish(self):
        self.m_amlUi.AmlAudioDebugPlayAudio_Button.setText('Play')