from abc import ABCMeta, abstractmethod

class AmlDebugModule():
    moduleList = []
    @staticmethod
    def initModule(aml_ui):
        import src.home.aml_debug_home_ui
        import src.audio.aml_debug_audio_ui
        import src.system_operation.aml_debug_sys_operation_ui

        AmlDebugModule.moduleList.append(src.home.aml_debug_home_ui.instance(aml_ui))
        AmlDebugModule.moduleList.append(src.audio.aml_debug_audio_ui.instance(aml_ui))
        AmlDebugModule.moduleList.append(src.system_operation.aml_debug_sys_operation_ui.instance(aml_ui))

    @staticmethod
    def closeEvent():
        for module in AmlDebugModule.moduleList:
            module.closeEvent()

class AmlDebugBaseUi(metaclass=ABCMeta):
    def __init__(self, aml_ui, moduleId):
        self.m_amlUi = aml_ui
        self.m_moduleId = moduleId
        self.log_fuc = aml_ui.terminalLogSignal.emit
        self.init_display_ui()
        self.signals_connect_slots()

    @abstractmethod
    def signals_connect_slots(self):
        pass

    @abstractmethod
    def init_display_ui(self):
        pass

    def start_capture(self, curTimeName, homeCallbackFinish):
        self.log_fuc('AmlDebugBaseUi::start_capture')
        print('AmlDebugBaseUi::start_capture: homeCallbackFinish id:' + self.m_moduleId)
        homeCallbackFinish(self.m_moduleId)

    def stop_capture(self, homeCallbackFinish):
        self.log_fuc('AmlDebugBaseUi::stop_capture')
        homeCallbackFinish(self.m_moduleId)

    def get_logcat_enable(self):
        return False

    @abstractmethod
    def closeEvent(self):
        pass