from src.common.aml_ini_parser import AmlParserIniBase, AmlParserIniManager

def instance(parser):
    return AmlParserIniSysOperation(parser)

class AmlParserIniSysOperation(AmlParserIniBase):
    AML_PARSER_SYS_OPERAT_PUSH_DOLBY_SRC_PATH         = 'push_dolby_src_path'
    AML_PARSER_SYS_OPERAT_PUSH_DTS_SRC_PATH           = 'push_dts_src_path'
    AML_PARSER_SYS_OPERAT_PUSH_MS12_SRC_PATH          = 'push_ms12_src_path'
    AML_PARSER_SYS_OPERAT_PUSH_DOLBYDTS_DST_PATH      = 'push_dolbydts_dst_path'
    AML_PARSER_SYS_OPERAT_PUSH_MS12_DST_PATH          = 'push_ms12_dst_path'

    AML_PARSER_SYS_OPERAT_PUSH_CUSTOM1_SRC_PATH        = 'push_custom1_src_path'
    AML_PARSER_SYS_OPERAT_PUSH_CUSTOM2_SRC_PATH        = 'push_custom2_src_path'
    AML_PARSER_SYS_OPERAT_PUSH_CUSTOM3_SRC_PATH        = 'push_custom3_src_path'
    AML_PARSER_SYS_OPERAT_PUSH_CUSTOM4_SRC_PATH        = 'push_custom4_src_path'
    AML_PARSER_SYS_OPERAT_PUSH_CUSTOM5_SRC_PATH        = 'push_custom5_src_path'
    AML_PARSER_SYS_OPERAT_PUSH_CUSTOM1_DST_PATH        = 'push_custom1_dst_path'
    AML_PARSER_SYS_OPERAT_PUSH_CUSTOM2_DST_PATH        = 'push_custom2_dst_path'
    AML_PARSER_SYS_OPERAT_PUSH_CUSTOM3_DST_PATH        = 'push_custom3_dst_path'
    AML_PARSER_SYS_OPERAT_PUSH_CUSTOM4_DST_PATH        = 'push_custom4_dst_path'
    AML_PARSER_SYS_OPERAT_PUSH_CUSTOM5_DST_PATH        = 'push_custom5_dst_path'

    AML_PARSER_SYS_OPERAT_PULL_CUSTOM1_SRC_PATH       = 'pull_custom1_src_path'
    AML_PARSER_SYS_OPERAT_PULL_CUSTOM2_SRC_PATH       = 'pull_custom2_src_path'
    AML_PARSER_SYS_OPERAT_PULL_CUSTOM3_SRC_PATH       = 'pull_custom3_src_path'
    AML_PARSER_SYS_OPERAT_PULL_CUSTOM4_SRC_PATH       = 'pull_custom4_src_path'
    AML_PARSER_SYS_OPERAT_PULL_CUSTOM1_DST_PATH       = 'pull_custom1_dst_path'
    AML_PARSER_SYS_OPERAT_PULL_CUSTOM2_DST_PATH       = 'pull_custom2_dst_path'
    AML_PARSER_SYS_OPERAT_PULL_CUSTOM3_DST_PATH       = 'pull_custom3_dst_path'
    AML_PARSER_SYS_OPERAT_PULL_CUSTOM4_DST_PATH       = 'pull_custom4_dst_path'
    def __init__(self, parser):
        super(AmlParserIniSysOperation, self).__init__(parser)
        self.m_section = AmlParserIniManager.AML_PARSER_SECTION_SYS_OPERATION

    def init_default_value(self):
        self.__dictionary_default_value = {
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBY_SRC_PATH         : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DTS_SRC_PATH           : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_SRC_PATH          : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBYDTS_DST_PATH      : '/odm/lib/',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_DST_PATH          : '/odm/etc/ms12/',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM1_SRC_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM2_SRC_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM3_SRC_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM4_SRC_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM5_SRC_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM1_DST_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM2_DST_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM3_DST_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM4_DST_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM5_DST_PATH       : '',

            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM1_SRC_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM2_SRC_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM3_SRC_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM4_SRC_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM1_DST_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM2_DST_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM3_DST_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM4_DST_PATH       : '',
        }
        return self.__dictionary_default_value

    def getValueByKey(self, key):
        return self.getStrValueByKey(key)

    def setValueByKey(self, key, value):
        #print('key:' + key + ', value:' + value)
        self.setStrValueByKey(key, value)
