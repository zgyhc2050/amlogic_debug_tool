from src.common.aml_common_utils import AmlCommonUtils
from pathlib import Path
from threading import Thread
from PyQt5.QtCore import *
import zipfile, os, requests, sys

class AmlDebugBurn:
    AML_BURN_SAVE_FILE_ENUM_SAVE_ALL        = 'Save All'
    AML_BURN_SAVE_FILE_ENUM_SAVE_LATEST     = 'Save the latest'
    AML_BURN_SAVE_FILE_ENUM_DELETE_ALL      = 'Delete current'

    def __init__(self, ui):
        self.log = ui.log
        self.ui = ui
        self.url = ''
        self.mode = ''
        self.stop = True
        self.AML_DEBUG_BURN_DIR_PATH = AmlCommonUtils.get_cur_root_path() + '\\burn'

    def initBurn(self, url, mode):
        self.url = url
        self.mode = mode
        self.thread = procThread(self)
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
    
    def openBurnDir(self):
        localPathDir = self.AML_DEBUG_BURN_DIR_PATH
        if not Path(localPathDir).exists():
            self.log.i('openBurnDir: localPathDir:' + localPathDir + ', not exist')
            return
        os.startfile(localPathDir) 

class procThread(QThread):
    burnSetCurButtonStatusSignal = pyqtSignal(str)
    burnSetCurProcessFormatSignal = pyqtSignal(str)
    burnSetCurProcessMaxValueSignal = pyqtSignal(int)
    burnSetCurProcessSignal = pyqtSignal(int)
    burnSetRefreshcurStatusSignal = pyqtSignal(str)
    def __init__(self, burn):
        super().__init__()
        self.burn = burn
        self.url = burn.url
        self.mode = burn.mode
        self.log = burn.log
        self.systemProcStop = AmlCommonUtils.ForceStop()
        self.urlPaser = AmlDebugBurnUrlPaser(self.log)

    def run(self):
        self.__burnProcess()
        self.__burnFinish()
    
    def __burnProcess(self):
        try:
            if self.url == '':
                self.log.e('__burnProcess: URL is empty.')
                return
            ## d:\aml_debug\burn
            localPathDir = self.burn.AML_DEBUG_BURN_DIR_PATH
            if not Path(localPathDir).exists():
                os.makedirs(localPathDir)
            if self.mode == AmlDebugBurn.AML_BURN_SAVE_FILE_ENUM_SAVE_LATEST:
                AmlCommonUtils.delAllFileAndDir(localPathDir)

            # serverFastbootFileName: ohm-fastboot-flashall-20220301.zip, versionID: 5272
            if self.urlPaser.paserUrl(self.url) != 0:
                self.log.e('__burnProcess: fail to paser URL')
                return

            serverFastbootFileName1 = self.urlPaser.getFastbootZipName()
            serverFastbootFileName2 = self.urlPaser.getFastbootZipNameShort()
            if serverFastbootFileName1 == '' and serverFastbootFileName2 == '':
                self.log.e('__burnProcess: cannot find fastboot name in URL:' + self.url)
                return
            # localFastbootFileName: ohm-fastboot-flashall-20220301-5272.zip
            localFastbootFileName = serverFastbootFileName1[: -4] + '-' + self.urlPaser.getIndexId() + '.zip'

            tryCnt = 0
            while True:
                ## download ohm-fastboot-flashall-20220301.zip to localPathDir(d:\aml_debug\burn\)
                if self.url[-1] != '/':
                    self.url = self.url + '/'
                ret = self.downloadFileByUrl(self.url, serverFastbootFileName1, serverFastbootFileName2, localPathDir, localFastbootFileName)
                if self.burn.stop or ret != 0:
                    # print('stop: '  + str(self.burn.stop) + ' ret:' + str(ret))
                    return
                tryCnt = tryCnt + 1

                ## unzip ohm-fastboot-flashall-20220301.zip to unzipPathDir(d:\aml_debug\burn\ohm-fastboot-flashall-20220301\)
                unzipPathDir = localPathDir + '\\' + localFastbootFileName[: -4]
                localFileNameAndPath = localPathDir + '\\' + localFastbootFileName
                ret = self.unzipFiles(unzipPathDir, localFileNameAndPath)
                if self.burn.stop or ret != 0:
                    if tryCnt > 1:
                        self.log.e('__burnProcess: try download 2 times fail')
                        return
                    else:
                        if os.path.exists(localFileNameAndPath):
                            os.remove(localFileNameAndPath)  
                        else:
                            self.log.w('__burnProcess: not find the bade file:' + localFileNameAndPath)
                        self.log.w('__burnProcess: unzipFiles fail, retry...')
                else:
                    break
            self.burnSetRefreshcurStatusSignal.emit('Burning ' + localFastbootFileName + ' ...')
            self.burnSetCurProcessMaxValueSignal.emit(0)

            batCmdPath = unzipPathDir + '\\' + 'flash-all.bat'
            self.__specialHandling(batCmdPath, self.urlPaser);

            AmlCommonUtils.exe_sys_cmd(cmd=batCmdPath, bprint=True, path=unzipPathDir, forceStop=self.systemProcStop)
            self.burnSetRefreshcurStatusSignal.emit('Burn compelete.')
            self.clearEnv(localFileNameAndPath, unzipPathDir)
        except:
            self.log.f('__burnProcess: somes except happed. =_=')
    
    def downloadFileByUrl(self, url, serverFilePathAndName1, serverFilePathAndName2, localPathDir, localFastbootFileName):
        try:
            if serverFilePathAndName1 is None or serverFilePathAndName2 is None or localPathDir is None \
                or localFastbootFileName is None or url is None:
                self.log.e('downloadFileByUrl: invalid param')
                return -1
            folder = os.path.exists(localPathDir)
            if not folder:
                self.log.e('downloadFileByUrl: not found the directory:' + localPathDir)
                return -1

            url1 = url + serverFilePathAndName1
            url2 = url + serverFilePathAndName2

            if os.path.isfile(localPathDir + '\\' + localFastbootFileName):
                self.log.i('downloadFileByUrl: ' + localPathDir + '\\' + localFastbootFileName + ' alread existed.')
                return 0

            res = requests.get(url1, stream=True)
            if res.status_code != 200:
                self.log.w('downloadFileByUrl: request file:' + serverFilePathAndName1 + ' fail')
                self.log.i('downloadFileByUrl: now retry request file:' + serverFilePathAndName2)
                res = requests.get(url2, stream=True)
                if res.status_code != 200:
                    self.log.e('downloadFileByUrl: retry request fail ret:' + str(res.status_code))
                    return -1
            totalSize = int(int(res.headers["Content-Length"]) / 1024 + 0.5)
            filePath = os.path.join(localPathDir, localFastbootFileName)
            peroidSizeByte = 1024 * 1024
            writteCntByte = 0
            
            self.burnSetRefreshcurStatusSignal.emit('Downloading file: ' + localFastbootFileName + ' size: ' + str(totalSize) + 'KB')
            self.burnSetCurProcessMaxValueSignal.emit(totalSize)
            self.burnSetCurProcessFormatSignal.emit('%v KB / ' + str(totalSize) + 'KB')
            fileFd = open(filePath, 'wb')
            self.log.i('downloadFileByUrl: ' + serverFilePathAndName1 + ', size: ' + str(totalSize) + ' KB')
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
        except:
            self.log.f('downloadFileByUrl: somes except happed. =_=')
            return -1

    def unzipFiles(self, unzipPathDir, filePath):
        try:
            # unzipPathDir: (d:\aml_debug\burn\ohm-fastboot-flashall-20220301\)
            # filePath: (d:\aml_debug\burn\ohm-fastboot-flashall-20220301.zip)
            self.log.d('unzipFiles: unzip ' + filePath)
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
        except:
            self.log.f('unzipFiles: somes except happed. =_=')
            return -1

    def clearEnv(self, zipFile, directory):
        if self.mode == AmlDebugBurn.AML_BURN_SAVE_FILE_ENUM_DELETE_ALL:
            if os.path.exists(zipFile):
                os.remove(zipFile)  
            else:
                self.log.w('clearEnv: not find the file:' + zipFile)
            AmlCommonUtils.delAllFileAndDir(directory, True)

    def __burnFinish(self):
        self.log.i('__burnFinish: burn compelete ^_^')
        self.burnSetCurButtonStatusSignal.emit('Start')
        self.burnSetCurProcessFormatSignal.emit('%p%')
        self.burnSetCurProcessMaxValueSignal.emit(100)
        self.burnSetCurProcessSignal.emit(0)
        self.burnSetRefreshcurStatusSignal.emit('')
        self.burn = None

    def  __specialHandling(self, batFile, urlPaser):
        try:
            if urlPaser.getAndroidVersion() == 'P' and urlPaser.getChipName() == 't982_ar301':
                self.log.i('__specialHandling: Android P + T982 need modify bat file...')
                with open(batFile, '+r') as f:
                    t = f.read()
                    t = t.replace('fastboot flash system system.img', 'fastboot flash -S 128M system system.img')
                    t = t.replace('fastboot flash vendor vendor.img', 'fastboot flash -S 128M vendor vendor.img')
                    f.seek(0, 0)    
                    f.write(t)
        except:
            self.log.f('__specialHandling: somes except happed. =_=')

class AmlDebugBurnUrlPaser:
    def __init__(self, log):
        self.log = log
        self.__androidVer = ''
        self.__date = ''
        self.__chipUrlName = ''
        self.__chipUrlNameShort = ''
        self.__indexId = ''

    def getAndroidVersion(self):
        return self.__androidVer
    def getDate(self):
        return self.__date
    def getChipName(self):
        return self.__chipUrlName
    def getChipNameShort(self):
        return self.__chipUrlNameShort
    def getIndexId(self):
        return self.__indexId
    def getFastbootZipName(self):
        # oppencas_irdeto-fastboot-flashall-20220311.zip
        return self.__chipUrlName + '-fastboot-flashall-' + self.__date + '.zip'
    def getFastbootZipNameShort(self):
        # oppencas-fastboot-flashall-20220311.zip
        return self.__chipUrlNameShort + '-fastboot-flashall-' + self.__date + '.zip'

    def paserUrl(self, url):
        try:
            # URL: http://firmware.amlogic.com/shanghai/image/android/Android-S/patchbuild/2022-03-01/ohm-userdebug-android32-kernel64-GTV-5272/
            index = url.find('Android-')
            if index == -1:
                self.log.w('paserUrl: not find Android- in url')
                return -1
            self.__androidVer = url[index + len('Android-')]

            url = url.strip(' ')
            index = url.find('20')
            if index == -1:
                self.log.w('paserUrl: not find the str 20, url invalid')
                return -1
            # 2022-
            if url[index + 4] != '-':
                self.log.w('paserUrl: not find the date in URL, url invalid')
                return -1

            # date: 20220301
            tempStr = url[index :]
            if len(tempStr) < len('20xx-xx-xx'):
                self.log.w('paserUrl: not find the date in URL, url invalid, date:' + tempStr)
                return -1

            versionIdStartIndex = url.rfind('-')
            if versionIdStartIndex == -1:
                self.log.w('paserUrl: not find the str "-", url invalid')
                return -1
            # 5272
            self.__indexId = url[versionIdStartIndex + 1 :].strip('/')
            if not self.__indexId.isdigit():
                self.log.w('paserUrl: not find the version ID in URL, url invalid, ID:' + self.__indexId)
                return -1

            self.__date = url[index : index + len('20xx')] + url[index + len('20xx-') : index + len('20xx-xx')] + url[index + len('20xx-xx-') : index + len('20xx-xx-xx')]
            # tempStr: ohm-userdebug-android32-kernel64-GTV-5272/
            tempStr = url[index + 11 :]
            index = tempStr.find('-')

            # __chipUrlName: oppencas_irdeto
            self.__chipUrlName = tempStr[: index]
            index = self.__chipUrlName.find('_')
            # __chipUrlNameShort: oppencas
            self.__chipUrlNameShort = tempStr[: index]
            
            self.log.i('paserUrl: Android-' + self.__androidVer + ', chip:' + self.__chipUrlName + ', chipShort:' + self.__chipUrlNameShort + ', index:' + self.__indexId)
            print('paserUrl: Android-' + self.__androidVer + ', chip:' + self.__chipUrlName + ', chipShort:' + self.__chipUrlNameShort + ', index:' + self.__indexId)
            return 0
        except:
            self.log.f('paserUrl: somes except happed. =_=')
            return -1