from threading import Thread
import time

from src.system_operation.aml_ini_parser_sys_operation import AmlParserIniSysOperation
from src.common.aml_ini_parser import amlParserIniContainer, AmlParserIniManager
from src.common.aml_debug_base_ui import AmlDebugBaseUi
from src.common.aml_common import AmlCommon

def instance(aml_ui):
    return AmlDebugCecUi(aml_ui)

########################################################################################################
# Table: "CEC"
class AmlDebugCecUi(AmlDebugBaseUi):
    def __init__(self, aml_ui):
        self.__m_amlUi = aml_ui
        self.moduleName = AmlParserIniManager.AML_PARSER_SECTION_CEC
        self.__m_iniPaser = amlParserIniContainer.getParserById(AmlParserIniManager.AML_PARSER_SECTION_CEC)
        super(AmlDebugCecUi, self).__init__(aml_ui)
        self.__m_stop_thread = False
        self.__adbSetDebugPropList = [
            'echo log.tag.AudioService=DEBUG >> vendor/build.prop',
            'echo log.tag.volume=DEBUG >> vendor/build.prop',
            'echo log.tag.HDMI=DEBUG >> vendor/build.prop',
        ]

    def signals_connect_slots(self):
        self.__m_amlUi.AmlDebugCecSetprop_pushButton.clicked.connect(self.__click_setprop)
        self.__m_amlUi.AmlDebugCecStart_pushButton.clicked.connect(self.__click_start_capture)

    def init_default_config(self):
        pass

    def init_display_ui(self):
        self.__m_amlUi.AmlSystemPushDolbySrc_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBY_SRC_PATH))

    def closeEvent(self):
        pass

    def __click_setprop(self):
        for cmd in self.__adbSetDebugPropList:
            AmlCommon.exe_adb_cmd(cmd)
            self.__m_amlUi.reboot()

    def __click_start_capture(self, src, dst):
        AmlCommon.exe_adb_cmd('adb pull "' + src + '" "' + dst + '"', True, self.__m_amlUi.terminalLog)
