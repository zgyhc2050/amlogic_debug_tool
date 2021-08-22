import sys
from threading import Thread

from src.audio.aml_debug_audio import AmlAudioDebug, AudioDebugCfg
from src.audio.aml_ini_parser_audio import AmlParserIniAudio
from src.common.aml_debug_base_ui import AmlDebugBaseUi
from src.common.aml_ini_parser import amlParserIniContainer, AmlParserIniManager


def instance(aml_ui):
    return AmlDebugAudioDebugUi(aml_ui)

########################################################################################################
# Table 1: "Audio Debug"
class AmlDebugAudioDebugUi(AmlDebugBaseUi):
    def __init__(self, aml_ui):
        self.__m_iniPaser = amlParserIniContainer.getParserById(AmlParserIniManager.AML_PARSER_SECTION_AUDIO)
        self.audioDebug = AmlAudioDebug()
        self.audioDebugcfg = AudioDebugCfg()
        super(AmlDebugAudioDebugUi, self).__init__(aml_ui)

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

    def init_display_ui(self):
        if self.audioDebugcfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL:
            self.m_amlUi.AmlAudioDebugModeManual_radioButton.setChecked(True)
            self.m_amlUi.AmlAudioDebugCaptureTime_groupBox.setEnabled(False)
        elif self.audioDebugcfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            self.m_amlUi.AmlAudioDebugModeAuto_radioButton.setChecked(True)
            self.m_amlUi.AmlAudioDebugCaptureTime_groupBox.setEnabled(True)
        else:
            self.m_amlUi.terminalLog('E refresh_capture_mode_ui: Not supported capture mode:' + str(self.audioDebugcfg.m_captureMode) + ' !!!')
        self.m_amlUi.AmlAudioDebugOptionsDebug_checkBox.setChecked(self.audioDebugcfg.m_debugInfoEnable)
        self.m_amlUi.AmlAudioDebugOptionsDump_checkBox.setChecked(self.audioDebugcfg.m_dumpDataEnable)
        self.m_amlUi.AmlAudioDebugOptionsLogcat_checkBox.setChecked(self.audioDebugcfg.m_logcatEnable)
        self.m_amlUi.AmlAudioPrintDebugEnable_checkBox.setChecked(self.audioDebugcfg.m_printDebugEnable)
        self.m_amlUi.AmlAudioCaptureTime_spinBox.setValue(self.audioDebugcfg.m_autoDebugTimeS)
        self.m_amlUi.AmlAudioCreateZipEnable_checkBox.setChecked(self.audioDebugcfg.m_createZipFile)

    def init_default_config(self):
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
        print('AmlDebugAudioDebugUi __click_start_capture')
        self.m_amlUi.AmlAudioDebugMode_groupBox.setEnabled(False)
        self.m_amlUi.AmlAudioDebugOptions_groupBox.setEnabled(False)
        self.m_amlUi.AmlAudioDebugCaptureTime_groupBox.setEnabled(False)
        self.m_amlUi.AmlAudioDebugPrintDebug_groupBox.setEnabled(False)
        self.m_amlUi.AmlAudioCreateZipEnable_checkBox.setEnabled(False)
        self.m_amlUi.AmlAudioDebugStart_pushButton.setEnabled(False)
  
        self.__pre_audio_debug_config()
        self.m_amlUi.terminalLog('')
        self.audioDebug.setAudioDebugCfg(self.audioDebugcfg)
        self.audioDebug.setShowStatusCallback(self.m_amlUi.terminalLog)
        thr = Thread(target = self.__startCaptureInfo)
        print('Thread start ++')
        thr.start()
        print('Thread start end--')

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

    def __click_stop_capture(self):
        self.m_amlUi.AmlAudioDebugStop_pushButton.setEnabled(False)
        thr = Thread(target = self.__stopCaptureInfo)
        thr.start()

    def __pre_audio_debug_config(self):
        if self.m_amlUi.AmlAudioDebugModeAuto_radioButton.isChecked() == True:
            self.audioDebugcfg.m_captureMode = AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO
        elif self.m_amlUi.AmlAudioDebugModeManual_radioButton.isChecked() == True:
            self.audioDebugcfg.m_captureMode = AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL
        else:
            self.m_amlUi.terminalLog('E __pre_audio_debug_config: Not supported capture mode!!!')
        self.audioDebugcfg.m_debugInfoEnable = self.m_amlUi.AmlAudioDebugOptionsDebug_checkBox.isChecked()
        self.audioDebugcfg.m_dumpDataEnable = self.m_amlUi.AmlAudioDebugOptionsDump_checkBox.isChecked()
        self.audioDebugcfg.m_logcatEnable = self.m_amlUi.AmlAudioDebugOptionsLogcat_checkBox.isChecked()
        self.audioDebugcfg.m_autoDebugTimeS = self.m_amlUi.AmlAudioCaptureTime_spinBox.value()
        self.audioDebugcfg.m_printDebugEnable = self.m_amlUi.AmlAudioPrintDebugEnable_checkBox.isChecked()
        self.audioDebugcfg.m_createZipFile = self.m_amlUi.AmlAudioCreateZipEnable_checkBox.isChecked()
        if self.audioDebugcfg.m_printDebugEnable:
            self.m_amlUi.terminalLog('m_captureMode:' + str(self.audioDebugcfg.m_captureMode))
            self.m_amlUi.terminalLog('m_debugInfoEnable:' + str(self.audioDebugcfg.m_debugInfoEnable))
            self.m_amlUi.terminalLog('m_dumpDataEnable:' + str(self.audioDebugcfg.m_dumpDataEnable))
            self.m_amlUi.terminalLog('m_logcatEnable:' + str(self.audioDebugcfg.m_logcatEnable))
            self.m_amlUi.terminalLog('m_printDebugEnable:' + str(self.audioDebugcfg.m_printDebugEnable))
            self.m_amlUi.terminalLog('m_autoDebugTimeS:' + str(self.audioDebugcfg.m_autoDebugTimeS))
            self.m_amlUi.terminalLog('m_createZipFile:' + str(self.audioDebugcfg.m_createZipFile))

    def __callback_startCaptureFinish(self):       
        if self.audioDebugcfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            self.m_amlUi.AmlAudioDebugMode_groupBox.setEnabled(True)
            self.m_amlUi.AmlAudioDebugOptions_groupBox.setEnabled(True)
            self.m_amlUi.AmlAudioDebugCaptureTime_groupBox.setEnabled(True)
            self.m_amlUi.AmlAudioDebugPrintDebug_groupBox.setEnabled(True)
            self.m_amlUi.AmlAudioCreateZipEnable_checkBox.setEnabled(True)
            self.m_amlUi.AmlAudioDebugStart_pushButton.setEnabled(True)
            self.m_amlUi.terminalLog('######## Auto mode capture Finish !!! ############')
        elif self.audioDebugcfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL:
            self.m_amlUi.AmlAudioDebugStop_pushButton.setEnabled(True)
            self.m_amlUi.terminalLog('Manual mode Start capture finish')

    def __startCaptureInfo(self):
        print('__startCaptureInfo+++')
        self.m_amlUi.remount()
        print('__startCaptureInfo  pppppp')
        self.audioDebug.start_capture(self.__callback_startCaptureFinish)
        print('__startCaptureInfo --')

    def __callback_stopCaptureFinish(self):
        self.m_amlUi.terminalLog('######## Manual mode capture Finish !!! ############')
        self.m_amlUi.AmlAudioDebugMode_groupBox.setEnabled(True)
        self.m_amlUi.AmlAudioDebugOptions_groupBox.setEnabled(True)
        self.m_amlUi.AmlAudioDebugPrintDebug_groupBox.setEnabled(True)
        self.m_amlUi.AmlAudioCreateZipEnable_checkBox.setEnabled(True)
        self.m_amlUi.AmlAudioDebugStart_pushButton.setEnabled(True)

    def __stopCaptureInfo(self):
        self.audioDebug.stop_capture(self.__callback_stopCaptureFinish)
