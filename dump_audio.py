import os
import time
from pathlib import Path


pcRootPath = "d:\dump_audio"
currentTime = time.strftime("%Y%m%d_%H-%M-%S", time.localtime())
nowPullPath = pcRootPath + "\\" + currentTime
print('Current date:' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ', directory is: ' + nowPullPath)
DUMP_DEBUG = False

if not Path(pcRootPath).exists():
    print(pcRootPath, " folder does not exist, create it.")
    os.makedirs(pcRootPath)
os.makedirs(nowPullPath)

os.system('adb root')
os.system('adb remount')

print('Please wait a moment, starting to dump debugging information...')
dumpCmdOutFilePath = '/data/dump_audio.log'
adbDumpCmdLists = [
    'cat /proc/asound/cards',
    'cat /proc/asound/pcm',
    'cat /proc/asound/card0/pcm*p/sub0/status',
    'cat /proc/asound/card0/pcm*p/sub0/hw_params',
    'cat /proc/asound/card0/pcm*p/sub0/sw_params',
    'cat /sys/class/amhdmitx/amhdmitx0/aud_cap',
    'cat /sys/class/amaudio/dts_enable',
    'cat /sys/class/amaudio/dolby_enable',
    'dumpsys hdmi_control',
    'dumpsys media.audio_policy',
    'dumpsys audio',
    'dumpsys media.audio_flinger',
    'tinymix'
]
os.system('adb shell rm ' + dumpCmdOutFilePath + ' -rf')
for i, adbDumpCmdList in enumerate(adbDumpCmdLists):
    echoCmdInfo = 'adb shell "echo cmd_' + str(i) + ' ' + adbDumpCmdList + ' >> ' + dumpCmdOutFilePath + '"'
    exeCmdInfo = 'adb shell "' + adbDumpCmdList + ' >> ' + dumpCmdOutFilePath + '"'
    if DUMP_DEBUG:
        print(echoCmdInfo)
        print(exeCmdInfo)
    os.system(echoCmdInfo)
    os.system(exeCmdInfo)


adbDumpDataStartLists = [
    'setenforce 0',
    'mkdir /data/audio /data/vendor/audiohal/ -p',
    'chmod 777 /data/audio /data/vendor/audiohal/',
    'rm /data/audio/* /data/vendor/audiohal/* -rf',
    'setprop vendor.media.audio.hal.debug 4096',
    'setprop vendor.media.audiohal.indump 1',
    'setprop vendor.media.audiohal.outdump 1',
    'setprop vendor.media.audiohal.alsadump 1',
    'setprop vendor.media.audiohal.a2dpdump 1',
    'setprop vendor.media.audiohal.ms12dump 0xfff',
    'setprop media.audio.hal.debug 4096',
    'setprop media.audiohal.indump 1',
    'setprop media.audiohal.outdump 1',
    'setprop media.audiohal.alsadump 1',
    'setprop media.audiohal.a2dpdump 1',
    'setprop media.audiohal.ms12dump 0xfff',
]
adbDumpDataStopLists = [
    'setprop vendor.media.audio.hal.debug 0',
    'setprop vendor.media.audiohal.indump 0',
    'setprop vendor.media.audiohal.outdump 0',
    'setprop vendor.media.audiohal.alsadump 0',
    'setprop vendor.media.audiohal.a2dpdump 0',
    'setprop vendor.media.audiohal.ms12dump 0',
    'setprop media.audio.hal.debug 0',
    'setprop media.audiohal.indump 0',
    'setprop media.audiohal.outdump 0',
    'setprop media.audiohal.alsadump 0',
    'setprop media.audiohal.a2dpdump 0',
    'setprop media.audiohal.ms12dump 0',
]

for adbDumpDataStart in adbDumpDataStartLists:
    exeCmdInfo = 'adb shell "' + adbDumpDataStart + '"'
    if DUMP_DEBUG:
        print(exeCmdInfo)
    os.system(exeCmdInfo)

print('Start fetching the audio data, wait for 3 seconds...')
time.sleep(3)
for adbDumpDataStop in adbDumpDataStopLists:
    exeCmdInfo = 'adb shell "' + adbDumpDataStop + '"'
    if DUMP_DEBUG:
        print(exeCmdInfo)
    os.system(exeCmdInfo)

dumpFileLists = [
    'vendor/etc/audio_policy_configuration.xml',
    'vendor/etc/audio_policy_volumes.xml',
    '/data/audio',
    '/data/vendor/audiohal/',
    dumpCmdOutFilePath,
]
for dumpFile in dumpFileLists:
    exeCmdInfo = 'adb pull ' + dumpFile + ' ' + nowPullPath
    if DUMP_DEBUG:
        print(exeCmdInfo)
    os.system(exeCmdInfo)

print('###############################################################################################')
print('##                                                                                           ##')
print('##  Please send folder %-40s' % nowPullPath + ' to RD colleagues! Thank You! ##')
print('##                                                                                           ##')
print('###############################################################################################')

os.system('pause')