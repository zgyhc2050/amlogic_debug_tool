import os
import sys
from pathlib import Path

import res.ico_debug
import Ui_aml_debug

from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from src.common.aml_ini_parser import amlParserIniContainer
from src.common.aml_common_utils import AmlCommonUtils
from src.common.aml_debug_base_ui import AmlDebugModule

class AmlDebugUi(Ui_aml_debug.Ui_MainWindow, QMainWindow):
    terminalLogSignal = pyqtSignal(str)
    def __init__(self):
        super(AmlDebugUi, self).__init__()
        super().setupUi(self)
        AmlDebugModule.initModule(self)
        
        import src.common.aml_common_ui
        self.m_commonUi = src.common.aml_common_ui.instance(self)
        self.m_commonUi.signals_connect_slots()
        self.terminalLogSignal.connect(self.terminalLog)
        AmlCommonUtils.set_log_fuc(self.terminalLogSignal.emit)

    def terminalLog(self, someInfo):
        self.AmlDebugTerminalLog_textBrowser.append(someInfo)
        self.AmlDebugTerminalLog_textBrowser.moveCursor(QTextCursor.End)

    def closeEvent(self,event):
        reply = QMessageBox.question(self, 'Amlogic Tips',"Confirm exit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            AmlDebugModule.closeEvent() 
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if not Path(AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT).exists():
        print(AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT + " folder does not exist, create it.")
        os.makedirs(AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT, 777)
    amlParserIniContainer.initParser()
    ui = AmlDebugUi()
    ui.setWindowIcon(QIcon(AmlCommonUtils.AML_DEBUG_TOOL_ICO_PATH))
    ui.setWindowTitle("Amlogic Debug Tool")
    ui.show()
    sys.exit(app.exec_())
