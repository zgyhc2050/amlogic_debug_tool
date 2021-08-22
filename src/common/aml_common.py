import os
import threading
import shutil
import subprocess
import zipfile

from threading import Thread

RET_VAL_SUCCESS         = 0
RET_VAL_FAIL            = -1
RET_VAL_EXCEPTION       = -2

class AmlThread(threading.Thread):

    def __init__(self, func, thread_num=0, timeout=1.0):
        super(AmlThread, self).__init__()
        self.thread_num = thread_num
        self.__subFuc = func
        self.__stopped = False
        self.timeout = timeout

    def run(self):
        subthread = threading.Thread(target=self.__subFuc, args=())
        subthread.setDaemon(True)
        subthread.start()

        while not self.__stopped:
            subthread.join(self.timeout)

        print('Thread __stopped')

    def stop(self):
        self.__stopped = True

    def isStopped(self):
        return self.__stopped


def exe_adb_cmd_default_print(str):
    print(str)

class AmlCommon:
    AML_DEBUG_DIRECOTRY_ROOT = "d:\\aml_debug"
    AML_DEBUG_DIRECOTRY_CONFIG = AML_DEBUG_DIRECOTRY_ROOT + '\\config.ini'
    @staticmethod
    def exe_adb_cmd(cmd, bprint=False, callback_print=exe_adb_cmd_default_print):
        return AmlCommon.exe_sys_cmd(cmd, bprint, callback_print)

    @staticmethod
    def exe_sys_cmd(cmd, bprint=False, callback_print=exe_adb_cmd_default_print):
        try:
            ret = subprocess.Popen(cmd, shell=True)
            ret.wait()
            if bprint == True:
                if ret.returncode == RET_VAL_SUCCESS:
                    callback_print(cmd + ' --> Success')
                else:
                    callback_print(cmd + ' --> Failed' + ', ret:'+ str(ret.returncode))
            return ret.returncode
        except:
            callback_print(cmd + ' --> Exception happend!!!')
            return RET_VAL_EXCEPTION

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

