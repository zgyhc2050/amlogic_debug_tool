from src.common.aml_ini_parser import AmlParserIniBase, AmlParserIniManager

def instance(parser):
    return AmlParserIniCec(parser)

class AmlParserIniCec(AmlParserIniBase):
    # Options
    AML_PARSER_CEC_LOGCAT                         = "logcat_enable"
    AML_PARSER_CEC_BUGREPORT                      = "bugreport_enable"

    def __init__(self, parser):
        super(AmlParserIniCec, self).__init__(parser)
        self.m_section = AmlParserIniManager.AML_PARSER_SECTION_CEC

    def init_default_value(self):
        self.__dictionary_default_value = {
            AmlParserIniCec.AML_PARSER_CEC_LOGCAT            : 'Flase',
            AmlParserIniCec.AML_PARSER_CEC_BUGREPORT         : 'Flase',
        }
        return self.__dictionary_default_value
    
    def getValueByKey(self, key):
        if key == AmlParserIniCec.AML_PARSER_CEC_LOGCAT or              \
            key == AmlParserIniCec.AML_PARSER_CEC_BUGREPORT:
            return self.getBoolValueByKey(key)
        else:
            return self.getStrValueByKey(key)

    def setValueByKey(self, key, value):
        self.setStrValueByKey(key, str(value))