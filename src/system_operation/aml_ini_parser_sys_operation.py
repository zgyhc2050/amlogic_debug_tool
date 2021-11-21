from src.common.aml_ini_parser import AmlParserIniBase, AmlParserIniManager

def instance(parser):
    return AmlParserIniSysOperation(parser)

class AmlParserIniSysOperation(AmlParserIniBase):
    AML_PARSER_SYS_OPERAT_PARAM_TITLE                   ='Title'
    AML_PARSER_SYS_OPERAT_PARAM_SRC                     ='Src'
    AML_PARSER_SYS_OPERAT_PARAM_DST                     ='Dst'
    AML_PARSER_SYS_OPERAT_PARAM_CHECK_BOX               ='CheckBox'

    AML_PARSER_SYS_OPERAT_DIRECT_PUSH                   ='Push'
    AML_PARSER_SYS_OPERAT_DIRECT_PULL                   ='Pull'

    AML_PARSER_SYS_OPERAT_ITEM_PUSH_NUM                 = 35
    AML_PARSER_SYS_OPERAT_ITEM_PULL_NUM                 = 15

    AML_PARSER_SYS_OPERAT_KEY_PUSH_CUSTOME_ALL          = 'push_all_check_box'
    def __init__(self, parser):
        super(AmlParserIniSysOperation, self).__init__(parser)
        self.m_section = AmlParserIniManager.AML_PARSER_SECTION_SYS_OPERATION

    def init_default_value(self):
        self.__dictionary_default_value = {
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_KEY_PUSH_CUSTOME_ALL : 'False',
        }
        self.__initDefaultValueL(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PUSH)
        self.__initDefaultValueL(AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PULL)
        return self.__dictionary_default_value

    def __initDefaultValueL(self, direct):
        if direct == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PUSH:
            ITEM_NUM = AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_ITEM_PUSH_NUM
        elif direct == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PULL:
            ITEM_NUM = AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_ITEM_PULL_NUM
        else:
            print('[getKeyStrByParam] not supported direct:' + direct)
            return ''
        for i in range(0, ITEM_NUM):
            self.__dictionary_default_value[self.getKeyStrByParam(direct, AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PARAM_TITLE, i)] = 'custom:'
            self.__dictionary_default_value[self.getKeyStrByParam(direct, AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PARAM_SRC, i)] = ''
            self.__dictionary_default_value[self.getKeyStrByParam(direct, AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PARAM_DST, i)] = ''
            if direct == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PUSH:
                self.__dictionary_default_value[self.getKeyStrByParam(direct, AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PARAM_CHECK_BOX, i)] = 'False'

    def getValueByKey(self, key):
        if 'check_box' in key:
            return self.getBoolValueByKey(key)
        else:
            return self.getStrValueByKey(key)

    def setValueByKey(self, key, value):
        #print('key:' + key + ', value:' + value)
        if 'check_box' in key:
             self.setBoolValueByKey(key, value)
        else:
            self.setStrValueByKey(key, value)

    def getKeyStrByParam(self, direct, param, i):
        if direct == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PUSH:
            DIRECT = 'push'
        elif direct == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_DIRECT_PULL:
            DIRECT = 'pull'
        else:
            print('[getKeyStrByParam] not supported direct:' + direct)
            return ''

        if param == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PARAM_TITLE:
            PARAM = 'title'
        elif param == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PARAM_SRC:
            PARAM = 'src'
        elif param == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PARAM_DST:
            PARAM = 'dst'
        elif param == AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PARAM_CHECK_BOX:
            PARAM = 'check_box'
        else:
            print('[getKeyStrByParam] not supported param:' + param)
            return ''
        return DIRECT + '_custom' + str(i) + '_' + PARAM
