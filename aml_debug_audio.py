import os
import time
import threading
from pathlib import Path
import subprocess
from tkinter.constants import TRUE


DEBUG_CAPTURE_MODE_AUTO         = 0
DEBUG_CAPTURE_MODE_MUNUAL       = 1
DEFAULT_CAPTURE_MODE            = DEBUG_CAPTURE_MODE_AUTO

class AudioDebugCfg:
    def __init__(self):
        self.m_debugInfoEnable = 1
        self.m_dumpDataEnable = 1
        self.m_logcatEnable = 1
        self.m_printDebugEnable = 0

class AmlAudioDebug:
    def __init__(self):
        self.DUMP_DEBUG = True
        self.DEFAULT_AUTO_MODE_DUMP_TIME_S = 3
        self.RUN_STATE_STARTED = 1
        self.RUN_STATE_STOPED = 2
        self.__curState = -1
        self.__dumpCmdOutFilePath = '/data/dump_audio.log'
        self.__logcatFileName = 'logcat.txt'
        self.__pcRootPath = "d:\dump_audio"
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
        ]
        self.__captureLogcatProcThread = 0
        self.__captureMode = DEFAULT_CAPTURE_MODE
        self.__nowPullPcPath = 0
        self.__callbackFunc = 0
        self.__autoDebugTimeS = self.DEFAULT_AUTO_MODE_DUMP_TIME_S

    def start_capture(self, startCaptureFinish):
        if self.__captureMode == DEBUG_CAPTURE_MODE_AUTO:
            self.__callbackFunc('Auto mode: Start to capture the info...')
        elif self.__captureMode == DEBUG_CAPTURE_MODE_MUNUAL:
            self.__callbackFunc('Manual mode: Start to capture the info...')
        if self.__curState == self.RUN_STATE_STARTED:
            self.__callbackFunc('current already started, do nothing')
            return
        self.__curState = self.RUN_STATE_STARTED
        subprocess.call('adb root', shell=True)
        subprocess.call('adb remount', shell=True)

        # 1. Create the audio dump directory on PC, and prepare env to debug.
        self.__nowPullPcPath = self.__capture_debug_create_directory()
        self.__prepare_debug_env()

        if self.__debugCfg.m_logcatEnable == 1:
            # open the audio hal debug level for capture logcat
            self.__capture_logcat_start()

        if self.__captureMode == DEBUG_CAPTURE_MODE_AUTO:
            # 2. Capture the debug info and write it to txt file.
            self.__capture_debug_text()

        if self.__debugCfg.m_logcatEnable == 1:
            self.__callbackFunc('3.1 Start to capture logcat')
            # 3. Create thread to capturing logcat
            logcat_file = open(self.__nowPullPcPath + '\\' + self.__logcatFileName, 'w')
            subprocess.call('adb logcat -G 40M; adb logcat -c', shell=True)
            logcmd = "adb logcat"
            self.__captureLogcatProcThread = subprocess.Popen(logcmd,stdout=logcat_file,stderr=subprocess.PIPE)

        # 4. Capture the audio data.
        self.__capture_audio_data_start()

        if self.__captureMode == DEBUG_CAPTURE_MODE_AUTO:
            if self.__debugCfg.m_logcatEnable == 1:
                if self.__debugCfg.m_dumpDataEnable != 1:
                    self.__callbackFunc('3.1 Please wait ' + str(self.DEFAULT_AUTO_MODE_DUMP_TIME_S) + 's for logcat...')
                    time.sleep(self.__autoDebugTimeS)
                self.__capture_logcat_stop()
                self.__callbackFunc('3.2 Stop capture logcat...')
                # 5. Kill the logcat thread, stop logcat.
                self.__captureLogcatProcThread.terminate()

            # 6. Pull the all debug files to PC
            self.__pull_capture_debug_info_to_pc(self.__nowPullPcPath)
            self.__print_help_info()
            self.__curState = self.RUN_STATE_STOPED

        startCaptureFinish()

    def stop_capture(self, stopcaptureFinish):
        if self.__curState != self.RUN_STATE_STARTED:
            self.__callbackFunc('stop_capture: current no start, do nothing')
            return
        if self.__captureMode != DEBUG_CAPTURE_MODE_MUNUAL:
            self.__callbackFunc('stop_capture: current not MUNAUL mode, not support stop!!!')
            return
        self.__manual_capture_stop()
        stopcaptureFinish()

    def __manual_capture_stop(self):
        self.__callbackFunc('2.2 MUNUAL mode: fetching the audio data end.')
        if self.__debugCfg.m_dumpDataEnable == 1:
            self.__capture_audio_data_prop_disable()
        if self.__debugCfg.m_logcatEnable == 1:
            self.__callbackFunc('3.2 Stop capture logcat...')
            self.__capture_logcat_stop()
            if self.__captureLogcatProcThread != 0:
                self.__captureLogcatProcThread.terminate()

        if self.__debugCfg.m_debugInfoEnable == 1:
            self.__capture_debug_text()
        self.__pull_capture_debug_info_to_pc(self.__nowPullPcPath)
        self.__print_help_info()
        self.__curState = self.RUN_STATE_STOPED
 
    def set_capture_mode(self, mode):
        self.__captureMode = mode

    def get_capture_mode(self):
        return self.__captureMode

    def setShowStatusCallback(self, func):
        self.__callbackFunc = func

    def setAudioDebugCfg(self, cfg):
        self.__debugCfg = cfg

    def setAutoDebugTimeS(self, timeS):
        if timeS > 999 or timeS < 0:
            self.__callbackFunc('setAutoDebugTimeS: invalid timeS: ' + str(timeS) + ' param， use the default:' + str(self.DEFAULT_AUTO_MODE_DUMP_TIME_S) + 's')
            timeS = self.DEFAULT_AUTO_MODE_DUMP_TIME_S
        self.__autoDebugTimeS = timeS

    def __capture_debug_create_directory(self):
        currentTime = time.strftime("%Y%m%d_%H-%M-%S", time.localtime())
        nowPullPath = self.__pcRootPath + "\\" + currentTime
        self.__callbackFunc('Current date:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ', directory is: ' + nowPullPath)
        if not Path(self.__pcRootPath).exists():
            self.__callbackFunc(self.__pcRootPath + " folder does not exist, create it.")
            os.makedirs(self.__pcRootPath, 777)
        os.makedirs(nowPullPath, 777)
        return nowPullPath

    def __capture_debug_text(self):
        if self.__debugCfg.m_debugInfoEnable != 1:
            return
        self.__callbackFunc('1.1 Please wait a moment, starting to dump debugging information...')
        self.__callbackFunc('1.2 Cat the some info to ' + self.__dumpCmdOutFilePath + ' file')
        for i, adbDumpCmdList in enumerate(self.__adbDumpCmdLists):
            echoCmdInfo = 'adb shell "echo cmd_' + str(i) + ' ' + adbDumpCmdList + ' >> ' + self.__dumpCmdOutFilePath + '"'
            exeCmdInfo = 'adb shell "' + adbDumpCmdList + ' >> ' + self.__dumpCmdOutFilePath + '"'
            self.__exe_adb_cmd(echoCmdInfo)
            self.__exe_adb_cmd(exeCmdInfo)

    def __capture_audio_data_start(self):
        if self.__debugCfg.m_dumpDataEnable != 1:
            return
        self.__capture_audio_data_prop_enable()
        self.__callbackFunc('2.1 AUTO mode: Start fetching the audio data, wait for ' + str(self.__autoDebugTimeS) + ' seconds...')
        if self.__captureMode == DEBUG_CAPTURE_MODE_AUTO:
            time.sleep(self.__autoDebugTimeS)
            self.__capture_audio_data_prop_disable()
            self.__callbackFunc('2.2 AUTO mode: fetching the audio data end.')

    def __prepare_debug_env(self):
        self.__capture_logcat_stop()
        self.__capture_audio_data_prop_disable()
        self.__capture_clear_all_files()

    def __pull_capture_debug_info_to_pc(self, pullPath):
        self.__callbackFunc('Pull all file to PC ...')
        for dumpFile in self.__dumpFileLists:
            exeCmdInfo = 'adb pull ' + dumpFile + ' ' + pullPath
            self.__exe_adb_cmd(exeCmdInfo)

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

    def __exe_adb_shell_cmd(self, cmdLists):
        for cmd in cmdLists:
            exeCmdInfo = 'adb shell "' + cmd + '"'
            self.__exe_adb_cmd(exeCmdInfo)

    def __exe_adb_cmd(self, cmd):
        if self.__debugCfg.m_printDebugEnable != 0:
            self.__callbackFunc(cmd)
        subprocess.call(cmd, shell=True)

    def __print_help_info(self):
            print('###############################################################################################')
            print('##                                                                                           ##')
            print('##  Please send folder %-40s' % self.__nowPullPcPath + ' to RD colleagues! Thank You! ##')
            print('##                                                                                           ##')
            print('###############################################################################################')
            self.__callbackFunc('Please send folder ' + self.__nowPullPcPath + ' to RD colleagues! Thank You!')