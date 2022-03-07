from PyQt5.QtCore import *
from threading import Thread

from src.common.aml_debug_base_ui import AmlDebugBaseUi
from src.common.aml_common_utils import AmlCommonUtils

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
        super(AmlDebugBurnUi, self).__init__(aml_ui, AmlCommonUtils.AML_DEBUG_MODULE_BURN)
        self.__isBurning = False
        self.__burn = AmlDebugBurn(self)

    def init_display_ui(self):
        self.m_mainUi.AmlDebugBurnTips_label.setOpenExternalLinks(True) 

    def signals_connect_slots(self):
        self.m_mainUi.AmlDebugBurnStart_pushButton.clicked.connect(self.__click_burnToggle)
        # self.m_mainUi.burnSetCurProcessFormatSignal.connect(self.signalSetCurProcessFormat)
        # self.m_mainUi.burnSetCurProcessMaxValueSignal.connect(self.signalSetCurProcessMaxValue)
        # self.m_mainUi.burnSetCurProcessSignal.connect(self.signalSetCurProcess)
        # self.m_mainUi.burnSetRefreshcurStatusSignal.connect(self.signalRefreshcurStatus)

    def closeEvent(self):
        pass

    def __click_burnToggle(self):
        if self.__isBurning == False:
            url = self.m_mainUi.AmlDebugBurnUrl_lineEdit.text()
            # url = 'http://firmware-sz.amlogic.com/shenzhen/image/android/Android-S/patchbuild/2022-03-03/ohm-userdebug-android32-kernel64-GTV-5327/'
            self.m_mainUi.AmlDebugBurnStart_pushButton.setText('Stop')
            self.thread = self.__burn.initBurn(url)
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