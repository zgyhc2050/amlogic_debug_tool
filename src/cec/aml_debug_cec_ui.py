from threading import Thread

from src.cec.aml_ini_parser_cec import AmlParserIniCec
from src.common.aml_debug_base_ui import AmlDebugBaseUi
from src.common.aml_common_utils import AmlCommonUtils

def instance(aml_ui):
    return AmlDebugCecUi(aml_ui)

########################################################################################################
# Table: "CEC"
class AmlDebugCecUi(AmlDebugBaseUi):
    def __init__(self, aml_ui):
        super(AmlDebugCecUi, self).__init__(aml_ui, AmlCommonUtils.AML_DEBUG_MODULE_CEC)
        self.__adbSetDebugPropList = [
            'echo log.tag.AudioService=DEBUG >> vendor/build.prop',
            'echo log.tag.volume=DEBUG >> vendor/build.prop',
            'echo log.tag.HDMI=DEBUG >> vendor/build.prop',
        ]
        self.__m_logcatEnable = False
        self.__m_bugreportEnable = False

    def init_display_ui(self):
        self.__m_logcatEnable = self.m_iniPaser.getValueByKey(AmlParserIniCec.AML_PARSER_CEC_LOGCAT)
        self.__m_bugreportEnable = self.m_iniPaser.getValueByKey(AmlParserIniCec.AML_PARSER_CEC_BUGREPORT)
        self.m_mainUi.AmlDebugCecOptionsLogcat_checkBox.setChecked(self.__m_logcatEnable)
        self.m_mainUi.AmlDebugCecOptionsBugreport_checkBox.setChecked(self.__m_bugreportEnable)

    def signals_connect_slots(self):
        self.m_mainUi.AmlDebugCecSetprop_pushButton.clicked.connect(self.__click_setprop)
        self.m_mainUi.AmlDebugCecReboot_pushButton.clicked.connect(AmlCommonUtils.adb_reboot)
        self.m_mainUi.AmlDebugCecStart_pushButton.clicked.connect(self.start_capture)
        self.m_mainUi.AmlDebugCecStop_pushButton.clicked.connect(self.stop_capture)
        self.m_mainUi.AmlDebugCecOptionsLogcat_checkBox.clicked[bool].connect(self.__click_optionsLogcat)
        self.m_mainUi.AmlDebugCecOptionsBugreport_checkBox.clicked[bool].connect(self.__click_optionsBugreport)

    def closeEvent(self):
        pass

    def __click_optionsLogcat(self, enable):
        if enable:
            self.m_mainUi.AmlDebugHomeOptionsLogcat_checkBox.setChecked(True)
        self.m_iniPaser.setValueByKey(AmlParserIniCec.AML_PARSER_CEC_LOGCAT, enable)
    def __click_optionsBugreport(self, enable):
        if enable:
            self.m_mainUi.AmlDebugHomeOptionsBugreport_checkBox.setChecked(True)
        self.m_iniPaser.setValueByKey(AmlParserIniCec.AML_PARSER_CEC_BUGREPORT, enable)
    def __click_setprop(self):
        AmlCommonUtils.adb_root()
        AmlCommonUtils.adb_remount()
        for cmd in self.__adbSetDebugPropList:
            AmlCommonUtils.exe_adb_shell_cmd(cmd, True)

    def start_capture(self, curTimeName='', homeCallbackFinish='', homeClick=False):
        self.log.i('start_capture')
        self.m_mainUi.AmlDebugCecStart_pushButton.setEnabled(False)
        self.__m_logcatEnable = self.m_mainUi.AmlDebugCecOptionsLogcat_checkBox.isChecked()
        self.__m_bugreportEnable = self.m_mainUi.AmlDebugCecOptionsBugreport_checkBox.isChecked()
        if homeClick:
            self.__nowPullPcTime = curTimeName
            homeCallbackFinish(self.m_moduleId)
        else:
            self.m_mainUi.AmlDebugCecOptions_groupBox.setEnabled(False)
            self.__nowPullPcTime = AmlCommonUtils.pre_create_directory(self.m_moduleId)
            self.__nowPullPcPath = AmlCommonUtils.get_path_by_module(self.__nowPullPcTime, self.m_moduleId)
            if self.__m_logcatEnable:
                AmlCommonUtils.logcat_start()
        self.m_mainUi.AmlDebugCecStop_pushButton.setEnabled(True)

    def stop_capture(self, homeCallbackFinish='', homeClick=False):
        self.log.i('stop_capture')
        self.m_mainUi.AmlDebugCecStop_pushButton.setEnabled(False)
        self.m_mainUi.AmlDebugCecCtrlPanel_groupBox.setEnabled(False)
        self.m_mainUi.AmlDebugCecOptions_groupBox.setEnabled(False)
        if homeClick:
            homeCallbackFinish()
        else:
            thread = Thread(target = self.__stop_capture_thread)
            thread.start()

    def __stop_capture_thread(self):
        if self.__m_logcatEnable:
            AmlCommonUtils.logcat_stop()
            AmlCommonUtils.pull_logcat_to_pc(self.__nowPullPcPath)
        if self.__m_bugreportEnable:
            AmlCommonUtils.bugreport(self.__nowPullPcPath)
        self.m_mainUi.AmlDebugCecStart_pushButton.setEnabled(True)
        self.m_mainUi.AmlDebugCecCtrlPanel_groupBox.setEnabled(True)
        self.m_mainUi.AmlDebugCecOptions_groupBox.setEnabled(True)