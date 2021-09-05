import time, threading, os, math
from pathlib import Path
import subprocess
import zipfile
import shutil


RET_VAL_SUCCESS         = 0
RET_VAL_FAIL            = -1
RET_VAL_EXCEPTION       = -2



class AmlCommonUtils():
    AML_DEBUG_MODULE_HOME                       = 0
    AML_DEBUG_MODULE_AUDIO                      = 1
    AML_DEBUG_MODULE_VIDEO                      = 2
    AML_DEBUG_MODULE_CEC                        = 3
    AML_DEBUG_MODULE_SYS_OPERATION              = 4
    AML_DEBUG_MODULE_MAX                        = AML_DEBUG_MODULE_SYS_OPERATION + 1

    AML_DEBUG_DIRECOTRY_ROOT                    = "d:\\aml_debug"
    AML_DEBUG_PLATFORM_DIRECOTRY_LOGCAT         = '/data/logcat.txt'
    AML_DEBUG_PLATFORM_DIRECOTRY_DMESG          = '/data/dmesg.txt'
    AML_DEBUG_TOOL_ICO_PATH                     = ':/debug.ico'
    AML_DEBUG_DIRECOTRY_CONFIG                  = AML_DEBUG_DIRECOTRY_ROOT + '\\config.ini'
    moduleDirPathDict = {
        AML_DEBUG_MODULE_AUDIO    :   'audio',
        AML_DEBUG_MODULE_VIDEO    :   'video',
        AML_DEBUG_MODULE_CEC      :   'cec',
    }

    AML_DEBUG_LOG_LEVEL_V                       = 'V'
    AML_DEBUG_LOG_LEVEL_D                       = 'D'
    AML_DEBUG_LOG_LEVEL_I                       = 'I'
    AML_DEBUG_LOG_LEVEL_W                       = 'W'
    AML_DEBUG_LOG_LEVEL_E                       = 'E'
    AML_DEBUG_LOG_LEVEL_F                       = 'F'


    log_func = print   
    adb_cur_dev = ''

    def log(info, level='D'):
        if AmlCommonUtils.log_func == print:
            AmlCommonUtils.log_func(level + ' ' + info)
        else:
            AmlCommonUtils.log_func(info, level)

    def default_log(info, level):
        print(level + ' ' + info)

    def set_log_fuc(func):
        AmlCommonUtils.log_func = func
    def set_adb_cur_device(dev):
        AmlCommonUtils.adb_cur_dev = dev

    def pre_create_directory(createByModule, moduleEnableArray=0):
        if not Path(AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT).exists():
            AmlCommonUtils.log(AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT + " folder does not exist, create it.", AmlCommonUtils.AML_DEBUG_LOG_LEVEL_I)
            os.makedirs(AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT, 777)
        curTime = time.strftime("%Y%m%d_%H-%M-%S", time.localtime())
        curPullPcTimePath = AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT + "\\" + curTime
        AmlCommonUtils.log('pre_create_directory Current date:' + \
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ', directory is: ' + curPullPcTimePath, AmlCommonUtils.AML_DEBUG_LOG_LEVEL_I)
        os.makedirs(curPullPcTimePath, 777)
        modulePath = curPullPcTimePath
        if createByModule == AmlCommonUtils.AML_DEBUG_MODULE_HOME:
            if moduleEnableArray == 0:
                AmlCommonUtils.log('__pre_create_directory: cfg is null', AmlCommonUtils.AML_DEBUG_LOG_LEVEL_E)
            for index in range(AmlCommonUtils.AML_DEBUG_MODULE_AUDIO, AmlCommonUtils.AML_DEBUG_MODULE_MAX):
                if moduleEnableArray[index] == True:
                        modulePath = curPullPcTimePath + "\\" + AmlCommonUtils.moduleDirPathDict[index]
                        os.makedirs(modulePath, 777)
        else:
            if createByModule in AmlCommonUtils.moduleDirPathDict:
                modulePath = curPullPcTimePath + "\\" + AmlCommonUtils.moduleDirPathDict[createByModule]
                os.makedirs(modulePath, 777)
                AmlCommonUtils.log('pre_create_directory create:' + modulePath)
            else:
                AmlCommonUtils.log('__pre_create_directory: createByModule:' + createByModule + ' invalid.', AmlCommonUtils.AML_DEBUG_LOG_LEVEL_E)
        return curTime

    def get_current_time():
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%H:%M:%S", local_time)
        decimals_t, integers_t =math.modf(ct)
        data_secs = (ct - integers_t) * 1000
        time_stamp = "%s.%03d" % (data_head, data_secs)
        return time_stamp

    def get_path_by_module(time, id):
        return AmlCommonUtils.AML_DEBUG_DIRECOTRY_ROOT + "\\" + time +  "\\" + AmlCommonUtils.moduleDirPathDict[id]

    def logcat_start(callbackFinish='', delayEndS=-1):
        logcatProcThread = threading.Thread(target=AmlCommonUtils.__logcat_wait_thread, args=(callbackFinish, delayEndS,))
        logcatProcThread.setDaemon(True)
        logcatProcThread.start()

    def __logcat_wait_thread(callbackFinish, delayEndS):
        AmlCommonUtils.log('__logcat_wait_thread: time:' + str(delayEndS) + 's, logcat loading...', AmlCommonUtils.AML_DEBUG_LOG_LEVEL_I)
        logcatProcThread = threading.Thread(target=AmlCommonUtils.__logcat_run_thread)
        logcatProcThread.setDaemon(True)
        logcatProcThread.start()
        if delayEndS != -1:
            time.sleep(delayEndS)
            AmlCommonUtils.logcat_stop()
            callbackFinish()

    def __logcat_run_thread():
        AmlCommonUtils.log('__logcat_run_thread: Start logcat+++++')
        AmlCommonUtils.exe_adb_shell_cmd('logcat -G 40M;logcat -c;logcat > ' + AmlCommonUtils.AML_DEBUG_PLATFORM_DIRECOTRY_LOGCAT, True)
        AmlCommonUtils.log('__logcat_run_thread: Exit logcat------')

    def logcat_stop():
        AmlCommonUtils.exe_adb_shell_cmd('ps -ef |grep -v grep|grep logcat| awk \'{print $2}\'|xargs kill -9', True)

    def pull_logcat_to_pc(pc_path):
        AmlCommonUtils.exe_adb_cmd('pull "' + AmlCommonUtils.AML_DEBUG_PLATFORM_DIRECOTRY_LOGCAT + '" ' + pc_path, True)

    def bugreport(path):
        AmlCommonUtils.log('Start bugreport+++++', AmlCommonUtils.AML_DEBUG_LOG_LEVEL_I)
        AmlCommonUtils.exe_adb_cmd('bugreport ' + path, True)
        AmlCommonUtils.log('Exit bugreport-----', AmlCommonUtils.AML_DEBUG_LOG_LEVEL_I)

    def dmesg():
        AmlCommonUtils.log('dmesg', AmlCommonUtils.AML_DEBUG_LOG_LEVEL_I)
        AmlCommonUtils.exe_adb_shell_cmd('rm ' + ' /data/dmesg.txt -rf', True)
        AmlCommonUtils.exe_adb_shell_cmd('dmesg' + ' > /data/dmesg.txt', True)

    def adb_root():
        return AmlCommonUtils.exe_adb_cmd('root', True)

    def adb_remount():
        return AmlCommonUtils.exe_adb_cmd('remount', True)

    def adb_reboot():
        return AmlCommonUtils.exe_adb_cmd('reboot', True)

    def adb_connect_by_ip(ip):
        ret =  AmlCommonUtils.exe_sys_cmd('adb connnect ' + ip, True)
        if 'connected to ' + ip not in ret:
            AmlCommonUtils.log('adb connect ip:' + ip + 'failed !!!', AmlCommonUtils.AML_DEBUG_LOG_LEVEL_E)
            return ''
        dev_name = ''
        dev_list = AmlCommonUtils.get_adb_devices()
        for dev in dev_list:
            if ip in dev:
                dev_name = dev
                break
        if dev_name == '':
            AmlCommonUtils.log('adb_connect_by_ip can\'t find ip:' + ip + ' in the listView.', AmlCommonUtils.AML_DEBUG_LOG_LEVEL_E)
            return  ''
        AmlCommonUtils.set_adb_cur_device(dev_name)
        AmlCommonUtils.adb_root()
        AmlCommonUtils.adb_connect_by_ip(ip)
        AmlCommonUtils.adb_remount()
        return dev_name

    def exe_adb_shell_cmd(cmd, bprint=False):
        return AmlCommonUtils.exe_adb_cmd('shell "' + cmd + '"', bprint)

    def exe_adb_cmd(cmd, bprint=False):
        if AmlCommonUtils.adb_cur_dev != '':
            return AmlCommonUtils.exe_sys_cmd('adb -s ' + AmlCommonUtils.adb_cur_dev + ' ' + cmd , bprint)
        else:
            return AmlCommonUtils.exe_sys_cmd('adb ' + cmd , bprint)

    def exe_sys_cmd(cmd, bprint=False):
        try:
            ret = ''
            proc = subprocess.Popen(cmd, shell=True, 
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
            proc.stdin.close()
            for line in iter(proc.stdout.readline, b''):
                temp_str = line.strip().decode('utf-8')
                if temp_str != '\n' and temp_str != '':
                    ret = ret + temp_str + '\n'
                if bprint:
                    AmlCommonUtils.log(temp_str)
            proc.wait()
            proc.stdout.close()
            if bprint == True:
                if proc.returncode == RET_VAL_SUCCESS:
                    AmlCommonUtils.log(cmd + ' --> Success')
                else:
                    AmlCommonUtils.log(cmd + ' --> Failed' + ', ret:'+ str(proc.returncode), AmlCommonUtils.AML_DEBUG_LOG_LEVEL_F)
            return ret
        except:
            AmlCommonUtils.log(cmd + ' --> Exception happend!!!', AmlCommonUtils.AML_DEBUG_LOG_LEVEL_F)
            return ''

    def get_adb_devices():
        devs_list = []
        ret = AmlCommonUtils.exe_adb_cmd('devices', True)
        i = 0
        devs = ret.split('\n')
        for dev in devs:
            dev.replace('\n', '')
            # The i=0 first line is not adb device id.
            if i > 0 and dev != '':
                id = dev.split()[0]
                devs_list.append(id)
                # print('id:' + id)
            i += 1
        return devs_list

    @staticmethod
    def zip_compress(srcPathName, targetPathName):
        z = zipfile.ZipFile(targetPathName,'w',zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(srcPathName):
            fpath = dirpath.replace(srcPathName,'')
            fpath = fpath and fpath + os.sep or ''
            for filename in filenames:
                z.write(os.path.join(dirpath, filename),fpath+filename)
        z.close()

    # 删除指定目录下的所有文件以及文件夹
    @staticmethod
    def del_all_file_and_direcotry(filepath):
        del_list = os.listdir(filepath)
        for f in del_list:
            file_path = os.path.join(filepath, f)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)

    @staticmethod
    def del_spec_file(filePath):
        if os.path.exists(filePath):
            try:
                os.remove(filePath)
            except:
                AmlCommonUtils.log('del_spec_file delete file:' + filePath + ' failed.', AmlCommonUtils.AML_DEBUG_LOG_LEVEL_F)


