import configparser
import sys
from pathlib import Path

import src.audio.aml_debug_audio
import src.common.aml_common
from src.common.aml_common import AmlCommon

class AmlParserIniManager:
    def __init__(self):
        self.__parser = configparser.ConfigParser()
        self.__m_dictionary_aml_parser = {
            AmlParserIniBase.AML_PARSER_AUDIO                            : AmlParserIniAudio(self.__parser),
            AmlParserIniBase.AML_PARSER_SYS_OPERATION                    : AmlParserIniSysOperation(self.__parser),
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
            default_value_dic = self.__m_dictionary_aml_parser[section].init_aml_default_value()
            #print('section:' +section )
            self.__parser.add_section(section)
            for key in default_value_dic.keys():
                self.__parser.set(section, key, default_value_dic[key])
                #print('key:' + key + ', value:' + default_value_dic[key]  )

    def getParserById(self, id):
        return self.__m_dictionary_aml_parser[id]


class AmlParserIniBase:
    AML_PARSER_AUDIO                                = "AM_AUDIO"
    AML_PARSER_VIDEO                                = "AM_VIDEO"
    AML_PARSER_SYS_OPERATION                        = "AM_SYS_OPERATION"
    def __init__(self, parser): 
        self.__parser = parser

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

class AmlParserIniAudio(AmlParserIniBase):
    AML_PARSER_AUDIO_CAPTRUE_MODE                   = "captrue_mode"
    AML_PARSER_AUDIO_DEBUG_INFO                     = "debug_info"
    AML_PARSER_AUDIO_DUMP_DATA                      = "dump_data"
    AML_PARSER_AUDIO_LOGCAT                         = "logcat"
    AML_PARSER_AUDIO_CAPTURE_TIME                   = "captrue_time"
    AML_PARSER_AUDIO_PRINT_DEBUG                    = "print_debug"
    AML_PARSER_AUDIO_CREATE_ZIP                     = "create_zip"
    def __init__(self, parser):
        AmlParserIniBase.__init__(self, parser)
        self.m_section = AmlParserIniBase.AML_PARSER_AUDIO

    def init_aml_default_value(self):
        self.__dictionary_default_value = {
            AmlParserIniAudio.AML_PARSER_AUDIO_CAPTRUE_MODE      : str(src.audio.aml_debug_audio.DEFAULT_CAPTURE_MODE),
            AmlParserIniAudio.AML_PARSER_AUDIO_DEBUG_INFO        : 'True',
            AmlParserIniAudio.AML_PARSER_AUDIO_DUMP_DATA         : 'True',
            AmlParserIniAudio.AML_PARSER_AUDIO_LOGCAT            : 'True',
            AmlParserIniAudio.AML_PARSER_AUDIO_CAPTURE_TIME      : str(src.audio.aml_debug_audio.DEFAULT_AUTO_MODE_DUMP_TIME_S),
            AmlParserIniAudio.AML_PARSER_AUDIO_PRINT_DEBUG       : 'True',
            AmlParserIniAudio.AML_PARSER_AUDIO_CREATE_ZIP        : 'Flase',
        }
        return self.__dictionary_default_value
    
    def getValueByKey(self, key):
        if key == AmlParserIniAudio.AML_PARSER_AUDIO_CAPTRUE_MODE or   \
            key == AmlParserIniAudio.AML_PARSER_AUDIO_CAPTURE_TIME :
            return self.getIntValueByKey(key)
        elif key == AmlParserIniAudio.AML_PARSER_AUDIO_DEBUG_INFO or   \
            key == AmlParserIniAudio.AML_PARSER_AUDIO_DUMP_DATA or   \
            key == AmlParserIniAudio.AML_PARSER_AUDIO_LOGCAT or   \
            key == AmlParserIniAudio.AML_PARSER_AUDIO_PRINT_DEBUG or   \
            key == AmlParserIniAudio.AML_PARSER_AUDIO_CREATE_ZIP :
            return self.getBoolValueByKey(key)
        else :
            print('[E] AmlParserIniAudio::getValueByKey key:' + key + ', not support key.')
            return -1

    def setValueByKey(self, key, value):
        self.setStrValueByKey(key, str(value))

class AmlParserIniSysOperation(AmlParserIniBase):
    AML_PARSER_SYS_OPERAT_PUSH_DOLBY_SRC_PATH         = 'push_dolby_src_path'
    AML_PARSER_SYS_OPERAT_PUSH_DTS_SRC_PATH           = 'push_dts_src_path'
    AML_PARSER_SYS_OPERAT_PUSH_MS12_SRC_PATH          = 'push_ms12_src_path'
    AML_PARSER_SYS_OPERAT_PUSH_CUSTOM_SRC_PATH        = 'push_custom_src_path'
    AML_PARSER_SYS_OPERAT_PUSH_DOLBYDTS_DST_PATH      = 'push_dolbydts_dst_path'
    AML_PARSER_SYS_OPERAT_PUSH_MS12_DST_PATH          = 'push_ms12_dst_path'
    AML_PARSER_SYS_OPERAT_PUSH_CUSTOM_DST_PATH        = 'push_custom_dst_path'

    AML_PARSER_SYS_OPERAT_PULL_CUSTOM1_SRC_PATH       = 'pull_custom1_src_path'
    AML_PARSER_SYS_OPERAT_PULL_CUSTOM2_SRC_PATH       = 'pull_custom2_src_path'
    AML_PARSER_SYS_OPERAT_PULL_CUSTOM1_DST_PATH       = 'pull_custom1_dst_path'
    AML_PARSER_SYS_OPERAT_PULL_CUSTOM2_DST_PATH       = 'pull_custom2_dst_path'

    def __init__(self, parser):
        AmlParserIniBase.__init__(self, parser)
        self.m_section = AmlParserIniBase.AML_PARSER_SYS_OPERATION

    def init_aml_default_value(self):
        self.__dictionary_default_value = {
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBY_SRC_PATH         : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DTS_SRC_PATH           : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_SRC_PATH          : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM_SRC_PATH        : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_DOLBYDTS_DST_PATH      : '/odm/lib/',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_MS12_DST_PATH          : '/odm/etc/ms12/',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PUSH_CUSTOM_DST_PATH        : '',

            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM1_SRC_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM2_SRC_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM1_DST_PATH       : '',
            AmlParserIniSysOperation.AML_PARSER_SYS_OPERAT_PULL_CUSTOM2_DST_PATH       : '',
        }
        return self.__dictionary_default_value

    def getValueByKey(self, key):
        return self.getStrValueByKey(key)
    def setValueByKey(self, key, value):
        self.setStrValueByKey(key, value)

amlParserIniContainer = AmlParserIniManager()