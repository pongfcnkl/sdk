# coding=utf-8

import os
import platform
import time
import tkinter
from tkinter import *
import ctypes

from HCNetSDK import *
from module.Playback import OpenPlayback, playBackInitial, CleanPlayBackUp
from module import GetPlayBackFile
from module.Preview import OpenPreview, RealDataCallBack_V30, InitializeGlobals, CleanRealUp

# 登录的设备信息
DEV_IP = ctypes.create_string_buffer(b'192.168.1.7')
DEV_PORT = 8000
DEV_USER_NAME = ctypes.create_string_buffer(b'1')
DEV_PASSWORD = ctypes.create_string_buffer(b'a1234567')

PlayCtrl_Port = ctypes.c_long(-1)  # 播放句柄
WINDOWS_FLAG = True


def SetSDKInitCfg(Objdll, strPath, WINDOWS_FLAG):
    sdk_ComPath = NET_DVR_LOCAL_SDK_PATH()
    sdk_ComPath.sPath = strPath
    Objdll.NET_DVR_SetSDKInitCfg(2, ctypes.byref(sdk_ComPath))

    if WINDOWS_FLAG:
        Objdll.NET_DVR_SetSDKInitCfg(3, ctypes.create_string_buffer(strPath + b'\libcrypto-1_1-x64.dll'))
        Objdll.NET_DVR_SetSDKInitCfg(4, ctypes.create_string_buffer(strPath + b'\libssl-1_1-x64.dll'))
    else:
        Objdll.NET_DVR_SetSDKInitCfg(3, ctypes.create_string_buffer(strPath + b'/libcrypto.so.1.1'))
        Objdll.NET_DVR_SetSDKInitCfg(4, ctypes.create_string_buffer(strPath + b'/libssl.so.1.1'))


def LoginDev(Objdll, DEV_IP, DEV_PORT, DEV_USER_NAME, DEV_PASSWORD):
    # 登录注册设备
    device_info = NET_DVR_DEVICEINFO_V30()
    lUserId = Objdll.NET_DVR_Login_V30(DEV_IP, DEV_PORT, DEV_USER_NAME, DEV_PASSWORD, ctypes.byref(device_info))
    return (lUserId, device_info)


def Initialize(Objdll, Playctrldll):
    # 初始化DLL
    Objdll.NET_DVR_Init()
    Objdll.NET_DVR_SetLogToFile(3, bytes('./SdkLog_Python/', encoding="utf-8"), False)

    # 获取一个播放句柄
    if not Playctrldll.PlayM4_GetPort(ctypes.byref(PlayCtrl_Port)):
        print(u'获取播放库句柄失败')


def GetPlatform():
    sysstr = platform.system()
    print('' + sysstr)
    if sysstr != "Windows":
        global WINDOWS_FLAG
        WINDOWS_FLAG = False


# 获取IP接入配置参数
def get_ip_channel_info(user_id):
    ibr_bytes_returned = c_int(0)  # 获取返回字节数
    m_str_ippara_cfg = NET_DVR_IPPARACFG_V40()
    memset(byref(m_str_ippara_cfg), 0, sizeof(m_str_ippara_cfg))  # 清空结构体

    # lpIpParaConfig 接收数据的缓冲指针
    lp_ip_para_config = cast(pointer(m_str_ippara_cfg), POINTER(NET_DVR_IPPARACFG_V40))

    # 假设你已经定义了 hCNetSDK 和相应的方法
    b_ret = Objdll.NET_DVR_GetDVRConfig(user_id, NET_DVR_GET_IPPARACFG_V40, 0, lp_ip_para_config,
                                        sizeof(m_str_ippara_cfg), byref(ibr_bytes_returned))

    if b_ret:
        print("起始数字通道号：", m_str_ippara_cfg.dwStartDChan)

        for i_channel_num in range(m_str_ippara_cfg.dwDChanNum):
            channel_num = i_channel_num + m_str_ippara_cfg.dwStartDChan
            stream_mode = m_str_ippara_cfg.struStreamMode[i_channel_num]

            if stream_mode.uGetStream.struChanInfo.byEnable == 1:
                print("IP通道", channel_num, "在线")
            else:
                print("IP通道", channel_num, "不在线")
    else:
        print("获取通道信息失败")


if __name__ == '__main__':

    GetPlatform()

    if WINDOWS_FLAG:
        os.chdir(r'./lib/win')
        Objdll = ctypes.CDLL(r'./HCNetSDK.dll')
        Playctrldll = ctypes.CDLL(r'./PlayCtrl.dll')
    else:
        os.chdir(r'./lib/linux')
        Objdll = ctypes.cdll.LoadLibrary(r'./libhcnetsdk.so')
        Playctrldll = ctypes.cdll.LoadLibrary(r'./libPlayCtrl.so')

    SetSDKInitCfg(Objdll, os.getcwd().encode('gbk') if WINDOWS_FLAG else os.getcwd().encode('utf-8'), WINDOWS_FLAG)

    Initialize(Objdll, Playctrldll)
    net_dvr_local_general_cfg = NET_DVR_LOCAL_GENERAL_CFG()
    net_dvr_local_general_cfg.byNotSplitRecordFile = 1
    Objdll.NET_DVR_SetSDKLocalCfg(17, byref(net_dvr_local_general_cfg))

    (lUserId, device_info) = LoginDev(Objdll, DEV_IP, DEV_PORT, DEV_USER_NAME, DEV_PASSWORD)
    if lUserId < 0:
        print('Login device fail, error code is: %d' % Objdll.NET_DVR_GetLastError())
        Objdll.NET_DVR_Cleanup()
        exit()

    """
    获取IP接入配置参数
    """
    # get_ip_channel_info(lUserId)

    """
    预览窗口调用示例、播放库回调抓图
    """
    # 初始化预览全局变量
    # InitializeGlobals(Objdll, Playctrldll, cv, PlayCtrl_Port, win)
    InitializeGlobals(Objdll, Playctrldll, PlayCtrl_Port)
    global funcRealDataCallBack_V30
    funcRealDataCallBack_V30 = REALDATACALLBACK(RealDataCallBack_V30)
    lRealPlayHandle = OpenPreview(lUserId, funcRealDataCallBack_V30)
    if lRealPlayHandle < 0:
        print('开始预览失败, 错误码: %d' % Objdll.NET_DVR_GetLastError())
        Objdll.NET_DVR_Logout(lUserId)
        Objdll.NET_DVR_Cleanup()
        exit()
    time.sleep(30)
    # win.mainloop()
    # 停止预览，释放播放库资源
    CleanRealUp(Objdll, Playctrldll, lRealPlayHandle)
    """
    预览时，单帧数据捕获并保存成图片
    """
    # preview_info = NET_DVR_PREVIEWINFO()
    # preview_info.hPlayWnd = 2
    # preview_info.lChannel = 33
    # preview_info.dwStreamType = 0
    # preview_info.dwLinkMode = 0
    # preview_info.bBlocked = 1
    # lRealPlayHandle = Objdll.NET_DVR_RealPlay_V40(lUserId, byref(preview_info), funcRealDataCallBack_V30, None)
    # if lRealPlayHandle < 0:
    #     print('开始预览失败, 错误码: %d' % Objdll.NET_DVR_GetLastError())
    #     Objdll.NET_DVR_Logout(lUserId)
    #     Objdll.NET_DVR_Cleanup()
    #     exit()
    # else:
    #     print("开始预览成功")
    #
    # time.sleep(5)

    """
    按时间回放窗口/取回放流保存文件调用示例
    """
    # # 初始化回放全局变量
    # playBackInitial(Objdll, Playctrldll, cv, PlayCtrl_Port, win)
    # iPlayBack = OpenPlayback(lUserId, 33, "win")
    # if iPlayBack < 0:
    #     print('开始回放失败, 错误码: %d' % Objdll.NET_DVR_GetLastError())
    #     Objdll.NET_DVR_Logout(lUserId)
    #     Objdll.NET_DVR_Cleanup()
    #     exit()
    # else:
    #     print("开始回放成功")
    # # 停止回放，释放播放库资源
    # CleanPlayBackUp(Objdll, Playctrldll, iPlayBack, lUserId)

    """
    查找录像文件并按文件名/时间下载
    """
    # GetPlayBackFile.PlayBackInitialize(Objdll, Playctrldll, cv, PlayCtrl_Port, win)
    # # 按文件名称下载
    # GetPlayBackFile.download_record_by_name(lUserId, 33)
    # 按时间下载
    # GetPlayBackFile.download_record_by_time(lUserId)

    """
    释放sdk资源
    """
    Objdll.NET_DVR_Logout(lUserId)
    Objdll.NET_DVR_Cleanup()
