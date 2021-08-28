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

    def init_display_ui(self):
        self.m_amlUi.AmlSystemPushDolbySrc_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBY_SRC_PATH))
        self.m_amlUi.AmlSystemPushDtsSrc_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DTS_SRC_PATH))
        self.m_amlUi.AmlSystemPushMs12Src_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_SRC_PATH))
        self.m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBYDTS_DST_PATH))
        self.m_amlUi.AmlSystemPushMs12Dst_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_DST_PATH))
        for i in range(1, 6):
            eval('self.m_amlUi.AmlSystemPushCustom' + str(i) + 'Src_lineEdit').\
            setText(self.__m_iniPaser.getValueByKey(eval('AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM' + str(i) + '_SRC_PATH')))
            eval('self.m_amlUi.AmlSystemPushCustom' + str(i) + 'Dst_lineEdit').\
            setText(self.__m_iniPaser.getValueByKey(eval('AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM' + str(i) + '_DST_PATH')))
        for i in range(1, 5):
            eval('self.m_amlUi.AmlSystemPullCustom' + str(i) + 'Src_lineEdit').\
            setText(self.__m_iniPaser.getValueByKey(eval('AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM' + str(i) + '_SRC_PATH')))
            eval('self.m_amlUi.AmlSystemPullCustom' + str(i) + 'Dst_lineEdit').\
            setText(self.__m_iniPaser.getValueByKey(eval('AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM' + str(i) + '_DST_PATH')))

    def signals_connect_slots(self):
        self.m_amlUi.AmlSystemPushDolbyDtsPush_Button.clicked.connect(self.__click_push_dst_dolby)
        self.m_amlUi.AmlSystemPushMs12Push_Button.clicked.connect(self.__click_push_ms12)
        self.m_amlUi.AmlSystemRemount_Button.clicked.connect(self.m_amlUi.remount)
        self.m_amlUi.AmlSystemReboot_Button.clicked.connect(self.m_amlUi.reboot)
        self.m_amlUi.AmlSystemCloseAvb_Button.clicked.connect(self.__click_close_avb)
        self.m_amlUi.AmlSystemPushDolbySrc_lineEdit.editingFinished.connect(self.__finished_PushDolbySrc)
        self.m_amlUi.AmlSystemPushDtsSrc_lineEdit.editingFinished.connect(self.__finished_PushDtsSrc)
        self.m_amlUi.AmlSystemPushMs12Src_lineEdit.editingFinished.connect(self.__finished_PushMs12Src)
        self.m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.editingFinished.connect(self.__finished_PushDolbyDtsDst)
        self.m_amlUi.AmlSystemPushMs12Dst_lineEdit.editingFinished.connect(self.__finished_PushMs12Dst)
        for i in range(1, 6):
            eval('self.m_amlUi.AmlSystemPushCustom' + str(i) + 'Src_lineEdit').editingFinished.connect(eval('self.finished_PushCustom' + str(i) + 'Src'))
            eval('self.m_amlUi.AmlSystemPushCustom' + str(i) + 'Dst_lineEdit').editingFinished.connect(eval('self.finished_PushCustom' + str(i) + 'Dst'))
            eval('self.m_amlUi.AmlSystemPushCustom' + str(i) + 'Push_Button').clicked.connect(eval('self.click_push_custom' + str(i)))
        for i in range(1, 5):
            eval('self.m_amlUi.AmlSystemPullCustom' + str(i) + 'Src_lineEdit').editingFinished.connect(eval('self.finished_PullCustom' + str(i) + 'Src'))
            eval('self.m_amlUi.AmlSystemPullCustom' + str(i) + 'Dst_lineEdit').editingFinished.connect(eval('self.finished_PullCustom' + str(i) + 'Dst'))
            eval('self.m_amlUi.AmlSystemPullCustom' + str(i) + 'Pull_Button').clicked.connect(eval('self.click_pull_custom' + str(i)))

    def closeEvent(self):
        self.__m_stop_thread = True

    def __pushFilesToSoc(self, src, dst):
        AmlCommon.exe_adb_cmd('adb push "' + src + '" "' + dst + '"', True)
    def __pullFilesToSoc(self, src, dst):
        AmlCommon.exe_adb_cmd('adb pull "' + src + '" "' + dst + '"', True)
        self.m_amlUi.AmlSystemPushDolbySrc_lineEdit.text()

    def __click_push_dst_dolby(self):
        self.__pushFilesToSoc(self.m_amlUi.AmlSystemPushDolbySrc_lineEdit.text() + '\\libHwAudio_dcvdec.so', self.m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.text())
        self.__pushFilesToSoc(self.m_amlUi.AmlSystemPushDtsSrc_lineEdit.text() + '\\libHwAudio_dtshd.so', self.m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.text())
    def __click_push_ms12(self):
        self.__pushFilesToSoc(self.m_amlUi.AmlSystemPushMs12Src_lineEdit.text() + '\\libdolbyms12.so', self.m_amlUi.AmlSystemPushMs12Dst_lineEdit.text())

    def __click_push_custom(self, i):
        self.__pushFilesToSoc(eval('self.m_amlUi.AmlSystemPushCustom' + str(i) + 'Src_lineEdit').text(), eval('self.m_amlUi.AmlSystemPushCustom' + str(i) + 'Dst_lineEdit').text())
    def click_push_custom1(self):
        self.__click_push_custom(1)
    def click_push_custom2(self):
        self.__click_push_custom(2)
    def click_push_custom3(self):
        self.__click_push_custom(3)
    def click_push_custom4(self):
        self.__click_push_custom(4)
    def click_push_custom5(self):
        self.__click_push_custom(5)

    def __click_pull_custom(self, i):
        self.__pullFilesToSoc(eval('self.m_amlUi.AmlSystemPullCustom' + str(i) + 'Src_lineEdit').text(), eval('self.m_amlUi.AmlSystemPullCustom' + str(i) + 'Dst_lineEdit').text())
    def click_pull_custom1(self):
        self.__click_pull_custom(1)
    def click_pull_custom2(self):
        self.__click_pull_custom(2)
    def click_pull_custom3(self):
        self.__click_pull_custom(3)
    def click_pull_custom4(self):
        self.__click_pull_custom(4)

    def __click_close_avb(self):
        self.m_amlUi.AmlSystemCloseAvb_Button.setEnabled(False)
        thread = Thread(target = self.__closeAvbProc)
        thread.start()

    def __closeAvbProc(self):
        AmlCommon.exe_sys_cmd('adb reboot bootloader', True)
        AmlCommon.exe_sys_cmd('fastboot flashing unlock_critical', True)
        AmlCommon.exe_sys_cmd('fastboot flashing unlock', True)
        AmlCommon.exe_sys_cmd('fastboot reboot', True)
        timeCntS = 40
        self.log_fuc('__closeAvbProc: flashing unlock reboot platform, please wait ' + str(timeCntS) + ' s...')
        while timeCntS > 0 and self.__m_stop_thread == False: 
            time.sleep(1)
            timeCntS -= 1
        AmlCommon.exe_sys_cmd('adb root', True)
        AmlCommon.exe_sys_cmd('adb disable-verity', True)
        AmlCommon.exe_sys_cmd('adb reboot', True)
        timeCntS = 40
        self.log_fuc('__closeAvbProc: disable-verity reboot platform, please wait ' + str(timeCntS) + ' s...')
        while timeCntS > 0 and self.__m_stop_thread == False: 
            time.sleep(1)
            timeCntS -= 1
        self.m_amlUi.remount()
        self.m_amlUi.AmlSystemCloseAvb_Button.setEnabled(True)

    def __finished_PushDolbySrc(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBY_SRC_PATH, self.m_amlUi.AmlSystemPushDolbySrc_lineEdit.text())
    def __finished_PushDtsSrc(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DTS_SRC_PATH, self.m_amlUi.AmlSystemPushDtsSrc_lineEdit.text())
    def __finished_PushMs12Src(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_SRC_PATH, self.m_amlUi.AmlSystemPushMs12Src_lineEdit.text())

    def __finished_PushDolbyDtsDst(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBYDTS_DST_PATH, self.m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.text())
    def __finished_PushMs12Dst(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_DST_PATH, self.m_amlUi.AmlSystemPushMs12Dst_lineEdit.text())

    def __finished_PushCustomSrc(self, i):
        self.__m_iniPaser.setValueByKey(eval('AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM' + str(i) + '_SRC_PATH'),\
        eval('self.m_amlUi.AmlSystemPushCustom' + str(i) + 'Src_lineEdit').text())
    def finished_PushCustom1Src(self):
        self.__finished_PushCustomSrc(1)
    def finished_PushCustom2Src(self):
        self.__finished_PushCustomSrc(2)
    def finished_PushCustom3Src(self):
        self.__finished_PushCustomSrc(3)
    def finished_PushCustom4Src(self):
        self.__finished_PushCustomSrc(4)
    def finished_PushCustom5Src(self):
        self.__finished_PushCustomSrc(5)

    def __finished_PushCustomDst(self, i):
        self.__m_iniPaser.setValueByKey(eval('AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM' + str(i) + '_DST_PATH'),\
        eval('self.m_amlUi.AmlSystemPushCustom' + str(i) + 'Dst_lineEdit').text())
    def finished_PushCustom1Dst(self):
        self.__finished_PushCustomDst(1)
    def finished_PushCustom2Dst(self):
        self.__finished_PushCustomDst(2)
    def finished_PushCustom3Dst(self):
        self.__finished_PushCustomDst(3)
    def finished_PushCustom4Dst(self):
        self.__finished_PushCustomDst(4)
    def finished_PushCustom5Dst(self):
        self.__finished_PushCustomDst(5)

    def __finished_PullCustomSrc(self, i):
        self.__m_iniPaser.setValueByKey(eval('AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM' + str(i) + '_SRC_PATH'),\
        eval('self.m_amlUi.AmlSystemPullCustom' + str(i) + 'Src_lineEdit').text())
    def finished_PullCustom1Src(self):
        self.__finished_PullCustomSrc(1)
    def finished_PullCustom2Src(self):
        self.__finished_PullCustomSrc(2)
    def finished_PullCustom3Src(self):
        self.__finished_PullCustomSrc(3)
    def finished_PullCustom4Src(self):
        self.__finished_PullCustomSrc(4)

    def __finished_PullCustomDst(self, i):
        self.__m_iniPaser.setValueByKey(eval('AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM' + str(i) + '_DST_PATH'),\
        eval('self.m_amlUi.AmlSystemPullCustom' + str(i) + 'Dst_lineEdit').text())
    def finished_PullCustom1Dst(self):
        self.__finished_PullCustomDst(1)
    def finished_PullCustom2Dst(self):
        self.__finished_PullCustomDst(2)
    def finished_PullCustom3Dst(self):
        self.__finished_PullCustomDst(3)
    def finished_PullCustom4Dst(self):
        self.__finished_PullCustomDst(4)
