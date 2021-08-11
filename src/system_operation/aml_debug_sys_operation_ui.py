import src.common.aml_common
from src.common.aml_ini_parser import amlParserIniContainer, AmlParserIniBase, AmlParserIniSysOperation
from src.common.aml_common import AmlCommon

########################################################################################################
# Table 2: "System Operation"
class AmlDebugSystemOperationUi():
    def __init__(self, aml_ui):
        self.__m_amlUi = aml_ui
        self.__m_iniPaser = amlParserIniContainer.getParserById(AmlParserIniBase.AML_PARSER_SYS_OPERATION)
        self.__m_amlUi.AmlSystemPushDolbyDtsPush_pushButton.clicked.connect(self.___click_push_dst_dolby)
        self.__m_amlUi.AmlSystemPushMs12Push_pushButton.clicked.connect(self.__click_push_ms12)
        self.__m_amlUi.AmlSystemPushCustomPush_pushButton.clicked.connect(self.__click_push_custom)
        self.__m_amlUi.AmlSystemPushAllPush_pushButton.clicked.connect(self.__click_push_all)
        self.__m_amlUi.AmlSystemRemount_pushButton.clicked.connect(self.__m_amlUi.remount)
        self.__m_amlUi.AmlSystemReboot_pushButton.clicked.connect(self.__m_amlUi.reboot)
        self.__m_amlUi.AmlSystemPullCustom1Pull__pushButton.clicked.connect(self.__click_pull_custom1)
        self.__m_amlUi.AmlSystemPullCustom2Pull2__pushButton.clicked.connect(self.__click_pull_custom2)

        self.__m_amlUi.AmlSystemPushDolbySrc_lineEdit.editingFinished.connect(self.__finished_PushDolbySrc)
        self.__m_amlUi.AmlSystemPushDtsSrc_lineEdit.editingFinished.connect(self.__finished_PushDtsSrc)
        self.__m_amlUi.AmlSystemPushMs12Src_lineEdit.editingFinished.connect(self.__finished_PushMs12Src)
        self.__m_amlUi.AmlSystemPushCustomSrc_lineEdit.editingFinished.connect(self.__finished_PushCustomSrc)
        self.__m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.editingFinished.connect(self.__finished_PushDolbyDtsDst)
        self.__m_amlUi.AmlSystemPushMs12Dst_lineEdit.editingFinished.connect(self.__finished_PushMs12Dst)
        self.__m_amlUi.AmlSystemPushCustomDst_lineEdit.editingFinished.connect(self.__finished_PushCustomDst)
        self.__m_amlUi.AmlSystemPullCustom1Src_lineEdit.editingFinished.connect(self.__finished_PullCustom1Src)
        self.__m_amlUi.AmlSystemPullCustom2Src_lineEdit.editingFinished.connect(self.__finished_PullCustom2Src)
        self.__m_amlUi.AmlSystemPullCustom1Dst_lineEdit.editingFinished.connect(self.__finished_PullCustom1Dst)
        self.__m_amlUi.AmlSystemPullCustom2Dst_lineEdit.editingFinished.connect(self.__finished_PullCustom2Dst)
        self.__init_default_config()

    def __init_default_config(self):
        self.__m_amlUi.AmlSystemPushDolbySrc_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBY_SRC_PATH))
        self.__m_amlUi.AmlSystemPushDtsSrc_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DTS_SRC_PATH))
        self.__m_amlUi.AmlSystemPushMs12Src_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_SRC_PATH))
        self.__m_amlUi.AmlSystemPushCustomSrc_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM_SRC_PATH))
        self.__m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBYDTS_DST_PATH))
        self.__m_amlUi.AmlSystemPushMs12Dst_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_DST_PATH))
        self.__m_amlUi.AmlSystemPushCustomDst_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM_DST_PATH))

        self.__m_amlUi.AmlSystemPullCustom1Src_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM1_SRC_PATH))
        self.__m_amlUi.AmlSystemPullCustom2Src_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM2_SRC_PATH))
        self.__m_amlUi.AmlSystemPullCustom1Dst_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM1_DST_PATH))
        self.__m_amlUi.AmlSystemPullCustom2Dst_lineEdit.setText(self.__m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM2_DST_PATH))


    def __pushFilesToSoc(self, src, dst):
        AmlCommon.exe_adb_cmd('adb push "' + src + '" "' + dst + '"', True, self.__m_amlUi.terminalLog)
    def __pullFilesToSoc(self, src, dst):
        AmlCommon.exe_adb_cmd('adb pull "' + src + '" "' + dst + '"', True, self.__m_amlUi.terminalLog)
        self.__m_amlUi.AmlSystemPushDolbySrc_lineEdit.text()

    def ___click_push_dst_dolby(self):
        self.__pushFilesToSoc(self.__m_amlUi.AmlSystemPushDolbySrc_lineEdit.text() + '\\libHwAudio_dcvdec.so', self.__m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.text())
        self.__pushFilesToSoc(self.__m_amlUi.AmlSystemPushDtsSrc_lineEdit.text() + '\\libHwAudio_dtshd.so', self.__m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.text())
    def __click_push_ms12(self):
        self.__pushFilesToSoc(self.__m_amlUi.AmlSystemPushMs12Src_lineEdit.text() + '\\libdolbyms12.so', self.__m_amlUi.AmlSystemPushMs12Dst_lineEdit.text())
    def __click_push_custom(self):
        self.__pushFilesToSoc(self.__m_amlUi.AmlSystemPushCustomSrc_lineEdit.text(), self.__m_amlUi.AmlSystemPushCustomDst_lineEdit.text())
    def __click_push_all(self):
        self.___click_push_dst_dolby()
        self.__click_push_ms12()
        self.__click_push_custom()
    def __click_pull_custom1(self):
        self.__pullFilesToSoc(self.__m_amlUi.AmlSystemPullCustom1Src_lineEdit.text(), self.__m_amlUi.AmlSystemPullCustom1Dst_lineEdit.text())
    def __click_pull_custom2(self):
        self.__pullFilesToSoc(self.__m_amlUi.AmlSystemPullCustom2Src_lineEdit.text(), self.__m_amlUi.AmlSystemPullCustom2Dst_lineEdit.text())

    def __finished_PushDolbySrc(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBY_SRC_PATH, self.__m_amlUi.AmlSystemPushDolbySrc_lineEdit.text())
    def __finished_PushDtsSrc(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DTS_SRC_PATH, self.__m_amlUi.AmlSystemPushDtsSrc_lineEdit.text())
    def __finished_PushMs12Src(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_SRC_PATH, self.__m_amlUi.AmlSystemPushMs12Src_lineEdit.text())
    def __finished_PushCustomSrc(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM_SRC_PATH, self.__m_amlUi.AmlSystemPushCustomSrc_lineEdit.text())
    def __finished_PushDolbyDtsDst(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBYDTS_DST_PATH, self.__m_amlUi.AmlSystemPushDolbyDtsDst_lineEdit.text())
    def __finished_PushMs12Dst(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_DST_PATH, self.__m_amlUi.AmlSystemPushMs12Dst_lineEdit.text())
    def __finished_PushCustomDst(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM_DST_PATH, self.__m_amlUi.AmlSystemPushCustomDst_lineEdit.text())

    def __finished_PullCustom1Src(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM1_SRC_PATH, self.__m_amlUi.AmlSystemPullCustom1Src_lineEdit.text())
    def __finished_PullCustom2Src(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM2_SRC_PATH, self.__m_amlUi.AmlSystemPullCustom2Src_lineEdit.text())
    def __finished_PullCustom1Dst(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM1_DST_PATH, self.__m_amlUi.AmlSystemPullCustom1Dst_lineEdit.text())
    def __finished_PullCustom2Dst(self):
        self.__m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM2_DST_PATH, self.__m_amlUi.AmlSystemPullCustom2Dst_lineEdit.text())
