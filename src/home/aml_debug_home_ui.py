from threading import Thread
import time

from src.home.aml_ini_parser_home import AmlParserIniHome
from src.common.aml_ini_parser import amlParserIniContainer, AmlParserIniManager
from src.common.aml_debug_base_ui import AmlDebugBaseUi, AmlDebugModule
from src.common.aml_common_utils import AmlCommon, AmlCommonUtils

def instance(aml_ui):
    return AmlDebugHomeUi(aml_ui)

########################################################################################################
# Tab: "Home"
class AmlDebugHomeUi(AmlDebugBaseUi):
    class AmlDebugHomeCfg():
        def __init__(self):
            self.m_ModuleEnableArray = dict()
            self.m_ModuleEnableArray[AmlCommon.AML_DEBUG_MODULE_HOME] = True
            for index in range(AmlCommon.AML_DEBUG_MODULE_AUDIO, AmlCommon.AML_DEBUG_MODULE_MAX):
                self.m_ModuleEnableArray[index] = False
            self.m_logcatEnable = False
            self.m_bugreportEnable = False
            self.m_dmesgEnable = False
            self.m_captureMode = 0
            self.m_debugTime = 0

    def __init__(self, aml_ui):
        self.__m_iniPaser = amlParserIniContainer.getParserById(AmlParserIniManager.AML_PARSER_SECTION_HOME)
        self.__m_debugCfg = AmlDebugHomeUi.AmlDebugHomeCfg()
        super(AmlDebugHomeUi, self).__init__(aml_ui, AmlCommon.AML_DEBUG_MODULE_HOME)
        self.__startFinishCnt = dict()
        self.__stopFinishCnt = dict()
        self.__nowPullPcTimePath = ''
        self.__curTimeName = ''

    def init_display_ui(self):
        captureMode = self.__m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_CAPTRUE_MODE)
        if captureMode == AmlParserIniHome.DEBUG_CAPTURE_MODE_MUNUAL:
            self.m_amlUi.AmlDebugHomeModeManual_radioButton.setChecked(True)
            self.m_amlUi.AmlDebugHomeCaptureTime_groupBox.setEnabled(False)
        elif captureMode == AmlParserIniHome.DEBUG_CAPTURE_MODE_AUTO:
            self.m_amlUi.AmlDebugHomeModeAuto_radioButton.setChecked(True)
            self.m_amlUi.AmlDebugHomeCaptureTime_groupBox.setEnabled(True)
        else:
            self.log_fuc('E AmlDebugHomeUi.init_display_ui: Not supported capture mode:' + str(captureMode) + ' !!!')
        self.m_amlUi.AmlDebugHomeModulesAudio_checkBox.setChecked(self.__m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_AUDIO_ENABLE))
        self.m_amlUi.AmlDebugHomeModulesVideo_checkBox.setChecked(self.__m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_VIDEO_ENABLE))
        self.m_amlUi.AmlDebugHomeModulesCec_checkBox.setChecked(self.__m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_CEC_ENABLE))
        self.m_amlUi.AmlDebugHomeOptionsLogcat_checkBox.setChecked(self.__m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_LOGCAT))
        self.m_amlUi.AmlDebugHomeOptionsBugreport_checkBox.setChecked(self.__m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_BUGREPORT))
        self.m_amlUi.AmlDebugHomeOptionsDmesg_checkBox.setChecked(self.__m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_DMESG))

    def signals_connect_slots(self):
        self.m_amlUi.AmlDebugHomeModeAuto_radioButton.clicked.connect(self.__click_auto_mode)
        self.m_amlUi.AmlDebugHomeModeManual_radioButton.clicked.connect(self.__click_manual_mode)
        self.m_amlUi.AmlDebugHomeStart_pushButton.clicked.connect(self.__click_start_capture)
        self.m_amlUi.AmlDebugHomeStop_pushButton.clicked.connect(self.__click_stop_capture)
        self.m_amlUi.AmlDebugHomeModulesAudio_checkBox.clicked.connect(self.__click_modulesAudio)
        self.m_amlUi.AmlDebugHomeModulesVideo_checkBox.clicked.connect(self.__click_modulesVideo)
        self.m_amlUi.AmlDebugHomeModulesCec_checkBox.clicked.connect(self.__click_modulesCec)
        self.m_amlUi.AmlDebugHomeOptionsLogcat_checkBox.clicked.connect(self.__click_optionsLogcat)
        self.m_amlUi.AmlDebugHomeOptionsBugreport_checkBox.clicked.connect(self.__click_optionsBugreport)
        self.m_amlUi.AmlDebugHomeOptionsDmesg_checkBox.clicked.connect(self.__click_optionsDmesg)
        self.m_amlUi.AmlDebugHomeCaptureTime_spinBox.editingFinished.connect(self.__editingFinished_CaptureTime)

    def __click_auto_mode(self):
        self.m_amlUi.AmlDebugHomeCaptureTime_groupBox.setEnabled(True)
        self.__m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_CAPTRUE_MODE, AmlParserIniHome.DEBUG_CAPTURE_MODE_AUTO)
    def __click_manual_mode(self):
        self.m_amlUi.AmlDebugHomeCaptureTime_groupBox.setEnabled(False)
        self.__m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_CAPTRUE_MODE, AmlParserIniHome.DEBUG_CAPTURE_MODE_MUNUAL)
    def __click_modulesAudio(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_AUDIO_ENABLE, self.m_amlUi.AmlDebugHomeModulesAudio_checkBox.isChecked())
    def __click_modulesVideo(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_VIDEO_ENABLE, self.m_amlUi.AmlDebugHomeModulesVideo_checkBox.isChecked())
    def __click_modulesCec(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_CEC_ENABLE, self.m_amlUi.AmlDebugHomeModulesCec_checkBox.isChecked())
    def __click_optionsLogcat(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_LOGCAT, self.m_amlUi.AmlDebugHomeOptionsLogcat_checkBox.isChecked())
    def __click_optionsBugreport(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_BUGREPORT, self.m_amlUi.AmlDebugHomeOptionsBugreport_checkBox.isChecked())
    def __click_optionsDmesg(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_DMESG, self.m_amlUi.AmlDebugHomeOptionsDmesg_checkBox.isChecked())
    def __editingFinished_CaptureTime(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_CAPTURE_TIME, self.m_amlUi.AmlDebugHomeCaptureTime_spinBox.value())

    def __click_start_capture(self):
        self.m_amlUi.AmlDebugHomeStart_pushButton.setEnabled(False)
        self.m_amlUi.AmlDebugHomeModules_groupBox.setEnabled(False)
        self.m_amlUi.AmlDebugHomeOptions_groupBox.setEnabled(False)
        self.m_amlUi.AmlDebugMode_groupBox.setEnabled(False)
        self.m_amlUi.AmlDebugHomeCaptureTime_groupBox.setEnabled(False)
        self.m_amlUi.remount()
        self.__pre_debug_cfg()
        for module in AmlDebugModule.moduleList:
            self.__startFinishCnt[module.m_moduleId] = False
        for module in AmlDebugModule.moduleList:
            if self.__m_debugCfg.m_ModuleEnableArray[module.m_moduleId] == True:
                module.start_capture(self.__curTimeName, self.__callback_startFinish)

    def __click_stop_capture(self):
        self.m_amlUi.AmlDebugAudioStop_pushButton.setEnabled(False)
        for module in AmlDebugModule.moduleList:
            self.__stopFinishCnt[module.m_moduleId] = False
        for module in AmlDebugModule.moduleList:
            module.stop_capture(self.__callback_stopFinish)

    def closeEvent(self):
        self.__m_stop_thread = True

    def start_capture(self, curTimeName, homeCallbackFinish):
        print('AmlDebugHomeUi:start_capture')
        self.__curTimeName = AmlCommonUtils.pre_create_directory(self.m_moduleId, self.__m_debugCfg.m_ModuleEnableArray)
        self.__nowPullPcTimePath = AmlCommon.AML_DEBUG_DIRECOTRY_ROOT + '\\' + self.__curTimeName
        print('m_bugreportEnable:' + str(self.__m_debugCfg.m_bugreportEnable) + ', m_logcatEnable:' + str(self.__m_debugCfg.m_logcatEnable) + ', dmesg:'+str(self.__m_debugCfg.m_dmesgEnable))
        thread = Thread(target = self.__start_capture_thread, args=(homeCallbackFinish,))
        thread.start()

    def stop_capture(self, homeCallbackFinish):
        AmlCommonUtils.logcat_stop()
        AmlCommon.exe_adb_cmd('adb pull "' + AmlCommon.AML_DEBUG_PLATFORM_DIRECOTRY_LOGCAT + '" ' + self.__nowPullPcTimePath, True)
        if self.__m_debugCfg.m_dmesgEnable:
            AmlCommon.exe_adb_cmd('adb pull "' + AmlCommon.AML_DEBUG_PLATFORM_DIRECOTRY_DMESG + '" ' + self.__nowPullPcTimePath, True)
        self.log_fuc('AmlDebugHomeUi::stop_capture')
        homeCallbackFinish(self.m_moduleId)

    def __start_capture_thread(self, homeCallbackFinish):
        if self.__m_debugCfg.m_logcatEnable:
            timeS = self.m_amlUi.AmlDebugHomeCaptureTime_spinBox.value()
            self.log_fuc('AmlDebugHomeUi::start_capture logcat start, please wait ' + str(timeS) + 's for logcat...')
            for module in AmlDebugModule.moduleList:
                if self.__m_debugCfg.m_ModuleEnableArray[module.m_moduleId] == True and module.get_logcat_enable() == True:
                    module.open_logcat()
            AmlCommonUtils.logcat_start()
            if self.__m_debugCfg.m_captureMode == AmlParserIniHome.DEBUG_CAPTURE_MODE_AUTO:
                time.sleep(timeS)
                self.log_fuc('AmlDebugHomeUi::start_capture logcat stop ++++')
                for module in AmlDebugModule.moduleList:
                    if self.__m_debugCfg.m_ModuleEnableArray[module.m_moduleId] == True and module.get_logcat_enable() == True:
                        module.close_logcat()
                AmlCommonUtils.logcat_stop()
                AmlCommon.exe_adb_cmd('adb pull "' + AmlCommon.AML_DEBUG_PLATFORM_DIRECOTRY_LOGCAT + '" ' + self.__nowPullPcTimePath, True)
        if self.__m_debugCfg.m_bugreportEnable:
            AmlCommonUtils.bugreport(self.__nowPullPcTimePath)
        if self.__m_debugCfg.m_dmesgEnable:
            AmlCommonUtils.dmesg()
            AmlCommon.exe_adb_cmd('adb pull "' + AmlCommon.AML_DEBUG_PLATFORM_DIRECOTRY_DMESG + '" ' + self.__nowPullPcTimePath, True)
        self.log_fuc('-------- [Home] Auto mode capture Finish !!! --------')
        homeCallbackFinish(self.m_moduleId)

    def __callback_startFinish(self, moduleId):
        self.__startFinishCnt[moduleId] = True
        self.log_fuc('__callback_startFinish moduleId:' + str(moduleId) + ' finished')
        for module in AmlDebugModule.moduleList:
            if self.__startFinishCnt[module.m_moduleId] == False and self.__m_debugCfg.m_ModuleEnableArray[module.m_moduleId] == True:
                return
        self.log_fuc('[Home] Please send folder ' + self.__nowPullPcTimePath + ' to RD colleagues! Thank You!')
        if self.__m_debugCfg.m_captureMode == AmlParserIniHome.DEBUG_CAPTURE_MODE_AUTO:
            self.m_amlUi.AmlDebugHomeModules_groupBox.setEnabled(True)
            self.m_amlUi.AmlDebugHomeOptions_groupBox.setEnabled(True)
            self.m_amlUi.AmlDebugMode_groupBox.setEnabled(True)
            self.m_amlUi.AmlDebugHomeCaptureTime_groupBox.setEnabled(True)
            self.m_amlUi.AmlDebugHomeStart_pushButton.setEnabled(True)
            self.log_fuc('######## [All Module] Auto mode capture Finish !!! ############')
        elif self.__m_debugCfg.m_captureMode == AmlParserIniHome.DEBUG_CAPTURE_MODE_MUNUAL:
            self.m_amlUi.AmlDebugHomeStop_pushButton.setEnabled(True)
            self.log_fuc('######## [All Module] Manual mode Start capture finish !!! ############')

    def __callback_stopFinish(self, moduleId):
        self.log_fuc('__callback_stopFinish moduleId:' + moduleId)
        self.__stopFinishCnt[moduleId] = True
        for module in AmlDebugModule.moduleList:
            if self.__stopFinishCnt[module.m_moduleId] == False and self.__m_debugCfg.m_ModuleEnableArray[module.m_moduleId] == True:
                self.log_fuc('__callback_stopFinish: return m_moduleId:' + str(module.m_moduleId))
                return
        self.log_fuc('######## [All Module] Manual mode capture Finish !!! ############')
        self.m_amlUi.AmlDebugHomeModules_groupBox.setEnabled(True)
        self.m_amlUi.AmlDebugHomeOptions_groupBox.setEnabled(True)
        self.m_amlUi.AmlDebugMode_groupBox.setEnabled(True)
        self.m_amlUi.AmlDebugHomeStart_pushButton.setEnabled(True)

    def __pre_debug_cfg(self):
        if self.m_amlUi.AmlDebugHomeModeAuto_radioButton.isChecked() == True:
            self.__m_debugCfg.m_captureMode = AmlParserIniHome.DEBUG_CAPTURE_MODE_AUTO
        elif self.m_amlUi.AmlDebugHomeModeManual_radioButton.isChecked() == True:
            self.__m_debugCfg.m_captureMode = AmlParserIniHome.DEBUG_CAPTURE_MODE_MUNUAL
        else:
            self.log_fuc('E Home __pre_debug_cfg: Not supported capture mode!!!')
        self.__m_debugCfg.m_ModuleEnableArray[AmlCommon.AML_DEBUG_MODULE_AUDIO] = self.m_amlUi.AmlDebugHomeModulesAudio_checkBox.isChecked()
        self.__m_debugCfg.m_ModuleEnableArray[AmlCommon.AML_DEBUG_MODULE_VIDEO] = self.m_amlUi.AmlDebugHomeModulesVideo_checkBox.isChecked()
        self.__m_debugCfg.m_ModuleEnableArray[AmlCommon.AML_DEBUG_MODULE_CEC] = self.m_amlUi.AmlDebugHomeModulesCec_checkBox.isChecked()
        self.__m_debugCfg.m_logcatEnable = self.m_amlUi.AmlDebugHomeOptionsLogcat_checkBox.isChecked()
        self.__m_debugCfg.m_bugreportEnable = self.m_amlUi.AmlDebugHomeOptionsBugreport_checkBox.isChecked()
        self.__m_debugCfg.m_dmesgEnable = self.m_amlUi.AmlDebugHomeOptionsDmesg_checkBox.isChecked()
        self.__m_debugCfg.m_debugTime = self.m_amlUi.AmlDebugHomeCaptureTime_spinBox.value()
