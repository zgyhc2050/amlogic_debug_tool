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
        dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
        dialog.setWindowIcon(QIcon(AmlCommonUtils.AML_DEBUG_TOOL_ICO_PATH))
        dialog.AmlDebugHelpAboutInfo_Label.setText(
            'Version: ' + AmlDebugConstant.AML_DEBUG_TOOL_ABOUT_VERSION +
            '\nCompile user: ' + AmlDebugConstant.AML_DEBUG_TOOL_ABOUT_USERE + 
            '\nDate: ' + AmlDebugConstant.AML_DEBUG_TOOL_ABOUT_DATE + 
            '\nCommit: ' + AmlDebugConstant.AML_DEBUG_TOOL_ABOUT_COMMIT)
        dialog.exec_()

class AmlDebugHelpAboutInfo_Dialog(Ui_AmlDebugHelpAboutInfo_Dialog, QDialog):
    def __init__(self):
        super(AmlDebugHelpAboutInfo_Dialog, self).__init__()
        super().setupUi(self)
