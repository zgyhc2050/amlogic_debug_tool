from src.common.aml_common_utils import AmlCommonUtils
from pathlib import Path
from threading import Thread
from PyQt5.QtCore import *
import zipfile, os, requests, sys

class AmlDebugBurn:
    def __init__(self, ui):
        self.log = ui.log
        self.ui = ui
        self.stop = True

    def initBurn(self, url):
        self.thread = procThread(self, url)
        return self.thread

    def startBurn(self):
        self.stop = False
        if self.thread != None:
            self.thread.start()

    def stopBurn(self):
        self.stop = True
        if self.thread != None:
            self.thread.systemProcStop.stop = True
            self.thread.wait()

class procThread(QThread):
    burnSetCurButtonStatusSignal = pyqtSignal(str)
    burnSetCurProcessFormatSignal = pyqtSignal(str)
    burnSetCurProcessMaxValueSignal = pyqtSignal(int)
    burnSetCurProcessSignal = pyqtSignal(int)
    burnSetRefreshcurStatusSignal = pyqtSignal(str)
    def __init__(self, burn, url, parent=None):
        super().__init__(parent)
        self.url = url
        self.burn = burn
        self.log = burn.log
        self.systemProcStop = AmlCommonUtils.ForceStop()

    def run(self):
        self.__burnProcess()
        self.__burnFinish()
    
    def __burnProcess(self):
        if self.url == '':
            self.log.e('__burnProcess: URL is empty.')
            return
        ## d:\aml_debug\burn
        localPathDir = AmlCommonUtils.get_cur_root_path() + '\\burn'
        if not Path(localPathDir).exists():
            os.makedirs(localPathDir)

        # ohm-fastboot-flashall-20220301.zip
        serverFastbootFileName = self.get_fastboot_zip_name(self.url)
        if serverFastbootFileName == '':
            self.log.e('__burnProcess: cannot find fastboot name in URL:' + self.url)
            return
        localFastbootFileName = serverFastbootFileName

        ## download ohm-fastboot-flashall-20220301.zip to localPathDir(d:\aml_debug\burn\)
        if self.url[-1] != '/':
            self.url = self.url + '/'
        ret = self.downloadFileByUrl(self.url + serverFastbootFileName, localPathDir, localFastbootFileName)
        if self.burn.stop or ret != 0:
            return

        ## unzip ohm-fastboot-flashall-20220301.zip to unzipPathDir(d:\aml_debug\burn\ohm-fastboot-flashall-20220301\)
        unzipPathDir = localPathDir + '\\' + localFastbootFileName[: -4]
        ret = self.unzipFiles(unzipPathDir, localPathDir + '\\' + localFastbootFileName)
        if self.burn.stop or ret != 0:
            return

        self.burnSetRefreshcurStatusSignal.emit('Burning ' + localFastbootFileName + ' ...')
        self.burnSetCurProcessMaxValueSignal.emit(0)
        
        AmlCommonUtils.exe_sys_cmd(cmd=unzipPathDir + '\\' + 'flash-all.bat', bprint=True, path=unzipPathDir, forceStop=self.systemProcStop)
        self.burnSetRefreshcurStatusSignal.emit('Burn compelete.')
    
    
    def downloadFileByUrl(self, urlAndFileName, localPathDir, localFastbootFileName):
        if urlAndFileName is None or localPathDir is None or localFastbootFileName is None:
            self.log.e('downloadFileByUrl: invalid param')
            return -1
        folder = os.path.exists(localPathDir)
        if not folder:
            self.log.e('downloadFileByUrl: not found the directory:' + localPathDir)
            return -1

        res = requests.get(urlAndFileName, stream=True)
        if res.status_code != 200:
            self.log.e('downloadFileByUrl: requests.get fail ret:' + res.status_code)
            return -1

        totalSize = int(int(res.headers["Content-Length"]) / 1024 + 0.5)
        filePath = os.path.join(localPathDir, localFastbootFileName)
        peroidSizeByte = 1024 * 1024
        writteCntByte = 0
        
        self.burnSetRefreshcurStatusSignal.emit('Downloading file: ' + localFastbootFileName + ' size: ' + str(totalSize) + 'KB')
        self.burnSetCurProcessMaxValueSignal.emit(totalSize)
        self.burnSetCurProcessFormatSignal.emit('%v KB / ' + str(totalSize) + 'KB')
        fileFd = open(filePath, 'wb')
        self.log.i('downloadFileByUrl: {}, current size: {}KB' .format(localFastbootFileName, totalSize))
        for chunk in res.iter_content(chunk_size=peroidSizeByte):
            if self.burn.stop:
                fileFd.close()
                return -1
            fileFd.write(chunk)
            writteCntByte = writteCntByte + peroidSizeByte
            curProcess = int(100 * (writteCntByte / 1024) / totalSize)
            self.burnSetCurProcessSignal.emit(int(writteCntByte / 1024))
            # print('cur: ' + str(100 * (writteCntByte / 1024) / totalSize) + '%, ' + str(writteCntByte/1024) + '/' + str(totalSize))
        fileFd.close()
        self.log.i('downloadFileByUrl: ' + localFastbootFileName + ' Download compelete!')
        return 0

    def unzipFiles(self, unzipPathDir, filePath):
        # unzipPathDir: (d:\aml_debug\burn\ohm-fastboot-flashall-20220301\)
        # filePath: (d:\aml_debug\burn\ohm-fastboot-flashall-20220301.zip)
        if not Path(unzipPathDir).exists():
            os.makedirs(unzipPathDir)
        zipFileHandle = zipfile.ZipFile(filePath)
        fileCnt = len(zipFileHandle.namelist())
        self.log.d('unzipFiles: unzip ' + str(fileCnt) + ' files...')
        self.burnSetCurProcessMaxValueSignal.emit(fileCnt)
        self.burnSetCurProcessFormatSignal.emit('%v / ' + str(fileCnt))
        i = 0
        for file in zipFileHandle.namelist():
            if self.burn.stop:
                return -1
            i = i + 1
            self.burnSetRefreshcurStatusSignal.emit('Unzip file: ' + file )
            zipFileHandle.extract(file, unzipPathDir)
            self.burnSetCurProcessSignal.emit(i)
        self.log.d('unzipFiles: unzip file: ' + filePath + ' finished.')
        return 0

    def get_fastboot_zip_name(self, url):
        # URL: http://firmware.amlogic.com/shanghai/image/android/Android-S/patchbuild/2022-03-01/ohm-userdebug-android32-kernel64-GTV-5272/
        index = url.find('20')
        if index == -1:
            self.log.w('get_fastboot_zip_name: not find the str 20, url invalid')
            return ''
        if url[index + 4] != '-':
            self.log.w('get_fastboot_zip_name: not find the date in URL, url invalid')
            return ''

        # date: 20220301
        new_str = url[index :]
        if len(new_str) < len('20xx-xx-xx'):
            self.log.w('get_fastboot_zip_name: not find the date in URL, url invalid, new_str:' + new_str)
            return ''

        date = url[index : index + len('20xx')] + url[index + len('20xx-') : index + len('20xx-xx')] + url[index + len('20xx-xx-') : index + len('20xx-xx-xx')]
        # new_str: ohm-userdebug-android32-kernel64-GTV-5272/
        new_str = url[index + 11 :]
        index = new_str.find('-')
        # device_name: ohm
        device_name = new_str[: index]
        # ohm-fastboot-flashall-20220301.zip
        fastboot_name_zip = device_name + '-fastboot-flashall-' + date + '.zip'
        self.log.i('get_fastboot_zip_name: find fastboot name:' + fastboot_name_zip)
        print('get_fastboot_zip_name: find fastboot name:' + fastboot_name_zip)
        return fastboot_name_zip

    def __burnFinish(self):
        self.log.i('__burnFinish: burn compelete ^_^')
        self.burnSetCurButtonStatusSignal.emit('Start')
        self.burnSetCurProcessFormatSignal.emit('%p%')
        self.burnSetCurProcessMaxValueSignal.emit(100)
        self.burnSetCurProcessSignal.emit(0)
        self.burnSetRefreshcurStatusSignal.emit('')
        self.burn = None