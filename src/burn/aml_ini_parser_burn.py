from src.common.aml_ini_parser import AmlParserIniBase, AmlParserIniManager
from src.burn.aml_debug_burn import AmlDebugBurn

def instance(parser):
    return AmlParserIniBurn(parser)

class AmlParserIniBurn(AmlParserIniBase):
    # Options
    AML_PARSER_BURN_FILE_SAVE_OPTION              = "burn_save_option"

    def __init__(self, parser):
        super(AmlParserIniBurn, self).__init__(parser)
        self.m_section = AmlParserIniManager.AML_PARSER_SECTION_BURN

    def init_default_value(self):
        self.__dictionary_default_value = {
            AmlParserIniBurn.AML_PARSER_BURN_FILE_SAVE_OPTION            : AmlDebugBurn.AML_BURN_SAVE_FILE_ENUM_SAVE_ALL,
        }
        return self.__dictionary_default_value
    
    def getValueByKey(self, key):
        return self.getStrValueByKey(key)

    def setValueByKey(self, key, value):
        self.setStrValueByKey(key, str(value))