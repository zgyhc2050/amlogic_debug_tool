import os
import shutil
import time, threading
from threading import Thread
from pathlib import Path
from src.common.aml_common import AmlCommon

class AudioDebugCfg:
    def __init__(self):
        self.m_captureMode = 0
        self.m_debugInfoEnable = 0
        self.m_dumpDataEnable = 0
        self.m_logcatEnable = 0
        self.m_printDebugEnable = 0
        self.m_autoDebugTimeS = 0
        self.m_createZipFile = 0

class AmlAudioDebug:
    DEBUG_CAPTURE_MODE_AUTO         = 0
    DEBUG_CAPTURE_MODE_MUNUAL       = 1
    DEFAULT_CAPTURE_MODE            = DEBUG_CAPTURE_MODE_AUTO
    DEFAULT_AUTO_MODE_DUMP_TIME_S   = 3
    m_stopPlay = False
    def __init__(self, log_fuc):
        self.log_fuc = log_fuc
        self.RUN_STATE_STARTED = 1
        self.RUN_STATE_STOPED = 2
        self.__curState = -1
        self.__m_isPlaying = False
        self.__dumpCmdOutFilePath = '/data/dump_audio.log'
        self.__logcatFilePath = '/data/logcat.txt'
        self.__adbDumpCmdLists = [
            'cat /proc/asound/cards',
            'cat /proc/asound/pcm',
            'cat /proc/asound/card0/pcm*p/sub0/status',
            'cat /proc/asound/card0/pcm*p/sub0/hw_params',
            'cat /proc/asound/card0/pcm*p/sub0/sw_params',
            'cat /sys/class/amhdmitx/amhdmitx0/aud_cap',
            'cat /sys/class/amaudio/dts_enable',
            'cat /sys/class/amaudio/dolby_enable',
            'dumpsys hdmi_control',
            'dumpsys media.audio_policy',
            'dumpsys audio',
            'dumpsys media.audio_flinger',
            'tinymix'
        ]

        self.__adbDumpDataClearCmdLists = [
            'setenforce 0',
            'mkdir /data/audio /data/vendor/audiohal/ -p',
            'chmod 777 /data/audio /data/vendor/audiohal/',
            'rm /data/audio/* /data/vendor/audiohal/* -rf',
            'rm ' + self.__dumpCmdOutFilePath + ' -rf',
            'rm ' + self.__logcatFilePath + ' -rf',
        ]

        self.__adbDumpDataStartLists = [
            'setprop vendor.media.audiohal.indump 1',
            'setprop vendor.media.audiohal.outdump 1',
            'setprop vendor.media.audiohal.alsadump 1',
            'setprop vendor.media.audiohal.a2dpdump 1',
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
            'setprop vendor.media.audiohal.ms12dump 0',
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
            '/data/vendor/audiohal/',
            self.__dumpCmdOutFilePath,
            self.__logcatFilePath,
        ]
        self.__nowPullPcPath = ''
        self.__nowPullPcTime = ''

    def start_capture(self, startCaptureFinish):
        if self.__debugCfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            self.log_fuc('Auto mode: Start to capture the info...')
        elif self.__debugCfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL:
            self.log_fuc('Manual mode: Start to capture the info...')
        if self.__curState == self.RUN_STATE_STARTED:
            self.log_fuc('current already started, do nothing')
            return
        self.__curState = self.RUN_STATE_STARTED
        # 1. Create the audio dump directory on PC, and prepare env to debug.
        self.__capture_debug_create_directory()
        self.__prepare_debug_env()
        if self.__debugCfg.m_logcatEnable:
            # open the audio hal debug level for capture logcat
            self.__capture_logcat_start()
        if self.__debugCfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            # 2. Capture the debug info and write it to txt file.
            self.__capture_debug_text()
        if self.__debugCfg.m_logcatEnable:
            logcatProcThread = threading.Thread(target=self.__catpture_logcat)
            logcatProcThread.setDaemon(True)
            logcatProcThread.start()
        # 4. Capture the audio data.
        self.__capture_audio_data_start()

        if self.__debugCfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            if self.__debugCfg.m_logcatEnable:
                if not self.__debugCfg.m_dumpDataEnable:
                    self.log_fuc('3.1 Please wait ' + str(self.__debugCfg.m_autoDebugTimeS) + 's for logcat...')
                    time.sleep(self.__debugCfg.m_autoDebugTimeS)
                else:
                    self.log_fuc('3.1 Start auto capture logcat...')
                # 5. Kill the logcat thread, stop logcat.
                self.log_fuc('3.2 Stop auto capture logcat...')
                self.__capture_logcat_stop()

            # 6. Pull the all debug files to PC
            self.__pull_capture_debug_info_to_pc()
            self.__print_help_info()
            self.__curState = self.RUN_STATE_STOPED
        startCaptureFinish()

    def stop_capture(self, stopcaptureFinish):
        if self.__curState != self.RUN_STATE_STARTED:
            self.log_fuc('stop_capture: current no start, do nothing')
            return
        if self.__debugCfg.m_captureMode != AmlAudioDebug.DEBUG_CAPTURE_MODE_MUNUAL:
            self.log_fuc('stop_capture: current not MUNAUL mode, not support stop!!!')
            return
        self.__manual_capture_stop()
        stopcaptureFinish()

    def __manual_capture_stop(self):
        self.log_fuc('2.2 MUNUAL mode: fetching the audio data end.')
        if self.__debugCfg.m_dumpDataEnable:
            self.__capture_audio_data_prop_disable()
        if self.__debugCfg.m_logcatEnable:
            self.log_fuc('3.2 Stop manual capture logcat...')
            self.__capture_logcat_stop()

        if self.__debugCfg.m_debugInfoEnable:
            self.__capture_debug_text()
        self.__pull_capture_debug_info_to_pc()
        self.__print_help_info()
        self.__curState = self.RUN_STATE_STOPED
    def __catpture_logcat(self):
        self.log_fuc('__catpture_logcat: Start logcat+++++')
        AmlCommon.exe_adb_cmd('adb shell "logcat -G 40M;logcat -c;logcat > ' + self.__logcatFilePath + '"')
        self.log_fuc('__catpture_logcat: Exit logcat------')

    def setAudioDebugCfg(self, cfg):
        self.__debugCfg = cfg
    
    def getCurDebugPath(self):
        return self.__nowPullPcPath

    def __capture_debug_create_directory(self):
        self.__nowPullPcTime = time.strftime("%Y%m%d_%H-%M-%S", time.localtime())
        self.__nowPullPcPath = AmlCommon.AML_DEBUG_DIRECOTRY_ROOT + "\\" + self.__nowPullPcTime
        self.log_fuc('Current date:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ', directory is: ' + self.__nowPullPcPath)
        if not Path(AmlCommon.AML_DEBUG_DIRECOTRY_ROOT).exists():
            self.log_fuc(AmlCommon.AML_DEBUG_DIRECOTRY_ROOT + " folder does not exist, create it.")
            os.makedirs(AmlCommon.AML_DEBUG_DIRECOTRY_ROOT, 777)
        os.makedirs(self.__nowPullPcPath, 777)
        return self.__nowPullPcPath

    def __capture_debug_text(self):
        if not self.__debugCfg.m_debugInfoEnable:
            return
        self.log_fuc('1.1 Please wait a moment, starting to dump debugging information...')
        self.log_fuc('1.2 Cat the some info to ' + self.__dumpCmdOutFilePath + ' file')
        dumpCmdListTemp = []
        for adbDumpCmd in self.__adbDumpCmdLists:
            dumpCmdListTemp.append('echo ' + adbDumpCmd + ' >> ' + self.__dumpCmdOutFilePath)
            dumpCmdListTemp.append(adbDumpCmd + ' >> ' + self.__dumpCmdOutFilePath)
        self.__exe_adb_shell_cmd(dumpCmdListTemp)

    def __capture_audio_data_start(self):
        if not self.__debugCfg.m_dumpDataEnable:
            return
        self.__capture_audio_data_prop_enable()
        self.log_fuc('2.1 AUTO mode: Start fetching the audio data, wait for ' + str(self.__debugCfg.m_autoDebugTimeS) + ' seconds...')
        if self.__debugCfg.m_captureMode == AmlAudioDebug.DEBUG_CAPTURE_MODE_AUTO:
            time.sleep(self.__debugCfg.m_autoDebugTimeS)
            self.__capture_audio_data_prop_disable()
            self.log_fuc('2.2 AUTO mode: fetching the audio data end.')

    def __prepare_debug_env(self):
        self.__capture_logcat_stop()
        self.__capture_audio_data_prop_disable()
        self.__capture_clear_all_files()

    def __pull_capture_debug_info_to_pc(self):
        self.log_fuc('Pull all file to PC ...')
        for dumpFile in self.__dumpFileLists:
            exeCmdStr = 'adb pull ' + dumpFile + ' ' + self.__nowPullPcPath
            AmlCommon.exe_adb_cmd(exeCmdStr, self.__debugCfg.m_printDebugEnable, self.log_fuc)
        if self.__debugCfg.m_createZipFile:
            tempFilePath = AmlCommon.AML_DEBUG_DIRECOTRY_ROOT + '\\' + self.__nowPullPcTime + '.zip'
            self.log_fuc('Zipping the files:' + self.__nowPullPcTime + '.zip')
            AmlCommon.zip_compress(self.__nowPullPcPath, tempFilePath)
            shutil.rmtree(self.__nowPullPcPath, ignore_errors=True)
            #shutil.move(tempFilePath, self.__nowPullPcPath)
            if self.__debugCfg.m_createZipFile:
                self.log_fuc('compress director:' + self.__nowPullPcPath + ' to ' + self.__nowPullPcPath + '\\' + self.__nowPullPcTime + '.zip')

    def __capture_audio_data_prop_enable(self):
        self.__exe_adb_shell_cmd(self.__adbDumpDataStartLists)

    def __capture_audio_data_prop_disable(self):
        self.__exe_adb_shell_cmd(self.__adbDumpDataStopLists)

    def __capture_clear_all_files(self):
        self.__exe_adb_shell_cmd(self.__adbDumpDataClearCmdLists)

    def __capture_logcat_start(self):
        self.__exe_adb_shell_cmd(self.__adbLogcatStartLists)

    def __capture_logcat_stop(self):
        self.__exe_adb_shell_cmd(self.__adbLogcatStopLists)
        AmlCommon.exe_adb_cmd('adb shell "ps -ef |grep -v grep|grep logcat| awk \'{print $2}\'|xargs kill -9"',
            self.__debugCfg.m_printDebugEnable, self.log_fuc)

    def __exe_adb_shell_cmd(self, cmdLists):
        exeCmdStr = ''
        for i, cmd in enumerate(cmdLists):
            #print(cmd)
            exeCmdStr += cmd + ';'
            if self.__debugCfg.m_printDebugEnable == True:
                if 'echo' not in cmd:
                    self.log_fuc(cmd)
        exeCmdStr = 'adb shell "' + exeCmdStr + '"' 
        AmlCommon.exe_adb_cmd(exeCmdStr, False, self.log_fuc)

    def __print_help_info(self):
            print('###############################################################################################')
            print('##                                                                                           ##')
            print('##  Please send folder %-40s' % self.__nowPullPcPath + ' to RD colleagues! Thank You! ##')
            print('##                                                                                           ##')
            print('###############################################################################################')
            self.log_fuc('Please send folder ' + self.__nowPullPcPath + ' to RD colleagues! Thank You!')

    def start_play_toggle(self, filePath, channel, byte, rate, func_playEnd):
        if not Path(filePath).exists():
            self.log_fuc('E [start_play_toggle]: filePath:' + filePath + ' not exists')
            return False
        if self.__m_isPlaying == False:
            thread = threading.Thread(target = self.__audio_pcm_play_thread, args = (filePath, channel, byte, rate, func_playEnd))
            thread.start()
        else:
            AmlAudioDebug.m_stopPlay = True
        self.__m_isPlaying = not self.__m_isPlaying
        return self.__m_isPlaying

    def __audio_pcm_play_thread(self, filePath, channel, byte, rate, func_playEnd):
        import pyaudio, wave
        AmlAudioDebug.m_stopPlay = False
        with open(filePath, 'rb') as pcmfile:
            pcmdata = pcmfile.read()
        with wave.open('D:\\temp.wav', 'wb') as wavfile:
            wavfile.setparams((channel, byte, rate, 0, 'NONE', 'NONE'))
            wavfile.writeframes(pcmdata)

        temp_wave = wave.open('D:\\temp.wav', 'rb')
        amlPyAudio = pyaudio.PyAudio()
        AmlAudioDebug.__m_isPlaying = True
        # for i in range(amlPyAudio.get_device_count()):
        #     print(amlPyAudio.get_device_info_by_index(i))

        frames = temp_wave.getnframes()
        bit_width = temp_wave.getsampwidth()
        channel = temp_wave.getnchannels()
        sample_rate = temp_wave.getframerate()
        print('frames:' + str(frames))
        read_frames = 1024
        self.log_fuc('I [__audio_pcm_play_thread]: play pcm data byte:' + str(bit_width) + ', channel:' + str(channel) + ', rate:' + str(sample_rate))
        stream = amlPyAudio.open(format = amlPyAudio.get_format_from_width(bit_width), channels = channel, rate = sample_rate, output = True)
        self.log_fuc('I [__audio_pcm_play_thread]: starting to play file:' + filePath)
        while frames > 0 and AmlAudioDebug.m_stopPlay == False:
            data = temp_wave.readframes(read_frames)
            stream.write(data)
        stream.stop_stream()
        stream.close()
        amlPyAudio.terminate()
        AmlAudioDebug.__m_isPlaying = False
        func_playEnd()
        self.log_fuc('I [__audio_pcm_play_thread]: exit play')