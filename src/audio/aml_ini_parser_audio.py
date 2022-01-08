from src.common.aml_ini_parser import AmlParserIniBase, AmlParserIniManager
from src.audio.aml_debug_audio import AmlAudioDebug
from src.common.aml_common_utils import AmlCommonUtils

def instance(parser):
    return AmlParserIniAudio(parser)

class AmlParserIniAudio(AmlParserIniBase):
    AML_PARSER_AUDIO_CAPTRUE_MODE                   = "captrue_mode"
    AML_PARSER_AUDIO_DEBUG_INFO                     = "debug_info"
    AML_PARSER_AUDIO_DUMP_DATA                      = "dump_data"
    AML_PARSER_AUDIO_LOGCAT                         = "logcat"
    AML_PARSER_AUDIO_TOMBSTONE                      = "tombstone"
    AML_PARSER_AUDIO_CAPTURE_TIME                   = "captrue_time"
    AML_PARSER_AUDIO_PRINT_DEBUG                    = "print_debug"
    AML_PARSER_AUDIO_CREATE_ZIP                     = "create_zip"
    # play audio param
    AML_PARSER_AUDIO_PLAY_AUDIO_CHANNEL             = "play_audio_channel"
    AML_PARSER_AUDIO_PLAY_AUDIO_BYTE                = "play_audio_byte"
    AML_PARSER_AUDIO_PLAY_AUDIO_RATE                = "play_audio_rate"
    AML_PARSER_AUDIO_PLAY_AUDIO_PATH                = "play_audio_path"
    AML_PARSER_AUDIO_PLAY_AUDIO_SEL_CHANNEL         = "play_audio_sel_channel"
    def __init__(self, parser):
        super(AmlParserIniAudio, self).__init__(parser)
        self.m_section = AmlParserIniManager.AML_PARSER_SECTION_AUDIO

    def init_default_value(self):
        self.__dictionary_default_value = {
            AmlParserIniAudio.AML_PARSER_AUDIO_CAPTRUE_MODE      : str(AmlAudioDebug.DEFAULT_CAPTURE_MODE),
            AmlParserIniAudio.AML_PARSER_AUDIO_DEBUG_INFO        : 'True',
            AmlParserIniAudio.AML_PARSER_AUDIO_DUMP_DATA         : 'True',
            AmlParserIniAudio.AML_PARSER_AUDIO_LOGCAT            : 'True',
            AmlParserIniAudio.AML_PARSER_AUDIO_CAPTURE_TIME      : str(AmlAudioDebug.DEFAULT_AUTO_MODE_DUMP_TIME_S),
            AmlParserIniAudio.AML_PARSER_AUDIO_PRINT_DEBUG       : 'Flase',
            AmlParserIniAudio.AML_PARSER_AUDIO_CREATE_ZIP        : 'Flase',
            AmlParserIniAudio.AML_PARSER_AUDIO_TOMBSTONE         : 'Flase',
            AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_CHANNEL: '2',
            AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_BYTE   : '2',
            AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_RATE   : '48000',
            AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_PATH   : AmlCommonUtils.get_cur_root_path(),
        }
        return self.__dictionary_default_value
    
    def getValueByKey(self, key):
        if key == AmlParserIniAudio.AML_PARSER_AUDIO_CAPTRUE_MODE or        \
            key == AmlParserIniAudio.AML_PARSER_AUDIO_CAPTURE_TIME:
            return self.getIntValueByKey(key)
        elif key == AmlParserIniAudio.AML_PARSER_AUDIO_DEBUG_INFO or        \
            key == AmlParserIniAudio.AML_PARSER_AUDIO_DUMP_DATA or          \
            key == AmlParserIniAudio.AML_PARSER_AUDIO_LOGCAT or             \
            key == AmlParserIniAudio.AML_PARSER_AUDIO_PRINT_DEBUG or        \
            key == AmlParserIniAudio.AML_PARSER_AUDIO_CREATE_ZIP or        \
            key == AmlParserIniAudio.AML_PARSER_AUDIO_TOMBSTONE :
            return self.getBoolValueByKey(key)
        else :
            return self.getStrValueByKey(key)

    def setValueByKey(self, key, value):
        if key == AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_PATH or         \
            key == AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_CHANNEL or     \
            key == AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_BYTE or        \
            key == AmlParserIniAudio.AML_PARSER_AUDIO_PLAY_AUDIO_RATE:
            self.setStrValueByKey(key, value)
        else:
            self.setStrValueByKey(key, str(value))