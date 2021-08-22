import os
import sys
from pathlib import Path
from threading import Thread

import res.ico_debug
import Ui_aml_debug

from PyQt5.QtGui import QTextCursor, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from src.common.aml_ini_parser import amlParserIniContainer
from src.common.aml_common import AmlCommon
from src.common.aml_debug_base_ui import AmlDebugModule


class AmlDebugUi(Ui_aml_debug.Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(AmlDebugUi, self).__init__()
        super().setupUi(self)
        AmlDebugModule.initModule(self)

    def terminalLog(self, someInfo):
        self.AmlAudioTerminalLog_textBrowser.append(someInfo)
        self.AmlAudioTerminalLog_textBrowser.moveCursor(QTextCursor.End)

    def remount(self):
        AmlCommon.exe_adb_cmd('adb root', True, self.terminalLog)
        return AmlCommon.exe_adb_cmd('adb remount', True, self.terminalLog)

    def reboot(self):
        AmlCommon.exe_adb_cmd('adb reboot', True, self.terminalLog)

    def closeEvent(self,event):
        reply = QMessageBox.question(self, 'Amlogic Tips',"Confirm exit?", QMessageBox.Yes |QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
            AmlDebugModule.closeEvent()
        else:
            event.ignore()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    if not Path(AmlCommon.AML_DEBUG_DIRECOTRY_ROOT).exists():
        print(AmlCommon.AML_DEBUG_DIRECOTRY_ROOT + " folder does not exist, create it.")
        os.makedirs(AmlCommon.AML_DEBUG_DIRECOTRY_ROOT, 777)
    amlParserIniContainer.initParser()

    ui = AmlDebugUi()
    ui.setWindowIcon(QIcon(':/debug.ico'))
    ui.setWindowTitle("Amlogic Debug Tool")
    ui.show()
    sys.exit(app.exec_())
