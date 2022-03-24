from PyQt5.QtCore import *
from threading import Thread

from src.common.aml_debug_base_ui import AmlDebugBaseUi
from src.common.aml_common_utils import AmlCommonUtils
from src.burn.aml_ini_parser_burn import AmlParserIniBurn

from src.burn.aml_debug_burn import AmlDebugBurn

def instance(aml_ui):
    return AmlDebugBurnUi(aml_ui)

########################################################################################################
# Table: "Burn"
class AmlDebugBurnUi(AmlDebugBaseUi):
    setCurProcessFormatSignal = pyqtSignal(str)
    setCurProcessMaxValueSignal = pyqtSignal(int)
    setCurProcessSignal = pyqtSignal(int)
    def __init__(self, aml_ui):
        self.dbBurnSelect = AmlDebugBurn.AML_BURN_SAVE_FILE_ENUM_SAVE_ALL
        self.__isBurning = False
        super(AmlDebugBurnUi, self).__init__(aml_ui, AmlCommonUtils.AML_DEBUG_MODULE_BURN)
        self.__burn = AmlDebugBurn(self)

    def init_display_ui(self):
        self.m_mainUi.AmlDebugBurnTips_label.setOpenExternalLinks(True)
        items = [AmlDebugBurn.AML_BURN_SAVE_FILE_ENUM_SAVE_ALL, 
                AmlDebugBurn.AML_BURN_SAVE_FILE_ENUM_SAVE_LATEST, AmlDebugBurn.AML_BURN_SAVE_FILE_ENUM_DELETE_ALL]
        self.m_mainUi.AmlDebugBurnSelect_comboBox.addItems(items)
        self.dbBurnSelect = self.m_iniPaser.getValueByKey(AmlParserIniBurn.AML_PARSER_BURN_FILE_SAVE_OPTION)
        print('bur sel:' + self.dbBurnSelect)
        self.m_mainUi.AmlDebugBurnSelect_comboBox.setCurrentText(self.dbBurnSelect)

    def signals_connect_slots(self):
        self.m_mainUi.AmlDebugBurnStart_pushButton.clicked.connect(self.__click_burnToggle)
        self.m_mainUi.AmlDebugBurnSelect_comboBox.currentTextChanged.connect(self.__textChanged_selectSaveFileMode)
        self.m_mainUi.AmlDebugBurnOpenBurDir_pushButton.clicked.connect(self.__click_openBurnDir)

    def closeEvent(self):
        pass

    def __click_burnToggle(self):
        if self.__isBurning == False:
            url = self.m_mainUi.AmlDebugBurnUrl_lineEdit.text()
            self.m_mainUi.AmlDebugBurnStart_pushButton.setText('Stop')
            print('__click_burnToggle sel:' + self.dbBurnSelect)
            self.thread = self.__burn.initBurn(url, self.dbBurnSelect)
            self.thread.burnSetCurButtonStatusSignal.connect(self.signalSetButtonStatus)
            self.thread.burnSetCurProcessFormatSignal.connect(self.signalSetCurProcessFormat)
            self.thread.burnSetCurProcessMaxValueSignal.connect(self.signalSetCurProcessMaxValue)
            self.thread.burnSetCurProcessSignal.connect(self.signalSetCurProcess)
            self.thread.burnSetRefreshcurStatusSignal.connect(self.signalRefreshcurStatus)
            self.__burn.startBurn()
        else:
            self.__burn.stopBurn()
            self.m_mainUi.AmlDebugBurnStart_pushButton.setText('Start')
            self.signalSetCurProcessFormat('%p%')
            self.signalSetCurProcessMaxValue(100)
            self.signalSetCurProcess(0)
            self.signalRefreshcurStatus('')
        self.__isBurning = bool(1 - self.__isBurning)

    def __click_openBurnDir(self):
        self.__burn.openBurnDir()

    def __textChanged_selectSaveFileMode(self):
        self.dbBurnSelect = self.m_mainUi.AmlDebugBurnSelect_comboBox.currentText()
        self.m_iniPaser.setValueByKey(AmlParserIniBurn.AML_PARSER_BURN_FILE_SAVE_OPTION, self.dbBurnSelect)

    def signalSetCurProcessFormat(self, value):
        self.m_mainUi.AmlDebugBurn_progressBar.setFormat(value)
    def signalSetCurProcessMaxValue(self, value):
        self.m_mainUi.AmlDebugBurn_progressBar.setMaximum(value)
    def signalSetCurProcess(self, value):
        self.m_mainUi.AmlDebugBurn_progressBar.setValue(value)
    def signalRefreshcurStatus(self, info):
        self.m_mainUi.AmlDebugBurnStatusDisplay_label.setText(info)
    def signalSetButtonStatus(self, value):
        self.m_mainUi.AmlDebugBurnStart_pushButton.setText(value)
