# coding=utf-8
import argparse
import time
from datetime import datetime
from ctypes import *
import os
from HCNetSDK import *

Objdll = None  # 网络库



def initialize_sdk(Objdll):
    """初始化SDK"""
    Objdll.NET_DVR_Init()
    Objdll.NET_DVR_SetLogToFile(3, b'./SdkLog_Python/', False)

def login_device(Objdll, dev_ip, dev_port, dev_user_name, dev_password):
    """登录设备"""
    device_info = NET_DVR_DEVICEINFO_V30()
    user_id = Objdll.NET_DVR_Login_V30(
        dev_ip.encode('utf-8'), dev_port, 
        dev_user_name.encode('utf-8'), dev_password.encode('utf-8'), 
        byref(device_info)
    )
    if user_id < 0:
        print(f"登录设备失败，错误码: {Objdll.NET_DVR_GetLastError()}")
        Objdll.NET_DVR_Cleanup()
        exit()
    print("设备登录成功")
    return user_id

def load_completed_files(completed_files_path):
    """加载已完成的文件列表"""
    if not os.path.exists(completed_files_path):
        return set()
    with open(completed_files_path, "r") as file:
        return set(line.strip() for line in file)

def save_completed_file(file_name, completed_files_path):
    """保存已完成的文件到记录文件"""
    with open(completed_files_path, "a") as file:
        file.write(f"{file_name}\n")

def find_file_by_name(lUserID, channel, start_time, end_time):
    """查找录像文件"""
    net_dvr_filecond = NET_DVR_FILECOND_V50()
    net_dvr_filecond.struStreamID.dwChannel = channel  # 通道号
    net_dvr_filecond.dwFileType = 0
    net_dvr_filecond.byFindType = 0

    # 设置开始时间
    net_dvr_filecond.struStartTime.wYear, net_dvr_filecond.struStartTime.byMonth, net_dvr_filecond.struStartTime.byDay = start_time.year, start_time.month, start_time.day
    net_dvr_filecond.struStartTime.byHour, net_dvr_filecond.struStartTime.byMinute, net_dvr_filecond.struStartTime.bySecond = start_time.hour, start_time.minute, start_time.second

    # 设置结束时间
    net_dvr_filecond.struStopTime.wYear, net_dvr_filecond.struStopTime.byMonth, net_dvr_filecond.struStopTime.byDay = end_time.year, end_time.month, end_time.day
    net_dvr_filecond.struStopTime.byHour, net_dvr_filecond.struStopTime.byMinute, net_dvr_filecond.struStopTime.bySecond = end_time.hour, end_time.minute, end_time.second

    find_handle = Objdll.NET_DVR_FindFile_V50(lUserID, byref(net_dvr_filecond))
    if find_handle < 0:
        print(f"查找录像文件失败，错误码: {Objdll.NET_DVR_GetLastError()}")
        return None

    stru_find_data = NET_DVR_FINDDATA_V50()
    while True:
        state = Objdll.NET_DVR_FindNextFile_V50(find_handle, byref(stru_find_data))
        if state == 1000:
            return stru_find_data.sFileName.decode('utf-8').strip()
        elif state in [1003, 1004, 1005]:
            print("查找结束或异常")
            break
    Objdll.NET_DVR_FindClose_V30(find_handle)
    return None

def find_and_download_all_files(lUserID, channel, start_time, end_time, save_path, completed_files_path):
    completed_files = load_completed_files(completed_files_path)
    net_dvr_filecond = NET_DVR_FILECOND_V50()
    net_dvr_filecond.struStreamID.dwChannel = channel
    net_dvr_filecond.dwFileType = 0
    net_dvr_filecond.byFindType = 0

    # Setting search time range
    net_dvr_filecond.struStartTime.wYear = start_time.year
    net_dvr_filecond.struStartTime.byMonth = start_time.month
    net_dvr_filecond.struStartTime.byDay = start_time.day
    net_dvr_filecond.struStartTime.byHour = start_time.hour
    net_dvr_filecond.struStartTime.byMinute = start_time.minute
    net_dvr_filecond.struStartTime.bySecond = start_time.second

    net_dvr_filecond.struStopTime.wYear = end_time.year
    net_dvr_filecond.struStopTime.byMonth = end_time.month
    net_dvr_filecond.struStopTime.byDay = end_time.day
    net_dvr_filecond.struStopTime.byHour = end_time.hour
    net_dvr_filecond.struStopTime.byMinute = end_time.minute
    net_dvr_filecond.struStopTime.bySecond = end_time.second

    find_handle = Objdll.NET_DVR_FindFile_V50(lUserID, byref(net_dvr_filecond))
    if find_handle < 0:
        print(f"Failed to find video files, error code: {Objdll.NET_DVR_GetLastError()}")
        return

    files_found = False
    while True:
        stru_find_data = NET_DVR_FINDDATA_V50()
        state = Objdll.NET_DVR_FindNextFile_V50(find_handle, byref(stru_find_data))
        if state == 1000:
            file_name = stru_find_data.sFileName.decode('utf-8').strip()
            if file_name not in completed_files:
                files_found = True
                start_file_time = datetime(
                    year=stru_find_data.struStartTime.wYear,
                    month=stru_find_data.struStartTime.byMonth,
                    day=stru_find_data.struStartTime.byDay,
                    hour=stru_find_data.struStartTime.byHour,
                    minute=stru_find_data.struStartTime.byMinute,
                    second=stru_find_data.struStartTime.bySecond,
                )
                print(f"Found file: {file_name}, starting time: {start_file_time}")
                download_by_name(lUserID, file_name, save_path, start_file_time, completed_files_path)
        elif state in [1003, 1004, 1005]:
            break

    Objdll.NET_DVR_FindClose_V30(find_handle)

    # Check if no files were found and if the completed_files.txt should be deleted
    if not files_found:
        try:
            os.remove(completed_files_path)
            print("All files downloaded. Completed files record has been deleted.")
        except OSError as e:
            print(f"Error deleting file {completed_files_path}: {e.strerror}")



def download_by_name(lUserID, file_name, save_path, start_time, completed_files_path):
    """按文件名下载录像，并支持断点续传"""
    time_str = start_time.strftime("%Y-%m-%d_%H-%M-%S")
    save_file_path = f"{save_path}/{time_str}.mp4"

    # 检查是否已下载完成
    if os.path.exists(save_file_path):
        print(f"文件已存在，跳过: {save_file_path}")
        save_completed_file(file_name, completed_files_path)  # 标记为已完成
        return

    print(f"开始下载文件: {file_name} 到 {save_file_path}")
    download_handle = Objdll.NET_DVR_GetFileByName(lUserID, file_name.encode('utf-8'), save_file_path.encode('utf-8'))
    if download_handle < 0:
        print(f"下载失败，错误码: {Objdll.NET_DVR_GetLastError()}")
        return

    # 启动下载
    Objdll.NET_DVR_PlayBackControl(download_handle, NET_DVR_PLAYSTART, 0, None)
    while True:
        progress = Objdll.NET_DVR_GetDownloadPos(download_handle)
        if progress == 100:
            print(f"文件下载完成: {save_file_path}")
            save_completed_file(file_name, completed_files_path)  # 下载完成后记录文件
            break
        elif progress < 0:
            print(f"下载失败，错误码: {Objdll.NET_DVR_GetLastError()}")
            break
        print(f"下载进度: {progress}%")
        time.sleep(1)
    Objdll.NET_DVR_StopGetFile(download_handle)


def main():
    parser = argparse.ArgumentParser(description="下载录像文件")
    parser.add_argument("--ip", required=True, help="设备IP地址")
    parser.add_argument("--port", type=int, default=8000, help="设备端口")
    parser.add_argument("--username", required=True, help="设备用户名")
    parser.add_argument("--password", required=True, help="设备密码")
    parser.add_argument("--channel", type=int, required=True, help="通道号")
    parser.add_argument("--start_time", required=True, help="开始时间，格式：YYYY-MM-DD HH:MM:SS")
    parser.add_argument("--end_time", required=True, help="结束时间，格式：YYYY-MM-DD HH:MM:SS")
    parser.add_argument("--save_path", default="./", help="录像保存路径")
    parser.add_argument("--completed_files", required=True, help="已完成文件记录路径")
    args = parser.parse_args()

    start_time = datetime.strptime(args.start_time, "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(args.end_time, "%Y-%m-%d %H:%M:%S")

    global Objdll
    Objdll = CDLL('./lib/win/HCNetSDK.dll') 
    initialize_sdk(Objdll)

    user_id = login_device(Objdll, args.ip, args.port, args.username, args.password)

    find_and_download_all_files(user_id, args.channel, start_time, end_time, args.save_path, args.completed_files)

    Objdll.NET_DVR_Logout(user_id)
    Objdll.NET_DVR_Cleanup()

if __name__ == "__main__":
    main()
