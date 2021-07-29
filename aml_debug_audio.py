import os
import time
import threading
from pathlib import Path
import subprocess
from tkinter.constants import TRUE


DEBUG_CAPTURE_MODE_AUTO         = 0
DEBUG_CAPTURE_MODE_MUNUAL       = 1
DEFAULT_CAPTURE_MODE            = DEBUG_CAPTURE_MODE_AUTO
class AmlAudioDebug:
    def __init__(self):
        self.DUMP_DEBUG = False
        self.AUTO_MODE_DUMP_TIME_S = 1
        self.RUN_STATE_STARTED = 1
        self.RUN_STATE_STOPED = 2
        self.__curState = -1
        self.__dumpCmdOutFilePath = '/data/dump_audio.log'
        self.__dumpCmdOutLogcatPath = '/data/logcat.txt'
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
            'rm ' + self.__dumpCmdOutLogcatPath + ' -rf',
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
            'setprop vendor.media.audio.hal.debug 0',
            'setprop vendor.media.audiohal.indump 0',
            'setprop vendor.media.audiohal.outdump 0',
            'setprop vendor.media.audiohal.alsadump 0',
            'setprop vendor.media.audiohal.a2dpdump 0',
            'setprop vendor.media.audiohal.ms12dump 0',
            'setprop media.audio.hal.debug 0',
            'setprop media.audiohal.indump 0',
            'setprop media.audiohal.outdump 0',
            'setprop media.audiohal.alsadump 0',
            'setprop media.audiohal.a2dpdump 0',
            'setprop media.audiohal.ms12dump 0',
        ]

        self.__dumpFileLists = [
            'vendor/etc/audio_policy_configuration.xml',
            'vendor/etc/audio_policy_volumes.xml',
            '/data/audio',
            '/data/vendor/audiohal/',
            self.__dumpCmdOutLogcatPath,
            self.__dumpCmdOutFilePath,
        ]
        self.__captureLogcatProcThread = 0
        self.__captureMode = DEFAULT_CAPTURE_MODE
        self.__nowPullPcPath = 0
        self.__callbackFunc = 0

    def start_capture(self, startCaptureFinish):
        self.__callbackFunc('Start to capture the info...\n')
        if self.__curState == self.RUN_STATE_STARTED:
            self.__callbackFunc('current already started, do nothing')
            return
        self.__curState = self.RUN_STATE_STARTED
        os.system('adb root')
        os.system('adb remount')

        # 1. Create the audio dump directory on PC, and prepare env to debug.
        self.__nowPullPcPath = self.__capture_debug_create_directory()
        self.__prepare_debug_env()

        # open the audio hal debug level for capture logcat
        os.system('adb shell setprop vendor.media.audio.hal.debug 4096')
        os.system('adb shell setprop media.audio.hal.debug 4096')

        if self.__captureMode == DEBUG_CAPTURE_MODE_AUTO:
            # 2. Capture the debug info and write it to txt file.
            self.__callbackFunc('Please wait a moment, starting to dump debugging information...')
            self.__capture_debug_text()

        self.__callbackFunc('Start to capture logcat')
        # 3. Create thread to capturing logcat
        self.__captureLogcatProcThread = subprocess.Popen('adb shell "logcat -G 40M; logcat -c; logcat > ' + self.__dumpCmdOutLogcatPath + '"')

        if self.__captureMode == DEBUG_CAPTURE_MODE_AUTO:
            # 4. Capture the audio data.
            self.__capture_debug_dump()

            self.__callbackFunc('Stop capture logcat...')
            # 5. Kill the logcat thread, stop logcat.
            self.__captureLogcatProcThread.kill()

            # 6. Pull the all debug files to PC
            self.__pull_capture_debug_info_to_pc(self.__nowPullPcPath)

            self.__print_help_info()
            self.__curState = self.RUN_STATE_STOPED
        elif self.__captureMode == DEBUG_CAPTURE_MODE_MUNUAL:
            self.__callbackFunc('MUNUAL mode: Start fetching the audio data, wait for manual stop...')
            self.__capture_debug_dump_start()
        startCaptureFinish()

    def stop_capture(self, stopcaptureFinish):
        self.__capture_debug_dump_stop()
        if self.__curState != self.RUN_STATE_STARTED:
            self.__callbackFunc('current no start, do nothing')
            return
        if self.__captureLogcatProcThread != 0:
            self.__callbackFunc('Stop capture logcat...')
            self.__captureLogcatProcThread.kill()
        if self.__captureMode == DEBUG_CAPTURE_MODE_MUNUAL:
            self.__capture_debug_text()
            self.__pull_capture_debug_info_to_pc(self.__nowPullPcPath)
            self.__print_help_info()
            stopcaptureFinish()
            self.__curState = self.RUN_STATE_STOPED
            

    def set_capture_mode(self, mode):
        self.__captureMode = mode

    def get_capture_mode(self):
        return self.__captureMode

    def setShowStatusCallback(self, func):
        self.__callbackFunc = func

    def __capture_debug_create_directory(self):
        currentTime = time.strftime("%Y%m%d_%H-%M-%S", time.localtime())
        nowPullPath = self.__pcRootPath + "\\" + currentTime
        self.__callbackFunc('Current date:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ', directory is: ' + nowPullPath)
        if not Path(self.__pcRootPath).exists():
            self.__callbackFunc(self.__pcRootPath, " folder does not exist, create it.")
            os.makedirs(self.__pcRootPath, 777)
        os.makedirs(nowPullPath, 777)
        return nowPullPath

    def __capture_debug_text(self):
        self.__callbackFunc('Cat the some info to ' + self.__dumpCmdOutFilePath + ' file')
        for i, adbDumpCmdList in enumerate(self.__adbDumpCmdLists):
            echoCmdInfo = 'adb shell "echo cmd_' + str(i) + ' ' + adbDumpCmdList + ' >> ' + self.__dumpCmdOutFilePath + '"'
            exeCmdInfo = 'adb shell "' + adbDumpCmdList + ' >> ' + self.__dumpCmdOutFilePath + '"'
            if self.DUMP_DEBUG:
                print(echoCmdInfo)
                print(exeCmdInfo)
            os.system(echoCmdInfo)
            os.system(exeCmdInfo)

    def __capture_debug_dump(self):
        self.__capture_debug_dump_start()
        if self.__captureMode == DEBUG_CAPTURE_MODE_AUTO:
            self.__callbackFunc('AUTO mode: Start fetching the audio data, wait for ' + str(self.AUTO_MODE_DUMP_TIME_S) + ' seconds...')
            time.sleep(self.AUTO_MODE_DUMP_TIME_S)
            self.__capture_debug_dump_stop()
        elif self.__captureMode == DEBUG_CAPTURE_MODE_MUNUAL:
            self.__callbackFunc('MUNUAL mode: Start fetching the audio data, wait for manual stop...')

    def __prepare_debug_env(self):
        self.__capture_debug_dump_stop()
        self.__capture_debug_dump_clear()

    def __pull_capture_debug_info_to_pc(self, pullPath):
        self.__callbackFunc('Pull all file to PC ...')
        for dumpFile in self.__dumpFileLists:
            exeCmdInfo = 'adb pull ' + dumpFile + ' ' + pullPath
            self.__exe_adb_cmd(exeCmdInfo)

    def __capture_debug_dump_start(self):
        self.__exe_adb_shell_cmd(self.__adbDumpDataStartLists)
        
    def __capture_debug_dump_stop(self):
        self.__exe_adb_shell_cmd(self.__adbDumpDataStopLists)

    def __capture_debug_dump_clear(self):
        self.__exe_adb_shell_cmd(self.__adbDumpDataClearCmdLists)

    def __exe_adb_shell_cmd(self, cmdLists):
        for cmd in cmdLists:
            exeCmdInfo = 'adb shell "' + cmd + '"'
            self.__exe_adb_cmd(exeCmdInfo)

    def __exe_adb_cmd(self, cmd):
        if self.DUMP_DEBUG:
            print(cmd)
        os.system(cmd)

    def __print_help_info(self):
            print('###############################################################################################')
            print('##                                                                                           ##')
            print('##  Please send folder %-40s' % self.__nowPullPcPath + ' to RD colleagues! Thank You! ##')
            print('##                                                                                           ##')
            print('###############################################################################################')
            self.__callbackFunc('Please send folder ' + self.__nowPullPcPath + ' to RD colleagues! Thank You!')