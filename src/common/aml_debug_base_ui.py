import os
from abc import ABCMeta, abstractmethod
from pathlib import Path
from PyQt5.QtCore import Qt

from src.common.aml_common_utils import AmlCommonUtils
from src.common.aml_ini_parser import amlParserIniContainer, AmlParserIniManager

class AmlDebugModule():
    moduleList = []
    @staticmethod
    def initModule(aml_ui):
        import src.home.aml_debug_home_ui
        import src.audio.aml_debug_audio_ui
        import src.cec.aml_debug_cec_ui
        import src.system_operation.aml_debug_sys_operation_ui

        AmlDebugModule.moduleList.append(src.home.aml_debug_home_ui.instance(aml_ui))
        AmlDebugModule.moduleList.append(src.audio.aml_debug_audio_ui.instance(aml_ui))
        AmlDebugModule.moduleList.append(src.cec.aml_debug_cec_ui.instance(aml_ui))
        AmlDebugModule.moduleList.append(src.system_operation.aml_debug_sys_operation_ui.instance(aml_ui))

    @staticmethod
    def closeEvent():
        for module in AmlDebugModule.moduleList:
            module.closeEvent()

class AmlDebugBaseUi(metaclass=ABCMeta):
    AML_MODULE_NAME_ARRAY = {
        AmlCommonUtils.AML_DEBUG_MODULE_HOME                     : 'HOME',
        AmlCommonUtils.AML_DEBUG_MODULE_AUDIO                    : 'AUDIO',
        AmlCommonUtils.AML_DEBUG_MODULE_VIDEO                    : 'VIDEO',
        AmlCommonUtils.AML_DEBUG_MODULE_CEC                      : 'CEC',
        AmlCommonUtils.AML_DEBUG_MODULE_SYS_OPERATION            : 'SYS_OP',
    }

    def __init__(self, mainUi, moduleId):
        self.m_mainUi = mainUi
        self.m_moduleId = moduleId
        self.m_iniPaser = amlParserIniContainer.getParserById(AmlParserIniManager.AML_INI_SECTION_DIC[moduleId])
        self.log  = log_print(mainUi.terminalLogSignal.emit, moduleId)
        self.init_display_ui()
        self.signals_connect_slots()

    @abstractmethod
    def signals_connect_slots(self):
        pass

    @abstractmethod
    def init_display_ui(self):
        pass

    @abstractmethod
    def closeEvent(self):
        pass

    def start_capture(self, curTimeName, homeCallbackFinish, homeClick):
        self.log.d('AmlDebugBaseUi::start_capture: homeCallbackFinish id:' + self.m_moduleId)
        homeCallbackFinish(self.m_moduleId)

    def stop_capture(self, homeCallbackFinish, homeClick):
        self.log.d('AmlDebugBaseUi::stop_capture')
        homeCallbackFinish(self.m_moduleId)

    def get_logcat_enable(self):
        return False
    def get_bugreport_enable(self):
        return False
    def get_dmesg_enable(self):
        return False

    def state_to_bool(self, state):
        if state == Qt.CheckState.Checked:
            return True
        elif state == Qt.CheckState.Unchecked:
            return False
        else:
            self.logW('AmlDebugBaseUi::state_to_bool not support state:' + str(state) + ', return False')
            return False

    def check_output_path(self, openPath):
        if not Path(openPath).exists() or openPath == '':
            self.log.i('check_output_path audio debug path:' + openPath + ' not exist')
            openPath = AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT
            if not Path(openPath).exists() or openPath == '':
                self.log.w('check_output_path root path:' + openPath + ' not exist')
                openPath = os.getcwd()
        else:
            self.log.i('check_output_path audio debug path:' + openPath + ' exist')
        return openPath


class log_print():
    def __init__(self, log_func, moduleId):
        self.m_moduleId = moduleId
        self.log_fuction = log_func
        
    def log(self, info, level=AmlCommonUtils.AML_DEBUG_LOG_LEVEL_D):
        if self.m_moduleId in AmlDebugBaseUi.AML_MODULE_NAME_ARRAY.keys():
            self.log_fuction('[' + AmlDebugBaseUi.AML_MODULE_NAME_ARRAY[self.m_moduleId] + '] ' + info, level)
        else:
            self.log_fuction('[Error] AmlDebugBaseUi Can\'t find module id:' + self.m_moduleId, AmlCommonUtils.AML_DEBUG_LOG_LEVEL_E)
    
    def v(self, info):
        self.log(info, AmlCommonUtils.AML_DEBUG_LOG_LEVEL_V)
    def d(self, info):
        self.log(info, AmlCommonUtils.AML_DEBUG_LOG_LEVEL_D)
    def i(self, info):
        self.log(info, AmlCommonUtils.AML_DEBUG_LOG_LEVEL_I)
    def w(self, info):
        self.log(info, AmlCommonUtils.AML_DEBUG_LOG_LEVEL_W)
    def e(self, info):
        self.log(info, AmlCommonUtils.AML_DEBUG_LOG_LEVEL_E)
    def f(self, info):
        self.log(info, AmlCommonUtils.AML_DEBUG_LOG_LEVEL_F)