import os
import sys
from pathlib import Path
from threading import Thread

import res.ico_debug
import Ui_aml_debug

from PyQt5.QtGui import QTextCursor, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow

from src.audio.aml_debug_audio_ui import AmlDebugAudioDebugUi
from src.system_operation.aml_debug_sys_operation_ui import AmlDebugSystemOperationUi
from src.common.aml_ini_parser import amlParserIniContainer
from src.common.aml_common import AmlCommon

class AmlDebugUi(Ui_aml_debug.Ui_MainWindow):
    def __init__(self, mainWindow):
        super().setupUi(mainWindow)
        self.__m_amlDebugAudioDebugUi = AmlDebugAudioDebugUi(self)
        self.__m_amlDebugSystemOperationUi = AmlDebugSystemOperationUi(self)

    def terminalLog(self, someInfo):
        self.AmlAudioTerminalLog_textBrowser.append(someInfo)
        self.AmlAudioTerminalLog_textBrowser.moveCursor(QTextCursor.End)

    def remount(self):
        AmlCommon.exe_adb_cmd('adb root', True, self.terminalLog)
        return AmlCommon.exe_adb_cmd('adb remount', True, self.terminalLog)

    def reboot(self):
        AmlCommon.exe_adb_cmd('adb reboot', True, self.terminalLog)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    MainWindow.setWindowIcon(QIcon(':/debug.ico'))
    if not Path(AmlCommon.AML_DEBUG_DIRECOTRY_ROOT).exists():
        print(AmlCommon.AML_DEBUG_DIRECOTRY_ROOT + " folder does not exist, create it.")
        os.makedirs(AmlCommon.AML_DEBUG_DIRECOTRY_ROOT, 777)
    amlParserIniContainer.initParser()

    ui = AmlDebugUi(MainWindow)
    MainWindow.setWindowTitle("Amlogic Debug Tool")

    MainWindow.show()
    sys.exit(app.exec_())
