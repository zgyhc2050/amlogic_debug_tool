from threading import Thread
from PyQt5 import QtCore, QtWidgets
import time


from src.system_operation.aml_ini_parser_sys_operation import AmlParserIniSysOperation
from src.common.aml_debug_base_ui import AmlDebugBaseUi
from src.common.aml_common_utils import AmlCommonUtils

def instance(aml_ui):
    return AmlDebugSystemOperationUi(aml_ui)

########################################################################################################
# Table: "System Operation"
class AmlDebugSystemOperationUi(AmlDebugBaseUi):
    def __init__(self, aml_ui):
        super(AmlDebugSystemOperationUi, self).__init__(aml_ui, AmlCommonUtils.AML_DEBUG_MODULE_SYS_OPERATION)
        self.__m_stop_thread = False

    def __createUiByType(self, direct):
        if direct == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PUSH:
            button_X = 600
            ITEM_NUM = AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_ITEM_PUSH_NUM
            widget_contents = self.m_mainUi.AmlSystemFilePush_scrollArea_WidgetContents
        elif direct == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PULL:
            button_X = 580
            ITEM_NUM = AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_ITEM_PULL_NUM
            widget_contents = self.m_mainUi.AmlSystemFilePull_scrollArea_WidgetContents
        else:
            print('[__createUiByType] not supported direct:' + direct)
            return
        pull_base_Y_value = 40
        pull_H_value = 30
        for i in range(0, ITEM_NUM):
            var_value = 'self.m_mainUi.AmlSystem' + direct +'TitleCustom_lineEdit' + str(i)
            exec(var_value + '= QtWidgets.QLineEdit(widget_contents)')
            eval(var_value).setGeometry(QtCore.QRect(10, pull_base_Y_value + pull_H_value * i, 61, 21))
            eval(var_value).setAutoFillBackground(False)
            eval(var_value).setStyleSheet("border:none;")
            eval(var_value).setObjectName(var_value)

            var_value = 'self.m_mainUi.AmlSystem' + direct +'CustomSrc_lineEdit' + str(i)
            exec(var_value + '= QtWidgets.QLineEdit(widget_contents)')
            eval(var_value).setGeometry(QtCore.QRect(80, pull_base_Y_value + pull_H_value * i, 311, 21))
            eval(var_value).setAutoFillBackground(False)
            eval(var_value).setObjectName(var_value)

            var_value = 'self.m_mainUi.AmlSystem' + direct +'CustomIco_label' + str(i)
            exec(var_value + '= QtWidgets.QLabel(widget_contents)')
            eval(var_value).setGeometry(QtCore.QRect(400, pull_base_Y_value + pull_H_value * i, 21, 21))
            eval(var_value).setObjectName(var_value)

            var_value = 'self.m_mainUi.AmlSystem' + direct +'CustomDst_lineEdit' + str(i)
            exec(var_value + '= QtWidgets.QLineEdit(widget_contents)')
            eval(var_value).setGeometry(QtCore.QRect(430, pull_base_Y_value + pull_H_value * i, 131, 21))
            eval(var_value).setObjectName(var_value)

            var_value = 'self.m_mainUi.AmlSystem' + direct +'CustomLabel' + str(i)
            exec(var_value + '= QtWidgets.QLabel(widget_contents)')
            eval(var_value).setGeometry(QtCore.QRect(400, pull_base_Y_value + pull_H_value * i, 21, 21))
            _translate = QtCore.QCoreApplication.translate
            eval(var_value).setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:7pt; font-weight:600;\">&gt;</span></p></body></html>"))
            eval(var_value).setObjectName(var_value)

            var_value = 'self.m_mainUi.AmlSystem' + direct +'Custom_Button' + str(i)
            exec(var_value + '= QtWidgets.QPushButton(widget_contents)')
            eval(var_value).setGeometry(QtCore.QRect(button_X, pull_base_Y_value + pull_H_value * i, 61, 23))
            eval(var_value).setObjectName(var_value)
            eval(var_value).setText(direct)

            if direct == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PUSH:
                var_value = 'self.m_mainUi.AmlSystem' + direct +'Custom_checkBox' + str(i)
                exec(var_value + '= QtWidgets.QCheckBox(widget_contents)')
                eval(var_value).setGeometry(QtCore.QRect(570, pull_base_Y_value + pull_H_value * i, 31, 21))
                eval(var_value).setEnabled(True)
                eval(var_value).setChecked(False)
                eval(var_value).setMouseTracking(True)
                eval(var_value).setObjectName(var_value)

    def __displayUiValue(self, direct):
        if direct == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PUSH:
            ITEM_NUM = AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_ITEM_PUSH_NUM
        elif direct == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PULL:
            ITEM_NUM = AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_ITEM_PULL_NUM
        else:
            print('[__displayUiValue] not supported direct:' + direct)
            return
        for i in range(0, ITEM_NUM):
            title_key = self.m_iniPaser.getKeyStrByParam(direct, AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PARAM_TITLE, i)
            src_key = self.m_iniPaser.getKeyStrByParam(direct, AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PARAM_SRC, i)
            dst_key = self.m_iniPaser.getKeyStrByParam(direct, AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PARAM_DST, i)
            eval('self.m_mainUi.AmlSystem' + direct +'TitleCustom_lineEdit' + str(i)).setText(self.m_iniPaser.getValueByKey(title_key))
            eval('self.m_mainUi.AmlSystem' + direct +'CustomSrc_lineEdit' + str(i)).setText(self.m_iniPaser.getValueByKey(src_key))
            eval('self.m_mainUi.AmlSystem' + direct +'CustomDst_lineEdit' + str(i)).setText(self.m_iniPaser.getValueByKey(dst_key))
            if direct == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PUSH:
                check_box_key = self.m_iniPaser.getKeyStrByParam(direct, AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PARAM_CHECK_BOX, i)
                eval('self.m_mainUi.AmlSystem' + direct +'Custom_checkBox' + str(i)).setChecked(self.m_iniPaser.getValueByKey(check_box_key))

    def init_display_ui(self):
        self.__createUiByType(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PUSH)
        self.__createUiByType(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PULL)
        self.__displayUiValue(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PUSH)
        self.__displayUiValue(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PULL)
        self.m_mainUi.AmlSystemPushAll_checkBox.setChecked(self.m_iniPaser.getValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_KEY_PUSH_CUSTOME_ALL))

    def signals_connect_slots(self):
        self.m_mainUi.AmlSystemRemount_Button.clicked.connect(self.__click_remount)
        self.m_mainUi.AmlSystemReboot_Button.clicked.connect(AmlCommonUtils.adb_reboot)
        self.m_mainUi.AmlSystemCloseAvb_Button.clicked.connect(self.__click_close_avb)
        self.m_mainUi.AmlSystemPushAll_checkBox.clicked.connect(self.__click_checkBox_pushCustomAll)
        self.m_mainUi.AmlSystemPushSelect_Button.clicked.connect(self.__click_button_pushCustomSel)
        for i in range(0, AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_ITEM_PUSH_NUM):
            self.__customeConnectSlots(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PUSH, i)
        for i in range(0, AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_ITEM_PULL_NUM):
            self.__customeConnectSlots(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PULL, i)

    def __customeConnectSlots(self, direct, i):
        eval('self.m_mainUi.AmlSystem' + direct +'TitleCustom_lineEdit' + str(i)).editingFinished.connect(lambda: self.__finished_editTitle(direct, i))
        eval('self.m_mainUi.AmlSystem' + direct +'CustomSrc_lineEdit' + str(i)).editingFinished.connect(lambda: self.__finished_editSrc(direct, i))
        eval('self.m_mainUi.AmlSystem' + direct +'CustomDst_lineEdit' + str(i)).editingFinished.connect(lambda: self.__finished_editDst(direct, i))
        if direct == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PUSH:
            eval('self.m_mainUi.AmlSystem' + direct +'Custom_checkBox' + str(i)).stateChanged.connect(lambda: self.__clicked_checkBox(direct, i))
        eval('self.m_mainUi.AmlSystem' + direct +'Custom_Button' + str(i)).clicked.connect(lambda: self.__click_custom(direct, i))

    def __finished_editTitle(self, direct, i):
        title_key = self.m_iniPaser.getKeyStrByParam(direct, AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PARAM_TITLE, i)
        title_value = eval('self.m_mainUi.AmlSystem' + direct +'TitleCustom_lineEdit' + str(i)).text()
        self.m_iniPaser.setValueByKey(title_key, title_value)

    def __finished_editSrc(self, direct, i):
        title_key = self.m_iniPaser.getKeyStrByParam(direct, AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PARAM_SRC, i)
        title_value = eval('self.m_mainUi.AmlSystem' + direct +'CustomSrc_lineEdit' + str(i)).text()
        self.m_iniPaser.setValueByKey(title_key, title_value)
    def __finished_editDst(self, direct, i):
        title_key = self.m_iniPaser.getKeyStrByParam(direct, AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PARAM_DST, i)
        title_value = eval('self.m_mainUi.AmlSystem' + direct +'CustomDst_lineEdit' + str(i)).text()
        self.m_iniPaser.setValueByKey(title_key, title_value)
    def __clicked_checkBox(self, direct, i):
        title_key = self.m_iniPaser.getKeyStrByParam(direct, AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PARAM_CHECK_BOX, i)
        title_value = eval('self.m_mainUi.AmlSystem' + direct +'Custom_checkBox' + str(i)).isChecked()
        self.m_iniPaser.setValueByKey(title_key, title_value)
    def __click_custom(self, direct, i):
        # print('[__click_custom] direct:' + direct + ', i:' + str(i))
        src_value = eval('self.m_mainUi.AmlSystem' + direct +'CustomSrc_lineEdit' + str(i)).text()
        dst_value = eval('self.m_mainUi.AmlSystem' + direct +'CustomDst_lineEdit' + str(i)).text()
        self.__adbProcFiles(direct, src_value, dst_value)
    def __click_button_pushCustomSel(self):
        for i in range(0, AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_ITEM_PUSH_NUM):
            selected = eval('self.m_mainUi.AmlSystem' + AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PUSH +'Custom_checkBox' + str(i)).isChecked()
            if selected:
                var_value = 'self.m_mainUi.AmlSystem' + AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PUSH +'Custom_Button' + str(i)
                eval(var_value).click()

    def __click_checkBox_pushCustomAll(self):
        allCheckValue = self.m_mainUi.AmlSystemPushAll_checkBox.isChecked()
        for i in range(0, AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_ITEM_PUSH_NUM):
            eval('self.m_mainUi.AmlSystem' + AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PUSH +'Custom_checkBox' + str(i)).setChecked(allCheckValue)
        self.m_iniPaser.setValueByKey(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_KEY_PUSH_CUSTOME_ALL, allCheckValue)

    def closeEvent(self):
        self.__m_stop_thread = True

    def __adbProcFiles(self, direct, src, dst):
        if direct == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PUSH:
            opt = 'push'
        elif direct == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PULL:
            opt = 'pull'
        else:
            self.log.w('[__adbProcFiles] not supported direct:' + direct)
            return
        AmlCommonUtils.exe_adb_cmd(opt + ' "' + src + '" "' + dst + '"', True)

    def __click_remount(self):
        AmlCommonUtils.adb_root()
        AmlCommonUtils.adb_remount()

    def __click_close_avb(self):
        self.m_mainUi.AmlSystemCloseAvb_Button.setEnabled(False)
        thread = Thread(target = self.__closeAvbProc)
        thread.start()

    def __closeAvbProc(self):
        AmlCommonUtils.exe_adb_cmd('reboot bootloader', True)
        AmlCommonUtils.exe_sys_cmd('fastboot flashing unlock_critical', True)
        AmlCommonUtils.exe_sys_cmd('fastboot flashing unlock', True)
        AmlCommonUtils.exe_sys_cmd('fastboot reboot', True)
        timeCntS = 60
        self.log.d('__closeAvbProc: flashing unlock reboot platform, please wait ' + str(timeCntS) + ' s...')
        while timeCntS > 0 and self.__m_stop_thread == False: 
            time.sleep(1)
            timeCntS -= 1
        AmlCommonUtils.adb_root()
        AmlCommonUtils.exe_adb_cmd('disable-verity', True)
        AmlCommonUtils.adb_reboot()
        timeCntS = 60
        self.log.d('__closeAvbProc: disable-verity reboot platform, please wait ' + str(timeCntS) + ' s...')
        while timeCntS > 0 and self.__m_stop_thread == False: 
            time.sleep(1)
            timeCntS -= 1
        AmlCommonUtils.adb_root()
        AmlCommonUtils.adb_remount()
        AmlCommonUtils.adb_reboot()
        self.m_mainUi.AmlSystemCloseAvb_Button.setEnabled(True)
