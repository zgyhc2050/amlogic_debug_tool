import threading
import tkinter
import os
import time
from tkinter.constants import DISABLED, NORMAL
from threading import Thread

import aml_debug_audio


root = tkinter.Tk()
root.title('Amlogic Debug Tool')
root.wm_attributes("-alpha", 0.9)  # 设置GUI透明度(0.0~1.0)
root.wm_attributes("-topmost", True)  # 设置GUI置顶
# 设定窗口的大小(长 * 宽)
root.geometry('700x300')  

captureMode = tkinter.IntVar()    
l = tkinter.Label(root, width=20, text='抓取模式')
l.place(x=20, y=3, width=100, height=20)

text_input = tkinter.Text(root, height=5, width=40)
text_input.place(x=0, y=90, width=680, height=200)

scroll_text = tkinter.Scrollbar()
#scroll_text.pack(side=tkinter.RIGHT,fill=tkinter.Y)
scroll_text.place(x=680, y=90, width=20, height=200)
scroll_text.config(command=text_input.yview)

def capture_mode_selection():
    audioDebug.set_capture_mode(captureMode.get())
    #l.config(text='you have selected ' + str(captureMode.get()))

captureAutoModeRadiobutton = tkinter.Radiobutton(root, text='自动抓取', variable=captureMode, value=aml_debug_audio.DEBUG_CAPTURE_MODE_AUTO, command=capture_mode_selection)
captureAutoModeRadiobutton.place(x=20, y=30, width=100, height=20)
captureManualModeRadiobutton = tkinter.Radiobutton(root, text='手动抓取', variable=captureMode, value=aml_debug_audio.DEBUG_CAPTURE_MODE_MUNUAL, command=capture_mode_selection)
#captureManualModeRadiobutton.pack(side=tkinter.LEFT)
captureManualModeRadiobutton.place(x=20, y=60, width=100, height=20)

def clik_button_startCaptureInfo():
    #text_input.delete("1.0", tkinter.END)
    audioDebug.setShowStatusCallback(callback_showCurstatusInfo)
    startCaptureButton.config(state=DISABLED)
    captureAutoModeRadiobutton.config(state=DISABLED)
    captureManualModeRadiobutton.config(state=DISABLED)
    startCaptureInfo()
        
def clik_button_stopCaptureInfo():
    stopCaptureButton.config(state=DISABLED)
    stopCaptureInfo()
    
startCaptureButton = tkinter.Button(root, text='开始抓取', command=clik_button_startCaptureInfo)
startCaptureButton.place(x=180, y=40, width=100, height=40)

stopCaptureButton = tkinter.Button(root, text='停止抓取', command=clik_button_stopCaptureInfo)
stopCaptureButton.place(x=350, y=40, width=100, height=40)

def async_call(func):
    def wrapper(*args, **kwargs):
        thr = Thread(target = func, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

def callback_startCaptureFinish():
    if audioDebug.get_capture_mode() == aml_debug_audio.DEBUG_CAPTURE_MODE_AUTO:
        startCaptureButton.config(state=NORMAL)
        captureAutoModeRadiobutton.config(state=NORMAL)
        captureManualModeRadiobutton.config(state=NORMAL)
        callback_showCurstatusInfo('\n######## Auto mode capture Finish !!! ############\n')
    elif audioDebug.get_capture_mode() == aml_debug_audio.DEBUG_CAPTURE_MODE_MUNUAL:
        stopCaptureButton.config(state=NORMAL)

def callback_stopCaptureFinish():
    callback_showCurstatusInfo('\n######## Munual mode capture Finish !!! ############\n')
    startCaptureButton.config(state=NORMAL)
    captureAutoModeRadiobutton.config(state=NORMAL)
    captureManualModeRadiobutton.config(state=NORMAL)

@async_call
def startCaptureInfo():
    audioDebug.start_capture(callback_startCaptureFinish)

@async_call
def stopCaptureInfo():
    audioDebug.stop_capture(callback_stopCaptureFinish)

captureMode.set(aml_debug_audio.DEFAULT_CAPTURE_MODE)
stopCaptureButton.config(state=DISABLED)

def callback_showCurstatusInfo(infoText):
    text_input.mark_set("here", "0.0")
    text_input.insert("here", infoText + ' \n')

audioDebug = aml_debug_audio.AmlAudioDebug()

root.mainloop()