import os, subprocess, sys
import zipfile, os, requests, sys
from constant import AmlDebugConstant
from threading import Thread

class defaultLog:
    def v(self, info):
        print('V ' + info)
    def d(self, info):
        print('D ' + info)
    def i(self, info):
        print('I ' + info)
    def w(self, info):
        print('W ' + info)
    def e(self, info):
        print('E ' + info)
    def f(self, info):
        print('F ' + info)

class httpDownload(Thread):
    def __init__(self, url, path, name, log=print):
        super().__init__()
        self.log = log
        if log == print:
            self.log = defaultLog()
        self.url = url
        self.path = path
        self.name = name
        self._return = 0
        self.stop = True

    def run(self):
        self._return = self.httpDownloadFile()
    def start(self):
        self.stop = False
        super().start()   
    def stop(self):
        self.stop = True
        super().join()
    def join(self):
        super().join()
        return self._return

    def httpDownloadFile(self):
        try:
            if self.url == '':
                self.log.e('httpDownloadFile: URL is empty.')
                return -1
            if not os.path.exists(self.path) or os.path.isfile(self.path):
                self.log.e('[httpDownloadFile] ' + self.path + ' not exists')
                return -1, ''
            res = requests.get(self.url, stream=True)
            if res.status_code != 200:
                self.log.e('httpDownloadFile: request file:' + self.url + ' fail')
                return -1

            totalSize = int(int(res.headers["Content-Length"]) / 1024 + 0.5)
            filePath = os.path.join(self.path, self.name)
            peroidSizeByte = 1024 * 1024
            writteCntByte = 0
            
            self.log.i('%v KB / ' + str(totalSize) + 'KB')
            fileFd = open(filePath, 'wb')
            self.log.i('httpDownloadFile: ' + "aml_debug_tool.exe" + ', size: ' + str(totalSize) + ' KB')
            for chunk in res.iter_content(chunk_size=peroidSizeByte):
                if self.stop:
                    fileFd.close()
                    return -1
                fileFd.write(chunk)
                writteCntByte = writteCntByte + peroidSizeByte
                self.log.d('cur: ' + str(100 * (writteCntByte / 1024) / totalSize) + '%, ' + str(writteCntByte/1024) + '/' + str(totalSize))
            fileFd.close()
            self.log.i('httpDownloadFile: Download compelete!')
            return 0
        except Exception as result:
            self.log.f('httpDownloadFile somes except happed. =_= result:' + result)
            return -1

def exe_sys_cmd(cmd, bprint=False):
    try:
        proc = subprocess.Popen(cmd, shell=True, 
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
        proc.stdin.close()
        proc.stdout.close()
    except:
        print('[online_updater] ' + cmd + ' --> Exception  happend!!!')

if __name__ == '__main__':
    print('[online_updater] Updating the software......')
    exe_type = ''
    if len(sys.argv) < 2:
        print('[online_updater] No paramters available! (/_\)')
    else:
        exe_type = sys.argv[1]
        print('[online_updater] cur soft exe type:' + exe_type)

##########################delete old ini key##################################
    import configparser
    from pathlib import Path
    oldIniKey = [
        'push_dolby_src_path',
        'push_dts_src_path',
        'push_ms12_src_path',
        'push_dolbydts_dst_path',
        'push_ms12_dst_path',
        'push_custom1_src_path',
        'push_custom2_src_path',
        'push_custom3_src_path',
        'push_custom4_src_path',
        'push_custom5_src_path',
        'push_custom1_dst_path',
        'push_custom2_dst_path',
        'push_custom3_dst_path',
        'push_custom4_dst_path',
        'push_custom5_dst_path',
        'pull_custom1_src_path',
        'pull_custom2_src_path',
        'pull_custom3_src_path',
        'pull_custom4_src_path',
        'pull_custom1_dst_path',
        'pull_custom2_dst_path',
        'pull_custom3_dst_path',
        'pull_custom4_dst_path',
    ]
    try:
        PATH_INI = 'd:\\aml_debug\\config.ini'
        if Path(PATH_INI).exists():
            parser = configparser.ConfigParser()
            parser.read(PATH_INI)
            for key in oldIniKey:
                parser.remove_option('AM_SYS_OPERATION', key)
            with open(PATH_INI, 'w+') as file:
                parser.write(file)
    except:
        print('[online_updater] cur soft exe type:' + exe_type)
#################################################################################

    upgrade_file_name = 'aml_debug_tool.exe'
    if exe_type == AmlDebugConstant.AML_DEBUG_TOOL_COMPILE_EXE_TYPE_INSTALLER:
        upgrade_file_name = 'Amlogic Debug Setup.exe'
    print('[online_updater] Downloading ' + upgrade_file_name + ' ......')

    print('[online_updater] cur path:' + os.getcwd())
    download = httpDownload('http://10.28.11.52:8080/amlogic_tools/Aml_Debug_Tool/' + upgrade_file_name, os.getcwd(), upgrade_file_name)
    download.start()
    ret = download.join()
    if (ret != 0):
        print('[online_updater] download online_updater.exe fail')
        exit(0)
    # upgrade_exe_file_path_server = "\\\\10.28.49.68\\amlogic debug tool\\" + upgrade_file_name
    # os.system('copy "' + upgrade_exe_file_path_server +  '" .\\')
    print('[online_updater] Download Complete ^_^')
    print('[online_updater] New software is being launched.')
    exe_sys_cmd(upgrade_file_name)
    print('[online_updater] UPDATE COMPLETE ^_^')

# Compile to an executable EXE package: online_updater.exe
# Cmd:  pyinstaller.exe -Fw .\res\script\online_updater.py --noconfirm