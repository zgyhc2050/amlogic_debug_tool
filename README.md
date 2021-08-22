# Amlogic_Debug_Tool



convert ico picture file to *.py:

    pyrcc5 -o object[ico_debug.py] source ico[debug.ico] 


Compile to an executable EXE package:

    pyinstaller.exe -Fw .\aml_debug_tool.py -i .\res\debug.ico

Compile to multiple files:

    pyinstaller.exe -Dw .\aml_debug_tool.py -i .\res\debug.ico