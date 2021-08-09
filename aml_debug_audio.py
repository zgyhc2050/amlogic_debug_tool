import os
import shutil
import signal
import time
import threading
from pathlib import Path
import subprocess
from tkinter.constants import TRUE
import aml_common

DEBUG_CAPTURE_MODE_AUTO         = 0
DEBUG_CAPTURE_MODE_MUNUAL       = 1

DEFAULT_CAPTURE_MODE            = DEBUG_CAPTURE_MODE_AUTO
DEFAULT_AUTO_MODE_DUMP_TIME_S   = 3
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
    def __init__(self):
        self.RUN_STATE_STARTED = 1
        self.RUN_STATE_STOPED = 2
        self.__curState = -1
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
        self.__callbackFunc = 0

    def start_capture(self, startCaptureFinish):
        if self.__debugCfg.m_captureMode == DEBUG_CAPTURE_MODE_AUTO:
            self.__callbackFunc('Auto mode: Start to capture the info...')
        elif self.__debugCfg.m_captureMode == DEBUG_CAPTURE_MODE_MUNUAL:
            self.__callbackFunc('Manual mode: Start to capture the info...')
        if self.__curState == self.RUN_STATE_STARTED:
            self.__callbackFunc('current already started, do nothing')
            return
        self.__curState = self.RUN_STATE_STARTED
        # 1. Create the audio dump directory on PC, and prepare env to debug.
        self.__capture_debug_create_directory()
        self.__prepare_debug_env()
        if self.__debugCfg.m_logcatEnable:
            # open the audio hal debug level for capture logcat
            self.__capture_logcat_start()
        if self.__debugCfg.m_captureMode == DEBUG_CAPTURE_MODE_AUTO:
            # 2. Capture the debug info and write it to txt file.
            self.__capture_debug_text()

        if self.__debugCfg.m_logcatEnable:
            logcatProcThread = threading.Thread(target=self.__catpture_logcat)
            logcatProcThread.setDaemon(True)
            logcatProcThread.start()

        # 4. Capture the audio data.
        self.__capture_audio_data_start()

        if self.__debugCfg.m_captureMode == DEBUG_CAPTURE_MODE_AUTO:
            if self.__debugCfg.m_logcatEnable:
                if not self.__debugCfg.m_dumpDataEnable:
                    self.__callbackFunc('3.1 Please wait ' + str(self.__debugCfg.m_autoDebugTimeS) + 's for logcat...')
                    time.sleep(self.__debugCfg.m_autoDebugTimeS)
                # 5. Kill the logcat thread, stop logcat.
                self.__callbackFunc('3.2 Stop auto capture logcat...')
                self.__capture_logcat_stop()

            # 6. Pull the all debug files to PC
            self.__pull_capture_debug_info_to_pc()
            self.__print_help_info()
            self.__curState = self.RUN_STATE_STOPED
        startCaptureFinish()

    def stop_capture(self, stopcaptureFinish):
        if self.__curState != self.RUN_STATE_STARTED:
            self.__callbackFunc('stop_capture: current no start, do nothing')
            return
        if self.__debugCfg.m_captureMode != DEBUG_CAPTURE_MODE_MUNUAL:
            self.__callbackFunc('stop_capture: current not MUNAUL mode, not support stop!!!')
            return
        self.__manual_capture_stop()
        stopcaptureFinish()

    def __manual_capture_stop(self):
        self.__callbackFunc('2.2 MUNUAL mode: fetching the audio data end.')
        if self.__debugCfg.m_dumpDataEnable:
            self.__capture_audio_data_prop_disable()
        if self.__debugCfg.m_logcatEnable:
            self.__callbackFunc('3.2 Stop manual capture logcat...')
            self.__capture_logcat_stop()

        if self.__debugCfg.m_debugInfoEnable:
            self.__capture_debug_text()
        self.__pull_capture_debug_info_to_pc()
        self.__print_help_info()
        self.__curState = self.RUN_STATE_STOPED
    def __catpture_logcat(self):
        self.__callbackFunc('__catpture_logcat: Start logcat+++++')
        aml_common.exe_adb_cmd('adb shell "logcat -G 40M;logcat -c;logcat > ' + self.__logcatFilePath + '"')
        self.__callbackFunc('__catpture_logcat: Exit logcat------')

    def setShowStatusCallback(self, func):
        self.__callbackFunc = func

    def setAudioDebugCfg(self, cfg):
        self.__debugCfg = cfg

    def __capture_debug_create_directory(self):
        self.__nowPullPcTime = time.strftime("%Y%m%d_%H-%M-%S", time.localtime())
        self.__nowPullPcPath = aml_common.AML_DEBUG_DIRECOTRY_ROOT + "\\" + self.__nowPullPcTime
        self.__callbackFunc('Current date:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ', directory is: ' + self.__nowPullPcPath)
        if not Path(aml_common.AML_DEBUG_DIRECOTRY_ROOT).exists():
            self.__callbackFunc(aml_common.AML_DEBUG_DIRECOTRY_ROOT + " folder does not exist, create it.")
            os.makedirs(aml_common.AML_DEBUG_DIRECOTRY_ROOT, 777)
        os.makedirs(self.__nowPullPcPath, 777)
        return self.__nowPullPcPath

    def __capture_debug_text(self):
        if not self.__debugCfg.m_debugInfoEnable:
            return
        self.__callbackFunc('1.1 Please wait a moment, starting to dump debugging information...')
        self.__callbackFunc('1.2 Cat the some info to ' + self.__dumpCmdOutFilePath + ' file')
        for i, adbDumpCmd in enumerate(self.__adbDumpCmdLists):
            echoCmdStr = 'adb shell "echo ' + adbDumpCmd + ' >> ' + self.__dumpCmdOutFilePath + '"'
            exeCmdStr = 'adb shell "' + adbDumpCmd + ' >> ' + self.__dumpCmdOutFilePath + '"'
            aml_common.exe_adb_cmd(echoCmdStr, self.__debugCfg.m_printDebugEnable, self.__callbackFunc)
            aml_common.exe_adb_cmd(exeCmdStr, self.__debugCfg.m_printDebugEnable, self.__callbackFunc)

    def __capture_audio_data_start(self):
        if not self.__debugCfg.m_dumpDataEnable:
            return
        self.__capture_audio_data_prop_enable()
        self.__callbackFunc('2.1 AUTO mode: Start fetching the audio data, wait for ' + str(self.__debugCfg.m_autoDebugTimeS) + ' seconds...')
        if self.__debugCfg.m_captureMode == DEBUG_CAPTURE_MODE_AUTO:
            time.sleep(self.__debugCfg.m_autoDebugTimeS)
            self.__capture_audio_data_prop_disable()
            self.__callbackFunc('2.2 AUTO mode: fetching the audio data end.')

    def __prepare_debug_env(self):
        self.__capture_logcat_stop()
        self.__capture_audio_data_prop_disable()
        self.__capture_clear_all_files()

    def __pull_capture_debug_info_to_pc(self):
        self.__callbackFunc('Pull all file to PC ...')
        for dumpFile in self.__dumpFileLists:
            exeCmdStr = 'adb pull ' + dumpFile + ' ' + self.__nowPullPcPath
            aml_common.exe_adb_cmd(exeCmdStr, self.__debugCfg.m_printDebugEnable, self.__callbackFunc)
        if self.__debugCfg.m_createZipFile:
            tempFilePath = aml_common.AML_DEBUG_DIRECOTRY_ROOT + '\\' + self.__nowPullPcTime + '.zip'
            self.__callbackFunc('Zipping the files:' + self.__nowPullPcTime + '.zip')
            aml_common.zip_compress(self.__nowPullPcPath, tempFilePath)
            shutil.rmtree(self.__nowPullPcPath, ignore_errors=True)
            #shutil.move(tempFilePath, self.__nowPullPcPath)
            if self.__debugCfg.m_createZipFile:
                self.__callbackFunc('compress director:' + self.__nowPullPcPath + ' to ' + self.__nowPullPcPath + '\\' + self.__nowPullPcTime + '.zip')

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
        aml_common.exe_adb_cmd('adb shell "ps -ef |grep -v grep|grep logcat| awk \'{print $2}\'|xargs kill -9"',
            self.__debugCfg.m_printDebugEnable, self.__callbackFunc)

    def __exe_adb_shell_cmd(self, cmdLists):
        for cmd in cmdLists:
            exeCmdStr = 'adb shell "' + cmd + '"'
            aml_common.exe_adb_cmd(exeCmdStr, self.__debugCfg.m_printDebugEnable, self.__callbackFunc)

    def __print_help_info(self):
            print('###############################################################################################')
            print('##                                                                                           ##')
            print('##  Please send folder %-40s' % self.__nowPullPcPath + ' to RD colleagues! Thank You! ##')
            print('##                                                                                           ##')
            print('###############################################################################################')
            self.__callbackFunc('Please send folder ' + self.__nowPullPcPath + ' to RD colleagues! Thank You!')