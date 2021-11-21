from PyQt5.QtGui import QIcon
from Ui_aml_debug_help_info import Ui_AmlDebugHelpAboutInfo_Dialog
from src.common.aml_debug_base_ui import AmlDebugBaseUi
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from res.script.constant import AmlDebugConstant
from src.common.aml_common_utils import AmlCommonUtils
def instance(aml_ui):
    return AmlCommonUi(aml_ui)

########################################################################################################
# "Common UI design"
class AmlCommonUi():
    def __init__(self, aml_ui):
        self.__m_amlUi = aml_ui
        AmlCommonUtils.log_func = aml_ui.terminalLogSignal.emit

    def signals_connect_slots(self):
        self.__m_amlUi.AmlDebug_actionAbout.triggered.connect(self.__click_menu_help_about)

    def init_default_config(self):
        pass

    def init_display_ui(self):
        pass
  
    def closeEvent(self):
        pass

    def __click_menu_help_about(self):
        dialog = AmlDebugHelpAboutInfo_Dialog()
        dialog.show()
        dialog.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.WindowStaysOnTopHint)  
        dialog.setFixedSize(dialog.width(), dialog.height())
        # dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
        dialog.setWindowIcon(QIcon(AmlCommonUtils.AML_DEBUG_TOOL_ICO_PATH))
        dialog.AmlDebugHelpAboutInfo_Label.setText(
            'Version: ' + 'Amlogic Debug Tool ' +AmlDebugConstant.AML_DEBUG_TOOL_ABOUT_VERSION +
            '\nCompile user: ' + AmlDebugConstant.AML_DEBUG_TOOL_ABOUT_USERE + 
            '\nDate: ' + AmlDebugConstant.AML_DEBUG_TOOL_ABOUT_DATE + 
            '\nCommit: ' + AmlDebugConstant.AML_DEBUG_TOOL_ABOUT_COMMIT + 
            '\n晶晨半导体（深圳）有限公司' + 
            '\nCopyright © 2021 . Amlogic(CA)Co., Inc. All Rights Reserved.')
        dialog.exec_()

class AmlDebugHelpAboutInfo_Dialog(Ui_AmlDebugHelpAboutInfo_Dialog, QDialog):
    def __init__(self):
        super(AmlDebugHelpAboutInfo_Dialog, self).__init__()
        super().setupUi(self)
        self.AmlDebugHelpAboutCheckUpdate_pushButton.clicked.connect(self.__check_for_updates)
        self.AmlDebugHelpAboutUpdateNow_pushButton.clicked.connect(self.__update_now)
        self.AmlDebugHelpAboutUpdateNow_pushButton.setVisible(False)
        self.AmlDebugHelpAboutUpdate_Label.setText('')

    def __check_for_updates(self):
        ret, version = AmlCommonUtils.check_for_updates()
        if ret == 1:
            self.AmlDebugHelpAboutUpdate_Label.setText('There is a new version: ' + version)
            self.AmlDebugHelpAboutUpdateNow_pushButton.setVisible(True)
        elif ret == -1:
            self.AmlDebugHelpAboutUpdate_Label.setText('Connect server failed!')
        elif ret == 0:
            self.AmlDebugHelpAboutUpdate_Label.setText('Your software is up to date.')

    def __update_now(self):
        AmlCommonUtils.update_tool_now()