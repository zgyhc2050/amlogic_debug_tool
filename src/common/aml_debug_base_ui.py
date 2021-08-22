from abc import ABCMeta, abstractmethod

import importlib

class AmlDebugModule():

    moduleList = []
    @staticmethod
    def initModule(aml_ui):
        import src.audio.aml_debug_audio_ui
        import src.system_operation.aml_debug_sys_operation_ui

        AmlDebugModule.moduleList.append(src.audio.aml_debug_audio_ui.instance(aml_ui))
        AmlDebugModule.moduleList.append(src.system_operation.aml_debug_sys_operation_ui.instance(aml_ui))

    @staticmethod
    def closeEvent():
        for module in AmlDebugModule.moduleList:
            module.closeEvent()

class AmlDebugBaseUi(metaclass=ABCMeta):
    def __init__(self, aml_ui):
        self.m_amlUi = aml_ui
        self.signals_connect_slots()
        self.init_default_config()
        self.init_display_ui()

    @abstractmethod
    def signals_connect_slots(self):
        pass

    @abstractmethod
    def init_default_config(self):
        pass

    @abstractmethod
    def init_display_ui(self):
        pass

    @abstractmethod
    def closeEvent(self):
        pass