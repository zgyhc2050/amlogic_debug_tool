import os, subprocess, sys
from constant import AmlDebugConstant

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

    upgrade_file_name = 'aml_debug_tool.exe'
    if exe_type == AmlDebugConstant.AML_DEBUG_TOOL_COMPILE_EXE_TYPE_INSTALLER:
        upgrade_file_name = 'Amlogic Debug Setup.exe'
    print('[online_updater] Downloading ' + upgrade_file_name + ' ......')
    upgrade_exe_file_path_server = "\\\\10.28.49.68\\amlogic debug tool\\" + upgrade_file_name
    os.system('copy "' + upgrade_exe_file_path_server +  '" .\\')
    print('[online_updater] Download Complete ^_^')
    print('[online_updater] New software is being launched.')
    exe_sys_cmd(upgrade_file_name)
    print('[online_updater] UPDATE COMPLETE ^_^')


