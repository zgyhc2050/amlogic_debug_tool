import time, threading, os
from pathlib import Path

from src.common.aml_common import AmlCommon
from src.common.aml_ini_parser import AmlParserIniManager

class AmlCommonUtils():
    moduleDirPathDict = {
        AmlCommon.AML_DEBUG_MODULE_AUDIO    :   'audio',
        AmlCommon.AML_DEBUG_MODULE_VIDEO    :   'video',
        AmlCommon.AML_DEBUG_MODULE_CEC      :   'cec',
    }
    def pre_create_directory(createByModule, moduleEnableArray=0):
        if not Path(AmlCommon.AML_DEBUG_DIRECOTRY_ROOT).exists():
            AmlCommon.log_func(AmlCommon.AML_DEBUG_DIRECOTRY_ROOT + " folder does not exist, create it.")
            os.makedirs(AmlCommon.AML_DEBUG_DIRECOTRY_ROOT, 777)
        curTime = time.strftime("%Y%m%d_%H-%M-%S", time.localtime())
        curPullPcTimePath = AmlCommon.AML_DEBUG_DIRECOTRY_ROOT + "\\" + curTime
        AmlCommon.log_func('pre_create_directory Current date:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ', directory is: ' + curPullPcTimePath)
        os.makedirs(curPullPcTimePath, 777)
        modulePath = curPullPcTimePath
        if createByModule == AmlCommon.AML_DEBUG_MODULE_HOME:
            if moduleEnableArray == 0:
                AmlCommon.log_func('W __pre_create_directory: cfg is null')
            for index in range(AmlCommon.AML_DEBUG_MODULE_AUDIO, AmlCommon.AML_DEBUG_MODULE_MAX):
                if moduleEnableArray[index] == True:
                        modulePath = curPullPcTimePath + "\\" + AmlCommonUtils.moduleDirPathDict[index]
                        os.makedirs(modulePath, 777)
        else:
            if createByModule in AmlCommonUtils.moduleDirPathDict:
                modulePath = curPullPcTimePath + "\\" + AmlCommonUtils.moduleDirPathDict[createByModule]
                os.makedirs(modulePath, 777)
            else:
                AmlCommon.log_func('E __pre_create_directory: createByModule:' + createByModule + ' invalid.')
        return curTime


    def logcat_start():
        AmlCommon.log_func('logcat_start: logcat loading...')
        logcatProcThread = threading.Thread(target=AmlCommonUtils.__catpture_logcat_thread)
        logcatProcThread.setDaemon(True)
        logcatProcThread.start()

    def logcat_stop():
        AmlCommon.exe_adb_cmd('adb shell "ps -ef |grep -v grep|grep logcat| awk \'{print $2}\'|xargs kill -9"', True)

    def __catpture_logcat_thread():
        AmlCommon.log_func('__catpture_logcat_thread: Start logcat+++++')
        AmlCommon.exe_adb_cmd('adb shell "logcat -G 40M;logcat -c;logcat > ' + AmlCommon.AML_DEBUG_PLATFORM_DIRECOTRY_LOGCAT + '"', True)
        AmlCommon.log_func('__catpture_logcat_thread: Exit logcat------')

    def bugreport(path):
        AmlCommon.exe_adb_cmd('adb bugreport ' + path, True)

    def dmesg():
        AmlCommon.exe_adb_cmd('adb shell "rm ' + ' /data/dmesg.txt -rf', True)
        AmlCommon.exe_adb_cmd('adb shell "dmesg' + ' > /data/dmesg.txt', True)
