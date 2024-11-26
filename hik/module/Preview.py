# --*-- conding:utf-8 --*--
# @Time : 2024/8/19 10:57
# @Author : wangchao124
# @Email : wangchao124@hikvision.com
# @File : Playback.py
# @Software : PyCharm

# coding=utf-8

import os
import ctypes
import time
from datetime import datetime

from HCNetSDK import *
from PlayCtrl import *

PlayCtrl_Port = ctypes.c_long(-1)  # 播放句柄
Objdll = None   # 网络库
Playctrldll = None  # 播放库
cv = None
FuncDecCB = None  # 播放库解码回调函数，需要定义为全局的
funcRealDataCallBack_V30 = None  # 实时预览回调函数，需要定义为全局的
callback_count = 0


def InitializeGlobals(loaded_Objdll, loaded_Playctrldll, loaded_PlayCtrl_Port):
    global Objdll
    Objdll = loaded_Objdll
    global Playctrldll
    Playctrldll = loaded_Playctrldll
    global PlayCtrl_Port
    PlayCtrl_Port = loaded_PlayCtrl_Port



def DecCBFun(nPort, pBuf, nSize, pFrameInfo, nUser, nReserved2):
    global callback_count
    callback_count += 1

    if callback_count % 100 == 0:
        print("进入播放库解码回调...")
    # 解码回调函数
    # if pFrameInfo.contents.nType == 3:
    #     sFileName = ('../../resource/pic/test_stamp[%d].jpg' % pFrameInfo.contents.nStamp)
    #     nWidth = pFrameInfo.contents.nWidth
    #     nHeight = pFrameInfo.contents.nHeight
    #     nType = pFrameInfo.contents.nType
    #     dwFrameNum = pFrameInfo.contents.dwFrameNum
    #     nStamp = pFrameInfo.contents.nStamp
    #     print(nSize, nWidth, nHeight, nType, dwFrameNum, nStamp, sFileName)
    #
    #     lRet = Playctrldll.PlayM4_ConvertToJpegFile(pBuf, nSize, nWidth, nHeight, nType,
    #                                                 ctypes.c_char_p(sFileName.encode()))
    #     if lRet == 0:
    #         print('PlayM4_ConvertToJpegFile fail, error code is:', Playctrldll.PlayM4_GetLastError(nPort))
    #     else:
    #         print('PlayM4_ConvertToJpegFile success')


def getPicbyPlayCtrl():
    # 取流成功后，延时一段时间保证播放库解码开始
    time.sleep(1)

    pWidth = c_int(0)
    pHeight = c_int(0)

    bFlag = Playctrldll.PlayM4_GetPictureSize(PlayCtrl_Port, byref(pWidth), byref(pHeight))
    print(f"m_lPort: {PlayCtrl_Port}")

    if not bFlag:
        print(f"获取失败：{Playctrldll.PlayM4_GetLastError(PlayCtrl_Port)}")

    print(pWidth.value)
    print(pHeight.value)

    RealPicSize = c_int(0)
    picsize = pWidth.value * pHeight.value * 5

    picByte = create_string_buffer(picsize)
    pByte = byref(picByte)

    b_GetPic = Playctrldll.PlayM4_GetBMP(PlayCtrl_Port, pByte, picsize, byref(RealPicSize))

    if not b_GetPic:
        print(f"抓图失败：{Playctrldll.PlayM4_GetLastError(PlayCtrl_Port)}")
        return

    newName = datetime.now().strftime("%Y%m%d%H%M%S")
    try:
        os.makedirs("pic", exist_ok=True)
        with open(f"./pic/{newName}.bmp", "wb") as fout:
            # 使用 ctypes.string_at 从指针读取数据
            fout.write(string_at(pByte, RealPicSize.value))
        print("抓图成功!")
    except Exception as e:
        print(f"文件写入失败：{str(e)}")


def RealDataCallBack_V30(lPlayHandle, dwDataType, pBuffer, dwBufSize, pUser):
    # 码流回调函数
    if dwDataType == NET_DVR_SYSHEAD:
        # 设置流播放模式
        Playctrldll.PlayM4_SetStreamOpenMode(PlayCtrl_Port, 0)
        # 打开码流，送入40字节系统头数据
        if Playctrldll.PlayM4_OpenStream(PlayCtrl_Port, pBuffer, dwBufSize, 1024 * 1024):
            # 设置解码回调，可以返回解码后YUV视频数据
            global FuncDecCB
            FuncDecCB = DECCBFUNWIN(DecCBFun)
            Playctrldll.PlayM4_SetDecCallBackExMend(PlayCtrl_Port, FuncDecCB, None, 0, None)
            # 开始解码播放
            if Playctrldll.PlayM4_Play(PlayCtrl_Port, None):
                print(u'播放库播放成功')
            else:
                print(u'播放库播放失败')
        else:
            print(u'播放库打开流失败')
    elif dwDataType == NET_DVR_STREAMDATA:
        Playctrldll.PlayM4_InputData(PlayCtrl_Port, pBuffer, dwBufSize)
    else:
        print(u'其他数据,长度:', dwBufSize)


def OpenPreview(lUserId, callbackFun):
    preview_info = NET_DVR_PREVIEWINFO()
    preview_info.hPlayWnd = 0
    preview_info.lChannel = 1
    preview_info.dwStreamType = 0
    preview_info.dwLinkMode = 0
    preview_info.bBlocked = 1
    lRealPlayHandle = Objdll.NET_DVR_RealPlay_V40(lUserId, byref(preview_info), callbackFun, None)
    print(lRealPlayHandle)
    # print('开始预览失败, 错误码: %d' % Objdll.NET_DVR_GetLastError())
    # getPicbyPlayCtrl() # 预览时，单帧数据捕获并保存成图片
    return lRealPlayHandle

def CleanRealUp(Objdll, Playctrldll, lRealPlayHandle):
    Objdll.NET_DVR_StopRealPlay(lRealPlayHandle)
    if PlayCtrl_Port.value > -1:
        Playctrldll.PlayM4_Stop(PlayCtrl_Port)
        Playctrldll.PlayM4_CloseStream(PlayCtrl_Port)
        Playctrldll.PlayM4_FreePort(PlayCtrl_Port)
