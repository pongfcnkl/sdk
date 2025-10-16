# coding=utf-8 
"""
大华NVR录像下载工具 - 根据文件列表下载多个录像文件

使用示例：
python dahua_nvr_downloader.py --ip 192.168.1.100 --user admin --password 123456 --path ./downloads --channel 1 --start "2024-01-01 00:00:00" --end "2024-01-01 23:59:59"
"""

import os 
import time
import logging
import json
import sys
import argparse
from datetime import datetime
from ctypes import *

from NetSDK.NetSDK import NetClient
from NetSDK.SDK_Enum import EM_USEDEV_MODE, EM_QUERY_RECORD_TYPE, EM_LOGIN_SPAC_CAP_TYPE
from NetSDK.SDK_Struct import NET_TIME, NET_RECORDFILE_INFO, NET_IN_PLAY_BACK_BY_TIME_INFO, NET_OUT_PLAY_BACK_BY_TIME_INFO, \
    C_LLONG, C_DWORD, C_LDWORD, NET_IN_LOGIN_WITH_HIGHLEVEL_SECURITY, NET_OUT_LOGIN_WITH_HIGHLEVEL_SECURITY
from NetSDK.SDK_Callback import fDisConnect, fHaveReConnect

logging.basicConfig(level=logging.INFO)

def DisConnectCallBack(lLoginID, pchDVRIP, nDVRPort, dwUser):
    print("PlayBack OffLine")

def ReConnectCallBack(lLoginID, pchDVRIP, nDVRPort, dwUser):
    print("PlayBack OnLine")

@WINFUNCTYPE(None, C_LLONG, C_DWORD, C_DWORD, C_LDWORD)
def DownLoadPosCallBack(lLoginID, pchDVRIP, nDVRPort, dwUser):
    pass

@WINFUNCTYPE(c_int, C_LLONG, C_DWORD, POINTER(c_ubyte), C_DWORD, C_LDWORD)
def DownLoadDataCallBack(lPlayHandle, dwDataType, pBuffer, dwBufSize, dwUser):
    return 1

@WINFUNCTYPE(None, C_LLONG, C_DWORD, C_DWORD, c_int, NET_RECORDFILE_INFO, C_LDWORD)
def TimeDownLoadPosCallBack(lPlayHandle, dwTotalSize, dwDownLoadSize, index, recordfileinfo, dwUser):
    try:
        dnd.update_download_progress(dwTotalSize, dwDownLoadSize)
    except Exception as e:
        logging.error(e)

class DahuaNVRDownloader(object):
    def __init__(self, ip, user, password, stream_type):
        self.ip = ip
        self.user = user
        self.password = password
        self.stream_type = stream_type
        self.resume_file = None
        self.sdk = NetClient()
        self.processing = False
        self.downloadID = None
        self.loginID = 0
        self.device_info = None
        self.error_msg = None
        self.last_progress = 0
        
        # 初始化回调函数
        m_DisConnectCallBack = fDisConnect(DisConnectCallBack)
        m_ReConnectCallBack = fHaveReConnect(ReConnectCallBack)
        self.sdk.InitEx(m_DisConnectCallBack)
        self.sdk.SetAutoReconnect(m_ReConnectCallBack)

    def resume_file_name(self):
        return f'resume_time_channel_{self.channel}.json'

    def load_resume_time(self):
        try:
            with open(self.resume_file_name(), 'r') as f:
                data = json.load(f)
            return data['resume_time']
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Failed to load resume time: {str(e)}")
            return None

    def save_resume_time(self, time):
        try:
            with open(self.resume_file_name(), 'w') as f:
                json.dump({'resume_time': time}, f)
        except Exception as e:
            logging.error(f"Failed to save resume time: {str(e)}")

    def update_download_progress(self, total_size, download_size):
        try:
            logging.debug("total_size:{} download_size:{}".format(total_size, download_size))
            if download_size == -1:
                self.sdk.StopDownload(self.downloadID)
                logging.warning("Download End")
            elif download_size == -2:
                logging.warning("Download Failed")
                self.StopDownload()
                self.save_resume_time(str(datetime.now()))
            else:
                if download_size >= total_size:
                    print(f"\r下载进度: 100.00% 完成")
                    self.StopDownload()
                else:
                    if total_size > 0:
                        percent = (download_size / total_size) * 100
                        # 只在进度变化超过1%时更新显示
                        if percent - self.last_progress >= 1.0:
                            print(f"\r下载进度: {percent:.2f}%", end="", flush=True)
                            self.last_progress = percent
        except Exception as e:
            logging.error(e)

    def StopDownload(self):
        self.processing = False

    def Login(self):
        stuInParam = NET_IN_LOGIN_WITH_HIGHLEVEL_SECURITY()
        stuInParam.dwSize = sizeof(NET_IN_LOGIN_WITH_HIGHLEVEL_SECURITY)
        stuInParam.szIP = self.ip.encode()
        stuInParam.nPort = 37777
        stuInParam.szUserName = self.user.encode()
        stuInParam.szPassword = self.password.encode()
        stuInParam.emSpecCap = EM_LOGIN_SPAC_CAP_TYPE.TCP
        stuInParam.pCapParam = None

        stuOutParam = NET_OUT_LOGIN_WITH_HIGHLEVEL_SECURITY()
        stuOutParam.dwSize = sizeof(NET_OUT_LOGIN_WITH_HIGHLEVEL_SECURITY)

        self.loginID, self.device_info, self.error_msg = self.sdk.LoginWithHighLevelSecurity(stuInParam, stuOutParam)
        login_result = self.loginID != 0
        if login_result:
            logging.info("login_ok" + self.error_msg)
            return False
        else:
            logging.info(self.device_info)
            logging.info("Login successful.")
            self.set_stream_type(self.stream_type)
            return True

    def set_stream_type(self, stream_type):
        stream_type = c_int(stream_type)
        result = self.sdk.SetDeviceMode(self.loginID, int(EM_USEDEV_MODE.RECORD_STREAM_TYPE), stream_type)
        if not result:
            logging.info(self.device_info)
            logging.info("Login successful.")
            self.set_stream_type(self.stream_type)
            return 0, 0, None

    def ConvertStrToDateTime(self, time_start, time_end):
        date_time_start = datetime.strptime(time_start, '%Y-%m-%d %H:%M:%S')
        date_time_end = datetime.strptime(time_end, '%Y-%m-%d %H:%M:%S')
    
        startDateTime = NET_TIME()
        startDateTime.dwYear = date_time_start.year
        startDateTime.dwMonth = date_time_start.month
        startDateTime.dwDay = date_time_start.day
        startDateTime.dwHour = date_time_start.hour
        startDateTime.dwMinute = date_time_start.minute
        startDateTime.dwSecond = date_time_start.second
    
        enddateTime = NET_TIME()
        enddateTime.dwYear = date_time_end.year
        enddateTime.dwMonth = date_time_end.month
        enddateTime.dwDay = date_time_end.day
        enddateTime.dwHour = date_time_end.hour
        enddateTime.dwMinute = date_time_end.minute
        enddateTime.dwSecond = date_time_end.second
    
        return startDateTime, enddateTime

    def delete_resume_file(self):
        """删除断点文件"""
        try:
            file_name = self.resume_file_name()
            if os.path.exists(file_name):
                os.remove(file_name)
                logging.info(f"Deleted resume file: {file_name}")
            else:
                logging.warning(f"Resume file does not exist: {file_name}")
        except Exception as e:
            logging.error(f"Failed to delete resume file: {e}")

    def DownloadByFile(self, save_file_path, nchannel, time_start, time_end, max_retries=555):
        resume_time = self.load_resume_time()
        if resume_time is not None:
            time_start = resume_time

        retries = 0
        success = False
        while retries < max_retries and not success:
            try:
                logging.info(f"Attempt {retries + 1}/{max_retries}: Downloading files from {time_start} to {time_end}")
                startDateTime, enddateTime = self.ConvertStrToDateTime(time_start, time_end)

                result, fileCount, infos = self.sdk.QueryRecordFile(
                    self.loginID, nchannel, int(EM_QUERY_RECORD_TYPE.ALL), startDateTime, enddateTime, None, 5000, False
                )

                if not result or fileCount == 0:
                    logging.warning(f"No files found for the given time range: {time_start} - {time_end}")
                    success = True
                    break

                for idx, info in enumerate(infos[:fileCount]):
                    st = info.starttime
                    et = info.endtime
                    file_name = f"{nchannel}-{st.dwYear:04d}_{st.dwMonth:02d}_{st.dwDay:02d}_{st.dwHour:02d}_{st.dwMinute:02d}_{st.dwSecond:02d}" \
                                f"-{et.dwYear:04d}_{et.dwMonth:02d}_{et.dwDay:02d}_{et.dwHour:02d}_{et.dwMinute:02d}_{et.dwSecond:02d}.dav"
                    save_file_name = os.path.join(save_file_path, file_name)
                    logging.info(f"Downloading file {idx + 1}/{fileCount}: {save_file_name}")

                    next_resume_time = f"{st.dwYear:04d}-{st.dwMonth:02d}-{st.dwDay:02d} {st.dwHour:02d}:{st.dwMinute:02d}:{st.dwSecond:02d}"
                    self.save_resume_time(next_resume_time)
                    logging.info(f"Set resume time to: {next_resume_time}")

                    self.DoDownload(save_file_name, nchannel, info.starttime, info.endtime, info.size)

                success = True  # Successful full cycle
            except Exception as e:
                retries += 1
                logging.error(f"Download attempt {retries}/{max_retries} failed: {str(e)}")
                time.sleep(5)

        if success:
            self.delete_resume_file()
        else:
            logging.critical("Unable to download files after maximum retries.")

    def DoDownload(self, save_file_name, nchannel, startDateTime, enddateTime, total_size=0):
        self.save_file_name = save_file_name
        self.last_progress = 0  # 重置进度
        print(f"开始下载: {os.path.basename(save_file_name)}")
        
        self.downloadID = self.sdk.DownloadByTimeEx(self.loginID, nchannel, int(EM_QUERY_RECORD_TYPE.ALL),
                                                    startDateTime, enddateTime, save_file_name,
                                                    TimeDownLoadPosCallBack, 0,
                                                    DownLoadDataCallBack, 0)
        self.processing = True
        while self.processing:
            time.sleep(1)
        self.sdk.StopDownload(self.downloadID)
        print()  # 换行

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='大华NVR录像下载工具 - 根据文件列表下载多个录像文件')
    parser.add_argument('--ip', required=True, help='NVR设备IP地址')
    parser.add_argument('--user', required=True, help='登录用户名')
    parser.add_argument('--password', required=True, help='登录密码')
    parser.add_argument('--path', required=True, help='下载保存路径')
    parser.add_argument('--channel', type=int, required=True, help='通道号')
    parser.add_argument('--start', required=True, help='开始时间 YYYY-MM-DD HH:MM:SS')
    parser.add_argument('--end', required=True, help='结束时间 YYYY-MM-DD HH:MM:SS')
    args = parser.parse_args()

    # 根据通道号创建子文件夹
    channel_path = os.path.join(args.path, str(args.channel))
    if not os.path.exists(channel_path):
        os.makedirs(channel_path)
        logging.info(f"创建通道文件夹: {channel_path}")

    dnd = DahuaNVRDownloader(args.ip, args.user, args.password, 0)
    dnd.channel = args.channel  # Store channel as an attribute for use in resume file naming

    # 确保登录后再尝试下载
    if dnd.Login():
        dnd.DownloadByFile(channel_path, args.channel, args.start, args.end)
    else:
        dnd.DownloadByFile(channel_path, args.channel, args.start, args.end)
