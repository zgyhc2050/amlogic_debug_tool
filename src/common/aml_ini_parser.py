import configparser
from pathlib import Path

from abc import ABCMeta, abstractmethod
from src.common.aml_common import AmlCommon

class AmlParserIniManager:
    AML_PARSER_SECTION_AUDIO                                = "AM_AUDIO"
    AML_PARSER_SECTION_VIDEO                                = "AM_VIDEO"
    AML_PARSER_SECTION_SYS_OPERATION                        = "AM_SYS_OPERATION"
    def __init__(self):
        self.__parser = configparser.ConfigParser()
        import src.audio.aml_ini_parser_audio
        import src.system_operation.aml_ini_parser_sys_operation
        self.__m_dictionary_aml_parser = {
            AmlParserIniManager.AML_PARSER_SECTION_AUDIO                            : src.audio.aml_ini_parser_audio.instance(self.__parser),
            AmlParserIniManager.AML_PARSER_SECTION_SYS_OPERATION                    : src.system_operation.aml_ini_parser_sys_operation.instance(self.__parser),
        }

    def initParser(self):
        if not Path(AmlCommon.AML_DEBUG_DIRECOTRY_CONFIG).exists():
            print('First start, create file and loading default value to file:' + AmlCommon.AML_DEBUG_DIRECOTRY_CONFIG + '...')
            self.save_default_value_to_file()
            self.__iniFile = open(AmlCommon.AML_DEBUG_DIRECOTRY_CONFIG, 'w+')
            self.__parser.write(self.__iniFile)
            self.__iniFile.close()
        self.__parser.read(AmlCommon.AML_DEBUG_DIRECOTRY_CONFIG)

    def save_default_value_to_file(self):
        for section in self.__m_dictionary_aml_parser.keys():
            default_value_dic = self.__m_dictionary_aml_parser[section].init_default_value()
            #print('section:' +section )
            self.__parser.add_section(section)
            for key in default_value_dic.keys():
                self.__parser.set(section, key, default_value_dic[key])
                #print('key:' + key + ', value:' + default_value_dic[key]  )

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
        except :
            print('[E] AmlParserIniBase::getStrValueByKey section:' + self.m_section + \
                ' not found.')

    def getIntValueByKey(self, key):
        val = self.getStrValueByKey(key)
        try:
            return int(val)
        except :
            print('[E] AmlParserIniAudio::getIntValueByKey section:' + self.m_section + \
                ', key:' + key + ', exception.')
            return 0

    def getBoolValueByKey(self, key):
        val = self.getStrValueByKey(key)
        if val == 'True' or val == '1' or val == 'true':
            return True
        else :
            return False

    def setStrValueByKey(self, key, value):
        file = open(AmlCommon.AML_DEBUG_DIRECOTRY_CONFIG, 'w+')
        self.__parser.set(self.m_section, key, value)
        self.__parser.write(file)
        file.close()

amlParserIniContainer = AmlParserIniManager()