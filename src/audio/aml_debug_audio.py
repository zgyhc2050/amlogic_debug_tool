import os, pyaudio, wave
import shutil
import time, threading
from pathlib import Path
from src.common.aml_common_utils import AmlCommonUtils
import numpy
class AudioDebugCfg:
    def __init__(self):
        self.m_captureMode = 0
        self.m_debugInfoEnable = 0
        self.m_dumpDataEnable = 0
        self.m_logcatEnable = 0
        self.m_tombstoneEnable = 0
        self.m_printDebugEnable = 0
        self.m_autoDebugTimeS = 0
        self.m_createZipFile = 0
        self.m_homeClick = False

class AmlAudioDebug:
    DEBUG_CAPTURE_MODE_AUTO         = 0
    DEBUG_CAPTURE_MODE_MUNUAL       = 1
    DEFAULT_CAPTURE_MODE            = DEBUG_CAPTURE_MODE_AUTO
    DEFAULT_AUTO_MODE_DUMP_TIME_S   = 3

    PLAY_AUDIO_CHANNEL_12           = 0
    PLAY_AUDIO_CHANNEL_34           = 1
    PLAY_AUDIO_CHANNEL_56           = 2
    PLAY_AUDIO_CHANNEL_78           = 3
    m_stopPlay = False
    def __init__(self, log_fuc):
        self.log = log_fuc
        self.RUN_STATE_STARTED = 1
        self.RUN_STATE_STOPED = 2
        self.__curState = -1
        self.__m_isPlaying = False
        self.__dumpCmdOutFilePath = '/data/dump_audio.log'
        self.__adbDumpCmdLists = [
            'cat /proc/asound/cards',
            'cat /proc/asound/pcm',
            'cat /proc/asound/card0/pcm*c/sub0/status',
            'cat /proc/asound/card0/pcm*c/sub0/hw_params',
            'cat /proc/asound/card0/pcm*c/sub0/sw_params',
            'cat /proc/asound/card0/pcm*p/sub0/status',
            'cat /proc/asound/card0/pcm*p/sub0/hw_params',
            'cat /proc/asound/card0/pcm*p/sub0/sw_params',
            'cat /sys/class/amhdmitx/amhdmitx0/aud_cap',
            'cat /sys/class/amaudio/dts_enable',
            'cat /sys/class/amaudio/dolby_enable',
            'ls -al /odm/lib/*Hw*',
            'ls -al /vendor/lib/*Hw*',
            'dumpsys hdmi_control',
            'dumpsys media.audio_policy',
            'dumpsys audio',
            'dumpsys media.audio_flinger',
            'tinymix'
        ]

        self.__adbDumpDataClearCmdLists = [
            'setenforce 0',
            'touch /data/audio_spk.pcm /data/audio_dtv.pcm /data/alsa_pcm_write.pcm',
            'mkdir /data/audio /data/audio_out /data/vendor/audiohal/ -p',
            'chmod 777 /data/audio /data/audio_out /data/vendor/audiohal/ /data/audio_spk.pcm /data/audio_dtv.pcm /data/alsa_pcm_write.pcm',
            'rm /data/audio/* /data/vendor/audiohal/* -rf',
            'rm ' + self.__dumpCmdOutFilePath + ' -rf',
            'rm ' + AmlCommonUtils.AML_DEBUG_PLATFORM_DIRECOTRY_COMMON_INFO + ' -rf',
        ]

        self.__adbDumpDataStartLists = [
            'setprop vendor.media.audiohal.indump 1',
            'setprop vendor.media.audiohal.outdump 1',
            'setprop vendor.media.audiohal.alsadump 1',
            'setprop vendor.media.audiohal.a2dpdump 1',
            'setprop vendor.media.audiohal.tvdump 1',
            'setprop vendor.media.audiohal.btpcm 1',
            'setprop vendor.media.audiohal.ms12dump 0xfff',
            'setprop media.audiohal.indump 1',
            'setprop media.audiohal.outdump 1',
            'setprop media.audiohal.alsadump 1',
            'setprop media.audiohal.a2dpdump 1',
            'setprop media.audiohal.ms12dump 0xfff',
        ]

        self.__adbDumpDataStopLists = [
            'setprop vendor.media.audiohal.indump 0',
            'setprop vendor.media.audiohal.outdump 0',
            'setprop vendor.media.audiohal.alsadump 0',
            'setprop vendor.media.audiohal.a2dpdump 0',
            'setprop vendor.media.audiohal.btpcm 0',
            'setprop vendor.media.audiohal.ms12dump 0',
            'setprop vendor.media.audiohal.tvdump 0',
            'setprop media.audiohal.indump 0',
            'setprop media.audiohal.outdump 0',
            'setprop media.audiohal.alsadump 0',
            'setprop media.audiohal.a2dpdump 0',
            'setprop media.audiohal.ms12dump 0',
        ]

        self.__adbLogcatStartLists = [
            'setprop vendor.media.audio.hal.debug 4096',
            'setprop media.audio.hal.debug 4096',
        ]

        self.__adbLogcatStopLists = [
            'setprop vendor.media.audio.hal.debug 0',
            'setprop media.audio.hal.debug 0',
        ]

        self.__dumpFileLists = [
            'vendor/etc/audio_policy_configuration.xml',
            'vendor/etc/audio_policy_volumes.xml',
            '/data/audio',
            '/data/audio_out',
            '/data/vendor/audiohal/',
            self.__dumpCmdOutFilePath,
            AmlCommonUtils.AML_DEBUG_PLATFORM_DIRECOTRY_LOGCAT,
        ]
        self.__nowPullPcPath = ''
        self.__nowPullPcTime = ''

    def start_capture(self, curTimeName, startCaptureFinish):
        if self.__debugCfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            self.log.d('Auto mode: Start to capture the info...')
        elif self.__debugCfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL:
            self.log.d('Manual mode: Start to capture the info...')
        if self.__curState == self.RUN_STATE_STARTED:
            self.log.w('current already started, do nothing')
            return
        self.log.d('AmlAudioDebug::start_capture m_homeClick:' + str(self.__debugCfg.m_homeClick))
        self.__curState = self.RUN_STATE_STARTED
        if self.__debugCfg.m_homeClick:
            self.__nowPullPcTime = curTimeName
        else :
            # 1. Create the audio dump directory on PC, and prepare env to debug.
            self.__nowPullPcTime = AmlCommonUtils.pre_create_directory(AmlCommonUtils.AML_DEBUG_MODULE_AUDIO)
        self.__nowPullPcPath = AmlCommonUtils.get_path_by_module(self.__nowPullPcTime, AmlCommonUtils.AML_DEBUG_MODULE_AUDIO)
        self.__prepare_debug_env()
        curpath = AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT + '\\' + self.__nowPullPcTime
        if self.__debugCfg.m_homeClick == False:
            AmlCommonUtils.cap_common_debug_info(curpath)
        if self.__debugCfg.m_logcatEnable and self.__debugCfg.m_homeClick == False:
            # open the audio hal debug level for capture logcat
            self.__capture_logcat_enable_prop()
        if self.__debugCfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            # 2. Capture the debug info and write it to txt file.
            self.__capture_debug_text()
        if self.__debugCfg.m_logcatEnable and self.__debugCfg.m_homeClick == False:
            AmlCommonUtils.logcat_start()
        # 4. Capture the audio data.
        self.__capture_audio_data_start()

        if self.__debugCfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            if self.__debugCfg.m_logcatEnable and self.__debugCfg.m_homeClick == False:
                if self.__debugCfg.m_dumpDataEnable == False:
                    self.log.d('3.1 Please wait ' + str(self.__debugCfg.m_autoDebugTimeS) + 's for logcat...')
                    time.sleep(self.__debugCfg.m_autoDebugTimeS)
                else:
                    self.log.d('3.1 Start auto capture logcat...')
                # 5. Kill the logcat thread, stop logcat.
                self.log.d('3.2 Stop auto capture logcat...')
                self.__capture_logcat_disable_prop()   
                AmlCommonUtils.logcat_stop()
            if self.__debugCfg.m_homeClick == False:
                AmlCommonUtils.cap_common_debug_info(curpath)

            # 6. Pull the all debug files to PC
            if self.__debugCfg.m_homeClick == False:
                AmlCommonUtils.pull_common_info_to_pc(curpath)
            self.__pull_capture_debug_info_to_pc()
            self.__print_help_info()
            self.__curState = self.RUN_STATE_STOPED
        startCaptureFinish()

    def stop_capture(self, stopcaptureFinish):
        if self.__curState != self.RUN_STATE_STARTED:
            self.log.d('stop_capture: current no start, do nothing')
            return
        if self.__debugCfg.m_captureMode != AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL:
            self.log.d('stop_capture: current not MUNAUL mode, not support stop!!!')
            return
        self.__manual_capture_stop()
        stopcaptureFinish()

    def open_logcat(self):
        self.__capture_logcat_enable_prop()

    def close_logcat(self):
        self.__capture_logcat_disable_prop()

    def __manual_capture_stop(self):
        curpath = AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT + '\\' + self.__nowPullPcTime
        self.log.d('2.2 MUNUAL mode: fetching the audio data end.')
        if self.__debugCfg.m_dumpDataEnable:
            self.__capture_audio_data_prop_disable()
        if self.__debugCfg.m_logcatEnable and self.__debugCfg.m_homeClick == False:
            self.log.d('3.2 Stop manual capture logcat...')
            self.__capture_logcat_disable_prop()

        if self.__debugCfg.m_debugInfoEnable:
            self.__capture_debug_text()
        if self.__debugCfg.m_homeClick == False:
            AmlCommonUtils.cap_common_debug_info(curpath)
            AmlCommonUtils.pull_common_info_to_pc(curpath)
        self.__pull_capture_debug_info_to_pc()
        self.__print_help_info()
        self.__curState = self.RUN_STATE_STOPED

    def setAudioDebugCfg(self, cfg):
        self.__debugCfg = cfg
    
    def getCurDebugPath(self):
        return self.__nowPullPcPath

    def __capture_debug_text(self):
        if not self.__debugCfg.m_debugInfoEnable:
            return
        self.log.d('1.1 Please wait a moment, starting to dump debugging information...')
        self.log.d('1.2 Cat the some info to ' + self.__dumpCmdOutFilePath + ' file')
        dumpCmdListTemp = []
        for adbDumpCmd in self.__adbDumpCmdLists:
            dumpCmdListTemp.append('echo ' + adbDumpCmd + ' >> ' + self.__dumpCmdOutFilePath)
            dumpCmdListTemp.append(adbDumpCmd + ' >> ' + self.__dumpCmdOutFilePath)
        self.__exe_adb_shell_cmd(dumpCmdListTemp)

    def __capture_audio_data_start(self):
        if not self.__debugCfg.m_dumpDataEnable:
            return
        self.__capture_audio_data_prop_enable()
        self.log.d('2.1 AUTO mode: Start fetching the audio data, wait for ' + str(self.__debugCfg.m_autoDebugTimeS) + ' seconds...')
        if self.__debugCfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            time.sleep(self.__debugCfg.m_autoDebugTimeS)
            self.__capture_audio_data_prop_disable()
            self.log.d('2.2 AUTO mode: fetching the audio data end.')

    def __prepare_debug_env(self):
        if self.__debugCfg.m_homeClick == False:
            self.__capture_logcat_disable_prop()
            
        self.__capture_audio_data_prop_disable()
        self.__capture_clear_all_files()

    def __pull_capture_debug_info_to_pc(self):
        self.log.d('Pull all file to PC ...')
        curpath = AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT + '\\' + self.__nowPullPcTime
        for dumpFile in self.__dumpFileLists:
            if ((self.__debugCfg.m_homeClick == True or self.__debugCfg.m_logcatEnable == False) and  dumpFile == AmlCommonUtils.AML_DEBUG_PLATFORM_DIRECOTRY_LOGCAT) or \
                (self.__debugCfg.m_dumpDataEnable == False and self.__dumpCmdOutFilePath == dumpFile):
                continue
            exeCmdStr = 'pull ' + dumpFile + ' ' + self.__nowPullPcPath
            AmlCommonUtils.exe_adb_cmd(exeCmdStr, self.__debugCfg.m_printDebugEnable)
        if self.__debugCfg.m_tombstoneEnable and self.__debugCfg.m_homeClick == False:
            AmlCommonUtils.pull_tombstones_to_pc(curpath)

        AmlCommonUtils.generate_snapshot(curpath)
        if self.__debugCfg.m_createZipFile:
            zip_src_dir = AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT + '\\' + self.__nowPullPcTime
            zip_dst_file = AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT + '\\' + self.__nowPullPcTime + '.zip'
            self.log.i('Zipping director:' + zip_src_dir + ' to ' + zip_dst_file)
            AmlCommonUtils.zip_compress(zip_src_dir, zip_dst_file)
            shutil.rmtree(zip_src_dir, ignore_errors=True)
            #shutil.move(zip_dst_dir, self.__nowPullPcPath)

    def __capture_audio_data_prop_enable(self):
        self.__exe_adb_shell_cmd(self.__adbDumpDataStartLists)

    def __capture_audio_data_prop_disable(self):
        self.__exe_adb_shell_cmd(self.__adbDumpDataStopLists)

    def __capture_clear_all_files(self):
        if self.__debugCfg.m_homeClick == False:
            AmlCommonUtils.exe_adb_shell_cmd('rm ' + AmlCommonUtils.AML_DEBUG_PLATFORM_DIRECOTRY_LOGCAT + ' -rf', self.__debugCfg.m_printDebugEnable)
        self.__exe_adb_shell_cmd(self.__adbDumpDataClearCmdLists)

    def __capture_logcat_enable_prop(self):
        self.__exe_adb_shell_cmd(self.__adbLogcatStartLists)

    def __capture_logcat_disable_prop(self):
        self.__exe_adb_shell_cmd(self.__adbLogcatStopLists)

    def __exe_adb_shell_cmd(self, cmdLists):
        exeCmdStr = ''
        for i, cmd in enumerate(cmdLists):
            #print(cmd)
            exeCmdStr += cmd + ';'
            if self.__debugCfg.m_printDebugEnable == True:
                if 'echo' not in cmd:
                    self.log.d(cmd)
        AmlCommonUtils.exe_adb_shell_cmd(exeCmdStr, False)

    def __print_help_info(self):
        if self.__debugCfg.m_createZipFile:
            target_file = AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT + '\\' + self.__nowPullPcTime + '.zip'
        else:
            target_file = self.__nowPullPcPath
        print('###############################################################################################')
        print('##                                                                                           ##')
        print('##  Please send folder %-40s' % target_file + ' to RD colleagues! Thank You! ##')
        print('##                                                                                           ##')
        print('###############################################################################################')
        self.log.i('Please send folder ' + target_file + ' to RD colleagues! Thank You!')

    def start_play_toggle(self, filePath, channel, byte, rate, selChn, func_playEnd):
        if not Path(filePath).exists():
            self.log.e('start_play_toggle filePath:' + filePath + ' not exists')
            return False
        if self.__m_isPlaying == False:
            thread = threading.Thread(target = self.__audio_pcm_play_thread, args = (filePath, channel, byte, rate, selChn, func_playEnd))
            thread.start()
        else:
            AmlAudioDebug.m_stopPlay = True
        self.__m_isPlaying = not self.__m_isPlaying
        return self.__m_isPlaying

    def __audio_pcm_play_thread(self, filePath, channel, byte, rate, selChn, func_playEnd):
        self.log.i('__audio_pcm_play_thread play pcm data byte:' + str(byte) + ', channel:' + \
            str(channel) + ', rate:' + str(rate) + ', sel ch:' + str(selChn * 2 + 1) + '_' + str(selChn * 2 + 2))
        AmlAudioDebug.m_stopPlay = False
        with open(filePath, 'rb') as pcmfile:
            pcmdata = pcmfile.read()
        tempWavFile = 'D:\\temp.wav'
        with wave.open(tempWavFile, 'wb') as wavfile:
            wavfile.setparams((channel, byte, rate, 0, 'NONE', 'NONE'))
            wavfile.writeframes(pcmdata)
        if channel > 2 or (channel == 2 and byte > 2):
            tempWavFile = self.__packageWavData(tempWavFile, channel, byte, rate, selChn)
 
        self.log.i('__audio_pcm_play_thread starting to play file:' + filePath)
        # for i in range(amlPyAudio.get_device_count()):
        #     print(amlPyAudio.get_device_info_by_index(i))
        AmlAudioDebug.__m_isPlaying = True
        self.__play_pcm_file(tempWavFile)
        AmlAudioDebug.__m_isPlaying = False
        func_playEnd()
        AmlCommonUtils.del_spec_file(tempWavFile)
        self.log.i('__audio_pcm_play_thread exit play')

    def __play_pcm_file(self, filePath):
        wavFile = wave.open(filePath, 'rb')
        amlPyAudio = pyaudio.PyAudio()
        remain_frames = wavFile.getnframes()
        bit_width = wavFile.getsampwidth()
        channel = wavFile.getnchannels()
        sample_rate = wavFile.getframerate()
        read_frames = 1024
        stream = amlPyAudio.open(format = amlPyAudio.get_format_from_width(bit_width), channels = channel, rate = sample_rate, output = True)
        self.log.i('__play_pcm_file starting to play' + ', frames:' + str(remain_frames) + ' (' + str(remain_frames//sample_rate) + ' s)')
        while remain_frames > 0 and AmlAudioDebug.m_stopPlay == False:
            if remain_frames > read_frames:
                frames = read_frames
            else:
                frames = remain_frames
            data = wavFile.readframes(frames)
            remain_frames -= frames
            stream.write(data)
        stream.stop_stream()
        stream.close()
        amlPyAudio.terminate()

    def __packageWavData(self, file, channel, sampleSize, rate, convertType):
        if channel % 2 != 0 or channel > 8 or channel <= 0:
            self.log.e('__packageWavData not support channel:' + channel + ' convert')
            return file
        if convertType >= channel / 2:
            self.log.e('__packageWavData not support convert type:' + convertType)
            return file
        srcWavFile =  wave.open(file, 'rb')
        srcWavData = srcWavFile.readframes(srcWavFile.getnframes())
        srcWavFile.close()

        dstWavData, channel = self.__convertTo2Channel(srcWavData, channel, sampleSize, convertType)
        dstWavData, sampleSize = self.__convertTo2ByteBitWide(dstWavData, sampleSize)
        AmlCommonUtils.del_spec_file(file)
        dstWavFile = 'D:\\temp_2ch.wav'
        with wave.open(dstWavFile, 'wb') as wavfile:
            wavfile.setparams((channel, sampleSize, rate, 0, 'NONE', 'NONE'))
            wavfile.writeframes(dstWavData.tostring())
        wavfile.close()
        return dstWavFile

    def __convertTo2Channel(self, src, channel, sampleSize, convertType):
        if channel <= 2:
            return src, channel
        if sampleSize == 1:
            numpy_type = numpy.int16
        elif sampleSize == 2:
            numpy_type = numpy.int32
        elif sampleSize == 4:
            numpy_type = numpy.int64
        else:
            self.log.d('E [__convertChannel]: not support sampleSize:' + sampleSize)
            return src, channel
        wavData = numpy.fromstring(src, dtype = numpy_type)
        wavData.shape = (-1, channel)
        wavData = wavData.T
        l_index = 2 * convertType
        r_index = 2 * convertType + 1
        dst = numpy.array(list(zip(wavData[l_index], wavData[r_index]))).flatten()
        return dst, 2

    def __convertTo2ByteBitWide(self, src, sampleSize):
        if sampleSize <= 2:
            return src, sampleSize
        if sampleSize != 4:
            self.log.d('E [__convertTo2ByteBitWide]: not support sampleSize:' + sampleSize)
            return src, sampleSize
        wavData = numpy.fromstring(src, dtype = numpy.int16)
        wavData.shape = (-1, 4)
        wavData = wavData.T
        dst = numpy.array(list(zip(wavData[1], wavData[3]))).flatten()
        return dst, 2