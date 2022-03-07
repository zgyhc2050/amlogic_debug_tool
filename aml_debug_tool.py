import os, sys
import res.ico_debug
import Ui_aml_debug

from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from src.common.aml_ini_parser import amlParserIniContainer
from res.script.constant import AmlDebugConstant
from src.common.aml_common_utils import AmlCommonUtils
from src.common.aml_debug_base_ui import AmlDebugModule

class AmlDebugUi(Ui_aml_debug.Ui_MainWindow, QMainWindow):
    terminalLogSignal = pyqtSignal(str, str)
    def __init__(self):
        super(AmlDebugUi, self).__init__()
        super().setupUi(self)
        AmlDebugModule.initModule(self)
        
        import src.common.aml_common_ui
        self.m_commonUi = src.common.aml_common_ui.instance(self)
        self.m_commonUi.signals_connect_slots()
        self.terminalLogSignal.connect(self.terminalLog)
        AmlCommonUtils.set_log_fuc(self.terminalLogSignal.emit)

    def terminalLog(self, log, level=AmlCommonUtils.AML_DEBUG_LOG_LEVEL_D):
        log = AmlCommonUtils.get_current_time() + ' ' + level + ' ' + log
        self.AmlDebugTerminalLog_textBrowser.append(log)
        self.AmlDebugTerminalLog_textBrowser.moveCursor(QTextCursor.End)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Amlogic Tips',"Confirm exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            AmlDebugModule.closeEvent() 
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ret = AmlCommonUtils.init()
    if ret != 0:
        exit
    amlParserIniContainer.initParser()
    ui = AmlDebugUi()
    
    ui.setWindowIcon(QIcon(AmlCommonUtils.AML_DEBUG_TOOL_ICO_PATH))
    ui.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)  
    ui.setFixedSize(ui.width(), ui.height())
    ui.setWindowTitle("Amlogic Debug Tool v" + AmlDebugConstant.AML_DEBUG_TOOL_ABOUT_VERSION)
    ui.show()
    ret, version = AmlCommonUtils.check_for_updates()
    if ret == 1:
        reply = QMessageBox.question(ui, 'Online updater', 'There is new version: ' + version + '.\n Update now?  ', 
        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            AmlCommonUtils.update_tool_now()
    sys.exit(app.exec_())
