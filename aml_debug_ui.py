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
root.geometry('650x350') # 设定窗口的大小(长 * 宽)
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

tab1 = tkinter.Frame(tabControl)            # Create a tab 
tabControl.add(tab1, text='Audio Debug')      # Add the tab
tab2 = tkinter.Frame(tabControl)            # Add a second tab
tabControl.add(tab2, text='Push')      # Make second tab visible
tabControl.pack(expand=1, fill="both")  # Pack to make visible


# LabelFrame using tab1 as the parent
LabelFrame_DebugCaptureAudio = tkinter.LabelFrame(tab1, text=' 抓取音频数据 ')
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

BuScrollbar_captureMode = tkinter.Scrollbar()
#BuScrollbar_captureMode.pack(side=tkinter.RIGHT,fill=tkinter.Y)
BuScrollbar_captureMode.place(x=627, y=140, width=20, height=200)
BuScrollbar_captureMode.config(command=Text_showInfo.yview)

# LabelFrame using tab1 as the parent
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


LabelFrame_DebugCaptureAudioOption = ttk.LabelFrame(LabelFrame_DebugCaptureAudio, text=' Capture option: ')
LabelFrame_DebugCaptureAudioOption.grid(row=0, column=1, rowspan=3, columnspan=1, sticky='NW')
Checkbutton_debugInfo = tkinter.Checkbutton(LabelFrame_DebugCaptureAudioOption, text='Debug Info', variable=debugInfoEnable)
Checkbutton_dumpData = tkinter.Checkbutton(LabelFrame_DebugCaptureAudioOption, text='Dump data', variable=dumpDataEnable)
Checkbutton_Logcat = tkinter.Checkbutton(LabelFrame_DebugCaptureAudioOption, text='Logcat Info', variable=logcatEnable)
Checkbutton_debugInfo.grid(row=2, column=1)
Checkbutton_dumpData.grid(row=3, column=1)
Checkbutton_Logcat.grid(row=4, column=1)

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
    audioDebugConfig.m_printDebugEnable = printDebugEnable.get
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