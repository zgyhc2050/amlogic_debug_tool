import threading
import tkinter
import time
import subprocess
import tkinter as tk

from tkinter import ttk
from tkinter.constants import DISABLED, NORMAL
from threading import Thread

import aml_debug_audio


root = tkinter.Tk()
#root.iconbitmap('tool.ico')
root.title('Amlogic Debug Tool')
root.wm_attributes("-alpha", 0.95)  # 设置GUI透明度(0.0~1.0)
root.wm_attributes("-topmost", True)  # 设置GUI置顶
root.geometry('650x400') # 设定窗口的大小(长 * 宽)
root.attributes('-topmost', False)  # 窗口置顶false

captureMode = tkinter.IntVar()
debugInfoEnable = tkinter.IntVar()
dumpDataEnable = tkinter.IntVar()
logcatEnable = tkinter.IntVar()
printDebugEnable = tkinter.IntVar()

captureMode.set(aml_debug_audio.DEFAULT_CAPTURE_MODE)
debugInfoEnable.set(1)
dumpDataEnable.set(1)
logcatEnable.set(1)
printDebugEnable.set(0)

audioDebug = aml_debug_audio.AmlAudioDebug()

def selection_capture_mode():
    change_capture_mode()

def clik_button_start_capture():
    start_capture()

def clik_button_stop_capture():
    stop_capture()

tabControl = ttk.Notebook(root)          # Create Tab Control



Frame_captrueAudio = tkinter.Frame(tabControl)
tabControl.add(Frame_captrueAudio, text='Audio Debug')

Frame_transferFile = tkinter.Frame(tabControl)
tabControl.add(Frame_transferFile, text='Transfer Files')

tabControl.pack(expand=1, fill="both")  # Pack to make visible


########################################################################################################
# Table 1: "Audio Debug"
LabelFrame_DebugCaptureAudio = tkinter.LabelFrame(Frame_captrueAudio, text=' 抓取音频数据 ')
LabelFrame_DebugCaptureAudio.grid(row=0, column=0, rowspan=500, columnspan=800)

LabelFrame_showInfo = tkinter.LabelFrame(LabelFrame_DebugCaptureAudio, text='cmd info:')
LabelFrame_showInfo.grid(row=3, column=0, rowspan=700, columnspan=350, sticky='NW')
Text_showInfo = tkinter.Text(LabelFrame_showInfo, height=13, width=88)
Text_showInfo.grid(row=20, column=30, rowspan=300, columnspan=100)

LabelFrame_captureTimeS = tkinter.LabelFrame(LabelFrame_DebugCaptureAudio, text='Auto times(s):')
LabelFrame_captureTimeS.grid(row=0, column=3, sticky='NS')
Text_captureTimeS = tkinter.Text(LabelFrame_captureTimeS, height=1, width=8)
Text_captureTimeS.grid(row=1, column=3, padx=5, sticky='NS')
Text_captureTimeS.insert("end", str(audioDebug.DEFAULT_AUTO_MODE_DUMP_TIME_S))

LabelFrame_printDebug = tkinter.LabelFrame(LabelFrame_DebugCaptureAudio, text='Print Debug:')
LabelFrame_printDebug.grid(row=1, column=3, sticky='NS')
Checkbutton_printDebug = tkinter.Checkbutton(LabelFrame_printDebug, text='Enable', variable=printDebugEnable)
Checkbutton_printDebug.grid(row=3, column=1)

'''
BuScrollbar_captureMode = tkinter.Scrollbar(LabelFrame_DebugCaptureAudio)
#BuScrollbar_captureMode.pack(side=tkinter.RIGHT,fill=tkinter.Y)
#BuScrollbar_captureMode.place(x=627, y=140, width=20, height=200)
BuScrollbar_captureMode.grid(row=19, column=380, rowspan=400, columnspan=20)
BuScrollbar_captureMode.config(command=Text_showInfo.yview)
'''

LabelFrame_DebugCaptureAudioMode = ttk.LabelFrame(LabelFrame_DebugCaptureAudio, text=' 抓取模式: ')
LabelFrame_DebugCaptureAudioMode.grid(row=0, column=0, rowspan=3, sticky='NW')
Radiobutton_captureAutoMode = tkinter.Radiobutton(LabelFrame_DebugCaptureAudioMode, text='自动抓取', variable=captureMode, \
    value=aml_debug_audio.DEBUG_CAPTURE_MODE_AUTO, command=selection_capture_mode)
Radiobutton_captureAutoMode.grid(row=0, column=1, padx=10, pady=10)
Radiobutton_captureManualMode = tkinter.Radiobutton(LabelFrame_DebugCaptureAudioMode, text='手动抓取', variable=captureMode, \
    value=aml_debug_audio.DEBUG_CAPTURE_MODE_MUNUAL, command=selection_capture_mode)
Radiobutton_captureManualMode.grid(row=1, column=1, padx=3, pady=3)

Button_startCapture = tkinter.Button(LabelFrame_DebugCaptureAudio, text='开始抓取', command=clik_button_start_capture, width=10, height=2)
Button_startCapture.grid(row=0, column=4, padx=6)
Button_stopCapture = tkinter.Button(LabelFrame_DebugCaptureAudio, text='停止抓取', command=clik_button_stop_capture, width=10, height=2)
Button_stopCapture.grid(row=1, column=4, padx=6, pady=9)

Button_startCapture = tkinter.Button(LabelFrame_DebugCaptureAudio, text='开始抓取', command=clik_button_start_capture, width=10, height=2)
Button_startCapture.grid(row=0, column=4, padx=6)

LabelFrame_DebugCaptureAudioOption = ttk.LabelFrame(LabelFrame_DebugCaptureAudio, text=' Capture option: ')
LabelFrame_DebugCaptureAudioOption.grid(row=0, column=1, rowspan=3, columnspan=1, sticky='NW')
Checkbutton_debugInfo = tkinter.Checkbutton(LabelFrame_DebugCaptureAudioOption, text='Debug Info', variable=debugInfoEnable)
Checkbutton_dumpData = tkinter.Checkbutton(LabelFrame_DebugCaptureAudioOption, text='Dump data', variable=dumpDataEnable)
Checkbutton_Logcat = tkinter.Checkbutton(LabelFrame_DebugCaptureAudioOption, text='Logcat Info', variable=logcatEnable)
Checkbutton_debugInfo.grid(row=2, column=1)
Checkbutton_dumpData.grid(row=3, column=1)
Checkbutton_Logcat.grid(row=4, column=1)

########################################################################################################
# Table 2: "Transfer Files"
LabelFrame_DebugPushFiles = tkinter.LabelFrame(Frame_transferFile, text='Push files')
LabelFrame_DebugPushFiles.grid(row=0, column=0)

AudioSrcPath_Label = tkinter.Label(LabelFrame_DebugPushFiles, text="Source path:")
AudioSrcPath_Label.grid(row=0, column=10, rowspan=1, columnspan=10)
AudioDstPath_Label = tkinter.Label(LabelFrame_DebugPushFiles, text="Destination path:")
AudioDstPath_Label.grid(row=0, column=43, rowspan=1, columnspan=10)




DolbyDtsDstPath = tk.StringVar()
DolbySrcPath = tk.StringVar()
DtsSrcPath = tk.StringVar()
dolbyMs2DstPath = tk.StringVar()
dolbyMs2SrcPath = tk.StringVar()
customPushDstPath = tk.StringVar()
customPushSrcPath = tk.StringVar()
DolbyDtsDstPath.set('/odm/lib/')
dolbyMs2DstPath.set('/odm/etc/ms12/')

customPullDstPath = tk.StringVar()
customPullSrcPath = tk.StringVar()


def pushFilesToSoc(src, dst):
    subprocess.call('adb push ' + src + ' ' + dst, shell=True)

def pullFilesToSoc(src, dst):
    subprocess.call('adb pull ' + src + ' ' + dst, shell=True)

def pushDstDolby():
    pushFilesToSoc(DolbySrcPath.get() + '\\libHwAudio_dcvdec.so', DolbyDtsDstPath.get())
    pushFilesToSoc(DtsSrcPath.get() + '\\libHwAudio_dtshd.so', DolbyDtsDstPath.get())
def pushMs12():
    pushFilesToSoc(dolbyMs2SrcPath.get() + '\\libdolbyms12.so', dolbyMs2DstPath.get())
def pushCustom():
    pushFilesToSoc(customPushSrcPath.get(), customPushDstPath.get())
def pushAll():
    pushDstDolby()
    pushMs12()
    pushCustom()
def pullCustom():
    pullFilesToSoc(customPullSrcPath.get(), customPullDstPath.get())
def remount():
    subprocess.call('adb root', shell=True)
    subprocess.call('adb remount', shell=True)
def reboot():
    subprocess.call('adb reboot', shell=True)

Label_AudioDolbySo = tkinter.Label(LabelFrame_DebugPushFiles, text="Dolby so:")
Label_AudioDolbySo.grid(row=1, column=0, rowspan=1, columnspan=10)
Entry_pushDolbySoSrcPath = tkinter.Entry(LabelFrame_DebugPushFiles, textvariable=DolbySrcPath)
Entry_pushDolbySoSrcPath.grid(row=1, column=10, rowspan=1, columnspan=10)

Label_AudioDtsSo = tkinter.Label(LabelFrame_DebugPushFiles, text="Dts so:")
Label_AudioDtsSo.grid(row=2, column=0, rowspan=1, columnspan=10)
Entry_pushDtsSoSrcPath = tkinter.Entry(LabelFrame_DebugPushFiles, textvariable=DtsSrcPath)
Entry_pushDtsSoSrcPath.grid(row=2, column=10, rowspan=1, columnspan=10)
Label_arrow0 = tkinter.Label(LabelFrame_DebugPushFiles, text=">")
Label_arrow0.grid(row=1, column=35, rowspan=2, columnspan=10)
Entry_pushDtsSoDstPath = tkinter.Entry(LabelFrame_DebugPushFiles, textvariable=DolbyDtsDstPath)
Entry_pushDtsSoDstPath.grid(row=1, column=45, rowspan=2, columnspan=10)
Button_startCapturedts = tkinter.Button(LabelFrame_DebugPushFiles, text='Push', command=pushDstDolby, width=10, height=1)
Button_startCapturedts.grid(row=1, column=75, padx=6, rowspan=2, columnspan=1)

Label_AudioMs12So = tkinter.Label(LabelFrame_DebugPushFiles, text="Ms12 so:")
Label_AudioMs12So.grid(row=3, column=0, rowspan=1, columnspan=10)
Entry_pushMs12SoSrcPath = tkinter.Entry(LabelFrame_DebugPushFiles, textvariable=dolbyMs2SrcPath)
Entry_pushMs12SoSrcPath.grid(row=3, column=10, rowspan=1, columnspan=10)
Label_arrow1 = tkinter.Label(LabelFrame_DebugPushFiles, text=">")
Label_arrow1.grid(row=3, column=35, rowspan=1, columnspan=10)
Entry_pushMs12SoDstPath = tkinter.Entry(LabelFrame_DebugPushFiles, textvariable=dolbyMs2DstPath)
Entry_pushMs12SoDstPath.grid(row=3, column=45, rowspan=1, columnspan=10)
Button_pushMs12So = tkinter.Button(LabelFrame_DebugPushFiles, text='Push', command=pushMs12, width=10, height=1)
Button_pushMs12So.grid(row=3, column=75, padx=6)

Label_AudioMs12So = tkinter.Label(LabelFrame_DebugPushFiles, text="custom:")
Label_AudioMs12So.grid(row=4, column=0, rowspan=1, columnspan=10)
Entry_pushMs12SoSrcPath = tkinter.Entry(LabelFrame_DebugPushFiles, textvariable=customPushSrcPath)
Entry_pushMs12SoSrcPath.grid(row=4, column=10, rowspan=1, columnspan=10)
Label_arrow2 = tkinter.Label(LabelFrame_DebugPushFiles, text=">")
Label_arrow2.grid(row=4, column=35, rowspan=1, columnspan=10)
Entry_pushMs12SoDstPath = tkinter.Entry(LabelFrame_DebugPushFiles, textvariable=customPushDstPath)
Entry_pushMs12SoDstPath.grid(row=4, column=45, rowspan=1, columnspan=10)
Button_pushCustom = tkinter.Button(LabelFrame_DebugPushFiles, text='Push', command=pushCustom, width=10, height=1)
Button_pushCustom.grid(row=4, column=75, padx=6)

Button_pushAllSo = tkinter.Button(LabelFrame_DebugPushFiles, text='Push\n\nAll', command=pushAll, width=5, height=8)
Button_pushAllSo.grid(row=1, column=90, padx=6, pady=6, rowspan=5, sticky='N')



LabelFrame_DebugPullFiles = tkinter.LabelFrame(Frame_transferFile, text='Pull files')
LabelFrame_DebugPullFiles.grid(row=100, column=0, sticky='W')
Label_pullCustom = tkinter.Label(LabelFrame_DebugPullFiles, text="custom:")
Label_pullCustom.grid(row=0, column=0, rowspan=1, columnspan=10)
Entry_pushCustomSrcPath = tkinter.Entry(LabelFrame_DebugPullFiles, textvariable=customPullSrcPath)
Entry_pushCustomSrcPath.grid(row=0, column=10, rowspan=1, columnspan=10)
Label_arrow3 = tkinter.Label(LabelFrame_DebugPullFiles, text=">")
Label_arrow3.grid(row=0, column=35, rowspan=1, columnspan=10)
Entry_pushCustomDstPath = tkinter.Entry(LabelFrame_DebugPullFiles, textvariable=customPullDstPath)
Entry_pushCustomDstPath.grid(row=0, column=45, rowspan=1, columnspan=10)
Button_pullCustom = tkinter.Button(LabelFrame_DebugPullFiles, text='Pull', command=pullCustom, width=10, height=1)
Button_pullCustom.grid(row=0, column=75, padx=6, sticky='N')


LabelFrame_systemOperation = tkinter.LabelFrame(Frame_transferFile, text='system operation')
LabelFrame_systemOperation.grid(row=0, column=1, rowspan=2, columnspan=4, sticky='N')
Button_remount = tkinter.Button(LabelFrame_systemOperation, text='Remount', command=remount, width=10, height=1)
Button_remount.grid(row=0, column=0, padx=6, pady=6, sticky='N')
Button_remount = tkinter.Button(LabelFrame_systemOperation, text='Reboot', command=reboot, width=10, height=1)
Button_remount.grid(row=1, column=0, padx=6, pady=6, sticky='N')

def change_capture_mode():
    audioDebug.set_capture_mode(captureMode.get())
    if captureMode.get() == aml_debug_audio.DEBUG_CAPTURE_MODE_AUTO:
        Text_captureTimeS.config(state=NORMAL)
    elif captureMode.get() == aml_debug_audio.DEBUG_CAPTURE_MODE_MUNUAL:
        Text_captureTimeS.config(state=DISABLED)

def start_capture():
    #Text_showInfo.delete("1.0", tkinter.END)
    Button_startCapture.config(state=DISABLED)
    Radiobutton_captureAutoMode.config(state=DISABLED)
    Radiobutton_captureManualMode.config(state=DISABLED)
    Checkbutton_debugInfo.config(state=DISABLED)
    Checkbutton_dumpData.config(state=DISABLED)
    Checkbutton_Logcat.config(state=DISABLED)
    startCaptureInfo()
        
def stop_capture():
    Button_stopCapture.config(state=DISABLED)
    stopCaptureInfo()

def __async_call(func):
    def wrapper(*args, **kwargs):
        thr = Thread(target = func, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

def callback_startCaptureFinish():
    if audioDebug.get_capture_mode() == aml_debug_audio.DEBUG_CAPTURE_MODE_AUTO:
        Button_startCapture.config(state=NORMAL)
        Radiobutton_captureAutoMode.config(state=NORMAL)
        Radiobutton_captureManualMode.config(state=NORMAL)
        Checkbutton_debugInfo.config(state=NORMAL)
        Checkbutton_dumpData.config(state=NORMAL)
        Checkbutton_Logcat.config(state=NORMAL)
        callback_showCurstatusInfo('\n######## Auto mode capture Finish !!! ############')
    elif audioDebug.get_capture_mode() == aml_debug_audio.DEBUG_CAPTURE_MODE_MUNUAL:
        Button_stopCapture.config(state=NORMAL)
        callback_showCurstatusInfo('Manual mode Start capture finish')

def callback_stopCaptureFinish():
    callback_showCurstatusInfo('\n######## Manual mode capture Finish !!! ############')
    Button_startCapture.config(state=NORMAL)
    Radiobutton_captureAutoMode.config(state=NORMAL)
    Radiobutton_captureManualMode.config(state=NORMAL)
    Checkbutton_debugInfo.config(state=NORMAL)
    Checkbutton_dumpData.config(state=NORMAL)
    Checkbutton_Logcat.config(state=NORMAL)

@__async_call
def startCaptureInfo():
    audioDebugConfig = aml_debug_audio.AudioDebugCfg()
    audioDebugConfig.m_debugInfoEnable = debugInfoEnable.get()
    audioDebugConfig.m_dumpDataEnable = dumpDataEnable.get()
    audioDebugConfig.m_logcatEnable = logcatEnable.get()
    audioDebugConfig.m_printDebugEnable = printDebugEnable.get()
    audioDebug.setAudioDebugCfg(audioDebugConfig)
    audioDebug.setShowStatusCallback(callback_showCurstatusInfo)

    Text_captureTimeS_value = str(Text_captureTimeS.get(1.0, tkinter.END))
    try:
        captureTimeS = int(Text_captureTimeS_value)
    except ValueError:
        captureTimeS = audioDebug.DEFAULT_AUTO_MODE_DUMP_TIME_S
        callback_showCurstatusInfo('startCaptureInfo: invalid captureTimeS!!!')
    audioDebug.setAutoDebugTimeS(captureTimeS)

    audioDebug.start_capture(callback_startCaptureFinish)


@__async_call
def stopCaptureInfo():
    audioDebug.stop_capture(callback_stopCaptureFinish)

def callback_showCurstatusInfo(infoText):
    Text_showInfo.mark_set("here", "0.0")
    Text_showInfo.insert("here", infoText + ' \n')


Button_stopCapture.config(state=DISABLED)

root.mainloop()