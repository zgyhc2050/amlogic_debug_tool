from abc import ABCMeta, abstractmethod

class AmlDebugModule():
    moduleList = []
    @staticmethod
    def initModule(aml_ui):
        import src.common.aml_common_ui
        import src.audio.aml_debug_audio_ui
        import src.system_operation.aml_debug_sys_operation_ui

        AmlDebugModule.moduleList.append(src.audio.aml_debug_audio_ui.instance(aml_ui))
        AmlDebugModule.moduleList.append(src.system_operation.aml_debug_sys_operation_ui.instance(aml_ui))
        AmlDebugModule.moduleList.append(src.common.aml_common_ui.instance(aml_ui))

    @staticmethod
    def closeEvent():
        for module in AmlDebugModule.moduleList:
            module.closeEvent()

class AmlDebugBaseUi(metaclass=ABCMeta):
    def __init__(self, aml_ui):
        self.m_amlUi = aml_ui
        self.log_fuc = aml_ui.terminalLogSignal.emit
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