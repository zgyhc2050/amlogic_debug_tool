import configparser
from pathlib import Path

from abc import ABCMeta, abstractmethod
from src.common.aml_common_utils import AmlCommonUtils

class AmlParserIniManager:
    AML_PARSER_SECTION_HOME                                 = "AM_HOME"
    AML_PARSER_SECTION_AUDIO                                = "AM_AUDIO"
    AML_PARSER_SECTION_VIDEO                                = "AM_VIDEO"
    AML_PARSER_SECTION_CEC                                  = "AM_CEC"
    AML_PARSER_SECTION_SYS_OPERATION                        = "AM_SYS_OPERATION"
    AML_INI_SECTION_DIC = {
        AmlCommonUtils.AML_DEBUG_MODULE_HOME                             : AML_PARSER_SECTION_HOME,
        AmlCommonUtils.AML_DEBUG_MODULE_AUDIO                            : AML_PARSER_SECTION_AUDIO,
        AmlCommonUtils.AML_DEBUG_MODULE_VIDEO                            : AML_PARSER_SECTION_VIDEO,
        AmlCommonUtils.AML_DEBUG_MODULE_CEC                              : AML_PARSER_SECTION_CEC,
        AmlCommonUtils.AML_DEBUG_MODULE_SYS_OPERATION                    : AML_PARSER_SECTION_SYS_OPERATION,
    }
    def __init__(self):
        self.__parser = configparser.ConfigParser()
        import src.home.aml_ini_parser_home
        import src.audio.aml_ini_parser_audio
        import src.cec.aml_ini_parser_cec
        import src.system_operation.aml_ini_parser_sys_operation
        self.__m_dictionary_aml_parser = {
            AmlParserIniManager.AML_PARSER_SECTION_HOME                             : src.home.aml_ini_parser_home.instance(self.__parser),
            AmlParserIniManager.AML_PARSER_SECTION_AUDIO                            : src.audio.aml_ini_parser_audio.instance(self.__parser),
            AmlParserIniManager.AML_PARSER_SECTION_CEC                              : src.cec.aml_ini_parser_cec.instance(self.__parser),
            AmlParserIniManager.AML_PARSER_SECTION_SYS_OPERATION                    : src.system_operation.aml_ini_parser_sys_operation.instance(self.__parser),
        }

    def initParser(self):
        self.__init_ini_data()
        with open(AmlCommonUtils.AML_DEBUG_DIRECOTRY_CONFIG, 'w+') as file:
            self.__parser.write(file)
        self.__parser.read(AmlCommonUtils.AML_DEBUG_DIRECOTRY_CONFIG)

    def __init_ini_data(self):
        self.__parser.read(AmlCommonUtils.AML_DEBUG_DIRECOTRY_CONFIG)
        for section in self.__m_dictionary_aml_parser.keys():
            default_value_dic = self.__m_dictionary_aml_parser[section].init_default_value()
            self.__add_section(section, default_value_dic)

    def __add_section(self, section, key_dic):
        if not self.__parser.has_section(section):
            #print('section:' + section)
            self.__parser.add_section(section)
        for key in key_dic.keys():
            self.__add_section_key(section, key, key_dic[key])

    def __add_section_key(self, section, key, value):
        if not self.__parser.has_option(section, key):
            self.__parser.set(section, key, value)
            #print('key:' + key + ', value:' + key_dic[key])

    def getParserById(self, id):
        return self.__m_dictionary_aml_parser[id]

class AmlParserIniBase(metaclass=ABCMeta):
    def __init__(self, parser): 
        self.__parser = parser

    @abstractmethod
    def init_default_value(self):
        pass

    def getStrValueByKey(self, key):
        try:
            return self.__parser.get(self.m_section, key)
        except:
            print('E [AmlParserIniBase::getStrValueByKey]: section:' + self.m_section + ', key:' + key + ' not found.')

    def getIntValueByKey(self, key):
        val = self.getStrValueByKey(key)
        try:
            return int(val)
        except:
            print('E [AmlParserIniBase::getIntValueByKey]: section:' + self.m_section + ', key:' + key + ' exception.')
            return 0

    def getBoolValueByKey(self, key):
        val = self.getStrValueByKey(key)
        if val == 'True' or val == '1' or val == 'true':
            return True
        else :
            return False

    def setStrValueByKey(self, key, value):
        with open(AmlCommonUtils.AML_DEBUG_DIRECOTRY_CONFIG, 'w+') as file:
            self.__parser.set(self.m_section, key, value)
            self.__parser.write(file)

amlParserIniContainer = AmlParserIniManager()