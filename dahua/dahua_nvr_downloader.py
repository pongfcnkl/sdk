# coding=utf-8
import os
import time
import logging
import json
import sys
import argparse
from tqdm import tqdm
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
        dnd.update_download_progress(dwTotalSize,dwDownLoadSize)
    except Exception as e:
        logging.error(e)

class DahuaNVRDownloader(object):
    def __init__(self,ip,user,password,stream_type):
        self.ip = ip
        self.user = user
        self.password = password
        self.stream_type = stream_type
        self.resume_file = None

        self.sdk = NetClient()
        m_DisConnectCallBack = fDisConnect(DisConnectCallBack)
        m_ReConnectCallBack = fHaveReConnect(ReConnectCallBack)
        self.sdk.InitEx(m_DisConnectCallBack)
        self.sdk.SetAutoReconnect(m_ReConnectCallBack)
    def resume_file_name(self):
        # Dynamically generate the resume file name based on the channel
        return f'resume_time_channel_{self.channel}.json'
        
    def load_resume_time(self):
        try:
            with open(self.resume_file_name(), 'r') as f:
                data = json.load(f)
            return data['resume_time']
        except FileNotFoundError:
            return None
    def save_resume_time(self, time):
        try:
            with open(self.resume_file_name(), 'w') as f:
                json.dump({'resume_time': time}, f)
        except FileNotFoundError:
            return None
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
                    self.progress_bar.update(total_size*1024 - self.progress_bar.n)
                    self.StopDownload()
                else:
                    if self.progress_bar is None:
                        self.progress_bar = tqdm(total=total_size*1024, unit='B', unit_scale=True)
                    else:
                        self.progress_bar.update(download_size*1024-self.progress_bar.n)
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
#            logging.info(self.device_info)
            logging.info("login_ok" + self.error_msg)
            return False
        else:
#            sys.exit("Login...")
            logging.info(self.device_info)
            logging.info("Login successful.")
            self.set_stream_type(self.stream_type)
            return True
#            sys.exit("Login...")
        return login_result

    def set_stream_type(self,stream_type):
        stream_type = c_int(stream_type)
        result = self.sdk.SetDeviceMode(self.loginID, int(EM_USEDEV_MODE.RECORD_STREAM_TYPE), stream_type)
        if not result:
            logging.info(self.device_info)
            logging.info("Login successful.")
            self.set_stream_type(self.stream_type)
            return 0, 0, None

    def ConvertStrToDateTime(self, time_start, time_end):
    # Replace underscores with spaces for parsing
        date_time_start = datetime.strptime(time_start, '%d-%m-%Y %H:%M:%S')
        date_time_end = datetime.strptime(time_end, '%d-%m-%Y %H:%M:%S')

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




    def DownloadByFile(self, save_file_path, nchannel, time_start, time_end, max_retries=555):
        resume_time = self.load_resume_time()
        if resume_time is not None:
            time_start = resume_time
        else:
            self.save_resume_time(time_start)
    
        retries = 0
        success = False
        while retries < max_retries and not success:
            try:
                logging.info(f"Attempt {retries + 1}/{max_retries}: Downloading files from {time_start}-{time_end}")
                startDateTime, enddateTime = self.ConvertStrToDateTime(time_start, time_end)
            
            # 查询记录文件
                result, fileCount, infos = self.sdk.QueryRecordFile(
                    self.loginID, nchannel, int(EM_QUERY_RECORD_TYPE.ALL), startDateTime, enddateTime, None, 5000, False
                )
            
                if not result or fileCount == 0:
                    logging.warning(f"No files found for the given time range: {time_start} - {time_end}")
                    success = True  # If no files found, treat it as success
                    break
            
            # Download all files
                for idx, info in enumerate(infos[:fileCount]):
                    st = info.starttime
                    et = info.endtime
                

                
                # Use both start and end time for the filename
                    file_name = "{}-{:04d}_{:02d}_{:02d}_{:02d}_{:02d}_{:02d}-{:04d}_{:02d}_{:02d}_{:02d}_{:02d}_{:02d}.dav".format(
                        nchannel, st.dwYear, st.dwMonth, st.dwDay, st.dwHour, st.dwMinute, st.dwSecond,
                        et.dwYear, et.dwMonth, et.dwDay, et.dwHour, et.dwMinute, et.dwSecond)
                    save_file_name = os.path.join(save_file_path, file_name)
                
                    logging.info(f"Downloading file {idx + 1}/{fileCount}: {save_file_name}")
                
                # Save resume time
                    self.save_resume_time(time_start)
                
                    self.DoDownload(save_file_name, nchannel, info.starttime, info.endtime, info.size)
            
                success = True  # Exit retry loop once all files are downloaded successfully
        
            except Exception as e:
                retries += 1
                logging.error(f"Download attempt {retries}/{max_retries} failed: {str(e)}")
                time.sleep(5)  # Wait for a while before retrying
    
        if not success:
            logging.critical("Failed to download files after maximum retries.")


        def DownloadByTime(self, save_file_name, nchannel, time_start, time_end):
            logging.info("Sarting download:{} - {}".format(time_start, time_end, nchannel))
            startDateTime, enddateTime = self.ConvertStrToDateTime(time_start, time_end)
            self.DoDownload(save_file_name, nchannel, startDateTime, enddateTime)

    def DoDownload(self, save_file_name, nchannel, startDateTime, enddateTime, total_size=0):
        self.save_file_name = save_file_name
        if os.path.exists(save_file_name):
            file_size = os.path.getsize(save_file_name)
            self.progress_bar = tqdm(total=total_size*1024-file_size, initial=file_size, unit='B', unit_scale=True)
        else:
            self.progress_bar = tqdm(total=total_size*1024, unit='B', unit_scale=True)
        self.downloadID = self.sdk.DownloadByTimeEx(self.loginID, nchannel, int(EM_QUERY_RECORD_TYPE.ALL),
                                                    startDateTime, enddateTime, save_file_name,
                                                    TimeDownLoadPosCallBack, 0,
                                                    DownLoadDataCallBack, 0)
        self.processing = True
        while self.processing:
            time.sleep(1)
        self.sdk.StopDownload(self.downloadID)
        self.progress_bar.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='下载')
    parser.add_argument('--ip', required=True, help='ip')
    parser.add_argument('--user', required=True, help='用户名')
    parser.add_argument('--password', required=True, help='密码')
    parser.add_argument('--path', required=True, help='下载位置')
    parser.add_argument('--channel', type=int, required=True, help='通道')
    parser.add_argument('--start', required=True, help='开始时间 DD-MM-YYYY HH:MM:SS')
    parser.add_argument('--end', required=True, help='结束时间 DD-MM-YYYY HH:MM:SS')

    args = parser.parse_args()

    dnd = DahuaNVRDownloader(args.ip, args.user, args.password, 0)
    dnd.channel = args.channel  # Store channel as an attribute for use in resume file naming

    # Ensure you login before attempting to download
    if dnd.Login():
        dnd.DownloadByFile(args.path, args.channel, args.start, args.end)
    else:
        dnd.DownloadByFile(args.path, args.channel, args.start, args.end)
