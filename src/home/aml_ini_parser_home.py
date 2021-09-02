from src.common.aml_ini_parser import AmlParserIniBase, AmlParserIniManager

def instance(parser):
    return AmlParserIniHome(parser)

class AmlParserIniHome(AmlParserIniBase):
    # Modules
    AML_PARSER_HOME_AUDIO_ENABLE                   = "audio_enable"
    AML_PARSER_HOME_VIDEO_ENABLE                   = "video_enable"
    AML_PARSER_HOME_CEC_ENABLE                     = "cec_enable"
    # Options
    AML_PARSER_HOME_LOGCAT                         = "logcat_enable"
    AML_PARSER_HOME_BUGREPORT                      = "bugreport_enable"
    AML_PARSER_HOME_DMESG                          = "dmesg_enable"

    AML_PARSER_HOME_CAPTRUE_MODE                   = "captrue_mode"
    AML_PARSER_HOME_CAPTURE_TIME                   = "captrue_time"

    DEBUG_CAPTURE_MODE_AUTO         = 0
    DEBUG_CAPTURE_MODE_MUNUAL       = 1
    DEFAULT_CAPTURE_MODE            = DEBUG_CAPTURE_MODE_AUTO
    def __init__(self, parser):
        super(AmlParserIniHome, self).__init__(parser)
        self.m_section = AmlParserIniManager.AML_PARSER_SECTION_HOME

    def init_default_value(self):
        self.__dictionary_default_value = {
            AmlParserIniHome.AML_PARSER_HOME_AUDIO_ENABLE      : 'Flase',
            AmlParserIniHome.AML_PARSER_HOME_VIDEO_ENABLE      : 'Flase',
            AmlParserIniHome.AML_PARSER_HOME_CEC_ENABLE        : 'Flase',
            AmlParserIniHome.AML_PARSER_HOME_LOGCAT            : 'Flase',
            AmlParserIniHome.AML_PARSER_HOME_BUGREPORT         : 'Flase',
            AmlParserIniHome.AML_PARSER_HOME_DMESG             : 'Flase',

            AmlParserIniHome.AML_PARSER_HOME_CAPTRUE_MODE      : str(AmlParserIniHome.DEFAULT_CAPTURE_MODE),
            AmlParserIniHome.AML_PARSER_HOME_CAPTURE_TIME      : '5',
        }
        return self.__dictionary_default_value
    
    def getValueByKey(self, key):
        if key == AmlParserIniHome.AML_PARSER_HOME_CAPTRUE_MODE or        \
            key == AmlParserIniHome.AML_PARSER_HOME_CAPTURE_TIME:
            return self.getIntValueByKey(key)
        elif key == AmlParserIniHome.AML_PARSER_HOME_AUDIO_ENABLE or       \
            key == AmlParserIniHome.AML_PARSER_HOME_VIDEO_ENABLE or        \
            key == AmlParserIniHome.AML_PARSER_HOME_CEC_ENABLE or          \
            key == AmlParserIniHome.AML_PARSER_HOME_LOGCAT or              \
            key == AmlParserIniHome.AML_PARSER_HOME_BUGREPORT or           \
            key == AmlParserIniHome.AML_PARSER_HOME_DMESG:
            return self.getBoolValueByKey(key)
        else :
            return self.getStrValueByKey(key)

    def setValueByKey(self, key, value):
        self.setStrValueByKey(key, str(value))