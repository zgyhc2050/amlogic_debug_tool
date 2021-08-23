from threading import Thread
import time

from src.system_operation.aml_ini_parser_sys_operation import AmlParserIniSysOperation
from src.common.aml_ini_parser import amlParserIniContainer, AmlParserIniManager
from src.common.aml_debug_base_ui import AmlDebugBaseUi
from src.common.aml_common import AmlCommon

def instance(aml_ui):
    return AmlDebugSystemOperationUi(aml_ui)

########################################################################################################
# Table 2: "System Operation"
class AmlDebugSystemOperationUi(AmlDebugBaseUi):
    def __init__(self, aml_ui):
        self.__m_iniPaser = amlParserIniContainer.getParserById(AmlParserIniManager.AML_PARSER_SECTION_SYS_OPERATION)
        super(AmlDebugSystemOperationUi, self).__init__(aml_ui)
        self.__m_stop_thread = False

    def signals_connect_slots(self):
        self.m_amlUi.AmlSystemPushDolbyDtsPush_pushButton.clicked.connect(self.__click_push_dst_dolby)
        self.m_amlUi.AmlSystemPushMs12Push_pushButton.clicked.connect(self.__click_push_ms12)
        self.m_amlUi.AmlSystemPushCustomPush_pushButton.clicked.connect(self.__click_push_custom)
        self.m_amlUi.AmlSystemPushAllPush_pushButton.clicked.connect(self.__click_push_all)
        self.m_amlUi.AmlSystemRemount_pushButton.clicked.connect(self.m_amlUi.remount)
        self.m_amlUi.AmlSystemReboot_pushButton.clicked.connect(self.m_amlUi.reboot)
        self.m_amlUi.AmlSystemCloseAvb_pushButton.clicked.connect(self.__click_close_avb)
        self.m_amlUi.AmlSystemPullCustom1Pull__pushButton.clicked.connect(self.__click_pull_custom1)
        self.m_amlUi.AmlSystemPullCustom2Pull2__pushButton.clicked.connect(self.__click_pull_custom2)
        self.m_amlUi.AmlSystemPushDolbySrc_lineEdit.editingFinished.connect(self.__finished_PushDolbySrc)
        self.m_amlUi.AmlSystemPushDtsSrc_lineEdit.editingFinished.connect(self.__finished_PushDtsSrc)
        self.m_amlUi.AmlSystemPushMs12Src_lineEdit.editingFinished.connect(self.__finished_PushMs12Src)
        self.m_amlUi.AmlSystemPushCustomSrc_lineEdit.editingFinished.connect(self.__finished_PushCustomSrc)
        self.m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.editingFinished.connect(self.__finished_PushDolbyDtsDst)
        self.m_amlUi.AmlSystemPushMs12Dst_lineEdit.editingFinished.connect(self.__finished_PushMs12Dst)
        self.m_amlUi.AmlSystemPushCustomDst_lineEdit.editingFinished.connect(self.__finished_PushCustomDst)
        self.m_amlUi.AmlSystemPullCustom1Src_lineEdit.editingFinished.connect(self.__finished_PullCustom1Src)
        self.m_amlUi.AmlSystemPullCustom2Src_lineEdit.editingFinished.connect(self.__finished_PullCustom2Src)
        self.m_amlUi.AmlSystemPullCustom1Dst_lineEdit.editingFinished.connect(self.__finished_PullCustom1Dst)
        self.m_amlUi.AmlSystemPullCustom2Dst_lineEdit.editingFinished.connect(self.__finished_PullCustom2Dst)

    def init_default_config(self):
        pass

    def init_display_ui(self):
        self.m_amlUi.AmlSystemPushDolbySrc_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBY_SRC_PATH))
        self.m_amlUi.AmlSystemPushDtsSrc_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DTS_SRC_PATH))
        self.m_amlUi.AmlSystemPushMs12Src_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_SRC_PATH))
        self.m_amlUi.AmlSystemPushCustomSrc_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM_SRC_PATH))
        self.m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBYDTS_DST_PATH))
        self.m_amlUi.AmlSystemPushMs12Dst_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_DST_PATH))
        self.m_amlUi.AmlSystemPushCustomDst_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM_DST_PATH))
        self.m_amlUi.AmlSystemPullCustom1Src_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM1_SRC_PATH))
        self.m_amlUi.AmlSystemPullCustom2Src_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM2_SRC_PATH))
        self.m_amlUi.AmlSystemPullCustom1Dst_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM1_DST_PATH))
        self.m_amlUi.AmlSystemPullCustom2Dst_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM2_DST_PATH))

    def closeEvent(self):
        self.__m_stop_thread = True

    def __pushFilesToSoc(self, src, dst):
        AmlCommon.exe_adb_cmd('adb push "' + src + '" "' + dst + '"', True, self.m_amlUi.terminalLog)
    def __pullFilesToSoc(self, src, dst):
        AmlCommon.exe_adb_cmd('adb pull "' + src + '" "' + dst + '"', True, self.m_amlUi.terminalLog)
        self.m_amlUi.AmlSystemPushDolbySrc_lineEdit.text()

    def __click_push_dst_dolby(self):
        self.__pushFilesToSoc(self.m_amlUi.AmlSystemPushDolbySrc_lineEdit.text() + '\\libHwAudio_dcvdec.so', self.m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.text())
        self.__pushFilesToSoc(self.m_amlUi.AmlSystemPushDtsSrc_lineEdit.text() + '\\libHwAudio_dtshd.so', self.m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.text())
    def __click_push_ms12(self):
        self.__pushFilesToSoc(self.m_amlUi.AmlSystemPushMs12Src_lineEdit.text() + '\\libdolbyms12.so', self.m_amlUi.AmlSystemPushMs12Dst_lineEdit.text())
    def __click_push_custom(self):
        self.__pushFilesToSoc(self.m_amlUi.AmlSystemPushCustomSrc_lineEdit.text(), self.m_amlUi.AmlSystemPushCustomDst_lineEdit.text())
    def __click_push_all(self):
        self.__click_push_dst_dolby()
        self.__click_push_ms12()
        self.__click_push_custom()
    def __click_pull_custom1(self):
        self.__pullFilesToSoc(self.m_amlUi.AmlSystemPullCustom1Src_lineEdit.text(), self.m_amlUi.AmlSystemPullCustom1Dst_lineEdit.text())
    def __click_pull_custom2(self):
        self.__pullFilesToSoc(self.m_amlUi.AmlSystemPullCustom2Src_lineEdit.text(), self.m_amlUi.AmlSystemPullCustom2Dst_lineEdit.text())

    def __click_close_avb(self):
        self.m_amlUi.AmlSystemCloseAvb_pushButton.setEnabled(False)
        thread = Thread(target = self.__closeAvbProc)
        thread.start()

    def __closeAvbProc(self):
        AmlCommon.exe_sys_cmd('adb reboot bootloader', True, self.m_amlUi.terminalLog)
        AmlCommon.exe_sys_cmd('fastboot flashing unlock_critical', True, self.m_amlUi.terminalLog)
        AmlCommon.exe_sys_cmd('fastboot flashing unlock', True, self.m_amlUi.terminalLog)
        AmlCommon.exe_sys_cmd('fastboot reboot', True, self.m_amlUi.terminalLog)
        timeCntS = 40
        self.m_amlUi.terminalLog('__closeAvbProc: flashing unlock reboot platform, please wait ' + str(timeCntS) + ' s...')
        while timeCntS > 0 and self.__m_stop_thread == False: 
            time.sleep(1)
            timeCntS -= 1
        AmlCommon.exe_sys_cmd('adb root', True, self.m_amlUi.terminalLog)
        AmlCommon.exe_sys_cmd('adb disable-verity', True, self.m_amlUi.terminalLog)
        AmlCommon.exe_sys_cmd('adb reboot', True, self.m_amlUi.terminalLog)
        timeCntS = 30
        self.m_amlUi.terminalLog('__closeAvbProc: disable-verity reboot platform, please wait ' + str(timeCntS) + ' s...')
        while timeCntS > 0 and self.__m_stop_thread == False: 
            time.sleep(1)
            timeCntS -= 1
        self.m_amlUi.remount()
        self.m_amlUi.AmlSystemCloseAvb_pushButton.setEnabled(True)

    def __finished_PushDolbySrc(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBY_SRC_PATH, self.m_amlUi.AmlSystemPushDolbySrc_lineEdit.text())
    def __finished_PushDtsSrc(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DTS_SRC_PATH, self.m_amlUi.AmlSystemPushDtsSrc_lineEdit.text())
    def __finished_PushMs12Src(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_SRC_PATH, self.m_amlUi.AmlSystemPushMs12Src_lineEdit.text())
    def __finished_PushCustomSrc(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM_SRC_PATH, self.m_amlUi.AmlSystemPushCustomSrc_lineEdit.text())
    def __finished_PushDolbyDtsDst(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBYDTS_DST_PATH, self.m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.text())
    def __finished_PushMs12Dst(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_DST_PATH, self.m_amlUi.AmlSystemPushMs12Dst_lineEdit.text())
    def __finished_PushCustomDst(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM_DST_PATH, self.m_amlUi.AmlSystemPushCustomDst_lineEdit.text())

    def __finished_PullCustom1Src(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM1_SRC_PATH, self.m_amlUi.AmlSystemPullCustom1Src_lineEdit.text())
    def __finished_PullCustom2Src(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM2_SRC_PATH, self.m_amlUi.AmlSystemPullCustom2Src_lineEdit.text())
    def __finished_PullCustom1Dst(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM1_DST_PATH, self.m_amlUi.AmlSystemPullCustom1Dst_lineEdit.text())
    def __finished_PullCustom2Dst(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM2_DST_PATH, self.m_amlUi.AmlSystemPullCustom2Dst_lineEdit.text())
