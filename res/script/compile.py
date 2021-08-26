import os, sys, shutil, getpass, getopt, time

NSIS_COMPILE_EXE_PATH = 'C:\Program Files (x86)/NSIS/makensisw.exe'
COMPILE_SCRIPT_EXE_ICO_PATH = './res/tool/compile.nsi'
EXE_ICO_PATH = './res/debug.ico'
AMLOGIC_DEBUG_TOOL_MAIN_PYTHON_PATH = './aml_debug_tool.py'


COMPILE_EXE_USER_NAME = getpass.getuser()
COMPILE_EXE_USER_TIME = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
COMPILE_EXE_VERSION   = '1.0.4'

AML_DEBUG_TOOL_BASE_ROW                     = 2
AML_DEBUG_TOOL_ABOUT_VERSION_ROW            = AML_DEBUG_TOOL_BASE_ROW + 1
AML_DEBUG_TOOL_ABOUT_USERE_ROW              = AML_DEBUG_TOOL_BASE_ROW + 2
AML_DEBUG_TOOL_ABOUT_DATE_ROW               = AML_DEBUG_TOOL_BASE_ROW + 3
AML_DEBUG_TOOL_ABOUT_COMMIT_ROW             = AML_DEBUG_TOOL_BASE_ROW + 4

def generating_version_info():
    read_constant_py = open('./res/script/constant.py', 'r', encoding = 'utf-8')
    temp_write_constant_py = open('./res/script/constant_temp.py', 'w', encoding = 'utf-8')
    row_num = 0
    for raw_str in read_constant_py:
        row_num += 1
        if row_num == AML_DEBUG_TOOL_ABOUT_VERSION_ROW:
            raw_str = "    AML_DEBUG_TOOL_ABOUT_VERSION            = '" + COMPILE_EXE_VERSION + "'\n"
        elif row_num == AML_DEBUG_TOOL_ABOUT_USERE_ROW:
            raw_str = "    AML_DEBUG_TOOL_ABOUT_USERE              = '" + COMPILE_EXE_USER_NAME + "'\n"
        elif row_num == AML_DEBUG_TOOL_ABOUT_DATE_ROW:
            raw_str = "    AML_DEBUG_TOOL_ABOUT_DATE               = '" + COMPILE_EXE_USER_TIME + "'\n"
        elif row_num == AML_DEBUG_TOOL_ABOUT_COMMIT_ROW:
            raw_str = "    AML_DEBUG_TOOL_ABOUT_COMMIT             = '" + '***' + "'\n"
        temp_write_constant_py.write(raw_str)
    read_constant_py.close()
    temp_write_constant_py.close()
    os.remove('./res/script/constant.py')
    os.rename('./res/script/constant_temp.py', './res/script/constant.py')

    read_nsi = open('./res/tool/compile.nsi', 'r')
    temp_write_nsi = open('./res/tool/compile_temp.nsi', 'w')
    row_num = 0
    for raw_str in read_nsi:
        row_num += 1
        if row_num == 5:
            raw_str = '!define PRODUCT_VERSION "' + COMPILE_EXE_VERSION + '"\n'
        temp_write_nsi.write(raw_str)
    read_nsi.close()
    temp_write_nsi.close()
    os.remove('./res/tool/compile.nsi')
    os.rename('./res/tool/compile_temp.nsi', './res/tool/compile.nsi')

def pyinstaller_compile(type):
    os.system('@echo y | pyinstaller.exe -' + type + 'w ' + AMLOGIC_DEBUG_TOOL_MAIN_PYTHON_PATH + ' -i ' + EXE_ICO_PATH)

def compile_executable():
    pyinstaller_compile('F')

def compile_installation_package():
    pyinstaller_compile('D')
    os.system('"' + NSIS_COMPILE_EXE_PATH + '" ' + COMPILE_SCRIPT_EXE_ICO_PATH)
    if os.path.exists('./res/tool/Amlogic Debug Setup.exe'):
        if os.path.exists('./dist/Amlogic Debug Setup.exe'):
            os.remove('./dist/Amlogic Debug Setup.exe')
        shutil.move('./res/tool/Amlogic Debug Setup.exe', './dist')
        print('[compile_installation_package:] ./dist/Amlogic Debug Setup.exe Compile successfully')
    else:
        print('[compile_installation_package:] ./res/tool/Amlogic Debug Setup.exe File not generated')

def compile(target):
    if target == 'F':
        print('[compile:] compile_executable')
        compile_executable()
    elif target == 'D':
        print('[compile:] compile_installation_package')
        compile_installation_package()
    elif target == 'A' or target == '':
        print('[compile:] compile all exe')
        compile_executable()
        compile_installation_package()
    else:
        print('[compile:] unsupport target param:' + target)

def help_param(param):
    if param == 'H' or param == 'help_param':
        print('eg: -H t')
        print('  t:    compile target')
        print('  h:    help info')
        print('  H:    help paramter info')
    elif param == 't' or param == 'target':
        print('eg: -t F')
        print('  F:    compile executable')
        print('  D:    compile installation_package')
        print('  A:    compile executable and installation_package')
    else:
        print('[help_param:] unsupport param:' + param)

def help():
    print('Usage: ./compile.py [-t target]\n')
    print('General options:')
    print('  -t, --target=<target>            Set the target type.')

def main(argv):
    try:
        options, args = getopt.getopt(argv, 'ht:H:', ['help', 'type=', 'help_param'])
    except getopt.GetoptError:
        print('except GetoptError')
        sys.exit()

    target = ''
    for option, value in options:
        if option in ('-h', '--help'):
            help()
            return
        if option in ('-H', '--help_param'):
            help_param(value)
            return
        if option in ('-t', '--target'):
            target = value

    generating_version_info()
    compile(target)

if __name__ == '__main__':
    main(sys.argv[1:])
    os.system('pause')