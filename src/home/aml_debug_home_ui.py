from threading import Thread
import time, os

from PyQt5.QtCore import QStringListModel

from src.home.aml_ini_parser_home import AmlParserIniHome
from src.common.aml_debug_base_ui import AmlDebugBaseUi, AmlDebugModule
from src.common.aml_common_utils import AmlCommonUtils

def instance(aml_ui):
    return AmlDebugHomeUi(aml_ui)

########################################################################################################
# Tab: "Home"
class AmlDebugHomeUi(AmlDebugBaseUi):
    class AmlDebugHomeCfg():
        def __init__(self):
            self.m_ModuleEnableArray = dict()
            self.m_ModuleEnableArray[AmlCommonUtils.AML_DEBUG_MODULE_HOME] = True
            for index in range(AmlCommonUtils.AML_DEBUG_MODULE_AUDIO, AmlCommonUtils.AML_DEBUG_MODULE_MAX):
                self.m_ModuleEnableArray[index] = False
            self.m_logcatEnable = False
            self.m_bugreportEnable = False
            self.m_dmesgEnable = False
            self.m_captureMode = 0
            self.m_debugTime = 0

    def __init__(self, aml_ui):
        self.__m_debugCfg = AmlDebugHomeUi.AmlDebugHomeCfg()
        super(AmlDebugHomeUi, self).__init__(aml_ui, AmlCommonUtils.AML_DEBUG_MODULE_HOME)
        self.__startFinishCnt = dict()
        self.__stopFinishCnt = dict()
        self.__nowPullPcTimePath = ''
        self.__curTimeName = ''

    def init_display_ui(self):
        captureMode = self.m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_CAPTRUE_MODE)
        if captureMode == AmlParserIniHome.DEBUG_CAPTURE_MODE_MUNUAL:
            self.m_mainUi.AmlDebugHomeModeManual_radioButton.setChecked(True)
            self.m_mainUi.AmlDebugHomeCaptureTime_groupBox.setEnabled(False)
        elif captureMode == AmlParserIniHome.DEBUG_CAPTURE_MODE_AUTO:
            self.m_mainUi.AmlDebugHomeModeAuto_radioButton.setChecked(True)
            self.m_mainUi.AmlDebugHomeCaptureTime_groupBox.setEnabled(True)
        else:
            self.logF('init_display_ui: Not supported capture mode:' + str(captureMode) + ' !!!')
        self.m_mainUi.AmlDebugHomeModulesAudio_checkBox.setChecked(self.m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_AUDIO_ENABLE))
        self.m_mainUi.AmlDebugHomeModulesVideo_checkBox.setChecked(self.m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_VIDEO_ENABLE))
        self.m_mainUi.AmlDebugHomeModulesCec_checkBox.setChecked(self.m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_CEC_ENABLE))
        self.m_mainUi.AmlDebugHomeOptionsLogcat_checkBox.setChecked(self.m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_LOGCAT))
        self.m_mainUi.AmlDebugHomeOptionsBugreport_checkBox.setChecked(self.m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_BUGREPORT))
        self.m_mainUi.AmlDebugHomeOptionsDmesg_checkBox.setChecked(self.m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_DMESG))
        self.m_mainUi.AmlDebugHomeAdbDevIp_lineEdit.setText(self.m_iniPaser.getValueByKey(AmlParserIniHome.AML_PARSER_HOME_IP_ADDRESS))

    def signals_connect_slots(self):
        self.m_mainUi.AmlDebugHomeModeAuto_radioButton.clicked.connect(self.__click_auto_mode)
        self.m_mainUi.AmlDebugHomeModeManual_radioButton.clicked.connect(self.__click_manual_mode)
        self.m_mainUi.AmlDebugHomeStart_pushButton.clicked.connect(self.__click_start_capture)
        self.m_mainUi.AmlDebugHomeStop_pushButton.clicked.connect(self.__click_stop_capture)
        self.m_mainUi.AmlDebugHomeModulesAudio_checkBox.clicked[bool].connect(self.__click_modulesAudio)
        self.m_mainUi.AmlDebugHomeModulesVideo_checkBox.clicked[bool].connect(self.__click_modulesVideo)
        self.m_mainUi.AmlDebugHomeModulesCec_checkBox.clicked[bool].connect(self.__click_modulesCec)
        self.m_mainUi.AmlDebugHomeOptionsLogcat_checkBox.stateChanged[int].connect(self.__changed_optionsLogcat)
        self.m_mainUi.AmlDebugHomeOptionsBugreport_checkBox.stateChanged[int].connect(self.__changed_optionsBugreport)
        self.m_mainUi.AmlDebugHomeOptionsDmesg_checkBox.stateChanged[int].connect(self.__changed_optionsDmesg)
        self.m_mainUi.AmlDebugHomeCaptureTime_spinBox.editingFinished.connect(self.__editingFinished_CaptureTime)
        self.m_mainUi.AmlDebugHomeAdbDevRefresh_pushButton.clicked.connect(self.__click_adbRefresh)
        self.m_mainUi.AmlDebugHomeAdbDevConnect_pushButton.clicked.connect(self.__click_adbConnect)
        self.m_mainUi.AmlDebugHomeAdbDev_comboBox.currentTextChanged[str].connect(self.__textChanged_selectAdbDev)
        self.m_mainUi.AmlDebugHomeOpenOutput_pushButton.clicked.connect(self.__click_open_output)
        self.m_mainUi.AmlDebugHomeAdbDevIp_lineEdit.textChanged.connect(self.__textChanged_adbIpAdress)

    def __click_auto_mode(self):
        self.m_mainUi.AmlDebugHomeCaptureTime_groupBox.setEnabled(True)
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_CAPTRUE_MODE, AmlParserIniHome.DEBUG_CAPTURE_MODE_AUTO)
    def __click_manual_mode(self):
        self.m_mainUi.AmlDebugHomeCaptureTime_groupBox.setEnabled(False)
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_CAPTRUE_MODE, AmlParserIniHome.DEBUG_CAPTURE_MODE_MUNUAL)
    def __click_modulesAudio(self, enable):
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_AUDIO_ENABLE, enable)
    def __click_modulesVideo(self, enable):
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_VIDEO_ENABLE, enable)
    def __click_modulesCec(self, enable):
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_CEC_ENABLE, enable)
    def __changed_optionsLogcat(self, state):
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_LOGCAT, self.state_to_bool(state))
    def __changed_optionsBugreport(self, state):
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_BUGREPORT, self.state_to_bool(state))
    def __changed_optionsDmesg(self, state):
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_DMESG, self.state_to_bool(state))
    def __editingFinished_CaptureTime(self):
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_CAPTURE_TIME, self.m_mainUi.AmlDebugHomeCaptureTime_spinBox.value())

    def __click_start_capture(self):
        self.m_mainUi.AmlDebugHomeStart_pushButton.setEnabled(False)
        self.m_mainUi.AmlDebugHomeModules_groupBox.setEnabled(False)
        self.m_mainUi.AmlDebugHomeOptions_groupBox.setEnabled(False)
        self.m_mainUi.AmlDebugMode_groupBox.setEnabled(False)
        self.m_mainUi.AmlDebugHomeCaptureTime_groupBox.setEnabled(False)
        AmlCommonUtils.adb_root()
        AmlCommonUtils.adb_remount()
        self.__pre_debug_cfg()
        for module in AmlDebugModule.moduleList:
            self.__startFinishCnt[module.m_moduleId] = False
        for module in AmlDebugModule.moduleList:
            if self.__m_debugCfg.m_ModuleEnableArray[module.m_moduleId] == True:
                module.start_capture(self.__curTimeName, self.__callback_startFinish, True)

    def __click_stop_capture(self):
        self.m_mainUi.AmlDebugAudioStop_pushButton.setEnabled(False)
        for module in AmlDebugModule.moduleList:
            self.__stopFinishCnt[module.m_moduleId] = False
        for module in AmlDebugModule.moduleList:
            module.stop_capture(self.__callback_stopFinish, True)

    def __click_adbRefresh(self):
        dev_list = self.__adb_dev_ui_refresh()
        if len(dev_list) > 0:
            cur_dev = self.m_mainUi.AmlDebugHomeAdbDev_comboBox.currentText()
            # self.log.d('__click_adbRefresh select adb device:' + cur_dev)
            AmlCommonUtils.set_adb_cur_device(cur_dev)
        else:
            AmlCommonUtils.set_adb_cur_device('')

    def __click_adbConnect(self):
        ip = self.m_mainUi.AmlDebugHomeAdbDevIp_lineEdit.text()
        dev_name = AmlCommonUtils.adb_connect_by_ip(ip)
        if dev_name == '':
            return
        self.__adb_dev_ui_refresh()
        self.m_mainUi.AmlDebugHomeAdbDev_comboBox.setCurrentText(dev_name)

    def __textChanged_selectAdbDev(self, value):
        AmlCommonUtils.set_adb_cur_device(value)

    def __click_open_output(self):
        os.startfile(self.check_output_path(self.__nowPullPcTimePath))

    def __textChanged_adbIpAdress(self, value):
        self.m_iniPaser.setValueByKey(AmlParserIniHome.AML_PARSER_HOME_IP_ADDRESS, value)

    def closeEvent(self):
        self.__m_stop_thread = True

    def start_capture(self, curTimeName, homeCallbackFinish, homeClick):
        self.log.i('start_capture')
        self.__curTimeName = AmlCommonUtils.pre_create_directory(self.m_moduleId, self.__m_debugCfg.m_ModuleEnableArray)
        self.__nowPullPcTimePath = AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT + '\\' + self.__curTimeName
        thread = Thread(target = self.__start_capture_thread, args=(homeCallbackFinish,))
        thread.start()

    def stop_capture(self, homeCallbackFinish):
        self.log.i('stop_capture')
        AmlCommonUtils.logcat_stop()
        AmlCommonUtils.pull_logcat_to_pc(self.__nowPullPcTimePath)
        if self.__m_debugCfg.m_dmesgEnable:
            AmlCommonUtils.exe_adb_cmd('pull "' + AmlCommonUtils.AML_DEBUG_PLATFORM_DIRECOTRY_DMESG + '" ' + self.__nowPullPcTimePath, True)
        self.log.i('stop_capture')
        homeCallbackFinish(self.m_moduleId)

    def __start_capture_thread(self, homeCallbackFinish):
        if self.__m_debugCfg.m_logcatEnable:
            timeS = self.m_mainUi.AmlDebugHomeCaptureTime_spinBox.value()
            self.log.i('start_capture logcat start, please wait ' + str(timeS) + 's for logcat...')
            for module in AmlDebugModule.moduleList:
                if self.__m_debugCfg.m_ModuleEnableArray[module.m_moduleId] == True and module.get_logcat_enable() == True:
                    module.open_logcat()
            if self.__m_debugCfg.m_captureMode == AmlParserIniHome.DEBUG_CAPTURE_MODE_AUTO:
                AmlCommonUtils.logcat_start()
                time.sleep(timeS)
                self.log.i('AmlDebugHomeUi::start_capture logcat stop ++++')
                for module in AmlDebugModule.moduleList:
                    if self.__m_debugCfg.m_ModuleEnableArray[module.m_moduleId] == True and module.get_logcat_enable() == True:
                        module.close_logcat()
                AmlCommonUtils.logcat_stop()
                AmlCommonUtils.pull_logcat_to_pc(self.__nowPullPcTimePath)
        if self.__m_debugCfg.m_bugreportEnable:
            AmlCommonUtils.bugreport(self.__nowPullPcTimePath)
        if self.__m_debugCfg.m_dmesgEnable:
            AmlCommonUtils.dmesg()
            AmlCommonUtils.exe_adb_cmd('pull "' + AmlCommonUtils.AML_DEBUG_PLATFORM_DIRECOTRY_DMESG + '" ' + self.__nowPullPcTimePath, True)
        self.log.i('-------- [Home] Auto mode capture Finish !!! --------')
        homeCallbackFinish(self.m_moduleId)

    def __callback_startFinish(self, moduleId):
        if moduleId not in self.AML_MODULE_NAME_ARRAY.keys():
            self.log.w(str(moduleId) + ' is invalid...')
            return
        self.__startFinishCnt[moduleId] = True
        self.log.i('__callback_startFinish ' + self.AML_MODULE_NAME_ARRAY[moduleId] + '[' + str(moduleId) + ']')
        for module in AmlDebugModule.moduleList:
            if self.__startFinishCnt[module.m_moduleId] == False and self.__m_debugCfg.m_ModuleEnableArray[module.m_moduleId] == True:
                return
        self.log.i('[Home] Please send folder ' + self.__nowPullPcTimePath + ' to RD colleagues! Thank You!')
        if self.__m_debugCfg.m_captureMode == AmlParserIniHome.DEBUG_CAPTURE_MODE_AUTO:
            self.m_mainUi.AmlDebugHomeModules_groupBox.setEnabled(True)
            self.m_mainUi.AmlDebugHomeOptions_groupBox.setEnabled(True)
            self.m_mainUi.AmlDebugMode_groupBox.setEnabled(True)
            self.m_mainUi.AmlDebugHomeCaptureTime_groupBox.setEnabled(True)
            self.m_mainUi.AmlDebugHomeStart_pushButton.setEnabled(True)
            AmlCommonUtils.generate_snapshot(self.__nowPullPcTimePath)
            self.log.i('######## [All Module] Auto mode capture Finish !!! ############')
        elif self.__m_debugCfg.m_captureMode == AmlParserIniHome.DEBUG_CAPTURE_MODE_MUNUAL:
            self.m_mainUi.AmlDebugHomeStop_pushButton.setEnabled(True)
            self.log.i('######## [All Module] Manual mode Start capture finish !!! ############')

    def __callback_stopFinish(self, moduleId):
        self.log.i('__callback_stopFinish ' + self.AML_MODULE_NAME_ARRAY[moduleId] + '[' + str(moduleId) + ']')
        self.__stopFinishCnt[moduleId] = True
        for module in AmlDebugModule.moduleList:
            if self.__stopFinishCnt[module.m_moduleId] == False and self.__m_debugCfg.m_ModuleEnableArray[module.m_moduleId] == True:
                self.log.i('__callback_stopFinish: return m_moduleId:' + str(module.m_moduleId))
                return
        AmlCommonUtils.generate_snapshot(self.__nowPullPcTimePath)
        self.log.i('######## [All Module] Manual mode capture Finish !!! ############')
        self.m_mainUi.AmlDebugHomeModules_groupBox.setEnabled(True)
        self.m_mainUi.AmlDebugHomeOptions_groupBox.setEnabled(True)
        self.m_mainUi.AmlDebugMode_groupBox.setEnabled(True)
        self.m_mainUi.AmlDebugHomeStart_pushButton.setEnabled(True)

    def __pre_debug_cfg(self):
        if self.m_mainUi.AmlDebugHomeModeAuto_radioButton.isChecked() == True:
            self.__m_debugCfg.m_captureMode = AmlParserIniHome.DEBUG_CAPTURE_MODE_AUTO
        elif self.m_mainUi.AmlDebugHomeModeManual_radioButton.isChecked() == True:
            self.__m_debugCfg.m_captureMode = AmlParserIniHome.DEBUG_CAPTURE_MODE_MUNUAL
        else:
            self.log.e('__pre_debug_cfg: Not supported capture mode!!!')
        self.__m_debugCfg.m_ModuleEnableArray[AmlCommonUtils.AML_DEBUG_MODULE_AUDIO] = self.m_mainUi.AmlDebugHomeModulesAudio_checkBox.isChecked()
        self.__m_debugCfg.m_ModuleEnableArray[AmlCommonUtils.AML_DEBUG_MODULE_VIDEO] = self.m_mainUi.AmlDebugHomeModulesVideo_checkBox.isChecked()
        self.__m_debugCfg.m_ModuleEnableArray[AmlCommonUtils.AML_DEBUG_MODULE_CEC] = self.m_mainUi.AmlDebugHomeModulesCec_checkBox.isChecked()
        self.__m_debugCfg.m_logcatEnable = self.m_mainUi.AmlDebugHomeOptionsLogcat_checkBox.isChecked()
        self.__m_debugCfg.m_bugreportEnable = self.m_mainUi.AmlDebugHomeOptionsBugreport_checkBox.isChecked()
        self.__m_debugCfg.m_dmesgEnable = self.m_mainUi.AmlDebugHomeOptionsDmesg_checkBox.isChecked()
        self.__m_debugCfg.m_debugTime = self.m_mainUi.AmlDebugHomeCaptureTime_spinBox.value()

    def __adb_dev_ui_refresh(self):
        dev_list = AmlCommonUtils.get_adb_devices()
        self.m_mainUi.AmlDebugHomeAdbDev_comboBox.clear()
        if len(dev_list) > 0:
            self.m_mainUi.AmlDebugHomeAdbDev_comboBox.addItems(dev_list)
        listModel = QStringListModel()
        listModel.setStringList(dev_list)
        self.m_mainUi.AmlDebugHomeAdbDev_listView.setModel(listModel)
        return dev_list