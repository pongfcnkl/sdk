# _*_ coding:utf-8 _*_

from ctypes import *
import platform
import re
import os

def system_get_platform_info():
    sys_platform = platform.system().lower().strip()
    python_bit = platform.architecture()[0]
    python_bit_num = re.findall('(\d+)\w*', python_bit)[0]
    return sys_platform, python_bit_num

sys_platform, python_bit_num = system_get_platform_info()
system_type = sys_platform + python_bit_num

netsdkdllpath_dict = {'windows64': os.path.dirname(__file__) + '\\Libs\\win64\\'+'dhnetsdk.dll', 'windows32': os.path.dirname(__file__) + '\\Libs\\win32\\'+'dhnetsdk.dll',
                      'linux64': os.path.dirname(__file__) + '/Libs/linux64/libdhnetsdk.so', 'linux32': os.path.dirname(__file__) + '/Libs/linux32/libdhnetsdk.so'}
configdllpath_dict = {'windows64': os.path.dirname(__file__) + '\\Libs\\win64\\'+'dhconfigsdk.dll', 'windows32': os.path.dirname(__file__) + '\\Libs\\win32\\'+'dhconfigsdk.dll',
                      'linux64': os.path.dirname(__file__) + '/Libs/linux64/libdhconfigsdk.so', 'linux32': os.path.dirname(__file__) + '/Libs/linux32/libdhconfigsdk.so'}
playsdkdllpath_dict = {'windows64': os.path.dirname(__file__) + '\\Libs\\win64\\'+'dhplay.dll', 'windows32': os.path.dirname(__file__) + '\\Libs\\win32\\'+'dhplay.dll',
                      'linux64': os.path.dirname(__file__) + '/Libs/linux64/libdhplay.so', 'linux32': os.path.dirname(__file__) + '/Libs/linux32/libdhplay.so'}
renderdllpath_dict = {'windows64': os.path.dirname(__file__) + '\\Libs\\win64\\'+'RenderEngine.dll', 'windows32': os.path.dirname(__file__) + '\\Libs\\win32\\'+'RenderEngine.dll',
                      'linux64': os.path.dirname(__file__) + '/Libs/linux64/libRenderEngine.so', 'linux32': os.path.dirname(__file__) + '/Libs/linux32/libRenderEngine.so'}
infrasdkdllpath_dict = {'windows64': os.path.dirname(__file__) + '\\Libs\\win64\\'+'Infra.dll', 'windows32': os.path.dirname(__file__) + '\\Libs\\win32\\'+'Infra.dll',
                      'linux64': os.path.dirname(__file__) + '/Libs/linux64/libInfra.so', 'linux32': os.path.dirname(__file__) + '/Libs/linux32/libInfra.so'}

C_LLONG_DICT = {'windows64': c_longlong, 'windows32': c_long, 'linux32': c_long, 'linux64': c_long}
C_LONG_DICT = {'windows64': c_long, 'windows32': c_long, 'linux32': c_int, 'linux64': c_int}
C_LDWORD_DICT = {'windows64': c_longlong, 'windows32': c_ulong, 'linux32': c_long, 'linux64': c_long}
C_DWORD_DICT = {'windows64': c_ulong, 'windows32': c_ulong, 'linux32': c_uint, 'linux64': c_uint}

C_LLONG = C_LLONG_DICT[system_type]
C_LONG = C_LONG_DICT[system_type]
C_LDWORD = C_LDWORD_DICT[system_type]
C_DWORD = C_DWORD_DICT[system_type]
C_TP_U64 = c_ulonglong
C_BOOL = c_int
C_UINT = c_uint
C_BYTE = c_ubyte
C_ENUM = c_int

if sys_platform == 'linux':
    load_library = cdll.LoadLibrary
    CB_FUNCTYPE = CFUNCTYPE
elif sys_platform == 'windows':
    load_library = windll.LoadLibrary
    CB_FUNCTYPE = WINFUNCTYPE
else:
    print("************不支持该平台**************")
    exit(0)

netsdkdllpath = netsdkdllpath_dict[system_type]
configdllpath = configdllpath_dict[system_type]
playsdkdllpath = playsdkdllpath_dict[system_type]
rendersdkdllpath = renderdllpath_dict[system_type]
infrasdkdllpath = infrasdkdllpath_dict[system_type]


class NETSDK_INIT_PARAM(Structure):
    """
    初始化参数;Initialization parameter
    """
    _fields_ = [
        ("nThreadNum", c_int),                 # 指定NetSDK常规网络处理线程数, 当值为0时, 使用内部默认值; specify netsdk's normal network process thread number, zero means using default value
        ("bReserved", c_ubyte * 1024),         # 保留字节; reserved
    ]


class NET_PARAM(Structure):
    """
    设置登入时的相关参数;The corresponding parameter when setting log in
    """
    _fields_ = [
        ("nWaittime", c_int),                 # 等待超时时间(毫秒为单位),为0默认5000ms;Waiting time(unit is ms), 0:default 5000ms.
        ("nConnectTime", c_int),              # 连接超时时间(毫秒为单位),为0默认1500ms;Connection timeout value(Unit is ms), 0:default 1500ms.
        ("nConnectTryNum", c_int),            # 连接尝试次数,为0默认1次;Connection trial times, 0:default 1.
        ("nSubConnectSpaceTime", c_int),      # 子连接之间的等待时间(毫秒为单位),为0默认10ms;Sub-connection waiting time(Unit is ms), 0:default 10ms.
        ("nGetDevInfoTime", c_int),           # 获取设备信息超时时间,为0默认1000ms;Access to device information timeout, 0:default 1000ms.
        ("nConnectBufSize", c_int),           # 每个连接接收数据缓冲大小(字节为单位),为0默认250*1024;Each connected to receive data buffer size(Bytes), 0:default 250*1024
        ("nGetConnInfoTime", c_int),          # 获取子连接信息超时时间(毫秒为单位),为0默认1000ms;Access to sub-connect information timeout(Unit is ms), 0:default 1000ms.
        ("nSearchRecordTime", c_int),         # 按时间查询录像文件的超时时间(毫秒为单位),为0默认为3000ms;Timeout value of search video (unit ms), default 3000ms
        ("nsubDisconnetTime", c_int),         # 检测子链接断线等待时间(毫秒为单位),为0默认为60000ms;dislink disconnect time,0:default 60000ms
        ("byNetType", c_ubyte),               # 网络类型, 0-LAN, 1-WAN;net type, 0-LAN, 1-WAN
        ("byPlaybackBufSize", c_ubyte),       # 回放数据接收缓冲大小（M为单位）,为0默认为4M;playback data from the receive buffer size(m),when value = 0,default 4M
        ("bDetectDisconnTime", c_ubyte),      # 心跳检测断线时间(单位为秒),为0默认为60s,最小时间为2s;Pulse detect offline time(second) .When it is 0, the default setup is 60s, and the min time is 2s
        ("bKeepLifeInterval", c_ubyte),       # 心跳包发送间隔(单位为秒),为0默认为10s,最小间隔为2s;Pulse send out interval(second). When it is 0, the default setup is 10s, the min internal is 2s.
        ("nPicBufSize", c_int),               # 实时图片接收缓冲大小（字节为单位）,为0默认为2*1024*1024;actual pictures of the receive buffer size(byte)when value = 0,default 2*1024*1024
        ("bReserved", c_ubyte*4)              # 保留字段字段;reserved
    ]


class NET_DEVICEINFO(Structure):
    """
    设备信息;Device info
    """
    _fields_ = [
        ('sSerialNumber', c_char * 48),     # 序列号;serial number
        ('byAlarmInPortNum', c_ubyte),      # DVR报警输入个数;DVR alarm input amount
        ('byAlarmOutPortNum', c_ubyte),     # DVR报警输出个数;DVR alarm output amount
        ('byDiskNum', c_ubyte),             # DVR硬盘个数;DVR HDD amount
        ('byDVRType', c_ubyte),             # DVR类型,见枚举 NET_DEVICE_TYPE DVR type.Please refer to NET_DEVICE_TYPE
        ('byChanNum', c_ubyte),             # DVR通道个数,登陆成功时有效,当登陆失败原因为密码错误时,通过此参数通知用户,剩余登陆次数,为0时表示此参数无效; DVR channel amount,When login failed due to password error, notice user via this parameter, remaining login times, is 0 means this parameter is invalid
    ]


class LOG_SET_PRINT_INFO(Structure):
    """
    SDK全局日志打印信息;SDK global log print
    """
    _fields_ = [
        ('dwSize', C_DWORD),                # 结构体大小;Structure size
        ('bSetFilePath', c_int),            # 是否重设日志路径;reset log path
        ('szLogFilePath', c_char * 260),    # 日志路径(默认"./sdk_log/sdk_log.log");log path(default"./sdk_log/sdk_log.log")
        ('bSetFileSize', c_int),            # 是否重设日志文件大小;reset log size
        ('nFileSize', c_uint),              # 每个日志文件的大小(默认大小10240), 单位:KB;each log file size(default size 10240), unit:KB
        ('bSetFileNum', c_int),             # 是否重设日志文件个数;reset log file number
        ('nFileNum', c_uint),               # 绕接日志文件个数(默认大小10);log file quantity(default size 10)
        ('bSetPrintStrategy', c_int),       # 是否重设日志打印输出策略;reset log print strategy
        ('nPrintStrategy', c_uint),         # 日志输出策略, 0:输出到文件(默认); 1:输出到窗口;log out strategy, 0: output to file(defualt); 1:output to window
        ('byReserved', c_ubyte * 4),        # 字节对齐;Byte alignment
        ('cbSDKLogCallBack', CB_FUNCTYPE(c_int, c_char_p, c_uint, C_LDWORD)),   # 日志回调，需要将sdk日志回调出来时设置，默认为None,对应SDK_Callback的fSDKLogCallBack;log callback, (default None),corresponding to SDK_Callback's fSDKLogCallBack
        ('dwUser', C_LDWORD)                # 用户数据;UserData
    ]


class DEVICE_NET_INFO_EX(Structure):
    """
    设备信息;Device info
    对应CLIENT_StartSearchDevices接口
    Corresponding to CLIENT_StartSearchDevices
    """
    _fields_ = [
        ('iIPVersion', c_int),          # 4代表IPV4,6代表IPV6;4 for IPV4, 6 for IPV6
        ('szIP', c_char*64),            # IP IPV4形如"192.168.0.1" IPV6形如"2008::1/64",;IP IPV4 likes "192.168.0.1" ,IPV6 likes "2008::1/64"
        ('nPort', c_int),               # tcp端口;Port
        ('szSubmask', c_char*64),       # 子网掩码 IPV6无子网掩码;Subnet mask
        ('szGateway', c_char*64),       # 网关;Gate way
        ('szMac', c_char*40),           # MAC地址;Mac
        ('szDeviceType', c_char*32),    # 设备类型;Device type
        ('byManuFactory', c_ubyte),     # 目标设备的生产厂商,具体参考sdk_enum.py的EM_IPC_TYPE;Manu factory,refer to EM_IPC_TYPE in sdk_enum.py
        ('byDefinition', c_ubyte),      # 1-标清 2-高清;1-Standard definition 2-High definition
        ('bDhcpEn', c_bool),            # Dhcp使能状态, true-开, false-关;Dhcp, true-open, false-close
        ('byReserved1', c_ubyte),       # 字节对齐;reserved
        ('verifyData', c_char * 88),    # 校验数据 通过异步搜索回调获取(在修改设备IP时会用此信息进行校验);ECC data
        ('szSerialNo', c_char * 48),    # 序列号;serial no
        ('szDevSoftVersion', c_char * 128),  # 设备软件版本号;soft version
        ('szDetailType', c_char * 32),  # 设备型号;device detail type
        ('szVendor', c_char * 128),     # OEM客户类型; OEM type
        ('szDevName', c_char * 64),     # 设备名称;device name
        ('szUserName', c_char * 16),    # 登陆设备用户名（在修改设备IP时需要填写）;user name for log in device(it need be filled when modify device ip)
        ('szPassWord', c_char * 16),    # 登陆设备密码（在修改设备IP时需要填写）;pass word for log in device(it need be filled when modify device ip)
        ('nHttpPort', c_ushort),        # HTTP服务端口号;HTTP server port
        ('wVideoInputCh', c_ushort),    # 视频输入通道数;count of video input channel
        ('wRemoteVideoInputCh', c_ushort),  # 远程视频输入通道数;count of remote video input
        ('wVideoOutputCh', c_ushort),   # 视频输出通道数;count of video output channel
        ('wAlarmInputCh', c_ushort),    # 报警输入通道数;count of alarm input
        ('wAlarmOutputCh', c_ushort),   # 报警输出通道数;count of alarm output
        ('bNewWordLen', c_int),         # TRUE使用新密码字段szNewPassWord;TRUE:szNewPassWord Enable
        ('szNewPassWord', c_char*64),   # 登陆设备密码（在修改设备IP时需要填写）;pass word for log in device(it need be filled when modify device ip)
        ('byInitStatus', c_ubyte),      # 设备初始化状态，按位确定初始化状态;init status
                                        # bit0~1：0-老设备，没有初始化功能 1-未初始化账号 2-已初始化账户;bit0~1：0-old device, can not be init; 1-not init; 2-already init
                                        # bit2~3：0-老设备，保留 1-公网接入未使能 2-公网接入已使能;bit2~3：0-old device,reserved; 1-connect to public network unable; 2-connect to public network enable
                                        # bit4~5：0-老设备，保留 1-手机直连未使能 2-手机直连使能;bit4~5：0-old device,reserved; 1-connect to cellphone unable; 2-connect to cellphone enable
                                        # bit6~7: 0- 未知 1-不支持密码重置 2-支持密码重置;bit6~7: 0- unknown 1-unsupported reset password 2-support password
        ('byPwdResetWay', c_ubyte),     # 支持密码重置方式：按位确定密码重置方式，只在设备有初始化账号时有意义;the way supported for reset password:make sense when the device is init
                                        # bit0-支持预置手机号 bit1-支持预置邮箱 ,bit2-支持文件导出;bit0-support reset password by cellphone; bit1-support reset password by mail; bit2-support reset password by XML file;
                                        # bit3-支持密保问题 bit4-支持更换手机号;bit3-support reset password by security question; bit4-support reset password by change cellphone
        ('bySpecialAbility', c_ubyte),  # 设备初始化能力，按位确定初始化能力,高八位 bit0-2D Code修改IP: 0 不支持 1 支持, bit1-PN制:0 不支持 1支持
                                        # ENGLISH_LANG:special ability of device ,high eight bit, bit0-2D Code:0 support  1 no support, bit1-PN:0 support  1 no support
        ('szNewDetailType', c_char*64),     # 设备型号;device detail type
        ('bNewUserName', c_int),        # true(szNewUserName)字段;TRUE:szNewUserName enable
        ('szNewUserName', c_char * 64), # 登陆设备用户名（在修改设备IP时需要填写）;new user name for login device(it need be filled when modify device ip)
        ('byPwdFindVersion', c_ubyte),  # 密码找回的版本号,设备支持密码重置时有效;;password find version, effective when device supports reset password
                                        # 0-设备使用的是老方案的密码重置版本;1-支持预留联系方式进行密码重置操作;2-支持更换联系方式进行密码重置操作;
                                        # ENGLISH_LANG:0-device of old scheme reset password version;1-support reset password by reserved contact;2-support reset password by change contact;
        ('szDeviceID', c_char * 24),    # 不对接通用客户端;do not use for general client
        ('dwUnLoginFuncMask', C_DWORD), # Bit0 Wifi列表扫描及WLan设置,Bit1 支持会话外修改过期密码;function mask before login, Bit0 means wifi config
        ('szMachineGroup', c_char * 64),  # 设备分组;machine group
        ('emIPVersionFrom', C_ENUM),    # 通过哪种网络搜索方式发现该设备;0:从IPv4组播地址发现设备 1:从IPv6组播地址发现设备 Refer: EM_IPVERSION;network search method to find the device;(0:form IPv4 Multicast 1:form IPv6 Multicast) Refer: EM_IPVERSION;
        ('szCountryCode', c_char * 3),  # 设备wifi国家码;Device WiFi country code, such as: "CN": China; "US": United States; "JP": Japan; "NA": NorthAmerica;
        ('cReserved', c_char * 5),      # 扩展字段;reserved;
    ]


class DEVICE_NET_INFO_EX2(Structure):
    """
    对应StartSearchDevicesEx接口;Corresponding to StartSearchDevicesEx
    """
    _fields_ = [
        ('stuDevInfo', DEVICE_NET_INFO_EX), # 设备信息结构体;device net info
        ('szLocalIP', c_char*64),           # 搜索到设备的本地IP地址;local ip
        ('cReserved', c_char*2048)          # 保留字段;reserved
    ]


class NET_DEVICEINFO_Ex(Structure):
    """
    设备信息扩展;Device extension info
    """
    _fields_ = [
        ('sSerialNumber', c_char * 48),     # 序列号;serial number
        ('nAlarmInPortNum', c_int),         # DVR报警输入个数;count of DVR alarm input
        ('nAlarmOutPortNum', c_int),        # DVR报警输出个数;count of DVR alarm output
        ('nDiskNum', c_int),                # DVR硬盘个数;number of DVR disk
        ('nDVRType', c_int),                # DVR类型;DVR type, refer to NET_DEVICE_TYPE
        ('nChanNum', c_int),                # DVR通道个数;number of DVR channel
        ('byLimitLoginTime', c_char),       # 在线超时时间,为0表示不限制登陆,非0表示限制的分钟数;Online Timeout, Not Limited Access to 0, not 0 Minutes Limit Said
        ('byLeftLogTimes', c_char),         # 当登陆失败原因为密码错误时,通过此参数通知用户,剩余登陆次数,为0时表示此参数无效; When login failed due to password error, notice user via this parameter, remaining login times, is 0 means this parameter is invalid
        ('bReserved', c_char * 2),          # 保留字节,字节对齐;keep bytes, bytes aligned
        ('nLockLeftTime', c_int),           # 当登陆失败,用户解锁剩余时间（秒数）, -1表示设备未设置该参数;when log in failed, the left time for users to unlock (seconds), -1 indicate the device haven't set the parameter
        ('Reserved', c_char * 24),          # 保留;reserved
    ]


class NET_IN_LOGIN_WITH_HIGHLEVEL_SECURITY(Structure):
    """
    LoginWithHighLevelSecurity 输入参数;LoginWithHighLevelSecurity input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),          # 结构体大小;Structrue size
        ('szIP', c_char*64),          # IP地址;IP address
        ('nPort', c_int),             # 端口;Port
        ('szUserName', c_char * 64),  # 用户名;User name
        ('szPassword', c_char * 64),  # 密码;Password
        ('emSpecCap', c_int),         # 登录模式,具体信息见sdk_enum.py内的EM_LOGIN_SPAC_CAP_TYPE;Spec login cap，refer to EM_LOGIN_SPAC_CAP_TYPE in sdk_enum.py
        ('byReserved', c_ubyte*4),    # 保留字节;Reserved
        ('pCapParam', c_void_p),      # emSpecCap = 0,pCapParam:None;emSpecCap = 0,pCapParam:None
                                      # emSpecCap = 2,pCapParam:None;emSpecCap = 2,pCapParam:None
                                      # emSpecCap = 3,pCapParam:None;emSpecCap = 3,pCapParam:None
                                      # emSpecCap = 4,pCapParam:None;emSpecCap = 4,pCapParam:None
                                      # emSpecCap = 6,pCapParam:None;emSpecCap = 6,pCapParam:None
                                      # emSpecCap = 7,pCapParam:None;emSpecCap = 7,pCapParam:None
                                      # emSpecCap = 9,pCapParam:填入远程设备的名字的字符串;emSpecCap = 9,pCapParam is string of remote device name
                                      # emSpecCap = 12,pCapParam:None;emSpecCap = 12,pCapParam:None
                                      # emSpecCap = 13,pCapParam:None;emSpecCap = 13,pCapParam:None
                                      # emSpecCap = 14,pCapParam:None;emSpecCap = 14,pCapParam:None
                                      # emSpecCap = 15,pCapParam:Socks5服务器的IP&&port&&ServerName&&ServerPassword字符串;emSpecCap = 15,pCapParam:IP&&port&&ServerName&&ServerPassword string of Socket5 server
                                      # emSpecCap = 16,pCapParam:SOCKET值;emSpecCap = 16,pCapParam:SOCKET value
                                      # emSpecCap = 19,pCapParam:None;emSpecCap = 19,pCapParam:None
                                      # emSpecCap = 20,pCapParam:None;emSpecCap = 20,pCapParam:None
        ('emTLSCap', C_ENUM),         # 登录的TLS模式，目前仅支持emSpecCap为EM_LOGIN_SPEC_CAP_TCP，EM_LOGIN_SPEC_CAP_SERVER_CONN 模式下的 tls登陆(TLS加密优先使用该选项) Refer: EM_LOGIN_TLS_TYPE;TLS mode of login, currently only supports emSpecCap for EM_LOGIN_SPEC_CAP_TCP and EM_LOGIN_SPEC_CAP_SERVER_CONN mode tls login(Use this option first for TLS encryption) Refer: EM_LOGIN_TLS_TYPE;
    ]


class NET_OUT_LOGIN_WITH_HIGHLEVEL_SECURITY(Structure):
    """
       LoginWithHighLevelSecurity 输出参数;LoginWithHighLevelSecurity output param
       """
    _fields_ = [
        ('dwSize', C_DWORD),                               # 结构体大小;Structrue size
        ('stuDeviceInfo', NET_DEVICEINFO_Ex),              # 设备信息;Device info
        ('nError', c_int),                                 # 错误码，见 Login 接口错误码;Error
        ('byReserved', c_ubyte * 132)                      # 预留字段,;Reserved
    ]


class NET_IN_STARTSERACH_DEVICE(Structure):
    """
    StartSearchDevicesEx接口输入参数;StartSearchDevicesEx input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),            # 结构体大小;Structrue size
        ('szLocalIp', c_char*64),       # 发起搜索的本地IP;local IP
        ('cbSearchDevices', CB_FUNCTYPE(None, C_LLONG, POINTER(DEVICE_NET_INFO_EX2), c_void_p)),   #设备信息回调函数;search device call back
        ('pUserData', c_void_p),        # 用户自定义数据;user data
        ('emSendType', c_int)           # 下发搜索类型,对应EM_SEND_SEARCH_TYPE;send search type,refer to EM_SEND_SEARCH_TYPE
    ]


class NET_OUT_STARTSERACH_DEVICE(Structure):
    """
        StartSearchDevicesEx接口输出参数;StartSearchDevicesEx output param
        """
    _fields_ = [
        ('dwSize', C_DWORD)           # 结构体大小，ENGLISH_LANG:Structrue size
    ]


class DEVICE_IP_SEARCH_INFO_IP(Structure):
    """
    具体待搜索的IP信息;the IPs info for search
    """
    _fields_ = [
        ('IP', c_char*64)               # 具体待搜索的IP信息;the IP for search
    ]


class DEVICE_IP_SEARCH_INFO(Structure):
    """
    SearchDevicesByIPs接口输入参数; SearchDevicesByIPs input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),                      # 结构体大小;Structure size
        ('nIpNum', c_int),                        # 当前搜索的IP个数;the IPs number for search
        ('szIP', DEVICE_IP_SEARCH_INFO_IP * 256)  # 具体待搜索的IP信息;the IPs info for search
    ]


class NET_IN_INIT_DEVICE_ACCOUNT(Structure):
    """
       InitDevAccount接口输入参数;InitDevAccount interface input param
       """
    _fields_ = [
        ('dwSize', C_DWORD),            # 结构体大小;Structure size
        ('szMac', c_char*40),           # 设备mac地址;mac addr
        ('szUserName', c_char * 128),   # 用户名;user name
        ('szPwd', c_char * 128),        # 设备密码;password
        ('szCellPhone', c_char * 32),   # 预留手机号;cellphone
        ('szMail', c_char * 64),        # 预留邮箱;mail addr
        ('byInitStatus', c_ubyte),      # 该字段废弃;this field already abandoned
        ('byPwdResetWay', c_ubyte),     # 设备支持的密码重置方式：搜索设备接口(StartSearchDevicesEx、SearchDevicesByIPs回调函数)返回字段byPwdResetWay的值
                                          # 该值的具体含义见 DEVICE_NET_INFO_EX2 结构体，需要与设备搜索接口返回的 byPwdResetWay 值保持一致
                                          # bit0 : 1-支持预留手机号，此时需要在szCellPhone数组中填入预留手机号(如果需要设置预留手机) ;
                                          # bit1 : 1-支持预留邮箱，此时需要在szMail数组中填入预留邮箱(如果需要设置预留邮箱)
                                          # the way supported for reset password:byPwdResetWay value of StartSearchDevicesEx's , SearchDevicesByIPs's callback function
                                          # the meaning of this parameter refers to DEVICE_NET_INFO_EX2, the value must be same as byPwdResetWay returned by StartSearchDevicesEx,SearchDevicesByIPs
                                          # bit0 : 1-support reset password by cellphone, you should set cellphone in szCellPhone if you need to set cellphone
                                          # bit1 : 1-support reset password by mail, you should set mail address in szMail if you need to set mail address
        ('byReserved', c_ubyte*2)       # 保留字段;Reserve
    ]


class NET_OUT_INIT_DEVICE_ACCOUNT(Structure):
    """
    InitDevAccount接口输出参数;InitDevAccount interface output param
    """
    _fields_ = [
        ('dwSize', C_DWORD)           # 结构体大小;Structrue size
    ]


class NET_TIME(Structure):
    """
    时间;time
    """
    _fields_ = [
        ('dwYear', C_DWORD),    # 年;Year
        ('dwMonth', C_DWORD),   # 月;Month
        ('dwDay', C_DWORD),     # 日;Date
        ('dwHour', C_DWORD),    # 时;Hour
        ('dwMinute', C_DWORD),  # 分;Minute
        ('dwSecond', C_DWORD)   # 秒;Second
    ]

class NET_RECORDFILE_INFO(Structure):
    """
    录像文件信息; Record file information
    """
    _fields_ = [
        ('ch', c_uint),                # 通道号; Channel number
        ('filename', c_char * 124),    # 文件名; File name
        ('framenum', c_uint),          # 文件总帧数; the total number of file frames
        ('size', c_uint),              # 文件长度, 单位为Kbyte; File length, unit: Kbyte
        ('starttime', NET_TIME),       # 开始时间; Start time
        ('endtime', NET_TIME),         # 结束时间; End time
        ('driveno', c_uint),           # 磁盘号(区分网络录像和本地录像的类型,0－127表示本地录像,其中64表示光盘1,128表示网络录像); HDD number
        ('startcluster', c_uint),      # 起始簇号; Initial cluster number
        ('nRecordFileType', c_ubyte),  # 录象文件类型  0：普通录象；1：报警录象；2：移动检测；3：卡号录象；4：图片, 5: 智能录像, 19: POS录像, 255:所有录像; Recorded file type  0:general record;1:alarm record ;2:motion detection;3:card number record ;4:image ; 19:Pos record ;255:all
        ('bImportantRecID', c_ubyte),  # 0:普通录像 1:重要录像; 0:general record 1:Important record
        ('bHint', c_ubyte),            # 文件定位索引(nRecordFileType==4<图片>时,bImportantRecID<<8 +bHint ,组成图片定位索引 ); Document Indexing
        ('bRecType', c_ubyte)          # 0-主码流录像 1-辅码1流录像 2-辅码流2 3-辅码流3录像; 0-main stream record 1-sub1 stream record 2-sub2 stream record 3-sub3 stream record
    ]


class NET_TIME_EX(Structure):
    """
    时间;time
    """
    _fields_ = [
        ('dwYear', C_DWORD),        # 年;Year
        ('dwMonth', C_DWORD),       # 月;Month
        ('dwDay', C_DWORD),         # 日;Date
        ('dwHour', C_DWORD),        # 时;Hour
        ('dwMinute', C_DWORD),      # 分;Minute
        ('dwSecond', C_DWORD),      # 秒;Second
        ('dwMillisecond', C_DWORD), # 毫秒;Millisecond
        ('dwUTC', C_DWORD),         # utc时间(获取时0表示无效，非0有效,下发无效);utc query: zero means invaild, non-zero means vaild;  set:invalid
        ('dwReserved', C_DWORD)     # 预留字段;reserved data
    ]

class SDK_RECT(Structure):
    """
     区域；各边距按整长8192的比例;Zone;Each margin is total lenght :8192
     """
    _fields_ = [
        ('left', c_long),       # 左;left
        ('top', c_long),        # 顶;top
        ('right', c_long),      # 右;right
        ('bottom', c_long)      # 底;bottom
    ]

class NET_RECT_EX(Structure):
    """
    区域；各边距按整长8192的比例
    Zone;Each margin is total lenght :8192
    """
    _fields_ = [
        ('left', c_long),  
        ('top', c_long),  
        ('right', c_long),  
        ('bottom', c_long),  
    ]


class SDK_POINT(Structure):
    """
     二维空间点;2 dimension point
     """
    _fields_ = [
        ('nx', c_short),        # x轴;x
        ('ny', c_short)         # y轴;y
    ]

class NET_POINT(Structure):
    """
    二维空间点
    2 dimension point
    """
    _fields_ = [
        ('nx', c_short),  
        ('ny', c_short),  
    ]
    

class SDK_PIC_INFO(Structure):
    """
     物体对应图片文件信息;picture info
     """
    _fields_ = [
        ('dwOffSet', C_DWORD),      # 文件在二进制数据块中的偏移位置, 单位:字节;current picture file's offset in the binary file, byte
        ('dwFileLenth', C_DWORD),   # 文件大小, 单位:字节;current picture file's size, byte
        ('wWidth', c_ushort),       # 图片宽度, 单位:像素;picture width, pixel
        ('wHeight', c_ushort),      # 图片高度, 单位:像素;picture high, pixel
        ('pszFilePath', c_char_p),  # 文件路径;File path
                                    # 鉴于历史原因,该成员只在事件上报时有效,用户使用该字段时需要自行申请空间进行拷贝保存;User use this field need to apply for space for copy and storage,When submit to the server, the algorithm has checked the image or not
        ('bIsDetected', c_ubyte),   # 图片是否算法检测出来的检测过的提交识别服务器时,则不需要再时检测定位抠图,1:检测过的,0:没有检测过;When submit to the server, the algorithm has checked the image or not
        ('bReserved', C_BYTE * 2),  # 预留字节数;reserved data;
        ('byQulityScore', C_BYTE),  # 人脸抓拍质量分数, 0-100;Quality score of face capture, range: 0-100;
        ('nFilePathLen', c_int),    # 文件路径长度 既pszFilePath 用户申请的大小;File path Len of pszFilePath
        ('stuPoint', SDK_POINT),    # 小图左上角在大图的位置，使用绝对坐标系;The upper left corner of the figure is in the big picture. Absolute coordinates are used
        ('nIndexInData', C_UINT),   # 在上传图片数据中的图片序号;The serial number of the picture in the uploaded picture data;
    ]

class NET_A_PIC_INFO(Structure):
    """
    物体对应图片文件信息
    picture info
    """
    _fields_ = [
        ('dwOffSet', C_DWORD),  # 文件在二进制数据块中的偏移位置, 单位:字节;current picture file's offset in the binary file, byte;
        ('dwFileLenth', C_DWORD),  # 文件大小, 单位:字节;current picture file's size, byte;
        ('wWidth', c_uint16),  # 图片宽度, 单位:像素;picture width, pixel;
        ('wHeight', c_uint16),  # 图片高度, 单位:像素;picture high, pixel;
        ('pszFilePath', POINTER(c_char)),  # 鉴于历史原因,该成员只在事件上报时有效文件路径用户使用该字段时需要自行申请空间进行拷贝保存;File pathUser use this field need to apply for space for copy and storage;
        ('bIsDetected', C_BYTE),  # 图片是否算法检测出来的检测过的提交识别服务器时,则不需要再时检测定位抠图,1:检测过的,0:没有检测过;When submit to the server, the algorithm has checked the image or not;
        ('bReserved', C_BYTE * 2),  # 预留字节数;reserved data;
        ('byQulityScore', C_BYTE),  # 目标抓拍质量分数, 0-100;Quality score of target capture, range: 0-100;
        ('nFilePathLen', c_int),  # 文件路径长度 既pszFilePath 用户申请的大小;File path Len of pszFilePath;
        ('stuPoint', NET_POINT),  # 小图左上角在大图的位置，使用绝对坐标系;The upper left corner of the figure is in the big picture. Absolute coordinates are used;
        ('nIndexInData', C_UINT),  # 在上传图片数据中的图片序号;The serial number of the picture in the uploaded picture data;
    ]

class NET_A_MSG_OBJECT(Structure):
    """
    视频分析物体信息结构体
    Struct of object info for video analysis
    """
    _pack_ = 4
    _fields_ = [
        ('nObjectID', c_int),  # 物体ID,每个ID表示一个唯一的物体;Object ID,each ID represent a unique object;
        ('szObjectType', c_char * 128),  # 物体类型;Object type;
        ('nConfidence', c_int),  # 置信度(0~100),值越大表示置信度越高;Confidence(0~100),a high value indicate a high confidence;
        ('nAction', c_int),  # 物体动作:1:Appear 2:Move 3:Stay 4:Remove 5:Disappear 6:Split 7:Merge 8:Rename;Object action:1:Appear 2:Move 3:Stay 4:Remove 5:Disappear 6:Split 7:Merge 8:Rename;
        ('BoundingBox', NET_RECT_EX),  # 包围盒;BoundingBox;
        ('Center', NET_POINT),  # 物体型心;The shape center of the object;
        ('nPolygonNum', c_int),  # 多边形顶点个数;the number of culminations for the polygon;
        ('Contour', NET_POINT * 16),  # 较精确的轮廓多边形;a polygon that have a exactitude figure;
        ('rgbaMainColor', C_DWORD),  # 表示车牌、车身等物体主要颜色；按字节表示,分别为红、绿、蓝和透明度,例如:RGB值为(0,255,0),透明度为0时, 其值为0x00ff0000.;The main color of the object;the first byte indicate red value, as byte order as green, blue, transparence, for example:RGB(0,255,0),transparence = 0, rgbaMainColor = 0x00ff0000.;
        ('szText', c_char * 128),  # 物体上相关的带0结束符文本,比如车牌,集装箱号等等"ObjectType"为"Vehicle"或者"Logo"时（尽量使用Logo。Vehicle是为了兼容老产品）表示车标,支持："Unknown"未知"Audi" 奥迪"Honda" 本田"Buick" 别克"Volkswagen" 大众"Toyota" 丰田"BMW" 宝马"Peugeot" 标致"Ford" 福特"Mazda" 马自达"Nissan" 尼桑(日产)"Hyundai" 现代"Suzuki" 铃木"Citroen" 雪铁龙"Benz" 奔驰"BYD" 比亚迪"Geely" 吉利"Lexus" 雷克萨斯"Chevrolet" 雪佛兰"Chery" 奇瑞"Kia" 起亚"Charade" 夏利"DF" 东风"Naveco" 依维柯"SGMW" 五菱"Jinbei" 金杯"JAC" 江淮"Emgrand" 帝豪"ChangAn" 长安"Great Wall" 长城"Skoda" 斯柯达"BaoJun" 宝骏"Subaru" 斯巴鲁"LandWind" 陆风"Luxgen" 纳智捷"Renault" 雷诺"Mitsubishi" 三菱"Roewe" 荣威"Cadillac" 凯迪拉克"MG" 名爵"Zotye" 众泰"ZhongHua" 中华"Foton" 福田"SongHuaJiang" 松花江"Opel" 欧宝"HongQi" 一汽红旗"Fiat" 菲亚特"Jaguar" 捷豹"Volvo" 沃尔沃"Acura" 讴歌"Porsche" 保时捷"Jeep" 吉普"Bentley" 宾利"Bugatti" 布加迪"ChuanQi" 传祺"Daewoo" 大宇"DongNan" 东南"Ferrari" 法拉利"Fudi" 福迪"Huapu" 华普"HawTai" 华泰"JMC" 江铃"JingLong" 金龙客车"JoyLong" 九龙"Karry" 开瑞"Chrysler" 克莱斯勒"Lamborghini" 兰博基尼"RollsRoyce" 劳斯莱斯"Linian" 理念"LiFan" 力帆"LieBao" 猎豹"Lincoln" 林肯"LandRover" 路虎"Lotus" 路特斯"Maserati" 玛莎拉蒂"Maybach" 迈巴赫"Mclaren" 迈凯轮"Youngman" 青年客车"Tesla" 特斯拉"Rely" 威麟"Lsuzu" 五十铃"Yiqi" 一汽"Infiniti" 英菲尼迪"YuTong" 宇通客车"AnKai" 安凯客车"Canghe" 昌河"HaiMa" 海马"Crown" 丰田皇冠"HuangHai" 黄海"JinLv" 金旅客车"JinNing" 精灵"KuBo" 酷博"Europestar" 莲花"MINI" 迷你"Gleagle" 全球鹰"ShiDai" 时代"ShuangHuan" 双环"TianYe" 田野"WeiZi" 威姿"Englon" 英伦"ZhongTong" 中通客车"Changan" 长安轿车"Yuejin" 跃进"Taurus" 金牛星"Alto" 奥拓"Weiwang" 威旺"Chenglong" 乘龙"Haige" 海格"Shaolin" 少林客车"Beifang" 北方客车"Beijing" 北京汽车"Hafu" 哈弗"BeijingTruck" 北汽货车"Besturn" 奔腾"ChanganBus" 长安客车"Dodge" 道奇"DongFangHong" 东方红"DongFengTruck" 东风货车"DongFengBus" 东风客车"MultiBrand" 多品牌"FotonTruck" 福田货车"FotonBus" 福田客车"GagcTruck" 广汽货车"HaFei" 哈飞"HowoBus" 豪沃客车"JACTruck" 江淮货车"JACBus" 江淮客车"JMCTruck" 江铃货车"JieFangTruck" 解放货车"JinBeiTruck" 金杯货车"KaiMaTruck" 凯马货车"CoasterBus" 柯斯达客车"MudanBus" 牡丹客车"NanJunTruck" 南骏货车"QingLing" 庆铃"NissanCivilian" 日产碧莲客车"NissanTruck" 日产货车"MitsubishiFuso" 三菱扶桑"SanyTruck" 三一货车"ShanQiTruck" 陕汽货车"ShenLongBus" 申龙客车"TangJunTruck" 唐骏货车"MicroTruck" 微货车"VolvoBus" 沃尔沃客车"LsuzuTruck" 五十铃货车"WuZhengTruck" 五征货车"Seat" 西雅特"YangZiBus" 扬子客车"YiqiBus" 一汽客车"YingTianTruck" 英田货车"YueJinTruck" 跃进货车"ZhongDaBus" 中大客车"ZxAuto""ZhongQiWangPai" 重汽王牌"WAW" 奥驰"BeiQiWeiWang" 北汽威旺"BYDDaimler" 比亚迪戴姆勒"ChunLan" 春兰"DaYun" 大运"DFFengDu" 东风风度"DFFengGuang" 东风风光"DFFengShen" 东风风神"DFFengXing" 东风风行"DFLiuQi" 东风柳汽"DFXiaoKang" 东风小康"FeiChi" 飞驰"FordMustang" 福特野马"GuangQi" 广汽"GuangTong" 广通"HuiZhongTruck" 汇众重卡"JiangHuai" 江环"SunWin" 申沃"ShiFeng" 时风"TongXin" 同心"WZL" 五洲龙"XiWo" 西沃"XuGong" 徐工"JingGong" 精工"SAAB" 萨博"SanHuanShiTong" 三环十通"KangDi" 康迪"YaoLong" 耀隆;
                              # the interrelated text of object,such as number plate,container number"ObjectType","Vehicle" or "Logo", try to use Logo.Vehicle is used to be compatible with old product, means logo, support:"Unknown" Unknown"Audi" Audi"Honda" Honda"Buick" Buick"Volkswagen" Volkswagen"Toyota" Toyota"BMW" BMW"Peugeot" Peugeot"Ford" Ford"Mazda" Mazda"Nissan" Nissan"Hyundai" Hyundai"Suzuki" Suzuki"Citroen" Citroen"Benz" Benz"BYD" BYD"Geely" Geely"Lexus" Lexus"Chevrolet" Chevrolet"Chery" Chery"Kia" Kia"Charade" Charade"DF" DF"Naveco" Naveco"SGMW" SGMW"Jinbei" Jinbei"JAC" JAC"Emgrand" Emgrand"ChangAn" ChangAn"Great Wall" Great Wall"Skoda" Skoda"BaoJun" BaoJun"Subaru" Subaru"LandWind" LandWind"Luxgen" Luxgen"Renault" Renault"Mitsubishi" Mitsubishi"Roewe" Roewe"Cadillac" Cadillac"MG" MG"Zotye" Zotye"ZhongHua" ZhongHua"Foton" Foton"SongHuaJiang" SongHuaJiang"Opel" Opel"HongQi" HongQi"Fiat" Fiat"Jaguar" Jaguar"Volvo" Volvo"Acura" Acura"Porsche" Porsche"Jeep" Jeep"Bentley" Bentley"Bugatti" Bugatti"ChuanQi" ChuanQi"Daewoo" Daewoo"DongNan" DongNan"Ferrari" Ferrari"Fudi" Fudi"Huapu" Huapu"HawTai" HawTai"JMC" JMC"JingLong" JingLong"JoyLong" JoyLong"Karry" Karry""Chrysler" Chrysler"Lamborghini" Lamborghini"RollsRoyce" RollsRoyce"Linian" Linian"LiFan" LiFan"LieBao" LieBao"Lincoln" Lincoln"LandRover" LandRover"Lotus" Lotus"Maserati" Maserati"Maybach" Maybach"Mclaren" Mclaren"Youngman" Youngman"Tesla" Tesla"Rely" Rely"Lsuzu" Lsuzu"Yiqi" Yiqi"Infiniti" Infiniti"YuTong" YuTong"AnKai" AnKai"Canghe" Canghe"HaiMa" HaiMa"Crown" Crown"HuangHai" HuangHai"JinLv" JinLv"JinNing" JinNing"KuBo" KuBo"Europestar" Europestar"MINI" MINI"Gleagle" Gleagle"ShiDai" ShiDai"ShuangHuan" ShuangHuan"TianYe" TianYe"WeiZi" WeiZi"Englon" Englon"ZhongTong" ZhongTong"Changan" Changan"Yuejin" Yuejin"Taurus" Taurus"Alto" Alto"Weiwang" Weiwang"Chenglong" Chenglong"Haige" Haige"Shaolin" Shaolin"Beifang" Beifang"Beijing" Beijing"Hafu" Hafu"BeijingTruck" BeiQi"Besturn" Besturn"ChanganBus" Changan"Dodge" Dodge"DongFangHong" Dongfanghong"DongFengTruck" DongFeng"DongFengBus" DongFeng"MultiBrand" MutiBrand"FotonTruck" Foton"FotonBus" Foton"GagcTruck" Gagc"HaFei" HaFei"HowoBus" Howo"JACTruck" JAC"JACBus" JAC"JMCTruck" JMC"JieFangTruck" JieFang"JinBeiTruck" JinBei"KaiMaTruck" KaiMa"CoasterBus" Coaster"MudanBus" Mudan"NanJunTruck" NanJun"QingLing" QingLing"NissanCivilian" Nissan Civilian"NissanTruck" Nissan"MitsubishiFuso" Mitsubishi Fuso"SanyTruck" Sany"ShanQiTruck" ShanQi"ShenLongBus" ShenLong"TangJunTruck" TangJun"MicroTruck" Micro"VolvoBus" Volvo"LsuzuTruck" Lsuzu"WuZhengTruck" WuZheng"Seat" Seat"YangZiBus" YangZi"YiqiBus" Yiqi"YingTianTruck" YingTian"YueJinTruck" YueJin"ZhongDaBus" ZhongDa"ZxAuto" ZxAuto"ZhongQiWangPai" ZhongQiWangPai"WAW" WAW"BeiQiWeiWang" BeiQiWeiWang"BYDDaimler" BYDDaimler"ChunLan" ChunLan"DaYun" DaYun"DFFengDu" DFFengDu"DFFengGuang" DFFengGuang"DFFengShen" DFFengShen"DFFengXing" DFFengXing"DFLiuQi" DFLiuQi"DFXiaoKang" DFXiaoKang"FeiChi" FeiChi"FordMustang" FordMustang"GuangQi" GuangQi"GuangTong" GuangTong"HuiZhongTruck" HuiZhongTruck"JiangHuai" JiangHuai"SunWin" SunWin"ShiFeng" ShiFeng"TongXin" TongXin"WZL" WZL"XiWo" XiWo"XuGong" XuGong"JingGong" JingGong"SAAB" SAAB"SanHuanShiTong" SanHuanShiTong"KangDi" KangDi"YaoLong" YaoLong;
        ('szObjectSubType', c_char * 62),  # 物体子类别,根据不同的物体类型,可以取以下子类型：Vehicle Category:"Unknown" 未知,"Motor" 机动车,"Non-Motor":非机动车,"Bus": 公交车,"Bicycle" 自行车,"Motorcycle":摩托车,"PassengerCar":客车,"LargeTruck":大货车, "MidTruck":中货车,"SaloonCar":轿车,"Microbus":面包车,"MicroTruck":小货车,"Tricycle":三轮车, "Passerby":行人"DregsCar":渣土车, "Excavator":挖掘车, "Bulldozer":推土车, "Crane":吊车, "PumpTruck":泵车, "MachineshopTruck":工程车, "Forklift"叉车, "Electricbike":二轮电瓶车Plate Category："Unknown" 未知,"Normal" 蓝牌黑牌,"Yellow" 黄牌,"DoubleYellow" 双层黄尾牌,"Police" 警牌,"SAR" 港澳特区号牌,"Trainning" 教练车号牌"Personal" 个性号牌,"Agri" 农用牌,"Embassy" 使馆号牌,"Moto" 摩托车号牌,"Tractor" 拖拉机号牌,"Other" 其他号牌"Civilaviation"民航号牌,"Black"黑牌"PureNewEnergyMicroCar"纯电动新能源小车,"MixedNewEnergyMicroCar,"混合新能源小车,"PureNewEnergyLargeCar",纯电动新能源大车"MixedNewEnergyLargeCar"混合新能源大车Human Category:"Normal" 普通目标,"HideEye" 眼部遮挡,"HideNose" 鼻子遮挡,"HideMouth" 嘴部遮挡,"TankCar"槽罐车(装化学药品、危险品)"ExtinguisherGeneral"普通类型灭火器，8kg左右,"ExtinguisherHandpush"35kg推车式灭火器, "SignboardGeneral" 普通标识牌"SignboardStaticEletricity "静电标示牌, "SignboardOilCap"加油口盖标示牌,"RoadCone"路锥,"CoverPlate"盖子;
                              # object sub type,different object type has different sub type:Vehicle Category:"Unknown","Motor","Non-Motor","Bus","Bicycle","Motorcycle","DregsCar", "Excavator", "Bulldozer", "Crane", "PumpTruck", "MachineshopTruck", "Forklift", "Electricbike"Plate Category:"Unknown","mal","Yellow","DoubleYellow","Police","SAR","Trainning""Personal" ,"Agri","Embassy","Moto","Tractor","Other"Human Category:"Normal","HideEye","HideNose","HideMouth","TankCar""ExtinguisherGeneral","ExtinguisherHandpush", "SignboardGeneral""SignboardStaticEletricity", "SignboardOilCap","RoadCone","CoverPlate";
        ('wColorLogoIndex', c_uint16),  # 车标索引;the index of car logo;
        ('wSubBrand', c_uint16),  # 车辆子品牌 需要通过映射表得到真正的子品牌 映射表详见开发手册;Specifies the sub-brand of vehicle,the real value can be found in a mapping table from the development manual;
        ('byReserved1', C_BYTE),  
        ('bPicEnble', c_bool),  # 是否有物体对应图片文件信息;picture info enable;
        ('stPicInfo', NET_A_PIC_INFO),  # 物体对应图片信息;picture info;
        ('bShotFrame', c_bool),  # 是否是抓拍张的识别结果;is shot frame;
        ('bColor', c_bool),  # 物体颜色(rgbaMainColor)是否可用;rgbaMainColor is enable;
        ('byReserved2', C_BYTE),  
        ('byTimeType', C_BYTE),  # 时间表示类型,详见EM_TIME_TYPE说明;Time indicates the type of detailed instructions, EM_TIME_TYPE;
        ('stuCurrentTime', NET_TIME_EX),  # 针对视频浓缩,当前时间戳（物体抓拍或识别时,会将此识别智能帧附在一个视频帧或jpeg图片中,此帧所在原始视频中的出现时间）;in view of the video compression,current time(when object snap or reconfnition, the frame will be attached to the frame in a video or pictures,means the frame in the original video of the time);
        ('stuStartTime', NET_TIME_EX),  # 开始时间戳（物体开始出现时）;strart time(object appearing for the first time);
        ('stuEndTime', NET_TIME_EX),  # 结束时间戳（物体最后出现时）;end time(object appearing for the last time);
        ('stuOriginalBoundingBox', NET_RECT_EX),  # 包围盒(绝对坐标);original bounding box(absolute coordinates);
        ('stuSignBoundingBox', NET_RECT_EX),  # 车标坐标包围盒;sign bounding box coordinate;
        ('dwCurrentSequence', C_DWORD),  # 当前帧序号（抓下这个物体时的帧）;The current frame number (frames when grabbing the object);
        ('dwBeginSequence', C_DWORD),  # 开始帧序号（物体开始出现时的帧序号）;Start frame number (object appeared When the frame number,;
        ('dwEndSequence', C_DWORD),  # 结束帧序号（物体消逝时的帧序号）;The end of the frame number (when the object disappearing Frame number);
        ('nBeginFileOffset', c_int64),  # 开始时文件偏移, 单位: 字节（物体开始出现时,视频帧在原始视频文件中相对于文件起始处的偏移）;At the beginning of the file offset, Unit: Word Section (when objects began to appear, the video frames in the original video file offset relative to the beginning of the file,;
        ('nEndFileOffset', c_int64),  # 结束时文件偏移, 单位: 字节（物体消逝时,视频帧在原始视频文件中相对于文件起始处的偏移）;At the end of the file offset, Unit: Word Section (when the object disappeared, video frames in the original video file offset relative to the beginning of the file);
        ('byColorSimilar', C_BYTE * 8),  # 物体颜色相似度,取值范围：0-100,数组下标值代表某种颜色,详见EM_COLOR_TYPE;Object color similarity, the range :0-100, represents an array subscript Colors, see EM_COLOR_TYPE,;
        ('byUpperBodyColorSimilar', C_BYTE * 8),  # 上半身物体颜色相似度(物体类型为人时有效);When upper body color similarity (valid object type man ,;
        ('byLowerBodyColorSimilar', C_BYTE * 8),  # 下半身物体颜色相似度(物体类型为人时有效);Lower body color similarity when objects (object type human valid ,;
        ('nRelativeID', c_int),  # 相关物体ID;ID of relative object;
        ('szSubText', c_char * 20),  # "ObjectType"为"Vehicle"或者"Logo"时,表示车标下的某一车系,比如奥迪A6L,由于车系较多,SDK实现时透传此字段,设备如实填写。;"ObjectType"is "Vehicle" or "Logo", means a certain brand under LOGO, such as Audi A6L, since there are so many brands, SDK sends this field in real-time ,device filled as real.;
        ('wBrandYear', c_uint16),  # 车辆品牌年款 需要通过映射表得到真正的年款 映射表详见开发手册;Specifies the model years of vehicle. the real value can be found in a mapping table from the development manual;
    ]

class SDK_MSG_OBJECT(Structure):
    """
    视频分析物体信息结构体;Struct of object info for video analysis
    """
    _pack_ = 4  # 补齐
    _fields_ = [
        ('nObjectID', c_int),           # 物体ID,每个ID表示一个唯一的物体;Object ID,each ID represent a unique object
        ('szObjectType', c_char*128),   # 物体类型;Object type
        ('nConfidence', c_int),         # 置信度(0~255),值越大表示置信度越高;Confidence(0~255),a high value indicate a high confidence
        ('nAction', c_int),             # 物体动作:1:Appear 2:Move 3:Stay 4:Remove 5:Disappear 6:Split 7:Merge 8:Rename;Object action:1:Appear 2:Move 3:Stay 4:Remove 5:Disappear 6:Split 7:Merge 8:Rename
        ('BoundingBox', SDK_RECT),      # 包围盒;BoundingBox
        ('Center', SDK_POINT),          # 物体型心;The shape center of the object
        ('nPolygonNum', c_int),         # 多边形顶点个数;the number of culminations for the polygon
        ('Contour', SDK_POINT * 16),    # 较精确的轮廓多边形;a polygon that have a exactitude figure
        ('rgbaMainColor', C_DWORD),     # 表示车牌、车身等物体主要颜色；按字节表示,分别为红、绿、蓝和透明度,例如:RGB值为(0,255,0),透明度为0时, 其值为0x00ff0000.
                                        # The main color of the object;the first byte indicate red value, as byte order as green, blue, transparence, for example:RGB(0,255,0),transparence = 0, rgbaMainColor = 0x00ff0000.
        ('szText', c_char * 128),       # 物体上相关的带0结束符文本,比如车牌,集装箱号等等;the interrelated text of object,such as number plate,container number
                                            # "ObjectType"为"Vehicle"或者"Logo"时（尽量使用Logo。Vehicle是为了兼容老产品）表示车标,支持："ObjectType","Vehicle" or "Logo", try to use Logo.Vehicle is used to be compatible with old product, means logo, support:
                                            # "Unknown"未知;Unknown
                                            # "Audi" 奥迪;Audi
                                            # "Honda" 本田;Honda
                                            # "Buick" 别克;Buick
                                            # "Volkswagen" 大众;Volkswagen
                                            # "Toyota" 丰田;Toyota
                                            # "BMW" 宝马;BMW
                                            # "Peugeot" 标致;Peugeot
                                            # "Ford" 福特;Ford
                                            # "Mazda" 马自达;Mazda
                                            # "Nissan" 尼桑(日产);Nissan
                                            # "Hyundai" 现代;Hyundai
                                            # "Suzuki" 铃木;Suzuki
                                            # "Citroen" 雪铁龙;Citroen
                                            # "Benz" 奔驰;Benz
                                            # "BYD" 比亚迪;BYD
                                            # "Geely" 吉利;Geely
                                            # "Lexus" 雷克萨斯;Lexus
                                            # "Chevrolet" 雪佛兰;Chevrolet
                                            # "Chery" 奇瑞;Chery
                                            # "Kia" 起亚;Kia
                                            # "Charade" 夏利;Charade
                                            # "DF" 东风;DF
                                            # "Naveco" 依维柯;Naveco
                                            # "SGMW" 五菱;SGMW
                                            # "Jinbei" 金杯;Jinbei
                                            # "JAC" 江淮;JAC
                                            # "Emgrand" 帝豪;Emgrand
                                            # "ChangAn" 长安;ChangAn
                                            # "Great Wall" 长城;Great Wall
                                            # "Skoda" 斯柯达;Skoda
                                            # "BaoJun" 宝骏;BaoJun
                                            # "Subaru" 斯巴鲁;Subaru
                                            # "LandWind" 陆风;LandWind
                                            # "Luxgen" 纳智捷;Luxgen
                                            # "Renault" 雷诺;Renault
                                            # "Mitsubishi" 三菱;Mitsubishi
                                            # "Roewe" 荣威;Roewe
                                            # "Cadillac" 凯迪拉克;Cadillac
                                            # "MG" 名爵;MG
                                            # "Zotye" 众泰;Zotye
                                            # "ZhongHua" 中华;ZhongHua
                                            # "Foton" 福田;Foton
                                            # "SongHuaJiang" 松花江;SongHuaJiang
                                            # "Opel" 欧宝;Opel
                                            # "HongQi" 一汽红旗;HongQi
                                            # "Fiat" 菲亚特;Fiat
                                            # "Jaguar" 捷豹;Jaguar
                                            # "Volvo" 沃尔沃;Volvo
                                            # "Acura" 讴歌;Acura
                                            # "Porsche" 保时捷;Porsche
                                            # "Jeep" 吉普;Jeep
                                            # "Bentley" 宾利;Bentley
                                            # "Bugatti" 布加迪;Bugatti
                                            # "ChuanQi" 传祺;ChuanQi
                                            # "Daewoo" 大宇;Daewoo
                                            # "DongNan" 东南;DongNan
                                            # "Ferrari" 法拉利;Ferrari
                                            # "Fudi" 福迪;Fudi
                                            # "Huapu" 华普;Huapu
                                            # "HawTai" 华泰;HawTai
                                            # "JMC" 江铃;JMC
                                            # "JingLong" 金龙客车;JingLong
                                            # "JoyLong" 九龙;JoyLong
                                            # "Karry" 开瑞;Karry
                                            # "Chrysler" 克莱斯勒;Chrysler
                                            # "Lamborghini" 兰博基尼;Lamborghini
                                            # "RollsRoyce" 劳斯莱斯;RollsRoyce
                                            # "Linian" 理念;Linian
                                            # "LiFan" 力帆;LiFan
                                            # "LieBao" 猎豹;LieBao
                                            # "Lincoln" 林肯;Lincoln
                                            # "LandRover" 路虎;LandRover
                                            # "Lotus" 路特斯;Lotus
                                            # "Maserati" 玛莎拉蒂;Maserati
                                            # "Maybach" 迈巴赫;Maybach
                                            # "Mclaren" 迈凯轮;Mclaren
                                            # "Youngman" 青年客车;Youngman
                                            # "Tesla" 特斯拉;Tesla
                                            # "Rely" 威麟;Rely
                                            # "Lsuzu" 五十铃;Lsuzu
                                            # "Yiqi" 一汽;Yiqi
                                            # "Infiniti" 英菲尼迪;Infiniti
                                            # "YuTong" 宇通客车;YuTong
                                            # "AnKai" 安凯客车;AnKai
                                            # "Canghe" 昌河;Canghe
                                            # "HaiMa" 海马;HaiMa
                                            # "Crown" 丰田皇冠;Crown
                                            # "HuangHai" 黄海;HuangHai
                                            # "JinLv" 金旅客车;JinLv
                                            # "JinNing" 精灵;JinNing
                                            # "KuBo" 酷博;KuBo
                                            # "Europestar" 莲花;Europestar
                                            # "MINI" 迷你;MINI
                                            # "Gleagle" 全球鹰;Gleagle
                                            # "ShiDai" 时代;ShiDai
                                            # "ShuangHuan" 双环;ShuangHuan
                                            # "TianYe" 田野;TianYe
                                            # "WeiZi" 威姿;WeiZi
                                            # "Englon" 英伦;Englon
                                            # "ZhongTong" 中通客车;ZhongTong
                                            # "Changan" 长安轿车;Changan
                                            # "Yuejin" 跃进;Yuejin
                                            # "Taurus" 金牛星;Taurus
                                            # "Alto" 奥拓;Alto
                                            # "Weiwang" 威旺;Weiwang
                                            # "Chenglong" 乘龙;Chenglong
                                            # "Haige" 海格;Haige
                                            # "Shaolin" 少林客车;Shaolin
                                            # "Beifang" 北方客车;Beifang
                                            # "Beijing" 北京汽车;Beijing
                                            # "Hafu" 哈弗;Hafu
                                            # "BeijingTruck" 北汽货车;BeijingTruck
                                            # "Besturn" 奔腾;Besturn
                                            # "ChanganBus" 长安客车;ChanganBus
                                            # "Dodge" 道奇;Dodge
                                            # "DongFangHong" 东方红;DongFangHong
                                            # "DongFengTruck" 东风货车;DongFengTruck
                                            # "DongFengBus" 东风客车;DongFengBus
                                            # "MultiBrand" 多品牌;MultiBrand
                                            # "FotonTruck" 福田货车;FotonTruck
                                            # "FotonBus" 福田客车;FotonBus
                                            # "GagcTruck" 广汽货车;GagcTruck
                                            # "HaFei" 哈飞;HaFei
                                            # "HowoBus" 豪沃客车;HowoBus
                                            # "JACTruck" 江淮货车;JACTruck
                                            # "JACBus" 江淮客车;JACBus
                                            # "JMCTruck" 江铃货车;JMCTruck
                                            # "JieFangTruck" 解放货车;JieFangTruck
                                            # "JinBeiTruck" 金杯货车;JinBeiTruck
                                            # "KaiMaTruck" 凯马货车;KaiMaTruck
                                            # "CoasterBus" 柯斯达客车;CoasterBus
                                            # "MudanBus" 牡丹客车;MudanBus
                                            # "NanJunTruck" 南骏货车;NanJunTruck
                                            # "QingLing" 庆铃;QingLing
                                            # "NissanCivilian" 日产碧莲客车;NissanCivilian
                                            # "NissanTruck" 日产货车;NissanTruck
                                            # "MitsubishiFuso" 三菱扶桑;MitsubishiFuso
                                            # "SanyTruck" 三一货车;SanyTruck
                                            # "ShanQiTruck" 陕汽货车;ShanQiTruck
                                            # "ShenLongBus" 申龙客车;ShenLongBus
                                            # "TangJunTruck" 唐骏货车;TangJunTruck
                                            # "MicroTruck" 微货车;MicroTruck
                                            # "VolvoBus" 沃尔沃客车;VolvoBus
                                            # "LsuzuTruck" 五十铃货车;LsuzuTruck
                                            # "WuZhengTruck" 五征货车;WuZhengTruck
                                            # "Seat" 西雅特;Seat
                                            # "YangZiBus" 扬子客车;YangZiBus
                                            # "YiqiBus" 一汽客车;YiqiBus
                                            # "YingTianTruck" 英田货车;YingTianTruck
                                            # "YueJinTruck" 跃进货车;YueJinTruck
                                            # "ZhongDaBus" 中大客车;ZhongDaBus
                                            # "ZhongQiWangPai" 重汽王牌;ZhongQiWangPai
                                            # "WAW" 奥驰;WAW
                                            # "BeiQiWeiWang" 北汽威旺;BeiQiWeiWang
                                            # "BYDDaimler"	比亚迪戴姆勒;BYDDaimler
                                            # "ChunLan" 春兰;ChunLan
                                            # "DaYun" 大运;DaYun
                                            # "DFFengDu" 东风风度;DFFengDu
                                            # "DFFengGuang" 东风风光;DFFengGuang
                                            # "DFFengShen" 东风风神;DFFengShen
                                            # "DFFengXing" 东风风行;DFFengXing
                                            # "DFLiuQi" 东风柳汽;DFLiuQi
                                            # "DFXiaoKang" 东风小康;DFXiaoKang
                                            # "FeiChi" 飞驰;FeiChi
                                            # "FordMustang" 福特野马;FordMustang
                                            # "GuangQi" 广汽;GuangQi
                                            # "GuangTong" 广通;GuangTong
                                            # "HuiZhongTruck" 汇众重卡;HuiZhongTruck
                                            # "JiangHuai" 江环;JiangHuai
                                            # "SunWin" 申沃;SunWin
                                            # "ShiFeng" 时风;ShiFeng
                                            # "TongXin" 同心;TongXin
                                            # "WZL" 五洲龙;WZL
                                            # "XiWo" 西沃;XiWo
                                            # "XuGong" 徐工;XuGong
                                            # "JingGong" 精工;JingGong
                                            # "SAAB" 萨博;SAAB
                                            # "SanHuanShiTong" 三环十通;SanHuanShiTong
                                            # "KangDi" 康迪;KangDi
                                            # "YaoLong" 耀隆;YaoLong
        ('szObjectSubType', c_char*62),     # 物体子类别,根据不同的物体类型,可以取以下子类型：
                                            # Vehicle Category:"Unknown"  未知,"Motor" 机动车,"Non-Motor":非机动车,"Bus": 公交车,"Bicycle" 自行车,"Motorcycle":摩托车,"PassengerCar":客车,
                                            # "LargeTruck":大货车,    "MidTruck":中货车,"SaloonCar":轿车,"Microbus":面包车,"MicroTruck":小货车,"Tricycle":三轮车,    "Passerby":行人
                                            # "DregsCar":渣土车, "Excavator":挖掘车, "Bulldozer":推土车, "Crane":吊车, "PumpTruck":泵车, "MachineshopTruck":工程车
                                            # Plate Category："Unknown" 未知,"Normal" 蓝牌黑牌,"Yellow" 黄牌,"DoubleYellow" 双层黄尾牌,"Police" 警牌,
                                            # "SAR" 港澳特区号牌,"Trainning" 教练车号牌
                                            # "Personal" 个性号牌,"Agri" 农用牌,"Embassy" 使馆号牌,"Moto" 摩托车号牌,"Tractor" 拖拉机号牌,"Other" 其他号牌
                                            # "Civilaviation"民航号牌,"Black"黑牌
                                            # "PureNewEnergyMicroCar"纯电动新能源小车,"MixedNewEnergyMicroCar,"混合新能源小车,"PureNewEnergyLargeCar",纯电动新能源大车
                                            # "MixedNewEnergyLargeCar"混合新能源大车
                                            # HumanFace Category:"Normal" 普通人脸,"HideEye" 眼部遮挡,"HideNose" 鼻子遮挡,"HideMouth" 嘴部遮挡,"TankCar"槽罐车(装化学药品、危险品)
                                            # object sub type,different object type has different sub type:
                                            # Vehicle Category:"Unknown","Motor","Non-Motor","Bus","Bicycle","Motorcycle",
                                            # "DregsCar", "Excavator", "Bulldozer", "Crane", "PumpTruck", "MachineshopTruck"
                                            # Plate Category:"Unknown","mal","Yellow","DoubleYellow","Police",
                                            # -
                                            # "Personal" ,"Agri","Embassy","Moto","Tractor","Other"
                                            # HumanFace Category:"Normal","HideEye","HideNose","HideMouth","TankCar"
        ('wColorLogoIndex', c_ushort),      # 车标索引;the index of car logo
        ('wSubBrand', c_ushort),            # 车辆子品牌 需要通过映射表得到真正的子品牌 映射表详见开发手册;Specifies the sub-brand of vehicle,the real value can be found in a mapping table from the development manual
        ('byReserved1', c_ubyte),           # 保留字段;Reserve
        ('bPicEnble', c_bool),              # 是否有物体对应图片文件信息; picture info enable
        ('stPicInfo', SDK_PIC_INFO),        # 物体对应图片信息;picture info
        ('bShotFrame', c_bool),             # 是否是抓拍张的识别结果;is shot frame
        ('bColor', c_bool),                 # 物体颜色(rgbaMainColor)是否可用; rgbaMainColor is enable
        ('byReserved2', c_ubyte),           # 保留字段;Reserve
        ('byTimeType', c_ubyte),            # 时间表示类型,详见EM_TIME_TYPE说明;Time indicates the type of detailed instructions, EM_TIME_TYPE
        ('stuCurrentTime', NET_TIME_EX),    # 针对视频浓缩,当前时间戳（物体抓拍或识别时,会将此识别智能帧附在一个视频帧或jpeg图片中,此帧所在原始视频中的出现时间）
                                            # in view of the video compression,current time(when object snap or reconfnition, the frame will be attached to the frame in a video or pictures,means the frame in the original video of the time)
        ('stuStartTime', NET_TIME_EX),      # 开始时间戳（物体开始出现时);strart time(object appearing for the first time)
        ('stuEndTime', NET_TIME_EX),        # 结束时间戳（物体最后出现时）;end time(object appearing for the last time)
        ('stuOriginalBoundingBox', SDK_RECT),  # 包围盒(绝对坐标);original bounding box(absolute coordinates)
        ('stuSignBoundingBox', SDK_RECT),   # 车标坐标包围盒;sign bounding box coordinate
        ('dwCurrentSequence', C_DWORD),     # 当前帧序号（抓下这个物体时的帧）; The current frame number (frames when grabbing the object)
        ('dwBeginSequence', C_DWORD),       # 开始帧序号（物体开始出现时的帧序号）;Start frame number (object appeared When the frame number,
        ('dwEndSequence', C_DWORD),         # 结束帧序号（物体消逝时的帧序号）;The end of the frame number (when the object disappearing Frame number)
        ('nBeginFileOffset', c_int64),      # 开始时文件偏移, 单位: 字节（物体开始出现时,视频帧在原始视频文件中相对于文件起始处的偏移）;At the beginning of the file offset, Unit: Word Section (when objects began to appear, the video frames in the original video file offset relative to the beginning of the file,
        ('nEndFileOffset', c_int64),        # 结束时文件偏移, 单位: 字节（物体消逝时,视频帧在原始视频文件中相对于文件起始处的偏移）;At the end of the file offset, Unit: Word Section (when the object disappeared, video frames in the original video file offset relative to the beginning of the file)
        ('byColorSimilar', c_ubyte*8),      # 物体颜色相似度,取值范围：0-100,数组下标值代表某种颜色,详见EM_COLOR_TYPE;Object color similarity, the range :0-100, represents an array subscript Colors, see EM_COLOR_TYPE,
        ('byUpperBodyColorSimilar', c_ubyte*8), # 上半身物体颜色相似度(物体类型为人时有效);When upper body color similarity (valid object type man ,
        ('byLowerBodyColorSimilar', c_ubyte*8), # 下半身物体颜色相似度(物体类型为人时有效);Lower body color similarity when objects (object type human valid ,
        ('nRelativeID', c_int),             # 相关物体ID;ID of relative object
        ('szSubText', c_char*20),           # "ObjectType"为"Vehicle"或者"Logo"时,表示车标下的某一车系,比如奥迪A6L,由于车系较多,SDK实现时透传此字段,设备如实填写。
                                            # "ObjectType"is "Vehicle" or "Logo",  means a certain brand under LOGO, such as Audi A6L, since there are so many brands, SDK sends this field in real-time ,device filled as real.
        ('wBrandYear', c_ushort)            # 车辆品牌年款 需要通过映射表得到真正的年款 映射表详见开发手册;Specifies the model years of vehicle. the real value can be found in a mapping table from the development manual
    ]

class SDK_EVENT_FILE_INFO(Structure):
    """
    事件对应文件信息;event file info
    """
    _fields_ = [
        ('bCount', c_ubyte),                # 当前文件所在文件组中的文件总数;the file count in the current file's group
        ('bIndex', c_ubyte),                # 当前文件在文件组中的文件编号(编号1开始);the index of the file in the group
        ('bFileTag', c_ubyte),              # 文件标签, EM_EVENT_FILETAG;file tag, see the enum struct EM_EVENT_FILETAG
        ('bFileType', c_ubyte),             # 文件类型,0-普通 1-合成 2-抠图;file type,0-normal 1-compose 2-cut picture
        ('stuFileTime', NET_TIME_EX),       # 文件时间;file time
        ('nGroupId', C_DWORD)               # 同一组抓拍文件的唯一标识;the only id of one group file
    ]

class SDK_RESOLUTION_INFO(Structure):
    """
    图片分辨率;pic resolution
    """
    _fields_ = [
        ('snWidth', c_ushort),      # 宽;width
        ('snHight', c_ushort)       # 高;hight
    ]

class EVENT_CUSTOM_WEIGHT_INFO(Structure):
    """
    称重信息; weight info
    """
    _fields_ = [
        ('dwRoughWeight', C_DWORD),     # 毛重,车辆满载货物重量。单位KG;Rough Weight,unit:KG
        ('dwTareWeight', C_DWORD),      # 皮重,空车重量。单位KG;Tare Weight,unit:KG
        ('dwNetWeight', C_DWORD),       # 净重,载货重量。单位KG;Net Weight,unit:KG
        ('bReserved', c_ubyte*28)       # 预留字节;Rough Weight,unit:KG
    ]

class NET_RADAR_FREE_STREAM(Structure):
    """
    雷达自由流信息;Radar free stream information
    """
    _fields_ = [
        ('nABSTime', C_TP_U64),             # 1年1月1日0时起至今的毫秒数;millisecond from 0001-01-01 00:00:00
        ('nVehicleID', c_int),              # 车辆ID;Vehicle ID
        ('unOBUMAC', c_uint),               # OBU的MAC地址;MAC of on board unit
    ]

class NET_CUSTOM_MEASURE_TEMPER(Structure):
    """
    测温信息
    Measure temper
    """
    _fields_ = [
        ('fLeft', c_float),  # 车辆左侧温度值;The temperature of the left side of the vehicle;
        ('fRight', c_float),  # 车辆右侧温度值;The temperature of the right side of the vehicle;
        ('fHead', c_float),  # 车辆发动机位置温度值 (车头);Vehicle engine position temperature value;
        ('emUnit', C_ENUM),  # 温度单位 Refer: EM_TEMPERATURE_UNIT;Temperature unit Refer: EM_TEMPERATURE_UNIT;
    ]

class EVENT_JUNCTION_CUSTOM_INFO(Structure):
    """
    卡口事件专用上报内容;
    """
    _fields_ = [
        ('stuWeightInfo', EVENT_CUSTOM_WEIGHT_INFO),  # 原始图片信息; weight info;
        ('nCbirFeatureOffset', C_DWORD),    # 数据偏移，单位字节 （由于结构体保留字节有限的限制,添加在此处， 下同）;Content Based Image Retrieval Feature offset,Unit:Byte;
        ('nCbirFeatureLength', C_DWORD),    # 数据大小，单位字节;Content Based Image Retrieval Feature length,Unit:Byte;
        ('dwVehicleHeadDirection', C_DWORD),  # 车头朝向 0:未知 1:左 2:中 3:右;Head direction 0:Unknown 1:left 2:center 3:right;
        ('nAvailableSpaceNum', C_UINT), # 停车场车位余位数量 (出入口相机）;Number of available parking space(entrance and exit camera);
        ('stuRadarFreeStream', NET_RADAR_FREE_STREAM),  # 雷达自由流信息;Radar free stream info;
        ('stuMeasureTemper', NET_CUSTOM_MEASURE_TEMPER),  # 测温信息;Measure temperature.;
        ('bReserved', C_BYTE * 12),  # 预留字节;Reserved;
    ]

class NET_GPS_INFO(Structure):
    """
    GPS信息;GPS Infomation
    """
    _pack_ = 4                              # 补齐
    _fields_ = [
        ('nLongitude', c_uint),             # 经度(单位是百万分之一度);Longitude(unit:1/1000000 degree)
                                            # 西经：0 - 180000000	实际值应为: 180*1000000 – dwLongitude;west Longitude: 0 - 180000000 practical value = 180*1000000 - dwLongitude
                                            # 东经：180000000 - 360000000	实际值应为: dwLongitude – 180*1000000;east Longitude: 180000000 - 360000000    practical value = dwLongitude - 180*1000000
                                            # 如: 300168866应为（300168866 - 180 * 1000000）/ 1000000 即东经120.168866度;eg: Longitude:300168866  (300168866 - 180*1000000)/1000000  equal east Longitude 120.168866 degree
        ('nLatidude', c_uint),              # 纬度(单位是百万分之一度);Latidude(unit:1/1000000 degree)
                                            # 南纬：0 - 90000000 实际值应为: 90*1000000 – dwLatidude;north Latidude: 0 - 90000000				practical value = 90*1000000 - dwLatidude
                                            # 北纬：90000000 – 180000000	实际值应为: dwLatidude – 90*1000000;south Latidude: 90000000 - 180000000	practical value = dwLatidude - 90*1000000
                                            # 如: 120186268应为 (120186268 - 90*1000000)/1000000 即北纬30. 186268度;eg: Latidude:120186268 (120186268 - 90*1000000)/1000000 equal south Latidude 30. 186268 degree
        ('dbAltitude', c_double),           # 高度,单位为米;altitude,unit:m
        ('dbSpeed', c_double),              # 速度,单位km/H;Speed,unit:km/H
        ('dbBearing', c_double),            # 方向角,单位°;Bearing,unit:°
        ('bReserved', c_ubyte*8)            # 保留字段;Reserved bytes
    ]

class NET_COLOR_RGBA(Structure):
    """
    颜色RGBA;color RGBA
    """
    _fields_ = [
        ('nRed', c_int),            # 红;red
        ('nGreen', c_int),          # 绿;green
        ('nBlue', c_int),           # 蓝;blue
        ('nAlpha', c_int)           # 透明;transparent
    ]

class NET_EXTENSION_INFO(Structure):
    """
    事件扩展信息;Extension info
    """
    _fields_ = [
        ('szEventID', c_char*52),       # 国标事件ID;Chinese standard event ID
        ('byReserved', c_ubyte*80)      # 保留字节;Reserved
    ]

class DRIVING_DIRECTION(Structure):
    """
    行驶方向;Driving direction
    """
    _fields_ = [
        ('DrivingDirection', c_char*256)    # 行驶方向;Driving direction
    ]

class SDK_SIG_CARWAY_INFO_EX(Structure):
    """
    车检器冗余信息;Vehicle detector redundancy info
    """
    _fields_ = [
        ('byRedundance', c_ubyte*8),        # 由车检器产生抓拍信号冗余信息;The vehicle detector generates the snap signal redundancy info
        ('bReserved', c_ubyte * 120)        # 保留字段;Reserved
    ]


class NET_WHITE_LIST_AUTHORITY_LIST(Structure):
    """
    允许名单权限列表;authority list of Allow list
    """
    _fields_ = [
        ('bOpenGate', c_int),      # 是否有开闸权限;true:having open gate authority,false:no having open gate authority
        ('bReserved', c_ubyte*16)  # 保留字节;reserved
    ]


class NET_TRAFFICCAR_WHITE_LIST(Structure):
    """
    允许名单信息;Allow list information
    """
    _fields_ = [
        ('bTrustCar', c_int),         # 车牌是否属于允许名单;true: the car is trust car,false:the car is not trust car
        ('stuBeginTime', NET_TIME),   # 允许名单起始时间;begin time of Allow list
        ('stuCancelTime', NET_TIME),  # 允许名单过期时间;cancel time of Allow list
        ('stuAuthorityList', NET_WHITE_LIST_AUTHORITY_LIST),  # 允许名单权限列表;authority list of Allow list
        ('bReserved', c_ubyte*32)     # 保留字节;Reserved
    ]

class NET_TRAFFICCAR_BLACK_LIST(Structure):
    """
    禁止名单信息;Blocklist information
    """
    _fields_ = [
        ('bEnable', c_int),          # 禁止名单信息;Enable blocklist
        ('bIsBlackCar', c_int),      # 车牌是否属于禁止名单;Whether is the plate on the blocklist or not
        ('stuBeginTime', NET_TIME),  # 禁止名单起始时间;Begin time
        ('stuCancelTime', NET_TIME), # 禁止名单过期时间;Cancel time
        ('emControlType', C_ENUM),   # 布控类型 Refer: EM_NET_TRAFFIC_CAR_CONTROL_TYPE;Control type Refer: EM_NET_TRAFFIC_CAR_CONTROL_TYPE;
        ('bReserved', c_ubyte * 28)  # 保留字节;Reserved
    ]

class NET_RECT(Structure):
    """
    事件上报携带卡片信息;Incidents reported to carry the card information
    """
    _fields_ = [
        ('nLeft', c_int),       # 左;Left
        ('nTop', c_int),        # 顶;Top
        ('nRight', c_int),      # 右;Right
        ('nBottom', c_int)      # 底;Bottom
    ]

class NET_TRAFFICCAR_ORIGINAL_VEHICLE(Structure):
    """
    车身抠图
    Body matting
    """
    _fields_ = [
        ('nOffset', C_UINT),  # 在二进制数据块中的偏移;Offset in binary data block;
        ('nLength', C_UINT),  # 数据大小,单位：字节;Data size in bytes;
        ('nIndexInData', C_UINT),  # 在上传图片数据中的图片序号;Picture serial number in uploaded picture data;
        ('szReserved', c_char * 60),  # 保留字节;Reserved;
    ]

class DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO(Structure):
    """
    交通车辆信息;TrafficCar information
    """
    _fields_ = [
        ('szPlateNumber', c_char * 32),     # 车牌号码;plate number
        ('szPlateType', c_char * 32),       # 号牌类型 "Unknown" 未知; "Normal" 蓝牌黑牌; "Yellow" 黄牌; "DoubleYellow" 双层黄尾牌;Plate type: "Unknown" =Unknown; "Normal"=Blue and black plate. "Yellow"=Yellow plate. "DoubleYellow"=Double-layer yellow plate
                                            # "Police" 警牌; "Police"=Police plate ;
                                            # "SAR" 港澳特区号牌; "Trainning" 教练车号牌; "Personal" 个性号牌; "Agri" 农用牌;"SAR" =HongK SAR or Macao SAR plate; "Trainning" =rehearsal plate; "Personal"=Personal plate; "Agri"=Agricultural plate
                                            # "Embassy" 使馆号牌; "Moto" 摩托车号牌; "Tractor" 拖拉机号牌; "Other" 其他号牌; "Embassy"=Embassy plate; "Moto"=Moto plate ; "Tractor"=Tractor plate; "Other"=Other plate
        ('szPlateColor', c_char * 32),      # 车牌颜色    "Blue","Yellow", "White","Black","YellowbottomBlackText","BluebottomWhiteText","BlackBottomWhiteText","ShadowGreen","YellowGreen"
                                            # plate color, "Blue","Yellow", "White","Black","YellowbottomBlackText","BluebottomWhiteText","BlackBottomWhiteText","ShadowGreen","YellowGreen"
        ('szVehicleColor', c_char * 32),    # 车身颜色    "White", "Black", "Red", "Yellow", "Gray", "Blue","Green";vehicle color, "White", "Black", "Red", "Yellow", "Gray", "Blue","Green"
        ('nSpeed', c_int),                  # 速度,单位Km/H;speed, Km/H
        ('szEvent', c_char*64),             # 触发的相关事件,参见事件列表Event List,只包含交通相关事件;trigger event type
        ('szViolationCode', c_char * 32),   # 违章代码;violation code
        ('szViolationDesc', c_char * 64),   # 违章描述;violation describe
        ('nLowerSpeedLimit', c_int),        # 速度下限;lower speed limit
        ('nUpperSpeedLimit', c_int),        # 速度上限;upper speed limit
        ('nOverSpeedMargin', c_int),        # 限高速宽限值,单位：km/h;over speed margin, km/h
        ('nUnderSpeedMargin', c_int),       # 限低速宽限值,单位：km/h;under speed margin, km/h
        ('nLane', c_int),                   # 车道,参见事件列表Event List中卡口和路口事件;lane
        ('nVehicleSize', c_int),            # 车辆大小,-1表示未知,否则按位;vehicle size, see VideoAnalyseRule's describe
                                             # 第0位:"Light-duty", 小型车;Bit 0:"Light-duty", small car
                                             # 第1位:"Medium", 中型车;Bit 1:"Medium", medium car
                                             # 第2位:"Oversize", 大型车;Bit 2:"Oversize", large car
                                             # 第3位:"Minisize", 微型车;Bit 3:"Minisize", mini car
                                             # 第4位:"Largesize", 长车;Bit 4:"Largesize", long car
        ('fVehicleLength', c_float),        # 车辆长度,单位米;vehicle length, Unit:m
        ('nSnapshotMode', c_int),           # 抓拍方式,0-未分类,1-全景,2-近景,4-同向抓拍,8-反向抓拍,16-号牌图像;snap mode 0-normal,1-globle,2-near,4-snap on the same side,8-snap on the reverse side,16-plant picture
        ('szChannelName', c_char*32),       # 本地或远程的通道名称,可以是地点信息,来源于通道标题配置ChannelTitle.Name;channel name
        ('szMachineName', c_char*256),      # 本地或远程设备名称,来源于普通配置General.MachineName;Machine name
        ('szMachineGroup', c_char * 256),   # 机器分组或叫设备所属单位,默认为空,用户可以将不同的设备编为一组,便于管理,可重复;machine group
        ('szRoadwayNo', c_char*64),         # 道路编号;road way number
        ('szDrivingDirection', DRIVING_DIRECTION * 3),      # 行驶方向 , "DrivingDirection" : ["Approach", "上海", "杭州"];DrivingDirection: for example ["Approach", "Shanghai", "Hangzhou"]
                                                            # "Approach"-上行,即车辆离设备部署点越来越近；"Leave"-下行;"Approach" means driving direction,where the car is more near;"Leave"-means where if mor far to the car
                                                            # 即车辆离设备部署点越来越远,第二和第三个参数分别代表上行和下行的两个地点;the second and third param means the location of the driving direction
        ('szDeviceAddress', c_char_p),      # 设备地址,OSD叠加到图片上的,来源于配置TrafficSnapshot.DeviceAddress,'\0'结束;device address,OSD superimposed onto the image,from TrafficSnapshot.DeviceAddress,'\0'means end.
        ('szVehicleSign', c_char*32),       # 车辆标识, 例如 "Unknown"-未知, "Audi"-奥迪, "Honda"-本田 ...;Vehicle identification, such as "Unknown" - unknown "Audi" - Audi, "Honda" - Honda ...
        ('stuSigInfo', SDK_SIG_CARWAY_INFO_EX),             # 由车检器产生抓拍信号冗余信息;Generated by the vehicle inspection device to capture the signal redundancy
        ('szMachineAddr', c_char_p),        # 设备部署地点;Equipment deployment locations
        ('fActualShutter', c_float),        # 当前图片曝光时间,单位为毫秒;Current picture exposure time, in milliseconds
        ('byActualGain', c_ubyte),          # 当前图片增益,范围为0~100;Current picture gain, ranging from 0 to 100
        ('byDirection', c_ubyte),           # 车道方向,0-南向北 1-西南向东北 2-西向东 3-西北向东南 4-北向南 5-东北向西南 6-东向西 7-东南向西北 8-未知 9-自定义;
                                            # Lane Direction,0 - south to north 1- Southwest to northeast 2 - West to east, 3 - Northwest to southeast 4 - north to south 5 - northeast to southwest 6 - East to West 7 - Southeast to northwest 8 - Unknown 9-customized
        ('byReserved', c_ubyte*2),          # 预留字节;Reserved
        ('szDetailedAddress', c_char_p),    # 详细地址, 作为szDeviceAddress的补充;Address, as szDeviceAddress supplement
        ('szDefendCode', c_char*64),        # 图片防伪码;waterproof
        ('nTrafficBlackListID', c_int),     # 关联阻止名单数据库记录默认主键ID, 0,无效；> 0,禁止名单数据记录;Link Block list data recorddefualt main keyID, 0, invalid, > 0, block list data record
        ('stuRGBA', NET_COLOR_RGBA),        # 车身颜色RGBA;bofy color RGBA
        ('stSnapTime', NET_TIME),           # 抓拍时间;snap time
        ('nRecNo', c_int),                  # 记录编号;Rec No
        ('szCustomParkNo', c_char*33),      # 自定义车位号（停车场用）;self defined parking space number, for parking
        ('byReserved1', c_ubyte * 3),       # 预留字节;Reserved
        ('nDeckNo', c_int),                 # 车板位号;Metal plate No.
        ('nFreeDeckCount', c_int),          # 空闲车板数量;Free metal plate No.
        ('nFullDeckCount', c_int),          # 占用车板数量;Occupized metal plate No.
        ('nTotalDeckCount', c_int),         # 总共车板数量;Total metal plate No.
        ('szViolationName', c_char * 64),   # 违章名称;violation name
        ('nWeight', c_uint),                # 车重(单位 Kg);Weight of car(kg)
        ('szCustomRoadwayDirection', c_char * 32),  # 自定义车道方向,byDirection为9时有效; road way, valid when byDirection is 9
        ('byPhysicalLane', c_ubyte),        # 物理车道号,取值0到5;the physical lane number,value form 0 to 5
        ('byReserved2', c_ubyte * 3),       # 预留字节;Reserved
        ('emMovingDirection', c_int),       # 车辆行驶方向,值的意义见EM_TRAFFICCAR_MOVE_DIRECTION;moving direction
        ('stuEleTagInfoUTC', NET_TIME),     # 对应电子车牌标签信息中的过车时间(ThroughTime);corresponding to throughTime
        ('stuCarWindowBoundingBox', NET_RECT),          # 车窗包围盒，0~8191;The BoundingBox of car window , 0~8191
        ('stuWhiteList', NET_TRAFFICCAR_WHITE_LIST),    # 允许名单信息;Allow list information
        ('emCarType', c_int),               # 车辆类型,详见EM_TRAFFICCAR_CAR_TYPE;car type,refer to EM_TRAFFICCAR_CAR_TYPE
        ('emLaneType', c_int),              # 车道类型,详见EM_TRAFFICCAR_LANE_TYPE;Lane type,refer to EM_TRAFFICCAR_LANE_TYPE
        ('szVehicleBrandYearText', c_char * 64),        # 车系年款翻译后文本内容;Translated year of vehicle
        ('szCategory', c_char * 32),        # 车辆子类型;category
        ('stuBlackList',NET_TRAFFICCAR_BLACK_LIST),     # 阻止名单信息;Blocklist information
        ('emFlowDirection', C_ENUM),    # 车流量方向 Refer: EM_VEHICLE_DIRECTION;Traffic flow direction Refer: EM_VEHICLE_DIRECTION;
        ('emTollsVehicleType', C_ENUM), # 收费公路车辆通行费车型分类 Refer: EM_TOLLS_VEHICLE_TYPE;Classification of toll road vehicle types Refer: EM_TOLLS_VEHICLE_TYPE;
        ('nAxleType', C_UINT),  # 轴型代码,参考轴型国标 0代表其他;Shaft type code, refer to the national standard of shaft type, and 0 represents others;
        ('nAxleCount', C_UINT),  # 车轴数量;Number of axles;
        ('nWheelNum', C_UINT),  # 车轮数量;Number of wheels;
        ('stuOriginalVehicle', NET_TRAFFICCAR_ORIGINAL_VEHICLE),  # 车身抠图;Body matting;
        ('emVehicleTypeByFunc', C_ENUM),    # 按功能划分的车辆类型 Refer: EM_VEHICLE_TYPE_BY_FUNC;Vehicle type by function Refer: EM_VEHICLE_TYPE_BY_FUNC;
        ('nSunBrand', c_uint16),            # 车辆子品牌;Sun Brand;
        ('nBrandYear', c_uint16),           # 车辆年款;Brand Year;
        ('nTrafficLightType', c_int),       # 交通灯类型,仅在EVENT_IVS_TRAFFIC_RUNREDLIGHT中有效, 0;未知, 1:箭头灯, 2:圆形灯;Traffic light type, valid only in EVENT_IVS_TRAFFIC_RUNREDLIGHT, 0; Unknown, 1: Head lamp, 2: Round lamp;
        ('emPlateAttribute', C_ENUM),       # 车牌属性 Refer: EM_PLATE_ATTRIBUTE;Plate Attribute Refer: EM_PLATE_ATTRIBUTE;
        ('bReserved', C_BYTE * 132),        # 保留字节,留待扩展.;Reserved bytes.;
    ]

class EVENT_CARD_INFO(Structure):
    """
    事件上报携带卡片信息;Incidents reported to carry the card information
    """
    _fields_ = [
        ('szCardNumber', c_char*36),       # 卡片序号字符串;Card number string
        ('bReserved', c_ubyte*32)          # 保留字节,留待扩展;Reserved bytes, leave extended
    ]

class SDK_MSG_OBJECT_EX(Structure):
    """
    视频分析物体信息扩展结构体;Video analysis object info expansion structure
    """
    _pack_ = 4  # 补齐
    _fields_ = [
        ('dwSize', C_DWORD),            # 结构体大小;Structure size
        ('nObjectID', c_int),           # 物体ID,每个ID表示一个唯一的物体;object ID, each ID means a exclusive object;
        ('szObjectType', c_char * 128), # 物体类型;object type;
        ('nConfidence', c_int),         # 置信度(0~255),值越大表示置信度越高;confidence coefficient (0~255), value the bigger means confidence coefficient the higher;
        ('nAction', c_int),             # 物体动作:1:Appear 2:Move 3:Stay 4:Remove 5:Disappear 6:Split 7:Merge 8:Rename;object motion :1:Appear 2:Move 3:Stay 4:Remove 5:Disappear 6:Split 7:Merge 8:Rename;
        ('BoundingBox', SDK_RECT),      # 包围盒;box;
        ('Center', SDK_POINT),          # 物体型心;object model center;
        ('nPolygonNum', c_int),         # 多边形顶点个数;polygon vertex number;
        ('Contour', SDK_POINT * 16),    # 较精确的轮廓多边形;relatively accurate outline the polygon;
        ('rgbaMainColor', C_DWORD),     # 表示车牌、车身等物体主要颜色；按字节表示,分别为红、绿、蓝和透明度,例如:RGB值为(0,255,0),透明度为0时, 其值为0x00ff0000.;means plate, vehicle body and etc. object major color, by byte means , are red, green, blue and transparency , such as:RGB value is (0,255,0), transparency is 0, its value is 0x00ff0000.;
        ('szText', c_char * 128),       # 同MSG_OBJECT相应字段;same as MSG_OBJECT corresponding field;
        ('szObjectSubType', c_char * 64),   # 物体子类别,根据不同的物体类型,可以取以下子类型：同MSG_OBJECT相应字段;object sub type , according to different object types , may use the following sub type :same as MSG_OBJECT field;
        ('byReserved1', C_BYTE * 3),    # 保留字节;Reserved
        ('bPicEnble', c_bool),          # 是否有物体对应图片文件信息;object corresponding to picture file info or not;
        ('stPicInfo', SDK_PIC_INFO),    # 物体对应图片信息;object corresponding to picture info;
        ('bShotFrame', c_bool),         # 是否是抓拍张的识别结果;snapshot recognition result or not;
        ('bColor', c_bool),             # 物体颜色(rgbaMainColor)是否可用;object color (rgbaMainColor) usable or not;
        ('bLowerBodyColor', C_BYTE),    # 下半身颜色(rgbaLowerBodyColor)是否可用;lower color (rgbaLowerBodyColor) usable or not;
        ('byTimeType', C_BYTE),         # 时间表示类型,详见EM_TIME_TYPE说明;time means type , see EM_TIME_TYPE note;
        ('stuCurrentTime', NET_TIME_EX),            # 针对视频浓缩,当前时间戳（物体抓拍或识别时,会将此识别智能帧附在一个视频帧或jpeg图片中,此帧所在原始视频中的出现时间）;for video compression, current time stamp, object snapshot or recognition, attach this recognition frame in one vire frame or jpegpicture, this frame appearance time in original video,;
        ('stuStartTime', NET_TIME_EX),              # 开始时间戳（物体开始出现时）;start time stamp, object start appearance,;
        ('stuEndTime', NET_TIME_EX),                # 结束时间戳（物体最后出现时）;end time stamp, object last aapearance,;
        ('stuOriginalBoundingBox', SDK_RECT),       # 包围盒(绝对坐标);box(absolute coordinate);
        ('stuSignBoundingBox', SDK_RECT),           # 车标坐标包围盒;LGO coordinate box;
        ('dwCurrentSequence', C_DWORD),             # 当前帧序号（抓下这个物体时的帧）;current frame no., snapshot this object frame,;
        ('dwBeginSequence', C_DWORD),               # 开始帧序号（物体开始出现时的帧序号）;start frame no., object start appearance frame no.,;
        ('dwEndSequence', C_DWORD),                 # 结束帧序号（物体消逝时的帧序号）;end frame no., object disappearance frame no.,;
        ('nBeginFileOffset', c_int64),              # 开始时文件偏移, 单位: 字节（物体开始出现时,视频帧在原始视频文件中相对于文件起始处的偏移）;start file shift, unit: byte, object start appearance, video in original video file moves toward file origin,;
        ('nEndFileOffset', c_int64),                # 结束时文件偏移, 单位: 字节（物体消逝时,视频帧在原始视频文件中相对于文件起始处的偏移）;End file shift, unit: byte, object disappearance, video in original video file moves toward file origin,;
        ('byColorSimilar', C_BYTE * 8),             # 物体颜色相似度,取值范围：0-100,数组下标值代表某种颜色,详见EM_COLOR_TYPE;object color similarity, take value range :0-100, group subscript value represents certain color , see EM_COLOR_TYPE;
        ('byUpperBodyColorSimilar', C_BYTE * 8),    # 上半身物体颜色相似度(物体类型为人时有效);upper object color similarity (object type as human is valid );
        ('byLowerBodyColorSimilar', C_BYTE * 8),    # 下半身物体颜色相似度(物体类型为人时有效);lower object color similarity (object type as human is valid );
        ('nRelativeID', c_int),                     # 相关物体ID;related object ID;
        ('szSubText', c_char * 20),                 # "ObjectType"为"Vehicle"或者"Logo"时,表示车标下的某一车系,比如奥迪A6L,由于车系较多,SDK实现时透传此字段,设备如实填写。;"ObjectType"is "Vehicle"or "Logo", means LOGO lower brand, such as Audi A6L, since there are many brands, SDK shows this field in real-time,device filled as real.;
        ('nPersonStature', c_int),                  # 入侵人员身高,单位cm;Intrusion staff height, unit cm;
        ('emPersonDirection', C_ENUM),              # 人员入侵方向 Refer: EM_MSG_OBJ_PERSON_DIRECTION;Staff intrusion direction Refer: EM_MSG_OBJ_PERSON_DIRECTION;
        ('rgbaLowerBodyColor', C_DWORD),            # 使用方法同rgbaMainColor,物体类型为人时有效;Use direction same as rgbaMainColor,object type as human is valid;
    ]

class NET_A_MSG_OBJECT_EX2(Structure):
    """
    视频分析物体信息扩展结构体,扩展版本2
    Video analysis object info extension structure, extension version 2.
    """
    _pack_ = 4
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nObjectID', c_int),  # 物体ID,每个ID表示一个唯一的物体;Object ID. Each ID presents one object.;
        ('szObjectType', c_char * 128),  # 物体类型;Object type;
        ('nConfidence', c_int),  # 置信度(0~255),值越大表示置信度越高;Confiidence(0-255). The higher the value is, the higher the confidence is.;
        ('nAction', c_int),  # 物体动作:1:Appear 2:Move 3:Stay 4:Remove 5:Disappear 6:Split 7:Merge 8:Rename;Object operation. 1:Appear 2:Move 3:Stay 4:Remove 5:Disappear 6:Split 7:Merge 8:Rename;
        ('BoundingBox', SDK_RECT),  # 包围盒;Surrounding rectangle;
        ('Center', SDK_POINT),  # 物体型心;Object size centre;
        ('nPolygonNum', c_int),  # 多边形顶点个数;Top amount of the polygon;
        ('Contour', SDK_POINT * 16),  # 较精确的轮廓多边形;Polygon of generaly accurate frame;
        ('rgbaMainColor', C_DWORD),  # 表示车牌、车身等物体主要颜色；按字节表示,分别为红、绿、蓝和透明度,例如:RGB值为(0,255,0),透明度为0时, 其值为0x00ff0000.;The plate and the vehicle body main color. Use byte to present: red, green, blue and transparent. When RGB value is (0,255,0), transparent is 0, the value is 0x00ff0000.;
        ('szText', c_char * 128),  # 同MSG_OBJECT相应字段;The same as the string of the MSG_OBJECT;
        ('szObjectSubType', c_char * 64),  # 物体子类别,根据不同的物体类型,可以取以下子类型：同MSG_OBJECT相应字段;Object sub-type. It has the following sub-tyes.The same as the string of the MSG_OBJECT;
        ('byReserved1', C_BYTE * 3),
        ('bPicEnble', c_bool),  # 是否有物体对应图片文件信息;There is image file info of the corresponding object;
        ('stPicInfo', SDK_PIC_INFO),  # 物体对应图片信息;Image info of the object;
        ('bShotFrame', c_bool),  # 是否是抓拍张的识别结果;Has been snapped or not;
        ('bColor', c_bool),  # 物体颜色(rgbaMainColor)是否可用;Object color (rgbaMainColor) is usable or not.;
        ('bLowerBodyColor', C_BYTE),  # 下半身颜色(rgbaLowerBodyColor)是否可用;The lower part color (rgbaLowerBodyColor) is usable or not;
        ('byTimeType', C_BYTE),  # 时间表示类型,详见EM_TIME_TYPE说明;Time type. Please refer to EM_TIME_TYPE.;
        ('stuCurrentTime', NET_TIME_EX),  # 针对视频浓缩,当前时间戳（物体抓拍或识别时,会将此识别智能帧附在一个视频帧或jpeg图片中,此帧所在原始视频中的出现时间）;For video synopsis. Current time stampl (When snap or recognize the object, use the recognition intelligent frame on one video frame or JPEG. It is the appearing time of the frame on the original video. );
        ('stuStartTime', NET_TIME_EX),  # 开始时间戳（物体开始出现时）;Start time stamp(When the object first appear );
        ('stuEndTime', NET_TIME_EX),  # 结束时间戳（物体最后出现时）;End time (When the object last appear );
        ('stuOriginalBoundingBox', SDK_RECT),  # 包围盒(绝对坐标);Surrounding box(Absolute coordinates);
        ('stuSignBoundingBox', SDK_RECT),  # 车标坐标包围盒;Vehicle symbol surrounding box;
        ('dwCurrentSequence', C_DWORD),  # 当前帧序号（抓下这个物体时的帧）;Current frame SN(Frame when snap the object );
        ('dwBeginSequence', C_DWORD),  # 开始帧序号（物体开始出现时的帧序号）;Start frame SN (The frame SN when the object start appearing);
        ('dwEndSequence', C_DWORD),  # 结束帧序号（物体消逝时的帧序号）;End frame SN (The frame SN when the object disappering);
        ('nBeginFileOffset', c_int64),  # 开始时文件偏移, 单位: 字节（物体开始出现时,视频帧在原始视频文件中相对于文件起始处的偏移）;The file offset when start. Unit:byte. (When the object appearing, the video frame offset value comparing with the file start positon in the original video);
        ('nEndFileOffset', c_int64),  # 结束时文件偏移, 单位: 字节（物体消逝时,视频帧在原始视频文件中相对于文件起始处的偏移）;The file offset when stop. Unit: byte. (When the object disappearing, the video frame offset value comparing with the file start position in the original video);
        ('byColorSimilar', C_BYTE * 8),  # 物体颜色相似度,取值范围：0-100,数组下标值代表某种颜色,详见EM_COLOR_TYPE;Object color similarity level. The valur ranges from 0 to 100. The underline value of the array represents one color. Plase refer to EM_COLOR_TYPE.;
        ('byUpperBodyColorSimilar', C_BYTE * 8),  # 上半身物体颜色相似度(物体类型为人时有效);The top body color similarity leve; (When the object is the human);
        ('byLowerBodyColorSimilar', C_BYTE * 8),  # 下半身物体颜色相似度(物体类型为人时有效);The lower body color similarity leve; (When the object is the human);
        ('nRelativeID', c_int),  # 相关物体ID;Related object ID;
        ('szSubText', c_char * 20),  # "ObjectType"为"Vehicle"或者"Logo"时,表示车标下的某一车系,比如奥迪A6L,由于车系较多,SDK实现时透传此字段,设备如实填写。;When "ObjectType" is "Vehicle" or "Logo", it represents one car series under the card symbol such as Audio A6L. Since there are too many card series, SDK use the network to realize COM transmission (szSubText) to realize this function.;
        ('nPersonStature', c_int),  # 入侵人员身高,单位cm;Intrusion person height. Unit is cm.;
        ('emPersonDirection', C_ENUM),  # 人员入侵方向 Refer: EM_MSG_OBJ_PERSON_DIRECTION;Intrusion person direction Refer: EM_MSG_OBJ_PERSON_DIRECTION;
        ('rgbaLowerBodyColor', C_DWORD),  # 使用方法同rgbaMainColor,物体类型为人时有效;The same usage as the rgbaMainColor, it is valid when the object type is human.;
        ('nSynopsisSpeed', c_int),  # 浓缩速度域值,共分1~10共十个档位,5表示浓缩后只保留5以上速度的物体。是个相对单位为0时,该字段无效;Synopsis speed threshold. There are ten levels (1 to 10). 5 means only reserve the object of speed higher than 5. It is a relative unit.When it is 0, the string is invalid.;
        ('nSynopsisSize', c_int),  # 浓缩尺寸域值,共分1~10共十个档位,3表示浓缩后只保留3以上大小的物体。是个相对单位为0时,该字段无效;Synopsis dimension threshold. There are ten levels (1 to 10). 3 means only reserve the object of speed higher than 3. It is a relative unit.When it is o, the string is invalid.;
        ('bEnableDirection', C_BOOL),  # 为True时,对物体运动方向做过滤为False时,不对物体运动方向做过滤,;When it is True, filter the object moving direction.When it is False, do not filter the object moving direction.;
        ('stuSynopsisStartLocation', SDK_POINT),  # 浓缩运动方向,起始坐标点,点的坐标归一化到[0,8191]区间,bEnableDirection为True时有效;Synopsis moving direction, start coordinates. The point coordinates [0,8191], it is valid when bEnableDirection is True.;
        ('stuSynopsisEndLocation', SDK_POINT),  # 浓缩运动方向,终止坐标点,点的坐标归一化到[0,8191]区间,bEnableDirection为True时有效;Synopsis moving direction, stop coordinates. The point coordinates [0,8191], it is valid when bEnableDirection is True.;
        ('szSerialUUID', c_char * 22),  # 智能物体全局唯一物体标识有效数据位21位，包含’\0’前2位%d%d:01-视频片段, 02-图片, 03-文件, 99-其他中间14位YYYYMMDDhhmmss:年月日时分秒后5位%u%u%u%u%u：物体ID，如00001;Intelligent object global unique object identificationValid data bits are 21 bits, including '\0'Top 2 bits %d%d: 01-video clip, 02-picture, 03-file, 99-otherMiddle 14 bit yyyymmddhhmmssLast 5 bits %U%U%U%U%U: object ID, such as 00001;
        ('szReserved', c_char * 2),  # 对齐;For align;
        ('byReserved', C_BYTE * 2024),  # 扩展字节;Extension byte;
    ]

class SDK_EXTRA_PLATE_NUMBER(Structure):
    """
    额外车牌信息;Extra plate number
    """
    _fields_ = [
        ('szNumber', c_char*32)  # 额外车牌信息;Extra plate number
    ]

class EVENT_COMM_STATUS(Structure):
    """
    违规状态;illegal state type of driver
    """
    _fields_ = [
        ('bySmoking', c_ubyte),     # 是否抽烟;smoking
        ('byCalling', c_ubyte),     # 是否打电话;calling
        ('szReserved', c_char*14),  # 预留字段;reversed
    ]

class NET_A_EVENT_COMM_STATUS(Structure):
    """
    违规状态
    illegal state type of driver
    """
    _fields_ = [
        ('bySmoking', C_BYTE),  # 是否抽烟, 0:未知, 1:抽烟, 2:未抽烟;smoking, 0:unknown, 1:Smoking, 2:NotSmoking;
        ('byCalling', C_BYTE),  # 是否打电话, 0:未知, 1:打电话, 2:未打电话;calling, 0:unknown, 1:calling, 2:NotCalling;
        ('szReserved', c_char * 14),  # 预留字段;reversed;
    ]

class EVENT_COMM_SEAT(Structure):
    """
    驾驶位违规信息;driver's illegal info
    """
    _fields_ = [
        ('bEnable', c_int),               # 是否检测到座驾信息;whether seat info detected
        ('emSeatType', c_int),            # 座驾类型, 0:未识别; 1:主驾驶; 2:副驾驶,详见EM_COMMON_SEAT_TYPE;seat type,refer to EM_COMMON_SEAT_TYPE
        ('stStatus', EVENT_COMM_STATUS),  # 违规状态;illegal state
        ('emSafeBeltStatus', c_int),      # 安全带状态,详见NET_SAFEBELT_STATE;safe belt state,refer to NET_SAFEBELT_STATE
        ('emSunShadeStatus', c_int),      # 遮阳板状态,详见NET_SUNSHADE_STATE;sun shade state,refer to NET_SUNSHADE_STATE
        ('emCallAction', C_ENUM),         # 打电话动作 Refer: EM_CALL_ACTION_TYPE;Call action Refer: EM_CALL_ACTION_TYPE;
        ('nSafeBeltConf', C_UINT),        # 安全带确信度;Safety belt confidence;
        ('nPhoneConf', C_UINT),           # 打电话置信度;Call confidence;
        ('nSmokeConf', C_UINT),           # 抽烟置信度;Smoking confidence;
        ('szReserved', c_ubyte * 8),      # 预留字节; reversed
    ]

class EVENT_COMM_ATTACHMENT(Structure):
    """
    车辆物件;car attachment
    """
    _fields_ = [
        ('emAttachmentType', c_int),    # 物件类型,详见EVENT_COMM_ATTACHMENT;type，refer to EVENT_COMM_ATTACHMENT
        ('stuRect', NET_RECT),          # 坐标;coordinate
        ('nConf', C_UINT),              # 置信度;Confidence;
        ('bReserved', c_ubyte * 16),      # 预留字节;reserved
    ]

class EVENT_PIC_INFO(Structure):
    """
    交通抓图图片信息;traffic event snap picture info
    """
    _fields_ = [
        ('nOffset', C_DWORD),  # 原始图片偏移，单位字节;offset,Unit:byte
        ('nLength', C_DWORD),  # 原始图片长度，单位字节;length of picture,Unit:byte
        ('nIndexInData', C_UINT),  # 在上传图片数据中的图片序号;The serial number of the picture in the uploaded picture data;
    ]

class NET_RFIDELETAG_INFO(Structure):
    """
    RFID 电子车牌标签信息;the info of RFID electronic tag
    """
    _fields_ = [
        ('szCardID', c_ubyte*16),       # 卡号;card ID
        ('nCardType', c_int),           # 卡号类型, 0:交通管理机关发行卡, 1:新车出厂预装卡;card type, 0:issued by transport administration offices, 1:new factory preloaded card
        ('emCardPrivince', c_int),      # 卡号省份,详见EM_CARD_PROVINCE;card privince,refer to EM_CARD_PROVINCE
        ('szPlateNumber', c_char*32),   # 车牌号码;plate number
        ('szProductionDate', c_char * 16),  # 出厂日期;production data
        ('emCarType', c_int),           # 车辆类型,详见EM_CAR_TYPE;car type,refer to EM_CAR_TYPE
        ('nPower', c_int),              # 功率,单位：千瓦时，功率值范围0~254；255表示该车功率大于可存储的最大功率值
                                        # power, unit:kilowatt-hour, range:0~254, 255 means larger than maximum power value can be stored
        ('nDisplacement', c_int),       # 排量,单位：百毫升，排量值范围0~254；255表示该车排量大于可存储的最大排量值
                                        # displacement, unit:100ml, range:0~254, 255 means larger than maximum displacement value can be stored
        ('nAntennaID', c_int),          # 天线ID，取值范围:1~4;antenna ID, range:1~4
        ('emPlateType', c_int),         # 号牌种类,详见EM_PLATE_TYPE;plate type,refer to EM_PLATE_TYPE
        ('szInspectionValidity', c_char*16),    # 检验有效期，年-月;validity of inspection, year-month
        ('nInspectionFlag', c_int),     # 逾期未年检标志, 0:已年检, 1:逾期未年检;the flag of inspetion, 0:already inspection, 1:not inspection
        ('nMandatoryRetirement', c_int), # 强制报废期，从检验有效期开始，距离强制报废期的年数;the years form effective inspection preiod to compulsory discarding preiod
        ('emCarColor', c_int),           # 车身颜色，详见EM_CAR_COLOR_TYPE;car color,refer to EM_CAR_COLOR_TYPE
        ('nApprovedCapacity', c_int),    # 核定载客量，该值<0时：无效；此值表示核定载客，单位为人;authorized capacity, unit:people, <0:incalid
        ('nApprovedTotalQuality', c_int), # 此值表示总质量，单位为百千克；该值<0时：无效；该值的有效范围为0~0x3FF，0x3FF（1023）表示数据值超过了可存储的最大值;total weight, unit:100kg, range:0~0x3FF,  0x3FF1023:larger than maximum value can be stored, <0:invalid
        ('stuThroughTime', NET_TIME_EX),  # 过车时间;the time when the car is pass
        ('emUseProperty', c_int),         # 使用性质,详见EM_USE_PROPERTY_TYPE;use property,refer to EM_USE_PROPERTY_TYPE
        ('szPlateCode', c_char*8),        # 发牌代号，UTF-8编码;Licensing code, UTF-8 encoding
        ('szPlateSN', c_char * 16),       # 号牌号码序号，UTF-8编码;Plate number, serial number, UTF-8 code
        ('szTID', c_char * 64),           # 标签(唯一标识), UTF-8编码;Label (Unique identifier), UTF-8 encoding
        ('bReserved', c_ubyte * 40),      # 保留字节,留待扩展;Reserved
    ]

class NET_EVENT_RADAR_INFO(Structure):
    """
    物体在雷达坐标系中的信息
    Radar Info
    """
    _fields_ = [
        ('fCoordinateX', c_float),  # X轴坐标(横向距离)，单位：米;X, unit: metre;
        ('fCoordinateY', c_float),  # Y轴坐标（纵向距离），单位：米;Y, unit: metre;
        ('fAccelerationX', c_float),# 雷达目标横向加速度ax, 横向指设备视角的右手方向; 数据为正表示车辆加速, 数据为负表示车辆减速; 单位为m/s2;Radar target transverse acceleration ax, The unit is m/s2;
        ('fAccelerationY', c_float),# 雷达目标纵向加速度ay，纵向指设备视角的正前方向；数据为正表示车辆加速，数据为负表示车辆减速；单位为m/s2;Radar target longitudinal acceleration ay, The unit is m/s2;
        ('bReserved', C_BYTE * 16), # 预留字节;reserved;
    ]

class NET_EVENT_GPS_INFO(Structure):
    """
    触发事件时物体的GPS信息
    Event Gps Info
    """
    _fields_ = [
        ('dLongitude', c_double),  # 经度，单位：度,正为东经，负为西经，取值范围[-180,180];longitude,[-180, 180],unit:degree,negative:west longitude;
        ('dLatitude', c_double),  # 纬度，单位：度,正为北纬，负为南纬，取值范围[-90,90];latitude,[-90, 90],unit:degree,negative:south latitude;
        ('bReserved', C_BYTE * 24),  # 预留字节;reserved;
    ]

class NET_EXTRA_PLATES(Structure):
    """
    辅车牌信息
    Auxiliary license plate information
    """
    _fields_ = [
        ('nOffset', C_UINT),  # 车牌图片在二进制数据内偏移，单位字节;The license plate picture is offset in binary data, in bytes;
        ('nLength', C_UINT),  # 车牌图片长度，单位字节;License plate picture length, in bytes;
        ('szText', c_char * 64),  # 辅车牌号码，UTF8格式;Auxiliary license plate number,UTF8;
        ('emCategory', C_ENUM),  # 车牌类型 Refer: EM_NET_PLATE_TYPE;License plate type Refer: EM_NET_PLATE_TYPE;
        ('emColor', C_ENUM),  # 车牌颜色 Refer: EM_NET_PLATE_COLOR_TYPE;License plate color Refer: EM_NET_PLATE_COLOR_TYPE;
        ('stuArea', NET_RECT),  # 辅车牌的包围盒，坐标已算上黑边高度车牌矩形框，绝对坐标，即真正的像素点坐标;The coordinates of the bounding box of the auxiliary license plate have been calculated into the height of the black edge, the rectangular box of the license plate, and the absolute coordinates, that is, the real pixel coordinates;
        ('bReserved', c_char * 32),  # 预留字节;reserved;
    ]

class EVENT_COMM_INFO(Structure):
    """
    事件上报携带卡片信息;Incidents reported to carry the card information
    """
    _fields_ = [
        ('emNTPStatus', c_int),      # NTP校时状态,详见EM_NTP_STATUS;NTP time sync status,refer to EM_NTP_STATUS
        ('nDriversNum', c_int),      # 驾驶员信息数;driver info number
        ('pstDriversInfo', POINTER(SDK_MSG_OBJECT_EX)),  # 保驾驶员信息数据;driver info data
        ('pszFilePath', c_char_p),   # 本地硬盘或者sd卡成功写入路径,为None时,路径不存在;writing path for local disk or sd card, or write to default path if None
        ('pszFTPPath', c_char_p),    # 设备成功写到ftp服务器的路径;ftp path
        ('pszVideoPath', c_char_p),  # 当前接入需要获取当前违章的关联视频的FTP上传路径;ftp path for assocated video
        ('stCommSeat', EVENT_COMM_SEAT*8),  # 驾驶位信息;Seat info
        ('nAttachmentNum', c_int),   # 车辆物件个数;Car Attachment number
        ('stuAttachment', EVENT_COMM_ATTACHMENT*8),   # 车辆物件信息;Car Attachment
        ('nAnnualInspectionNum', c_int),        # 年检标志个数;Annual Inspection number
        ('stuAnnualInspection', NET_RECT*8),    # 年检标志;Annual Inspection
        ('fHCRatio', c_float),       # HC所占比例，单位：%/1000000;The ratio of HC,unit,%/1000000
        ('fNORatio', c_float),       # NO所占比例，单位：%/1000000;The ratio of NO,unit,%/1000000
        ('fCOPercent', c_float),     # CO所占百分比，单位：% 取值0~100;The percent of CO,unit,% ,range from 0 to 100
        ('fCO2Percent', c_float),    # CO2所占百分比，单位：% 取值0~100;The percent of CO2,unit: % ,range from 0 to 100
        ('fLightObscuration', c_float), # 不透光度，单位：% 取值0~100;The obscuration of light,unit,% ,range from 0 to 100
        ('nPictureNum', c_int),      # 原始图片张数;Original pictures info number
        ('stuPicInfos', EVENT_PIC_INFO*6),  # 原始图片信息;Original pictures info data
        ('fTemperature', c_float),   # 温度值,单位摄氏度;Temperature,unit: centigrade
        ('nHumidity', c_int),        # 相对湿度百分比值;Humidity,unit: %
        ('fPressure', c_float),      # 气压值,单位Kpa;Pressure,unit: Kpa
        ('fWindForce', c_float),     # 风力值,单位m/s;Wind force,unit: m/s
        ('nWindDirection', c_uint),  # 风向,单位度,范围:[0,360];Wind direction,unit: degree,range:[0,360]
        ('fRoadGradient', c_float),  # 道路坡度值,单位度;Road gradient,unit: degree
        ('fAcceleration', c_float),  # 加速度值,单位:m/s2;Acceleration,unit: m/s2
        ('stuRFIDEleTagInfo', NET_RFIDELETAG_INFO),   # RFID 电子车牌标签信息;RFID electronics tag info
        ('stuBinarizedPlateInfo', EVENT_PIC_INFO),    # 二值化车牌抠图;Binarized plate matting
        ('stuVehicleBodyInfo', EVENT_PIC_INFO),       # 车身特写抠图;Vehicle body close-up matting
        ('emVehicleTypeInTollStation', c_int),        # 收费站车型分类,详见EM_VEHICLE_TYPE;Vehicle type inToll station,refer to EM_VEHICLE_TYPE
        ('emSnapCategory', c_int),                    # 抓拍的类型，默认为机动车，详见EM_SNAPCATEGORY;Snap Category;,refer to EM_SNAPCATEGORY
        ('nRegionCode', c_int),                       # 车牌所属地区代码,(海外车牌识别),默认-1表示未识别;Location code of license plate,default -1 indicates unrecognized
        ('emVehicleTypeByFunc', c_int),               # 按功能划分的车辆类型，详见EM_VEHICLE_TYPE_BY_FUNC;Vehicle type by function,refer to EM_VEHICLE_TYPE_BY_FUNC
        ('emStandardVehicleType', c_int),             # 标准车辆类型，详见EM_STANDARD_VEHICLE_TYPE;Standard vehicle type,refer to EM_STANDARD_VEHICLE_TYPE
        ('nExtraPlateCount', c_uint),                 # 额外车牌数量;Count of extra plates
        ('szExtraPlateNumber', SDK_EXTRA_PLATE_NUMBER * 3),  # 额外车牌信息;Extra plate number
        ('emOverseaVehicleCategory', c_int),                # 海外车辆类型中的子类别，详见EM_OVERSEA_VEHICLE_CATEGORY_TYPE;oversea vehicle category,refer to EM_OVERSEA_VEHICLE_CATEGORY_TYPE
        ('szProvince', c_char*64),                          # 车牌所属国家的省、州等地区名;Province
        ('stuRadarInfo', NET_EVENT_RADAR_INFO),             # 物体在雷达坐标系中的信息,单位：米，设备视角：右手方向为X轴正向，正前方为Y轴正向;Radar Info;
        ('stuGPSInfo', NET_EVENT_GPS_INFO),                 # 触发事件时物体的GPS信息;gps info;
        ('stuExtraPlates', NET_EXTRA_PLATES * 2),           # 辅车牌信息，某些国家或地区一车多牌; Auxiliary license plate information;
        ('nExtraPlatesCount', c_int),                       # 辅车牌有效个数;Auxiliary license plate number;
        ('nPlateRecogniseConf', C_UINT),                    # 车牌识别置信度;License plate recognition confidence;
        ('nVecPostureConf', C_UINT),                        # 车辆姿态置信度;Vehicle attitude confidence;
        ('nVecColorConf', C_UINT),                          # 车身颜色置信度;Vehicle Body color confidence;
        ('nSpecialVehConf', C_UINT),                        # 特殊车辆识别结果置信度;special vehicle recognition results confidence;
        ('nIsLargeAngle', C_UINT),                          # 机动车是否为大角度;Is the motor vehicle at a large angle;
        ('nIsRelatedPlate', C_UINT),                        # 当前机动车车身是否曾经关联车牌;Has the current vehicle body ever been associated with a license plate;
        ('nDetectConf', C_UINT),                            # 机动车检测置信度;Vehicle detection confidence;
        ('nClarity', C_UINT),                               # 机动车清晰度分值;Motor vehicle definition score;
        ('nCompleteScore', C_UINT),                         # 机动车完整度评分;Motor vehicle integrity score;
        ('nQeScore', C_UINT),                               # 机动车优选分数;Motor vehicle preference score;
        ('fSpeedFloat', c_float),                           # 浮点型速度值，单位km/h;Floating point speed value in km/h;
        ('dbHeadingAngle', c_double),                       # 航向角, 以正北方向为基准输出车辆运动方向同正北方向的角度; 范围 0~360，顺时针正,单位为度
        ('nDriverNum', C_UINT),                             # 车辆前排驾驶室人员数量
        ('bReserved', C_BYTE * 112),                        # 预留字节;reserved;
        ('szCountry', c_char*20)                            # 国家;Country
    ]

class NET_NONMOTOR_PIC_INFO(Structure):
    """
    非机动车抠图信息;Non-Motor Image
    """
    _fields_ = [
        ('uOffset', c_uint),            # 在二进制数据块中的偏移;Offset
        ('uLength', c_uint),            # 图片大小,单位：字节;Image size, Unit : Byte
        ('uWidth', c_uint),             # 图片宽度;Image Width
        ('uHeight', c_uint),            # 图片高度;Image Height
        ('szFilePath', c_char*260),     # 文件路径;FilePath
        ('nIndexInData', C_UINT),       # 在上传图片数据中的图片序号;Index in data;
        ('byReserved', c_ubyte*508),    # 保留字节;Reserved
    ]

class RIDER_FACE_IMAGE_INFO(Structure):
    """
    骑车人脸图片信息;face image information
    """
    _fields_ =[
        ('nOffSet', c_uint),    # 在二进制数据块中的偏移;image offset in the data
        ('nLength', c_uint),    # 图片大小,单位字节;Image size, Unit : Byte
        ('nWidth', c_uint),     # 图片宽度(像素);Image width(pixel)
        ('nHeight', c_uint),    # 图片高度(像素);Image height(pixel)
        ('nIndexInData', C_UINT),       # 图片的序号;index in data;
        ('byReserved', C_BYTE * 44),    # 保留;Reserved;
    ]

class NET_INTELLIGENCE_IMAGE_INFO(Structure):
    """
    智能事件抓图信息
    intelli image information
    """
    _fields_ = [
        ('nOffSet', C_UINT),  # 在二进制数据块中的偏移;The offset of image data in binary data;
        ('nLength', C_UINT),  # 图片大小,单位字节;The image data length, Unit:Byte;
        ('nWidth', C_UINT),  # 图片宽度(像素);Image width(pixel);
        ('nHeight', C_UINT),  # 图片高度(像素);Image height(pixel);
        ('nIndexInData', C_UINT),  # 在上传图片数据中的图片序号;The serial number of the picture in the uploaded picture data;
        ('byReserved', C_BYTE * 44),  # 预留字节;Reserved;
    ]


class NET_FACE_ATTRIBUTE_EX(Structure):
    """
    人脸属性;Face attribute
    """
    _fields_ =[
        ('emSex', c_uint),                  # 性别，详见EM_SEX_TYPE;Sex，refer to EM_SEX_TYPE
        ('nAge', c_int),                    # 年龄,-1表示该字段数据无效;age,-1 means invalid
        ('szReserved', c_char * 4),         # Reserved
        ('emEye', c_int),                   # 眼睛状态,详见EM_EYE_STATE_TYPE;Eye state,refer to EM_EYE_STATE_TYPE
        ('emMouth', c_int),                 # 嘴巴状态,详见EM_MOUTH_STATE_TYPE;Mouth state,refer to EM_MOUTH_STATE_TYPE
        ('emMask', c_int),                  # 口罩状态,详见EM_MASK_STATE_TYPE;Mask state,refer to EM_MASK_STATE_TYPE
        ('emBeard', c_int),                 # 胡子状态,详见EM_BEARD_STATE_TYPE;Beard state,refer to EM_BEARD_STATE_TYPE
        ('nAttractive', c_int),             # 魅力值, 0未识别，识别时范围1-100,得分高魅力高;Attractive, 0 Not distinguish,Range[1,100]
        ('emGlass', c_int),                 # 眼镜,详见EM_HAS_GLASS;Glasses,refer to EM_HAS_GLASS
        ('emEmotion', c_int),               # 表情,详见EM_EMOTION_TYPE;Emotion,refer to EM_EMOTION_TYPE
        ('stuBoundingBox', SDK_RECT),       # 包围盒(8192坐标系);BoundingBox(8192 Coordinate)
        ('bReserved1', C_BYTE*4),           # 保留字节;Reserved;
        ('emStrabismus', c_int),            # 斜视状态,详见EM_STRABISMUS_TYPE;Strabismus,refer to EM_STRABISMUS_TYPE
        ('nAngle', c_int * 3),              # 人脸抓拍角度, 三个角度依次分别是Pitch（仰俯角）, 指抬头低头的角度, 范围是-70~60;yaw（偏航角）, 指左右转头的角度, 范围是-90~90;Roll（翻滚角）, 指左右倾斜的角度, 范围是-90~90;[180,180,180]表示未识别到角度;Face capture angle, three angles are respectivelyPitch(pitch angle), refers to the angle of head up and head down, with the range of - 70 ~ 60;Yaw(yaw angle), refers to the angle of left and right turning head, and the range is - 90 ~ 90;Roll (roll angle), refers to the angle of left and right tilt, the range is - 90 ~ 90;[180180180] indicates the angle is not recognized;
        ('stuObjCenter', SDK_POINT),        # 物体型心(不是包围盒中心), 0-8191相对坐标, 相对于大图;Center of object(not center of bounding box), 0-8191 relative coordinates, relative to large graph;
        ('byReserved', c_ubyte*48),         # 保留字节,留待扩展;Reserved
    ]

class NET_FACE_FEATURE_VECTOR_INFO(Structure):
    """
    人脸特征值数据在二进制数据中的位置信息
    Location information of face characteristic value data in binary data
    """
    _fields_ = [
        ('nOffset', C_UINT),  # 人脸特征值在二进制数据中的偏移, 单位:字节;Offset of face characteristic value data in binary data, unit: byte;
        ('nLength', C_UINT),  # 人脸特征值数据长度, 单位:字节;Length of face characteristic value data, unit: byte;
        ('bFeatureEnc', C_BOOL),  # 用于标识特征值是否加密;Identifies whether the characteristic value data is encrypted;
        ('byReserved', C_BYTE * 28),  # 保留字节;reserved;
    ]

class NET_HUMAN_FEATURE_VECTOR_INFO(Structure):
    """
    人体特征值数据在二进制数据中的位置信息
    Position info of human feature data in binary data
    """
    _fields_ = [
        ('nOffset', C_UINT),  # 人体特征值在二进制数据中的偏移, 单位:字节;The offset of human feature data in binary data, unit:bytes;
        ('nLength', C_UINT),  # 人体特征值数据长度, 单位:字节;The length of human feature data, unit:bytes;
        ('bFeatureEnc', C_BOOL),  # 用于标识特征值是否加密;Identifies whether the characteristic value data is encrypted;
        ('byReserved', C_BYTE * 28),  # 保留字节;Reserved;
    ]

class NET_RIDER_INFO(Structure):
    """
    骑车人信息;Rider information
    """
    _fields_ = [
        ('bFeatureValid', c_int),       # 是否识别到特征信息, TRUE时下面数据才有效;Enable
        ('emSex', c_int),               # 性别,详见EM_SEX_TYPE;its sex,refer to EM_SEX_TYPE
        ('nAge', c_int),                # 年龄;its age
        ('emHelmet', c_int),            # 头盔状态,详见EM_NONMOTOR_OBJECT_STATUS;Whether or not wearing a helmet,refer to EM_NONMOTOR_OBJECT_STATUS
        ('emCall', c_int),              # 是否在打电话,详见EM_NONMOTOR_OBJECT_STATUS;Whether on the phone,refer to EM_NONMOTOR_OBJECT_STATUS
        ('emBag', c_int),               # 是否有背包,详见EM_NONMOTOR_OBJECT_STATUS; Whether or not have bag,refer to EM_NONMOTOR_OBJECT_STATUS
        ('emCarrierBag', c_int),        # 有没有手提包,详见EM_NONMOTOR_OBJECT_STATUS;Whether or not have carrierbag,refer to EM_NONMOTOR_OBJECT_STATUS
        ('emUmbrella', c_int),          # 是否打伞,详见EM_NONMOTOR_OBJECT_STATUS;Whether an umbrella,refer to EM_NONMOTOR_OBJECT_STATUS
        ('emGlasses', c_int),           # 是否有带眼镜,详见EM_NONMOTOR_OBJECT_STATUS; Whether or not wear glasses,refer to EM_NONMOTOR_OBJECT_STATUS
        ('emMask', c_int),              # 是否带口罩,详见EM_NONMOTOR_OBJECT_STATUS;Whether to wear a face mask,refer to EM_NONMOTOR_OBJECT_STATUS
        ('emEmotion', c_int),           # 表情,详见EM_EMOTION_TYPE;Emotion,refer to EM_EMOTION_TYPE
        ('emUpClothes', c_int),         # 上衣类型,详见EM_CLOTHES_TYPE;UpClothes type,refer to EM_CLOTHES_TYPE
        ('emDownClothes', c_int),       # 下衣类型,详见EM_CLOTHES_TYPE;DownClothes type,refer to EM_CLOTHES_TYPE
        ('emUpperBodyColor', c_int),    # 上衣颜色,详见EM_OBJECT_COLOR_TYPE;UpClothes color,refer to EM_OBJECT_COLOR_TYPE
        ('emLowerBodyColor', c_int),    # 下衣颜色,详见EM_OBJECT_COLOR_TYPE;DownClothes color,refer to EM_OBJECT_COLOR_TYPE
        ('bHasFaceImage', c_int),       # 是否有骑车人人脸抠图信息;Whether rider's face image information is contained
        ('stuFaceImage', RIDER_FACE_IMAGE_INFO),    # 骑车人人脸特写描述;Rider face image
        ('bHasFaceAttributes', c_int),  # 是否有人脸属性;Whether rider's face Attributes is contained
        ('stuFaceAttributes', NET_FACE_ATTRIBUTE_EX),   # 人脸属性;face Attributes
        ('emHasHat', c_int),            # 是否戴帽子,详见EM_HAS_HAT;whether has hat,refer to EM_HAS_HAT
        ('emCap', c_int),               # 帽类型,详见EM_CAP_TYPE;Cap type,refer to EM_CAP_TYPE
        ('emHairStyle', c_int),         # 头发样式,详见EM_HAIR_STYLE; Hair style,refer to EM_HAIR_STYLE
        ('stuFaceFeatureVectorInfo', NET_FACE_FEATURE_VECTOR_INFO), # 人脸特征值数据在二进制数据中的位置信息;Location information of Face characteristic value data in binary data;
        ('emFaceFeatureVersion', C_ENUM),   # 人脸特征值版本号 Refer: EM_FEATURE_VERSION;Face feature versio Refer: EM_FEATURE_VERSION;
        ('stuHumanFeatureVectorInfo', NET_HUMAN_FEATURE_VECTOR_INFO),   # 人体特征值数据在二进制数据中的位置信息;Location information of Human characteristic value data in binary data;
        ('emHumanFeatureVersion', C_ENUM),  # 人体特征值版本号 Refer: EM_FEATURE_VERSION;Human feature versio Refer: EM_FEATURE_VERSION;
        ('nAgeConf', C_UINT),               # 年龄段置信度;Age confidence;
        ('nUpColorConf', C_UINT),           # 上衣颜色置信度;Jacket color confidence;
        ('nDownColorConf', C_UINT),         # 下衣颜色置信度;Lower garment color confidence;
        ('nUpTypeConf', C_UINT),            # 上衣种类置信度;Confidence of coat type;
        ('nDownTypeConf', C_UINT),          # 下衣种类置信度;nDownTypeConf;
        ('nHatTypeConf', C_UINT),           # 帽子类型置信度;Hat type confidence;
        ('nHairTypeConf', C_UINT),          # 发型种类置信度;Confidence of hairstyle type;
        ('emUpperPattern', C_ENUM),         # 上半身衣服图案 Refer: EM_CLOTHES_PATTERN;Upper garment pattern Refer: EM_CLOTHES_PATTERN;
        ('nUpClothes', C_UINT),             # 上衣类型 0:未知 1:长袖 2:短袖 3:长款大衣 4:夹克及牛仔服 5:T恤6:运动装 7:羽绒服 8:衬衫 9:连衣裙 10:西装 11:毛衣 12:无袖 13:背心;Type of coat 0:Unknown 1:Long sleeve 2:Short sleeve 3:Long coat 4:Jacket and jeans 5: T-shirt6:Sportswear 7:Down-filled coat 8:shirt 9:Dress 10:suit 11:sweater 12:Sleeveless 13:vest;
        ('emUniformStyle', C_ENUM),         # 制服类型 Refer: EM_UNIFORM_STYLE;Uniform type Refer: EM_UNIFORM_STYLE;
        ('nRainCoat', C_UINT),              # 是否有雨披 0:未识别 1:无 2:有;Poncho 0:unrecognized 1:none 2:Yes;
        ('emCoatStyle', C_ENUM),            # 上衣款式 Refer: EM_COAT_TYPE;Coat style Refer: EM_COAT_TYPE;
        ('emAgeSeg', C_ENUM),               # 年龄段 Refer: EM_AGE_SEG;Age segmentation Refer: EM_AGE_SEG;
        ('nShoulderBag', C_UINT),           # 是否有肩包 0-未识别 1-无 2-有;Is there a shoulder bag 0:unrecognized 1:none 2:Yes;
        ('nMessengerBag', C_UINT),          # 是否有斜挎包 0-未识别 1-无 2-有;Is there a messenger bag 0:unrecognized 1:none 2:Yes;
        ('bNewUpClothes', C_BOOL),          # 是否支持新上衣类型;whether support emNewUpClothes;
        ('emNewUpClothes', C_ENUM),         # 新上衣类型 Refer: EM_NEWUPCLOTHES_TYPE;New up clothes type Refer: EM_NEWUPCLOTHES_TYPE;
        ('bNewDownClothes', C_BOOL),        # 是否支持新下衣类型;whether support emNewDownClothes;
        ('emNewDownClothes', C_ENUM),       # 新下衣类型 Refer: EM_NEWDOWNCLOTHES_TYPE;New down clothes type Refer: EM_NEWDOWNCLOTHES_TYPE;
        ('byReserved', C_BYTE * 140),       # 保留;Reserved;
    ]

class SCENE_IMAGE_INFO(Structure):
    """
    全景广角图;Scene image
    """
    _fields_ = [
        ('nOffSet', c_uint),            # 在二进制数据块中的偏移;image offset in the data
        ('nLength', c_uint),            # 图片大小,单位字节;image data length
        ('nWidth', c_uint),             # 图片宽度(像素);image width(pixel)
        ('nHeight', c_uint),            # 图片高度(像素);image Height(pixel)
        ('nIndexInData', C_UINT),  # 在上传图片数据中的图片序号;The serial number of the picture in the uploaded picture data;
        ('byReserved', c_ubyte*52),     # 预留字节;Reserved
    ]

class FACE_SCENE_IMAGE(Structure):
    """
   人脸全景图; Face scene image
    """
    _fields_ = [
        ('nOffSet', c_uint),    # 在二进制数据块中的偏移;image offset in the data
        ('nLength', c_uint),    # 图片大小,单位字节;image data length
        ('nWidth', c_uint),     # 图片宽度(像素);image width(pixel)
        ('nHeight', c_uint),    # 图片高度(像素);image Height(pixel)
        ('nIndexInData', C_UINT),  # 在上传图片数据中的图片序号;The serial number of the picture in the uploaded picture data;
        ('byReserved', c_ubyte * 52),  # 预留字节;Reserved
    ]

class NET_NONMOTOR_FEATURE_VECTOR_INFO(Structure):
    """
    非机动车特征值数据在二进制数据中的位置信息;Position info of non-motor feature data in binary data
    """
    _fields_ = [
        ('nOffset', c_uint),            # 非机动车特征值在二进制数据中的偏移, 单位:字节;The offset of non-motor feature data in binary data, unit:bytes
        ('nLength', c_uint),            # 非机动车特征值数据长度, 单位:字节;The length of non-motor feature data, unit:bytes
        ('bFeatureEnc', C_BOOL),  # 用于标识特征值是否加密;Identifies whether the feature is encrypted;
        ('byReserved', c_ubyte*28),     # 保留字节;Reserved
    ]

class NET_NONMOTOR_PLATE_IMAGE(Structure):
    """
    非机动车车牌图片信息;The plate image of no-motor
    """
    _fields_ = [
        ('nOffset', c_uint),            # 在二进制数据块中的偏移;image offset in the data
        ('nLength', c_uint),            # 图片大小,单位字节;image data length，Unit:byte
        ('nWidth', c_uint),             # 图片宽度;image width
        ('nHeight', c_uint),            # 图片高度;image Height
        ('nIndexInData', C_UINT),       # 在上传图片数据中的图片序号;Index in data;
        ('byReserved', c_ubyte * 508),  # 预留字节;Reserved
    ]


class NET_NONMOTOR_PLATE_INFO(Structure):
    """
    非机动车配牌信息;Plate info of nomotor
    """
    _fields_ = [
        ('szPlateNumber', c_char*128),                  # 非机动车车牌号;plate number
        ('stuBoundingBox', NET_RECT),                   # 包围盒， 非机动车矩形框，0~8191相对坐标;BoundingBox Rect, 0~8192
        ('stuOriginalBoundingBox', NET_RECT),           # 包围盒， 非机动车矩形框，绝对坐标;BoundingBox Rect, absolute coordinates
        ('stuPlateImage', NET_NONMOTOR_PLATE_IMAGE),    # 非机动车车牌抠图;plate image info
        ('emPlateColor', c_int),                        # 车牌颜色; Plate color
        ('byReserved', c_ubyte*132),                    # 保留;Reserved

    ]


class EVENT_INTELLI_COMM_INFO(Structure):
    """
    智能报警事件公共信息;intelli event comm info
    """
    _fields_ = [
        ('emClassType', c_int),             # 智能事件所属大类,详见EM_CLASS_TYPE;class type，refer to EM_CLASS_TYPE
        ('nPresetID', c_int),               # 该事件触发的预置点，取值范围为0~255，大于0表示在此预置点时有效。
                                            # Preset ID, value range is 0~255 and when the value is greater than 0 is valied
        ('bReserved', c_ubyte*124),         # 保留字节,留待扩展;reserved
    ]

class EVENT_PLATE_INFO(Structure):
    """
    车辆信息，记录了车头、车尾车牌号和车牌颜色;Plate info, Record the plate number and color of the front and back of the car
    """
    _fields_ = [
        ('szFrontPlateNumber', c_char*64),      # 车头车牌号码;front plate number
        ('emFrontPlateColor', c_int),           # 车头车牌颜色,详见EM_PLATE_COLOR_TYPE;front plate color,refer to EM_PLATE_COLOR_TYPE
        ('szBackPlateNumber', c_char * 64),     # 车尾车牌号码;back plate number
        ('emBackPlateColor', c_int),            # 车尾车牌颜色,详见EM_PLATE_COLOR_TYPE;back plate color,refer to EM_PLATE_COLOR_TYPE
        ('reversed', c_ubyte*128),              # 保留;reserved
    ]

class VA_OBJECT_NONMOTOR(Structure):
    """
    非机动车对象;Nonmotor
    """
    _fields_ = [
        ('nObjectID', c_int),           # 物体ID,每个ID表示一个唯一的物体;Object id
        ('emCategory', c_int),          # 非机动车子类型,详见EM_CATEGORY_NONMOTOR_TYPE;Non-motor type,refer to EM_CATEGORY_NONMOTOR_TYPE
        ('stuBoundingBox', SDK_RECT),   # 包围盒， 非机动车矩形框，0~8191相对坐标;BoundingBox Rect, 0~8192
        ('stuOriginalBoundingBox', SDK_RECT),   # 包围盒， 非机动车矩形框，绝对坐标;BoundingBox Rect, absolute coordinates
        ('stuMainColor', NET_COLOR_RGBA),       # 非机动车颜色, RGBA;Non-motor color (RGBA value)
        ('emColor', c_int),                     # 非机动车颜色, 枚举,详见EM_OBJECT_COLOR_TYPE;Non-motor color enumeration，refer to EM_OBJECT_COLOR_TYPE
        ('bHasImage', c_int),                   # 是否有抠图; whether has image or not
        ('stuImage', NET_NONMOTOR_PIC_INFO),    # 物体截图;Image information
        ('nNumOfCycling', c_int),               # 骑车人数量;The number of rider
        ('stuRiderList', NET_RIDER_INFO*16),    # 骑车人特征,个数和nNumOfCycling关联;The information of rider
        ('stuSceneImage', SCENE_IMAGE_INFO),    # 全景广角图;SceneImage
        ('stuFaceSceneImage', FACE_SCENE_IMAGE),    # 人脸全景广角图; Face SceneImage
        ('nNumOfFace', c_int),                      # 检测到的人脸数量;The number of face
        ('fSpeed', c_float),                        # 物体速度，单位为km/h;Object speed, Unit:km/h
        ('stuNonMotorFeatureVectorInfo', NET_NONMOTOR_FEATURE_VECTOR_INFO), #  非机动车特征值数据在二进制数据中的位置信息
                                                                            # Position info of non-motor feature data in binary data
        ('emNonMotorFeatureVersion', c_int),    #  非机动车特征值版本号,详见EM_FEATURE_VERSION;Non-motor feature data version，refer to EM_FEATURE_VERSION
        ('stuNomotorPlateInfo', NET_NONMOTOR_PLATE_INFO),  #  非机动车牌信息;Plate info of nomotor
        ('stuObjCenter', SDK_POINT),            # 物体型心(不是包围盒中心), 0-8191相对坐标, 相对于大图; Center of object(not center of bounding box), 0-8191 relative coordinates, relative to large graph
        ('stuFaceFeatureVectorInfo', NET_FACE_FEATURE_VECTOR_INFO), # 人脸特征值数据在二进制数据中的位置信息, 废弃;(Discard)Location information of face characteristic value data in binary data;
        ('emFaceFeatureVersion', C_ENUM),           # 人脸特征值版本号, 废弃 Refer: EM_FEATURE_VERSION;(Discard)face feature version Refer: EM_FEATURE_VERSION;
        ('nCategoryConf', c_int),                   # 非机动车类型置信度;Non motor vehicle type confidence;
        ('szNonMotorFeatureVersion', c_char * 32),  # 非机动车特征值版本号-字符串;Non-motor feature data version-string;
        ('emNonMotorAngle', C_ENUM),                # 非机动车的角度 Refer: EM_OBJECT_NONMOTORANGLE_TYPE;Non Motor vehicle angle Refer: EM_OBJECT_NONMOTORANGLE_TYPE;
        ('emBasket', C_ENUM),                       # 非机动车车篮 Refer: EM_OBJECT_BASKET_TYPE;Non Motor vehicle basket Refer: EM_OBJECT_BASKET_TYPE;
        ('emStorageBox', C_ENUM),                   # 非机动车后备箱 Refer: EM_OBJECT_STORAGEBOX_TYPE;Non Motor vehicle StorageBox Refer: EM_OBJECT_STORAGEBOX_TYPE;
        ('nCompleteScore', C_UINT),                 # 非机动车完整度评分，范围[0,100]，越大越完整;Non motor vehicle integrity score, range [0,100];
        ('nClarityScore', C_UINT),                  # 非机动车清晰度分值 取值范围为[1,100], 越大越清晰, 0为无效值;The value range of non motor vehicle definition score is [1,100];
        ('nStartSequence', C_UINT),                 # 目标出现的帧号;The frame number of the target start;
        ('nEndSequence', C_UINT),                   # 目标消失的帧号;The frame number of the target end;
        ('bIsErrorDetect', C_BOOL),                 # 非机动车车身及骑手整体，是否虚检，0: 否，1: 是;Whether the whole non motor vehicle body and rider are falsely inspected, 0: No, 1: Yes;
        ('nImageLightType', C_UINT),                # 图像成像光源类型, 0:未知, 1:可见光成像, 2:近红外成像(灰度图), 3:热红外成像(伪彩色);Image imaging light source type,0:unknown, 1:visible imaging, 2:near infrared imaging(gray image), 3:thermal infrared imaging (pseudo color);
        ('nAbsScore', C_UINT),                      # 非机动车综合质量评分，范围[0,100]，越大质量越好;Non motor vehicle comprehensive quality score, range [0,100], the larger the score, the better the quality;
        ('emRainShedType', C_ENUM),                 # 雨棚（伞）类型 Refer: EM_RAIN_SHED_TYPE;Canopy (umbrella) type Refer: EM_RAIN_SHED_TYPE;
        ('szSerialUUID', c_char * 22),              # 智能物体全局唯一物体标识有效数据位21位，包含’\0’前2位%d%d:01-视频片段, 02-图片, 03-文件, 99-其他中间14位YYYYMMDDhhmmss:年月日时分秒后5位%u%u%u%u%u：物体ID，如00001;Intelligent object global unique object identificationValid data bits are 21 bits, including '\0'Top 2 bits %d%d: 01-video clip, 02-picture, 03-file, 99-otherMiddle 14 bit yyyymmddhhmmssLast 5 bits %U%U%U%U%U: object ID, such as 00001;
        ('szReserved', c_char * 2),                 # 对齐;reserved;
        ('nHumanFeatureExtractSingle', C_UINT),  # 非机动车的骑手和车身是否单独提取, 0:否, 1:是;Whether the rider and body of non-motor vehicle are extracted separately, 0: No, 1: Yes;
        ('byReserved', C_BYTE * 2920),              # 保留;reserved;
    ]

class SCENE_IMAGE_INFO_EX(Structure):
    """
    全景广角图; Scene image
    """
    _fields_ = [
        ('nOffSet', c_uint),             # 在二进制数据块中的偏移;mage offset in the data
        ('nLength', c_uint),             # 图片大小,单位字节;image data length
        ('nWidth', c_uint),              # 图片宽度(像素);image width(pixel)
        ('nHeight', c_uint),             # 图片高度(像素);image Height(pixel)
        ('szFilePath', c_char*260),      # 全景图片路径;file path
        ('nIndexInData', C_UINT),        # 在上传图片数据中的图片序号;The serial number of the picture in the uploaded picture data;
        ('szImageID', c_char * 42),      # 图片ID;Image ID;
        ('szReserved', c_char * 6),      # 预留字节;Reserved;
        ('byReserved', C_BYTE * 460),    # 预留字节;Reserved;
    ]

class NET_IMAGE_INFO_EX2(Structure):
    """
    图片信息
    image information
    """
    _fields_ = [
        ('emType', C_ENUM),  # 图片类型 Refer: EM_IMAGE_TYPE_EX2;Picture type Refer: EM_IMAGE_TYPE_EX2;
        ('nOffset', C_UINT),  # 在二进制数据块中的偏移;Offset in the binary data block;
        ('nLength', C_UINT),  # 图片大小,单位:字节;Picture size, unit: byte;
        ('byReserverd', c_char * 4),  # 用于字节对齐;for byte alignment;
        ('szPath', c_char * 256),  # 图片存储位置;Picture storage location;
    ]

class NET_IMAGE_INFO_EX3(Structure):
    """
    图片扩展信息
    image information
    """
    _fields_ = [
        ('emType', C_ENUM),  # 图片类型 Refer: EM_IMAGE_TYPE_EX2;Picture type Refer: EM_IMAGE_TYPE_EX2;
        ('nOffset', C_UINT),  # 在二进制数据块中的偏移;Offset in the binary data block;
        ('nLength', C_UINT),  # 图片大小,单位:字节;Picture size, unit: byte;
        ('byReserverd', c_char * 4),  # 用于字节对齐;for byte alignment;
        ('szPath', c_char * 256),  # 图片存储位置;Picture storage location;
        ('szEncryptKey', c_char * 128),  # 二进制图片加密秘钥，设备传过来的是Base64编码之后的，SDK不做解码处理;The binary image encryption key is transmitted from the device after Base64 encoding, and the SDK does not perform decoding processing;
        ('szEncryptLKey', c_char * 256),  # 二进制图片加密秘钥，设备传过来的是Base64编码之后的，SDK不做解码处理;The binary image encryption key is transmitted from the device after Base64 encoding, and the SDK does not perform decoding processing;
        ('byReserverd2', C_BYTE * 768),  # 用于字节对齐;Reserved bytes;
    ]

class NET_A_MSG_OBJECT_SUPPLEMENT(Structure):
    """
    视频分析物体信息补充字段，与 MSG_OBJECT 的合集表示视频分析物体信息
    Supplementary field of video analysis object information
    """
    _pack_ = 4
    _fields_ = [
        ('szObjectUUID', c_char * 48),  # 智能物体全局唯一物体标识;Global unique object identification of intelligent object;
        ('nMuckHide', C_UINT),  # 渣土车是否遮盖识别,0:渣土车是否遮盖未知,1:渣土车遮盖,2:渣土车无遮盖空载,3:渣土车无遮盖满载.;Whether the muck truck is covered and identified, 0: whether the muck truck is covered is unknown, 1: the muck truck is covered, 2: the muck truck is not covered and unloaded, 3: the muck truck is not covered and fully loaded;
        ('nCarryType', C_UINT),  # 货车载货类型,0:货车是否载货未知,1:沙子,2:泥浆,3:石头,4:石渣. char szReserved[256];  预留字节;Truck loading type, 0: unknown whether the truck is loaded, 1: sand, 2: mud, 3: stone, 4: stone slag;
        ('szCategory', c_char * 32),  # 物体类型;Category type;
        ('szReserved', c_char * 216),  # Reserved;Reserved;
    ]

class NET_EVENT_INFO_EXTEND(Structure):
    """
    事件公共字段扩展结构体: 该结构体仅用于 普通报警事件类型(不带图报警事件类型) 和 智能报警事件类型(带图报警事件类型) 的公共字段扩展使用
    Event public field extension structure: This structure is only used for common field expansion of common alarm event type (without graph alarm event type) and intelligent alarm event type (with graph alarm event type)
    """
    _fields_ = [
        ('bRealUTC', C_BOOL),  # RealUTC 是否有效，bRealUTC 为 TRUE 时，用 stuRealUTC，否则 stuRealUTC 字段无效(用原事件结构体中的 事件发生时间/事件触发时间(UTC) 字段);Whether RealUTC is valid, when bRealUTC is TRUE, use stuRealUTC, otherwise the stuRealUTC field is invalid (use the event occurrence time/event trigger time (UTC) field in the original event structure);
        ('byReserved', c_char * 4),  # 仅用于字节对齐;only for byte alignment;
        ('stuRealUTC', NET_TIME_EX),  # 事件发生的时间(标准UTC时间(不带时区夏令时偏差)), 由于事件的UTC时间在产品线之间使用的差异性, 故增加RealUTC作为标准UTC时间, 平台在收到事件解析首优先级是RealUTC, 其次是UTC.;The time when the event occurred (standard UTC time (without time zone daylight saving time offset)), due to the difference in the use of the UTC time of the event between product lines, RealUTC is added as the standard UTC time, and the platform receives The first priority of event parsing is RealUTC, followed by UTC.;
        ('bIsEventsTypeValid', C_BOOL),  # 事件类型是否有效;is enable EventsType;
        ('szEventsType', C_UINT),  # 事件类型, bIsEventsTypeValid为TRUE时有效, 0:正常抓图事件, 1:邮件联动抓图事件(图片通过第二路抓图码流上来，和正常抓图的图片可以不一样);Event type: This parameter is valid when bIsEventsTypeValid is TRUE. 0: normal capture event. 1: Email linkage capture event.;
        ('szReserved', c_char * 1012),  # 保留字节;reserved bytes;
    ]

class DEV_EVENT_TRAFFICJUNCTION_INFO(Structure):
    """
    事件类型TRAFFICJUNCTION(交通路口老规则事件/视频电警上的交通卡口老规则事件)对应的数据块描述信息;Event Type TRAFFICJUNCTION (transportation card traffic junctions old rule event / video port on the old electric alarm event rules) corresponding to the description of the data block
    """
    _fields_ = [
        ('nChannelID', c_int),              # 通道号;ChannelId
        ('szName', c_char*128),             # 事件名称;event name
        ('byMainSeatBelt', c_ubyte),        # 主驾驶座,系安全带状态,1-系安全带,2-未系安全带;main driver, seat, safety belt , 1-fastened, 2-unfastened
        ('bySlaveSeatBelt', c_ubyte),       # 副驾驶座,系安全带状态,1-系安全带,2-未系安全带;co-drvier, seat, safety belt, 1-fastened, 2-unfastened
        ('byVehicleDirection', c_ubyte),    # 当前被抓,拍到的车辆是车头还是车尾,具体请见 EM_VEHICLE_DIRECTION;Current snapshot is head or rear, see  EM_VEHICLE_DIRECTION
        ('byOpenStrobeState', c_ubyte),     # 开闸状态,具体请见EM_OPEN_STROBE_STATE;Open status, see EM_OPEN_STROBE_STATE
        ('PTS', c_double),                  # 时间戳(单位是毫秒);PTS(ms)
        ('UTC', NET_TIME_EX),               # 事件发生的时间;the event happen time
        ('nEventID', c_int),                # 事件ID;event ID
        ('stuObject', SDK_MSG_OBJECT),      # 检测到的物体;have being detected object
        ('nLane', c_int),                   # 对应车道号;road number
        ('dwBreakingRule', C_DWORD),        # 违反规则掩码,第一位:闯红灯;BreakingRule's mask,first byte: crash red light;
                                            # 第二位:不按规定车道行驶;secend byte:break the rule of driving road number;
                                            # 第三位: 逆行;the third byte:converse;
                                            # 第四位：违章掉头;the forth byte:break rule to turn around;
                                            # 第五位: 交通堵塞;the five byte:traffic jam;
                                            # 第六位: 交通异常空闲;the six byte:traffic vacancy;
                                            # 第七位:压线行驶;否则默认为: 交通路口事件;the seven byte: Overline; defalt:trafficJunction
        ('RedLightUTC', NET_TIME_EX),       # 红灯开始UTC时间;the begin time of red light
        ('stuFileInfo', SDK_EVENT_FILE_INFO),  # 事件对应文件信息;event file info
        ('nSequence', c_int),               # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;snap index,such as 3,2,1,1 means the last one,0 means there has some exception and snap stop
        ('nSpeed', c_int),                  # 车辆实际速度Km/h;car's speed (km/h)
        ('bEventAction', c_ubyte),          # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;
        ('byDirection', c_ubyte),           # 路口方向,1-表示正向,2-表示反向;Intersection direction 1 - denotes the forward 2 - indicates the opposite
        ('byLightState', c_ubyte),          # LightState表示红绿灯状态:0 未知,1 绿灯,2 红灯,3 黄灯;LightState means red light status:0 unknown,1 green,2 red,3 yellow
        ('byReserved', c_ubyte),            # 保留字节;reserved
        ('byImageIndex', c_ubyte),          # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0
        ('stuVehicle', SDK_MSG_OBJECT),     # 车身信息;vehicle info
        ('dwSnapFlagMask', C_DWORD),        # 抓图标志(按位),0位:"*",1位:"Timing",2位:"Manual",3位:"Marked",4位:"Event",5位:"Mosaic",6位:"Cutout"
                                            # snap flags(by bit),0bit:"*",1bit:"Timing",2bit:"Manual",3bit:"Marked",4bit:"Event",5bit:"Mosaic",6bit:"Cutout"
        ('stuResolution', SDK_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution
        ('szRecordFile', c_char*128),            # 报警对应的原始录像文件信息;Alarm corresponding original video file information
        ('stuCustomInfo', EVENT_JUNCTION_CUSTOM_INFO),  # 报警对应的原始录像文件信息; info
        ('byPlateTextSource', c_ubyte),     # 车牌识别来源, 0:本地算法识别,1:后端服务器算法识别;the source of plate text, 0:Local,1:Server
        ('bReserved1', c_ubyte*3),          # 保留字节,留待扩展.;Reserved bytes, leave extended_
        ('stuGPSInfo', NET_GPS_INFO),       # GPS信息 车载;GPS info ,use in mobile DVR/NVR
        ('byNoneMotorInfo', c_ubyte),       # 0-无非机动车人员信息信息,1-有非机动车人员信息信息;specified the person info of none motor
                                            # 此字段为1时下面11个字段生效;1 means 11 fields followed is valid
        ('byBag', c_ubyte),                 # 是否背包, 0-未知 1-不背包   2-背包;0-unknown 1-no bag   2-bag
        ('byUmbrella', c_ubyte),            # 是否打伞, 0-未知 1-不打伞   2-打伞;0-unknown 1-no umbrella   2-Umbrella
        ('byCarrierBag', c_ubyte),          # 手提包状态,0-未知 1-没有 2-有;0-unknown 1-no carrierBag 2-carrierBag
        ('byHat', c_ubyte),                 # 是否戴帽子, 0-未知 1-不戴帽子 2-戴帽子;0-unknown 1-no helmet 2-helmet
        ('byHelmet', c_ubyte),              # 头盔状态,0-未知 1-没有 2-有;0-unknown 1-no hat 2-hat
        ('bySex', c_ubyte),                 # 性别,0-未知 1-男性 2-女性;0-unknown 1-man 2-woman
        ('byAge', c_ubyte),                 # 年龄;age
        ('stuUpperBodyColor', NET_COLOR_RGBA),      # 上身颜色;upper body color
        ('stuLowerBodyColor', NET_COLOR_RGBA),      # 下身颜色;lower body color
        ('byUpClothes', c_ubyte),                   # 上身衣服类型 0:未知 1:长袖 2:短袖 3:长裤 4:短裤 5:裙子 6:背心 7:超短裤 8:超短裙;upper clothes 0:unknown 1:long sleeve 2:short sleeve 3:trousers 4:breeches 5:skirt 6:vest 7:minipants 8:miniskirt
        ('byDownClothes', c_ubyte),                 # 下身衣服类型 0:未知 1:长袖 2:短袖 3:长裤 4:短裤 5:裙子 6:背心 7:超短裤 8:超短裙;lower clothes 0:unknown 1:long sleeve 2:short sleeve 3:trousers 4:breeches 5:skirt 6:vest 7:minipants 8:miniskirt
        ('stuExtensionInfo', NET_EXTENSION_INFO),   # 扩展信息;Extension info
        ('bReserved', c_ubyte*22),                  # 保留字节,留待扩展;Reserved bytes, leave extended
        ('nTriggerType', c_int),                    # TriggerType:触发类型,0车检器,1雷达,2视频,3RSU;Trigger Type:0 vehicle inspection device, 1 radar, 2 video, 3 RSU
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),         # 交通车辆信息;Traffic vehicle info
        ('dwRetCardNumber', C_DWORD),           # 卡片个数;Card Number
        ('stuCardInfo', EVENT_CARD_INFO*16),    # 卡片信息;Card information
        ('stCommInfo', EVENT_COMM_INFO),        # 公共信息;public info
        ('bNonMotorInfoEx', c_int),             # 是否有非机动车信息;Non-motor info enable
        ('stuNonMotor', VA_OBJECT_NONMOTOR),    # 非机动车信息;Non-motor information
        ('stuIntelliCommInfo', EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info
        ('stuPlateInfo', EVENT_PLATE_INFO),     # 车辆信息，记录了车头、车尾车牌号和车牌颜色;Plate info, Record the plate number and color of the front and back of the car;
        ('bSceneImage', C_BOOL),                # 全景图是否有效;Scene Image valid or invalid;
        ('stuSceneImage', SCENE_IMAGE_INFO_EX),  # 全景图;Scene Image;
        ('pstObjects', POINTER(SDK_MSG_OBJECT)),  # 检测到的多个车牌信息;detected objects;
        ('nObjectNum', c_int),                  # 检测到的多个车牌个数;detected objects numbers;
        ('emVehiclePosture', C_ENUM),           # 车辆姿势 Refer: EM_VEHICLE_POSTURE_TYPE;vehicle posture Refer: EM_VEHICLE_POSTURE_TYPE;
        ('nVehicleSignConfidence', C_UINT),     # 车标置信度（范围：0~100）;vehicle sign confidence(range:0~100);
        ('nVehicleCategoryConfidence', C_UINT),  # 车型置信度（范围：0~100）;vehicle category confidence(range:0~100);
        ('emCarDrivingDirection', C_ENUM),      # 规则区内车辆行驶方向 Refer: EM_CAR_DRIVING_DIRECTION;Driving direction of vehicles in the regular area Refer: EM_CAR_DRIVING_DIRECTION;
        ('stuImageInfo', NET_IMAGE_INFO_EX2 * 32),  # 图片信息数组;image information array;
        ('nImageInfoNum', c_int),               # 图片信息个数;the number of image information;
        ('szSerialNo', c_char * 128),           # 和客户端请求的抓图序列号对应;Corresponds to the snapshot serial number requested by the client;
        ('nAlarmCompliance', C_UINT),           # 报警合规, 0:未知, 1:不合规, 2:合规;Alarm Compliance, 0:Unknown, 1:Not Compliant, 2:Compliant;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('stObjectInfoEx', NET_A_MSG_OBJECT_SUPPLEMENT),    # 视频分析物体信息补充字段，与 MSG_OBJECT 的合集表示视频分析物体信息;Supplementary field of video analysis object information;
        ('pstuObjectEx2', POINTER(NET_A_MSG_OBJECT_EX2)),  # 检测到的物体扩展;have being detected object expansion;
        ('pstuVehicleEx2', POINTER(NET_A_MSG_OBJECT_EX2)),  # 车身信息扩展;vehicle info expansion;
        ('pstuObjectsEx2', POINTER(NET_A_MSG_OBJECT_EX2)),  # 检测到的多个车牌信息扩展，数量为nObjectNum;detected objects,The number is nObjectNum;
        ('nPresetID', C_UINT),  # 事件触发的预置点号，从1开始, 0表示未知;The preset point number triggered by the event, starting from 1, and 0 means unknown;
        ('nTransfer', c_int),
        # 文件传输状态, -1: 未知, 0-实时数据下载，1-离线数据下载, 2-离线数据传输完成, 3-离线数据传输中断;File transfer status, - 1: unknown, 0 - real-time data download, 1 - offline data download, 2 - offline data transfer completed, 3 - offline data transfer interrupted;
        ('szFeatureVersion', c_char * 32),  # 特征值的版本号;Version of the Feature;
        ('nDetectMode', C_UINT),
        # 检测物体具体包含的信息类型: 0: 只包含属性 1: 只包含特征值 2: 属性、特征值都包含 3:属性和特征值都不包含;The specific type of information contained in the detected object: 0: Only contains attributes 1: Only contains feature values 2: Both attributes and feature values contain 3: Neither attributes nor feature values contain;
        ('byReserved2', c_char * (544 - 3 * sizeof(c_void_p))),  # 保留字节;Reserved;
    ]

class EVENT_INFO(Structure):
    """
    事件信息;Event info
    """
    _fields_ = [
        ('nEvent', c_int),                  # 事件类型,参见智能事件类型，如 EVENT_IVS_ALL;Event type, see intelligent analysis event type,like EVENT_IVS_ALL
        ('arrayObejctType', c_int * 16),    # 支持的物体类型，当前支持 EM_OBJECT_TYPE.HUMAN, EM_OBJECT_TYPE.VECHILE, EM_OBJECT_TYPE.NOMOTOR, EM_OBJECT_TYPE.ALL,参考EM_OBJECT_TYPE;object type, currently support EM_OBJECT_TYPE_HUMAN, EM_OBJECT_TYPE_VECHILE, EM_OBJECT_TYPE_NOMOTOR, EM_OBJECT_TYPE_ALL
        ('nObjectCount', c_int),            # szObejctType 数量;szObejctType's count
        ('byReserved', c_ubyte * 512),      # 预留字段;reserved
    ]

class NET_VKINFO(Structure):
    """
    VK二值对信息
    VK info
    """
    _fields_ = [
        ('szVKID', c_char * 128),  # VKID;VKID;
        ('szVK', c_char * 128),  # VK;VK;
        ('emAlgorithmType', C_ENUM),  # 加密算法类型 Refer: EM_ALGORITHM_TYPE;AlgorithmType Refer: EM_ALGORITHM_TYPE;
        ('nRetVKIDLen', c_int),  # 返回的VKID字段的实际大小;Return VKID len;
        ('nRetVKLen', c_int),  # 返回的VK实际大小;Return VK len;
        ('emIsEncrypt', C_ENUM),  # 是否加密 Refer: EM_IS_ENCRYPT;Encrypt or not Refer: EM_IS_ENCRYPT;
        ('emIsCurrent', C_ENUM),  # 是否是当前VK 0 ：未知，1：当前， 2：之前 Refer: EM_IS_CURRENT_VK;Is the current VK 0: unknown, 1: current, 2: previous Refer: EM_IS_CURRENT_VK;
        ('byReserved', C_BYTE * 492),  # 保留字节;Reserved;
    ]

class NET_IN_PLAY_BACK_BY_TIME_INFO(Structure):
    """
    录像回放入参信息; record play back parameter in
    """
    _fields_ = [
        ('stStartTime', NET_TIME),      # 开始时间;Begin time;
        ('stStopTime', NET_TIME),       # 结束时间;End time;
        ('hWnd', c_long),               # 播放窗格, 可为NULL;Play window;
        ('cbDownLoadPos', CB_FUNCTYPE(None, C_LLONG, C_DWORD, C_DWORD, C_LDWORD)),  # 进度回调;Download pos callback;
        ('dwPosUser', C_LDWORD),        # 进度回调用户信息;Pos user;
        ('fDownLoadDataCallBack', CB_FUNCTYPE(c_int, C_LLONG, C_DWORD, POINTER(C_BYTE), C_DWORD, C_LDWORD)),# 数据回调;Download data callback;
        ('dwDataUser', C_LDWORD),       # 数据回调用户信息;Data user;
        ('nPlayDirection', c_int),      # 播放方向, 0:正放; 1:倒放;;Playback direction;
        ('nWaittime', c_int),           # 接口超时时间, 目前倒放使用;Watiting time;
        ('pstuEventInfo', POINTER(EVENT_INFO)), # 事件信息，用户分配内存，不用时赋值为NULL;Event info, user allocate memory;
        ('nEventInfoCount', C_UINT),    # pstuEventInfo 个数，最大为 16;pstuEventInfo's count, max num is 16;
        ('emSubClass', C_ENUM),         # 从设备类型 Refer: EM_SUBCLASSID_TYPE;subclass ID Refer: EM_SUBCLASSID_TYPE;
        ('pVKInfoCallBack', CB_FUNCTYPE(None, C_LLONG, POINTER(NET_VKINFO), C_DWORD, C_LDWORD, c_void_p)),  # VK信息回调;VK message callback;
        ('dwVKInfoUser', C_LDWORD),     # VK信息回调用户信息;VK message Callback user information;
        ('pOriDataCallBack', CB_FUNCTYPE(c_int, C_LLONG, C_DWORD, POINTER(C_BYTE), C_DWORD, C_LDWORD)), # 原始数据回调;original data callback;
        ('dwOriDataUser', C_LDWORD),    # 原始数据回调用户信息;original data callback user information;
        ('bOnlySupportRealUTC', C_BOOL),    # 为TRUE表示仅下发stuStartTimeRealUTC和stuEndTimeRealUTC(不下发stStartTime, stStopTime), 为FALSE表示仅下发stStartTime, stStopTime(不下发stuStartTimeRealUTC和stuEndTimeRealUTC);TRUE means only send stuStartTimeRealUTC and stuEndTimeRealUTC (do not send stStartTime, stStopTime), if FALSE means only send stStartTime, stStopTime (do not send stuStartTimeRealUTC and stuEndTimeRealUTC);
        ('stuStartTimeRealUTC', NET_TIME),  # 录像的起始UTC时间(标准UTC时间);Recording start UTC time (standard UTC time);
        ('stuEndTimeRealUTC', NET_TIME),    # 录像的结束UTC时间(标准UTC时间);end UTC time of recording (standard UTC time);
        ('bReserved', C_BYTE * (940 - 2 * sizeof(c_void_p))),   # 预留字段;Reserved;
    ]

class NET_OUT_PLAY_BACK_BY_TIME_INFO(Structure):
    """
    录像回放出参信息; record play back parameter out
    """
    _fields_ = [
        ('bReserved', c_ubyte * 1024),                # 预留字节; reserved
    ]

class SNAP_PARAMS(Structure):
    """
    抓图参数结构体;Snapshot parameter structure
    """
    _fields_ = [
        ('Channel', c_uint),            # 抓图的通道；Snapshot channel
        ('Quality', c_uint),            # 画质；1~6；Image quality:level 1 to level 6
        ('ImageSize', c_uint),          # 画面大小；0：QCIF,1：CIF,2：D1；Video size;0:QCIF,1:CIF,2:D1
        ('mode', c_uint),               # 抓图模式；-1:表示停止抓图, 0：表示请求一帧, 1：表示定时发送请求, 2：表示连续请求；Snapshot mode;0:request one frame,1:send out requestion regularly,2: Request consecutively
        ('InterSnap', c_uint),          # 时间单位秒；若mode=1表示定时发送请求时,只有部分特殊设备(如：车载设备)支持通过该字段实现定时抓图时间间隔的配置
                                        # Time unit is second.If mode=1, it means send out requestion regularly. The time is valid.
        ('CmdSerial', c_uint),          # 请求序列号，有效值范围 0~65535，超过范围会被截断为 unsigned short；Request serial number，valid value:0~65535
        ('Reserved', c_uint*4),         # 预留字节;reserved
    ]

class NET_MOTIONDETECT_REGION_INFO(Structure):
    """
    动检区域信息;Region info of motion detection
    """
    _fields_ = [
        ('nRegionID', c_uint),          # 区域ID;region ID
        ('szRegionName', c_char*64),    # 区域名称;region name
        ('bReserved', c_ubyte*508),     # 保留字节;reserved
    ]

class NET_GPS_STATUS_INFO(Structure):
    """
    GPS状态信息; GPS statu information
    """
    _fields_ = [
        ('revTime', NET_TIME),  # 定位时间; time;
        ('DvrSerial', c_char * 50),  # 设备序列号; device number;
        ('byRserved1', C_BYTE * 6),  # 对齐字节; align;
        ('longitude', c_double),  # 经度(单位是百万分之度,范围0-360度); longitude(1/1000000,range[0-360]);
        ('latidude', c_double),  # 纬度(单位是百万分之度,范围0-180度); latitude(1/1000000,range[0-180]);
        ('height', c_double),  # 高度(米); highness(m);
        ('angle', c_double),  # 方向角(正北方向为原点,顺时针为正); angle(north is source point,clockwise is positive);
        ('speed', c_double),  # 速度(单位km/H); speed(sea mile,speed/1000*1.852km/h);
        ('starCount', c_uint16),  # 定位星数, emDateSource为 EM_DATE_SOURCE_GPS时有效; star count;
        ('byRserved2', C_BYTE * 2),  # 对齐字节; align;
        ('antennaState', C_ENUM),  # 天线状态, emDateSource为 EM_DATE_SOURCE_GPS时有效,参考枚举NET_THREE_STATUS_BOOL; antenna state(true good, false bad) valid when emDateSource is EM_DATE_SOURCE_GPS,Please refer to NET_THREE_STATUS_BOOL;
        ('orientationState', C_ENUM),   # 定位状态; positioning status
        ('workStae', c_int),  # 工作状态(0=未定位,1=非差分定位,2=差分定位,3=无效PPS,6=正在估算,emDateSource为 EM_DATE_SOURCE_GPS时有效; working state(true normal, false abnormity),valid when emDateSource is EM_DATE_SOURCE_GPS;
        ('nAlarmCount', c_int),  # 发生的报警位置个数; alarm count;
        ('nAlarmState', c_int * 128),  # 发生的报警位置,值可能多个, emDateSource为 EM_DATE_SOURCE_GPS时有效; alarm type valid when emDateSource is EM_DATE_SOURCE_GPS;
        ('bOffline', C_BYTE),  # 0-实时 1-补传; 0- real time 1-fill;
        ('bSNR', C_BYTE),  # GPS信噪比,表示GPS信号强度,值越大,信号越强 范围：0~100,0表示不可用; SNR for GPS, range: 0~100, 0 for unusable;
        ('byRserved3', C_BYTE * 2),  # 对齐字节; align;
        ('emDateSource', C_ENUM),  # 数据来源,参考枚举EM_DATE_SOURCE; source of date,Please refer to EM_DATE_SOURCE;
        ('nSignalStrength', c_int), # 在当前工作模式下（GPS或北斗等系统）的信号强度;The signal strength in the current working mode (GPS or Beidou systems);
        ('fHdop', c_float),  # 水平精度因子惯性导航时无效;The horizontal precision factor is invalid during inertial navigation;
        ('fPdop', c_float),  # 位置精度因子,惯性导航时无效;Position precision factor, invalid in inertial navigation;
        ('byRserved', C_BYTE * 100),  # 保留字节; reserved bytes;
    ]

class ALARM_MOTIONDETECT_INFO(Structure):
    """
    报警事件类型SDK_ALARM_TYPE.EVENT_MOTIONDETECT(视频移动侦测事件)对应的数据描述信息;alarm event type SDK_ALARM_TYPE.EVENT_MOTIONDETECT (video motion detection event) corresponding data description info
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小；Structure size
        ('nChannelID', c_int),                          # 通道号;channel
        ('PTS', c_double),                              # 时间戳(单位是毫秒);timestamp (unit is millisecond)
        ('UTC', NET_TIME_EX),                           # 事件发生的时间;event occurrence time
        ('nEventID', c_int),                            # 事件ID;event ID
        ('nEventAction', c_int),                        # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;event action, 0 means pulse event, 1 means continuous event begin, 2 means continuous event end;
        ('nRegionNum', c_uint),                         # 动检区域个数;count of region
        ('stuRegion', NET_MOTIONDETECT_REGION_INFO*32),    # 动检区域信息;region info of motion detection
        ('bSmartMotionEnable', c_int),                  # 智能动检是否使能;smart motion detection is enable or not
        ('nDetectTypeNum', c_uint),                     # 动检触发类型个数;count of triggeing motion detection type
        ('emDetectType', c_int*32),                     # 动检触发类型, 当nRegionNum大于0时，和stuRegion数组一一对应,参考枚举EM_MOTION_DETECT_TYPE;triggeing motion detection type, when nRegionNum>0，one-to-one correspondence with stuRegion if nRegionNum is biger than 0，refer to EM_MOTION_DETECT_TYPE
                                                        # 若nRegionNum为0，触发区域未知，不与窗口绑定，默认第一个元素表示触发类型;the type is the first value of emDetectType if nRegionNum is 0
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),      # 事件公共扩展字段结构体;Event public extension field structure;
        ('stuGPSStatusInfo', NET_GPS_STATUS_INFO), # GPS信息; GPS information
        
    ]

class NET_FACE_INFO(Structure):
    """
    多人脸检测信息; multi faces detect info
    """
    _fields_ = [
        ('nObjectID', c_int),               # 物体ID,每个ID表示一个唯一的物体;object id
        ('szObjectType', c_char * 128),     # 物体类型;object type
        ('nRelativeID', c_int),             # 这张人脸抠图所属的大图的ID;same with the source picture id
        ('BoundingBox', SDK_RECT),          # 包围盒;bounding box
        ('Center', SDK_POINT),              # 物体中心;object center
    ]

class NET_FEATURE_VECTOR(Structure):
    """
    特征值信息; Feature data Information
    """
    _fields_ = [
        ('dwOffset', C_DWORD),  # 人脸小图特征值在二进制数据块中的偏移;Face feature data offset in data block(Unit:BYTE)
        ('dwLength', C_DWORD),  # 人脸小图特征值长度，单位:字节;Face feature data length(Unit:BYTE)
        ('bFeatureEnc', C_BOOL),  # 标识特征值是否加密;Identifies whether the characteristic value data is encrypted;
        ('byReserved', C_BYTE * 116),  # 保留;Reserved;
    ]

class NET_EULER_ANGLE(Structure):
    """
    姿态角数据; euler angle
    """
    _fields_ = [
        ('nPitch', c_int),      # 仰俯角;pitch
        ('nYaw', c_int),        # 偏航角;yaw
        ('nRoll', c_int),       # 翻滚角;roll
    ]

class NET_HUMAN_TEMPERATURE_INFO(Structure):
    """
    人温度信息; Information of human body temperature
    """
    _fields_ = [
        ('dbTemperature', c_double),        # 温度;Temperature
        ('emTemperatureUnit', c_int),       # 温度单位，参考EM_HUMAN_TEMPERATURE_UNIT;Temperature unit,refer to EM_HUMAN_TEMPERATURE_UNIT
        ('bIsOverTemp', c_int),             # 
        ('bIsUnderTemp', c_int),            # 
        ('bReserved', c_ubyte * 132),       # 预留字段;Reserved
    ]

class NET_FACE_ORIGINAL_SIZE(Structure):
    """
    算法人脸分析时的实际人脸图片尺寸
    Actual face image size during algorithm face analysis
    """
    _fields_ = [
        ('nWidth', C_UINT),  # 人脸图片宽度;Width;
        ('nHeight', C_UINT),  # 人脸图片高;Height;
    ]

class DEV_EVENT_FACEDETECT_INFO(Structure):
    """
    事件类型FACEDETECT(人脸检测事件)对应的数据块描述信息; the describe of FACEDETECT's data
    """
    _fields_ = [
        ('nChannelID', c_int),                          # 通道号；channel ID
        ('szName', c_char * 128),                       # 事件名称;event name
        ('bReserved1', c_char * 4),                     # 字节对齐;byte alignment
        ('PTS', c_double),                              # 时间戳(单位是毫秒);PTS(ms)
        ('UTC', NET_TIME_EX),                           # 事件发生的时间;the event happen time
        ('nEventID', c_int),                            # 事件ID;event ID
        ('stuObject', SDK_MSG_OBJECT),                  # 检测到的物体;have being detected object
        ('stuFileInfo', SDK_EVENT_FILE_INFO),           # 事件对应文件信息;event file info
        ('bEventAction', c_ubyte),                      # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;Event action: 0 means pulse event,1 means continuous event's begin,2means continuous event's end;
        ('reserved', c_ubyte * 2),                      # 保留字节;reserved
        ('byImageIndex', c_ubyte),                      # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0
        ('nDetectRegionNum', c_int),                    # 规则检测区域顶点数;detect region point number
        ('DetectRegion', SDK_POINT * 20),               # 规则检测区域;detect region
        ('dwSnapFlagMask', C_DWORD),                    # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON
        ('szSnapDevAddress', c_char * 260),             # 抓拍当前人脸的设备地址,如：滨康路37号;snapshot current face device address
        ('nOccurrenceCount', c_uint),                   # 事件触发累计次数;event trigger accumilated times
        ('emSex', c_int),                               # 性别，参考EM_DEV_EVENT_FACEDETECT_SEX_TYPE;sex type,refer to EM_DEV_EVENT_FACEDETECT_SEX_TYPE
        ('nAge', c_ubyte),                              # 年龄,-1表示该字段数据无效;age, invalid if it is -1
        ('nFeatureValidNum', c_uint),                   # 人脸特征数组有效个数,与 emFeature 结合使用;invalid number in array emFeature
        ('emFeature', c_uint * 32),                     # 人脸特征数组,与 nFeatureValidNum 结合使用，参考EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE;human face features,refer to EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE
        ('nFacesNum', c_int),                           # 指示stuFaces有效数量;number of stuFaces
        ('stuFaces', NET_FACE_INFO * 10),               # 多张人脸时使用,此时没有Object;when nFacesNum > 0, stuObject invalid
        ('stuIntelliCommInfo', EVENT_INTELLI_COMM_INFO),# 智能事件公共信息;public info
        ('szReserved1', c_char * 4),                    # Reserved
        ('emEye', c_int),                               # 眼睛状态，参考EM_EYE_STATE_TYPE;eyes state,refer to EM_EYE_STATE_TYPE
        ('emMouth', c_int),                             # 嘴巴状态，参考EM_MOUTH_STATE_TYPE;mouth state,refer to EM_MOUTH_STATE_TYPE
        ('emMask', c_int),                              # 口罩状态，参考EM_MASK_STATE_TYPE;mask state,refer to EM_MASK_STATE_TYPE
        ('emBeard', c_int),                             # 胡子状态，参考EM_BEARD_STATE_TYPE;beard state,refer to EM_BEARD_STATE_TYPE
        ('nAttractive', c_int),                         # 魅力值, -1表示无效, 0未识别，识别时范围1-100,得分高魅力高;Attractive value, -1: invalid, 0:no disringuish，range: 1-100, the higher value, the higher charm
        ('szUID', c_char * 32),                         # 抓拍人员写入数据库的唯一标识符;The unique identifier of the snap person to write to the database
        ('bReserved2', C_BYTE*4),
        ('stuFeatureVector', NET_FEATURE_VECTOR),       # 特征值信息;Feature data information
        ('szFeatureVersion', c_char * 32),              # 特征值算法版本;The version of the feature data algorithm
        ('emFaceDetectStatus', c_int),                  # 人脸在摄像机画面中的状态，参考EM_FACE_DETECT_STATUS;The status of person in camera picture,refer to EM_FACE_DETECT_STATUS
        ('stuFaceCaptureAngle', NET_EULER_ANGLE),       # 人脸在抓拍图片中的角度信息, nPitch:抬头低头的俯仰角, nYaw左右转头的偏航角, nRoll头在平面内左偏右偏的翻滚角;euler angle of face in the capture picture, nPitch:pitch of the head, nYaw: yaw of the head, nRoll:roll of the head
                                                        # 角度值取值范围[-90,90], 三个角度值都为999表示此角度信息无效;range of the angle value is [-90,90], stuFaceCaptureAngle is invalid if the three angles are 999.
        ('dHumanSpeed', c_double),                      # 人的运动速度, km/h;human speed, km/h
        ('nFaceAlignScore', c_int),                     # 人脸对齐得分分数,范围 0~10000,-1为无效值;The score of face picture align.The range is 0~10000,-1 is invalid
        ('nFaceClarity', c_int),                        # 人脸清晰度分数,范围 0~10000,-1为无效值;The score of face picture clarity.The range is 0~10000,-1 is invalid
        ('bHumanTemperature', c_int),                   # 人温度信息是否有效;Whether the information of human body temperature is valid
        ('stuHumanTemperature', NET_HUMAN_TEMPERATURE_INFO),        # 人温度信息, bHumanTemperature为TURE时有效;Information of human body temperature, It is valid whne bHumanTemperature is TURE
        ('szCameraID', c_char * 64),                    # 国标编码;GB encoding;
        ('stuResolution', SDK_RESOLUTION_INFO),         # 对应图片的分辨率;picture resolution;
        ('stuOriginalSize', NET_FACE_ORIGINAL_SIZE),    # 算法人脸分析时的实际人脸尺寸. 宽高为0是无效;Actual face image size during algorithm face analysis.;
        ('emGlass', C_ENUM),                            # 戴眼镜状态 Refer: EM_GLASS_STATE_TYPE;Wearing glasses state Refer: EM_GLASS_STATE_TYPE;
        ('emHat', C_ENUM),                              # 帽子状态 Refer: EM_HAT_STYLE;Hat state Refer: EM_HAT_STYLE;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),      # 事件公共扩展字段结构体;Event public extension field structure;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX3)), # 图片信息数组;Picture information;
        ('nImageInfoNum', c_int),                       # 图片信息个数;Picture number;
        ('bReserved', C_BYTE * (392 - sizeof(c_void_p))),  # 保留字节,留待扩展;Reserved;
    ]

class FACERECOGNITION_PERSON_INFO(Structure):
    """
    人员信息; person info
    """
    _fields_ = [
        ('szPersonName', c_char * 16),      # 姓名,此参数作废；name
        ('wYear', c_ushort),                # 出生年,作为查询条件时,此参数填0,则表示此参数无效;birth year
        ('byMonth', c_ubyte),               # 出生月,作为查询条件时,此参数填0,则表示此参数无效;birth month
        ('byDay', c_ubyte),                 # 出生日,作为查询条件时,此参数填0,则表示此参数无效;birth day
        ('szID', c_char * 32),              # 人员唯一标示(证件号码,工号,或其他编号);the unicle ID for the person
        ('bImportantRank', c_ubyte),        # 人员重要等级,1~10,数值越高越重要,作为查询条件时,此参数填0,则表示此参数无效;importance level,1~10,the higher value the higher level
        ('bySex', c_ubyte),                 # 性别,1-男,2-女,作为查询条件时,此参数填0,则表示此参数无效;sex, 0-man, 1-female
        ('wFacePicNum', c_ushort),          # 图片张数;picture number
        ('szFacePicInfo', SDK_PIC_INFO * 48),  # 当前人员对应的图片信息;picture info
        ('byType', c_ubyte),                # 人员类型,详见 EM_PERSON_TYPE;Personnel types, see EM_PERSON_TYPE
        ('byIDType', c_ubyte),              # 证件类型,详见 EM_CERTIFICATE_TYPE;Document types, see EM_CERTIFICATE_TYPE
        ('byGlasses', c_ubyte),             # 是否戴眼镜，0-未知 1-不戴 2-戴;Whether wear glasses or not,0-unknown,1-not wear glasses,2-wear glasses
        ('byAge', c_ubyte),                 # 年龄,0表示未知;Age,0 means unknown
        ('szProvince', c_char * 64),        # 省份;flag(by bit),see NET_RESERVED_COMMON;province
        ('szCity', c_char * 64),            # 城市;snapshot current face device address;city
        ('szPersonNameEx', c_char * 64),    # 姓名,因存在姓名过长,16字节无法存放问题,故增加此参数,;Name, the name is too long due to the presence of 16 bytes can not be Storage problems, the increase in this parameter
        ('szUID', c_char * 32),             # 人员唯一标识符,首次由服务端生成,区别于ID字段,修改,删除操作时必填;person unique ID
        ('szCountry', c_char * 3),          # 国籍,符合ISO3166规范;country
        ('byIsCustomType', c_ubyte),        # 人员类型是否为自定义: 0 使用Type规定的类型 1 自定义,使用szPersonName字段;using person type: 0 using byType, 1 using szPersonName
        ('pszComment', c_char_p),           # 备注信息, 用户自己申请内存的情况时;comment info, when the memory is alloced by user,
                                                # 下方bCommentLen需填写对应的具体长度值，推荐长度 NET_COMMENT_LENGTH;the value of bCommentLen needs to be filled in，recommended length is NET_COMMENT_LENGTH
        ('pszGroupID', c_char_p),           # 人员所属组ID, 用户自己申请内存的情况时;group ID, when the memory is alloced by user,
                                                # 下方bGroupIdLen需填写对应的具体长度值，推荐长度 NET_GROUPID_LENGTH;the value of bGroupIdLen needs to be filled in，recommended length is NET_GROUPID_LENGTH
        ('pszGroupName', c_char_p),         # 人员所属组名, 用户自己申请内存的情况时;group name, when the memory is alloced by user,
                                            # 下方bGroupNameLen需填写对应的具体长度值，推荐长度 NET_GROUPNAME_LENGTH;the value of bGroupNameLen needs to be filled in，recommended length is NET_GROUPNAME_LENGTH
        ('pszFeatureValue', c_char_p),      # 人脸特征, 用户自己申请内存的情况时;the face feature , when the memory is alloced by user,
                                            # 下方bFeatureValueLen需填写对应的具体长度值，推荐长度 NET_FEATUREVALUE_LENGTH;the value of bFeatureValueLen needs to be filled in，recommended length is NET_FEATUREVALUE_LENGTH
        ('bGroupIdLen', c_ubyte),           # pszGroupID的长度;len of pszGroupID
        ('bGroupNameLen', c_ubyte),         # pszGroupName的长度;len of pszGroupName
        ('bFeatureValueLen', c_ubyte),      # pszFeatureValue的长度;len of pszFeatureValue
        ('bCommentLen', c_ubyte),           # pszComment的长度;len of pszComment
        ('emEmotion', c_int),               # 表情，参考EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE;Emotion,refer to EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE
    ]

class CUSTOM_PERSON_INFO(Structure):
    """
    注册人员信息扩展结构体; extension of registered personnel information
    """
    _fields_ = [
        ('szPersonInfo', c_char * 64),      # 人员扩展信息;personnel extension information
        ('byReserved', c_ubyte * 124),      # 保留字节;Reserved bytes
    ]

class NET_FACE_PIC_INFO(Structure):
    """
    人脸图片信息
    Face picture information
    """
    _fields_ = [
        ('dwOffSet', C_DWORD),  # 文件在二进制数据块中的偏移位置, 单位:字节;Offset position of file in binary data block, unit: byte;
        ('dwFileLenth', C_DWORD),  # 文件大小, 单位:字节;File size in bytes;
        ('dwWidth', C_DWORD),  # 图片宽度, 单位:像素;Picture width in pixels;
        ('dwHeight', C_DWORD),  # 图片高度, 单位:像素;Picture height in pixels;
        ('bIsDetected', C_BOOL),  # 图片是否算法检测出来的检测过的提交识别服务器时,则不需要再时检测定位抠图,1:检测过的,0:没有检测过;Whether the image is detected by algorithm. When a detected server is submittedor identification, it is not necessary to detect the location matting again.TRUE: detected, FALSE: not detected;
        ('nFilePathLen', c_int),  # 文件路径长度 既pszFilePath 的大小;File path length, it is the size of both pszfilepath;
        ('pszFilePath', POINTER(c_char)),  # 文件路径, 由用户申请空间, 作为输入条件时不需要;File path,Space requested by user. It is not required as input condition.;
        ('szPictureID', c_char * 32),  # 图片ID, 针对一人多人脸的情况, 用于区分不同人脸;Picture ID is used to distinguish different faces in the case of one person with multiple faces;
        ('emFeatureState', C_ENUM),  # 图片建模状态 Refer: EM_PERSON_FEATURE_STATE;Picture modeling status Refer: EM_PERSON_FEATURE_STATE;
        ('emFeatureErrCode', C_ENUM),  # 建模失败原因 Refer: EM_PERSON_FEATURE_ERRCODE;Modeling failure reason Refer: EM_PERSON_FEATURE_ERRCODE;
        ('emPicOperate', C_ENUM),  # 图片操作类型 Refer: EM_PIC_OPERATE_TYPE;Picture operation type Refer: EM_PIC_OPERATE_TYPE;
        ('bReserved', C_BYTE * 20),  # 预留字节;Reserved;
    ]

class NET_PERSON_FEATURE_VALUE_INFO(Structure):
    """
    人员特征信息
    Personnel characteristics information
    """
    _fields_ = [
        ('nOffset', C_UINT),  # 二进制数据块中的偏移值;Offset value in binary data block;
        ('nLength', C_UINT),  # 特征值大小;Eigenvalue size;
        ('byReserved', C_BYTE * 128),  # 保留字节;Reserved;
    ]

class NET_PERSON_FREQUENCY_INFO(Structure):
    """
    频次报警信息
    alarm frequency info
    """
    _fields_ = [
        ('emAlarmType', C_ENUM),  # 报警类型 Refer: EM_FREQUENCY_ALARM_TYPE;alarm Type Refer: EM_FREQUENCY_ALARM_TYPE;
        ('nTimes', c_int),  # 频次;frequency;
        ('szReserved', c_char * 128),  # 保留字节;Reserved;
    ]

class NET_A_FACERECOGNITION_CUSTOM_PASSER_BY_INFO(Structure):
    """
    人脸库路人信息
    Face database passerby information
    """
    _fields_ = [
        ('nStorageAddrChannel', c_int),  # 入库地点对应的通道号;storage address channel;
        ('nStoragePresetID', c_int),  # 入库地点(首次抓拍到的地点)对应的预置点号;storage address perset id;
        ('stuStorageTime', NET_TIME),  # 入库时间;storage time;
        ('stuLastAppearTime', NET_TIME),  # 最近出现时间;last appear time;
        ('nLastAppearAddrChannel', c_int),  # 最近出现地点对应的通道号;last appear address channel;
        ('nLastAppearPresetID', c_int),  # 最近出现地点对应的预置点号(球机预置点从1开始);last appear address perset id;
        ('nOccurrenceNumber', C_UINT),  # 出现次数;occurrence number;
        ('szReserved', c_char * 1020),  # 保留字段;Reserved;
    ]

class FACERECOGNITION_PERSON_INFOEX(Structure):
    """
    人员信息扩展结构体; expansion of  personnel information
    """
    _fields_ = [
        ('szPersonName', c_char * 64),      # 姓名；name
        ('wYear', c_ushort),                # 出生年,作为查询条件时,此参数填0,则表示此参数无效;birth year
        ('byMonth', c_ubyte),               # 出生月,作为查询条件时,此参数填0,则表示此参数无效;birth month
        ('byDay', c_ubyte),                 # 出生日,作为查询条件时,此参数填0,则表示此参数无效;birth day
        ('bImportantRank', c_ubyte),        # 人员重要等级,1~10,数值越高越重要,作为查询条件时,此参数填0,则表示此参数无效;importance level,1~10,the higher value the higher level
        ('bySex', c_ubyte),                 # 性别,1-男,2-女,作为查询条件时,此参数填0,则表示此参数无效;sex, 0-man, 1-female
        ('szID', c_char * 32),              # 人员唯一标示(证件号码,工号,或其他编号);the unicle ID for the person
        ('wFacePicNum', c_ushort),          # 图片张数;picture number
        ('szFacePicInfo', SDK_PIC_INFO * 48),  # 当前人员对应的图片信息;picture info
        ('byType', c_ubyte),                # 人员类型,详见 EM_PERSON_TYPE;Personnel types, see EM_PERSON_TYPE
        ('byIDType', c_ubyte),              # 证件类型,详见 EM_CERTIFICATE_TYPE;Document types, see EM_CERTIFICATE_TYPE
        ('byGlasses', c_ubyte),             # 是否戴眼镜，0-未知 1-不戴 2-戴;Whether wear glasses or not,0-unknown,1-not wear glasses,2-wear glasses
        ('byAge', c_ubyte),                 # 年龄,0表示未知;Age,0 means unknown
        ('szProvince', c_char * 64),        # 省份;flag(by bit),see NET_RESERVED_COMMON;province
        ('szCity', c_char * 64),            # 城市;snapshot current face device address;city
        ('szUID', c_char * 32),             # 人员唯一标识符,首次由服务端生成,区别于ID字段,修改,删除操作时必填;person unique ID
        ('szCountry', c_char * 3),          # 国籍,符合ISO3166规范;country
        ('byIsCustomType', c_ubyte),        # 人员类型是否为自定义: 0 使用Type规定的类型 1 自定义,使用szCustomType字段;using person type: 0 using byType, 1 using szCustomType
        ('szCustomType', c_char * 16),      # 人员自定义类型; type of person
        ('szComment', c_char * 100),        # 备注信息;comment info
        ('szGroupID', c_char * 64),         # 人员所属组ID;group ID
        ('szGroupName', c_char * 128),      # 人员所属组名, 用户自己申请内存的情况时;group name
        ('emEmotion', c_int),               # 表情，参考EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE;Emotion,refer to EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE
        ('szHomeAddress', c_char * 128),    # 注册人员家庭地址;home address of the person
        ('emGlassesType', c_int),           # 眼镜类型，参考EM_GLASSES_TYPE;glasses type,refer to EM_GLASSES_TYPE
        ('szReserved1', c_char * 4),        # Reserved
        ('emEye', c_int),                   # 眼睛状态，参考EM_EYE_STATE_TYPE;eye state,refer to EM_EYE_STATE_TYPE
        ('emMouth', c_int),                 # 嘴巴状态，参考EM_MOUTH_STATE_TYPE;mouth state,refer to EM_MOUTH_STATE_TYPE
        ('emMask', c_int),                  # 口罩状态，参考EM_MASK_STATE_TYPE;mask state,refer to EM_MASK_STATE_TYPE
        ('emBeard', c_int),                 # 胡子状态，参考EM_BEARD_STATE_TYPE;beard state,refer to EM_BEARD_STATE_TYPE
        ('nAttractive', c_int),             # 魅力值, -1表示无效, 0未识别，识别时范围1-100,得分高魅力高;attractive, -1:invalid, 0:unknown，1-100
        ('emFeatureState', c_int),          # 人员建模状态, 详见EM_PERSON_FEATURE_STATE;person feature state,refer to EM_PERSON_FEATURE_STATE
        ('bAgeEnable', c_int),              # 是否指定年龄段;age range is enabled
        ('nAgeRange', c_int * 2),           # 年龄范围;age range
        ('nEmotionValidNum', c_int),        # 人脸特征数组有效个数,与 emFeature 结合使用, 如果为0则表示查询所有表情;invalid number in array emEmotion, 0 means all emotion
        ('emEmotions', c_int * 32),         # 人脸特征数组,与 byFeatureValidNum 结合使用  设置查询条件的时候使用，参考EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE;human emotion  set the query condition，refer to EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE
        ('nCustomPersonInfoNum', c_int),    # 注册人员信息扩展个数;extension number of registered personnel information
        ('szCustomPersonInfo', CUSTOM_PERSON_INFO * 4),  # 注册人员信息扩展;extension of registered personnel information
        ('emRegisterDbType', c_int),        # 注册库类型，参考EM_REGISTER_DB_TYPE;type of register face DB
        ('stuEffectiveTime', NET_TIME),     # 有效期时间;effective time
        ('emFeatureErrCode', c_int),        # 建模失败原因，参考EM_PERSON_FEATURE_ERRCODE;error code of person feature,refer to EM_PERSON_FEATURE_ERRCODE
        ('wFacePicNumEx', C_DWORD),         # 人脸图片张数;Number of face pictures;
        ('szFacePicInfoEx', NET_FACE_PIC_INFO * 6),                 # 当前人员对应的图片信息;The picture information corresponding to the current person. It is an extension of szFacePicInfo. This field will be used first in the future;
        ('stuPersonFeatureValue', NET_PERSON_FEATURE_VALUE_INFO),   # 人员特征信息;Personnel characteristics information;
        ('bFrozenStatus', C_BOOL),          # 人员冻结状态;person frozen status;
        ('szReserved', c_char * 4),         # 保留字节;Reserved bytes;
        ('stuFrequencyInfo', NET_PERSON_FREQUENCY_INFO),            # 频次报警信息;alarm frequency info;
        ('szUUID', c_char * 64),            # 平台唯一标识人脸字段，区别于UID,IVSS根据faceRecognitionServer.getCaps能力，SupportIDFromServer值为true时，支持UUID有效;The platform uniquely identifies the face field, which is different from UID. According to the capability of faceRecognitionServer.getCaps, IVSS supports UUID when the value of SupportIDFromServer is true.;
        ('pstuCustomPasserbyInfo', POINTER(NET_A_FACERECOGNITION_CUSTOM_PASSER_BY_INFO)),   # 路人信息,由用户申请内存,一次申请一个;passer info,the space application by the user,Apply one at a time;
        ('byReserved', C_BYTE * (188 - sizeof(c_void_p))),  # 保留字节;Reserved bytes;
    ]

class NET_FACE_MATCH_OPTIONS(Structure):
    """
    人脸匹配信息结构体; Face Matching Options
    """
    _fields_ = [
        ('dwSize', C_DWORD),                            # 结构体大小; Struct size
        ('nMatchImportant', c_uint),                    # 人员重要等级,1~10,数值越高越重要,(查询重要等级大于等于此等级的人员); Important level 1 to 10 staff, the higher the number the more important (check important level greater than or equal to this level of staff)
        ('emMode', C_ENUM),                             # 人脸比对模式,详见EM_FACE_COMPARE_MODE; Face comparison mode, see EM_FACE_COMPARE_MODE
        ('nAreaNum', c_int),                            # 人脸区域个数; Face the number of regional
        ('szAreas', C_ENUM * 8),                        # 人脸区域组合,emMode为EM_FACE_COMPARE_MODE.AREA时有效,详见EM_FACE_AREA_TYPE; Regional groupings of people face is EM_FACE_COMPARE_MODE.AREA effective when emMode, see EM_FACE_AREA_TYPE
        ('nAccuracy', c_int),                           # 识别精度(取值1~10,随着值增大,检测精度提高,检测速度下降。最小值为1 表示检测速度优先,最大值为10表示检测精度优先。 暂时只对人脸检测有效); Recognition accuracy (ranging from 1 to 10, with the value increases, the detection accuracy is improved, the detection rate of decline. Minimum value of 1 indicates the detection speed priority, the maximum is 10, said detection accuracy preferred. Temporarily valid only for face detection)
        ('nSimilarity', c_int),                         # 相似度(必须大于该相识度才报告;百分比表示,1~100); Similarity (must be greater than the degree of acquaintance before the report; expressed as a percentage, from 1 to 100)
        ('nMaxCandidate', c_int),                       # 报告的最大候选个数(根据相似度进行排序,取相似度最大的候选人数报告); Reported the largest number of candidate (based on similarity to sort candidates to take the maximum number of similarity report)
        ('emQueryMode', C_ENUM),                        # 以图搜图查询模式,详见 EM_FINDPIC_QUERY_MODE; The query mode of searching face database by picture, see EM_FINDPIC_QUERY_MODE
        ('emOrdered', C_ENUM),                          # 以图搜图结果上报排序方式,详见 EM_FINDPIC_QUERY_ORDERED; The sort order of the result about searching face database by picture, see EM_FINDPIC_QUERY_ORDERED
    ]

class NET_FACE_FILTER_CONDTION(Structure):
    """
    查询过滤条件; Query filters
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                # 结构体大小; Struct size
        ('stStartTime', NET_TIME),                          # 开始时间; Start time
        ('stEndTime', NET_TIME),                            # 结束时间; End Time
        ('szMachineAddress', c_char * 260),                 # 地点,支持模糊匹配; Place to support fuzzy matching
        ('nRangeNum', c_int),                               # 实际数据库个数; The actual number of database
        ('szRange', C_BYTE * 8),                            # 待查询数据库类型,详见 EM_FACE_DB_TYPE; To query the database type, see EM_FACE_DB_TYPE
        ('emFaceType', C_ENUM),                             # 待查询人脸类型,详见 EM_FACERECOGNITION; Face to query types, see EM_FACERECOGNITION
        ('nGroupIdNum', c_int),                             # 人员组数; staff group
        ('szGroupId', c_char * 64 * 128),                   # 人员组ID; staff group ID
        ('stBirthdayRangeStart', NET_TIME),                 # 生日起始时间; start birthday time
        ('stBirthdayRangeEnd', NET_TIME),                   # 生日结束时间; end birthday time
        ('byAge', C_BYTE * 2),                              # 年龄区间，当byAge[0]=0与byAge[1]=0时，表示查询全年龄; Age range, When byAge[0] is 0 and byAge[1] is 0, it means query all age
        ('byReserved', C_BYTE * 2),                         # 保留字节对齐; Reserved
        ('emEmotion', C_ENUM * 8),                          # 表情条件,详见 EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE; Emotion, see EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE
        ('nEmotionNum', c_int),                             # 表情条件的个数; Emotion num
        ('nUIDNum', c_int),                                 # 人员唯一标识数; UID num
        ('szUIDs', c_char * 64 *32),                        # 人员唯一标识列表; UID list
        ('nUUIDNum', c_int),                                # 平台端人员唯一标识数;UUID num;
        ('szUUIDs', c_char * 64 * 32),                      # 平台端人员唯一标识列表，根据faceRecognitionServer.getCaps获取到的能力是否存在字段SupportIDFromServer且值为true时有效;A list of the unique identifiers of the personnel on the platform, according to whether the ability obtained by faceRecognitionServer.getCaps has the field SupportIDFromServer and the value is true, it is valid;
        ('bIsUsingRealUTCTime', C_BOOL),                    #  是否使用UTC格式的开始、结束时间;Whether to use the start time and end time in UTC format;
        ('stuStartTimeRealUTC', NET_TIME),                  # 开始时间（UTC时间格式）; Start time (UTC time format)
        ('stuEndTimeRealUTC', NET_TIME),                    # 结束时间（UTC时间格式）备注：与StartTimeRealUTC配对使用;End Time (UTC time format) Note: This parameter is paired with StartTimeRealUTC
        ('bIsUsingRegisterStorageTime', C_BOOL),            # 是否使用注册库人员的开始、结束时间;Whether to use the start and end time of the registration database personnel;
        ('stuStartRegisterStorageTime', NET_TIME),          # 注册库人员的入库开始时间; Starting time for registration of personnel in the repository
        ('stuEndRegisterStorageTime', NET_TIME),            # 注册库人员的入库结束时间;End time of registration of personnel in the repository
        ('bIsUsingModifyTime', C_BOOL),                     # 是否使用注册库人员的修改开始、结束时间;Whether to use the modification start and end time of the registration database personnel;
        ('stuStartModifyTime', NET_TIME),                   # 注册库人员的修改开始时间; Starting time for modifying the registration database personnel
        ('stuEndModifyTime', NET_TIME),                     # 注册库人员的修改结束时间;End time of modification for registration database personnel
    ]

class NET_IN_STARTMULTIFIND_FACERECONGNITION(Structure):
    """
    CLIENT_StartMultiFindFaceRecognition 接口输入参数
    CLIENT_StartMultiFindFaceRecognition input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('pChannelID', POINTER(c_int)),  # 通道号;Channel ID;
        ('nChannelCount', c_int),  # 通道申请个数;number of channel;
        ('bPersonEnable', C_BOOL),  # 人员信息查询条件是否有效;Personnel information query is valid;
        ('stPerson', FACERECOGNITION_PERSON_INFO),  # 人员信息查询条件;Personnel information query;
        ('stMatchOptions', NET_FACE_MATCH_OPTIONS),  # 人脸匹配选项;Face Matching Options;
        ('stFilterInfo', NET_FACE_FILTER_CONDTION),  # 查询过滤条件;Query filters;
        ('pBuffer', POINTER(c_char)),  # 缓冲地址;Buffer address;
        ('nBufferLen', c_int),  # 缓冲数据长度;Buffer data length;
        ('bPersonExEnable', C_BOOL),  # 人员信息查询条件是否有效, 并使用人员信息扩展结构体;use stPersonInfoEx when bUsePersonInfoEx is true, otherwise use stPersonInfo;
        ('stPersonInfoEx', FACERECOGNITION_PERSON_INFOEX),  # 人员信息扩展;expansion of personnel information;
        ('emObjectType', C_ENUM),  # 搜索的目标类型 Refer: EM_OBJECT_TYPE;The type of object Refer: EM_OBJECT_TYPE;
        ('nChannelNum', c_int),  # 通道有效个数;Channel number;
        ('szChannelString', c_char * 512 * 32),  # 通道号;Channel ID
        ('nProcessType', c_int),  # 以图搜图类型, -1: 未知, 0: 特征值搜索, 1: SMD属性特征搜索 ; Map search type, - 1: Unknown, 0: Feature value search, 1: SMD attribute feature search;
        ('bIsUsingTaskID', C_BOOL),  # 是否使能订阅的TaskID字段;Whether the TaskID field of the subscription is enabled
        ('nTaskIDNum', c_int),  # 订阅的TaskID数组有效个数;Valid number of TaskID arrays subscribed to
        ('nTaskID', C_UINT * 128),              # 订阅的TaskID, bIsUsingTaskID为TRUE,nTaskIDNum为0表示订阅所有任务结果; For the TaskID of a subscription, bIsUsingTaskID is TRUE, and nTaskIDNum is 0, indicating the result of subscribing to all tasks
    ]

class NET_OUT_STARTMULTIFIND_FACERECONGNITION(Structure):
    """
    CLIENT_StartMultiFindFaceRecognition 接口输出参数
    CLIENT_StartMultiFindFaceRecognition output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nTotalCount', c_int),  # 返回的符合查询条件的记录个数-1表示总条数未生成,要推迟获取使用CLIENT_AttachFaceFindState接口状态;Record number of returns that match the query criteria;
        ('lFindHandle', C_LLONG),  # 查询句柄;Query handle;
        ('nToken', c_int),  # 获取到的查询令牌;The search token received;
    ]

class NET_CB_FACE_FIND_STATE(Structure):
    """
    人脸查询状态信息回调函数, lAttachHandle是CLIENT_AttachFaceFindState的返回值
    callback data
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nToken', c_int),  # 视频浓缩任务数据库主键ID;Video synopsis task database main key ID;
        ('nProgress', c_int),  # 正常取值范围：0-100,-1,表示查询token不存在(当订阅一个不存在或结束的查询时);Normal value: 0-100. 1=Searched token does not exist (When subscribe a search that does not exist or already finished);
        ('nCurrentCount', c_int),  # 目前符合查询条件的人脸数量;The human face amount that match current criteria;
    ]

class NET_IN_FACE_FIND_STATE(Structure):
    """
    CLIENT_AttachFaceFindState接口输入参数
    CLIENT_AttachFaceFindState interface parameter in
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小,必须填写;Structure size. Must fill in.;
        ('nTokenNum', c_int),  # 查询令牌数,为0时,表示订阅所有的查询任务;Search token. 0=subscribe all searched tasks.;
        ('nTokens', POINTER(c_int)),  # 查询令牌,由用户申请内存，大小为sizeof(int)*nTokenNum;Search toke,the space application by the user, apply to sizeof(int)*nTokenNum;
        ('cbFaceFindState', CB_FUNCTYPE(None, C_LLONG, C_LLONG, POINTER(NET_CB_FACE_FIND_STATE), c_int, C_LDWORD)),  # 回调函数;Call function;
        ('dwUser', C_LDWORD),  # 用户数据;User data;
    ]

class NET_OUT_FACE_FIND_STATE(Structure):
    """
    CLIENT_AttachFaceFindState接口输出参数
    CLIENT_AttachFaceFindState interface parameter in
    """
    _fields_ = [
        ('dwSize', C_DWORD),
    ]

class NET_IN_DOFIND_FACERECONGNITION(Structure):
    """
    CLIENT_DoFindFaceRecognition 接口输入参数
    CLIENT_DoFindFaceRecognition Interface input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('lFindHandle', C_LLONG),  # 查询句柄;Query handle;
        ('nBeginNum', c_int),  # 查询起始序号;Queries starting serial number;
        ('nCount', c_int),  # 当前想查询的记录条数;The current number of records you want to search for;
        ('emDataType', C_ENUM),  # 指定查询结果返回图片的格式 Refer: EM_NEEDED_PIC_RETURN_TYPE;the format of the image returned in the query results Refer: EM_NEEDED_PIC_RETURN_TYPE;
    ]

class SDK_PIC_INFO_EX3(Structure):
    """
    物体对应图片文件信息(包含图片路径); picture info
    """
    _fields_ = [
        ('dwOffSet', C_DWORD),          # 文件在二进制数据块中的偏移位置, 单位:字节;current picture file's offset in the binary file, byte
        ('dwFileLenth', C_DWORD),       # 文件大小, 单位:字节;current picture file's size, byte
        ('wWidth', c_ushort),           # 图片宽度, 单位:像素;picture width, pixel
        ('wHeight', c_ushort),          # 图片高度, 单位:像素;picture high, pixel
        ('szFilePath', c_char * 64),    # 文件路径; File path
        ('bIsDetected', c_ubyte),       # 图片是否算法检测出来的检测过的提交识别服务器时, 则不需要再时检测定位抠图,1:检测过的,0:没有检测过;When submit to the server, the algorithm has checked the image or not
        ('bReserved', c_ubyte * 11),    # 预留字段;Reserved
    ]

class CANDIDATE_INFO(Structure):
    """
    候选人员信息; cadidate person info
    """
    _fields_ = [
        ('stPersonInfo', FACERECOGNITION_PERSON_INFO),          # 人员信息;person info
                                                                    # 布控（禁止名单）库, 指布控库中人员信息；
                                                                    # 历史库, 指历史库中人员信息
                                                                    # 报警库, 指布控库的人员信息
        ('bySimilarity', c_ubyte),                              # 和查询图片的相似度,百分比表示,1~100;similarity
        ('byRange', c_ubyte),                                   # 人员所属数据库范围,详见EM_FACE_DB_TYPE; Range officer's database, see EM_FACE_DB_TYPE
        ('byReserved1', c_ubyte * 2),                           # 预留字段;Reserved
        ('stTime', NET_TIME),                                   # 当byRange为历史数据库时有效,表示查询人员出现的时间;When byRange historical database effectively, which means that the query time staff appeared
        ('szAddress', c_ubyte * 260),                           # 当byRange为历史数据库时有效,表示查询人员出现的地点;When byRange historical database effectively, which means that people place a query appears
        ('bIsHit', c_int),                                      # 是否有识别结果,指这个检测出的人脸在库中有没有比对结果;Is hit, means the result face has compare result in database
        ('stuSceneImage', SDK_PIC_INFO_EX3),                    # 人脸全景图;Scene Image
        ('nChannelID', c_int),                                  # 通道号;Channel Id
        ('byReserved', c_ubyte * 32),                           # 保留字节;Reserved bytes
    ]

class NET_HISTORY_HUMAN_IMAGE_INFO(Structure):
    """
    历史库人体图片信息; Image info of human in history data base
    """
    _fields_ = [
        ('nLength', c_int),             # 图片大小,单位:字节;Image, unit:byte
        ('nWidth', c_int),              # 图片宽度;Image width
        ('nHeight', c_int),             # 图片高度;Image height
        ('szFilePath', c_char * 260),   # 文件路径;Image path
    ]

class NET_HISTORY_HUMAN_INFO(Structure):
    """
    历史库人体信息; Human info in history data base
    """
    _fields_ = [
        ('emCoatColor', c_int),             # 上衣颜色,参考EM_CLOTHES_COLOR; Coat color,refer to EM_CLOTHES_COLOR
        ('emCoatType', c_int),              # 上衣类型，参考EM_COAT_TYPE; Coat type, refer to EM_COAT_TYPE
        ('emTrousersColor', c_int),         # 裤子颜色,参考EM_CLOTHES_COLOR; Trousers color,refer to EM_CLOTHES_COLOR
        ('emTrousersType', c_int),          # 裤子类型，参考EM_TROUSERS_TYPE; Trousers type,refer to EM_TROUSERS_TYPE
        ('emHasHat', c_int),                # 是否戴帽子，参考EM_HAS_HAT; Has hat or not,refer to EM_HAS_HAT
        ('emHasBag', c_int),                # 是否带包，参考EM_HAS_BAG; Has bag or not,refer to EM_HAS_BAG
        ('stuBoundingBox', NET_RECT),       # 包围盒(8192坐标系); Bounding box
        ('nAge', c_int),                    # 年龄;Age
        ('emSex', c_int),                   # 性别，参考EM_SEX_TYPE;Sex,refer to EM_SEX_TYPE
        ('emAngle', c_int),                 # 角度，参考EM_ANGLE_TYPE;Angle,refer to EM_ANGLE_TYPE
        ('emHasUmbrella', c_int),           # 是否打伞，参考EM_HAS_UMBRELLA;Has umbrella or not,refer to EM_HAS_UMBRELLA
        ('emBag', c_int),                   # 包类型，参考EM_BAG_TYPE;Bag type,refer to EM_BAG_TYPE
        ('emUpperPattern', c_int),          # 上半身衣服图案，参考EM_CLOTHES_PATTERN;Upper pattern,refer to EM_CLOTHES_PATTERN
        ('emHairStyle', c_int),             # 头发样式，参考EM_HAIR_STYLE;Hair style,refer to EM_HAIR_STYLE
        ('emCap', c_int),                   # 帽类型，参考EM_CAP_TYPE;Cap type,refer to EM_CAP_TYPE
        ('emHasBackBag', c_int),            # 是否有背包，参考EM_HAS_BACK_BAG;Has back bag or not,refer to EM_HAS_BACK_BAG
        ('emHasCarrierBag', c_int),         # 是否带手提包，参考EM_HAS_CARRIER_BAG;Has carrier bag or not,refer to EM_HAS_CARRIER_BAG
        ('emHasShoulderBag', c_int),        # 是否有肩包，参考EM_HAS_SHOULDER_BAG;Has shoulder bag or not,refer to EM_HAS_SHOULDER_BAG
        ('emMessengerBag', c_int),          # 是否有斜跨包，参考EM_HAS_MESSENGER_BAG;Has messenger bag or not,refer to EM_HAS_MESSENGER_BAG
        ('stuImageInfo', NET_HISTORY_HUMAN_IMAGE_INFO),         # 人体图片信息;Human image info
        ('stuFaceImageInfo', NET_HISTORY_HUMAN_IMAGE_INFO),     # 人脸图片信息;Face image info
        ('byReserved', c_ubyte * 256),      # 保留字节;Reserved bytes
    ]


class CANDIDATE_INFOEX(Structure):
    """
    候选人员信息扩展结构体; cadidate person info
    """
    _fields_ = [
        ('stPersonInfo', FACERECOGNITION_PERSON_INFOEX),        # 人员信息;person info
                                                                    # 布控（禁止名单）库, 指布控库中人员信息；
                                                                    # 历史库, 指历史库中人员信息
                                                                    # 报警库, 指布控库的人员信息
        ('bySimilarity', c_ubyte),                              # 和查询图片的相似度,百分比表示,1~100;similarity
        ('byRange', c_ubyte),                                   # 人员所属数据库范围,详见EM_FACE_DB_TYPE; Range officer's database, see EM_FACE_DB_TYPE
        ('byReserved1', c_ubyte * 2),                           # 预留字段;Reserved
        ('stTime', NET_TIME),                                   # 当byRange为历史数据库时有效,表示查询人员出现的时间;When byRange historical database effectively, which means that the query time staff appeared
        ('szAddress', c_ubyte * 260),                           # 当byRange为历史数据库时有效,表示查询人员出现的地点;When byRange historical database effectively, which means that people place a query appears
        ('bIsHit', c_int),                                      # 是否有识别结果,指这个检测出的人脸在库中有没有比对结果;Is hit, means the result face has compare result in database
        ('stuSceneImage', SDK_PIC_INFO_EX3),                    # 人脸全景图;Scene Image
        ('nChannelID', c_int),                                  # 通道号;Channel Id
        ('szFilePathEx', c_char * 256),                         # 文件路径;File path
        ('stuHistoryHumanInfo', NET_HISTORY_HUMAN_INFO),        # 历史库人体信息;Human info in history data base
        ('szChannelString', c_char * 32),                       # 视频通道号;Video channel id;
        ('byReserved', C_BYTE * 104),                           # 保留字节;Reserved byte;
    ]

class NET_OUT_DOFIND_FACERECONGNITION(Structure):
    """
    CLIENT_DoFindFaceRecognition接口输出参数
    CLIENT_DoFindFaceRecognitionInterface output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nCadidateNum', c_int),  # 实际返回的候选信息结构体个数;The actual number of candidate information structure returned;
        ('stCadidateInfo', CANDIDATE_INFO * 20),  # 候选信息数组;An array of candidate information;
        ('pBuffer', POINTER(c_char)),  # 缓冲地址;Buffer address;
        ('nBufferLen', c_int),  # 缓冲数据长度;Buffer data length;
        ('bUseCandidatesEx', C_BOOL),  # 是否使用候选对象扩展结构体,若为TRUE, 则表示使用stuCandidatesEx, 且stuCandidates无效, 否则相反;whether or not to use stuCandidatesExstuCandidatesEx is effective and stuCandidates is invalid when the bUseCandidatesEx is TRUE, otherwise, on the contrary;
        ('nCadidateExNum', c_int),  # 实际返回的候选信息结构体个数;the actual return number of stuCandidatesEx;
        ('stuCandidatesEx', CANDIDATE_INFOEX * 20),  # 当前人脸匹配到的候选对象信息, 实际返回个数同nCandidateNum;the expansion of candidate information;
    ]

class NET_FACE_DATA(Structure):
    """
    人脸数据; the data of face
    """
    _fields_ = [
        ('emSex', c_int),               # 性别，参考EM_DEV_EVENT_FACEDETECT_SEX_TYPE;sex type,refer to EM_DEV_EVENT_FACEDETECT_SEX_TYPE
        ('nAge', c_int),                # 年龄,-1表示该字段数据无效;age, invalid if it is -1
        ('nFeatureValidNum', c_uint),   # 人脸特征数组有效个数,与 emFeature 结合使用; invalid number in array emFeature
        ('emFeature', c_int * 32),      # 人脸特征数组,与 nFeatureValidNum 结合使用，参考EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE;human face features,refer to EM_DEV_EVENT_FACEDETECT_FEATURE_TYPE
        ('szReserved1', c_char * 4),    # Reserved
        ('emEye', c_int),               # 眼睛状态，参考EM_EYE_STATE_TYPE;eyes state,refer to EM_EYE_STATE_TYPE
        ('emMouth', c_int),             # 嘴巴状态，参考EM_MOUTH_STATE_TYPE;mouth state,refer to EM_MOUTH_STATE_TYPE
        ('emMask', c_int),              # 口罩状态，参考EM_MASK_STATE_TYPE;mask state,refer to EM_MASK_STATE_TYPE
        ('emBeard', c_int),             # 胡子状态，参考EM_BEARD_STATE_TYPE;beard state,refer to EM_BEARD_STATE_TYPE
        ('nAttractive', c_int),         # 魅力值, -1表示无效, 0未识别，识别时范围1-100,得分高魅力高;Attractive value, -1: invalid, 0:no disringuish，range: 1-100, the higher value, the higher charm
        ('bReserved1', C_BYTE*4),
        ('stuFaceCaptureAngle', NET_EULER_ANGLE),  # 人脸在抓拍图片中的角度信息,角度值取值范围[-90,90], 三个角度值都为999表示此角度信息无效; euler angle of face in the capture picture,range of the angle value is [-90,90], stuFaceCaptureAngle is invalid if the three angles are 999.
        ('nFaceQuality', c_uint),       # 人脸抓拍质量分数;quality about capture picture
        ('nFaceAlignScore', c_int),     # 人脸对齐得分分数,范围 0~10000,-1为无效值;The score of face picture align.The range is 0~10000,-1 is invalid
        ('nFaceClarity', c_int),        # 人脸清晰度分数,范围 0~10000,-1为无效值;The score of face picture clarity.The range is 0~10000,-1 is invalid
        ('dbTemperature', c_double),    # 温度, bAnatomyTempDetect 为TRUE时有效;Temperature, it is valid when bAnatomyTempDetect is true
        ('bAnatomyTempDetect', c_int),  # 是否人体测温;Is anatomy temperature detection
        ('emTemperatureUnit', c_int),   # 温度单位, bAnatomyTempDetect 为TRUE时有效,参考EM_HUMAN_TEMPERATURE_UNIT;Temperature unit, it is valid when bAnatomyTempDetect is true,refer to EM_HUMAN_TEMPERATURE_UNIT
        ('bIsOverTemp', c_int),         # 
        ('bIsUnderTemp', c_int),        # 
        ('stuOriginalSize', NET_FACE_ORIGINAL_SIZE),    # 算法人脸分析时的实际人脸图片尺寸, 宽高为0时无效;Actual face image size during algorithm face analysis.;
        ('emGlass', C_ENUM),            # 戴眼镜状态 Refer: EM_GLASS_STATE_TYPE;Wearing glasses state Refer: EM_GLASS_STATE_TYPE;
        ('bReserved', C_BYTE * 64),     # 保留字节,留待扩展.;Reserved;
    ]

class NET_PASSERBY_INFO(Structure):
    """
    路人信息; passerby info
    """
    _fields_ = [
        ('szPasserbyUID', c_char * 32),             # 路人唯一标识符;The unique identifier of the passerby to write to the database
        ('szPasserbyGroupId', c_char * 64),         # 路人库ID;Passerby group ID
        ('szPasserbyGroupName', c_char * 128),      # 路人库名称;Passerby group name
        ('byReserved', c_ubyte * 128),              # 保留;Reserved
    ]


class NET_FACECOMPARISON_PTZ_INFO(Structure):
    """
    人脸比对事件触发对应球机信息; Face matching event triggers corresponding ball machine information
    """
    _fields_ = [
        ('szPresetName', c_char * 64),             # 球机抓拍到人脸时预置点名称;Preset point name when the ball machine captures the face
        ('dwPresetNumber', C_DWORD),         # 球机抓拍到人脸时预置点编号;Preset point number when the ball machine captures the face
        ('byReserved1', c_ubyte * 4),           # 字节对齐;Byte alaginment
        ('byReserved', c_ubyte * 256),           # 保留字节;Reserved
    ]

class NET_CUSTOM_PROJECTS_INFO(Structure):
    """
    信息; info
    """
    _fields_ = [
        ('stuGPSInfo', NET_GPS_INFO),             # GPS位置信息;GPS info
        ('stuFaceComparisonPTZInfo', NET_FACECOMPARISON_PTZ_INFO),         # 人脸比对事件触发对应球机信息;Face matching event triggers corresponding ball machine information
        ('szPlateNumber', c_char * 64),           # 人脸比对时车牌信息;License plate information in face comparison
        ('byReserved', c_ubyte * 1024),           # 保留;Reserved
    ]


class DEV_EVENT_FACERECOGNITION_INFO(Structure):
    """
    事件类型FACERECOGNITION(目标识别)对应的数据块描述信息; the describe of FACERECOGNITION's data
    """
    _fields_ = [
        ('nChannelID', c_int),                          # 通道号；channel ID
        ('szName', c_char * 128),                       # 事件名称;event name
        ('nEventID', c_int),                            # 事件ID;event ID
        ('UTC', NET_TIME_EX),                           # 事件发生的时间;the event happen time
        ('stuObject', SDK_MSG_OBJECT),                  # 检测到的物体;have being detected object
        ('nCandidateNum', c_int),                       # 当前人脸匹配到的候选对象数量;candidate number
        ('stuCandidates', CANDIDATE_INFO * 50),         # 当前人脸匹配到的候选对象信息;candidate info
        ('bEventAction', c_ubyte),                      # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;
        ('byImageIndex', c_ubyte),                      # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0
        ('byReserved1', c_ubyte * 2),                   # 字节对齐;byte alignment
        ('bGlobalScenePic', c_int),                     # 全景图是否存在;The existence panorama
        ('stuGlobalScenePicInfo', SDK_PIC_INFO),        # 全景图片信息;Panoramic Photos
        ('szSnapDevAddress',  c_char * 260),            # 抓拍当前人脸的设备地址,如：滨康路37号;Snapshot current face aadevice address
        ('nOccurrenceCount', c_uint),                   # 事件触发累计次数;event trigger accumilated times
        ('stuIntelliCommInfo', EVENT_INTELLI_COMM_INFO),# 智能事件公共信息;intelligent things info
        ('stuFaceData', NET_FACE_DATA),                 # 人脸数据;the data of face
        ('szUID', c_char * 32),                         # 抓拍人员写入数据库的唯一标识符;The unique identifier of the snap person to write to the database
        ('stuFeatureVector', NET_FEATURE_VECTOR),       # 特征值信息;Feature data information
        ('szFeatureVersion', c_char * 32),              # 特征值算法版本;The version of the feature data algorithm
        ('emFaceDetectStatus', c_int),                  # 人脸在摄像机画面中的状态,参考EM_FACE_DETECT_STATUS;The status of person in camera picture,refer to EM_FACE_DETECT_STATUS
        ('szSourceID', c_char * 32),                    # 事件关联ID,同一个物体或图片生成多个事件时SourceID相同;Correlate event ID, events arising from same object or picture could have same correlate event ID
        ('stuPasserbyInfo', NET_PASSERBY_INFO),         # 路人库信息;passerby info
        ('nStayTime', c_uint),                          # 路人逗留时间 单位：秒;stay time Unit:s
        ('stuGPSInfo', NET_GPS_INFO),                   # GPS信息;GPS info
        ('bReserved', c_ubyte * 432),                   # 保留字节,留待扩展;Reserved
        ('nRetCandidatesExNum', c_int),                 # 当前人脸匹配到的候选对象数量实际返回值;the actual return number of stuCandidatesEx
        ('stuCandidatesEx', CANDIDATE_INFOEX * 50),     # 当前人脸匹配到的候选对象信息扩展;the expansion of candidate information
        ('szSerialUUID', c_char * 22),                  # 级联物体ID唯一标识;szSerial UUID
                                                            # 格式如下：前2位%d%d:01-视频片段,02-图片,03-文件,99-其他;The format is as follows：Front 2:%d%d:01-video,02-picture,03-file,99-other;
                                                            # 中间14位YYYYMMDDhhmmss:年月日时分秒;后5位%u%u%u%u%u：物体ID，如00001;Middle 14:YYYYMMDDhhmmss:year,month,day,hour,minute,second;Last 5:%u%u%u%u%u：object ID，as 00001
        ('byReserved', c_ubyte * 2),                    # 对齐;reserved
        ('stuCustomProjects', NET_CUSTOM_PROJECTS_INFO),  # 信息;info
        ('bIsDuplicateRemove', c_int),                  # 智慧零售，是否符合去重策略（TRUE：符合 FALSE：不符合）;Smart retail, whether it conforms to the de duplication strategy (true: conforms to false: does not conform to)
        ('byReserved2', C_BYTE * 4),                    # 字节对齐;byte alaginment;
        ('stuImageInfo', NET_IMAGE_INFO_EX2 * 32),      # 图片信息数组;image information array;
        ('nImageInfoNum', c_int),                       # 图片信息个数;the number of image information;
        ('stuObjectSupplement', NET_A_MSG_OBJECT_SUPPLEMENT),  # 检测到的物体补充字段;Detected object supplementary field;
        ('nMode', C_UINT),                              # 0-普通 1-开启陌生人模式;0 - normal 1 - enable stranger mode;
        ('stuThumImageInfo', SCENE_IMAGE_INFO),         # 大图（全景图）的缩略图信息;Thumbnail information of large image (Panorama);
        ('stuHumanImageInfo', SCENE_IMAGE_INFO),        # 人体图片信息;Human body picture information;
        ('szVideoPath', c_char * 256),                  # 违章关联视频FTP上传路径;ftp path for assocated video;
        ('bIsHighFrequencyAlarm', C_BOOL),              # 是否是高频次报警;Is it a high frequency alarm;
        ('szFrequencyAlarmName', c_char * 32),          # 频次报警名称, 当bIsHighFrequencyAlarm字段值为TRUE时才有效，表示高频次报警名称;Frequency alarm name, It is valid only when the value of bIshighfrequencylalarm field is TRUE, indicating the name of high-frequency alarm;
        ('PTS', c_double),                              # 时间戳(单位是毫秒);Time stamp(ms);
        ('byReserved3', c_char * 272),                  # 保留字节;reserved;
    ]


class PLAY_FRAME_INFO(Structure):
    """
    事件类型FACERECOGNITION(目标识别)对应的数据块描述信息; the describe of FACERECOGNITION's data
    """
    _fields_ = [
        ('nWidth', c_int),                          # Width, unit is pixel, 0 for audio data.
        ('nHeight', c_int),                         # height, 0 for audio data
        ('nStamp', c_int),                          # Time stamp info, unit is ms
        ('nType', c_int),                           # Video frame type,T_AUDIO16,T_RGB32,T_IYUV
        ('nFrameRate', c_int),                      # Video represents frame rate,audio represents sampling rate
    ]

class NET_VAOBJECT_NUMMAN(Structure):
    """
    检测到的人信息; Human info
    """
    _fields_ = [
        ('nObjectID', c_uint),             # 物体ID，每个ID表示一个唯一的物体;Object ID
        ('emUniformStyle', c_int),         # 制服样式,参考EM_UNIFORM_STYLE;Uniform style，refer to EM_UNIFORM_STYLE
        ('stuBoundingBox', NET_RECT),         # 包围盒,手套对象在全景图中的框坐标,为0~8191相对坐标;Bounding box(8192 coordinate system)
        ('stuOriginalBoundingBox', NET_RECT), # 包围盒,绝对坐标;BoundingBox Rect, absolute coordinates
        ('byReserved', c_byte*128),           # 预留字节;Reserved
    ]

class NET_PRESET_POSITION(Structure):
    """
    预置点的坐标和放大倍数
    The coordinates and magnification of the preset points
    """
    _fields_ = [
        ('nHorizontal', c_int),  # 水平坐标;Horizontal coordinates;
        ('nVertical', c_int),  # 垂直坐标;The vertical coordinate;
        ('nMagnification', c_int),  # 放大倍数;Magnification;
    ]

class NET_BOAT_OBJECT(Structure):
    """
    船只物体信息
    Ship object information
    """
    _fields_ = [
        ('nObjectID', C_UINT),  # 物体ID，每个ID表示一个唯一的物体，不同的物体不能共用一个ID，已经使用过的ID也不能再次使用。;Object ID, each ID represents a unique object, different objects cannot share an ID, and IDs that have been used cannot be used again.;
        ('nDistance', c_int),  # 船身体到相机的距离，单位米 取值范围0-65535;The distance from the ship's body to the camera, in meters. Value range: 0-65535;
        ('nHeight', c_int),  # 船的高度，单位米 取值范围0-255;The height of the ship, in meters, the value range is 0-255;
        ('nWidth', c_int),  # 船的长度，单位米 取值范围0-2000;The length of the ship, in meters, the value range is 0-2000;
        ('nSpeed', c_int),  # 船的速度，单位米/秒 取值范围0-255;The speed of the ship, in meters/second, the value range is 0-255;
        ('emActionType', C_ENUM),  # 物体动作支持类型 Refer: EM_ACTION;Object action support type Refer: EM_ACTION;
        ('stuBoundingBox', NET_RECT),  # 矩形范围,点的坐标归一化到[0,8191]区间;Rectangular range, the coordinates of the point are normalized to the interval [0,8191];
        ('stuOriginalBoundingBox', NET_RECT),  # 包围盒(绝对坐标);Bounding box (absolute coordinates);
        ('emDirection', C_ENUM),  # 行驶方向 Refer: EM_BOAT_DIRECTION;Direction of the boat Refer: EM_BOAT_DIRECTION;
        ('szBoatCode', c_char * 64),  # 船名或船舷号;BoatCode;
        ('byReserved', C_BYTE * 60),  # 预留字节;Reserved byte;
    ]

class DEV_EVENT_CROSSLINE_INFO(Structure):
    """
    事件类型CROSSLINEDETECTION(警戒线)对应的数据块描述信息; the describe of CROSSLINEDETECTION's data
    """
    _fields_ = [
        ('nChannelID', c_int),              # 通道号;Channel
        ('szName', c_char * 128),           # 事件名称;event name
        ('bReserved1', c_char * 4),         # 字节对齐;byte alignment
        ('PTS', c_double),                  # 时间戳(单位是毫秒);PTS(ms)
        ('UTC', NET_TIME_EX),               # 事件发生的时间;the event happen time
        ('nEventID', c_int),                # 事件ID;event ID
        ('stuObject', SDK_MSG_OBJECT),      # 检测到的物体;have being detected object
        ('stuFileInfo', SDK_EVENT_FILE_INFO),   # 事件对应文件信息;event file info
        ('DetectLine', SDK_POINT*20),           # 规则检测线;rule detect line
        ('nDetectLineNum', c_int),          # 规则检测线顶点数;rule detect line's point number
        ('TrackLine', SDK_POINT*20),        # 物体运动轨迹;object moveing track
        ('nTrackLineNum', c_int),           # 物体运动轨迹顶点数;object moveing track's point number
        ('bEventAction', c_byte),           # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;
        ('bDirection', c_byte),             # 表示入侵方向, 0-由左至右, 1-由右至左;direction, 0-left to right, 1-right to left
        ('byReserved', c_byte),             # 字节对齐;byte alignment
        ('byImageIndex', c_byte),           # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0
        ('dwSnapFlagMask', C_DWORD),        # 抓图标志(按位),0位:"*",1位:"Timing",2位:"Manual",3位:"Marked",4位:"Event",5位:"Mosaic",6位:"Cutout";flag(by bit),0bit:"*",1bit:"Timing",2bit:"Manual",3bit:"Marked",4bit:"Event",5bit:"Mosaic",6bit:"Cutout"
        ('nSourceIndex', c_int),            # 事件源设备上的index,-1表示数据无效,-1表示数据无效;the source device's index,-1 means data in invalid
        ('szSourceDevice', c_char*260),     # 事件源设备唯一标识,字段不存在或者为空表示本地设备;the source device's sign(exclusive),field said local device does not exist or is empty
        ('nOccurrenceCount', c_uint),       # 事件触发累计次数;event trigger accumulated times
        ('stuIntelliCommInfo', EVENT_INTELLI_COMM_INFO),    # 智能事件公共信息;intelli comm info
        ('stuExtensionInfo', NET_EXTENSION_INFO),       # 扩展信息;Extension info
        ('stuSceneImage', SCENE_IMAGE_INFO_EX),         # 全景广角图;Scene image
        ('nObjetcHumansNum', c_uint),                   # 检测到人的数量;Number of people detected
        ('stuObjetcHumans', NET_VAOBJECT_NUMMAN * 100), # 检测的到人;People detected
        ('nRuleID', C_UINT),                    # 规则编号,用于标示哪个规则触发的事件，缺省时默认为0;Rule ID, used to indicate which rule triggers the event. The default value is 0;
        ('emEventType', C_ENUM),                # 事件级别 Refer: EM_EVENT_LEVEL;Event level Refer: EM_EVENT_LEVEL;
        ('stPosition', NET_PRESET_POSITION),    # 预置点的坐标和放大倍数;The coordinates and magnification of the preset points;
        ('nVisibleHFOV', C_UINT),               # 可见光横向视场角,单位度 实际角度乘以100;Horizontal field Angle of visible light ,the actual Angle times 100;
        ('nVisibleVFOV', C_UINT),               # 可见光纵向视场角,单位度 实际角度乘以100;Longitudinal field Angle of visible light ,the actual Angle times 100;
        ('nCurChannelHFOV', C_UINT),            # 当前报警通道的横向视场角，单位度，实际角度乘以100;Lateral field angle of view of the current alarm channel,Unit: degrees,the actual Angle times 100;
        ('nCurChannelVFOV', C_UINT),            # 当前报警通道的纵向视场角，单位度，实际角度乘以100;Longitudinal field angle of view of the current alarm channel,Unit: degrees,the actual Angle times 100;
        ('nImageNum', c_int),                   # 图片信息个数;picture number;
        ('pImageArray', POINTER(NET_IMAGE_INFO_EX2)),  # 图片信息数组;picture info;
        ('nCarMirrorStatus', c_int),            # 车的后视镜状态，-1: 未知, 0: 正常, 1: 不正常(如数量缺失等);The status of the rearview mirror of the car, -1: Unknown 0-normal, 1-abnormal (such as missing quantity, etc.);
        ('nCarLightStatus', c_int),             # 车的车灯状态,-1: 未知, 0: 正常, 1:不正常(如灯未亮等);Status of vehicle lights: -1: Unknown 0-normal, 1-abnormal (such as lights not on, etc.);
        ('nObjectBoatsNum', C_UINT),            # 船只物体个数;Number of Boat objects;
        ('stuBoatObjects', NET_BOAT_OBJECT * 100),  # 船只物品信息;Boat Objects Info;
        ('nUpDownGoing', c_int),                # 车道/航道方向, 0:未知, 1:上行, 2:下行;Lane/Course Direction, 0: Unknown, 1: UpGoing, 2: DownGoing;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('byReserved1', C_BYTE * 452),          # 预留字节;Reserved;
    ]

class NET_IN_GET_CAMERA_STATEINFO(Structure):
    """
    QueryDevInfo 接口 NET_QUERY_GET_CAMERA_STATE 命令入参;QueryDevInfo interface NET_QUERY_GET_CAMERA_STATE command to input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),        # 结构体大小;Struct size
        ('bGetAllFlag', c_bool),    # 是否查询所有摄像机状态,若该成员为 TRUE,则 nChannels 成员无需设置;
                                    # if it is to check all the cameras status, if the member is TRUE, then nChannels member is unnecessary to set.
        ('nValidNum', c_int),       # 该成员,bGetAllFlag 为 FALSE时有效,表示 nChannels 成员有效个数
                                    # the member is valid when bGetAllFlag is FALSE, which means valid number of nChannels member
        ('nChannels', c_int*1024),  # 该成员,bGetAllFlag 为 FALSE时有效,将需要查询的通道号依次填入
                                    # The member is valid when bGetAllFlag is FALSE, it is to fill in the channel numbers in turn which needs inquiry.
    ]

class NET_CAMERA_STATE_INFO(Structure):
    """
    摄像机通道信息; Camera state info
    """
    _fields_ = [
        ('nChannel', c_int),            # 摄像机通道号, -1表示通道号无效;camera channel number, -1 means invalid channel number
        ('emConnectionState', c_int),   # 连接状态,参见SDK_Enum.py内的EM_CAMERA_STATE_TYPE;connection state，refer to EM_CAMERA_STATE_TYPE in SDK.Enum.py
        ('szReserved', c_char*1024),    # 保留字节;byte reserved
    ]

class NET_OUT_GET_CAMERA_STATEINFO(Structure):
    """
    QueryDevInfo 接口 NET_QUERY_GET_CAMERA_STATE 命令出参;QueryDevInfo interface NET_QUERY_GET_CAMERA_STATE command to output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                        # 结构体大小;Struct size
        ('nValidNum', c_int),                                       # 查询到的摄像机通道状态有效个数,由sdk返回;valid number of camera channel state, returned by sdk
        ('nMaxNum', c_int),                                         # pCameraStateInfo 数组最大个数,由用户填写;max number of array, filled in by user
        ('pCameraStateInfo', POINTER(NET_CAMERA_STATE_INFO)),       # 摄像机通道信息数组,由用户分配,大小为sizeof(NET_CAMERA_STATE_INFO)*nMaxNum;camera channel info array, distributed by user,apply to sizeof(NET_CAMERA_STATE_INFO)*nMaxNum;
    ]

class DEV_ACCESS_CTL_IMAGE_INFO(Structure):
    """
    图片信息; access control image info
    """
    _fields_ = [
        ('emType', C_ENUM),             # 图片类型, 参考 EM_ACCESS_CTL_IMAGE_TYPE; Image type, Please refer to EM_ACCESS_CTL_IMAGE_TYPE
        ('nOffSet', C_UINT),            # 二进制块偏移字节; Offset in binary block
        ('nLength', C_UINT),            # 图片大小; Image size
        ('nWidth', C_UINT),             # 图片宽度(单位:像素); Image width(Unit:pixel)
        ('nHeight', C_UINT),            # 图片高度(单位:像素); Image height(Unit:pixel)
        ('stuBoundingBox', NET_RECT),   # 包围盒; Bounding box
        ('byReserved', C_BYTE * 48),    # 保留字节; Reserved
    ]

class DEV_ACCESS_CTL_CUSTOM_WORKER_INFO(Structure):
    """
    人员信息; worker info
    """
    _fields_ = [
        ('emSex', C_ENUM),                              # 性别, 参考 NET_ACCESSCTLCARD_SEX; sex, Please refer to NET_ACCESSCTLCARD_SEX
        ('szRole', c_char * 32),                        # 角色; role
        ('szProjectNo', c_char * 32),                   # 项目ID; project No.
        ('szProjectName', c_char * 64),                 # 项目名称; project name
        ('szBuilderName', c_char * 64),                 # 施工单位全称; builder name
        ('szBuilderID', c_char * 32),                   # 施工单位ID; builder ID
        ('szBuilderType', c_char * 32),                 # 施工单位类型;builder type
        ('szBuilderTypeID', c_char * 8),                # 施工单位类别ID; builder type ID
        ('szPictureID', c_char * 64),                   # 人员照片ID; picture ID
        ('szContractID', c_char * 16),                  # 原合同系统合同编号; contract ID in original contract system
        ('szWorkerTypeID', c_char * 8),                 # 工种ID; worker type ID
        ('szWorkerTypeName', c_char * 32),              # 工种名称; worker type name
        ('bPersonStatus', C_BOOL),                      # 人员状态, TRUE:启用, FALSE:禁用; person status, TRUE:enable, FALSE:forbidden
        ('byReserved', C_BYTE * 256),                   # 保留字节; Reserved
    ]

class NET_MAN_TEMPERATURE_INFO(Structure):
    """
    人员温度信息; Human temperature info
    """
    _fields_ = [
        ('fCurrentTemperature', c_float),               # 人员温度, 参考 EM_HUMAN_TEMPERATURE_UNIT; Human temperature, Please refer to EM_HUMAN_TEMPERATURE_UNIT
        ('emTemperatureUnit', C_ENUM),                  # 温度单位; Temperature unit
        ('bIsOverTemperature', C_BOOL),                 # 是否超温; Is over temperature or not
        ('emTemperatureStatus', C_ENUM),                # 人体测温状态 Refer: EM_HUMAN_TEMPERATURE_STATUS;Human body temperature status Refer: EM_HUMAN_TEMPERATURE_STATUS;
        ('byReserved', C_BYTE * 256),                   # 预留字节; Reserved
    ]

class NET_COMPANION_INFO(Structure):
    """
    人员温度信息; Human temperature info
    """
    _fields_ = [
        ('szCompanionCard', c_char * 32),               # 陪同者卡号; card
        ('szCompanionUserID', c_char * 32),             # 陪同者ID	; user id
        ('szCompanionName', c_char * 120),              # 陪同者姓名; name
        ('szCompanionCompany', c_char * 200),           # 陪同者单位;Company;
        ('byReserved', C_BYTE * 56),                   # 预留字段; Reserved
    ]

class NET_TEST_RESULT(Structure):
    """
    ESD阻值测试结果
    ESD resistance test result
    """
    _fields_ = [
        ('nHandValue', C_UINT),  # k欧姆（阻值单位）;k ohm (resistance unit);
        ('nLeftFootValue', C_UINT),  # k欧姆（阻值单位）;k ohm (resistance unit);
        ('nRightFootValue', C_UINT),  # k欧姆（阻值单位）;k ohm (resistance unit));
        ('emEsdResult', C_ENUM),  # 测试结果 Refer: EM_ESD_RESULT;Test Result Refer: EM_ESD_RESULT;
        ('bReserved', C_BYTE * 128),  # 预留字节;Reserved byte;
    ]

class NET_VACCINE_INFO(Structure):
    """
    新冠疫苗接种信息
    New crown vaccination information
    """
    _fields_ = [
        ('nVaccinateFlag', c_int),  # 是否已接种新冠疫苗, 0: 否, 1: 是;Have you been vaccinated against the new crown vaccine, 0: No, 1: Yes;
        ('szVaccineName', c_char * 128),  # 新冠疫苗名称;New crown vaccine name;
        ('nDateCount', c_int),  # 历史接种日期有效个数;Valid number of historical vaccination dates;
        ('szVaccinateDate', c_char * 256),  # 历史接种日期 (yyyy-MM-dd). 如提供不了时间, 则填"0000-00-00", 表示已接种;Historical vaccination date(yyyy-MM-dd). If you cannot provide the time, fill in "0000-00-00", which means that you have been vaccinated;
        ('nVaccineIntensifyFlag', c_int),   # 是否已接种新冠疫苗加强针, 0: 未知, 1:否  2: 是;Have you been vaccinated Intensify against the new crown vaccine, 0: unKnown, 1:No, 2: Yes;
        ('szReserved', c_char * 1020),  # 保留字节;Reserved;
    ]

class NET_HSJC_INFO(Structure):
    """
    核酸检测信息
    Nucleic acid detection information
    """
    _fields_ = [
        ('szHSJCReportDate', c_char * 32),  # 核酸检测报告日期 (yyyy-MM-dd);Date of nucleic acid test report (yyyy-MM-dd);
        ('nHSJCExpiresIn', c_int),  # 核酸检测报告有效期(天);Nucleic acid test report validity period (days);
        ('nHSJCResult', c_int),  # 核酸检测报告结果;Nucleic acid test report result
        ('szHSJCInstitution', c_char * 256),  # 核酸检测机构;Nucleic acid testing institutions;
        ('szReserved', c_char * 768),  # 保留字节;Reserved;
    ]

class NET_ANTIGEN_INFO(Structure):
    """
    抗原检测信息
    Antigen Test Information
    """
    _fields_ = [
        ('szAntigenReportDate', c_char * 32),  # 抗原检测报告日期;Antigen test report date;
        ('nAntigenStatus', c_int),  # 抗原检测报告结果;Antigen Test Report Result;
        ('nAntigenExpiresIn', c_int),  # 抗原检测报告有效期(单位:天);Validity period of antigen test report (unit: day);
        ('szResvered', c_char * 256),  # 保留字节;Reserved;
    ]

class NET_TRAVEL_INFO(Structure):
    """
    行程码信息
    Travel Info
    """
    _fields_ = [
        ('emTravelCodeColor', C_ENUM),  # 行程码状态 Refer: EM_TRAVEL_CODE_COLOR;Travel Code Color Refer: EM_TRAVEL_CODE_COLOR;
        ('nCityCount', c_int),  # 最近14天经过的城市个数;Number of cities passed in the last 14 days;
        ('szPassingCity', c_char * 2048),  # 最近14天经过的城市名. 按时间顺序排列, 最早经过的城市放第一个;The names of the cities that have passed in the last 14 days. In chronological order, the earliest passing city is placed first;
        ('szReserved', c_char * 1024),  # 保留字节;Reserved;
    ]

class NET_ACCESS_CTL_OBJECT_PROPERTIES(Structure):
    """
    动态识别的结构化信息对象
    Dynamically Recognized Structured Information Objects
    """
    _fields_ = [
        ('nRedScarfResult', C_UINT),  # 红领巾识别结果 UINT_MAX(-1):未知 0:未佩戴 1:已佩戴；255:未使能算法识别;Red scarf recognition result UINT_ MAX (-1): unknown 0: not worn 1: worn; 255: Algorithm recognition not enabled;
        ('szReserved', c_char * 60),  # 保留字节;Reserved;
    ]

class DEV_EVENT_ACCESS_CTL_INFO(Structure):
    """
    事件类型 ACCESS_CTL(门禁事件)对应数据块描述信息; Corresponding data description info of event type ACCESS_CTL (Access control info event)
    """
    _fields_ = [
        ('nChannelID', c_int),                  # 门通道号;Door Channel Number
        ('szName', c_char * 128),               # 事件名称;Entrance Guard Name
        ('bReserved1', c_char * 4),             # 字节对齐;Align byte
        ('PTS', c_double),                      # 时间戳(单位是毫秒);Time stamp (Unit:ms)
        ('UTC', NET_TIME_EX),                   # 事件发生的时间;Event occurrence time
        ('nEventID', c_int),                    # 事件ID;Event ID
        ('stuObject', SDK_MSG_OBJECT),          # 检测到的物体;have being detected object
        ('stuFileInfo', SDK_EVENT_FILE_INFO),   # 事件对应文件信息;The corresponding file info of the event
        ('emEventType', C_ENUM),                # 门禁事件类型,参考 NET_ACCESS_CTL_EVENT_TYPE; Entrance Guard Event Type,Please refer to NET_ACCESS_CTL_EVENT_TYPE
        ('bStatus', C_BOOL),                    # 刷卡结果,TRUE表示成功,FALSE表示失败;Swing Card Result,True is Success,False is Fail
        ('emCardType', C_ENUM),                 # 卡类型,参考 NET_ACCESSCTLCARD_TYPE;Card Type,Please refer to NET_ACCESSCTLCARD_TYPE
        ('emOpenMethod', C_ENUM),               # 开门方式,参考 NET_ACCESS_DOOROPEN_METHOD;Open The Door Method,Please refer to NET_ACCESS_DOOROPEN_METHOD
        ('szCardNo', c_char * 32),              # 卡号;Card Number
        ('szPwd', c_char * 64),                 # 密码;Password
        ('szReaderID', c_char * 32),            # 门读卡器ID;Reader ID
        ('szUserID', c_char * 64),              # 开门用户;unlock user
        ('szSnapURL', c_char * 128),            # 抓拍照片存储地址;snapshot picture storage address
        ('nErrorCode', c_int),                  # 开门操作码，配合 bStatus 使用;Open door operate code, use with bStatus
                                                    # 0x00 没有错误;no error
                                                    # 0x10 未授权;unauthorized
                                                    # 0x11 卡挂失或注销;card lost or cancelled
                                                    # 0x12 没有该门权限;no door right
                                                    # 0x13 开门模式错误;unlock mode error
                                                    # 0x14 有效期错误;valid period error
                                                    # 0x15 防反潜模式;anti sneak into mode
                                                    # 0x16 胁迫报警未打开;forced alarm not unlocked
                                                    # 0x17 门常闭状态;door NC status
                                                    # 0x18 AB互锁状态;AB lock status
                                                    # 0x19 巡逻卡;patrol card
                                                    # 0x1A 设备处于闯入报警状态;device is under intrusion alarm status
                                                    # 0x20 时间段错误;period error
                                                    # 0x21 假期内开门时间段错误;unlock period error in holiday period
                                                    # 0x30 需要先验证有首卡权限的卡片;first card right check required
                                                    # 0x40 卡片正确,输入密码错误;card correct, input password error
                                                    # 0x41 卡片正确,输入密码超时;card correct, input password timed out
                                                    # 0x42 卡片正确,输入错误;card correct, input error
                                                    # 0x43 卡片正确,输入超时;card correct, input timed out
                                                    # 0x44 正确,输入密码错误; correct, input password error
                                                    # 0x45 正确,输入密码超时; correct, input password timed out
                                                    # 0x50 组合开门顺序错误;group unlock sequence error
                                                    # 0x51 组合开门需要继续验证;test required for group unlock
                                                    # 0x60 验证通过,控制台未授权;test passed, control unauthorized
                                                    # 0x61 卡片正确,人脸错误;card correct, input face error
                                                    # 0x62 卡片正确,人脸超时;card correct, input face timed out
                                                    # 0x63 重复进入;repeat enter
                                                    # 0x64 未授权,需要后端平台识别;unauthorized, requiring back-end platform identification
                                                    # 0x65 温度过高;high body temperature
                                                    # 0x66	未戴口罩;no mask
                                                    # 0x67 健康码获取失败;get health code fail
                                                    # 0x68 黄码禁止通行;No Entry because of yellow code
                                                    # 0x69 红码禁止通行;No Entry because of red code
                                                    # 0x6a 健康码无效;health code is invalid
                                                    # 0x6b 绿码验证通过;entry because of green code
                                                    # 0x70 获取健康码信息;get health code info
                                                    # 0x71 校验证件信息（平台下发对应证件号的校验结果）;verify citizenId (platform issues the verification result of the corresponding citizenId)
                                                    # 0xA8 未佩戴安全帽;not wear safety helmet
        ('nPunchingRecNo', c_int),              # 刷卡记录集中的记录编号;punching record number
        ('nNumbers', c_int),                    # 抓图张数;picture Numbers
        ('byImageIndex', c_ubyte),              # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0
        ('byReserved', c_ubyte * 3),            # 字节对齐;Align byte
        ('dwSnapFlagMask', C_DWORD),            # 抓图标志(按位),具体见 NET_RESERVED_COMMON;Snap flag(by bit)0 bit:"*",1 bit:"Timing",2 bit:"Manual",3 bit:"Marked",4 bit:"Event",5 bit:"Mosaic",6 bit:"Cutout"
        ('emAttendanceState', C_ENUM),          # 考勤状态,参考 NET_ATTENDANCESTATE;Attendance state,Please refer to NET_ATTENDANCESTATE
        ('szClassNumber', c_char * 32),         # 班级;Class number(depricated, please use szClassNumberEx)
        ('szPhoneNumber', c_char * 16),         # 电话;Phone number
        ('szCardName', c_char * 64),            # 卡命名;Card name
        ('uSimilarity', c_uint),                # 目标识别相似度,范围为0~100;target recognition similarity,range is 0~100
        ('stuImageInfo', DEV_ACCESS_CTL_IMAGE_INFO * 6),                # 图片信息;Image information
        ('nImageInfoCount', c_int),             # 图片信息数量;Image information count
        ('szCitizenIDNo',  c_char * 20),        # 证件号;Citizen ID
        ('nGroupID', c_uint),                   # 事件组ID;Event group ID
        ('nCompanionCardCount', c_int),         # 陪同者卡号个数;Companion card count
        ('szCompanionCards', c_char * 6 * 32),  # 陪同者卡号信息（废弃，使用 stuCompanionInfo）;Companion card information
        ('stuCustomWorkerInfo', DEV_ACCESS_CTL_CUSTOM_WORKER_INFO),     # 人员信息; worker info
        ('emCardState', C_ENUM),                # 当前事件是否为采集卡片,参考 EM_CARD_STATE;Weather to collect cards,Please refer to EM_CARD_STATE
        ('szSN', c_char * 32),                  # 设备序列号;Device serial number
        ('emHatStyle', C_ENUM),                 # 帽子类型,参考EM_HAT_STYLE;hat style,Please refer to EM_HAT_STYLE
        ('emHatColor', C_ENUM),                 # 帽子颜色,参考EM_UNIFIED_COLOR_TYPE ;hat color,Please refer to EM_UNIFIED_COLOR_TYPE
        ('emLiftCallerType', C_ENUM),           # 梯控方式触发者,参考 EM_LIFT_CALLER_TYPE; lift caller type,Please refer to EM_LIFT_CALLER_TYPE
        ('bManTemperature', C_BOOL),            # 人员温度信息是否有效;Whether the information of human body temperature is valid
        ('stuManTemperatureInfo', NET_MAN_TEMPERATURE_INFO),            # 人员温度信息, bManTemperature 为TRUE时有效;Information of human body temperature, It is valid whne bManTemperature is TURE
        ('szCitizenName', c_char * 256),        # 证件姓名;citizen name
        ('nCompanionInfo', c_int),              # 陪同人员 stuCompanionInfo 个数;stuCompanionInfo's count
        ('stuCompanionInfo', NET_COMPANION_INFO * 12),                  # 陪同人员信息;companion info
        ('emMask', C_ENUM),                     # 口罩状态,参考EM_MASK_STATE_TYPE;mask( EM_MASK_STATE_UNKNOWN、EM_MASK_STATE_NOMASK、EM_MASK_STATE_WEAR is valid ),Please refer to EM_MASK_STATE_TYPE
        ('nFaceIndex', C_UINT),                 # 一人多脸的人脸序号;face index
        ('bClassNumberEx', C_BOOL),             # szClassNumberEx 是否有效，为TRUE时，szClassNumberEx 有效;whether szClassNumberEx is valid. TRUE : szClassNumberEx is valid, else invalid
        ('szClassNumberEx', c_char * 512),      # 班级;ClassNumber extended
        ('szDormitoryNo', c_char * 64),         # 宿舍号;dormitory no
        ('szStudentNo', c_char * 64),  # 学号;student no
        ('emUserType', C_ENUM),                 # 用户类型( EM_USER_TYPE); user type( from EM_USER_TYPE)
        ('bRealUTC', C_BOOL),                   # RealUTC 是否有效，bRealUTC 为 TRUE 时，用 RealUTC，否则用 UTC 字段; whether RealUTC is valid. when bRealUTC is TRUE, use RealUTC, otherwise use stuTime
        ('RealUTC', NET_TIME_EX),               # 事件发生的时间（标准UTC）; event occur time
        ('szQRCode', c_char * 512),             # 二维码信息; QRcode
        ('szCompanyName', c_char * 200),        # 公司名称; company name
        ('nScore', c_int),                      # 人脸质量评分; face quality score
        ('emFaceCheck', C_ENUM),                # 刷卡开门时，门禁后台校验人脸是否是同一个人 Refer: EM_FACE_CHECK;When swiping the card to open the door, the access control background checks whether the face is the same person Refer: EM_FACE_CHECK;
        ('emQRCodeIsExpired', C_ENUM),          # 
        ('emQRCodeState', C_ENUM),              # 
        ('stuQRCodeValidTo', NET_TIME),         # 二维码截止日期;QR code deadline;
        ('nBlockId', C_UINT),                   # 上报事件数据序列号从1开始自增;The serial number of the reported event data increases from 1;
        ('szSection', c_char * 64),             # 部门名称;Department name;
        ('szWorkClass', c_char * 256),          # 工作班级;Work class;
        ('emTestItems', C_ENUM),                # 测试项目 Refer: EM_TEST_ITEMS;Test items Refer: EM_TEST_ITEMS;
        ('stuTestResult', NET_TEST_RESULT),     # ESD阻值测试结果;ESD resistance test result;
        ('szDeviceID', c_char * 128),           # 门禁设备编号;Access control equipment number;
        ('szUserUniqueID', c_char * 128),       # 用户唯一表示ID;User unique ID;
        ('bUseCardNameEx', C_BOOL),             # 是否使用卡命名扩展;Whether to use the card name extension;
        ('szCardNameEx', c_char * 128),         # 卡命名扩展;Card name extension;
        ('nHSJCResult', c_int),                 # 核酸检测报告结果;Nucleic acid test report result;
        ('stuVaccineInfo', NET_VACCINE_INFO),   # 新冠疫苗接种信息;New crown vaccination information;
        ('stuTravelInfo', NET_TRAVEL_INFO),     # 行程码信息;Trip code information;
        ('szTrafficPlate', c_char * 32),        # 车牌;TrafficPlate;
        ('szQRCodeEx', c_char * 2048),          # 用来上传大二维码内容; used to upload the content of the large QR code;
        ('szRecordUrl', c_char * 128),          # 设备开门录制15-30s的视频, 上报事件中通知录制视频的地址,视频名以编号和时间命名.;The device opens the door to record 15-30s video, and reports the address of the recorded video in the event. The video name is named after the number and time.;
        ('stuHSJCInfo', NET_HSJC_INFO),         # 核酸信息;Nucleic acid detection information;
        ('stuAntigenInfo', NET_ANTIGEN_INFO),   # 抗原检测信息;Antigen Test Information;
        ('szHealthGreenStatus', c_char * 20),   # 个人健康状态 绿码:"Green" 红码:"Red" 黄码:"Yellow" 橙:"Orange" 未知:"None";Personal health status Green Code:"Green" Red code:"Red" Yellow code:"Yellow" Orange code:"Orange" unknown:"None";
        ('szCitizenIDAddress', c_char * 108),   # 住址;Citizen ID Address;
        ('nCitizenIDEC', C_UINT),               # 民族(参照DEV_EVENT_ALARM_CITIZENIDCARD_INFO的nECType定义);EC (refer to the nECType definition of DEV_EVENT_ALARM_CITIZENIDCARD_INFO);
        ('stuCitizenIDBirth', NET_TIME),        # 出生日期（年月日有效）;Date of birth (valid for year, month, day);
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('nAge', c_int),                        # 年龄;Age;
        ('szCheckOutType', c_char * 32),        # 签出类型;Check Out Type;
        ('szCheckOutCause', c_char * 512),      # 签出原因;Check out Reason;
        ('szLocationName', c_char * 256),       # 场所码名称;Location Name;
        ('szLocationAddress', c_char * 256),    # 场所码所在省市区县;Location Address;
        ('szLocationType', c_char * 256),       # 场所码类型;Location Type;
        ('szCallLiftFloor', c_char * 16),  # 呼梯楼层号;call number;
        ('stuObjectProperties', NET_ACCESS_CTL_OBJECT_PROPERTIES),  # 动态识别的结构化信息对象;Dynamically Recognized Structured Information Objects;
        ('szReversed', C_BYTE * 320),           # 预留字节;Reserved byte;
    ]

class SDK_TSECT(Structure):
    """
    时间段结构; Time period structure
    """
    _fields_ = [
        ('bEnable', c_int),         # 当表示录像时间段时,按位表示四个使能,从低位到高位分别表示动检录象、报警录象、普通录象、动检和报警同时发生才录像; Current record period . Bit means the four Enable functions. From the low bit to the high bit:Motion detection record, alarm record and general record, when Motion detection and alarm happened at the same time can record.
                                        # 当表示布撤防时间段时, 表示使能; used in NET_POS_EVENT_LINK, it means enable;
                                        # 当表示推送时间段时, 表示使能：1表示使能，0表示非使能; used in NET_IN_ADD_MOBILE_PUSHER_NOTIFICATION, it means enable：1 means enable, 0 means unable
        ('iBeginHour', c_int),
        ('iBeginMin', c_int),
        ('iBeginSec', c_int),
        ('iEndHour', c_int),
        ('iEndMin', c_int),
        ('iEndSec', c_int),
    ]

class PASSERBY_DB_DUPLICATE_REMOVE_CONFIG_INFO(Structure):
    """
    路人库去重策略配置(选填); Passerby DB duplicate remove strategy config
    """
    _fields_ = [
        ('bEnable', C_DWORD),                   # 使能开关，TRUE：开 FALSE：关; Enable switch, true: on false: off
        ('emDuplicateRemoveType', C_ENUM),      # 路人库去重策略类型,详见 EM_PASSERBY_DB_DUPLICATE_REMOVE_TYPE; Passerby DB duplicate remove strategy, see EM_PASSERBY_DB_DUPLICATE_REMOVE_TYPE
        ('stuTimeSection', SDK_TSECT * 8 * 6),          # 时间段间隔(emDuplicateRemoveType 为 EM_PASSERBY_DB_DUPLICATE_REMOVE_TYPE.TIME_SLOT有效); Time period interval(emDuplicateRemoveType by EM_PASSERBY_DB_DUPLICATE_REMOVE_TYPE.TIME_SLOT Effective)
        ('dwInterval', C_DWORD),                # 时间间隔，单位分钟（emDuplicateRemoveType 为 EM_PASSERBY_DB_DUPLICATE_REMOVE_TYPE.TIME有效); time interval，Unit minute（emDuplicateRemoveType by EM_PASSERBY_DB_DUPLICATE_REMOVE_TYPE.TIME Effective）
        ('byReserved1', C_BYTE * 4),            # 字节对齐; byte alaginmen
        ('byReserved', C_BYTE * 256),           # 字节保留; byte reserved
    ]

class NET_PASSERBY_DB_CONFIG_INFO(Structure):
    """
    路人库配置（选填）; passerby  db config
    """
    _fields_ = [
        ('dwCapacity', C_DWORD),                                                        # 路人库最大注册数目; Maximum registration number of passer-by Library
        ('emOverWriteType', C_ENUM),                                                    # 路人库满时覆盖策略,详见 EM_PASSERBY_DB_OVERWRITE_TYPE; Coverage strategy when the passer-by library is full, see EM_PASSERBY_DB_OVERWRITE_TYPE
        ('stuDuplicateRemoveConfigInfo', PASSERBY_DB_DUPLICATE_REMOVE_CONFIG_INFO),     # 路人库去重策略配置(选填); Passerby DB duplicate remove strategy config
        ('dwFileHoldTime', C_DWORD),                                                    # 设置文件保留天数【范围：0~31】单位：天，超过时间将被删除 0：永不过期; Set the file retention days [range: 0-31] unit: days, which will be deleted if the time exceeds 0: never expire
        ('byReserved1', C_BYTE * 4),                                                    # 字节对齐; byte alaginmen
        ('byReserved', C_BYTE * 256),                                                   # 字节保留; byte reserved
    ]

class NET_FACERECONGNITION_GROUP_INFO(Structure):
    """
    人员组信息; staff group info
    """
    _fields_ = [
        ('dwSize', C_DWORD),                    # 结构体大小; Struct size
        ('emFaceDBType', C_ENUM),               # 人员组类型,详见 EM_FACE_DB_TYPE; staff group type, see EM_FACE_DB_TYPE
        ('szGroupId', c_char * 64),             # 人员组ID,唯一标识一组人员(不可修改,添加操作时无效); staff group ID, SN(cannot modify, invalid when adding operation)
        ('szGroupName', c_char * 128),          # 人员组名称; staff operation name
        ('szGroupRemarks', c_char * 256),       # 人员组备注信息; staff group note info
        ('nGroupSize', c_int),                  # 当前组内人员数; current group staff number
        ('nRetSimilarityCount', c_int),         # 实际返回的库相似度阈值个数; rect similarity count
        ('nSimilarity', c_int * 1024),                 # 库相似度阈值，人脸比对高于阈值认为匹配成功; library similarity threshold
        ('nRetChnCount', c_int),                # 实际返回的通道号个数; rect channel count
        ('nChannel', c_int * 1024),                    # 当前组绑定到的视频通道号列表; the list of channels
        ('nFeatureState', C_UINT * 4),              # 人脸组建模状态信息; feature state of the group:
                                                    # [0] - 准备建模的人员数量，不保证一定建模成功; the number of people ready to model, but no guarantee of sucess
                                                    # [1]-建模失败的人员数量，图片不符合算法要求，需要更换图片; the number of people who failed to model, need to change the picture
                                                    # [2]-已建模成功人员数量，数据可用于算法进行目标识别; the number of people who success to model, the data can be used for target recognition
                                                    # [3]-曾经建模成功，但因算法升级变得不可用的数量，重新建模就可用; once modeling was successful, but became unusable after upgrading, need to abstract
        ('emRegisterDbType', C_ENUM),           # 注册库类型,详见 EM_REGISTER_DB_TYPE; type of register face DB, see EM_REGISTER_DB_TYPE
        ('byReserved1', C_BYTE * 4),                # 字节对齐; byte alagin
        ('stuPasserbyDBConfig', NET_PASSERBY_DB_CONFIG_INFO),       # 路人库配置（选填）; Configuration of pedestrian base (optional)
        ('nGroupSimilarity', C_UINT),              # 组相似度阈值，人脸比对高于阈值认为匹配成功; Group similarity threshold, face alignment higher than the threshold is considered successful matching:
        ('nMaskSimilarity', C_UINT),              # 库口罩相似度阈值，取值范围0-100，可用于口罩检测; Mask Similarity:
        ('dwCapacity', C_DWORD),                    # 最大注册数目; Maximum registration number
        ('nOverWrite', c_int),                  # 注册库满覆盖策略: 0:未知, 1:满停止, 2:满覆盖; Registry full coverage policy: 0: unknown, 1: full stop, 2: full coverage
    ]

class NET_IN_FIND_GROUP_INFO(Structure):
    """
    FindGroupInfo接口输入参数; FindGroupInfo port input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),                    # 结构体大小; Struct size
        ('szGroupId', c_char * 64),             # 人员组ID,唯一标识一组人员,为空表示查询全部人员组信息; staff ID, SN staff, as null means search all staff group info
    ]

class NET_OUT_FIND_GROUP_INFO(Structure):
    """
    FindGroupInfo接口输出参数; FindGroupInfo port output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                                    # 结构体大小; Struct size
        ('pGroupInfos', POINTER(NET_FACERECONGNITION_GROUP_INFO)),              # 人员组信息,由用户申请空间,大小为sizeof(NET_FACERECONGNITION_GROUP_INFO)*nMaxGroupNum; staff group info , apply space by user, apply to sizeof(NET_FACERECONGNITION_GROUP_INFO)*nMaxGroupNum
        ('nMaxGroupNum', c_int),                                                # 当前申请的数组大小; current applied group size
        ('nRetGroupNum', c_int),                                                # 设备返回的人员组个数; device returned staff group number
    ]

class NET_ADD_FACERECONGNITION_GROUP_INFO(Structure):
    """
    添加人员组信息; add staff group info
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                                    # 结构体大小; Struct size
        ('stuGroupInfo', NET_FACERECONGNITION_GROUP_INFO),                      # 人员组信息; staff group info
    ]

class NET_MODIFY_FACERECONGNITION_GROUP_INFO(Structure):
    """
    修改人员组信息; modify staff group info
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                                    # 结构体大小; Struct size
        ('stuGroupInfo', NET_FACERECONGNITION_GROUP_INFO),                      # 人员组信息; staff group info
    ]

class NET_DELETE_FACERECONGNITION_GROUP_INFO(Structure):
    """
    删除人员组信息; delete staff group info
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                # 结构体大小; Struct size
        ('szGroupId', c_char * 64),                         # 人员组信息; staff group info
    ]

class NET_IN_OPERATE_FACERECONGNITION_GROUP(Structure):
    """
    OperateFaceRecognitionGroup接口输入参数; OperateFaceRecognitionGroup port input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                                    # 结构体大小; Struct size
        ('emOperateType', C_ENUM),                                              # 操作类型,参考 EM_OPERATE_FACERECONGNITION_GROUP_TYPE; operation type, the space application by the user,please refer to EM_OPERATE_FACERECONGNITION_GROUP_TYPE
        ('pOPerateInfo', c_void_p),                                             # 相关操作信息,由用户申请内存，申请大小参照操作类型对应的结构体; operation type, the space application by the user,please refer to the structure of operate type
                                                                                    # 若操作类型为EM_OPERATE_FACERECONGNITION_GROUP_TYPE.ADD,对应结构体为NET_ADD_FACERECONGNITION_GROUP_INFO; if operate type is EM_OPERATE_FACERECONGNITION_GROUP_TYPE.ADD,corresponding to NET_ADD_FACERECONGNITION_GROUP_INFO
                                                                                    # 若操作类型为EM_OPERATE_FACERECONGNITION_GROUP_TYPE.MODIFY,对应结构体为NET_MODIFY_FACERECONGNITION_GROUP_INFO; if operate type is EM_OPERATE_FACERECONGNITION_GROUP_TYPE.MODIFY,corresponding to NET_MODIFY_FACERECONGNITION_GROUP_INFO
                                                                                    # 若操作类型为EM_OPERATE_FACERECONGNITION_GROUP_TYPE.DELETE,对应结构体为NET_DELETE_FACERECONGNITION_GROUP_INFO; if operate type is EM_OPERATE_FACERECONGNITION_GROUP_TYPE.DELETE,corresponding to NET_DELETE_FACERECONGNITION_GROUP_INFO
    ]

class NET_OUT_OPERATE_FACERECONGNITION_GROUP(Structure):
    """
    OperateFaceRecognitionGroup接口输出参数; OperateFaceRecognitionGroup port output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),                            # 结构体大小; Struct size
        ('szGroupId', c_char * 64),                     # 新增记录的人员组ID,唯一标识一组人员; new record staff group ID, SN staff
    ]

class NET_IN_STARTFIND_FACERECONGNITION(Structure):
    """
    StartFindFaceRecognition接口输入参数; StartFindFaceRecognitionInterface input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                                    # 结构体大小; Struct size
        ('bPersonEnable', C_BOOL),                                              # 人员信息查询条件是否有效; Personnel information query is valid
        ('stPerson', FACERECOGNITION_PERSON_INFO),                              # 人员信息查询条件; Personnel information query
        ('stMatchOptions', NET_FACE_MATCH_OPTIONS),                             # 人脸匹配选项; Face Matching Options
        ('stFilterInfo', NET_FACE_FILTER_CONDTION),                             # 查询过滤条件; Query filters

        # 图片二进制数据
        ('pBuffer', c_char_p),                                                  # 缓冲地址; Buffer address
        ('nBufferLen', c_int),                                                  # 缓冲数据长度; Buffer data length

        ('nChannelID', c_int),                                                  # 通道号; Channel ID
        ('bPersonExEnable', C_BOOL),                                            # 人员信息查询条件是否有效, 并使用扩展结构体; use stPersonInfoEx when bUsePersonInfoEx is true, otherwise use stPersonInfo
        ('stPersonInfoEx', FACERECOGNITION_PERSON_INFOEX),                      # 人员信息扩展; expansion of personnel information
        ('nSmallPicIDNum', c_int),                                              # 小图ID数量; the count of small picture ID
        ('nSmallPicID', c_int * 32),                                            # 小图ID; small picture ID
        ('emObjectType', C_ENUM),                                               # 搜索的目标类型,详见 EM_OBJECT_TYPE; The type of object, see EM_OBJECT_TYPE
        ('szChannel', c_char * 32),                                             # 通道号;Channel ID;
    ]

class NET_OUT_STARTFIND_FACERECONGNITION(Structure):
    """
    StartFindFaceRecognition接口输出参数; StartFindFaceRecognitionInterface output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                        # 结构体大小; Struct size
        ('nTotalCount', c_int),                                     # 返回的符合查询条件的记录个数,-1表示总条数未生成,要推迟获取; Record number of returns that match the query criteria
        ('lFindHandle', C_LLONG),                                   # 查询句柄; Query handle
        ('nToken', c_int),                                          # 获取到的查询令牌; The search token received
    ]

class NET_UID_CHAR(Structure):
    """
    UID内容; UID contents
    """
    _fields_ = [
        ('szUID', c_char * 32),                                        # UID内容; UID contents
    ]

class NET_UUID_CHAR(Structure):
    """
    人员唯一标识符
    Person unique mark
    """
    _fields_ = [
        ('szUUID', c_char * 64),  # UUID内容;UUID contents;
    ]

class NET_IN_OPERATE_FACERECONGNITIONDB(Structure):
    """
    OperateFaceRecognitionDB接口输入参数; OperateFaceRecognitionDBInterface input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),                                    # 结构体大小; Struct size
        ('emOperateType', C_ENUM),                              # 操作类型,见 EM_OPERATE_FACERECONGNITIONDB_TYPE; Type of operation， see EM_OPERATE_FACERECONGNITIONDB_TYPE
        ('stPersonInfo', FACERECOGNITION_PERSON_INFO),          # 人员信息; Personnel information
        ('nUIDNum', C_DWORD),                                   # UID个数; UID amount

        ('stuUIDs', POINTER(NET_UID_CHAR)),                     # 人员唯一标识符,首次由服务端生成,区别于ID字段; Person unique mark. Generated by the client if it is the first time. Different from the ID string.
                                                                    # 由用户申请内存,大小为sizeof(NET_UID_CHAR)*nUIDNum; the space application by the user, apply to sizeof(NET_UID_CHAR)*nUIDNum
        ('pBuffer', c_char_p),                                  # 缓冲地址; Buffer address
        ('nBufferLen', c_int),                                  # 缓冲数据长度; Buffer data length
        ('bUsePersonInfoEx', C_BOOL),                           # 使用人员扩展信息; use stPersonInfoEx when bUsePersonInfoEx is true, otherwise use stPersonInfo
        ('stPersonInfoEx', FACERECOGNITION_PERSON_INFOEX),      # 人员信息扩展; expansion of personnel information
        ('nUUIDNum', C_DWORD),                                  # UUID个数;UUID number;
        ('stuUUIDs', POINTER(NET_UUID_CHAR)),                   # 人员唯一标识符,由平台端下发，区别于UID字段由用户申请内存,大小为sizeof(NET_UUID_CHAR)*nUUIDNum;The unique identifier of the personnel, issued by the platform, which is different from the UID fieldThe memory is requested by the user, the size is sizeof(NET_UUID_CHAR)*nUUIDNum;
    ]

class NET_OUT_OPERATE_FACERECONGNITIONDB(Structure):
    """
    OperateFaceRecognitionDB接口输出参数; OperateFaceRecognitionDB port output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),                            # 结构体大小; Struct size
        ('szUID', c_char * 32),                         # 人员唯一标识符, 只有在操作类型为EM_OPERATE_FACERECONGNITIONDB_TYPE.ADD时有效; Person unique mark. it is effective when emOperateType is EM_OPERATE_FACERECONGNITIONDB_TYPE.ADD
                                                        # emOperateType操作类型为ET_FACERECONGNITIONDB_DELETE_BY_UID时使用
                                                        # the following fields are effective when emOperateType is NET_FACERECONGNITIONDB_DELETE_BY_UID
        ('nErrorCodeNum', c_int),                       # 错误码个数; error code number
        ('emErrorCodes', C_ENUM * 512),                 # 错误码; error code
    ]

class NET_CUSTOM_INFO(Structure):
    """
    货物通道信息;Cargo Channel Info
    """
    _fields_ = [
        ('nCargoChannelNum', c_int),        # 货物通道个数;Cargo Channel Num
        ('fCoverageRate', c_float*8),       # 货物覆盖率;Cargo Coverage Rate
        ('byReserved', C_BYTE*40),          # 保留字节;Reserved bytes
    ]

class SDK_POLY_POINTS(Structure):
    """
    区域或曲线顶点信息;poly points
    """
    _fields_ =[
        ('nPointNum', c_int),            # 顶点数;point num
        ('stuPoints', SDK_POINT * 20),   # 顶点信息;points info
    ]

class NET_PTZSPACE_UNNORMALIZED(Structure):
    """
    云台定位中非归一化坐标和变倍; unnormalized position and zoom
    """
    _fields_ = [
        ('nPosX', c_int),       # x坐标; x;
        ('nPosY', c_int),       # y坐标; y;
        ('nZoom', c_int),       # 放大倍率; Zoom;
        ('byReserved', C_BYTE * 52),        # 预留字节; Reserved;
    ]

class DEV_EVENT_CROSSREGION_INFO(Structure):
    """
    事件类型CROSSREGIONDETECTION(警戒区事件)对应的数据块描述信息;the describe of CROSSREGIONDETECTION's data
    """
    _fields_ = [
        ('nChannelID', c_int),          # 通道号;ChannelId
        ('szName', c_char*128),         # 事件名称;event name
        ('bReserved2', c_char*4),       # 字节对齐;byte alignment
        ('PTS', c_double),              # 时间戳(单位是毫秒);PTS(ms)
        ('UTC', NET_TIME_EX),           # 事件发生的时间;the event happen time
        ('nEventID', c_int),            # 事件ID;event ID
        ('stuObject', SDK_MSG_OBJECT),  # 检测到的物体;have being detected object
        ('stuFileInfo', SDK_EVENT_FILE_INFO),  # 事件对应文件信息;event file info
        ('DetectRegion', SDK_POINT * 20),  # 规则检测区域;rule detect region
        ('nDetectRegionNum', c_int),    # 规则检测区域顶点数;rule detect region's point number
        ('TrackLine', SDK_POINT*20),    # 物体运动轨迹;object moving track
        ('nTrackLineNum', c_int),       # 物体运动轨迹顶点数;object moving track's point number
        ('bEventAction', C_BYTE),       # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;
        ('bDirection', C_BYTE),         # 表示入侵方向, 0-进入, 1-离开,2-出现,3-消失;direction, 0-in, 1-out,2-apaer,3-leave
        ('bActionType', C_BYTE),        # 表示检测动作类型,0-出现 1-消失 2-在区域内 3-穿越区域;action type,0-appear 1-disappear 2-in area 3-cross area
        ('byImageIndex', C_BYTE),       # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0
        ('dwSnapFlagMask', C_DWORD),    # 抓图标志(按位),0位:"*",1位:"Timing",2位:"Manual",3位:"Marked",4位:"Event",5位:"Mosaic",6位:"Cutout"
                                        # snap flags(by bit),0bit:"*",1bit:"Timing",2bit:"Manual",3bit:"Marked",4bit:"Event",5bit:"Mosaic",6bit:"Cutout"
        ('nSourceIndex', c_int),        # 事件源设备上的index,-1表示数据无效;the source device's index,-1 means data in invalid
        ('szSourceDevice', c_char * 260),  # 事件源设备唯一标识,字段不存在或者为空表示本地设备;the source device's sign(exclusive),field said local device does not exist or is empty
        ('nOccurrenceCount', c_uint),    # 事件触发累计次数;event trigger times
        ('stuCustom', NET_CUSTOM_INFO), # 货物通道信息;Cargo Channel Info
        ('stuExtensionInfo', NET_EXTENSION_INFO), #扩展信息;Extension info
        ('bReserved', C_BYTE*328),      # 保留字节,留待扩展;reserved
        ('nObjectNum', c_int),          # 检测到的物体个数;Detect object amount
        ('stuObjectIDs', SDK_MSG_OBJECT*16), # 检测到的物体;Detected object
        ('nTrackNum', c_int),               # 轨迹数(与检测到的物体个数对应);Locus amount(Corresponding to the detected object amount.)
        ('stuTrackInfo', SDK_POLY_POINTS*16),  # 轨迹信息(与检测到的物体对应);Locus info(Corresponding to the detected object)
        ('stuIntelliCommInfo', EVENT_INTELLI_COMM_INFO),    # 智能事件公共信息;intelli comm info
        ('stuSceneImage', SCENE_IMAGE_INFO_EX),         # 全景广角图; scene image
        ('nObjetcHumansNum', c_uint),                    # 检测到人的数量;Number of people detected
        ('stuObjetcHumans', NET_VAOBJECT_NUMMAN * 100), # 检测的到人;People detected
        ('stuVehicle', SDK_MSG_OBJECT),  # 车身信息;vehicle info
        ('emTriggerType', C_ENUM),  # 触发类型,参考EM_TRIGGER_TYPE;Trigger type,refer to EM_TRIGGER_TYPE
        ('nMark', c_int),  # 标记抓拍帧;Used to mark capture frames
        ('nSource', c_int),  # 视频分析的数据源地址;Data source address of the video analysis
        ('nFrameSequence', c_int),  # 视频分析帧序号;Video analysis frame number
        ('emCaptureProcess', C_ENUM),  # 抓拍过程,参考EM_CAPTURE_PROCESS_END_TYPE;Capture process,refer to EM_CAPTURE_PROCESS_END_TYPE
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info
        ('stuCommInfo', EVENT_COMM_INFO),  # 公共信息;public info
        ('stuAbsPosition', NET_PTZSPACE_UNNORMALIZED), # 云台方向与放大倍数（扩大100倍表示）第一个元素为水平角度，0-36000；第二个元素为垂直角度，（-18000）-（18000）；第三个元素为显示放大倍数，0-MaxZoom*100;PTZ direction and magnification (indicated by 100 times enlargement)The first element is the horizontal angle, 0-36000;The second element is the vertical angle, (-18000)-(18000)The third element is the display magnification, 0-MaxZoom*100;
        ('nHFovValue', c_int), # 对应倍率水平视场角, 单位0.01度, 扩大100倍表示;HFov Value, unit: 0.01 degree, Enlarged 100 times display;
        ('dbFocusPosition', c_double),  # 聚焦位置;Focus Position;
        ('nObjectBoatNum', C_UINT),  # 船只物体个数;Number of ship objects;
        ('stuBoatObject', NET_BOAT_OBJECT * 100),  # 船只物品信息;Ship item information;
        ('nImageNum', c_int),  # 图片信息个数;picture number;
        ('pImageArray', POINTER(NET_IMAGE_INFO_EX2)),  # 图片信息数组;picture info;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('pstuObjectEx2', POINTER(NET_A_MSG_OBJECT_EX2)),  # / 检测到的物体扩展;have being detected object
        ('pstuObjectIDsEx2', POINTER(NET_A_MSG_OBJECT_EX2)),  # / 检测到的物体扩展,数量为nObjectNum;Detected object,The number is nObjectNum
        ('pstuVehicleEx2', POINTER(NET_A_MSG_OBJECT_EX2)),  # / 车身信息扩展;vehicle info expansion
    ]

class NET_OBJECT_IMAGE_INFO(Structure):
    """
    物体截图
    Object image info
    """
    _fields_ = [
        ('nOffSet', C_UINT),  # 在二进制数据块中的偏移;Offset in binary data;
        ('nLength', C_UINT),  # 图片大小,单位字节;Image size, unit:bytes;
        ('nWidth', C_UINT),  # 图片宽度(像素);Image width (pixels);
        ('nHeight', C_UINT),  # 图片高度(像素);Image height (pixels);
        ('szFilePath', c_char * 260),  # 全景图片路径;Scene image path;
        ('nIndexInData', C_UINT),  # 图片序号;picture index;
        ('byReserved', C_BYTE * 504),  # 预留字节;Reserved;
    ]

class NET_A_VA_OBJECT_ANIMAL(Structure):
    """
    视频分析物体(动物)
    Video Analyse Animal info
    """
    _fields_ = [
        ('nObjectID', C_UINT),  # 物体ID, 每个ID表示一个唯一的物体;Object ID;
        ('emCategory', C_ENUM),  # 目标动物类型 Refer: EM_ANINAL_CATEGORY;Animal Category Refer: EM_ANINAL_CATEGORY;
        ('stuBoundingBox', NET_RECT),  # 包围盒 动物对象在全景图中的框坐标,为0~8191相对坐标;BoundingBox, The frame coordinates of the animal object in the panorama;
        ('nObjectWeight', C_UINT),  # 动物对象重量，单位:g;Object weight, unit:g;
        ('stuImage', NET_OBJECT_IMAGE_INFO),  # 物体截图;Object screenshot;
        ('emMoveStatus', C_ENUM),  # 运动状态 Refer: EM_A_ENUM_MOTION_STATUS;Move Status Refer: EM_A_ENUM_MOTION_STATUS;
        ('emInRegionStatus', C_ENUM),  # 区域内状态 Refer: EM_A_ENUM_IN_REGION_STATUS;In-region status Refer: EM_A_ENUM_IN_REGION_STATUS;
        ('nResultType', c_int),  # 结果类型 0-实时 1-非实时;Result Type. 0-realtime 1- no reel-time;
        ('bReserved', C_BYTE * 1024),  # 保留字节,留待扩展;Reserved bytes;
    ]

class DEV_EVENT_MOVE_INFO(Structure):
    """
    事件类型MOVEDETECTION(移动事件)对应的数据块描述信息;the describe of MOVEDETECTION's data
    """
    _fields_ =[
        ('nChannelID', c_int),  # 通道号;ChannelId
        ('szName', c_char * 128),  # 事件名称;event name
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms)
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time
        ('nEventID', c_int),  # 事件ID;event ID
        ('stuObject', SDK_MSG_OBJECT),  # 检测到的物体;have being detected object
        ('stuFileInfo', SDK_EVENT_FILE_INFO),  # 事件对应文件信息;event file info
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;
        ('byReserved', C_BYTE * 2), # 对齐;Reserved
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0
        ('nDetectRegionNum', c_int),  # 规则检测区域顶点数;detect region point
        ('DetectRegion', SDK_POINT * 20),  # 规则检测区域;detect region
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON
        ('nSourceIndex', c_int),  # 事件源设备上的index,-1表示数据无效;the source device's index,-1 means data in invalid
        ('szSourceDevice', c_char*260),    # 事件源设备唯一标识,字段不存在或者为空表示本地设备;the source device's sign(exclusive),field said local device does not exist or is empty
        ('nTrackLineNum', c_int),  # 物体运动轨迹顶点数;Object trajectories vertices
        ('stuTrackLine', SDK_POINT * 20),  # 物体运动轨迹;Object trajectories
        ('nOccurrenceCount', c_uint),  # 事件触发累计次数;event trigger accumilated times
        ('stuIntelliCommInfo', EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info
        ('stuExtensionInfo', NET_EXTENSION_INFO),  # 扩展信息;Extension info
        ('nAnimalNum', c_int),  # 动物个数;Animal numbers;
        ('pstuAnimals', POINTER(NET_A_VA_OBJECT_ANIMAL)),  # 动物信息;Animal info;
        ('nMsgObjArrayCount', c_int),  # 检测到的物体信息个数;Number of detected object information;
        ('pMsgObjArray', POINTER(SDK_MSG_OBJECT_EX)),  # 检测到的物体信息数组指针;Detected object information array pointer;
        ('nImageNum', c_int),  # 图片信息个数;Number of picture information;
        ('pImageArray', POINTER(NET_IMAGE_INFO_EX2)),  # 图片信息数组;Image information array;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('bReserved', C_BYTE * 236),  # 保留字节,留待扩展.;Reserved bytes, leave extended;
    ]

class DEV_EVENT_FIGHT_INFO(Structure):
    """
    事件类型FIGHTDETECTION(斗殴事件)对应的数据块描述信息;the describe of FIGHTDETECTION's data
    """
    _fields_ = [
        ('nChannelID', c_int),          # 通道号;ChannelId
        ('szName', c_char*128),         # 事件名称;event name
        ('bReserved1', c_char * 4),     # 字节对齐;byte alignment
        ('PTS', c_double),              # 时间戳(单位是毫秒);PTS(ms)
        ('UTC', NET_TIME_EX),           # 事件发生的时间;the event happen time
        ('nEventID', c_int),            # 事件ID;event ID
        ('nObjectNum', c_int),          # 检测到的物体个数;have being detected object number
        ('stuObjectIDs', SDK_MSG_OBJECT*16), # 检测到的物体列表;have being detected object list
        ('stuFileInfo', SDK_EVENT_FILE_INFO),   # 事件对应文件信息;event file info
        ('bEventAction', C_BYTE),       # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;
        ('byReserved', C_BYTE*2),       # 保留字节;Reserved
        ('byImageIndex', C_BYTE),       # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0
        ('nDetectRegionNum', c_int),    # 规则检测区域顶点数;detect region point
        ('DetectRegion', SDK_POINT * 20), # 规则检测区域;detect region
        ('dwSnapFlagMask', C_DWORD),    # 抓图标志(按位),0位:"*",1位:"Timing",2位:"Manual",3位:"Marked",4位:"Event",5位:"Mosaic",6位:"Cutout"
                                        # snap flags(by bit),0bit:"*",1bit:"Timing",2bit:"Manual",3bit:"Marked",4bit:"Event",5bit:"Mosaic",6bit:"Cutout"
        ('nSourceIndex', c_int),        # 事件源设备上的index,-1表示数据无效;the source device's index,-1 means data in invalid
        ('szSourceDevice', C_BYTE*260), # 事件源设备唯一标识,字段不存在或者为空表示本地设备;the source device's sign(exclusive),field said local device does not exist or is empty
        ('nOccurrenceCount', c_uint),    # 事件触发累计次数;event trigger accumilated times
        ('stuIntelliCommInfo', EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info
        ('stuExtensionInfo', NET_EXTENSION_INFO),   # 扩展信息;Extension info
        ('szSourceID', c_char*32),      # 事件关联ID。应用场景是同一个物体或者同一张图片做不同分析，产生的多个事件的SourceID相同
                                        # 缺省时为空字符串，表示无此信息
                                        # 格式：类型 + 时间 + 序列号，其中类型2位，时间14位，序列号5位
                                        # Event source ID. The application scenario is different analysis of the same object or the same picture, resulting in the same sourceid of multiple events
                                        # The default is an empty string, indicating no such information
                                        # Format: type + time + serial number, in which type 2 digits, time 14 digits and serial number 5 digits
        ('emActionType', C_ENUM),       # 动作类型 Refer: EM_STEREO_ACTION_TYPE;Action Type Refer: EM_STEREO_ACTION_TYPE;
        ('stuSceneImage', SCENE_IMAGE_INFO),            # 全景广角图;Panoramic wide-angle map;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX2)), # 图片信息数组;Image information array;
        ('nImageInfoNum', c_int),       # 图片信息个数;Number of picture information;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),      # 事件公共扩展字段结构体;Event public extension field structure;
        ('bReserved', C_BYTE * 240),    # 保留字节,留待扩展.;Reserved;
    ]

class NET_CROWD_LIST_INFO(Structure):
    """
    全局拥挤人群密度列表(圆形)信息;Crowd list info(circular description)
    """
    _fields_ = [
        ('stuCenterPoint', SDK_POINT),      #中心点坐标,8192坐标系;Center point
        ('nRadiusNum', c_uint),              #半径像素点个数;Radius num
        ('byReserved', C_BYTE*1024),        #保留字节;Reserved
    ]

class NET_CROWD_RECT_LIST_INFO(Structure):
    """
    全局拥挤人群密度列表(矩形)信息;crowd list info(rect description)
    """
    _fields_ = [
        ('stuRectPoint', SDK_POINT*2),      # 矩形的左上角点与右下角点,8192坐标系，表示矩形的人群密度矩形框
        ('byReserved', C_BYTE*32),          # 保留字节;Reserved
    ]

class DEV_EVENT_CROWD_DETECTION_INFO(Structure):
    """
    事件类型 CROWDDETECTION(人群密度检测事件）对应的数据块描述信息;CROWDDETECTION(CrowdDetection)corresponding data block description info
    """
    _fields_ = [
        ('nChannelID', c_int),                  # 通道号;Channel ID
        ('nEventID', c_int),                    # 事件ID;Event ID
        ('PTS', c_double),                      # 时间戳(单位是毫秒);Time stamp (Unit:ms)
        ('UTC', NET_TIME_EX),                   # 事件发生的时间;Event occurrence time
        ('nEventAction', c_int),                # 事件动作,1表示持续性事件开始,2表示持续性事件结束;Event action,1 means continues event start,2 means continuous event stop
        ('emAlarmType', C_ENUM),                 # 报警业务类型,参考EM_ALARM_TYPE；Alarm Type,refer to EM_ALARM_TYPE
        ('szName', c_char*128),                 # 事件名称;Event name
        ('nCrowdListNum', c_int),               # 返回的全局拥挤人群密度列表个数 （圆形描述）;Crowd list num (circular description)
        ('nRegionListNum', c_int),              # 返回的人数超限的报警区域ID列表个数;Region list num
        ('stuCrowdList', NET_CROWD_LIST_INFO * 5), # 全局拥挤人群密度列表信息（圆形描述）;Crowd list info(circular description)
        ('stuRegionList', NET_CROWD_LIST_INFO * 8), # 人数超限的报警区域ID列表信息;Region list info
        ('stuExtensionInfo', NET_EXTENSION_INFO),   # 扩展信息; Extension info
        ('nCrowdRectListNum', c_int),               # 返回的全局拥挤人群密度列表个数 (矩形描述);Crowd list num (rect description)
        ('stuCrowdRectList', NET_CROWD_RECT_LIST_INFO * 5), # 全局拥挤人群密度列表信息(矩形描述);Crowd list info(rect description)
        ('nGlobalPeopleNum', c_int),                # 检测区全局总人数;The total number of people
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX2)),  # 图片信息数组;Image information array;
        ('nImageInfoNum', c_int),                   # 图片信息个数;Number of picture information;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('byReserved', C_BYTE * 680),               # 保留扩展字节;Reserved;
    ]

class NET_VIDEOSTAT_SUBTOTAL(Structure):
    """
    视频统计小计信息;video statistical subtotal
    """
    _fields_ = [
        ('nTotal', c_int),          #设备运行后人数统计总数;count since device operation
        ('nHour', c_int),           #小时内的总人数;count in the last hour
        ('nToday', c_int),          #当天的总人数, 不可手动清除;count for today
        ('nOSD', c_int),            #统计人数, 用于OSD显示, 可手动清除;count for today, on screen display
        ('reserved', c_char*252),   #保留字节；reserved
    ]

class NET_EXITMAN_STAY_STAT(Structure):
    """
    离开人员的滞留时间信息;The stay time of the peoples left
    """
    _fields_ = [
        ('stuEnterTime', NET_TIME),     #人员进入区域时间;Time to enter the region
        ('stuExitTime', NET_TIME),      #人员离开区域时间;Time to exit the region
        ('reserved', C_BYTE*128),       #保留字节;Reserved
    ]

class NET_NONMOTOR_STAY_STAT(Structure):
    """
    非机动车的滞留时间信息
    nonmotor stay state
    """
    _fields_ = [
        ('stuEnterTime', NET_TIME),  # 非机动车进入区域的时间;Time for non-motorized vehicles to enter the area;
        ('stuExitTime', NET_TIME),  # 非机动车离开区域的时间;Time for non-motorized vehicles to exit the area;
        ('reserved', C_BYTE * 128),  # 保留字节;reserved;
    ]

class NET_PIG_STAY_STAT(Structure):
    """
    猪只离开开滞留时间信息
    Pig Stay Stat info
    """
    _fields_ = [
        ('stuEnterTime', NET_TIME),  # 猪只进入区域的时间;Enter Time;
        ('stuExitTime', NET_TIME),  # 猪只离开区域的时间;Exit Time;
        ('szReserved', c_char * 208),  # 保留字节;Reserved;
    ]

class NET_PASSED_SUBTOTAL_INFO(Structure):
    """
    经过小计信息
    Passed Subtotal Info
    """
    _fields_ = [
        ('nTotal', c_int),  # 设备运行后经过人数统计总数;The total number of people after the equipment is running;
        ('nHour', c_int),  # 小时内的总人数;total number of people during the hour;
        ('nToday', c_int),  # 当天的总人数(自然天);The total number of people on the day (natural days);
        ('nTotalInTimeSection', c_int),  # IPC专用，如果不执行clearSectionStat操作，等同于Today人数;IPC only, if the clearSectionStat operation is not performed, it is equivalent to the number of Today;
        ('szReserved', c_char * 112),  # 保留字节;Reserved bytes;
    ]

class NET_VIDEOSTAT_SUMMARY(Structure):
    """
    视频统计摘要信息;Video statistical summary
    """
    _fields_ = [
        ('nChannelID', c_int),          #通道号;Channel ID
        ('szRuleName', c_char*32),      #规则名称;Rule name
        ('stuTime', NET_TIME_EX),       #统计时间;Time of this statistics
        ('stuEnteredSubtotal', NET_VIDEOSTAT_SUBTOTAL), #进入小计;Subtotal for the entered
        ('stuExitedSubtotal', NET_VIDEOSTAT_SUBTOTAL),  #出去小计;Subtotal for the exited
        ('nInsidePeopleNum', c_uint),                    #区域内人数;Total number of people in the area
        ('emRuleType', C_ENUM),                          #规则类型;Rule type,refer to EM_RULE_TYPE
        ('nRetExitManNum', c_int),                      #离开的人数个数;The count of peoples left
        ('stuExitManStayInfo', NET_EXITMAN_STAY_STAT*32), #离开人员的滞留时间信息;The stay time of the peoples left
        ('nPlanID', c_uint),                             #计划ID,仅球机有效,从1开始;Plan ID,Speed Dome use,start from 1
        ('nAreaID', c_uint),                             #区域ID(一个预置点可以对应多个区域ID);Area ID(a preset point can correspond to multiple area IDs)
        ('nCurrentDayInsidePeopleNum', c_uint),          #当天区域内总人数;Total number of people current day in the area
        ('nInsideTotalNonMotor', C_UINT),               # 区域内非机动车总数;Total number of non-motor vehicles in the area;
        ('nInsideTodayNonMotor', C_UINT),               # 当天的非机动车数;Number of non-motorized vehicles on the day;
        ('nRetNonMotorNum', c_int),                     # 非机动车的滞留个数;Number of non-motor vehicles stranded;
        ('stuNonMotorStayStat', NET_NONMOTOR_STAY_STAT * 32),   # 非机动车的滞留时间信息;Information on the detention time of non-motor vehicles;
        ('nInsideTotalPig', C_UINT),                    # 区域内猪只数;Inside Total Pig Number;
        ('nPigStayStatCount', c_int),                   # 猪只离开滞留时间信息个数;Pig Stay Stat Count;
        ('stuPigStayStatInfo', NET_PIG_STAY_STAT * 32), # 猪只离开滞留时间信息;Pig Stay Stat Info;
        ('nInsideTodayPig', C_UINT),                    # 当天的猪只数;Inside Today Pig Number;
        ('szReserved', c_char * 4),                     # 字节对齐;byte alignment;
        ('stuPassedSubtotal', NET_PASSED_SUBTOTAL_INFO),    # 经过小计;Passed Subtotal Info;
        ('reserved', C_BYTE * 884),                     # 保留字节;Reserved;
    ]

class NET_IN_ATTACH_VIDEOSTAT_SUM(Structure):
    """
    AttachVideoStatSummary 入参;input param for AttachVideoStatSummary
    """
    _fields_ = [
        ('dwSize', C_DWORD),        # 结构体大小;Structure size
        ('nChannel', c_int),        # 视频通道号;video channel ID
        ('cbVideoStatSum', CB_FUNCTYPE(None, C_LLONG, POINTER(NET_VIDEOSTAT_SUMMARY), C_DWORD, C_LDWORD)), # 视频统计摘要信息回调;video statistical summary callback
        ('dwUser', C_LDWORD),       # 用户数据;user data
    ]

class NET_OUT_ATTACH_VIDEOSTAT_SUM(Structure):
    """
    AttachVideoStatSummary 出参;output param for AttachVideoStatSummary
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size
    ]

class NET_TRAFFIC_FLOWSTAT_INFO_DIR(Structure):
    """
    车辆流量统计车辆行驶方向信息;Vehicle flow statistics lane direction information
    """
    _fields_ = [
        ('emDrivingDir', C_ENUM),              # 行驶方向,参考NET_FLOWSTAT_DIRECTION;Driving direction，refer to NET_FLOWSTAT_DIRECTION
        ('szUpGoing', c_char*16),           # 上行地点;Uplink locations
        ('szDownGoing', c_char*16),         # 下行地点;Go down location
        ('reserved', C_BYTE*32),            # 保留字节;Reserved bytes
    ]

class NET_TRAFFIC_FLOW_STATE(Structure):
    """
    流量状态;
    """
    _fields_ = [
        ('nLane', c_int),           # 车道号;Lane number
        ('dwState', C_DWORD),       # 状态值.若emJamState字段为有效值(不为 JAM_STATUS_UNKNOW) ,则dwState字段无效;State value,if emJamState is valid,then dwState is invalid
                                    # 1- 流量过大;1 - heavy traffic
                                    # 2- 流量过大恢复;2-heavy traffic recovery
                                    # 3- 正常;3-normal;
                                    # 4- 流量过小;4 - Flow is too  little
                                    # 5- 流量过小恢复;5-Traffic too low recovery
        ('dwFlow', C_DWORD),        # 流量值, 单位: 辆;Flow value, units: vehicles
        ('dwPeriod', C_DWORD),      # 流量值对应的统计时间, 单位:分钟。与dwPeriodByMili一起使用;Corresponding statistical time of the flow value,Unit:minute,Used with dwPeriodByMili.
        ('stTrafficFlowDir', NET_TRAFFIC_FLOWSTAT_INFO_DIR),  # 车道方向信息;Lane direction information
        ('nVehicles', c_int),       # 通过车辆总数;Total number of passing vehicles
        ('fAverageSpeed', c_float), # 平均车速,单位km/h;Average speed, unit km / h
        ('fAverageLength', c_float),    # 平均车长,单位米;The average vehicle length, unit meters
        ('fTimeOccupyRatio', c_float),  # 时间占有率,即单位时间内通过断面的车辆所用时间的总和占单位时间的比例;Share of the time , i.e., The ratio of the sum time for the vehicle passing the cross-section  in  the unit  time and per unit time
        ('fSpaceOccupyRatio', c_float), # 空间占有率,即按百分率计量的车辆长度总和除以时间间隔内车辆平均行驶距离;Share of the space ,is the result that the average driving distance intervals vehicle is divided the sum of the length of the vehicle measured by the percentage
        ('fSpaceHeadway', c_float),     # 车头间距,相邻车辆之间的距离,单位米/辆;Headway, the distance between adjacent vehicles in m / vehicle
        ('fTimeHeadway', c_float),      # 车头时距,单位秒/辆;Headway in seconds / vehicle
        ('fDensity', c_float),          # 车辆密度,每公里的车辆数,单位辆/km;Vehicle density, the number of vehicles per kilometer, unit vehicles / km
        ('nOverSpeedVehicles', c_int),  # 超速车辆数;The number of Speeding vehicles
        ('nUnderSpeedVehicles', c_int), # 低速车辆数;The number of low speeding vehicles
        ('nLargeVehicles', c_int),      # 大车交通量(9米<车长<12米),辆/单位时间;Carts traffic (9 m <car length <12 m), vehicle / unit time
        ('nMediumVehicles', c_int),     # 中型车交通量(6米<车长<9米),辆/单位时间;Medium car Traffic 6 m <car length <9 meters, vehicle / unit time
        ('nSmallVehicles', c_int),      # 小车交通量(4米<车长<6米),辆/单位时间;Car Traffic 4 m <car length <6 meters), vehicle / unit time
        ('nMotoVehicles', c_int),       # 摩托交通量(微型车,车长<4米),辆/单位时间;Motorized traffic (mini-car, car length <4 m, vehicle / unit time
        ('nLongVehicles', c_int),       # 超长交通量(车长>=12米),辆/单位时间;long traffic (car length> = 12 m), vehicle / unit time
        ('nVolume', c_int),             # 交通量, 辆/单位时间, 某时间间隔通过车道、道路或其他通道上一点的车辆数,常以1小时计;Traffic, vehicles / unit time, the number of vehicles which pass through the lane, the road and other vehicles, caculated in one hour
        ('nFlowRate', c_int),           # 流率小车当量,辆/小时, 车辆通过车道、道路某一断面或某一路段的当量小时流量;Flow rate of the car, Vehicles / hour, equivalent hours for Vehicle through the lane, a section or a section of the road
        ('nBackOfQueue', c_int),        # 排队长度,单位：米, 从信号交叉口停车线到上游排队车辆末端之间的距离(建议废掉 改用dBackOfQueue下面);Queue length, unit: m, distance from the signalized intersection stop line between the upstream end of the line vehicle)(proposed repeal)
        ('nTravelTime', c_int),         # 旅行时间,单位：秒, 车辆通过某一条道路所用时间。包括所有停车延误;Travel time, unit: second, a road vehicle used by a certain time. Including all parking delays
        ('nDelay', c_int),              # 延误,单位：秒,驾驶员、乘客或行人花费的额外的行程时间;Delay unit: seconds, extra travel time for the driver, passenger or pedestrian spend
        ('byDirection', C_BYTE*16),     # 车道方向, 详见NET_ROAD_DIRECTION;lane direction, see NET_ROAD_DIRECTION
        ('byDirectionNum', C_BYTE),     # 车道行驶方向个数;lane direction quantity
        ('reserved1', C_BYTE*3),        # 字节对齐;text align
        ('emJamState', C_ENUM),            # 道路拥挤状况,详见NET_TRAFFIC_JAM_STATUS，若此字段为有效值(不为 JAM_STATUS_UNKNOW) ,则以此字段为准, dwState字段无效;road jam status, refer to NET_TRAFFIC_JAM_STATUS. if emJamState is valid,then dwState is invalid
        #  按车辆类型统计交通量;Traffic statisitcs according to vehicle type
        ('nPassengerCarVehicles', c_int),  # 客车交通量(辆/单位时间);Passenger vehicle statistics amount (amount/hour)
        ('nLargeTruckVehicles', c_int), # 大货车交通量(辆/单位时间);Large truck statistics amount
        ('nMidTruckVehicles', c_int),   # 中货车交通量(辆/单位时间);Medium truck statistics amount (amount/hour)
        ('nSaloonCarVehicles', c_int),  # 轿车交通量(辆/单位时间);Car statistics amount (amount/hour)
        ('nMicrobusVehicles', c_int),   # 面包车交通量(辆/单位时间);Minivan statistics amount (amount/hour)
        ('nMicroTruckVehicles', c_int), # 小货车交通量(辆/单位时间);Small van statistics amount (amount/hour)
        ('nTricycleVehicles', c_int),   # 三轮车交通量(辆/单位时间);Tricycle statistics amount (amount/hour)
        ('nMotorcycleVehicles', c_int), # 摩托车交通量(辆/单位时间);Motor statistics amount (amount/hour)
        ('nPasserbyVehicles', c_int),   # 行人交通量(辆/单位时间);Pedestrian statistics amount (amount/hour)
        ('emRank', C_ENUM),              # 道路等级,详见NET_TRAFFIC_ROAD_RANK;road rank,refer to NET_TRAFFIC_ROAD_RANK
        ('nState', c_int),              # 流量状态;State value
                                        # 1- 流量过大(拥堵);1 - heavy traffic
                                        # 2- 流量过大恢复(略堵);2-heavy traffic recovery
                                        # 3- 正常;3-normal
                                        # 4- 流量过小(通畅);4 - Flow is too  little
                                        # 5- 流量过小恢复(良好);5-Traffic too low recovery
        ('bOccupyHeadCoil', C_BOOL),    # 车头虚拟线圈是否被占用 TURE表示占用，FALSE表示未占用;indicating whether the head coil is occupyied
        ('bOccupyTailCoil', C_BOOL),    # 车尾虚拟线圈是否被占用 TURE表示占用，FALSE表示未占用;indicating whether the tail coil is occupyied
        ('bStatistics', C_BOOL),        # 流量数据是否有效 TURE表示有效，FALSE表示无效;indicating whether the statistics is valid
        ('nLeftVehicles', c_int),       # 左转车辆总数,单位:分钟;Total nubmer of turn left Vehicles, unit: min
        ('nRightVehicles', c_int),      # 右转车辆总数,单位:分钟;Total number of turn right Vehicles, unit: min
        ('nStraightVehicles', c_int),   # 直行车辆总数,单位:分钟;Total number of straight-head Vehicles,unit: min
        ('nUTurnVehicles', c_int),      # 掉头车辆总数,单位:分钟;Total number of U-turn Vehicles,unit: min
        ('stQueueEnd', SDK_POINT),      # 每个车道的最后一辆车坐标,采用8192坐标系;the last car coordinate in a quene of lane,coordinate value 0~8192
        ('dBackOfQueue', c_double),     # 排队长度,单位：米, 从信号交叉口停车线到上游排队车辆末端之间的距离;Queue length, unit: m, distance from the signalized intersection stop line between the upstream end of the line vehicle
        ('dwPeriodByMili', C_DWORD),    # 流量值的毫秒时间,值不超过60000,和dwPeriod一起使用,流量值总时间:dwPeriod*60*1000+dwPeriodByMili(单位：毫秒);
                                        # Corresponding statistical time of the flow millisecond value,Value is not more than 60000.Used with dwPeriod,statistical total time of the flow value:dwPeriod*60*1000+dwPeriodByMili(Unit:millisecond)
        ('nBusVehicles', c_int),        # 公交车交通量(辆/单位时间);Bus vehicle statistics amount (amount/hour)
        ('nMPVVehicles', c_int),        # MPV交通量(辆/单位时间);MPV vehiclestatistics amount (amount/hour)
        ('nMidPassengerCarVehicles', c_int),  # 中客车交通量(辆/单位时间);midpassenger car vehicle statistics amount (amount/hour)
        ('nMiniCarriageVehicles', c_int),   # 微型轿车交通量(辆/单位时间);mini carriage vehicle statistics amount (amount/hour)
        ('nOilTankTruckVehicles', c_int),   # 油罐车交通量(辆/单位时间);oil tank trunk vehicle statistics amount (amount/hour)
        ('nPickupVehicles', c_int),         # 皮卡车交通量(辆/单位时间);pick up vehicle statistics amount (amount/hour)
        ('nSUVVehicles', c_int),        # SUV交通量(辆/单位时间);SUV vehicle statistics amount (amount/hour)
        ('nSUVorMPVVehicles', c_int),   # SUV或者MPV交通量(辆/单位时间);SUV or MPV vehicle statistics amount (amount/hour)
        ('nTankCarVehicles', c_int),    # 槽罐车交通量(辆/单位时间);tank car vehicle statistics amount (amount/hour)
        ('nUnknownVehicles', c_int),    # 未知车辆交通量(辆/单位时间);unknown vehicle statistics amount (amount/hour)
        ('emCustomFlowAttribute', C_ENUM),   # 车道流量信息属性,详见NET_EM_FLOW_ATTRIBUTE;Flow attribute,refer to NET_EM_FLOW_ATTRIBUTE
        ('nRoadFreeLength', c_int),     # 道路空闲长度，例：如设定路段长度为100米，实际检测到排队长度为30米，那么道路空闲长度就为70米，单位：米;Road Free Length. unit:meter;
        ('emOverflowState', C_ENUM),    # 溢出状态。例：如给当前路段设定允许排队长度阀值，实际排队长度超过阀值后就判定当前时刻该路段有溢出。 Refer: EM_A_NET_EM_OVER_FLOW_STATE;overflow state of car queue. Refer: EM_A_NET_EM_OVER_FLOW_STATE;
        ('reserved', C_BYTE * 712),     # 保留字节;Reserved
    ]

class NET_A_ALARM_TRAFFIC_FLOW_STAT_INFO(Structure):
    """
    交通路口车道统计事件 (对应 ALARM_TRAFFIC_FLOW_STAT)
    Statistical events of traffic intersection Lane (corresponding to ALARM_TRAFFIC_FLOW_STAT)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作 0:脉冲;0: pulse;
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('PTS', C_DWORD),  # 时间戳(单位是毫秒);Timestamp (in milliseconds);
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间;Time of event;
        ('nSequence', c_int),  # 序号;Indicates the capture sequence number. 1 indicates the normal end of the capture. 0 indicates the abnormal end of the capture;
        ('nStateNum', c_int),  # 流量状态数量;Number of flow states;
        ('stuStates', NET_TRAFFIC_FLOW_STATE * 8),  # 流量状态, 每个车道对应数组中一个元素;Flow status, each lane corresponds to an element in the array;
        ('nStopVehiclenum', c_int),  # 静止车辆数，当前时刻检测范围内车速小于某个阀值的车辆数，单位：辆;Number of stationary vehicles: the number of vehicles whose speed is less than a certain threshold within the detection range at the current time, unit: vehicle;
        ('nDetectionAreaVehicleNum', c_int),  # 车辆总数，当前时刻检测范围内检测到的所有车道内的车辆总数，单位：辆;Total number of vehicles: the total number of vehicles in all lanes detected within the detection range at the current time, unit: vehicles;
        ('szReserverd', c_char * 1024),  # 保留字节;Reserved;
    ]

class NET_DATA_CALL_BACK_TIME(Structure):
    """
    回调数据时间信息; callback data time information
    """
    _fields_ = [
        ('dwYear', C_DWORD),    # 年; year
        ('dwMonth', C_DWORD),   # 月; month
        ('dwDay', C_DWORD),     # 日; day
        ('dwHour', C_DWORD),    # 时; hour
        ('dwMinute', C_DWORD),  # 分; minute
        ('dwSecond', C_DWORD),  # 秒; second
        ('dwMillisecond', C_DWORD), # 毫秒; millisecond
        ('dwPTS', C_DWORD),     # pts时间戳; pts timestamp
        ('dwDTS', C_DWORD),     # dts时间戳; dts timestamp
        ('dwReserved', C_DWORD * 3),    # 预留字段; Reserved bytes
    ]

class NET_DATA_CALL_BACK_INFO(Structure):
    """
    回调数据信息; callback data information
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; struct size
        ('dwDataType', C_DWORD),    # 数据类型; data type
        ('pBuffer', c_char_p),      # 数据; data
        ('dwBufSize', C_DWORD),     # 数据长度; data size
        ('stuTime', NET_DATA_CALL_BACK_TIME), # 时间戳; timestamp
        ('emFramType', C_ENUM),     # 帧类型 具体参考EM_DATA_CALL_BACK_FRAM_TYPE; Frame Type Specific Reference EM_DATA_CALL_BACK_FRAM_TYPE
        ('emFramSubType', C_ENUM),  # 帧子类型 具体参考EM_DATA_CALL_BACK_FRAM_SUB_TYPE; Frame Subtype Specific Reference EM_DATA_CALL_BACK_FRAM_SUB_TYPE
    ]

class DEV_EVENT_TRAFFIC_FLOW_STATE(Structure):
    """
    事件类型 FLOWSTATE(交通流量事件)对应数据块描述信息;FLOWSTATE (Corresponding data block description)
    """
    _fields_ = [
        ('nChannelID', c_int),          # 通道号;Channel number
        ('szName', c_char*128),         # 事件名称;Event name
        ('nRuleID', c_uint),            # 规则编号, 用于标示哪个规则触发的事件，缺省时默认为0;Rule ID, used to indicate which rule triggers the event.
        ('bReserved1', c_char*4),       # 字节对齐;Byte alignment
        ('PTS', C_DWORD),               # 时间戳(单位是毫秒);Timestamp (in milliseconds)
        ('UTC', NET_TIME_EX),           # 事件发生的时间;Time for the event occurred
        ('nEventID', c_int),            # 事件ID;Event ID
        ('nSequence', c_int),           # 序号;No.
        ('nStateNum', c_int),           # 流量状态数量;the number of traffic state
        ('stuStates', NET_TRAFFIC_FLOW_STATE*8),  # 流量状态, 每个车道对应数组中一个元素;Flow state, each lane corresponding to an element in the array
        ('stuIntelliCommInfo', EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info
        ('nStopVehiclenum', c_int),
        # 静止车辆数，当前时刻检测范围内车速小于某个阀值的车辆数，单位：辆;Vehicle count of speed lower than the threshold value;
        ('nDetectionAreaVehicleNum', c_int),  # 车辆总数，当前时刻检测范围内检测到的所有车道内的车辆总数，单位：辆;Vehicle count in the detection area;
        ('bReserved', C_BYTE * 884),  # 保留字节;(Reserved bytes);
    ]

class NET_IN_REALPLAY_BY_DATA_TYPE(Structure):
    """
    开始实时预览并指定回调数据格式入参;RealPlay By Stream Data Type (in param)
    """
    _fields_ = [
        ('dwSize', C_DWORD),                        # 结构体大小; struct size
        ('nChannelID', c_int),                      # 通道编号; channel id
        ('hWnd', C_LLONG),                          # 窗口句柄; play handle
        ('rType', C_ENUM),                          # 码流类型,详见SDK_RealPlayType; real play stream type,refer to SDK_RealPlayType
        ('cbRealData', CB_FUNCTYPE(None, C_LLONG, C_DWORD, POINTER(c_byte), C_DWORD, C_LLONG, C_LDWORD)),        # 数据回调函数,对应SDK_Callback的fRealDataCallBackEx; realplay data callback function prototype，corresponding to SDK_Callback's fRealDataCallBackEx
        ('emDataType', C_ENUM),                     # 回调的数据类型,详见EM_REAL_DATA_TYPE; stream data type,refer to EM_REAL_DATA_TYPE
        ('dwUser', C_LDWORD),                       # 用户数据; data user
        ('szSaveFileName', c_char_p),               # 转换后的文件名; file name to convert
        ('cbRealDataEx', CB_FUNCTYPE(None, C_LLONG, C_DWORD, POINTER(c_byte), C_DWORD, C_LLONG, C_LDWORD)),     # 数据回调函数-扩展,对应SDK_Callback的fRealDataCallBackEx2; realplay data callback function prototype-ex，corresponding to SDK_Callback's fRealDataCallBackEx2
        ('emAudioType', C_ENUM),                    # 音频格式,详见EM_AUDIO_DATA_TYPE; audio data type, refer to EM_AUDIO_DATA_TYPE
        ('cbRealDataEx2', CB_FUNCTYPE(c_int, C_LLONG, POINTER(NET_DATA_CALL_BACK_INFO), C_LDWORD)), # 数据回调（扩展带时间戳，帧类型）;realplay data callbackExtension(With time stamp, frame type);
    ]

class NET_OUT_REALPLAY_BY_DATA_TYPE(Structure):
    """
    开始实时预览并指定回调数据格式出参;RealPlay By Stream Data Type (out param)
    """
    _fields_ = [
        ('dwSize', C_DWORD),                        # 结构体大小; struct size
    ]

class NET_IN_PLAYBACK_BY_DATA_TYPE(Structure):
    """
    开始回放并指定回调数据格式入参;Start playback and specify the callback data format Input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; struct size
        ('nChannelID', c_int),  # 通道编号; channel id
        ('stStartTime', NET_TIME),  # 开始时间; start time
        ('stStopTime', NET_TIME),   # 结束时间; end time
        ('hWnd', C_LLONG),  # 窗口句柄; play handle
        ('cbDownLoadPos', CB_FUNCTYPE(None, C_LLONG, C_DWORD, C_DWORD, C_LDWORD)),  # 进度回调;progress callback
        ('dwPosUser', C_LDWORD),    # 进度回调用户信息; Progress callback user information
        ('fDownLoadDataCallBack', CB_FUNCTYPE(c_int, C_LLONG, C_DWORD, POINTER(c_ubyte), C_DWORD, C_LDWORD)),    # 数据回调; data callback
        ('emDataType', C_ENUM),  # 回调的数据类型,详见EM_REAL_DATA_TYPE; stream data type,refer to EM_REAL_DATA_TYPE
        ('dwDataUser', C_LDWORD),   # 数据回调用户信息; Data callback user information
        ('nPlayDirection', c_int),  # 播放方向, 0:正放; 1:倒放; Play direction, 0: play forward; 1: play backward
        ('emAudioType', C_ENUM),  # 音频格式,详见EM_AUDIO_DATA_TYPE; audio data type, refer to EM_AUDIO_DATA_TYPE
        ('fDownLoadDataCallBackEx', CB_FUNCTYPE(c_int, C_LLONG, POINTER(NET_DATA_CALL_BACK_INFO), C_LDWORD)) # 数据回调（扩展带时间戳，帧类型）; Data callback (extended with timestamp, frame type)
    ]

class NET_OUT_PLAYBACK_BY_DATA_TYPE(Structure):
    """
    开始回放并指定回调数据格式出参;Start playback and specify the callback data format Output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; struct size
    ]

class NET_IN_DOWNLOAD_BY_DATA_TYPE(Structure):
    """
    开始下载并指定回调数据格式 入参; Start the download and specify the callback data format Input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),        # 结构体大小; struct size
        ('nChannelID', c_int),      # 通道编号; channel id
        ('emRecordType', C_ENUM),   # 录像类型 参考EM_QUERY_RECORD_TYPE; record type, refer to EM_QUERY_RECORD_TYPE
        ('szSavedFileName', c_char_p),  # 下载的文件路径; Downloaded file path
        ('stStartTime', NET_TIME),  # 开始时间; start time
        ('stStopTime', NET_TIME),  # 结束时间; end time
        ('cbDownLoadPos', CB_FUNCTYPE(None, C_LLONG, C_DWORD, C_DWORD, c_int, NET_RECORDFILE_INFO, C_LDWORD)),  # 进度回调;progress callback
        ('dwPosUser', C_LDWORD),  # 进度回调用户信息; Progress callback user information
        ('fDownLoadDataCallBack', CB_FUNCTYPE(c_int, C_LLONG, C_DWORD, POINTER(c_ubyte), C_DWORD, C_LDWORD)),   # 数据回调; data callback
        ('emDataType', C_ENUM),  # 回调的数据类型,详见EM_REAL_DATA_TYPE; stream data type,refer to EM_REAL_DATA_TYPE
        ('dwDataUser', C_LDWORD),  # 数据回调用户信息; Data callback user information
        ('emAudioType', C_ENUM),  # 音频格式,详见EM_AUDIO_DATA_TYPE; audio data type, refer to EM_AUDIO_DATA_TYPE
    ]

class NET_OUT_DOWNLOAD_BY_DATA_TYPE(Structure):
    """
        开始下载并指定回调数据格式 出参; Start the download and specify the callback data format Output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; struct size
    ]

class NET_CTRL_RAINBRUSH_MOVEONCE(Structure):
    """
    雨刷来回刷一次,雨刷模式配置为手动模式时有效(对应命令CtrlType.RAINBRUSH_MOVEONCE); (corresponding to CtrlType.RAINBRUSH_MOVEONCE)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannel', c_int),  # 表示雨刷的索引; Rain-brush channel;
    ]

class NET_CTRL_RAINBRUSH_MOVECONTINUOUSLY(Structure):
    """
    雨刷来回循环刷,雨刷模式配置为手动模式时有效(对应命令 CtrlType.RAINBRUSH_MOVECONTINUOUSLY); (corresponding to CtrlType.RAINBRUSH_MOVECONTINUOUSLY)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannel', c_int),  # 表示雨刷的索引; Rain-brush channel;
        ('nInterval', C_UINT),  # 雨刷间隔; Interval;
    ]

class NET_CTRL_RAINBRUSH_STOPMOVE(Structure):
    """
    雨刷停止刷,雨刷模式配置为手动模式时有效(对应命令 CtrlType.RAINBRUSH_STOPMOVE); (corresponding to CtrlType.RAINBRUSH_STOPMOVE)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannel', c_int),  # 表示雨刷的索引; Rain-brush channel;
    ]

class NET_ANGEL_RANGE(Structure):
    """
    人脸抓拍角度范围; Face capture angle range
    """
    _fields_ = [
        ('nMin', c_int),    # 角度最小值; Minimum angle;
        ('nMax', c_int),    # 角度最大值; Maximum angle;
    ]

class NET_EVENT_WHOLE_FACE_INFO(Structure):
    """
    人脸抓拍角度范围; Face capture angle range
    """
    _fields_ = [
        ('stuFaceCaptureAngle', NET_EULER_ANGLE),       # 人脸在抓拍图片中的角度信息, nPitch:抬头低头的俯仰角, nYaw左右转头的偏航角, nRoll头在平面内左偏右偏的翻滚角,角度值取值范围[-90,90], 三个角度值都为999表示此角度信息无效; The angle information of the face in the captured image, nPitch: the pitch angle of the head up and down, the yaw angle of the nYaw left and right head, and the roll angle of the nRoll head in the plane left and right,Angle value range [-90,90], all three angle values are 999, indicating that the angle information is invalid;
        ('stuAngelRange', NET_ANGEL_RANGE * 3),         # 人脸抓拍角度范围(角度最小值,最大值),  三个角度依次分别是Pitch抬头低头,仰俯角;yaw是左右转头,偏航角;Roll是头在平面内左偏右偏，翻滚角; Face capture angle range (minimum angle, maximum angle), the three angles are Pitch up and down, pitch and pitch angles; yaw is left and right turn head, yaw angle; Roll is head left and right in the plane, roll angle;
        ('byReserved', C_BYTE * 256),                   # 保留字段; Reserved
    ]

class ALARM_EVENT_FACE_INFO(Structure):
    """
    人脸检测事件(对应事件 DH_EVENT_FACE_DETECTION); Human face detect event( corresponding to event DH_EVENT_FACE_DETECTION)
    """
    _fields_ = [
        ('dwSize', C_DWORD),                            # 结构体大小;Structure size
        ('nChannelID', c_int),                          # 通道号; Channel No.;
        ('PTS', c_double),                              # 时间戳(单位是毫秒); Time stamp (Unit is ms);
        ('UTC', NET_TIME_EX),                           # 事件发生的时间; Event occurrence time;
        ('nEventID', c_int),                            # 事件ID; Event ID;
        ('nEventAction', c_int),                        # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;; Event operation. 0=pulse event.1=continues event begin. 2=continuous event stop;
        ('nFaceCount', c_int),                          # 人脸个数; face count
        ('stuFaces', NET_EVENT_WHOLE_FACE_INFO * 10),   # 人脸信息; face info
        ('nPresetID', C_UINT),                          # 事件触发的预置点号, 从1开始; Preset point number triggered by event, starting from 1
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),      # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class AV_CFG_Color(Structure):
    """
    颜色;Color
    """
    _fields_ = [
        ('nStructSize', c_int), # 结构体大小;Structure size
        ('nRed', c_int), # 红; Red;
        ('nGreen', c_int), # 绿; Green;
        ('nBlue', c_int), # 蓝; Blue;
        ('nAlpha', c_int), # 透明; Transparent;
    ]

class AV_CFG_Rect(Structure):
    """
    区域;Zone
    """
    _fields_ = [
        ('nStructSize', c_int), # 结构体大小;Structure size
        ('nLeft', c_int), # 左; Left
        ('nTop', c_int), # 顶; Top
        ('nRight', c_int), # 右; Right
        ('nBottom', c_int),  # 底; Bottom
    ]

class AV_CFG_VideoWidgetChannelTitle(Structure):
    """
    编码物件-通道标题;Encode widget-channel title
    """
    _fields_ = [
        ('nStructSize', c_int),   # 结构体大小;Structure size
        ('bEncodeBlend', C_BOOL), # 叠加到主码流; Overlay to main stream;
        ('bEncodeBlendExtra1', C_BOOL), # 叠加到辅码流1; Overlay to extra stream 1;
        ('bEncodeBlendExtra2', C_BOOL), # 叠加到辅码流2; Overlay to extra stream 2;
        ('bEncodeBlendExtra3', C_BOOL), # 叠加到辅码流3; Overlay to extra stream 3;
        ('bEncodeBlendSnapshot', C_BOOL), # 叠加到抓图; Add to snap;
        ('stuFrontColor', AV_CFG_Color), # 前景色; Foreground color;
        ('stuBackColor', AV_CFG_Color), # 背景色; Background color;
        ('stuRect', AV_CFG_Rect), # 区域, 坐标取值0~8191, 仅使用left和top值, 点(left,top)应和(right,bottom)设置成同样的点; Zone. The coordinates value ranges from 0 to 8191. Only use left value and top value.The point (left,top) shall be the same as the point(right,bottom).;
        ('bPreviewBlend', C_BOOL), # 叠加到预览视频; Overlay to preview mode;
    ]

class AV_CFG_VideoWidgetTimeTitle(Structure):
    """
    编码物件-时间标题;Encode widget-Time title
    """
    _fields_ = [
        ('nStructSize', c_int),     # 结构体大小;Structure size
        ('bEncodeBlend', C_BOOL), # 叠加到主码流; Overlay to main stream;
        ('bEncodeBlendExtra1', C_BOOL), # 叠加到辅码流1; Overlay to extra stream 1;
        ('bEncodeBlendExtra2', C_BOOL), # 叠加到辅码流2; Overlay to extra stream 2;
        ('bEncodeBlendExtra3', C_BOOL), # 叠加到辅码流3; Overlay to extra stream 3;
        ('bEncodeBlendSnapshot', C_BOOL), # 叠加到抓图; Overlay to snap;
        ('stuFrontColor', AV_CFG_Color), # 前景色; Foreground color;
        ('stuBackColor', AV_CFG_Color), # 背景色; Background color;
        ('stuRect', AV_CFG_Rect), # 区域, 坐标取值0~8191, 仅使用left和top值, 点(left,top)应和(right,bottom)设置成同样的点; Zone. The coordinates value ranges from 0 to 8191. Only use left value and top value.The point (left,top) shall be the same as the point(right,bottom).;
        ('bShowWeek', C_BOOL), # 是否显示星期; Display week or not;
        ('bPreviewBlend', C_BOOL), # 叠加到预览视频; Overlay to preview mode;
    ]

class AV_CFG_VideoWidgetCover(Structure):
    """
    编码物件-区域覆盖配置;Encode widget-Privacy mask setup
    """
    _fields_ = [
        ('nStructSize', c_int),    # 结构体大小;Structure size
        ('bEncodeBlend', C_BOOL), # 叠加到主码流; Overlay to main stream;
        ('bEncodeBlendExtra1', C_BOOL), # 叠加到辅码流1; Overlay to extra stream 1;
        ('bEncodeBlendExtra2', C_BOOL), # 叠加到辅码流2; Overlay to extra stream 2;
        ('bEncodeBlendExtra3', C_BOOL), # 叠加到辅码流3; Overlay to extra stream 3;
        ('bEncodeBlendSnapshot', C_BOOL), # 叠加到抓图; Overlay to snap;
        ('stuFrontColor', AV_CFG_Color), # 前景色; Foreground color;
        ('stuBackColor', AV_CFG_Color), # 背景色; Background color;
        ('stuRect', AV_CFG_Rect), # 区域, 坐标取值0~8191; Zone. The coordinates value ranges from 0 to 8191;
        ('bPreviewBlend', C_BOOL), # 叠加到预览视频; Overlay to preview mode;
    ]

class AV_CFG_VideoWidgetCustomTitle(Structure):
    """
    编码物件-自定义标题;Encode widget-Self-defined title
    """
    _fields_ = [
        ('nStructSize', c_int),    # 结构体大小;Structure size
        ('bEncodeBlend', C_BOOL), # 叠加到主码流; Overlay to main stream;
        ('bEncodeBlendExtra1', C_BOOL), # 叠加到辅码流1; Overlay to extra stream 1;
        ('bEncodeBlendExtra2', C_BOOL), # 叠加到辅码流2; Overlay to extra stream 2;
        ('bEncodeBlendExtra3', C_BOOL), # 叠加到辅码流3; Overlay to extra stream 3;
        ('bEncodeBlendSnapshot', C_BOOL), # 叠加到抓图; Overlay to snap;
        ('stuFrontColor', AV_CFG_Color), # 前景色; Foreground color;
        ('stuBackColor', AV_CFG_Color), # 背景色; Background color;
        ('stuRect', AV_CFG_Rect), # 区域, 坐标取值0~8191, 仅使用left和top值, 点(left,top)应和(right,bottom)设置成同样的点; Zone. The coordinates value ranges from 0 to 8191. Only use left value and top value.The point (left,top) shall be the same as the point(right,bottom).;
        ('szText', c_char * 1024), # 标题内容; Title contents;
        ('bPreviewBlend', C_BOOL), # 叠加到预览视频; Overlay to preview mode;
        ('szType', c_char * 32), # 标题类型 "Rtinfo" 实时刻录信息 "Custom" 自定义叠加、温湿度叠加 "Title" :片头信息 "Check" 校验码,地理信息 "Geography" ATM卡号信息 "ATMCardInfo" 摄像机编号 "CameraID"; Title type "Rtinfo" real-time recorder information, "Custom" custom overlay, temperature and humidity overlay, "Title": credit information "Check" check code,Geography info "Geography" ATM card info "ATMCardInfo" Camera ID "CameraID";
        ('emTextAlign', C_ENUM), # 标题对齐方式,参考枚举 EM_TITLE_TEXT_ALIGN; Title alignment method,Please refer to EM_TITLE_TEXT_ALIGN;
        ('bUpdate', C_BOOL),    # 是否需要设备端更新叠加内容 true:更新 false:不更新;Do you need to update the overlay content on the device side; true: update , false: do not update;
    ]

class AV_CFG_VideoWidgetSensorInfo_Description(Structure):
    """
    编码物件-叠加传感器信息-叠加内容描述;Encoding object - overlay sensor information - superimposed Description
    """
    _fields_ = [
        ('nStructSize', c_int),   # 结构体大小;Structure size
        ('nSensorID', c_int), # 需要描述的传感器的ID(即模拟量报警通道号); Need to describe the sensor ID (analog alarm channel number);
        ('szDevID', c_char * 32), # 设备ID; 璁惧ID;
        ('szPointID', c_char * 32), # 测点ID; 娴嬬偣ID;
        ('szText', c_char * 256), # 需要叠加的内容; 闇€瑕佸彔鍔犵殑鍐呭;
    ]

class AV_CFG_VideoWidgetSensorInfo(Structure):
    """
    编码物件-叠加传感器信息;Encoding object - overlay sensor information
    """
    _fields_ = [
        ('nStructSize', c_int),     # 结构体大小;Structure size
        ('bPreviewBlend', C_BOOL), # 叠加到预览视频; Overlay the preview video;
        ('bEncodeBlend', C_BOOL), # 叠加到主码流视频编码; Stack to the main stream of video coding;
        ('stuRect', AV_CFG_Rect), # 区域, 坐标取值0~8191; Area, coordinates ranging from 0 to 8191;
        ('nDescriptionNum', c_int), # 叠加区域描述数目; The Description number of stacking area;
        ('stuDescription', AV_CFG_VideoWidgetSensorInfo_Description * 4), # 叠加区域描述信息; Stacking area description information;
    ]

class AV_CFG_VideoWidget(Structure):
    """
    视频编码物件配置;Video encode widget config
    """
    _fields_ = [
        ('nStructSize', c_int),  # 结构体大小;Structure size
        ('stuChannelTitle', AV_CFG_VideoWidgetChannelTitle), # 通道标题; Channel title;
        ('stuTimeTitle', AV_CFG_VideoWidgetTimeTitle), # 时间标题; Time title;
        ('nConverNum', c_int), # 区域覆盖数量; Privacy mask zone amount;
        ('stuCovers', AV_CFG_VideoWidgetCover * 16), # 覆盖区域; Privacy mask zone;
        ('nCustomTitleNum', c_int), # 自定义标题数量; Self-defined title amount;
        ('stuCustomTitle', AV_CFG_VideoWidgetCustomTitle * 8), # 自定义标题; Self-defined title;
        ('nSensorInfo', c_int), # 传感器信息叠加区域数目; The number of sensor information overlay area;
        ('stuSensorInfo', AV_CFG_VideoWidgetSensorInfo * 2), # 传感器信息叠加区域信息; Sensor information overlay zone information;
        ('fFontSizeScale', c_double), # 叠加字体大小放大比例,当fFontSizeScale≠0时,nFontSize不起作用,当fFontSizeScale=0时,nFontSize起作用,设备默认fFontSizeScale=1.0,如果需要修改倍数，修改该值,如果需要按照像素设置，则置该值为0，nFontSize的值生效; overlay font size scale;
        ('nFontSize', c_int), # 叠加到主码流上的全局字体大小,单位 px.,和fFontSizeScale共同作用; global font size overlay to main stream, unit px.;
        ('nFontSizeExtra1', c_int), # 叠加到辅码流1上的全局字体大小,单位 px; global font size overlay to sub stream 1, unit px.;
        ('nFontSizeExtra2', c_int), # 叠加到辅码流2上的全局字体大小,单位 px; global font size overlay to sub stream 2, unit px.;
        ('nFontSizeExtra3', c_int), # 叠加到辅码流3上的全局字体大小,单位 px; global font size overlay to sub stream 3, unit px.;
        ('nFontSizeSnapshot', c_int), # 叠加到抓图流上的全局字体大小, 单位 px; global font size overlay to snapshot stream, unit px;
        ('nFontSizeMergeSnapshot', c_int), # 叠加到抓图流上合成图片的字体大小,单位 px; combination picture overlay to snapshot stream, unit px;
        ('emFontSolutionSnapshot', C_ENUM), # 叠加到抓图流上的字体方案,参考枚举EM_FONT_SOLUTION; combination picture overlay to font solution,Please refer to EM_FONT_SOLUTION;
        ('stuGPSTitle', AV_CFG_VideoWidgetCover),  # GPS标题显示, 车载设备用;GPS title;
        ('stuCarNoTitle', AV_CFG_VideoWidgetCover),  # 车牌标题显示, 车载设备用;Plate title;
        ('szChannelName', c_char * 256),  # 通道名称(只为Onvif使用);Channel Name(Only for Onvif);
    ]

class NET_ENCODE_CHANNELTITLE_INFO(Structure):
    """
    通道名称配置;channel title info
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小;Structure size
        ('szChannelName', c_char * 256),   # 通道名称;Channel name
    ]

class SDK_CPU_INFO(Structure):
    """
    CPU信息;CPU info
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('nUsage', c_int), # CPU利用率; CPU usage;
    ]

class SDK_CPU_STATUS(Structure):
    """
    CPU状态;CPU status
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('bEnable', C_BOOL), # 查询是否成功; Search succeeded or not;
        ('nCount', c_int), # CPU数量; CPU amount;
        ('stuCPUs', SDK_CPU_INFO * 16), # CPU信息; CPU info;
    ]

class SDK_MEMORY_INFO(Structure):
    """
    内存信息;Memory info
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('dwTotal', C_DWORD), # 总内存, M; Total memory, M;
        ('dwFree', C_DWORD), # 剩余内存, M; Free memory, M;
    ]

class SDK_MEMORY_STATUS(Structure):
    """
    内存状态;Memory status
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('bEnable', C_BOOL), # 查询是否成功; Search succeeded or not;
        ('stuMemory', SDK_MEMORY_INFO), # 内存信息; Memory info;
    ]

class SDK_FAN_INFO(Structure):
    """
    风扇信息;Fan info
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('szName', c_char * 64), # 名称; Name;
        ('nSpeed', C_DWORD), # 速度; Speed;
    ]

class SDK_FAN_STATUS(Structure):
    """
    风扇状态;Fan status
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('bEnable', C_BOOL), # 查询是否成功; Search succeeded or not;
        ('nCount', c_int), # 风扇数量; Fan amount;
        ('stuFans', SDK_FAN_INFO * 16), # 风扇状态; Fan status;
    ]

class SDK_POWER_INFO(Structure):
    """
    电源信息;Power info
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('bPowerOn', C_BOOL), # 电源状态, 0-关闭, 1-打开, 2-打开但有故障; Power is on or not;
        ('emCurrentState', C_ENUM), # 电源电流状态,参考枚举EM_CURRENT_STATE_TYPE; power current status,Please refer to EM_CURRENT_STATE_TYPE;
        ('emVoltageState', C_ENUM), # 电源电压状态,参考枚举EM_VOLTAGE_STATE_TYPE; power voltage status,Please refer to EM_VOLTAGE_STATE_TYPE;
    ]

class SDK_BATTERY_INFO(Structure):
    """
    电池信息;Battery Information
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('nPercent', c_int), # 电池容量百分比; Battery Capacity Percentage;
        ('bCharging', C_BOOL), # 是否正在充电; Whether real charging;
        ('emExistState', C_ENUM), # 电池在位状态,参考枚举EM_BATTERY_EXIST_STATE; battery in-place status,Please refer to EM_BATTERY_EXIST_STATE;
        ('emState', C_ENUM), # 电池电量状态,参考枚举EM_BATTERY_STATE; battery power status,Please refer to EM_BATTERY_STATE;
        ('fVoltage', c_float), # 电池电压; battery voltage;
        ('emTemperState', C_ENUM),# 电池温度状态 Refer: EM_BATTERY_TEMPER_STATE;Battery temperature status Refer: EM_BATTERY_TEMPER_STATE;
    ]

class SDK_POWER_STATUS(Structure):
    """
    电源状态;Power status
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('bEnable', C_BOOL), # 查询是否成功; Search succeeded or not;
        ('nCount', c_int), # 电源数量; Power amount;
        ('stuPowers', SDK_POWER_INFO * 16), # 电源状态; Power status;
        ('nBatteryNum', c_int), # 电池数量; Battery Number;
        ('stuBatteries', SDK_BATTERY_INFO * 16), # 电池状态; Battery Status;
    ]

class SDK_TEMPERATURE_INFO(Structure):
    """
    温度信息;Temperature info
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('szName', c_char * 64), # 传感器名称; Sensor name;
        ('fTemperature', c_float), # 温度; Temperature;
    ]

class SDK_TEMPERATURE_STATUS(Structure):
    """
    温度状态;Temperature status
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('bEnable', C_BOOL), # 查询是否成功; Search succeeded or not;
        ('nCount', c_int), # 温度数量; Temperature amount;
        ('stuTemps', SDK_TEMPERATURE_INFO * 256), # 温度信息; Temperature info;
    ]

class SDK_SYSTEM_STATUS(Structure):
    """
    系统状态;System status
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('pstuCPU', POINTER(SDK_CPU_STATUS)), # CPU状态; CPU status;
        ('pstuMemory', POINTER(SDK_MEMORY_STATUS)), # 内存状态; Memory status;
        ('pstuFan', POINTER(SDK_FAN_STATUS)), # 风扇状态; Fan status;
        ('pstuPower', POINTER(SDK_POWER_STATUS)), # 电源状态; Power status;
        ('pstuTemp', POINTER(SDK_TEMPERATURE_STATUS)), # 温度状态; Temperature status;
    ]

class NET_DEV_DISKSTATE(Structure):
    """
    硬盘信息;HDD informaiton
    """
    _fields_ = [
        ('dwVolume', C_DWORD), # 硬盘的容量, 单位MB(B表示字节); HDD capacity;
        ('dwFreeSpace', C_DWORD), # 硬盘的剩余空间, 单位MB(B表示字节); HDD free space;
        ('dwStatus', C_BYTE),   # 高四位的值表示硬盘类型,具体见枚举类型EM_DISK_TYPE；低四位的值表示硬盘的状态,0-休眠,1-活动,2-故障等；将DWORD拆成四个BYTE;
                                # higher 4 byte instruct hdd type, see the enum struct EM_DISK_TYPE; lower four byte instruct HDD status,0-hiberation,1-active,2-malfucntion and etc.;Devide DWORD into four BYTE;
        ('bDiskNum', C_BYTE), # 硬盘号; HDD number;
        ('bSubareaNum', C_BYTE), # 分区号; Subarea number;
        ('bSignal', C_BYTE), # 标识,0为本地 1为远程; Symbol. 0:local. 1:remote;
    ]

class SDK_HARDDISK_STATE(Structure):
    """
    设备硬盘信息;Device HDD informaiton
    """
    _fields_ = [
        ('dwDiskNum', C_DWORD), # 个数; Amount;
        ('stDisks', NET_DEV_DISKSTATE * 256), # 硬盘或分区信息; HDD or subarea information;
    ]

class NET_VIDEOIN_EXPOSURE_NORMAL_INFO(Structure):
    """
    通用曝光属性配置;normal exposure config of video input
    """
    _fields_ = [
        ('dwSize', C_DWORD), 
        ('emCfgType', C_ENUM), # 配置类型，获取和设置时都要指定,参考枚举NET_EM_CONFIG_TYPE; config type, you need set the value wether set or get config,Please refer to NET_EM_CONFIG_TYPE;
        ('emExposureMode', C_ENUM), # 曝光模式,参考枚举NET_EM_EXPOSURE_MODE; exposure mode,Please refer to NET_EM_EXPOSURE_MODE;
        ('nAntiFlicker', c_int), # 防闪烁0-Outdoor 1-50Hz防闪烁 2-60Hz防闪烁; anti flicker 0-Outdoor 1-50Hz 2-60Hz;
        ('nCompensation', c_int), # 曝光补偿0-100; Compensation 0-100;
        ('nGain', c_int), # 增益值; gain value 0-100;
        ('nGainMin', c_int), # 增益下限0-100; the min value of Gain 0-100;
        ('nGainMax', c_int), # 增益上限0-100; the max value of gain 0-100;
        ('nExposureIris', c_int), # 光圈值，模式为光圈优先时有效，0-100; the value of iris(0-100), it is valid when mode is NET_EM_EXPOSURE_APERTUREFIRST;
        ('dbExposureValue1', c_double), # 自动曝光时间下限或者手动曝光自定义时间,毫秒为单位，取值0.1ms~80ms; Auto exposure value min limit or manual axposure custom, unit is millisecond (0.1ms~80ms).;
        ('dbExposureValue2', c_double), # 自动曝光时间上限,毫秒为单位，取值0.1ms~80ms，且必须不小于"ExposureValue1"取值; Auto exposure time max limit, unit is millisecond (0.1ms~80ms);
        ('bIrisAuto', C_BOOL), # 自动光圈使能; Automatic aperture enabling;
        ('emDoubleExposure', C_ENUM), # 双快门的支持类型,参考枚举EM_DOUBLE_EXPOSURE_TYPE; Support Type of Double Shutter,Please refer to EM_DOUBLE_EXPOSURE_TYPE;
    ]

class NET_IN_GET_DISTANCE_RES(Structure):
    """
    CLIENT_GetDistanceRes 接口输入参数; Input param of CLIENT_GetDistanceRes
    """
    _fields_ = [
        ('dwSize', C_DWORD), # 结构体大小; struct size;
        ('nChannel', C_UINT), # 通道; Channel;
    ]

class NET_OUT_GET_DISTANCE_RES(Structure):
    """
    GetDistanceRes 接口输出参数; Output param of GetDistanceRes
    """
    _fields_ = [
        ('dwSize', C_DWORD),            # 结构体大小; struct size;
        ('nDistance', C_UINT),          # 目标距离，单位米; Target Distance, Unit Meter;
        ('nOverTimeStatus', c_int),     # 超时状态（0,超时 1未超时）; Timeout state (0, timeout 1 not timeout);
        ('emStatus', C_ENUM),           # 结果状态,参考枚举EM_GET_DISTANCE_RES_STATUS; Result status,Please refer to EM_GET_DISTANCE_RES_STATUS;
    ]

class CFG_NEARLIGHT_INFO(Structure):
    """
    近光灯信息; low beam info
    """
    _fields_ = [
        ('bEnable', C_BOOL), # 是否使能，TRUE使能，FALSE不使能; Whether enabled, TRUE enabled, FALSE does not enable;
        ('dwLightPercent', C_DWORD), # 灯光亮度百分比值(0~100); Light brightness percentage (0~100);
        ('dwAnglePercent', C_DWORD), # 灯光角度百分比值(0~100); Lighting angle in percentage (0~100);
    ]

class CFG_FARLIGHT_INFO(Structure):
    """
    远光灯信息; High beam information
    """
    _fields_ = [
        ('bEnable', C_BOOL), # 是否使能，TRUE使能，FALSE不使能; Whether enabled, TRUE enabled, FALSE does not enable;
        ('dwLightPercent', C_DWORD), # 灯光亮度百分比值(0~100); Light brightness percentage (0~100);
        ('dwAnglePercent', C_DWORD), # 灯光角度百分比值(0~100); Lighting angle in percentage (0~100);
    ]

class CFG_LIGHTING_DETAIL(Structure):
    """
    灯光设置详情; Light setting details
    """
    _fields_ = [
        ('nCorrection', c_int),  # 灯光补偿 (0~4) 倍率优先时有效; Light compensation (0 ~ 4) effective ratio is preferred;
        ('nSensitive', c_int),  # 灯光灵敏度(0~5)倍率优先时有效，默认为3; Light sensitivity (0 ~ 5) are effective ratio is preferred, the default value is 3 EM_CFG_LIGHTING_MODE emMode;  Light pattern;
        ('emMode', C_ENUM),  # 灯光模式,参考枚举EM_CFG_LIGHTING_MODE; Light mode,Please refer to EM_CFG_LIGHTING_MODE;
        ('nNearLight', c_int),  # 近光灯有效个数; Dipped headlights effective number;
        ('stuNearLights', CFG_NEARLIGHT_INFO * 16),  # 近光灯列表; Dipped headlight list;
        ('nFarLight', c_int),  # 远光灯有效个数; High beam effective number;
        ('stuFarLights', CFG_FARLIGHT_INFO * 16),  # 远光灯列表; High beam list;
    ]

class CFG_LIGHTING_INFO(Structure):
    """
     灯光设置(对应 CFG_CMD_TYPE.LIGHTING 命令); Light setting (corresponding CFG_CMD_TYPE.LIGHTING command)
    """
    _fields_ = [
        ('nLightingDetailNum', c_int),  # 灯光设置有效个数; Light setting effective number;
        ('stuLightingDetail', CFG_LIGHTING_DETAIL * 16),  # 灯光设置信息列表; Light setting information list;
    ]

class SDK_PTZ_LOCATION_INFO(Structure):
    """
    云台定位信息报警; PTZ positioning information alarm
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号; Channel number;
        ('nPTZPan', c_int),     # 云台水平运动位置,有效范围：[0,3600]; Horizontal movement of the head position, effective range: [0,3600];
        ('nPTZTilt', c_int),    # 云台垂直运动位置,有效范围：[-1800,1800]; PTZ vertical position, the effective range: [-1800,1800];
        ('nPTZZoom', c_int),    # 云台光圈变动位置,有效范围：[0,128]; PTZ iris position changes, effective range: [0,128];
        ('bState', C_BYTE),     # 云台运动状态, 0-未知 1-运动 2-空闲; PTZ motion, 0 - Unknown 1 - Movement 2 - Idle;
        ('bAction', C_BYTE),    # 云台动作,255-未知,0-预置点,1-线扫,2-巡航,3-巡迹,4-水平旋转,5-普通移动,6-巡迹录制,7-全景云台扫描,8-热度图,9-精确定位,10-设备校正,11-智能配置，12-云台重启; PTZ movement, 255- unknown,0 - preset ,1 - line scan, 2 - Cruise, 3 - patrol track, 4 - horizontal rotation,5 -GeneralMove,6-PatternRecord,7-WideViewScan,,8-HeatMap,9-AbsoluteMove,10-CheckDeviceOffset,11-IntelliConfigure，12-Restart;
        ('bFocusState', C_BYTE),    # 云台聚焦状态, 0-未知, 1-运动状态, 2-空闲; PTZ focus state, 0 - unknown 1 - state of motion 2 - Idle;
        ('bEffectiveInTimeSection', C_BYTE),    # 在时间段内预置点状态是否有效,如果当前上报的预置点是时间段内的预置点,则为1,其他情况为0; In the period of validity of the preset state,If the current is preset reported preset period of time, compared with one, otherwise 0;
        ('nPtzActionID', c_int),    # 巡航ID号; Cruise ID number;
        ('dwPresetID', C_DWORD),    # 云台所在预置点编号; PTZ preset number where;
        ('fFocusPosition', c_float),    # 聚焦位置; Focus position;
        ('bZoomState', C_BYTE),     # 云台ZOOM状态,0-未知,1-ZOOM,2-空闲; ZOOM PTZ status, 0 - Unknown,1-ZOOM, 2 - Idle;
        ('bReserved', C_BYTE * 3),  # 对齐; Alignment;
        ('dwSequence', C_DWORD),    # 包序号,用于校验是否丢包; Packet sequence number, used to verify whether the loss;
        ('dwUTC', C_DWORD),     # 对应的UTC(1970-1-1 00:00:00)秒数。; Corresponding UTC (1970-1-1 00:00:00) seconds.;
        ('emPresetStatus', C_ENUM),     # 预置点位置,参考枚举EM_SDK_PTZ_PRESET_STATUS; preset status,Please refer to EM_SDK_PTZ_PRESET_STATUS;
        ('nZoomValue', c_int),  # 真实变倍值 当前倍率（扩大100倍表示）; real zoom value ,expanded 100 times;
        ('stuAbsPosition', NET_PTZSPACE_UNNORMALIZED),  # 云台方向与放大倍数（扩大100倍表示）,第一个元素为水平角度，0-36000；,第二个元素为垂直角度，（-18000）-（18000）；,第三个元素为显示放大倍数，0-MaxZoom*100; Ptz abs position,First is horizontal angle,0-36000,Second is vertical angle,-18000-18000,nZoom is zoom factors,0-MaxZoom*100;
        ('nFocusMapValue', c_int),  # 聚焦映射值; Focus map value
        ('nZoomMapValue', c_int),  # 变倍映射值; Variable magnification mapping value
        ('emPanTiltStatus', C_ENUM),  # 云台P/T运动状态,参考 EM_SDK_PTZ_PAN_TILT_STATUS;  P/T movement status of gimbal.Please refer to EM_SDK_PTZ_PAN_TILT_STATUS
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('reserved', c_char * 696),  # 保留字段; Reserved;
    ]

class NET_A_OUT_PTZ_VIEW_RANGE_STATUS(Structure):
    """
    云台可视域状态结构
    PTZ conditions for visual structure
    """
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('dbDistance', c_double),  # 可视距离, 单位:米;Visual range, the unit: m;
        ('nAngelH', c_int),  # 水平可视角度, 0~1800, 单位:十分之一度;Horizontal viewing angles, 0~1800, unit: 1/10 degrees;
        ('nAzimuthH', c_int),  # 水平方位角度, 0~3600, 单位:十分之一度;Horizontal azimuth Angle, 0 ~ 3600, unit: 1/10 degrees;
        ('nInclinationH', c_int),  # 水平倾斜角度, -900~900, 单位:十分之一度;Horizontal inclination angle, -900~900, unit: 1/10 degree;
        ('nAngelV', c_int),  # 垂直可视角度, 0~1800, 单位:十分之一度;Vertical viewing angles, 0~1800, unit: 1/10 degrees;
        ('nAzimuthV', c_int),  # 垂直方位角度, 0~3600, 单位:十分之一度;Vertical azimuth Angle, 0 ~ 3600, unit: 1/10 degrees;
        ('nPan', c_int),  # 水平角度，扩大100倍值，[0-36000];Horizontal angle, increase by 100 times the value，[0-36000]
        ('nTilt', c_int),  # 垂直角度，扩大100倍值，[-18000-18000];Vertical angle, increase by 100 times the value，[-18000-18000]
        ('nZoom', c_int),  # 显示放大倍数，扩大100倍值，[0-MaxZoom*100];Display magnification, increase the value by 100 times，[0-MaxZoom*100]
    ]

class PTZ_SPACE_UNIT(Structure):
    """
    云台控制位置单元; PTZ control position unit
    """
    _fields_ = [
        ('nPositionX', c_int),          # 云台水平运动位置,有效范围：[0,3600]; PTZ horizontal motion position, effective range:[0,3600];
        ('nPositionY', c_int),          # 云台垂直运动位置,有效范围：[-1800,1800]; PTZ vertical motion position, effective range:[-1800,1800];
        ('nZoom', c_int),               # 云台光圈变动位置,有效范围：[0,128]; PTZ aperture change position, the effective range:[0,128];
        ('szReserve', c_char * 32),     # 预留32字节; Reserved;
    ]

class PTZ_SPEED_UNIT(Structure):
    """
    云台控制速率单元; PTZ control speed unit
    """
    _fields_ = [
        ('fPositionX', c_float),        # 云台水平方向速率,归一化到-1~1; PTZ horizontal speed, normalized to -1~1;
        ('fPositionY', c_float),        # 云台垂直方向速率,归一化到-1~1; PTZ vertical speed, normalized to -1~1;
        ('fZoom', c_float),             # 云台光圈放大倍率,归一化到 0~1; PTZ aperture magnification, normalized to 0~1;
        ('szReserve', c_char * 32),     # 预留32字节; Reserved;
    ]

class PTZ_CONTROL_ABSOLUTELY(Structure):
    """
    绝对控制云台对应结构; Absolute control PTZ corresponding structure
    """
    _fields_ = [
        ('stuPosition', PTZ_SPACE_UNIT),    # 云台绝对移动位置; PTZ Absolute Speed;
        ('stuSpeed', PTZ_SPEED_UNIT),       # 云台运行速度; PTZ Operation Speed;
        ('szReserve', c_char * 64),         # 预留64字节; Reserved;
    ]

class CFG_PTZ_MOTION_RANGE(Structure):
    """
    云台转动角度范围，单位：度; PTZ rotation angle range, unit: degree
    """
    _fields_ = [
        ('nHorizontalAngleMin', c_int), # 水平角度范围最小值,单位:度; Minimum level angle range, unit: degree;
        ('nHorizontalAngleMax', c_int), # 水平角度范围最大值,单位:度; The maximum horizontal angle range, unit: degree;
        ('nVerticalAngleMin', c_int), # 垂直角度范围最小值,单位:度; Vertical angle range minimum, unit: degree;
        ('nVerticalAngleMax', c_int), # 垂直角度范围最大值,单位:度; Maximum vertical angle range, unit: degree;
    ]

class CFG_PTZ_LIGHTING_CONTROL(Structure):
    """
    云台转动角度范围，单位：度; PTZ rotation angle range, unit: degree
    """
    _fields_ = [
        ('szMode', c_char * 32),  # 手动灯光控制模式,on-off"：直接开关模式,,"adjustLight"：手动调节亮度模式; Manual Lighting Control Mode,On - off ": Direct Switch Mode,,"adjustLight":Manually Adjust Brightness Mode;
        ('dwNearLightNumber', C_DWORD),  # 近光灯组数量; The number of near light group;
        ('dwFarLightNumber', C_DWORD),  # 远光灯组数量; The number of beam group;
    ]

class CFG_PTZ_AREA_SCAN(Structure):
    """
    云台-区域扫描能力集; PTZ -Area Scan capability
    """
    _fields_ = [
        ('bIsSupportAutoAreaScan', C_BOOL),  # 是否支持区域扫描; Whether to support Area Scan;
        ('wScanNum', c_uint16),  # 区域扫描的个数; Area Scan Numbers;
    ]

class CFG_PTZ_PRIVACY_MASKING(Structure):
    """
    隐私遮挡能力集; the capability of privacy masking
    """
    _fields_ = [
        ('bPrivacyMasking', C_BOOL), # 是否支持隐私遮挡设置; support setting privacy masking or not;
        ('bSetColorSupport', C_BOOL), # 是否支持遮挡块颜色设置; support setting color of privacy masking or not;
        ('abMaskType', C_BOOL), # emMaskType是否有效; emMaskType is effective or not;
        ('nMaskTypeCount', c_int), # 实际支持的遮挡块形状个数; the count of mask types actual supported;
        ('emMaskType', C_ENUM * 8), # 支持的遮挡块形状，没有该项配置时默认支持矩形,参考枚举NET_EM_MASK_TYPE; the list os mask types supported, no value means support rect,Please refer to NET_EM_MASK_TYPE;
        ('bSetMosaicSupport', C_BOOL), # 是否支持马赛克遮挡块设置; support settingh mosaic or not;
        ('bSetColorIndependent', C_BOOL), # 是否支持遮挡块颜色相互独立(bSetColorSupport为true时该能力有效); support independent color of privacy masking or not(effective when bSetColorSupport is true);
        ('abMosaicType', C_BOOL), # emMosaicType是否有效; emMosaicType is effective or not;
        ('nMosaicTypeCount', c_int), # 实际支持的马赛克类型个数; the count of mosaic types actual support;
        ('emMosaicType', C_ENUM * 8), # 支持的马赛克类型(SetMosaicSupport为true时该能力有效，没有该项配置时默认支持24x24大小马赛克),参考枚举NET_EM_MOSAIC_TYPE; the list of mosaic types supported(effective SetMosaicSupport is true, no value means support 24x24),Please refer to NET_EM_MOSAIC_TYPE;
    ]

class CFG_PTZ_MEASURE_DISTANCE(Structure):
    """
    图像测距能力;the capability of measureing distance of the image
    """
    _fields_ = [
        ('bSupport', C_BOOL), # 是否支持图像测距; support measureing distance of the image or not;
        ('bOsdEnable', C_BOOL), # 是否将图像测距结果数据叠加至码流; support stack the result of measureing to the stream or not;
        ('nDisplayMin', c_int), # 图像测距信息的最小显示时长, 单位秒; the min time of display, unit:second;
        ('nDisplayMax', c_int), # 图像测距信息的最大显示时长, 单位秒; the max time of display, unit:second;
    ]

class CFG_PTZ_ACTION_CAPS(Structure):
    """
    支持的云台动作类型; Ptz action type
    """
    _fields_ = [
        ('bSupportPan', C_BOOL), # 是否支持水平移动; Whether to support PTZ horizontal swing;
        ('bSupportTile', C_BOOL), # 是否支持垂直移动; Whether to support PTZ vertical swing;
        ('bSupportZoom', C_BOOL), # 是否支持变倍; Whether to support PTZ changed times;
        ('byReserved', C_BYTE * 116), # 预留; Reserved;
    ]

class CFG_PTZ_ABSOLUTELY_CAPS(Structure):
    """
    支持的云台精确定位方式类型;Ptz absolutely type
    """
    _fields_ = [
        ('bSupportNormal', C_BOOL), # 是否支持归一化定位; Whether to support normalized move;
        ('bSupportReal', C_BOOL), # 是否支持实际参数值定位; Whether to support unnormalized move;
        ('byReserved', C_BYTE * 120), # 预留; Reserved;
    ]

class CFG_PTZ_MOVE_ABSOLUTELY_CAP(Structure):
    """
    绝对控制云台能力; The caps of ptz move absolutely
    """
    _fields_ = [
        ('stuPTZ', CFG_PTZ_ACTION_CAPS), # 支持的云台动作类型; Ptz action types supported;
        ('stuType', CFG_PTZ_ABSOLUTELY_CAPS), # 支持的云台精确定位方式类型; Ptz absolutely types supported;
        ('byReserved', C_BYTE * 768), # 预留; Reserved;
    ]

class CFG_PTZ_CONTINUOUSLY_TYPE(Structure):
    """
    连续移动方式类型; Continuously move type
    """
    _fields_ = [
        ('bSupportNormal', C_BOOL), # 是否支持归一化值定位; Whether to support normalized move;
        ('bSupportExtra', C_BOOL), # 是否支持非归一化值定位; Whether to support unnormalized move;
        ('byReserved', C_BYTE * 120), # 预留; Reserved;
    ]

class CFG_PTZ_MOVE_CONTINUOUSLY_CAPS(Structure):
    """
    云台连续运动能力; Continuously move caps
    """
    _fields_ = [
        ('stuPTZ', CFG_PTZ_ACTION_CAPS), # 支持的PTZ动作; Ptz action types supported;
        ('stuType', CFG_PTZ_CONTINUOUSLY_TYPE), # 连续移动方式类型; Ptz absolutely types supported;
        ('byReserved', C_BYTE * 1024), # 预留; Reserved;
    ]

class CFG_PTZ_PROTOCOL_CAPS_INFO(Structure):
    """
    获取云台能力集信息; Get PTZ capability set information
    """
    _fields_ = [
        ('nStructSize', c_int),
        ('bPan', C_BOOL), # 是否支持云台水平摆动; Whether to support PTZ horizontal swing;
        ('bTile', C_BOOL), # 是否支持云台垂直摆动; Whether to support PTZ vertical swinging;
        ('bZoom', C_BOOL), # 是否支持云台变倍; Whether to support PTZ changed times;
        ('bIris', C_BOOL), # 是否支持云台光圈调节; Whether to support PTZ aperture adjustment;
        ('bPreset', C_BOOL), # 是否支持预置点; Whether to support the preset point;
        ('bRemovePreset', C_BOOL), # 是否支持清除预置点; Whether to support removal of preset point;
        ('bTour', C_BOOL), # 是否支持自动巡航线路; Whether to support automatic cruise lines;
        ('bRemoveTour', C_BOOL), # 是否支持清除巡航; Whether to support Clear cruise;
        ('bPattern', C_BOOL), # 是否支持轨迹线路; Whether to support the track line;
        ('bAutoPan', C_BOOL), # 是否支持自动水平摆动; Whether to support automatic level swing;
        ('bAutoScan', C_BOOL), # 是否支持自动扫描; Whether to support automatic scanning;
        ('bAux', C_BOOL), # 是否支持辅助功能; Whether to support accessibility;
        ('bAlarm', C_BOOL), # 是否支持报警功能; Support alarm function;
        ('bLight', C_BOOL), # 是否支持灯光, 内容见下面"stuPtzLightingControl"，该字段已废除使用; Whether or not support the lighting, the contents see below "stuPtzLightingControl", this member is invalid;
        ('bWiper', C_BOOL), # 是否支持雨刷; Whether or not support the wipers;
        ('bFlip', C_BOOL), # 是否支持镜头翻转; Whether or not support Flip camera;
        ('bMenu', C_BOOL), # 是否支持云台内置菜单; Whether or not support PTZ built-in menus;
        ('bMoveRelatively', C_BOOL), # 是否支持云台按相对坐标定位; Whether or not support the PTZ by a relative coordinate positioning;
        ('bMoveAbsolutely', C_BOOL), # 是否支持云台按绝对坐标定位; Whether or not support PTZ in absolute coordinates;
        ('bMoveDirectly', C_BOOL), # 是否支持云台按三维坐标定位; Whether or not support ptz 3D point direct motion;
        ('bReset', C_BOOL), # 是否支持云台复位; Whether or not support PTZ reset;
        ('bGetStatus', C_BOOL), # 是否支持获取云台运动状态及方位坐标; Whether or not support Get the state of motion and orientation coordinates of PTZ;
        ('bSupportLimit', C_BOOL), # 是否支持限位; Whether or not support the limit;
        ('bPtzDevice', C_BOOL), # 是否支持云台设备; Whether or not support PTZ equipment;
        ('bIsSupportViewRange', C_BOOL), # 是否支持云台可视域; Whether or not support PTZ visible range;
        ('wCamAddrMin', c_uint16), # 通道地址的最小值; The minimum channel address;
        ('wCamAddrMax', c_uint16), # 通道地址的最大值; The maximum number of channel address;
        ('wMonAddrMin', c_uint16), # 预览地址的最小值; Minimum monitoring addresses;
        ('wMonAddrMax', c_uint16), # 预览地址的最大值; The maximum number of monitoring the address;
        ('wPresetMin', c_uint16), # 预置点的最小值; Minimum preset points;
        ('wPresetMax', c_uint16), # 预置点的最大值; The maximum preset points;
        ('wTourMin', c_uint16), # 自动巡航线路的最小值; The minimum value of automatic cruise lines;
        ('wTourMax', c_uint16), # 自动巡航线路的最大值; The maximum number of automatic cruise lines;
        ('wPatternMin', c_uint16), # 轨迹线路的最小值; The minimum value of track circuit;
        ('wPatternMax', c_uint16), # 轨迹线路的最大值; The maximum number of track circuit;
        ('wTileSpeedMin', c_uint16), # 垂直速度的最小值; The minimum value of vertical speed;
        ('wTileSpeedMax', c_uint16), # 垂直速度的最大值; The maximum vertical speed;
        ('wPanSpeedMin', c_uint16), # 水平速度的最小值; The minimum value of horizontal velocity;
        ('wPanSpeedMax', c_uint16), # 水平速度的最大值; The maximum horizontal velocity;
        ('wAutoScanMin', c_uint16), # 自动扫描的最小值; The minimum value of automatic scanning;
        ('wAutoScanMax', c_uint16), # 自动扫描的最大值; The maximum number of automatic scanning;
        ('wAuxMin', c_uint16), # 辅助功能的最小值; The minimum value of auxiliary functions;
        ('wAuxMax', c_uint16), # 辅助功能的最大值; The maximum number of auxiliary functions;
        ('dwInterval', C_DWORD), # 发送命令的时间间隔; Send the command time interval;
        ('dwType', C_DWORD), # 协议的类型，0-本地云台，1-远程云台; The type of agreement, 0 - Local PTZ 1 - Remote PTZ;
        ('dwAlarmLen', C_DWORD), # 协议的报警长度; The length of the alarm of the agreement;
        ('dwNearLightNumber', C_DWORD), # 近光灯组数量,0~4,为0时表示不支持; The number of near light group, 0-4, 0 means not supported;
        ('dwFarLightNumber', C_DWORD), # 远光灯组数量,0~4,为0时表示不支持; The number of beam group, 0-4, 0 means not supported;
        ('dwSupportViewRangeType', C_DWORD), # 支持的可视域数据获取方式掩码,从低位到高位依次数,目前支持,第1位:为1表示支持"ElectronicCompass" 电子罗盘方式; Visual field data acquisition mode supported by the mask, from low to high depending on the number , currently supported,The first 1: 1 expressed support the "ElectronicCompass" electronic compass mode;
        ('dwSupportFocusMode', C_DWORD), # 支持的支持的焦距模式掩码,从低位到高位依次数,见#EM_SUPPORT_FOCUS_MODE; Supported Focus mode mask, from low to high depending on the number, see # EM_SUPPORT_FOCUS_MODE;
        ('szName', c_char * 32), # 操作的协议名; The name of the protocol operations;
        ('szAuxs', c_char * 1024), # 云台辅助功能名称列表; PTZ auxiliary function names list;
        ('stuPtzMotionRange', CFG_PTZ_MOTION_RANGE), # 云台转动角度范围，单位：度; PTZ rotation angle range, unit: degree;
        ('stuPtzLightingControl', CFG_PTZ_LIGHTING_CONTROL), # 灯光控制内容，该字段已废除使用; Lighting control content, this member is invalid;
        ('bSupportPresetTimeSection', C_BOOL), # 是否支持预置点时间段配置的功能; Whether to support the function of the preset point time configuration;
        ('bFocus', C_BOOL), # 是否支持云台变焦; Whether to support to Ptz focus;
        ('stuPtzAreaScan', CFG_PTZ_AREA_SCAN), # 区域扫描能力集; Area Scan capability;
        ('stuPtzPrivacyMasking', CFG_PTZ_PRIVACY_MASKING), # 隐私遮挡能力集; privacy masking capability;
        ('stuPtzMeasureDistance', CFG_PTZ_MEASURE_DISTANCE), # 图像测距能力集; measure distance capability;
        ('bSupportPtzPatternOSD', C_BOOL), # 是否支持云台巡迹OSD叠加; support PTZ pattern OSD or not;
        ('bSupportPtzRS485DetectOSD', C_BOOL), # 是否支持云台RS485检测OSD叠加; support PTZ RS485 detect OSD or not;
        ('bSupportPTZCoordinates', C_BOOL), # 是否支持云台坐标叠加; support PTZ coordinates or not;
        ('bSupportPTZZoom', C_BOOL), # 是否支持云台变倍叠加; support PTZ zoom or not;
        ('bDirectionDisplay', C_BOOL), # 是否支持云台方向状态显示; support direction display or not;
        ('dwZoomMax', C_DWORD), # 变倍最大值; Zoom Maximum;
        ('dwZoomMin', C_DWORD), # 变倍最小值; Zoom Minimum;
        ('stuMoveAbsolutely', CFG_PTZ_MOVE_ABSOLUTELY_CAP), # 绝对控制云台能力，bMoveAbsolutely==TRUE 时有效; The caps of ptz move absolutely , Valid when bMoveAbsolutely==TRUE;
        ('bMoveContinuously', C_BOOL), # stuMoveContinuously 字段是否有效; Whether stuMoveContinuously is valid or not;
        ('stuMoveContinuously', CFG_PTZ_MOVE_CONTINUOUSLY_CAPS), # 云台连续运动能力; The caps of ptz move Continuously;
        ('nUnSupportDirections', c_int), # 云台不支持的转动方向个数; Number of rotation directions not supported by the gimbal;
        ('emUnSupportDirections', C_ENUM * 10), # 云台不支持的转动方向,参考枚举EM_PTZ_UNSUPPORT_DIRECTION; UnSupport Directions,Please refer to EM_PTZ_UNSUPPORT_DIRECTION;
        ('bSupportEptzLink', C_BOOL),  # 是否支持电子云台联动;Whether to support electronic PTZ linkage;
    ]

class NET_IN_PTZBASE_MOVEABSOLUTELY_INFO(Structure):
    """
    设置云台方向; Move absolulety, Corresponding to BASE_MOVE_ABSOLUTELY
    """
    _fields_ = [
        ('dwSize', C_DWORD),            				# 结构体大小; struct size;
        ('nZoomFlag', c_int),    						# 1表示显示倍率; 2保留，内部用; 3表示映射倍率值；如为0则默认映射倍率值; 1 according to ratio, 2 Reserved, 3 Mapping radio; 0 default Mapping radio
        ('stuPosition', NET_PTZSPACE_UNNORMALIZED),    	# 云台绝对移动位置云台绝对定位参数,扩大10倍,云台水平坐标(0~3600),云台垂直坐标(-1800~1800),倍率值，范围：nZoomFlag为1时(0~最大显示倍率*10)，nZoomFlag为3时(0~16384); Ptz absolutely position,Horizontal angle(0~3600),Vertical angle(-1800~1800),Zoom(0~16384)
        ('stuSpeed', NET_PTZSPACE_UNNORMALIZED),       	# 若无speed则表示默认速度运动 P，T，以0.01度/秒为单位，扩大100倍显示，范围与PtzSpeedLevel中的范围保持一致[0，100000]，水平和垂直分别最大不会超过PtzSpeedLevel中最大档位水平和垂直的最大值，zoom变倍速度为0~100;  If there is no speed, it means the default speed movement P, T, with 0.01 degree/second as the unit, enlarged by 100 times, the range is consistent with the range in PtzSpeedLevel [0, 100000], the maximum horizontal and vertical respectively will not exceed the maximum in PtzSpeedLevel The maximum value of the horizontal and vertical gears, the zoom speed is 0~100.
        ('szReserve', c_char * 448),         			# 预留字节; Reserved;
    ]

class NET_IN_PTZ_STATUS_PROC(Structure):
    """
    订阅云台元数据接口输入参数; Subscribe to PTZ metadata interface input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),   # 结构体大小; struct size;
        ('nChannel', c_int),   # 云台通道; PTZ Channel
        ('cbPTZStatusProc', CB_FUNCTYPE(None, C_LLONG, C_LLONG, c_void_p, c_int, C_LDWORD)),  # 状态回调函数; Callback function
        ('dwUser', C_LDWORD),  # 用户数据; User data
    ]

class NET_OUT_PTZ_STATUS_PROC(Structure):
    """
    订阅云台元数据接口输输出参数; Subscribe to PTZ metadata interface output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; struct size;
    ]

class NET_IN_PTZBASE_MOVEABSOLUTELY_ONLYPT_INFO(Structure):
    """
    绝对定位独立控制PT; Absolute positioning independent control Pt
    """
    _fields_ = [
        ('dwSize', C_DWORD),                            # 结构体大小; struct size;
        ('nPositionP', c_int),                          # P轴坐标，范围0~36000（扩大100倍）;P-axis coordinate, range 0-36000 (expanded 100 times);
        ('nPositionT', c_int),                          # T轴坐标，范围-18000~18000（扩大100倍）;T-axis coordinate, range - 18000 ~ 18000 (expanded 100 times);
        ('nSpeedP', c_int),                             # P轴速度，以0.01度/秒为单位，扩大100倍显示，范围[0，100000];P-axis speed, in the unit of 0.01 deg / s, expanded 100 times display, range [0，100000];
        ('nSpeedT', c_int),                             # T轴速度，以0.01度/秒为单位，扩大100倍显示，范围[0，100000];T-axis speed, in the unit of 0.01 deg / s, expanded 100 times display, range [0，100000];
        ('szReserve', c_char * 1024),                   # 预留字节; Reserved;
    ]

class NET_IN_PTZBASE_MOVEABSOLUTELY_ONLYZOOM_INFO(Structure):
    """
    绝对定位独立控制zoom; Absolute positioning independent control zoom
    """
    _fields_ = [
        ('dwSize', C_DWORD),                            # 结构体大小; struct size;
        ('nZoomFlag', c_int),                           # 1表示显示倍率; 2保留，内部用; 3表示映射倍率值；如为0则默认映射倍率值; 1 according to ratio, 2 Reserved, 3 Mapping radio; 0 default Mapping radio;
        ('nZoomValue', c_int),                          # 根据zoomFlag值确认Zoom位置范围：1：0~显示倍率最大值*100; 3:映射倍率值(0~16384);Confirm the zoom position range according to the zoom flag value: 1:0 ~ maximum display magnification * 100; 3: Mapping ratio value (0 ~ 16384);
        ('nZoomSpeed', c_int),                          # zoom变倍速度为0~100;Zoom speed is 0 ~ 100;
        ('szReserve', c_char * 1024),                   # 预留字节; Reserved;
    ]

class NET_IN_STORAGE_DEV_INFOS(Structure):
    """
    QueryDevInfo接口STORAGE_INFOS枚举接口输入参数; QueryDevInfo，STORAGE_INFOS port input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('emVolumeType', C_ENUM),  # 要获取的卷类型,参考枚举NET_VOLUME_TYPE; volume type to get,Please refer to NET_VOLUME_TYPE;
    ]

class SDK_STORAGE_PARTITION(Structure):
    """
    存储分区信息; Storage partition info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szName', c_char * 128),  # 名称; Name;
        ('nTotalSpace', c_int64),  # 总空间, byte; Total space(MB);
        ('nFreeSpace', c_int64),  # 剩余空间, byte; free space(MB);
        ('szMountOn', c_char * 64),  # 挂载点; Mount point;
        ('szFileSystem', c_char * 16),  # 文件系统; File system;
        ('nStatus', c_int),  # 分区状态, 0-LV不可用, 1-LV可用; partition state, 0-LV not available, 1-LV available;
        ('bIsSupportFs', C_BOOL),  # 设备是否支持当前文件系统, TRUE:支持， FALSE:不支持;Whether the device supports the current file system, TRUE: Yes, FALSE: No;
    ]

class NET_RAID_MEMBER_INFO(Structure):
    """
    RAID成员信息; RAID member info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('dwID', C_DWORD),  # 磁盘号, 可用于描述磁盘在磁柜的槽位; disk no., may use to describe disk cabinet slot;
        ('bSpare', C_BOOL),  # 是否局部热备, true-局部热备, false-RAID子盘; partial hot device, true-partial hot device, false-RAID sub disk;
    ]

class SDK_STORAGE_RAID(Structure):
    """
    RAID信息; RAID Info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nLevel', c_int),  # 等级; level;
        ('nState', c_int),  # RAID状态组合, 如 DH_RAID_STATE_ACTIVE | DH_RAID_STATE_DEGRADED; RAID state combinationDH_RAID_STATE_ACTIVE | DH_RAID_STATE_DEGRADED;
        ('nMemberNum', c_int),  # 成员数量; member amount;
        ('szMembers', c_char * 4096),  # RAID成员; RAID member;
        ('fRecoverPercent', c_float),  # 同步百分比, 0~100, RAID状态中有"Recovering"或"Resyncing"时有效; Sync percentage, 0~100, RAID status has"Recovering" or "Resyncing" valid;
        ('fRecoverMBps', c_float),  # 同步速度, 单位MBps, RAID状态中有"Recovering"或"Resyncing"时有效; Sync speed, unit MBps, RAID status has"Recovering" or "Resyncing" valid;
        ('fRecoverTimeRemain', c_float),  # 同步剩余时间, 单位分钟, RAID状态中有"Recovering"或"Resyncing"时有效; Sync remaining time, unit minute, RAID status has "Recovering" or "Resyncing" valid;
        ('stuMemberInfos', NET_RAID_MEMBER_INFO * 32),  # RAID成员信息; RAID member info;
        ('nRaidDevices', c_int),  # RAID设备个数; The number of RAID device;
        ('nTotalDevices', c_int),  # RAID设备总数; The total count of RAID device;
        ('nActiveDevices', c_int),  # 活动设备个数; The number of active device;
        ('nWorkingDevices', c_int),  # 工作设备个数; The number of working device;
        ('nFailedDevices', c_int),  # 失败设备个数; The number of failed device;
        ('nSpareDevices', c_int),  # 热备设备个数; The number of hot-spare device;
        ('szAliasName', c_char * 24),  # RAID别名,UTF-8编码; Alias Name,UTF-8 code;
        ('szAliasNameEx', c_char * 32),  # RAID别名,UTF-8编码; Alias Name,UTF-8 code;
    ]

class SDK_ISCSI_TARGET(Structure):
    """
    ISCSI Target信息; ISCSI Target Info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szName', c_char * 128),  # 名称; Name;
        ('szAddress', c_char * 64),  # 服务器地址; service address;
        ('szUser', c_char * 128),  # 用户名; user name;
        ('nPort', c_int),  # 端口; port;
        ('nStatus', C_UINT),  # 状态, 0-未知, 1-已连接, 2-未连接, 3-连接失败, 4-认证失败, 5-连接超时, 6-不存在; status, 0- unknow, 1-connected, 2-un connected, 3-connect failed, 4-authentication failed, 5-connect time out;
    ]

class SDK_STORAGE_TANK(Structure):
    """
    扩展柜信息; storage tank info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nLevel', c_int),  # 级别, 主机是第0级,其它下属级别类推; level, the host is 0 level;
        ('nTankNo', c_int),  # 同一级扩展柜内的扩展口编号, 从0开始; extend port number from 0;
        ('nSlot', c_int),  # 对应主柜上的板卡号, 从0开始编号; Corresponding cabinet board card no., start from 0;
    ]

class SDK_STORAGE_DEVICE(Structure):
    """
    存储设备信息; Storage device info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szName', c_char * 128),  # 名称; name;
        ('nTotalSpace', c_int64),  # 总空间, byte; Total space, byte;
        ('nFreeSpace', c_int64),  # 剩余空间, byte; free space, byte;
        ('byMedia', C_BYTE),  # 介质, 0-DISK, 1-CDROM, 2-FLASH; Media, 0-DISK, 1-CDROM, 2-FLASH medium,;
        ('byBUS', C_BYTE),  # 总线, 0-ATA, 1-SATA, 2-USB, 3-SDIO, 4-SCSI; BUS, 0-ATA, 1-SATA, 2-USB, 3-SDIO, 4-SCSI main line 0-ATA, 1-SATA, 2-USB, 3-SDIO, 4-SCSI;
        ('byVolume', C_BYTE),  # 卷类型, 0-物理卷, 1-Raid卷, 2-VG虚拟卷, 3-ISCSI, 4-独立物理卷, 5-全局热备卷, 6-NAS卷(包括FTP, SAMBA, NFS); volume type, 0-physics, 1-Raid, 2- VG virtual 3-ISCSI, 4-Invidual Physical Volume, 5-VolumeGroup, 6-NAS ( FTP, SAMBA, NFS), 7-Invidual Raid Volume;
        ('byState', C_BYTE),  # 物理硬盘状态, 取值为 NET_STORAGE_DEV_OFFLINE 和 NET_STORAGE_DEV_RUNNING 等; Physics disk state, 0-physics disk offline state 1-physics disk 2- RAID activity 3- RAID sync 4-RAID hotspare 5-RAID invalidation 6- RAID re-creation 7- RAID delete;
        ('nPhysicNo', c_int),  # 同类设备存储接口的物理编号; storage interface of devices of same type logic number;
        ('nLogicNo', c_int),  # 同类设备存储接口的逻辑编号; storage interface of devices of same type physics number;
        ('szParent', c_char * 128),  # 上级存储组名称; superior storage group name;
        ('szModule', c_char * 128),  # 设备模块; device module;
        ('szSerial', c_char * 48),  # 设备序列号; device serial number;
        ('szFirmware', c_char * 64),  # 固件版本; Firmware version;
        ('nPartitionNum', c_int),  # 分区数; partition number;
        ('stuPartitions', SDK_STORAGE_PARTITION * 32),  # 分区信息; partition info;
        ('stuRaid', SDK_STORAGE_RAID),  # RAID信息, 只对RAID有效(byVolume == 1); Raid info, for RAID use only(byVolume == 1);
        ('stuISCSI', SDK_ISCSI_TARGET),  # ISCSI信息, 只对ISCSI盘有效(byVolume == 3); Iscsi info, for iscsi use only (byVolume == 2);
        ('abTank', C_BOOL),  # 扩展柜使能; tank enable;
        ('stuTank', SDK_STORAGE_TANK),  # 硬盘所在扩展柜信息, abTank为TRUE时有效; tank info, effective when abTank = TRUE;
        ('emPowerMode', C_ENUM),  # 硬盘电源状态,参考枚举EM_STORAGE_DISK_POWERMODE; hard disk power mode,Please refer to EM_STORAGE_DISK_POWERMODE;
        ('emPreDiskCheck', C_ENUM),  # 硬盘预检状态(配合磁盘预检功能使用),参考枚举EM_STORAGE_DISK_PREDISKCHECK; pre disk check(EVS),Please refer to EM_STORAGE_DISK_PREDISKCHECK;
        ('nOpState', c_int),  #  设备操作状态; Equipment operation status;
    ]

class NET_OUT_STORAGE_DEV_INFOS(Structure):
    """
    QueryDevInfo , STORAGE_INFOS接口输出参数; QueryDevInfo , STORAGE_INFOS port output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nDevInfosNum', c_int),  # 获取到设备的存储模块信息列表; device storage moduleinfo list to get;
        ('stuStoregeDevInfos', SDK_STORAGE_DEVICE * 128),  # 设备信息列表,SDK_STORAGE_DEVICE的dwsize需赋值; device info list, dwsize of SDK_STORAGE_DEVICE need to assign value;
    ]

class NET_IN_GET_TEMPERATUREEX(Structure):
    """
    FaceBoard_GetTemperatureEx的入参; FaceBoard_GetTemperatureEx input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; Structure size;
        ('emTemperatureType', C_ENUM),  # 温度类型,参考枚举EM_TEMPERATUREEX_TYPE; Temperature Type,Please refer to EM_TEMPERATUREEX_TYPE;
    ]

class NET_TEMPERATUREEX_VALUE(Structure):
    """
    每个监测点的温度; Each monitor point temperature
    """
    _fields_ = [
        ('emTemperatureType', C_ENUM),  # 温度类型,参考枚举EM_TEMPERATUREEX_TYPE; Temperature Type,Please refer to EM_TEMPERATUREEX_TYPE;
        ('nRetTemperatureNum', c_int),  # 返回的有效温度值个数; The number of return valid temperature value;
        ('fTemperature', c_float * 64),  # 温度值,单位:摄氏度; Temperature value,unit:centigrade;
        ('byReserved', C_BYTE * 128),  # 保留字节; Reserved byte;
    ]

class NET_OUT_GET_TEMPERATUREEX(Structure):
    """
    FaceBoard_GetTemperatureEx的出参; FaceBoard_GetTemperatureEx output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; Structure size;
        ('nRetMonitorPointNum', c_int),  # 返回的有效温度监测点的个数,num>1时,对应emTemperatureType为ALL; The number of return valid monitor point temperature, when num>1,emTemperatureType is ALL;
        ('stuTemperatureEx', NET_TEMPERATUREEX_VALUE * 12),  # 监测点温度; monitor point temperature;
    ]

class NET_RADIOMETRY_CONDITION(Structure):
    """
    获取测温项温度的条件;Conditions for obtaining the temperature of the temperature item
    """
    _fields_ = [
        ('nPresetId', c_int),   # 预置点编号;Preset point number
        ('nRuleId', c_int),     # 规则编号;Rule number
        ('nMeterType', c_int),  # 测温项类别,见 NET_RADIOMETRY_METERTYPE ;Types of temperature items, see NET_RADIOMETRY_METERTYPE
        ('szName', c_char*64),  # 测温项的名称,从测温配置规则名字中选取;The name of the temperature item, selected from the name of the temperature configuration rule
        ('nChannel', c_int),    # 通道号;Channel number
        ('reserved', c_char*256),# 保留字节;byte reserved
    ]

class NET_IN_RADIOMETRY_GETTEMPER(Structure):
    """
    QueryDevInfo 接口 NET_QUERY_DEV_RADIOMETRY_TEMPER 命令入参;QueryDevInfo interface NET_QUERY_DEV_RADIOMETRY_TEMPER command to input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小;Struct size
        ('stCondition', NET_RADIOMETRY_CONDITION),  # 获取测温项温度的条件;Conditions for obtaining the temperature of the temperature item
    ]

class NET_RADIOMETRYINFO(Structure):
    """
    测温信息;Temperature information
    """
    _fields_ = [
        ('nMeterType', c_int),      # 返回测温类型,见 NET_RADIOMETRY_METERTYPE ;Return temperature type, see NET_RADIOMETRY_METERTYPE
        ('nTemperUnit', c_int),     # 温度单位(当前配置的温度单位),见 NET_TEMPERATURE_UNIT ;Temperature unit (temperature unit currently configured), see NET_TEMPERATURE_UNIT
        ('fTemperAver', c_float),   # 点的温度或者平均温度点的时候,只返回此字段;Point temperature or average temperature point, only return this field
        ('fTemperMax', c_float),    # 温度异常;Maximum temperature
        ('fTemperMin', c_float),    # 温度异常;lowest temperature
        ('fTemperMid', c_float),    # 中间温度值;Intermediate temperature value
        ('fTemperStd', c_float),    # 标准方差值;Standard deviation
        ('reserved', c_char*64),    # 保留字节;byte reserved
    ]

class NET_OUT_RADIOMETRY_GETTEMPER(Structure):
    """
    QueryDevInfo 接口 NET_QUERY_DEV_RADIOMETRY_TEMPER 命令出参;QueryDevInfo interface NET_QUERY_DEV_RADIOMETRY_TEMPER command to output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; Struct size
        ('stTempInfo', NET_RADIOMETRYINFO), # 获取测温参数值;Get the temperature parameter value
    ]

class NET_IN_RADIOMETRY_GETPOINTTEMPER(Structure):
    """
    QueryDevInfo 接口 RADIOMETRY_POINT_TEMPER 命令入参;QueryDevInfo interface RADIOMETRY_POINT_TEMPER command to input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),        # 结构体大小; Struct size
        ('nChannel', c_int),        # 通道号; Channel number
        ('stCoordinate', SDK_POINT), # 测温点的坐标,坐标值 0~8192; The coordinates of the temperature point, the coordinate value is 0~8192
    ]

class NET_OUT_RADIOMETRY_GETPOINTTEMPER(Structure):
    """
    QueryDevInfo 接口 RADIOMETRY_POINT_TEMPER 命令出参;QueryDevInfo interface RADIOMETRY_POINT_TEMPER command to output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; Struct size
        ('stPointTempInfo', NET_RADIOMETRYINFO), # 获取测温参数值;Get the temperature parameter value
    ]

class CFG_POLYGON(Structure):
    """
    区域顶点信息; Area vertex information
    """
    _fields_ = [
        ('nX', c_int),  # 0~8191
        ('nY', c_int),
    ]

class CFG_RECT(Structure):
    """
    区域信息; Area information
    """
    _fields_ = [
        ('nLeft', c_int),
        ('nTop', c_int),
        ('nRight', c_int),
        ('nBottom', c_int),
    ]

class CFG_VIDEO_IN_NIGHT_OPTIONS(Structure):
    """
     视频输入夜晚特殊配置选项，在晚上光线较暗时自动切换到夜晚的配置参数;
     Video input night special configuration options, automatically switch to night configuration parameters when the light is dark at night
    """
    _fields_ = [
        ('bySwitchMode', C_BYTE),   # 已废弃,使用CFG_VIDEO_IN_OPTIONS里面的bySwitchMode; Obsolete, use bySwitchMode in CFG_VIDEO_IN_OPTIONS
        ('byProfile', C_BYTE),      # 当前使用的配置文件; The currently used configuration file
                                    # 0-白天;1-晚上;2-Normal;0、1、2都为临时配置,使图像生效，便于查看图像调试效果，不点击确定，离开页面不保存至设备,3-非临时配置，点击确定后保存至设备，与SwitchMode结合使用，根据SwitchMode决定最终生效的配置。
                                    # SwitchMode=0，Profile=3，设置白天配置到设备;SwitchMode=1，Profile=3，则设置夜晚配置到设备; SwitchMode=2，Profile=3，根据日出日落时间段切换，白天时间段使用白天配置，夜晚时间段使用夜晚配置，保存至设备;SwitchMode=4，Profile=3；使用普通配置，保存至设备
        ('byBrightnessThreshold', C_BYTE), # 亮度阈值 0~100; Brightness threshold 0~100
        ('bySunriseHour', C_BYTE),  # 大致日出和日落时间，日落之后日出之前，将采用夜晚特殊的配置; Approximate sunrise and sunset time, after sunset and before sunrise, special night configuration will be adopted
        ('bySunriseMinute', C_BYTE),# 00:00:00 ~ 23:59:59
        ('bySunriseSecond', C_BYTE),
        ('bySunsetHour', C_BYTE),
        ('bySunsetMinute', C_BYTE),
        ('bySunsetSecond', C_BYTE),
        ('byGainRed', C_BYTE),      # 红色增益调节，白平衡为"Custom"模式下有效 0~100; Red gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byGainBlue', C_BYTE),     # 蓝色增益调节，白平衡为"Custom"模式下有效 0~100; Blue gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byGainGreen', C_BYTE),    # 绿色增益调节，白平衡为"Custom"模式下有效 0~100; Green gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byExposure', C_BYTE),     # 曝光模式；取值范围取决于设备能力集：0-自动曝光，1-曝光等级1，2-曝光等级2…n-1最大曝光等级数 n带时间上下限的自动曝光 n+1自定义时间手动曝光 (n==byExposureEn）;
                                    # Exposure mode; the value range depends on the device capability set: 0-automatic exposure, 1-exposure level 1, 2-exposure level 2...n-1 maximum number of exposure levels n automatic exposure with time upper and lower limits n+1 custom time Manual exposure (n==byExposureEn)
        ('fExposureValue1', c_float),# 自动曝光时间下限或者手动曝光自定义时间,毫秒为单位，取值0.1ms~80ms; The lower limit of automatic exposure time or the custom time of manual exposure, in milliseconds, the value is 0.1ms~80ms
        ('fExposureValue2', c_float),# 自动曝光时间上限,毫秒为单位，取值0.1ms~80ms; The upper limit of auto exposure time, in milliseconds, the value is 0.1ms~80ms
        ('byWhiteBalance', C_BYTE), # 白平衡;White balance 0-"unable", 1-"Auto", 2-"Custom", 3-"Sunny", 4-"Cloudy", 5-"Home", 6-"Office", 7-"Night", 8-"HighColorTemperature", 9-"LowColorTemperature", 10-"AutoColorTemperature", 11-"CustomColorTemperature"
        ('byGain', C_BYTE),         # 0~100增益调节, GainAuto为true时表示自动增益的上限，否则表示固定的增益值; 0~100 Gain adjustment, when GainAuto is true, it means the upper limit of automatic gain, otherwise it means a fixed gain value
        ('bGainAuto', c_bool),      # 自动增益; Automatic gain
        ('bIrisAuto', c_bool),      # 自动光圈; Auto iris
        ('fExternalSyncPhase', c_float),  # 外同步的相位设置 0~360; Phase setting of external synchronization 0~360
        ('byGainMin', C_BYTE),      # 增益下限; Gain lower limit
        ('byGainMax', C_BYTE),      # 增益上限; Gain upper limit
        ('byBacklight', C_BYTE),    # 背光补偿：取值范围取决于设备能力集：0-关闭1-启用2-指定区域背光补偿;Backlight compensation: The value range depends on the device capability set: 0-off 1-enable 2-specified area backlight compensation
        ('byAntiFlicker', C_BYTE),  # 防闪烁模式; Anti-flicker mode; 0-Outdoor 1-50Hz防闪烁 2-60Hz防闪烁
        ('byDayNightColor', C_BYTE),# 日/夜模式；0-总是彩色，1-根据亮度自动切换，2-总是黑白;Day/night mode; 0-always color, 1-automatically switch according to brightness, 2-always black and white
        ('byExposureMode', C_BYTE), # 曝光模式调节 曝光等级为自动曝光时有效，取值：0-默认自动，1-增益优先，2-快门优先; Exposure mode adjustment The exposure level is effective when the exposure level is automatic exposure, value: 0-default automatic, 1-gain priority, 2-shutter priority
        ('byRotate90', C_BYTE),     # 0-不旋转，1-顺时针90°，2-逆时针90°; 0-No rotation, 1-90°clockwise, 2-90°counterclockwise
        ('bMirror', c_bool),        # 镜像; Mirroring
        ('byWideDynamicRange', C_BYTE), # 宽动态值 0-关闭，1~100-为真实范围值; Wide dynamic value, 0-closed, 1~100-is the true range value
        ('byGlareInhibition', C_BYTE),  # 强光抑制 0-关闭， 1~100为范围值; Strong light suppression 0-off, 1~100 is the range value
        ('stuBacklightRegion', CFG_RECT),# 背光补偿区域; Backlight compensation area
        ('byFocusMode', C_BYTE),    # 0-关闭，1-辅助聚焦，2-自动聚焦; 0-off, 1-assisted focus, 2-auto focus
        ('bFlip', c_bool),          # 翻转; Flip
        ('reserved', C_BYTE*74)     # 保留; reserved
    ]

class CFG_FLASH_CONTROL(Structure):
    """
    闪光灯配置; Flash configuration
    """
    _fields_ = [
        ('byMode', C_BYTE),         # 工作模式，0-禁止闪光，1-始终闪光，2-自动闪光; Working mode, 0-flash prohibited, 1-always flash, 2-auto flash
        ('byValue', C_BYTE),        # 工作值, 0-0us, 1-64us, 2-128us, 3-192...15-960us; Working value, 0-0us, 1-64us, 2-128us, 3-192...15-960us
        ('byPole', C_BYTE),         # 触发模式, 0-低电平 1-高电平 2-上升沿 3-下降沿; Trigger mode, 0-low level 1-high level 2-rising edge 3-falling edge
        ('byPreValue', C_BYTE),     # 亮度预设值  区间0~100; Brightness preset value range 0~100
        ('byDutyCycle', C_BYTE),    # 占空比, 0~100; Duty cycle, 0~100
        ('byFreqMultiple', C_BYTE), # 倍频, 0~10; Frequency multiplier, 0~10
        ('reserved', C_BYTE*122),   # 保留; reserved
    ]

class CFG_VIDEO_IN_SNAPSHOT_OPTIONS(Structure):
    """
    抓拍参数特殊配置; Snapshot parameter special configuration
    """
    _fields_ = [
        ('byGainRed', C_BYTE),      # 红色增益调节，白平衡为"Custom"模式下有效 0~100; Red gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byGainBlue', C_BYTE),     # 蓝色增益调节，白平衡为"Custom"模式下有效 0~100; Blue gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byGainGreen', C_BYTE),    # 绿色增益调节，白平衡为"Custom"模式下有效 0~100; Green gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byExposure', C_BYTE),     # 曝光模式；取值范围取决于设备能力集：0-自动曝光，1-曝光等级1，2-曝光等级2…n-1最大曝光等级数 n带时间上下限的自动曝光 n+1自定义时间手动曝光 (n==byExposureEn）;
                                    # Exposure mode; the value range depends on the device capability set: 0-automatic exposure, 1-exposure level 1, 2-exposure level 2...n-1 maximum number of exposure levels n automatic exposure with time upper and lower limits n+1 custom time Manual exposure (n==byExposureEn)
        ('fExposureValue1', c_float),   # 自动曝光时间下限或者手动曝光自定义时间,毫秒为单位，取值0.1ms~80ms; The lower limit of automatic exposure time or the custom time of manual exposure, in milliseconds, the value is 0.1ms~80ms
        ('fExposureValue2', c_float),   # 自动曝光时间上限,毫秒为单位，取值0.1ms~80ms; The upper limit of auto exposure time, in milliseconds, the value is 0.1ms~80ms
        ('byWhiteBalance', C_BYTE),     # 白平衡;White balance 0-"unable", 1-"Auto", 2-"Custom", 3-"Sunny", 4-"Cloudy", 5-"Home", 6-"Office", 7-"Night", 8-"HighColorTemperature", 9-"LowColorTemperature", 10-"AutoColorTemperature", 11-"CustomColorTemperature"
        ('byColorTemperature', C_BYTE), # 色温等级, 白平衡为"CustomColorTemperature"模式下有效;Color temperature level, white balance is valid in "CustomColorTemperature" mode
        ('bGainAuto', c_bool),      # 自动增益; Automatic gain
        ('byGain', C_BYTE),         # 0~100增益调节, GainAuto为true时表示自动增益的上限，否则表示固定的增益值; 0~100 Gain adjustment, when GainAuto is true, it means the upper limit of automatic gain, otherwise it means a fixed gain value
        ('reversed', C_BYTE * 112), # 保留; reserved
    ]

class CFG_FISH_EYE(Structure):
    """
    鱼眼镜头配置; Fisheye lens configuration
    """
    _fields_ = [
        ('stuCenterPoint', CFG_POLYGON),    # 鱼眼圆心坐标,范围[0,8192]; Fisheye center coordinates, range [0,8192]
        ('nRadius', c_uint),                # 鱼眼半径大小,范围[0,8192]; Fisheye radius size, range [0,8192]
        ('fDirection', c_float),            # 镜头旋转方向,旋转角度[0,360.0]; Lens rotation direction, rotation angle [0,360.0]
        ('byPlaceHolder', C_BYTE),          # 镜头安装方式	1顶装，2壁装；3地装,默认1; Lens installation method 1 top installation, 2 wall installation; 3 floor installation, default 1
        ('byCalibrateMode', C_BYTE),        # 鱼眼矫正模式,详见CFG_CALIBRATE_MODE枚举值; Fisheye correction mode, see CFG_CALIBRATE_MODE enumeration value for details
        ('reversed', C_BYTE*31),            # 保留; reserved
    ]

class CFG_VIDEO_IN_NORMAL_OPTIONS(Structure):
    """
    普通参数; Common parameters
    """
    _fields_ = [
        ('byGainRed', C_BYTE),      # 红色增益调节，白平衡为"Custom"模式下有效 0~100; Red gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byGainBlue', C_BYTE),     # 蓝色增益调节，白平衡为"Custom"模式下有效 0~100; Blue gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byGainGreen', C_BYTE),    # 绿色增益调节，白平衡为"Custom"模式下有效 0~100; Green gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byExposure', C_BYTE),     # 曝光模式；取值范围取决于设备能力集：0-自动曝光，1-曝光等级1，2-曝光等级2…n-1最大曝光等级数 n带时间上下限的自动曝光 n+1自定义时间手动曝光 (n==byExposureEn）;
                                    # Exposure mode; the value range depends on the device capability set: 0-automatic exposure, 1-exposure level 1, 2-exposure level 2...n-1 maximum number of exposure levels n automatic exposure with time upper and lower limits n+1 custom time Manual exposure (n==byExposureEn)
        ('fExposureValue1', c_float),# 自动曝光时间下限或者手动曝光自定义时间,毫秒为单位，取值0.1ms~80ms; The lower limit of automatic exposure time or the custom time of manual exposure, in milliseconds, the value is 0.1ms~80ms
        ('fExposureValue2', c_float),# 自动曝光时间上限,毫秒为单位，取值0.1ms~80ms; The upper limit of auto exposure time, in milliseconds, the value is 0.1ms~80ms
        ('byWhiteBalance', C_BYTE), # 白平衡;White balance 0-"unable", 1-"Auto", 2-"Custom", 3-"Sunny", 4-"Cloudy", 5-"Home", 6-"Office", 7-"Night", 8-"HighColorTemperature", 9-"LowColorTemperature", 10-"AutoColorTemperature", 11-"CustomColorTemperature"
        ('byGain', C_BYTE),         # 0~100增益调节, GainAuto为true时表示自动增益的上限，否则表示固定的增益值; 0~100 Gain adjustment, when GainAuto is true, it means the upper limit of automatic gain, otherwise it means a fixed gain value
        ('bGainAuto', c_bool),      # 自动增益; Automatic gain
        ('bIrisAuto', c_bool),      # 自动光圈; Auto iris
        ('fExternalSyncPhase', c_float),  # 外同步的相位设置 0~360; Phase setting of external synchronization 0~360
        ('byGainMin', C_BYTE),      # 增益下限; Gain lower limit
        ('byGainMax', C_BYTE),      # 增益上限; Gain upper limit
        ('byBacklight', C_BYTE),    # 背光补偿：取值范围取决于设备能力集：0-关闭1-启用2-指定区域背光补偿;Backlight compensation: The value range depends on the device capability set: 0-off 1-enable 2-specified area backlight compensation
        ('byAntiFlicker', C_BYTE),  # 防闪烁模式; Anti-flicker mode; 0-Outdoor 1-50Hz防闪烁 2-60Hz防闪烁
        ('byDayNightColor', C_BYTE),# 日/夜模式；0-总是彩色，1-根据亮度自动切换，2-总是黑白;Day/night mode; 0-always color, 1-automatically switch according to brightness, 2-always black and white
        ('byExposureMode', C_BYTE), # 曝光模式调节 曝光等级为自动曝光时有效，取值：0-默认自动，1-增益优先，2-快门优先; Exposure mode adjustment The exposure level is effective when the exposure level is automatic exposure, value: 0-default automatic, 1-gain priority, 2-shutter priority
        ('byRotate90', C_BYTE),     # 0-不旋转，1-顺时针90°，2-逆时针90°; 0-No rotation, 1-90°clockwise, 2-90°counterclockwise
        ('bMirror', c_bool),        # 镜像; Mirroring
        ('byWideDynamicRange', C_BYTE), # 宽动态值 0-关闭，1~100-为真实范围值; Wide dynamic value, 0-closed, 1~100-is the true range value
        ('byGlareInhibition', C_BYTE),  # 强光抑制 0-关闭， 1~100为范围值; Strong light suppression 0-off, 1~100 is the range value
        ('stuBacklightRegion', CFG_RECT),# 背光补偿区域; Backlight compensation area
        ('byFocusMode', C_BYTE),    # 0-关闭，1-辅助聚焦，2-自动聚焦; 0-off, 1-assisted focus, 2-auto focus
        ('bFlip', c_bool),          # 翻转; Flip
        ('reserved', C_BYTE*74)     # 保留; reserved
    ]

class CFG_VIDEO_IN_OPTIONS(Structure):
    """
     视频输入前端选项(对应 CFG_CMD_TYPE.VideoInOptions); Video input front-end options (corresponding CFG_CMD_TYPE.VideoInOptions)
    """
    _fields_ = [
        ('byBacklight', C_BYTE),    # 背光补偿：取值范围取决于设备能力集：0-关闭1-启用2-指定区域背光补偿;Backlight compensation: The value range depends on the device capability set: 0-off 1-enable 2-specified area backlight compensation
        ('byDayNightColor', C_BYTE),# 日/夜模式；0-总是彩色，1-根据亮度自动切换，2-总是黑白;Day/night mode; 0-always color, 1-automatically switch according to brightness, 2-always black and white
        ('byWhiteBalance', C_BYTE), # 白平衡;White balance 0-"unable", 1-"Auto", 2-"Custom", 3-"Sunny", 4-"Cloudy", 5-"Home", 6-"Office", 7-"Night", 8-"HighColorTemperature", 9-"LowColorTemperature", 10-"AutoColorTemperature", 11-"CustomColorTemperature"
        ('byColorTemperature', C_BYTE), # 色温等级, 白平衡为"CustomColorTemperature"模式下有效;Color temperature level, white balance is valid in "CustomColorTemperature" mode
        ('bMirror', c_bool),        # 镜像; Mirroring
        ('bFlip', c_bool),          # 翻转; Flip
        ('bIrisAuto', c_bool), # 自动光圈; Auto iris
        ('bInfraRed', c_bool), # 根据环境光自动开启红外补偿灯; Automatically turn on the infrared compensation light according to the ambient light
        ('byGainRed', C_BYTE), # 红色增益调节，白平衡为"Custom"模式下有效 0~100;Red gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byGainBlue', C_BYTE),# 蓝色增益调节，白平衡为"Custom"模式下有效 0~100;Blue gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byGainGreen', C_BYTE),# 绿色增益调节，白平衡为"Custom"模式下有效 0~100;Green gain adjustment, white balance is effective in "Custom" mode 0~100
        ('byExposure', C_BYTE), # 曝光模式；取值范围取决于设备能力集：0-自动曝光，1-曝光等级1，2-曝光等级2…n-1最大曝光等级数 n带时间上下限的自动曝光 n+1自定义时间手动曝光 (n==byExposureEn）;
                                # Exposure mode; the value range depends on the device capability set: 0-automatic exposure, 1-exposure level 1, 2-exposure level 2...n-1 maximum number of exposure levels n automatic exposure with time upper and lower limits n+1 custom time Manual exposure (n==byExposureEn)
        ('fExposureValue1', c_float), # 自动曝光时间下限或者手动曝光自定义时间,毫秒为单位，取值0.1ms~80ms; The lower limit of automatic exposure time or the custom time of manual exposure, in milliseconds, the value is 0.1ms~80ms
        ('fExposureValue2', c_float), # 自动曝光时间上限,毫秒为单位，取值0.1ms~80ms; The upper limit of auto exposure time, in milliseconds, the value is 0.1ms~80ms
        ('bGainAuto', c_bool),  # 自动增益; Automatic gain
        ('byGain', C_BYTE),     # 增益调节, GainAuto为true时表示自动增益的上限，否则表示固定的增益值; Gain adjustment, when GainAuto is true, it means the upper limit of automatic gain, otherwise it means a fixed gain value
        ('bySignalFormat', C_BYTE), # 信号格式, 0-Inside(内部输入) 1-BT656 2-720p 3-1080p  4-1080i  5-1080sF; Signal format, 0-Inside (internal input) 1-BT656 2-720p 3-1080p 4-1080i 5-1080sF
        ('byRotate90', C_BYTE), # 0-不旋转，1-顺时针90°，2-逆时针90°; 0-No rotation, 1-90°clockwise, 2-90°counterclockwise
        ('fExternalSyncPhase', c_float), # 外同步的相位设置 0~360; Phase setting of external synchronization 0~360
        ('byExternalSync', C_BYTE), # 外部同步信号输入,0-内部同步 1-外部同步; External synchronization signal input, 0-internal synchronization 1-external synchronization
        ('bySwitchMode', C_BYTE), # 0-不切换，总是使用白天配置；1-根据亮度切换；2-根据时间切换；3-不切换，总是使用夜晚配置；4-使用普通配置;
                                  # 0-Do not switch, always use day configuration; 1- Switch according to brightness; 2- Switch according to time; 3- Don’t switch, always use night configuration; 4- Use normal configuration
        ('byDoubleExposure', C_BYTE), # 双快门, 0-不启用，1-双快门全帧率，即图像和视频只有快门参数不同，2-双快门半帧率，即图像和视频快门及白平衡参数均不同;
                                      # Double shutter, 0-not enabled, 1-double shutter full frame rate, that is, only the shutter parameters are different for image and video, 2-double shutter half frame rate, that is, the image and video shutter and white balance parameters are different
        ('byWideDynamicRange', C_BYTE), # 宽动态值; Wide dynamic value
        ('stuNightOptions', CFG_VIDEO_IN_NIGHT_OPTIONS),    # 夜晚参数; Night parameters
        ('stuFlash', CFG_FLASH_CONTROL),                    # 闪光灯配置; Flash configuration
        ('stuSnapshot', CFG_VIDEO_IN_SNAPSHOT_OPTIONS),     # 抓拍参数, 双快门时有效; Snapshot parameters, valid when double shutter
        ('stuFishEye', CFG_FISH_EYE),                       # 鱼眼镜头; Fisheye lens
        ('byFocusMode', C_BYTE),    # 0-关闭，1-辅助聚焦，2-自动聚焦; 0-off, 1-assisted focus, 2-auto focus
        ('reserved', C_BYTE*28),    # 保留; reserved
        ('byGainMin', C_BYTE),      # 增益下限; Gain lower limit
        ('byGainMax', C_BYTE),      # 增益上限; Gain upper limit
        ('byAntiFlicker', C_BYTE),  # 防闪烁模式; Anti-flicker mode; 0-Outdoor 1-50Hz防闪烁 2-60Hz防闪烁
        ('byExposureMode', C_BYTE), # 曝光模式调节 曝光等级为自动曝光时有效，取值：0-默认自动，1-增益优先，2-快门优先,4-手动;
                                    # Exposure mode adjustment. The exposure level is effective when the exposure level is automatic. Values: 0-default automatic, 1-gain priority, 2-shutter priority, 4-manual
        ('byGlareInhibition', C_BYTE),  # 强光抑制 0-关闭， 1~100为范围值; Strong light suppression 0-off, 1~100 is the range value
        ('stuBacklightRegion', CFG_RECT),  # 背光补偿区域; Backlight compensation area
        ('stuNormalOptions', CFG_VIDEO_IN_NORMAL_OPTIONS), # 普通参数; Common parameters
    ]

class NET_VIDEOIN_EXPOSURE_SHUTTER_INFO(Structure):
    """
    GetConfig和SetConfig接口,曝光快门属性配置; GetConfig and SetConfig interfaces,Exposure shutter property configuration
    """
    _fields_ = [
        ('dwSize',C_DWORD),         # 结构体大小; struct size
        ('bAutoSyncPhase', C_BOOL), # 自动相位调节使能; Automatic phase adjustment enable
        ('fShutter', c_float),      # 快门值，AutoSyncPhase为true时有效，毫秒为单位，取值0.1ms~80ms; Shutter value, valid when AutoSyncPhase is true, in milliseconds, the value is 0.1ms~80ms
                                    # 且必须不小于NET_VIDEOIN_EXPOSURE_NORMAL_INFO中的"ExposureValue1"、不大于"ExposureValue2"; And must be no less than "ExposureValue1" and no greater than "ExposureValue2" in NET_VIDEOIN_EXPOSURE_NORMAL_INFO
        ('nPhase', c_int),          # 相位值,取值0~360°; Phase value, value is 0~360°
    ]

class CFG_THERMO_GAIN(Structure):
    """
    增益设置; Gain setting
    """
    _fields_ = [
        ('nAgc', c_int),        # 自动增益控制 [0-255]具体取值范围由能力决定; Automatic gain control [0-255] The specific value range is determined by the ability
        ('nAgcMaxGain', c_int), # 最大自动增益 [0-255]具体取值范围由能力决定; Maximum automatic gain [0-255] The specific value range is determined by the ability
        ('nAgcPlateau', c_int), # 增益均衡 具体取值范围由能力决定; Gain equalization The specific value range is determined by ability
    ]

class CFG_THERMO_AUTO_GAIN(Structure):
    """
    热成像自动增益设置; Thermal imaging automatic gain setting
    """
    _fields_ = [
        ('nLowToHigh', c_int),  # 温度超过此设定值时，自动切换到高模式; When the temperature exceeds this set value, it will automatically switch to high temperature mode
        ('nLHROI', c_int),      # 由低切换到高时的ROI 百分比0~100; ROI percentage when switching from low temperature to high temperature 0~100
        ('nHighToLow', c_int),  # 温度下降到此设定值时，自动切换到低模式; When the temperature drops to this set value, it will automatically switch to low temperature mode
        ('nHLROI', c_int),      # 由高切换到低时的ROI 百分比0~100; ROI percentage when switching from high temperature to low temperature 0~100
    ]

class CFG_THERMOGRAPHY_OPTION(Structure):
    """
    热成像配置，单个模式的配置; Thermal imaging configuration, single mode configuration
    """
    _fields_ = [
        ('nEZoom', c_int),      # 倍数; multiple
        ('nThermographyGamma', c_int),  # 伽马值; Gamma value
        ('nColorization', c_int),       # 伪彩色，见 NET_THERMO_COLORIZATION; Pseudo color, see NET_THERMO_COLORIZATION
        ('nSmartOptimizer', c_int),     # 智能场景优化指数 0 ~100， 具体取值范围由能力决定; Intelligent scene optimization index 0 ~ 100, the specific value range is determined by ability
        ('bOptimizedRegion', C_BOOL),   # 是否开启感兴趣区域，只有感兴趣区域内的信息会被纳入统计用来做自动亮度调整（AGC）; Whether to enable the area of interest, only the information in the area of interest will be included in the statistics for automatic brightness adjustment (AGC)
        ('nOptimizedROIType', c_int),   # 感兴趣区域类型，见 NET_THERMO_ROI; Type of region of interest, see NET_THERMO_ROI
        ('nCustomRegion', c_int),       # 自定义区域个数; Number of custom regions
        ('stCustomRegions', NET_RECT*64),# 自定义区域，仅在 nOptimizedROIType 为 NET_THERMO_ROI_CUSTOM 时有效; Custom area, only valid when nOptimizedROIType is NET_THERMO_ROI_CUSTOM
        ('Reserved', c_char*256),       # 保留; reserved
        ('stuLowTempGain', CFG_THERMO_GAIN),    # 温度异常增益设置; Gain setting at low temperature
        ('nGainMode', c_int),                   # 增益模式，参见 CFG_THERMO_GAIN_MODE; Gain mode, see CFG_THERMO_GAIN_MODE
        ('stAutoGain', CFG_THERMO_AUTO_GAIN),   # 自动增益设置，只在增益模式为 CFG_THERMO_GAIN_MODE_AUTO 有效; Automatic gain setting, only valid when the gain mode is CFG_THERMO_GAIN_MODE_AUTO
        ('stuHighTempGain', CFG_THERMO_GAIN),   # 温度异常增益设置; Gain setting at high temperature
        ('nBaseBrightness', c_int),             # 基准亮度; Reference brightness
        ('nStretchIntensity', c_int),           # 拉伸强度; Tensile Strength
        ('stuContrastRect', NET_RECT),          # 区域增强位置,增加本区域与周边的对比度,8192坐标系; Area enhancement position, increase the contrast between this area and the surrounding area, 8192 coordinate system
    ]

class CFG_THERMOGRAPHY_INFO(Structure):
    """
    热成像配置; Thermal imaging configuration
    """
    _fields_ = [
        ('nModeCount', c_int),                      # 模式个数，目前只有一个; The number of modes, currently there is only one
        ('stOptions', CFG_THERMOGRAPHY_OPTION * 16),# 对应不同模式的配置; Corresponding to the configuration of different modes
    ]

class PTZ_LOCATION_SPEED_UNIT(Structure):
    """
    云台控制坐标,速度单元; PTZ control coordinates, speed unit
    """
    _fields_ = [
        ('nSpeedX', c_int),     # 云台水平角速度的真实值,无范围限定(超过云台最大速度时以云台最大速度移动),左为负、右为正,1000代表10°/s，扩大100倍表示
                                # The true value of the horizontal angular velocity of the gimbal, unlimited range (when the maximum speed of the gimbal is exceeded, it will move at the maximum speed of the gimbal), the left is negative, the right is positive, 1000 represents 10°/s, and it is enlarged by 100 times.
        ('nSpeedY', c_int),     # 云台垂直角速度的真实值,无范围限定(超过云台最大速度时以云台最大速度移动),上为负、下为正,1000代表10°/s，扩大100倍表示
                                # The true value of the vertical angular velocity of the gimbal, unlimited range (when the maximum speed of the gimbal is exceeded, it will move at the maximum speed of the gimbal), the upper is negative, the lower is positive, 1000 represents 10°/s, and it is expressed by a factor of 100
        ('szReserve', c_char*32)# 预留字节; Reserved byte
    ]

class PTZ_LOCATION_TRACK_OBJECT(Structure):
    """
    跟踪物体信息; Tracking object information
    """
    _fields_ = [
        ('nCommand', c_uint),     # 指令, 0:无效, 1:检测开启,自主跟踪开启, 2:检测开启,自主跟踪关闭, 3:检测关闭,跟踪关闭, 4:检测关闭,普通抓图上报;nstruction, 0: Invalid, 1: Detection on, Autonomous tracking on, 2: Detection on, Autonomous tracking off, 3: Detection off, Tracking off, 4: Detection off, Normal capture report
        ('nLinkObjectID', c_uint),     # 联动物体ID;Linked object ID
        ('nLinkEventID', c_uint),     # 联动事件ID;Linkage Event ID
        ('nAlarmType', c_uint),     # 报警类型, 第0bit位表示是否超速(1:超速, 0:未超速), 第1bit位表示是否AIS匹配, 第2bit位表示是否禁行, 第3bit位表示是否逆行;Alarm type, the 0th bit indicates whether there is overspeed (1: overspeed, 0: no overspeed), the 1st bit indicates whether AIS matches, the 2nd bit indicates whether driving is prohibited, and the 3rd bit indicates whether driving is in reverse
        ('nSpeedValue', c_uint),     # 速度，单位米/秒，扩大100倍;Speed, in meters/second, expanded by 100 times
        ('nLongitude', c_uint),     # 经度，单位百万分之一度;Longitude, in millionths of a degree
        ('nLatitude', c_uint),     # 纬度，单位百万分之一度;Latitude, in millionths of a degree
        ('nDistance', c_uint),     # 目标距离，单位米，扩大100倍表示;Target distance, in meters, multiplied by 100 times
        ('szObjectType', c_char*16),# 跟踪物体类型;Tracking object type
        ('stuLinkRealUTC', NET_TIME),   # 外部设备（如雷达）识别到目标上报报警的时间;The time when external devices (such as radar) recognize the target and report an alarm
        ('nAzimuth', c_int),     # 航向：正北方向为0° 顺时针为正，范围 0-360°，扩大100倍表示;Heading: 0 ° due north, clockwise as positive, range 0-360 °, expanded by 100 times to indicate
        ('szLinkTargetUUID', c_char*32),# 目标点唯一id;Unique ID of the target point
        ('szReserve', c_char*1028)# 预留字节; Reserved byte
    ]
    
class PTZ_CONTROL_INTELLI_TRACKMOVE(Structure):
    """
    云台连续移动,枪球联动专用结构. 对应操作 DH_EXTPTZ_INTELLI_TRACKMOVE; The gimbal moves continuously, and the gun-ball linkage is a special structure. Corresponding operation DH_EXTPTZ_INTELLI_TRACKMOVE
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; struct size;
        ('nChannelID', c_int),  # 通道号; Channel number
        ('nFlag', c_int),       # 移动标识位; Mobile logo
                                # 0:起始locate定位使用,speed速度无效,position的变倍值有效; 0: The initial locate is used, the speed is invalid, and the zoom value of position is valid
                                # 1:持续跟踪移动使用,speed速度无效,position的变倍值无效; 1: Continue to track and move, the speed speed is invalid, and the position zoom value is invalid
                                # 2:持续跟踪移动使用,speed速度有效,position的变倍值无效; 2: Continue to track the use of movement, the speed speed is valid, and the position zoom value is invalid
        ('stuPosition', PTZ_SPACE_UNIT),        # 云台绝对移动位置; Absolute moving position of gimbal
        ('stuSpeed', PTZ_LOCATION_SPEED_UNIT),   # 云台运行速度; PTZ operating speed
        ('bTrackObject', C_BOOL),   # 是否下发跟踪物体信息; Is tracking object information issued
        ('stuTrackObject', PTZ_LOCATION_TRACK_OBJECT)   # 跟踪物体信息; Tracking object information
    ]


class NET_RADIOMETRY_METADATA(Structure):
    """
    热图元数据信息; Heat map metadata information
    """
    _fields_ = [
        ('nHeight', c_int),     # 高; height
        ('nWidth', c_int),      # 宽; width
        ('nChannel', c_int),    # 通道; channels
        ('stTime', NET_TIME),   # 获取数据时间; Time to get data
        ('nLength', c_int),     # 数据大小; data len
        ('szSensorType', c_char * 64),  # 机芯类型; Movement type
        ('nUnzipParamR', c_int),    # 解压缩参数R; Decompression parameter R
        ('nUnzipParamB', c_int),    # 解压缩参数B; Decompression parameter B
        ('nUnzipParamF', c_int),    # 解压缩参数F; Decompression parameter F
        ('nUnzipParamO', c_int),    # 解压缩参数O; Decompression parameter O
        ('Reserved', c_char * 256), # 保留字节;byte reserved
    ]

class NET_RADIOMETRY_DATA(Structure):
    """
    fRadiometryAttachCB 回调使用,热图数据; fRadiometryAttachCB callback use, heat map data
    """
    _fields_ = [
        ('stMetaData', NET_RADIOMETRY_METADATA), # 元数据; Metadata
        ('pbDataBuf', c_char_p),  # 热图数据缓冲区（压缩过的数据,里面是每个像素点的温度数据,可以使用元数据信息解压）;Heat map data buffer (compressed data, which contains the temperature data of each pixel, which can be decompressed using metadata information)
        ('dwBufSize', C_DWORD), # 热图数据缓冲区大小; Heat map data buffer size
        ('reserved', c_char * 512), # 保留字节;byte reserved
    ]

class NET_IN_RADIOMETRY_ATTACH(Structure):
    """
    CLIENT_RadiometryAttach 入参 ; CLIENT_RadiometryAttach input
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; Struct size
        ('nChannel', c_int),    # 视频通道号 -1 表示全部; Video channel number, -1 means all
        ('cbNotify', CB_FUNCTYPE(None, C_LLONG, POINTER(NET_RADIOMETRY_DATA), c_int, C_LDWORD)),  # 状态回调函数指针; State callback function pointer
        ('dwUser', C_LDWORD),   # 用户数据; user data
    ]

class NET_OUT_RADIOMETRY_ATTACH(Structure):
    """
    CLIENT_RadiometryAttach 出参 ; CLIENT_RadiometryAttach output
    """
    _fields_ = [
        ('dwSize', C_DWORD)  # 结构体大小; Struct size
    ]

class NET_IN_RADIOMETRY_FETCH(Structure):
    """
    CLIENT_RadiometryFetch 入参; CLIENT_RadiometryFetch input
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; Struct size
        ('nChannel', c_int)     # 通道号, 通道号要与订阅时一致, -1除外; Channel number, the channel number should be the same as when subscribing, except -1
    ]

class NET_OUT_RADIOMETRY_FETCH(Structure):
    """
    CLIENT_RadiometryFetch 出参; CLIENT_RadiometryFetch output
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; Struct size
        ('nStatus', c_int)      # 0: 未知, 1: 空闲, 2: 获取热图中; 0: unknown, 1: idle, 2: get heat map
    ]

class CFG_RADIOMETRY_ALARMSETTING(Structure):
    """
    测温点报警设置; Temperature point alarm setting
    """
    _fields_ = [
        ('nId', c_int), # 报警唯一编号 报警编号统一编码
        ('bEnable', C_BOOL),        # 是否开启该点报警
        ('nResultType', c_int),     # 测温报警结果类型，见 CFG_STATISTIC_TYPE，可取值
                                    # 点测温：具体值
                                    # 线测温：最大, 最小, 平均
                                    # 区域测温：最大, 最小, 平均, 标准, 中间, ISO
        ('nAlarmCondition', c_int), # 报警条件，见 CFG_COMPARE_RESULT
        ('fThreshold', c_float),    # 报警阈值温度 浮点数
        ('fHysteresis', c_float),   # 温度误差，浮点数，比如0.1 表示正负误差在0.1范围内
        ('nDuration', c_int)        # 阈值温度持续时间	单位：秒
    ]

class CFG_RADIOMETRY_LOCALPARAM(Structure):
    """
    测温规则本地参数配置; Local parameter configuration of temperature rules
    """
    _fields_ = [
        ('bEnable', C_BOOL),    # 是否启用本地配置
        ('fObjectEmissivity', c_float), # 目标辐射系数 浮点数 0~1
        ('nObjectDistance', c_int),     # 目标距离
        ('nRefalectedTemp', c_int),     # 目标反射温度
    ]

class CFG_RADIOMETRY_RULE(Structure):
    """
    测温规则; Temperature rules
    """
    _fields_ = [
        ('bEnable', C_BOOL),    # 测温使能
        ('nPresetId', c_int),   # 预置点编号
        ('nRuleId', c_int),     # 规则编号
        ('szName', c_char * 128), # 自定义名称
        ('nMeterType', c_int),  # 测温模式的类型，见 NET_RADIOMETRY_METERTYPE
        ('stCoordinates', CFG_POLYGON * 64), # 测温点坐标	使用相对坐标体系，取值均为0~8191
        ('nCoordinateCnt', c_int),  # 测温点坐标实际个数
        ('nSamplePeriod', c_int),   # 温度采样周期 单位 : 秒
        ('stAlarmSetting', CFG_RADIOMETRY_ALARMSETTING * 64),   # 测温点报警设置
        ('nAlarmSettingCnt', c_int), # 测温点报警设置实际个数
        ('stLocalParameters', CFG_RADIOMETRY_LOCALPARAM),   # 本地参数配置
        ('emAreaSubType', C_ENUM),     # 区域测温的子类型 EM_CFG_AREA_SUBTYPE
    ]

class NET_A_CFG_RADIOMETRY_RULE_EX(Structure):
    """
    测温规则扩展
    Temperature Monitoring ruleEX
    """
    _fields_ = [
        ('nBlackBodyTemp', c_int),  # 标定黑体温度，精度0.1，实际值扩大了10倍；比如显示是38度，实际该值获取的是380；如果需要设置39度，如该值需要传入390。;Black Body Temp,The accuracy is 0.1, and the actual value is increased by 10 times; For example, the display is 38 degrees, and the actual value is 380; If you need to set 39 degrees, for example, this value needs to be passed in 390;
        ('byReserved', c_char * 252),  # 保留字节;Reserved;
    ]

class CFG_RADIOMETRY_RULE_INFO(Structure):
    """
    测温规则配置结构; Temperature rule configuration structure
    """
    _fields_ = [
        ('nCount', c_int),      # 规则个数; rule number
        ('stRule', CFG_RADIOMETRY_RULE * 512),   # 测温规则; Temperature rules
        ('stRuleEx', NET_A_CFG_RADIOMETRY_RULE_EX * 512),  # 测温规则-扩展新增的字段;Temperature rule-EX;
    ]

class NET_COAXIAL_CONTROL_IO_INFO(Structure):
    """
    同轴IO信息结构体; Coaxial IO information structure
    """
    _fields_ = [
        ('emType', C_ENUM),     # 同轴IO控制类型 0:未知 1:白光灯 2:speak音频; Coaxial IO control type 0: unknown 1: white light 2: speak audio
        ('emSwicth', C_ENUM),   # 同轴IO控制开关 0:未知 1:开 2:关; Coaxial IO control switch 0: unknown 1: on 2: off
        ('emMode', C_ENUM),     # 同轴IO触发方式 0:未知 1:联动触发 2:手动触发; Coaxial IO trigger mode 0: unknown 1: linkage trigger 2: manual trigger
        ('byReserved', C_BYTE * 128),   # 预留字节; Reserved;
    ]

class NET_IN_CONTROL_COAXIAL_CONTROL_IO(Structure):
    """
    发送同轴IO控制命令, CLIENT_ControlDeviceEx 入参 对应 DH_CTRL_COAXIAL_CONTROL_IO;
    Send coaxial IO control command, CLIENT_ControlDeviceEx input parameter corresponds to DH_CTRL_COAXIAL_CONTROL_IO
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; struct size;
        ('nChannel', c_int),    # 通道号; channel
        ('nInfoCount', c_int),  # 同轴IO信息个数; Number of coaxial IO information
        ('stInfo', NET_COAXIAL_CONTROL_IO_INFO * 8), # 同轴IO信息; coaxial IO information
    ]

class NET_OUT_CONTROL_COAXIAL_CONTROL_IO(Structure):
    """
    发送同轴IO控制命令, CLIENT_ControlDeviceEx 出参 对应 DH_CTRL_COAXIAL_CONTROL_IO;
    Send coaxial IO control command, CLIENT_ControlDeviceEx output parameter corresponds to DH_CTRL_COAXIAL_CONTROL_IO
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; struct size;
    ]

class NET_IN_GET_SOFTWAREVERSION_INFO(Structure):
    """
    CLIENT_GetSoftwareVersion 入参; CLIENT_GetSoftwareVersion input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; struct size;
    ]

class NET_PERIPHERAL_VERSIONS(Structure):
    """
    设备的外设软件版本
    Peripheral version
    """
    _fields_ = [
        ('szVersion', c_char * 32),  # 对应外设的版本信息;Peripheral version;
        ('emPeripheralType', C_ENUM),  # 外设类型 Refer: EM_PERIPHERAL_TYPE;Peripheral type Refer: EM_PERIPHERAL_TYPE;
        ('szBuildDate', c_char * 24),  # 对应外设版本的编译日期，精确到天;The compilation date of the corresponding peripheral version, accurate to days;
        ('byReserved', C_BYTE * 228),  # 保留字节;Reserved;
    ]

class NET_OUT_GET_SOFTWAREVERSION_INFO(Structure):
    """
    CLIENT_GetSoftwareVersion 出参; CLIENT_GetSoftwareVersion output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; struct size;
        ('szVersion', c_char * 64),     # 软件版本; software version
        ('stuBuildDate', NET_TIME),     # 日期; date
        ('szWebVersion', c_char * 16),  # web软件信息; web software version
        ('szSecurityVersion', c_char * 64),# 安全基线版本; Security Baseline Version
        ('nPeripheralNum', c_int),      # 返回的外设数量; Number of peripherals returned
        ('stuPeripheralVersions', NET_PERIPHERAL_VERSIONS * 32),    # 设备的外设软件版本; Peripheral software version of the device
        ('szAlgorithmTrainingVersion', c_char * 64),  # 算法训练对外代号;Algorithm training external code;
    ]

class CFG_NTP_SERVER(Structure):
    """
    NTP服务器; ntp server
    """
    _fields_ = [
        ('bEnable', C_BOOL),    # enable
        ('szAddress', c_char * 256),    # IP地址或网络名; IP address or network name
        ('nPort', c_int),       # 端口号; port
    ]

class CFG_NTP_INFO(Structure):
    """
    时间同步服务器配置; Time synchronization server configuration
    """
    _fields_ = [
        ('bEnable', C_BOOL),        # 使能开关; enable switch
        ('szAddress', c_char * 256),# IP地址或网络名; IP address or network name
        ('nPort', c_int),           # 端口号; port
        ('nUpdatePeriod', c_int),   # 更新周期 单位为分钟; Update cycle, in minutes
        ('emTimeZoneType', C_ENUM), # 时区; time zone
        ('szTimeZoneDesc', c_char * 128),# 时区描述; time zone description
        ('nSandbyServerNum', c_int),    # 实际备用NTP服务器个数; Actual number of backup NTP servers
        ('stuStandbyServer', CFG_NTP_SERVER * 4), # 备选NTP服务器地址; Alternative NTP server address
        ('nTolerance', c_int),      # (机器人使用)表示设置的时间和当前时间的容差，单位为秒，如果设置的时间和当前的时间在容差范围内，则不更新当前时间。0 表示每次都修改
                                    # (Used by the robot) indicates the tolerance between the set time and the current time, in seconds.
                                    # If the set time and the current time are within the tolerance range, the current time will not be updated.0 means modify every time
    ]

class DH_VERSION_INFO(Structure):
    """
    设备软件版本信息,高16位表示主版本号,低16位表示次版本号
    Device software version information, the upper 16 bits represent the major version number, and the lower 16 bits represent the minor version number
    """
    _fields_ = [
        ('dwSoftwareVersion', C_DWORD),
        ('dwSoftwareBuildDate', C_DWORD),
        ('dwDspSoftwareVersion', C_DWORD),
        ('dwDspSoftwareBuildDate', C_DWORD),
        ('dwPanelVersion', C_DWORD),
        ('dwPanelSoftwareBuildDate', C_DWORD),
        ('dwHardwareVersion', C_DWORD),
        ('dwHardwareDate', C_DWORD),
        ('dwWebVersion', C_DWORD),
        ('dwWebBuildDate', C_DWORD),
    ]

class DH_DSP_ENCODECAP(Structure):
    """
    DSP能力描述,对应CLIENT_GetDevConfig接口; DSP capability description, corresponding to the CLIENT_GetDevConfig interface
    """
    _fields_ = [
        ('dwVideoStandardMask', C_DWORD),   # 视频制式掩码,按位表示设备能够支持的视频制式; Video format mask, bitwise indicates the video format that the device can support
        ('dwImageSizeMask', C_DWORD),       # 分辨率掩码,按位表示设备能够支持的分辨率设置; Resolution mask, bitwise representation of the resolution settings that the device can support
        ('dwEncodeModeMask', C_DWORD),      # 编码模式掩码,按位表示设备能够支持的编码模式设置; Encoding mode mask, bitwise indicates the encoding mode settings that the device can support
        ('dwStreamCap', C_DWORD),           # 按位表示设备支持的多媒体功能; A bitwise representation of the multimedia features supported by the device
                                            # 第一位表示支持主码流; The first bit indicates that the main stream is supported
                                            # 第二位表示支持辅码流1; The second digit indicates that auxiliary stream 1 is supported
                                            # 第三位表示支持辅码流2; The third digit indicates that auxiliary stream 2 is supported
                                            # 第五位表示支持jpg抓图; The fifth digit indicates that jpg snapshots are supported
        ('dwImageSizeMask_Assi', C_DWORD * 8), # 表示主码流为各分辨率时,支持的辅码流分辨率掩码; Indicates the supported sub-stream resolution mask when the primary stream is each resolution
        ('dwMaxEncodePower', C_DWORD),      # DSP支持的最高编码能力; Highest encoding capability supported by DSP
        ('wMaxSupportChannel', c_uint16),    # 每块DSP支持最多输入视频通道数; Each DSP supports the maximum number of input video channels
        ('wChannelMaxSetSync', c_uint16),    # DSP每通道的最大编码设置是否同步；0：不同步,1：同步;
                                            # Whether the maximum encoding setting of each channel of DSP is synchronized; 0: not synchronized, 1: synchronized
    ]

class DHDEV_SYSTEM_ATTR_CFG(Structure):
    """
    系统信息; system message
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; struct size
        # 下面是设备的只读部分; Below is the read-only part of the device
        ('stVersion', DH_VERSION_INFO),
        ('stDspEncodeCap', DH_DSP_ENCODECAP), # DSP能力描述; DSP Capability Description
        ('szDevSerialNo', C_BYTE * 48),         # 序列号; serial number
        ('byDevType', C_BYTE),                  # 设备类型,见枚举 EM_A_NET_DEVICE_TYPE; Device type, see enumeration EM_A_NET_DEVICE_TYPE
        ('szDevType', C_BYTE * 32),             # 设备详细型号,字符串格式,可能为空; The detailed model of the device, in string format, may be empty
        ('byVideoCaptureNum', C_BYTE),          # 视频口数量; Number of video ports
        ('byAudioCaptureNum', C_BYTE),          # 音频口数量; Number of audio ports
        ('byTalkInChanNum', C_BYTE),            # 对讲输入接口数量; Number of intercom input interfaces
        ('byTalkOutChanNum', C_BYTE),           # 对讲输出接口数量; Number of intercom output interfaces
        ('byDecodeChanNum', C_BYTE),            # NSP
        ('byAlarmInNum', C_BYTE),               # 报警输入口数; Number of alarm input ports
        ('byAlarmOutNum', C_BYTE),              # 报警输出口数; Number of alarm output ports
        ('byNetIONum', C_BYTE),                 # 网络口数; Number of network ports
        ('byUsbIONum', C_BYTE),                 # USB口数量; Number of usb ports
        ('byIdeIONum', C_BYTE),                 # IDE数量; Number of IDE
        ('byComIONum', C_BYTE),                 # 串口数量; Number of serial ports
        ('byLPTIONum', C_BYTE),                 # 并口数量; Number of parallel ports
        ('byVgaIONum', C_BYTE),                 # NSP
        ('byIdeControlNum', C_BYTE),            # NSP
        ('byIdeControlType', C_BYTE),           # NSP
        ('byCapability', C_BYTE),               # NSP,扩展描述; NSP, Extended Description
        ('byMatrixOutNum', C_BYTE),             # 视频矩阵输出口数; Number of video matrix output ports
        # 下面是设备的可写部分; Below is the writable part of the device
        ('byOverWrite', C_BYTE),                # 硬盘满处理方式(覆盖、停止); Disk full processing method (overwrite, stop)
        ('byRecordLen', C_BYTE),                # 录象打包长度; Video Packing Length
        ('byDSTEnable', C_BYTE),                # 是否实行夏令时 1-实行 0-不实行; Whether to implement daylight saving time 1-implement 0-do not implement
        ('wDevNo', c_uint16),                    # 设备编号,用于遥控; Device number, for remote control
        ('byVideoStandard', C_BYTE),            # 视频制式:0-PAL,1-NTSC; Video format: 0-PAL, 1-NTSC
        ('byDateFormat', C_BYTE),               # 日期格式; date format
        ('byDateSprtr', C_BYTE),                # 日期分割符(0：".",1："-",2："/"); date separator(0：".",1："-",2："/")
        ('byTimeFmt', C_BYTE),                  # 时间格式 (0-24小时,1－12小时); Time format (0-24 hours, 1-12 hours)
        ('byLanguage', C_BYTE),                 # 枚举值详见DH_LANGUAGE_TYPE; 枚举值详见DH_LANGUAGE_TYPE
    ]

class AV_CFG_ChannelName(Structure):
    """
    通道名称; channel name
    """
    _fields_ = [
        ('nStructSize', c_int),
        ('nSerial', c_int),             # 摄像头唯一编号; camera unique number
        ('szName', c_char * 256),       # 通道名; channel name
    ]

class ALARM_FRONTDISCONNET_INFO(Structure):
    """
    前端断网报警信息; Front-end disconnection alarm information
    """
    _fields_ = [
        ('dwSize', C_DWORD),    # 结构体大小; struct size
        ('nChannelID', c_int),  # 通道号; channel number
        ('nAction', c_int),     # 0:开始 1:停止; 0:start 1:stop
        ('stuTime', NET_TIME),  # 事件发生时间; event time
        ('szIpAddress', c_char * 260), # 前端IPC的IP地址; IP address of the front-end IPC
        ('stGPSStatus', NET_GPS_STATUS_INFO), # GPS信息; GPS information
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class ALARM_STORAGE_LOW_SPACE_INFO(Structure):
    """
    存储容量不足事件; Insufficient storage capacity event
    """
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('nAction', c_int),  # 0:开始 1:停止; 0:start 1:stop;
        ('szName', c_char * 128),  # 事件名称; name;
        ('szDevice', c_char * 128),  # 存储设备名称; device name;
        ('szGroup', c_char * 128),  # 存储组名称; group name;
        ('nTotalSpace', c_int64),  # 总容量, byte; total space byte;
        ('nFreeSpace', c_int64),  # 剩余容量, byte; free space byte;
        ('nPercent', c_int),  # 已经使用的百分比; used percent;
        ('stuTime', NET_TIME_EX),  # 事件触发时间; Event occurrence time;
        ('stGPSStatus', NET_GPS_STATUS_INFO),  # GPS信息; GPS info;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class ALARM_STORAGE_FAILURE(Structure):
    """
    存储异常报警; Storage exception alarm
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; struct size;
        ('ActionType', C_UINT),  # 0：停止, 1：开始; 0:stop 1:start;
        ('szProtocol', c_char * 128),  # 协议类型,目前只支持FTP; protocol type;
        ('szServerAddr', c_char * 64),  # 服务器IP地址; server device's ip;
        ('dwPort', C_DWORD),  # 端口号; port number;
        ('stuTime', NET_TIME),  # 事件发生时间; event happen time;
        ('nChannel', c_int),  # 通道号, 从1开始, 0表示不区分通道; channel, from 1, 0 means does not distinguish;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class ALARM_RECORD_CHANGED_INFO_EX(Structure):
    """
    录像状态变化报警(DH_ALARM_RECORD_CHANGED_EX); Recording state change alarm (DH_ALARM_RECORD_CHANGED_EX)
    """
    _fields_ = [
        ('nAction', c_int),  # 0:开始 1:停止; 0:start 1:stop;
        ('nChannel', c_int),  # 通道; channel;
        ('szStoragePoint', c_char * 64),  # 录像存储点; StoragePoint;
        ('emStreamType', C_ENUM),  # 录像码流,参考枚举NET_STREAM_TYPE; stream type,Please refer to NET_STREAM_TYPE;
        ('szUser', c_char * 128),  # 操作用户; username;
        ('byReserved', C_BYTE * 828),  # 保留; reserved;
    ]

class ALARM_REMOTE_ALARM_INFO(Structure):
    """
    远程外部报警信息; Remote external alarm information
    """
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('nChannelID', c_int),  # 通道号,从1开始; channel ID,from 1;
        ('nState', c_int),  # 报警状态,0-报警复位,1-报警置位; state,0-reset,1-setting;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class ALARM_RECORD_SCHEDULE_CHANGE_INFO(Structure):
    """
    录像计划改变事件(对应事件 DH_ALARM_RECORD_SCHEDULE_CHANGE); Recording plan change event (corresponding to event DH_ALARM_RECORD_SCHEDULE_CHANGE)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号; Channel ID;
        ('nEventID', c_int),  # 事件ID; Event ID;
        ('dbPTS', c_double),  # 时间戳(单位是毫秒); Time stamp (Unit:ms);
        ('stuTime', NET_TIME_EX),  # 事件发生的时间; Event occurrence time;
        ('nEventAction', c_int),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束; Event operation. 0=pulse event.1=continues event begin. 2=continuous event stop;
        ('szUser', c_char * 128),  # 操作用户; Username;
        ('byReserved', C_BYTE * 1024),  # 保留字节; Reserved;
    ]

class NET_MEDIA_QUERY_TRAFFICCAR_PARAM_EX(Structure):
    """
    DH_MEDIA_QUERY_TRAFFICCAR对应的查询条件 参数扩展; Query conditions corresponding to DH_MEDIA_QUERY_TRAFFICCAR Parameter expansion
    """
    _fields_ = [
        ('szViolationCode', c_char * 16),  # 违法代码; Violation code;
        ('szCountry', c_char * 4),  # 国籍，2字节，符合ISO3166规范; Nationality, 2 bytes, in line with ISO3166 specification;
        ('bOnlySupportRealUTC', C_BOOL),  # 为TRUE表示仅下发stuStartTimeRealUTC和stuEndTimeRealUTC(不下发StartTime, EndTime), 为FALSE表示仅下发StartTime, EndTime(不下发stuStartTimeRealUTC和stuEndTimeRealUTC); TRUE means only send stuStartTimeRealUTC and stuEndTimeRealUTC (do not send StartTime, EndTime), FALSE means only send StartTime, EndTime (do not send stuStartTimeRealUTC and stuEndTimeRealUTC);
        ('stuStartTimeRealUTC', NET_TIME),  # UTC开始时间(标准UTC时间), 与stuEndTimeRealUTC配对使用，与(StartTime, EndTime)互斥; UTC start time (standard UTC time), paired with stuEndTimeRealUTC, mutually exclusive with (StartTime, EndTime);
        ('stuEndTimeRealUTC', NET_TIME),  # UTC结束时间(标准UTC时间), 与stuStartTimeRealUTC配对使用，与(StartTime, EndTime)互斥; UTC end time (standard UTC time), paired with stuStartTimeRealUTC, mutually exclusive with (StartTime, EndTime);
        ('szPlateCode', c_char * 16),  # 车牌代码; Plate code;
        ('byReserved', C_BYTE * 952),  # 保留字节; Reserved;
    ]

class MEDIA_QUERY_TRAFFICCAR_PARAM(Structure):
    """
    DH_MEDIA_QUERY_TRAFFICCAR对应的查询条件; Query conditions corresponding to DH_MEDIA_QUERY_TRAFFICCAR
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号从0开始,-1表示查询所有通道; The channel number begins with 0. -1 is to search information of all channels .;
        ('StartTime', NET_TIME),  # 开始时间; Start time;
        ('EndTime', NET_TIME),  # 结束时间; End time;
        ('nMediaType', c_int),  # 文件类型,0:任意类型, 1:jpg图片, 2:dav文件; File type:0=search any type.1=search jpg file;
        ('nEventType', c_int),  # 事件类型,详见"智能分析事件类型", 0:表示查询任意事件,此参数废弃,请使用pEventTypes; deprecated, to get same info, use pEventType instead;
        ('szPlateNumber', c_char * 32),  # 车牌号, "\0"则表示查询任意车牌号; Vehicle plate. "\0" is to search any plate number.;
        ('nSpeedUpperLimit', c_int),  # 查询的车速范围; 速度上限 单位: km/h; The searched vehicle speed range. Max speed unit is km/h;
        ('nSpeedLowerLimit', c_int),  # 查询的车速范围; 速度下限 单位: km/h; The searched vehicle speed range. Min speed unit is km/h;
        ('bSpeedLimit', C_BOOL),  # 是否按速度查询; TRUE:按速度查询,nSpeedUpperLimit和nSpeedLowerLimit有效。; Search according to the speed or not. TRUE: search according to the speed.nSpeedUpperLimit and nSpeedLowerLimit is valid.;
        ('dwBreakingRule', C_DWORD),  # 违章类型：,当事件类型为 EVENT_IVS_TRAFFICGATE时,第一位:逆行; 第二位:压线行驶; 第三位:超速行驶;,第四位：欠速行驶; 第五位:闯红灯;,当事件类型为 EVENT_IVS_TRAFFICJUNCTION,第一位:闯红灯; 第二位:不按规定车道行驶;,第三位:逆行; 第四位：违章掉头;,第五位:压线行驶;; Illegal type:,When event type is EVENT_IVS_TRAFFICGATE,bit1: Retrograde; bit2: Overline;,bit3: Overspend; bit4:Under speed;,bit5: RunRedLight;,When event type is EVENT_IVS_TRAFFICJUNCTION,bit1: RunRedLight; bit2: WrongLan;,bit3: Retrograde; bit4:UTurn;,bit5: Overline;;
        ('szPlateType', c_char * 32),  # 车牌类型,"Unknown" 未知,"Normal" 蓝牌黑牌,"Yellow" 黄牌,"DoubleYellow" 双层黄尾牌,"Police" 警牌,"SAR" 港澳特区号牌,"Trainning" 教练车号牌,"Personal" 个性号牌,"Agri" 农用牌,"Embassy" 使馆号牌,"Moto" 摩托车号牌,"Tractor" 拖拉机号牌,"Other" 其他号牌,"Civilaviation"民航号牌,"Black"黑牌,"PureNewEnergyMicroCar"纯电动新能源小车,"MixedNewEnergyMicroCar,"混合新能源小车,"PureNewEnergyLargeCar",纯电动新能源大车,"MixedNewEnergyLargeCar"混合新能源大车; Plate type: "Unknown" =Unknown; "Normal"=Blue and black plate. "Yellow"=Yellow plate. "DoubleYellow"=Double-layer yellow plate,"Police"=Police plate ; "SAR" =HongK SAR or Macao SAR plate; "Trainning" =rehearsal plate; "Personal"=Personal plate; "Agri"=Agricultural plate,"Embassy"=Embassy plate; "Moto"=Moto plate ; "Tractor"=Tractor plate; "Other"=Other plate;
        ('szPlateColor', c_char * 16),  # 车牌颜色, "Blue"蓝色,"Yellow"黄色, "White"白色,"Black"黑色; plate color, "Blue","Yellow", "White","Black";
        ('szVehicleColor', c_char * 16),  # 车身颜色:"White"白色, "Black"黑色, "Red"红色, "Yellow"黄色, "Gray"灰色, "Blue"蓝色,"Green"绿色; vehicle color:"White", "Black", "Red", "Yellow", "Gray", "Blue","Green";
        ('szVehicleSize', c_char * 16),  # 车辆大小类型:"Light-duty":小型车;"Medium":中型车; "Oversize":大型车; "Unknown": 未知; vehicle type:"Light-duty";"Medium"; "Oversize";
        ('nGroupID', c_int),  # 事件组编号(此值>=0时有效); id of event group(it works when >= 0);
        ('byLane', c_short),  # 车道号(此值>=0时表示具体车道,-1表示所有车道,即不下发此字段); lane number(it works when >= 0);
        ('byFileFlag', C_BYTE),  # 文件标志, 0xFF-使用nFileFlagEx, 0-表示所有录像, 1-定时文件, 2-手动文件, 3-事件文件, 4-重要文件, 5-合成文件; file flag, 0xFF-use nFileFlagEx, 0-all record, 1-timing file, 2-manual, 3-event, 4-important, 5-mosaic;
        ('byRandomAccess', C_BYTE),  # 是否需要在查询过程中随意跳转,0-不需要,1-需要; The need for random jumps in the query process, 0 - no need 1 - need;
        ('nFileFlagEx', c_int),  # 文件标志, 按位表示: bit0-定时文件, bit1-手动文件, bit2-事件文件, bit3-重要文件, bit4-合成文件, bit5-禁止名单图片 0xFFFFFFFF-所有录像; file flag, bit0-timing, bit1-manual, bit2-event, bit3-important, bit4-mosaic, 0xFFFFFFFF-all;
        ('nDirection', c_int),  # 车道方向（车开往的方向） 0-北 1-东北 2-东 3-东南 4-南 5-西南 6-西 7-西北 8-未知 -1-所有方向; direction(to the direction of car) 0-north 1-northeast 2-east 3-southeast 4-south 5-southwest 6-west 7-northwest 8-unknown -1-all directions;
        ('szDirs', c_void_p),  # 工作目录列表,一次可查询多个目录,为空表示查询所有目录。目录之间以分号分隔,如“/mnt/dvr/sda0;/mnt/dvr/sda1”,szDirs==null 或"" 表示查询所有; working directory list,can inquire multiple directory at a atime,separated by ";",example "/mnt/dvr/sda0;/mnt/dvr/sda1",if szDirs==null or szDirs == "" ,means search all;
        ('pEventTypes', c_void_p),  # 待查询的事件类型数组指针,事件类型,详见"智能分析事件类型",若为NULL则认为查询所有事件（缓冲需由用户申请）; Check the event type to be an array of pointers, event type, see "intelligent analysis event type", if the query is NULL considered all events (buffer required to apply by the user);
        ('nEventTypeNum', c_int),  # 事件类型数组大小; Event Type array size;
        ('pszDeviceAddress', c_void_p),  # 设备地址, NULL表示该字段不起作用; Device address, NULL indicates that the field does not work;
        ('pszMachineAddress', c_void_p),  # 机器部署地点, NULL表示该字段不起作用; Machine deployment locations, NULL indicates that the field does not work;
        ('pszVehicleSign', c_void_p),  # 车辆标识, 例如 "Unknown"-未知, "Audi"-奥迪, "Honda"-本田... NULL表示该字段不起作用; Vehicle identification, such as "Unknown" - unknown, "Audi" - Audi, "Honda" - Honda ... NULL indicates that the field does not work;
        ('wVehicleSubBrand', c_uint16),  # 车辆子品牌 需要通过映射表得到真正的子品牌 映射表详见开发手册; Specifies the sub-brand of vehicle,the real value can be found in a mapping table from the development manual;
        ('wVehicleYearModel', c_uint16),  # 车辆品牌年款 需要通过映射表得到真正的年款 映射表详见开发手册; Specifies the model years of vehicle. the real value can be found in a mapping table from the development manual;
        ('emSafeBeltState', C_ENUM),  # 安全带状态,参考枚举EM_SAFE_BELT_STATE; Safe belt state,Please refer to EM_SAFE_BELT_STATE;
        ('emCallingState', C_ENUM),  # 打电话状态,参考枚举EM_CALLING_STATE; Calling state,Please refer to EM_CALLING_STATE;
        ('emAttachMentType', C_ENUM),  # 车内饰品类型,参考枚举EM_ATTACHMENT_TYPE; Attachment type,Please refer to EM_ATTACHMENT_TYPE;
        ('emCarType', C_ENUM),  # 车辆类型,参考枚举EM_CATEGORY_TYPE; Car type,Please refer to EM_CATEGORY_TYPE;
        ('pstuTrafficCarParamEx', POINTER(NET_MEDIA_QUERY_TRAFFICCAR_PARAM_EX)),  # 参数扩展; parameter extension;
        ('bReserved', c_int * 4),  # 保留字段; Reserved field for future extension.;
    ]

class MEDIAFILE_TRAFFICCAR_INFO(Structure):
    """
    DH_MEDIA_QUERY_TRAFFICCAR查询出来的media文件信息; DH_MEDIA_QUERY_TRAFFICCAR查询出来的media文件信息
    """
    _fields_ = [
        ('ch', C_UINT),  # 通道号; Channel number;
        ('szFilePath', c_char * 128),  # 文件路径; File path;
        ('size', C_UINT),  # 文件长度,该字段废弃，请使用sizeEx; File length,This field is discarded,please use the sizeEx;
        ('starttime', NET_TIME),  # 开始时间; Start time;
        ('endtime', NET_TIME),  # 结束时间; End time;
        ('nWorkDirSN', C_UINT),  # 工作目录编号; Working directory serial number;
        ('nFileType', C_BYTE),  # 文件类型 1:图片 2:视频; File type. 1:picture 2:video;
        ('bHint', C_BYTE),  # 文件定位索引; File location index;
        ('bDriveNo', C_BYTE),  # 磁盘号; drive number;
        ('bReserved2', C_BYTE),  
        ('nCluster', C_UINT),  # 簇号; cluster number;
        ('byPictureType', C_BYTE),  # 图片类型或文件标记, 0-普通, 1-合成, 2-抠图。更多文件标记信息请参考 MEDIAFILE_TRAFFICCAR_INFO_EX 的 emFalgLists 字段; picture type or file flag, 0-Normal, 1-Mosaic, 2-Cutout. more flags information ref to MEDIAFILE_TRAFFICCAR_INFO_EX's filed emFalgLists;
        ('byVideoStream', C_BYTE),  # 视频码流 0-未知 1-主码流 2-辅码流1 3-辅码流2 4-辅码流; video stream 0-unknown 1-main 2-sub1 3-sub2 4-sub3;
        ('byPartition', C_BYTE),  # 精确定位号; accurate positioning No.;
        ('bReserved', C_BYTE * 1),  # 保留字段,以下是交通车辆信息; Reserved field for future extension.,The following contents is the vehicle information;
        ('szPlateNumber', c_char * 32),  # 车牌号码; Vehicle plate number;
        ('szPlateType', c_char * 32),  # 号牌类型"Unknown" 未知; "Normal" 蓝牌黑牌; "Yellow" 黄牌; "DoubleYellow" 双层黄尾牌,"Police" 警牌; "SAR" 港澳特区号牌; "Trainning" 教练车号牌; "Personal" 个性号牌; "Agri" 农用牌,"Embassy" 使馆号牌; "Moto" 摩托车号牌; "Tractor" 拖拉机号牌; "Other" 其他号牌,"Civilaviation"民航号牌,"Black"黑牌,"PureNewEnergyMicroCar"纯电动新能源小车,"MixedNewEnergyMicroCar,"混合新能源小车,"PureNewEnergyLargeCar",纯电动新能源大车,"MixedNewEnergyLargeCar"混合新能源大车; Plate type: "Unknown" =Unknown; "Normal"=Blue and black plate. "Yellow"=Yellow plate. "DoubleYellow"=Double-layer yellow plate,"Police"=Police plate ; "SAR" =HongK SAR or Macao SAR plate; "Trainning" =rehearsal plate; "Personal"=Personal plate; "Agri"=Agricultural plate,"Embassy"=Embassy plate; "Moto"=Moto plate ; "Tractor"=Tractor plate; "Other"=Other plate;
        ('szPlateColor', c_char * 16),  # 车牌颜色:"Blue","Yellow", "White","Black"; Plate color:"Blue","Yellow", "White","Black";
        ('szVehicleColor', c_char * 16),  # 车身颜色:"White", "Black", "Red", "Yellow", "Gray", "Blue","Green"; Vehicle color:"White", "Black", "Red", "Yellow", "Gray", "Blue","Green";
        ('nSpeed', c_int),  # 车速,单位Km/H; Speed. The unit is Km/H;
        ('nEventsNum', c_int),  # 关联的事件个数; Activation event amount;
        ('nEvents', c_int * 32),  # 关联的事件列表,数组值表示相应的事件,详见"智能分析事件类型"; Activation event list. The number refers to the corresponding event. Please refer to Intelligent Analytics Event Type.;
        ('dwBreakingRule', C_DWORD),  # 具体违章类型掩码,第一位:闯红灯; 第二位:不按规定车道行驶;,第三位:逆行; 第四位：违章掉头;否则默认为:交通路口事件; Detailed offense type subnet mask. The first bit means redlight offense, the second bit is illegal straight/left-turn/right-turn driving.,The third bit is the wrong way driving; the four bit is illegal U-turn. Otherwise default value is intersection accident.;
        ('szVehicleSize', c_char * 16),  # 车辆大小类型:"Light-duty":小型车;"Medium":中型车; "Oversize":大型车; Vehicle type:"Light-duty"=small;"Medium"=medium; "Oversize"=large;
        ('szChannelName', c_char * 32),  # 本地或远程的通道名称; Local or remote channel name;
        ('szMachineName', c_char * 16),  # 本地或远程设备名称; Local or remote device name;
        ('nSpeedUpperLimit', c_int),  # 速度上限 单位: km/h; up limit of speed, km/h;
        ('nSpeedLowerLimit', c_int),  # 速度下限 单位: km/h; lower limit of speed km/h;
        ('nGroupID', c_int),  # 事件里的组编号; id of event group;
        ('byCountInGroup', C_BYTE),  # 一个事件组内的抓拍张数; total count of the event group;
        ('byIndexInGroup', C_BYTE),  # 一个事件组内的抓拍序号; the index of this event;
        ('byLane', C_BYTE),  # 车道,参见MEDIA_QUERY_TRAFFICCAR_PARAM; lane number;
        ('bReserved1', C_BYTE * 21),  # 保留; reserved;
        ('stSnapTime', NET_TIME),  # 抓拍时间; snap time;
        ('nDirection', c_int),  # 车道方向,参见MEDIA_QUERY_TRAFFICCAR_PARAM; direction,MEDIA_QUERY_TRAFFICCAR_PARAM;
        ('szMachineAddress', c_char * 260),  # 机器部署地点; machine address;
        ('sizeEx', c_int64),  # 文件长度扩展，支持文件长度大于4G，单位字节; size of file extension, Support file length is greater than 4G,unit:Byte;
    ]

class NET_ATTACH_MENET_INFO(Structure):
    """
    车内饰品信息; Car interior accessories information
    """
    _fields_ = [
        ('emAttachMentType', C_ENUM),  # 车内物品类型,参考枚举EM_ATTACHMENT_TYPE; attachment type,Please refer to EM_ATTACHMENT_TYPE;
        ('bReserved1', C_BYTE * 128),  # 保留字节; Reserved;
    ]

class NET_UPLOAD_CLIENT_INFO(Structure):
    """
    客户端信息; client message
    """
    _fields_ = [
        ('szClientID', c_char * 20),  # 平台客户端的标识，当前是IPv4地址或者MAC地址; The id of clent, IPv4 address or MAC;
        ('emUploadFlag', C_ENUM),  # 平台上传标识,参考枚举EM_UPLOAD_FLAG; The upload flag of clent,Please refer to EM_UPLOAD_FLAG;
        ('stuUploadTime', NET_TIME),  # 上传到平台的UTC时间; The time to upload to clent;
        ('byReserved', C_BYTE * 64),  # 预留; Reserved bytes;
    ]

class NET_PLATE_IMAGE_INFO(Structure):
    """
    车牌图片信息
    License plate picture information
    """
    _fields_ = [
        ('szFilePath', c_char * 128),  # 图片文件路径;Picture file path;
        ('nLength', c_int),  # 图片文件大小，单位:字节;Image file size, bytes;
        ('szReserved', c_char * 252),  # 预留字段;Reserved;
    ]

class NET_CARBODY_IMAGE_INFO(Structure):
    """
    车身图片信息
    car body picture information
    """
    _fields_ = [
        ('szFilePath', c_char * 128),  # 图片文件路径;Picture file path;
        ('nLength', c_int),  # 图片文件大小，单位:字节;Image file size, bytes;
        ('szReserved', c_char * 252),  # 预留字段;Reserved;
    ]

class MEDIAFILE_TRAFFICCAR_INFO_EX(Structure):
    """
    DH_MEDIA_QUERY_TRAFFICCAR_EX查询出来的文件信息; File information queried by DH_MEDIA_QUERY_TRAFFICCAR_EX
    """
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('stuInfo', MEDIAFILE_TRAFFICCAR_INFO),  # 基本信息; Basic Information;
        ('szDeviceAddr', c_char * 256),  # 设备地址; Device Address;
        ('szVehicleSign', c_char * 32),  # 车辆标识, 例如 "Unknown"-未知, "Audi"-奥迪, "Honda"-本田...; Vehicle identification, such as "Unknown" - unknown, "Audi" - Audi, "Honda" - Honda ..;
        ('szCustomParkNo', c_char * 64),  # 自定义车位号（停车场用）; self defined parking space number, for parking,;
        ('wVehicleSubBrand', c_uint16),  # 车辆子品牌，需要通过映射表得到真正的子品牌; Specifies the sub-brand of vehicle,the real value can be found in a mapping table from the development manual;
        ('wVehicleYearModel', c_uint16),  # 车辆年款，需要通过映射表得到真正的年款; Specifies the model years of vehicle. the real value can be found in a mapping table from the development manual;
        ('stuEleTagInfoUTC', NET_TIME),  # 对应电子车牌标签信息中的过车时间(ThroughTime); corresponding to throughTime in electronic tag info;
        ('emFalgLists', C_ENUM * 128),  # 录像或抓图文件标志,参考枚举EM_RECORD_SNAP_FLAG_TYPE; record or snapshot file mark,Please refer to EM_RECORD_SNAP_FLAG_TYPE;
        ('nFalgCount', c_int),  # 标志总数; mark total;
        ('emSafeBelSate', C_ENUM),  # 安全带状态,参考枚举EM_SAFE_BELT_STATE; safe belt state,Please refer to EM_SAFE_BELT_STATE;
        ('emCallingState', C_ENUM),  # 打电话状态,参考枚举EM_CALLING_STATE; calling state,Please refer to EM_CALLING_STATE;
        ('nAttachMentNum', c_int),  # 车内物品个数; the count of attachment;
        ('stuAttachMent', NET_ATTACH_MENET_INFO * 8),  # 车内物品信息; attachment info;
        ('szCountry', c_char * 32),  # 车牌所属国家和地区; the country about the plate;
        ('emCarType', C_ENUM),  # 车辆类型,参考枚举EM_CATEGORY_TYPE; car type,Please refer to EM_CATEGORY_TYPE;
        ('emSunShadeState', C_ENUM),  # 遮阳板状态,参考枚举NET_SUNSHADE_STATE; sun shade state,Please refer to NET_SUNSHADE_STATE;
        ('emSmokingState', C_ENUM),  # 是否抽烟,参考枚举EM_SMOKING_STATE; smoking state,Please refer to EM_SMOKING_STATE;
        ('nAnnualInspection', c_int),  # 年检标个数; the count of annual inspections;
        ('byReserved', C_BYTE * 4),  # 字节对齐; Byte alignment;
        ('nPicIDHigh', c_int),  # PictureID高四字节; PictureID high 4 bytes;
        ('nPicIDLow', c_int),  # PictureID低四字节; PictureID low 4 bytes;
        ('stuClient1', NET_UPLOAD_CLIENT_INFO),  # 平台客户端1上传信息; The client 1 upload information;
        ('stuClient2', NET_UPLOAD_CLIENT_INFO),  # 平台客户端2上传信息; The client 2 upload information;
        ('szExtraPlateNumber', c_char * 96),  # 三地车牌; Three places license plate;
        ('nExtraPlateNumberNum', c_int),  # 车牌个数; Number of license plates;
        ('nEntranceTime', C_UINT),  # 车辆进站时间，时间格式：UTC时间(IVSS, 用于加油站场景); Vehicle entry time, time format: UTC time (IVSS, used for gas station scene);
        ('nOilTime', C_UINT),  # 车辆加油时间，时间格式：UTC时间(IVSS, 用于加油站场景); Vehicle refueling time, time format: UTC time (IVSS, used for gas station scenes);
        ('nExitTime', C_UINT),  # 车辆出站时间，时间格式：UTC时间(IVSS, 用于加油站场景); Vehicle exit time, time format: UTC time (IVSS, used for gas station scene);
        ('bRealUTC', C_BOOL),   # 为TRUE表示仅stuStartTimeRealUTC和stuEndTimeRealUTC有效(仅使用stuStartTimeRealUTC和stuEndTimeRealUTC), 为FALSE表示仅starttime和endtime有效(仅使用starttime和endtime, starttime和endtime在MEDIAFILE_TRAFFICCAR_INFO中);TRUE means only stuStartTimeRealUTC and stuEndTimeRealUTC are valid (only stuStartTimeRealUTC and stuEndTimeRealUTC are used), FALSE means only starttime and endtime are valid (only starttime and endtime are used, starttime and endtime are in MEDIAFILE_TRAFFICCAR_INFO);
        ('stuStartTimeRealUTC', NET_TIME),  # UTC开始时间(标准UTC时间), 与stuEndTimeRealUTC配对使用;UTC start time (standard UTC time), paired with stuEndTimeRealUTC;
        ('stuEndTimeRealUTC', NET_TIME),    # UTC结束时间(标准UTC时间), 与stuStartTimeRealUTC配对使用;UTC end time (standard UTC time), paired with stuStartTimeRealUTC;
        ('stuPlateImageInfo', NET_PLATE_IMAGE_INFO),  # 车牌图片信息;License plate picture information;
        ('stuCarBodyImageInfo', NET_CARBODY_IMAGE_INFO),  # 车身图片信息;car body picture information;
        ('szPlateCode', c_char * 16),  # 车牌代码; Plate code;
    ]

class NET_IN_FIND_RECORD_PARAM(Structure):
    """
    FindRecord接口输入参数; FindRecord Interface Input Parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; The Structure Size;
        ('emType', C_ENUM),  # 待查询记录类型,参考枚举EM_NET_RECORD_TYPE; The record type to query,Please refer to EM_NET_RECORD_TYPE;
        ('pQueryCondition', c_void_p),  # 查询类型对应的查询条件,由用户申请内存，根据查询记录类型，找到查询条件对应的结构体，进而确定内存大小; Query types corresponding to the query conditions,the space application by the user,according to query condition type,find corresponding structure,then ensure memory size;
    ]

class NET_OUT_FIND_RECORD_PARAM(Structure):
    """
    FindRecord接口输出参数; FindRecord Interface Output Parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; Structure Size;
        ('lFindeHandle', C_LLONG),  # 查询记录句柄,唯一标识某次查询; Query Log Handle,Uniquely identifies a certain query;
    ]

class NET_IN_FIND_NEXT_RECORD_PARAM(Structure):
    """
    FindNextRecord接口输入参数; FindNextRecord Interface Input Parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; Structure Size;
        ('lFindeHandle', C_LLONG),  # 查询句柄; Query Log Handle;
        ('nFileCount', c_int),  # 当前想查询的记录条数; The current number of records need query;
    ]

class NET_OUT_FIND_NEXT_RECORD_PARAM(Structure):
    """
    FindNextRecord接口输出参数; FindNextRecord Interface Output Parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; Structure Size;
        ('pRecordList', c_void_p),  # 记录列表,用户分配内存,根据NET_IN_FIND_RECORD_PARAM中的查询类型EM_NET_RECORD_TYPE，确定对应结构体，进入确定内存大小; Record List, the user allocates memory, ensure structure by query record type(EM_NET_RECORD_TYPE) of NET_IN_FIND_RECORD_PARAM,then ensure memory size;
        ('nMaxRecordNum', c_int),  # 最大查询列表记录数; Max list Record Number;
        ('nRetRecordNum', c_int),  # 查询到的记录条数,当查询到的条数小于想查询的条数时,查询结束; Query to the number of records, when the query to the article number less than want to query the number, end;
    ]

class NET_IN_OPERATE_TRAFFIC_LIST_RECORD(Structure):
    """
    CLIENT_OperateTrafficList 接口入参; CLIENT_OperateTrafficList interface input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('emOperateType', C_ENUM),  # 操作类型,参考枚举EM_RECORD_OPERATE_TYPE; Operate Type,Please refer to EM_RECORD_OPERATE_TYPE;
        ('emRecordType', C_ENUM),  # 要操作的记录信息类型（仅NET_RECORD_TRAFFICREDLIST和NET_RECORD_TRAFFICBLACKLIST有效）,参考枚举EM_NET_RECORD_TYPE; record type to operate (Just NET_RECORD_TRAFFICREDLIST and NET_RECORD_TRAFFICBLACKLIST is valid),Please refer to EM_NET_RECORD_TYPE;
        ('pstOpreateInfo', c_void_p),  # 由用户申请内存，参照操作类型emOperateType，得到操作类型对应的结构体，进而确定对应的内存大小; the space application by the user,please refer to emOperateType to ensure corresponding structure,then ensure memory size;
    ]

class NET_OUT_OPERATE_TRAFFIC_LIST_RECORD(Structure):
    """
    CLIENT_OperateTrafficList 接口出参; CLIENT_OperateTrafficList interface output parameters
    现阶段实现的操作接口中,只有返回nRecordNo的操作,stRetRecord暂时不可用; Among the operation interfaces implemented at this stage, only the operation that returns nRecordNo, stRetRecord is temporarily unavailable
    """
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('nRecordNo', c_int),  # 记录号; Record Number;
    ]

class FIND_RECORD_TRAFFICREDLIST_CONDITION(Structure):
    """
    交通可用名单账户记录查询条件; Traffic Availability List Account Record Query Conditions
    """
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('szPlateNumber', c_char * 32),  # 车牌号; License Plate Number;
        ('szPlateNumberVague', c_char * 32),  # 车牌号码模糊查询; License Plate Number Fuzzy Query;
        ('nQueryResultBegin', c_int),  # 第一个条返回结果在查询结果中的偏移量; Offset in the query results of first results returned;
        ('bRapidQuery', C_BOOL),  # 是否快速查询, TRUE:为快速,快速查询时不等待所有增、删、改操作完成。默认为非快速查询; Whether support the quick query, TRUE: for quick, quick query time don't wait for all add, delete, change operation is completed. The default is non-quick query;
        ('szProvince', c_char * 64),  # 省份类型; Province;
        ('emPlateType', C_ENUM),  # 车牌类型;  License Plate Type    
    ]

class NET_AUTHORITY_TYPE(Structure):
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('emAuthorityType', C_ENUM),  # 权限类型,参考枚举EM_NET_AUTHORITY_TYPE; Permission Types,Please refer to EM_NET_AUTHORITY_TYPE;
        ('bAuthorityEnable', C_BOOL),  # 权限使能; Permission Enabled;
    ]

class NET_TRAFFIC_LIST_RECORD(Structure):
    """
    交通可用名单记录信息; Traffic availability list record information
    """
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('nRecordNo', c_int),  # 之前查询到的记录号; Queried Record Number;
        ('szMasterOfCar', c_char * 16),  # 车主姓名; Car Owner's Name;
        ('szPlateNumber', c_char * 32),  # 车牌号码; License Plate Number;
        ('emPlateType', C_ENUM),  # 车牌类型,参考枚举EM_NET_PLATE_TYPE; License Plate Type,Please refer to EM_NET_PLATE_TYPE;
        ('emPlateColor', C_ENUM),  # 车牌颜色,参考枚举EM_NET_PLATE_COLOR_TYPE; License Plate Color,Please refer to EM_NET_PLATE_COLOR_TYPE;
        ('emVehicleType', C_ENUM),  # 车辆类型,参考枚举EM_NET_VEHICLE_TYPE; Vehicle Type,Please refer to EM_NET_VEHICLE_TYPE;
        ('emVehicleColor', C_ENUM),  # 车身颜色,参考枚举EM_NET_VEHICLE_COLOR_TYPE; Car Body Color,Please refer to EM_NET_VEHICLE_COLOR_TYPE;
        ('stBeginTime', NET_TIME),  # 开始时间; Start Time;
        ('stCancelTime', NET_TIME),  # 撤销时间; Undo Time;
        ('nAuthrityNum', c_int),  # 权限个数; Permission Number;
        ('stAuthrityTypes', NET_AUTHORITY_TYPE * 16),  # 权限列表 , 允许名单仅有; Permissions List, Allow List Only;
        ('emControlType', C_ENUM),  # 布控类型 ,禁止名单仅有,参考枚举EM_NET_TRAFFIC_CAR_CONTROL_TYPE; Monitor Type, Block List Only,Please refer to EM_NET_TRAFFIC_CAR_CONTROL_TYPE;
        ('nControlledRouteID', C_UINT), # 布控路线ID; Controlled Route ID;
        ('nLocation', C_UINT), # 车辆所处位置; Vehicle location;
        ('bLocation', C_BOOL),  #车辆所处位置是否下发，TRUE:下发，FALSE:不下发;Is the nLocation valid? TRUE:YES, FALSE:NO;
        ('szCustomParkNo', c_char * 32),  # 自定义车位号，适用于车检器场景; Customized parking lot number;
        ('szProvince', c_char * 64),  # 省份类型;Province;
        ('szMasterOfCarEx', c_char * 64),  #  车主姓名(拓展);Owner's name (expanded);
        ('bIsMasterOfCarExValid', C_BOOL),  # 是否使用szMasterOfCarEx下发;Whether to use szMasterOfCarEx to deliver data
    ]

class NET_INSERT_RECORD_INFO(Structure):
    """
    增加记录操作
    Increase the record operation
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('pRecordInfo', POINTER(NET_TRAFFIC_LIST_RECORD)),  # 记录内容信息,由用户分配内存，大小为sizeof(NET_TRAFFIC_LIST_RECORD);Record the content information,the space application by the user,apply to sizeof(NET_TRAFFIC_LIST_RECORD);
    ]

class NET_UPDATE_RECORD_INFO(Structure):
    _fields_ = [
        ('dwSize', C_DWORD),
        ('pRecordInfo', POINTER(NET_TRAFFIC_LIST_RECORD)),  # 记录内容信息,由用户分配内存，大小为sizeof(NET_TRAFFIC_LIST_RECORD); Record the content information,the space application by the user,apply to sizeof(NET_TRAFFIC_LIST_RECORD);
    ]

class NET_REMOVE_RECORD_INFO(Structure):
    """
    删除记录操作
    Delete the record operation
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nRecordNo', c_int),  # 之前查询到的记录号;Queried Record Number;
    ]

class CFG_VIDEO_FORMAT(Structure):
    """
    视频格式; Video format
    """
    _fields_ = [
        ('abCompression', c_bool),  
        ('abWidth', c_bool),  
        ('abHeight', c_bool),  
        ('abBitRateControl', c_bool),  
        ('abBitRate', c_bool),  
        ('abFrameRate', c_bool),  
        ('abIFrameInterval', c_bool),  
        ('abImageQuality', c_bool),  
        ('abFrameType', c_bool),  
        ('abProfile', c_bool),  # 信息; Information;
        ('emCompression', C_ENUM),  # 视频压缩格式,参考枚举CFG_VIDEO_COMPRESSION; Video compression mode,Please refer to CFG_VIDEO_COMPRESSION;
        ('nWidth', c_int),  # 视频宽度; Video width;
        ('nHeight', c_int),  # 视频高度; Video height;
        ('emBitRateControl', C_ENUM),  # 码流控制模式,参考枚举CFG_BITRATE_CONTROL; Bit rate control mode,Please refer to CFG_BITRATE_CONTROL;
        ('nBitRate', c_int),  # 视频码流(kbps); Video bit rate (kbps);
        ('nFrameRate', c_float),  # 视频帧率; Frame Rate;
        ('nIFrameInterval', c_int),  # I帧间隔(1-100)，比如50表示每49个B帧或P帧，设置一个I帧。; I frame interval(1-100). For example, 50 means there is I frame in each 49 B frame or P frame.;
        ('emImageQuality', C_ENUM),  # 图像质量,参考枚举CFG_IMAGE_QUALITY; Video quality,Please refer to CFG_IMAGE_QUALITY;
        ('nFrameType', c_int),  # 打包模式，0－DHAV，1－"PS"; Sniffer mode,0-DHAV,1-"PS";
        ('emProfile', C_ENUM),  # H.264编码级别,参考枚举CFG_H264_PROFILE_RANK; H.264 Encode level,Please refer to CFG_H264_PROFILE_RANK;
        ('nMaxBitrate', c_int),  # 最大码流单位是kbps（博世专用）; The maximum stream unit is kbps (Bosch dedicated);
    ]

class CFG_AUDIO_ENCODE_FORMAT(Structure):
    """
    音频格式; audio format
    """
    _fields_ = [
        ('abCompression', c_bool),  
        ('abDepth', c_bool),  
        ('abFrequency', c_bool),  
        ('abMode', c_bool),  
        ('abFrameType', c_bool),  
        ('abPacketPeriod', c_bool),  
        ('abChannels', c_bool),  
        ('abMix', c_bool),  # 信息; Info;
        ('emCompression', C_ENUM),  # 音频压缩模式,参考枚举CFG_AUDIO_FORMAT; Audio compression mode,Please refer to CFG_AUDIO_FORMAT;
        ('nDepth', c_int),  # 音频采样深度; Audio sampling depth;
        ('nFrequency', c_int),  # 音频采样频率; Audio sampling frequency;
        ('nMode', c_int),  # 音频编码模式; Audio encode mode;
        ('nFrameType', c_int),  # 音频打包模式, 0-DHAV, 1-PS; 0-DHAV, 1-PS Audio pack mode;
        ('nPacketPeriod', c_int),  # 音频打包周期, ms; Audio pack period(ms);
        ('nChannelsNum', c_int),  # 视频通道的伴音通道号列表个数; Sound channels list num of video;
        ('arrChannels', C_UINT * 8),  # 视频通道的伴音通道号列表; Sound channels list of video;
        ('bMix', C_BOOL),  # 是否同源; Whether homology;
    ]

class CFG_VIDEOENC_OPT(Structure):
    """
    视频编码参数; Video coding parameters
    """
    _fields_ = [
        ('abVideoEnable', c_bool),  
        ('abAudioEnable', c_bool),  
        ('abSnapEnable', c_bool),  
        ('abAudioAdd', c_bool),  # 音频叠加能力; Audio overlay capacity;
        ('abAudioFormat', c_bool),  # 信息; Information;
        ('bVideoEnable', C_BOOL),  # 视频使能; Video enable;
        ('stuVideoFormat', CFG_VIDEO_FORMAT),  # 视频格式; Video format;
        ('bAudioEnable', C_BOOL),  # 音频使能; Audio enable;
        ('bSnapEnable', C_BOOL),  # 定时抓图使能; Schedule snapshot enable;
        ('bAudioAddEnable', C_BOOL),  # 音频叠加使能; Audio add enable;
        ('stuAudioFormat', CFG_AUDIO_ENCODE_FORMAT),  # 音频格式; Audio format;
    ]

class CFG_RGBA(Structure):
    """
    RGBA信息; RGBA message
    """
    _fields_ = [
        ('nRed', c_int),  
        ('nGreen', c_int),  
        ('nBlue', c_int),  
        ('nAlpha', c_int),  
    ]

class CFG_COVER_INFO(Structure):
    """
    遮挡信息; Occlusion information
    """
    _fields_ = [
        ('abBlockType', c_bool),  
        ('abEncodeBlend', c_bool),  
        ('abPreviewBlend', c_bool),  # 信息; Information;
        ('stuRect', CFG_RECT),  # 覆盖的区域坐标; The position (coordinates) of the mask zone;
        ('stuColor', CFG_RGBA),  # 覆盖的颜色; The mask color;
        ('nBlockType', c_int),  # 覆盖方式；0－黑块，1－马赛克; The mask mode ;0-black block,1-Mosaic;
        ('nEncodeBlend', c_int),  # 编码级遮挡；1－生效，0－不生效; Encode-level privacy mask;1-enable,0-unable;
        ('nPreviewBlend', c_int),  # 预览遮挡；1－生效，0－不生效; Preview mask;1-enable,0-unable;
    ]

class CFG_VIDEO_COVER(Structure):
    """
    多区域遮挡配置; Multi area occlusion configuration
    """
    _fields_ = [
        ('nTotalBlocks', c_int),  # 支持的遮挡块数; The supported privacy mask zone amount;
        ('nCurBlocks', c_int),  # 已设置的块数; The zone amount already set;
        ('stuCoverBlock', CFG_COVER_INFO * 16),  # 覆盖的区域; The mask zone;
    ]

class CFG_OSD_INFO(Structure):
    """
    OSD信息; OSD message
    """
    _fields_ = [
        ('abShowEnable', c_bool),  # 信息; Information;
        ('stuFrontColor', CFG_RGBA),  # 前景颜色; Front color;
        ('stuBackColor', CFG_RGBA),  # 背景颜色; Background color;
        ('stuRect', CFG_RECT),  # 矩形区域; Rectangle zone;
        ('bShowEnable', C_BOOL),  # 显示使能; Display enbale;
    ]

class CFG_COLOR_INFO(Structure):
    """
    画面颜色属性; Picture color attribute
    """
    _fields_ = [
        ('nBrightness', c_int),  # 亮度(0-100); Brgihtness(0-100);
        ('nContrast', c_int),  # 对比度(0-100); Contrast(0-100);
        ('nSaturation', c_int),  # 饱和度(0-100); Saturation (0-100);
        ('nHue', c_int),  # 色度(0-100); Hue (0-100);
        ('nGain', c_int),  # 增益(0-100); Gain(0-100);
        ('bGainEn', C_BOOL),  # 增益使能; Gain enable;
    ]

class CFG_ENCODE_INFO(Structure):
    """
    图像通道属性信息; Image channel attribute information
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号(0开始),获取时，该字段有效；设置时，该字段无效; Channel number(Begins with 0);
        ('szChnName', c_char * 64),  # 无效字段; Channel name;
        ('stuMainStream', CFG_VIDEOENC_OPT * 4),  # 主码流，0－普通录像，1-动检录像，2－报警录像; Main stream,0-General record,1-Motion detect,2-alarm record;
        ('nValidCountMainStream', c_int),  # 主码流数组中有效的个数; The valid count of MainStream array;
        ('stuExtraStream', CFG_VIDEOENC_OPT * 4),  # 辅码流，0－辅码流1，1－辅码流2，2－辅码流3; Extra stream,0-Extra stream 1,1-Extra stream 2,2-Extra stream 3;
        ('nValidCountExtraStream', c_int),  # 辅码流数组中有效的个数; The valid count of ExtraStream array;
        ('stuSnapFormat', CFG_VIDEOENC_OPT * 4),  # 抓图，0－普通抓图，1－动检抓图，2－报警抓图; Snapshot,0-General snapshot,1-Motion detect snapshot,2-alarm snapshot;
        ('nValidCountSnapFormat', c_int),  # 抓图数组中有效的个数; The valid count of SnapFormat array;
        ('dwCoverAbilityMask', C_DWORD),  # 无效字段; The subnet mask of the privacy mask competence. Use the bit to represent. There are local preview, record and network monitor.;
        ('dwCoverEnableMask', C_DWORD),  # 无效字段; The subnet mask of the privacy mask enable.Use the bit to represent. There are local preview, record and network monitor.;
        ('stuVideoCover', CFG_VIDEO_COVER),  # 无效字段; Privacy mask;
        ('stuChnTitle', CFG_OSD_INFO),  # 无效字段; Channel title;
        ('stuTimeTitle', CFG_OSD_INFO),  # 无效字段; Time title;
        ('stuVideoColor', CFG_COLOR_INFO),  # 无效字段; Video color;
        ('emAudioFormat', C_ENUM),          # 无效字段; Audio Format
        ('nProtocolVer', c_int),  # 协议版本号, 只读,获取时，该字段有效；设置时，该字段无效; Protocol Version No., read only;
    ]

class NET_HDDSMART_INFO(Structure):
    """
    硬盘Smart信息; Hard disk smart information
    """
    _fields_ = [
        ('nID', c_int),  # 属性ID; ID;
        ('nCurrent', c_int),  # 属性值; Current;
        ('szName', c_char * 64),  # 属性名; Name;
        ('nWorst', c_int),  # 最大出错值; Worst;
        ('nThreshold', c_int),  # 阈值; Threshold;
        ('szRaw', c_char * 32),  # 实际值,可能不仅是数字，需要字符串返回; Actual Value;
        ('nPredict', c_int),  # 状态,对硬盘状态的预测值,无实际意义; The predictive value of the state of HDD;
        ('emSync', C_ENUM),  # Raid同步状态,参考枚举EM_RAID_SYNC_STATE; Raid Sync State,Please refer to EM_RAID_SYNC_STATE;
        ('byReserved', C_BYTE * 512),  # 保留字节; Reserved Byte;
    ]

class ALARM_HDD_HEALTHALARM_INFO(Structure):
    """
    硬盘健康状况报警事件( DH_ALARM_HDD_HEALTHALARM ); Hard disk health alarm event (dh_alarm_hdd_healthalarm)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作1:Start 2:Stop; Action:1:Start 2:Stop;
        ('stuTime', NET_TIME_EX),  # 事件发生的时间; Event occurrence time;
        ('szHDDName', c_char * 64),  # 硬盘名称; HDD Name;
        ('stuHDDSmartInfo', NET_HDDSMART_INFO),  # 硬盘Smart信息; HDD Smart info;
        ('byReserved', C_BYTE * 512),  # 保留字节; Reserved Byte;
    ]

class ALARM_DISK_CHECK_INFO(Structure):
    """
    磁盘巡检报警事件信息(对应 DH_ALARM_DISK_CHECK); Disk patrol alarm event information (corresponding to dh_alarm_disk_check)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作,1表示持续性事件开始,2表示持续性事件结束;; Event operation.1=continues event begin. 2=continuous event stop;
        ('UTC', NET_TIME_EX),  # 事件发生的时间; Event occurrence time;
        ('szName', c_char * 128),  # 报警名称; Name;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('byReserved', C_BYTE * 1024),  # 保留字节; Reserved;
    ]

class ALARM_HDD_SHAKEALARM_INFO(Structure):
    """
    硬盘震动报警事件( DH_ALARM_HDD_SHAKEALARM ); Hard disk vibration alarm event (dh_alarm_hdd_shakealarm)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作1:Start 2:Stop; Action:1:Start 2:Stop;
        ('stuTime', NET_TIME_EX),  # 事件发生的时间; Event occurrence time;
        ('szHDDName', c_char * 64),  # 硬盘名称; HDD Name;
        ('stuHDDSmartInfo', NET_HDDSMART_INFO),  # 硬盘Smart信息; HDD Smart info;
        ('byReserved', C_BYTE * 512),  # 保留字节; Reserved Byte;
    ]

class ALARM_HDD_TEMPERATUREALARM_INFO(Structure):
    """
    硬盘温度报警事件( DH_ALARM_HDD_TEMPERATUREALARM ); Hard disk temperature alarm event (dh_alarm_hdd_temperaturealarm)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作1:Start 2:Stop; Action:1:Start 2:Stop;
        ('nTemperature', c_int),  # 硬盘当前温度值; HDD Temperature;
        ('stuTime', NET_TIME_EX),  # 事件发生的时间; Event occurrence time;
        ('szHDDName', c_char * 64),  # 硬盘名称; HDD Name;
        ('stuHDDSmartInfo', NET_HDDSMART_INFO),  # 硬盘Smart信息; HDD Smart info;
        ('byReserved', C_BYTE * 512),  # 保留字节; Reserved Byte;
    ]

class NET_RECORD_CARD_INFO(Structure):
    """
    卡号录像信息; Card number video information
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nType', c_int),  # 类型, 0-Card, 1-Field; type, 0-Card, 1-Field;
        ('szCardNo', c_char * 256),  # 卡号; card no.;
        ('emTradeType', C_ENUM),  # 交易类型,参考枚举EM_ATM_TRADE_TYPE; transaction type,Please refer to EM_ATM_TRADE_TYPE;
        ('szAmount', c_char * 64),  # 交易金额, 空字符串表示不限金额; transaction amount, nullstring means no limit amount;
        ('nError', c_int),  # 错误码, 0-所有错误, 1-吞钞, 2-吞卡; error code, 0-all errors, 1-retain cash, 2-retain card;
        ('nFieldCount', c_int),  # 域数量, 按域查询时有效; domain quantity, by domain search is valid;
        ('szFields', c_char * 4096),  # 域信息, 按域查询时有效; domain info, by domain search is valid;
        ('szChange', c_char * 32),  # 零钱; change;
    ]

class NET_IN_MEDIA_QUERY_FILE(Structure):
    """
    录像信息对应 CLIENT_FindFileEx 接口的 DH_FILE_QUERY_FILE / DH_FILE_QUERY_FILE_EX 命令 查询条件, 目前支持通过路径查询
    Video information corresponding to client_ DH of findfileex interface_ FILE_ QUERY_ FILE / DH_ FILE_ QUERY_ FILE_ Ex command query criteria. Currently, path query is supported
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; size;
        ('szDirs', c_void_p),  # 工作目录列表,一次可查询多个目录,为空表示查询所有目录。目录之间以分号分隔,如“/mnt/dvr/sda0;/mnt/dvr/sda1”,szDirs==null 或"" 表示查询所有; working directory list,can inquire multiple directory at a atime,separated by ";",example "/mnt/dvr/sda0;/mnt/dvr/sda1",if szDirs==null or szDirs == "" ,means search all;
        ('nMediaType', c_int),  # 文件类型,0:查询任意类型,1:查询jpg图片,2:查询dav; file info,0:any type,1:search jpg image,2:search dav;
        ('nChannelID', c_int),  # 通道号从0开始,-1表示查询所有通道; Channel start from 0, -1 means search all channel;
        ('stuStartTime', NET_TIME),  # 开始时间; start time;
        ('stuEndTime', NET_TIME),  # 结束时间; end time;
        ('nEventLists', c_int * 256),  # 事件类型列表,参见智能分析事件类型; Event type list, see intelligent analysis event type;
        ('nEventCount', c_int),  # 事件总数; event total;
        ('byVideoStream', C_BYTE),  # 视频码流 0-未知 1-主码流 2-辅码流1 3-辅码流2 4-辅码流3 5-所有的辅码流类型; video stream 0-unknown; 1-main; 2-sub 1; 3-sub 2; 4- sub 3; 5-ExtraX;
        ('bReserved', C_BYTE * 3),  # 字节对齐; aligh text;
        ('emFalgLists', C_ENUM * 128),  # 录像或抓图文件标志, 不设置标志表示查询所有文件,参考枚举EM_RECORD_SNAP_FLAG_TYPE; Record or snapshot file mark, not set mark to search all files,Please refer to EM_RECORD_SNAP_FLAG_TYPE;
        ('nFalgCount', c_int),  # 标志总数; total mark;
        ('stuCardInfo', NET_RECORD_CARD_INFO),  # 卡号录像信息, emFalgLists包含卡号录像时有效; card no. record info, emFalgLists including card no. video is valid;
        ('nUserCount', c_int),  # 用户名有效个数; user total;
        ('szUserName', c_char * 512),  # 用户名; user name;
        ('emResultOrder', C_ENUM),  # 查询结果排序方式,参考枚举EM_RESULT_ORDER_TYPE; result order,Please refer to EM_RESULT_ORDER_TYPE;
        ('bTime', C_BOOL),  # 是否按时间查询; find file by time;
        ('emCombination', C_ENUM),  # 查询结果是否合并录像文件,参考枚举NET_EM_COMBINATION_MODE; Whether to combine video,Please refer to NET_EM_COMBINATION_MODE;
        ('stuEventInfo', EVENT_INFO * 16),  # 事件信息，当查询为 DH_FILE_QUERY_FILE_EX 类型时有效; event info,when query type in EM_FILE_QUERY_TYPE is DH_FILE_QUERY_FILE_EX valid;
        ('nEventInfoCount', c_int),  # stuEventInfo 个数; stuEventInfo's count;
        ('bOnlySupportRealUTC', C_BOOL),    # 为TRUE表示仅下发stuStartTimeRealUTC和stuEndTimeRealUTC(不下发stuStartTime, stuEndTime), 为FALSE表示仅下发stuStartTime, stuEndTime(不下发stuStartTimeRealUTC和stuEndTimeRealUTC);TRUE means only deliver stuStartTimeRealUTC and stuEndTimeRealUTC (do not deliver stuStartTime, stuEndTime), FALSE means deliver only stuStartTime, stuEndTime (do not deliver stuStartTimeRealUTC and stuEndTimeRealUTC);
        ('stuStartTimeRealUTC', NET_TIME),  # UTC开始时间(标准UTC时间), 与stuEndTimeRealUTC配对使用，与(stuStartTime, stuEndTime)互斥;UTC start time (standard UTC time), paired with stuEndTimeRealUTC, mutually exclusive with (stuStartTime, stuEndTime);
        ('stuEndTimeRealUTC', NET_TIME),    # UTC结束时间(标准UTC时间), 与stuStartTimeRealUTC配对使用，与(stuStartTime, stuEndTime)互斥;UTC end time (standard UTC time), paired with stuStartTimeRealUTC, mutually exclusive with (stuStartTime, stuEndTime);
    ]

class NET_FILE_SUMMARY_INFO(Structure):
    """
    文件摘要信息; Document summary information
    """
    _fields_ = [
        ('szKey', c_char * 64),  # 摘要名称; Abstract name;
        ('szValue', c_char * 512),  # 摘要内容; Abstract contents;
        ('bReserved', C_BYTE * 256),  # 保留字段; Reserved string;
    ]

class NET_OUT_MEDIA_QUERY_FILE(Structure):
    """
    录像信息对应 CLIENT_FindFileEx 接口的 DH_FILE_QUERY_FILE / DH_FILE_QUERY_FILE_EX 命令 查询结果
    Video information corresponding to client_ DH of findfileex interface_ FILE_ QUERY_ FILE / DH_ FILE_ QUERY_ FILE_ Ex command query results
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小; size;
        ('nChannelID', c_int),  # 通道号从0开始,-1表示查询所有通道; channel ID,from 0,-1 means search all;
        ('stuStartTime', NET_TIME),  # 开始时间; start time;
        ('stuEndTime', NET_TIME),  # 结束时间; end time;
        ('nFileSize', C_UINT),  # 文件长度,该字段废弃,使用nFileSizeEx字段; size of file,This field is discarded,please use the nFileSizeEx;
        ('byFileType', C_BYTE),  # 文件类型 1:jpg图片, 2: dav; file type 1:jpg, 2: dav;
        ('byDriveNo', C_BYTE),  # 该字段已废弃,后续开发使用 nDriveNo成员; deprecated, to get same info, use nDriveNo instead;
        ('byPartition', C_BYTE),  # 分区号; zone no.;
        ('byVideoStream', C_BYTE),  # 视频码流 0-未知 1-主码流 2-辅码流1 3-辅码流 4-辅码流; video stream 0-unknown 1-main 2-sub 1 3-sub 4-sub;
        ('nCluster', C_UINT),  # 簇号; cluster;
        ('szFilePath', c_char * 260),  # 文件路径; FilePath;
        ('nEventLists', c_int * 256),  # 关联的事件列表,事件类型列表,参见智能分析事件类型; Link event list,see event intelligent analysis event type;
        ('nEventCount', c_int),  # 事件总数; event total;
        ('emFalgLists', C_ENUM * 128),  # 录像或抓图文件标志,参考枚举EM_RECORD_SNAP_FLAG_TYPE; record or snapshot file mark,Please refer to EM_RECORD_SNAP_FLAG_TYPE;
        ('nFalgCount', c_int),  # 标志总数; mark total;
        ('nDriveNo', C_UINT),  # 磁盘号,频浓缩文件相关信息; disk driver number;
        ('szSynopsisPicPath', c_char * 512),  # 预处理文件提取到的快照 文件路径,支持HTTP URL表示:"http:www.test.com/1.jpg",支持FTP URL表示: "ftp:ftp.test.com/1.jpg",支持服务器本地路径,a)"C:/pic/1.jpg",b)"/mnt2010/8/11/dav/15:40:50.jpg"; snap file path when pre-process the file;
        ('nSynopsisMaxTime', c_int),  # 支持浓缩视频最大时间长度,单位 秒; video synopsis max time. Unit is second.;
        ('nSynopsisMinTime', c_int),  # 支持浓缩视频最小时间长度,单位 秒,文件摘要信息; video synopsis min time. Unit is second.;
        ('nFileSummaryNum', c_int),  # 文件摘要信息数; file summary number;
        ('stFileSummaryInfo', NET_FILE_SUMMARY_INFO * 32),  # 文件摘要信息; file summary info;
        ('nFileSizeEx', c_int64),  # 文件长度扩展,支持文件长度大于4G，单位字节; size of file extension, Support file length is greater than 4G,unit:Byte;
        ('nTotalFrame', C_UINT),  # 查询录像段内所有帧总和，不区分帧类型; all frames' num, not distinguish by frame type;
        ('emFileState', C_ENUM),  # 录像文件的状态,参考枚举EM_VIDEO_FILE_STATE; video file status,Please refer to EM_VIDEO_FILE_STATE;
        ('szWorkDir', c_char * 256),  # 录像文件的存储目录; Storage directory of video files;
        ('szThumbnail', c_char * 260),  # 缩略图路径，可根据该路径下载缩略图; Thumbnail path, according to which thumbnails can be downloaded;
        ('bRealUTC', C_BOOL),   # 为TRUE表示仅stuStartTimeRealUTC和stuEndTimeRealUTC有效(仅使用stuStartTimeRealUTC和stuEndTimeRealUTC), 为FALSE表示仅stuStartTime和stuEndTime有效(仅使用stuStartTime和stuEndTime);TRUE means only stuStartTimeRealUTC and stuEndTimeRealUTC are valid (only stuStartTimeRealUTC and stuEndTimeRealUTC are used), FALSE means only stuStartTime and stuEndTime are valid (only stuStartTime and stuEndTime are used);
        ('stuStartTimeRealUTC', NET_TIME),  # UTC开始时间(标准UTC时间), 与stuEndTimeRealUTC配对使用;UTC start time (standard UTC time), paired with stuEndTimeRealUTC;
        ('stuEndTimeRealUTC', NET_TIME),    # UTC结束时间(标准UTC时间), 与stuStartTimeRealUTC配对使用;UTC end time (standard UTC time), paired with stuStartTimeRealUTC;
    ]

class CFG_NETWORK_INTERFACE(Structure):
    """
    网口配置; Network port configuration
    """
    _fields_ = [
        ('szName', c_char * 128),  # 网络接口名称; Network address name;
        ('szIP', c_char * 256),  # ip地址; IP address;
        ('szSubnetMask', c_char * 256),  # 子网掩码; Subnet mask;
        ('szDefGateway', c_char * 256),  # 默认网关; Default gateway;
        ('bDhcpEnable', C_BOOL),  # 是否开启DHCP; Enable DHCP or not.;
        ('bDnsAutoGet', C_BOOL),  # DNS获取方式，dhcp使能时可以设置为true，支持通过dhcp获取; DNS get way.,It is true if the dhcp is enabled. Support DHCP.;
        ('szDnsServers', c_char * 512),  # DNS服务器地址; DNS address;
        ('nMTU', c_int),  # 网络最大传输单元; Network max transmission unit.;
        ('szMacAddress', c_char * 256),  # mac地址; Mac address;
        ('bInterfaceEnable', C_BOOL),  # 网络接口使能开关，表示该网口配置是否生效。不生效时，IP地址不设置到网卡上。; Enable network interface,if false,ip address will not set for the config;
        ('bReservedIPEnable', C_BOOL),  # DHCP失败时是否使用保留IP，使用保留IP时还继续发DHCP请求; Enable to reserved ip when DHCP failed,true:continue to send DHCP ask;
        ('emNetTranmissionMode', C_ENUM),  # 网络传输模式，默认adapt自适应模式,参考枚举CFG_ENUM_NET_TRANSMISSION_MODE; Net transmission mode，default:adapt,Please refer to CFG_ENUM_NET_TRANSMISSION_MODE;
        ('emInterfaceType', C_ENUM),  # 网口类型,参考枚举CFG_ENUM_NET_INTERFACE_TYPE; Network interface type,Please refer to CFG_ENUM_NET_INTERFACE_TYPE;
        ('bBond', C_ENUM),  # 是否绑定虚拟网口,参考枚举CFG_THREE_STATUS_BOOL; enable to bond Network interface,Please refer to CFG_THREE_STATUS_BOOL;
    ]

class CFG_NETWORK_BOND_INTERFACE(Structure):
    """
    绑定虚拟网口; Bind virtual network port
    """
    _fields_ = [
        ('bBonding', C_BOOL),  # 是否绑定虚拟网口，只有网卡名是bondxx时，才允许有Bonding字段，其它网卡不能用,true-绑定网卡生效,物理网口对外不可用,false-解绑网卡(多址模式),使Members中的网卡可用; Whether to bind the virtual network port, the bonding field is allowed only when the network card name is bondxx, and other network cards cannot be used,true-the binding of the network card takes effect, and the physical network port is unavailable to the outside world,false-Unbind the network card (multi-access mode) to make the network card in Members available;
        ('emMode', C_ENUM),  # 网卡绑定模式,参考枚举CFG_ENUM_NET_BOND_MODE; NIC bonding mode,Please refer to CFG_ENUM_NET_BOND_MODE;
        ('emLacp', C_ENUM),  # 802.3ad链路聚合控制方式,参考枚举CFG_ENUM_NET_BOND_LACP; 802.3ad link aggregation control method,Please refer to CFG_ENUM_NET_BOND_LACP;
        ('nMTU', c_int),  # 网络最大传输单元; Network maximum transmission unit;
        ('szMembers', c_char * 256),  # 物理网口成员; Physical network port member;
        ('szIP', c_char * 256),  # ip地址; IP;
        ('szName', c_char * 128),  # 网络接口名称; Name;
        ('szAlias', c_char * 128),  # 网络接口名称; Alias;
        ('szDnsServers', c_char * 512),  # DNS服务器地址; DNS Servers;
        ('szMacAddress', c_char * 256),  # mac地址; mac Address;
        ('szSubnetMask', c_char * 256),  # 子网掩码; Subnet mask;
        ('szDefGateway', c_char * 256),  # 默认网关; Default gateway;
        ('bDhcpEnable', C_BOOL),  # 是否开启DHCP; Whether to enable DHCP;
    ]

class CFG_NETWORK_BR_INTERFACE(Structure):
    """
    网桥; bridge
    """
    _fields_ = [
        ('szName', c_char * 128),  # 网络接口名称; Network interface name;
        ('bEnable', C_BOOL),  # 使能; enable;
        ('nMTU', c_int),  # 网络最大传输单元; MTU;
        ('szMembers', c_char * 256),  # 物理网口成员; Physical network port member;
        ('szIP', c_char * 256),  # ip地址; IP;
        ('szSubnetMask', c_char * 256),  # 子网掩码; Subnet mask;
        ('szDefGateway', c_char * 256),  # 默认网关; Default gateway;
        ('szDnsServers', c_char * 512),  # DNS服务器地址; DNS Servers;
        ('bDhcpEnable', C_BOOL),  # 是否开启DHCP; Whether to enable DHCP;
        ('bReservedIPEnable', C_BOOL),  # DHCP失败时是否使用保留IP，使用保留IP时还继续发DHCP请求; Whether to use reserved IP when DHCP fails, and continue to send DHCP requests when reserved IP is used;
        ('bDnsAutoGet', C_BOOL),  # DNS获取方式，dhcp使能时可以设置为true，支持通过dhcp获取; DNS acquisition method, can be set to true when dhcp is enabled, and it can be acquired through dhcp;
    ]

class CFG_NETWORK_INFO(Structure):
    """
    网络接口配置; Network interface configuration
    """
    _fields_ = [
        ('szHostName', c_char * 128),  # 主机名称; Host name;
        ('szDomain', c_char * 128),  # 所属域; Belonging domain;
        ('szDefInterface', c_char * 128),  # 默认使用的网卡; Default network card;
        ('nInterfaceNum', c_int),  # 网卡数量; Network card amount;
        ('stuInterfaces', CFG_NETWORK_INTERFACE * 32),  # 网卡列表; Network card list;
        ('nBondInterfaceNum', c_int),  # 虚拟绑定网口数量; Number of virtual binding network ports;
        ('stuBondInterfaces', CFG_NETWORK_BOND_INTERFACE * 32),  # 虚拟绑定网口列表; Virtual bonding network port list;
        ('nBrInterfaceNum', c_int),  # 网桥数量; Number of bridges;
        ('stuBrInterfaces', CFG_NETWORK_BR_INTERFACE * 32),  # 网桥列表; List of bridges;
    ]

class NET_UTCTIME(Structure):
    _fields_ = [
        ('utc', C_UINT),  # utc时间; utc;
        ('tolerance', C_UINT),  # 容差，表示容许设置时间和当前差多少秒内不做修改 (下发时用到); tolerance, allows the setting time to be seconds away from the current time without modification; set:valid;
        ('reserved', c_char * 8),  # 预留字段; reserved data;
    ]

class NET_OPEN_INTELLI_OBJECT_ATTRIBUTE_INFO(Structure):
    """
    目标属性数组; Target attribute array
    """
    _fields_ = [
        ('szAttrTypeName', c_char * 128),  # 属性类型名称; attribute type name;
        ('szAttrValueName', c_char * 128),  # 属性值名称; attribute value name;
    ]

class NET_OPEN_INTELLI_OBJECT_INFO(Structure):
    """
    检测到的目标属性信息列表; List of detected target attribute information
    """
    _fields_ = [
        ('nObjectId', c_int),  # 目标id; target id;
        ('stuBoundingBox', NET_RECT),  # 包围盒 矩形类型,8192坐标系; Bounding box rectangle type, 8192 coordinate system;
        ('szObjectTypeName', c_char * 128),  # 目标类型名称; target type name;
        ('nObjectAttributeNums', c_int),  # 目标属性数组中的有效个数; valid number in the target attribute array;
        ('stuObjectAttributes', NET_OPEN_INTELLI_OBJECT_ATTRIBUTE_INFO * 128),  # 目标属性数组; Array of target attributes;
    ]

class NET_OPEN_INTELLI_USER_DATA_INFO(Structure):
    """
    用户数据; user data
    """
    _fields_ = [
        ('nAlarmId', c_int),  # 自定义报警id; custom alarm id;
        ('szReserved', c_char * 512),  # 保留字节; reserved bytes;
    ]

class DEV_EVENT_OPEN_INTELLI_INFO(Structure):
    """
    事件类型 EVENT_IVS_OPEN_INTELLI (开放智能事件)对应的数据块描述信息;
    Event type event_ IVS_ OPEN_ Data block description information corresponding to Intelli (open intelligent event)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号; channel number;
        ('nAction', c_int),  # 0:脉冲,1:开始, 2:停止; 0: pulse, 1: start, 2: stop;
        ('szOpenCode', c_char * 32),  # 所属开放算法的Id; Id of the open algorithm it belongs to;
        ('szOpenName', c_char * 128),  # 所属开放算法的名称; The name of the open algorithm to which it belongs;
        ('szRuleType', c_char * 32),  # 所属开放算法的规则类型, 仅支持: 拌线入侵CrossLineDetection(EVENT_IVS_CROSSLINEDETECTION)、区域入侵CrossRegionDetection(EVENT_IVS_CROSSREGIONDETECTION)、滞留检测StayDetection(EVENT_IVS_STAYDETECTION)、数量统计ObjectNumDetection(EVENT_IVS_OBJECT_NUM_DETECTION); Rule type of the open algorithm, only supported: CrossLineDetection(EVENT_IVS_CROSSLINEDETECTION)、CrossRegionDetection(EVENT_IVS_CROSSREGIONDETECTION)、StayDetection(EVENT_IVS_STAYDETECTION)、ObjectNumDetection(EVENT_IVS_OBJECT_NUM_DETECTION);
        ('pstuOpenData', c_void_p),  # 与开放算法的规则类型支持的带图事件类型对应的结构体对应(只解析Event Data中的字段),拌线入侵CrossLineDetection(EVENT_IVS_CROSSLINEDETECTION) - DEV_EVENT_CROSSLINE_INFO,区域入侵CrossRegionDetection(EVENT_IVS_CROSSREGIONDETECTION) - DEV_EVENT_CROSSREGION_INFO,滞留检测StayDetection(EVENT_IVS_STAYDETECTION) - DEV_EVENT_STAY_INFO,数量统计ObjectNumDetection(EVENT_IVS_OBJECT_NUM_DETECTION) - DEV_EVENT_OBJECT_NUM_DETECTION_INFO; Corresponds to the structure corresponding to the event type with graph supported by the rule type of the open algorithm (only parses the fields in Event Data),CrossLineDetection(EVENT_IVS_CROSSLINEDETECTION) - DEV_EVENT_CROSSLINE_INFO,CrossRegionDetection(EVENT_IVS_CROSSREGIONDETECTION) - DEV_EVENT_CROSSREGION_INFO,StayDetection(EVENT_IVS_STAYDETECTION) - DEV_EVENT_STAY_INFO,ObjectNumDetection(EVENT_IVS_OBJECT_NUM_DETECTION) - DEV_EVENT_OBJECT_NUM_DETECTION_INFO;
        ('nObjectNums', c_int),  # 检测到的目标属性信息列表的个数; number of detected target attribute information lists;
        ('stuObjects', NET_OPEN_INTELLI_OBJECT_INFO * 100),  # 检测到的目标属性信息列表; List of detected object attribute information;
        ('stuUserData', NET_OPEN_INTELLI_USER_DATA_INFO),  # 用户数据; User data;
        ('szReserved', c_char * 1024),  # 保留字节; reserved bytes;
    ]

class NET_FIND_RECORD_ACCESSCTLCARDREC_ORDER(Structure):
    """
    门禁出入记录排序规则详情
    Order rule of entrance guard access records
    """
    _fields_ = [
        ('emField', C_ENUM),  # 排序字段 Refer: EM_RECORD_ACCESSCTLCARDREC_ORDER_FIELD;field Refer: EM_RECORD_ACCESSCTLCARDREC_ORDER_FIELD;
        ('emOrderType', C_ENUM),  # 排序类型 Refer: EM_RECORD_ORDER_TYPE;order type Refer: EM_RECORD_ORDER_TYPE;
        ('byReverse', c_char * 64),  # 保留字节;Reserved;
    ]

class NET_FIND_RECORD_ACCESSCTLCARDREC_CONDITION_EX(Structure):
    """
    门禁出入记录查询条件
    A&C extry/exit search criteria
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('bCardNoEnable', C_BOOL),  # 启用卡号查询;Enable card search;
        ('szCardNo', c_char * 32),  # 卡号;Card No.;
        ('bTimeEnable', C_BOOL),  # 启用时间段查询;Enable search by period;
        ('stStartTime', NET_TIME),  # 起始时间;Start time;
        ('stEndTime', NET_TIME),  # 结束时间;End time;
        ('nOrderNum', c_int),  # 规则数;The number of rules;
        ('stuOrders', NET_FIND_RECORD_ACCESSCTLCARDREC_ORDER * 6),  # 规则数组;The array of rules;
        ('bRealUTCTimeEnable', C_BOOL),  # 启动RealUTC时间查询, bRealUTCTimeEnable为TRUE时bTimeEnable无效;Start RealUTC time query
        ('nStartRealUTCTime', C_UINT),  # 真实UTC时间戳，起始时间;Real UTC timestamp, start time
        ('nEndRealUTCTime', C_UINT),  # 真实UTC时间戳，结束时间;Real UTC timestamp, end time
        ('szReserved', c_char * 40),  # 字节对齐;Reserved
    ]

class NET_CTRL_RECORDSET_PARAM(Structure):
    """
    记录集操作参数
    Query device recording information
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('emType', C_ENUM),  # 记录集信息类型 Refer: EM_NET_RECORD_TYPE;Record Information Type Refer: EM_NET_RECORD_TYPE;
        ('pBuf', c_void_p),  # 新增\更新\查询\导入时,为记录集信息缓存,详见 EM_NET_RECORD_TYPE 注释,由用户申请内存，长度为nBufLen删除时,为存放记录集编号的内存地址(类型为int*), 批量删除时，为NET_CTRL_RECORDSET_REMOVEEX_PARAM, 由用户申请内存, 长度为nBufLen;New/Renew/Inquire,It is Record Information Cache, the EM_NET_RECORD_TYPE Note is Details)Delete,It is memory address for storage Record Number(type is int*);
        ('nBufLen', c_int),  # 记录集信息缓存大小,大小参照记录集信息类型对应的结构体;Record Information Cache Size,please refer to the structure of EM_NET_RECORD_TYPE;
    ]

class NET_IN_DOWNLOAD_REMOTE_FILE(Structure):
    """
    CLIENT_DownloadRemoteFile 接口输入参数(文件下载)
    CLIENT_DownloadRemoteFile    Interface Input Parameters (the file download)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('pszFileName', POINTER(c_char)),  # 需要下载的文件名;File Name Needs to Download;
        ('pszFileDst', POINTER(c_char)),  # 存放文件路径;File Path;
    ]

class NET_OUT_DOWNLOAD_REMOTE_FILE(Structure):
    """
    CLIENT_DownloadRemoteFile 接口输出参数(文件下载)
    CLIENT_DownloadRemoteFile Interface Output Parameters (the file download)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('dwMaxFileBufLen', C_DWORD),  # 文件缓存区pstFileBuf的大小, 由用户指定;The size of pstFileBuf, it is specified by user;
        ('pstFileBuf', POINTER(c_char)),  # 文件缓存区, 由用户申请和释放;File buf, application an release by user;
        ('dwRetFileBufLen', C_DWORD),  # 缓存区中返回的实际文件数据大小;The actual size of the file;
        ('byReserved', C_BYTE * 4),  # 字节对齐;Alignment;
    ]

class NET_RECORDSET_ACCESS_CTL_CARDREC(Structure):
    """
    门禁刷卡记录记录集信息
    Access control card swiping record set information
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nRecNo', c_int),  # 记录集编号,只读;Record Number,Read-Only;
        ('szCardNo', c_char * 32),  # 卡号;Card Number;
        ('szPwd', c_char * 64),  # 密码;Password;
        ('stuTime', NET_TIME),  # 刷卡时间;Swing Card Time;
        ('bStatus', C_BOOL),  # 刷卡结果,TRUE表示成功,FALSE表示失败;Swing Card Result,True is Success,False is Fail;
        ('emMethod', C_ENUM),  # 开门方式 Refer: NET_ACCESS_DOOROPEN_METHOD;Open Door Method Refer: NET_ACCESS_DOOROPEN_METHOD;
        ('nDoor', c_int),  # 门号,即CFG_CMD_ACCESS_EVENT配置CFG_ACCESS_EVENT_INFO的数组下标;Door Number,That is CFG_CMD_ACCESS_EVENT Configure Array Subscript;
        ('szUserID', c_char * 32),  # 用户ID;user ID;
        ('nReaderID', c_int),  # 读卡器ID (废弃,不再使用);card reader ID (abandoned);
        ('szSnapFtpUrl', c_char * 260),  # 开锁抓拍上传的FTP地址;unlock snap upload ftp url;
        ('szReaderID', c_char * 32),  # 读卡器ID              开门并上传抓拍照片,在记录集记录存储地址,成功才有;card reader ID;
        ('emCardType', C_ENUM),  # 卡类型 Refer: NET_ACCESSCTLCARD_TYPE;Card Type Refer: NET_ACCESSCTLCARD_TYPE;
        ('nErrorCode', c_int),  # 开门失败的原因,仅在bStatus为FALSE时有效0x00 没有错误0x10 未授权0x11 卡挂失或注销0x12 没有该门权限0x13 开门模式错误0x14 有效期错误0x15 防反潜模式0x16 胁迫报警未打开0x17 门常闭状态0x18 AB互锁状态0x19 巡逻卡0x1A 设备处于闯入报警状态0x20 时间段错误0x21 假期内开门时间段错误0x23 卡逾期0x30 需要先验证有首卡权限的卡片0x40 卡片正确,输入密码错误0x41 卡片正确,输入密码超时0x42 卡片正确,输入错误0x43 卡片正确,输入超时0x44 正确,输入密码错误0x45 正确,输入密码超时0x50 组合开门顺序错误0x51 组合开门需要继续验证0x60 验证通过,控制台未授权0x61 卡片正确,人脸错误0x62 卡片正确,人脸超时0x63 重复进入0x64 未授权,需要后端平台识别0x65 温度过高0x66 未戴口罩0x67 健康码获取失败0x68 黄码禁止通行0x69 红码禁止通行0x6a 健康码无效0x6b 绿码验证通过0x6c  绿码, 绿码,未接种0x70 获取健康码信息;Reason of unlock failure, only because it is valid when bStatus is FALSE0x00 no error0x10 unauthorized0x11 card lost or cancelled0x12 no door right0x13 unlock mode error0x14 valid period error0x15 anti sneak into mode0x16 forced alarm not unlocked0x17 door NC status0x18 AB lock status0x19 patrol card0x1A device is under intrusion alarm status0x20 period error0x21 unlock period error in holiday period0x23 Card is overdue0x30 first card right check required0x40 card correct, input password error0x41 card correct, input password timed out0x42 card correct, input error0x43 card correct, input timed out0x44 correct, input password error0x45 correct, input password timed out0x50 group unlock sequence error0x51 test required for group unlock0x60 test passed, control unauthorized0x61 card correct, input face error0x62 card correct, input face timed out0x63 repeat enter0x64 unauthorized, requiring back-end platform identification0x65 High body temperature0x66 no mask0x67 get health code fail0x68 No Entry because of yellow code0x69 No Entry because of red code0x6a health code is invalid0x6b entry because of green code0x70 get health code info;
        ('szRecordURL', c_char * 128),  # 刷卡录像的地址;record url;
        ('nNumbers', c_int),  # 抓图的张数;snap picture numbers;
        ('emAttendanceState', C_ENUM),  # 考勤状态 Refer: NET_ATTENDANCESTATE;attendance state Refer: NET_ATTENDANCESTATE;
        ('emDirection', C_ENUM),  # 开门方向 Refer: NET_ENUM_DIRECTION_ACCESS_CTL;open door direction Refer: NET_ENUM_DIRECTION_ACCESS_CTL;
        ('szClassNumber', c_char * 32),  # 班级（考勤）;Class number;
        ('szPhoneNumber', c_char * 16),  # 电话（考勤）;Phone number;
        ('szCardName', c_char * 64),  # 卡命名;Card name;
        ('szSN', c_char * 32),  # 智能锁序列号,无线配件需要该字段;wireless device serial number;
        ('bCitizenIDResult', C_BOOL),  # 人证比对结果;Compare result;
        ('szCitizenIDName', c_char * 30),  # 名字;Name;
        ('byReserved1', C_BYTE * 2),  # 字节对齐;Align;
        ('emCitizenIDSex', C_ENUM),  # 性别 Refer: EM_CITIZENIDCARD_SEX_TYPE;Sex Refer: EM_CITIZENIDCARD_SEX_TYPE;
        ('emCitizenIDEC', C_ENUM),  # 民族 Refer: EM_CITIZENIDCARD_EC_TYPE;EC Refer: EM_CITIZENIDCARD_EC_TYPE;
        ('stuCitizenIDBirth', NET_TIME),  # 出生日期(时分秒无效);Birth date;
        ('szCitizenIDAddress', c_char * 108),  # 住址;Address;
        ('szCitizenIDAuthority', c_char * 48),  # 签发机关;Authority;
        ('stuCitizenIDStart', NET_TIME),  # 有效起始日期(时分秒无效);Start time;
        ('stuCitizenIDEnd', NET_TIME),  # 有效截止日期(时分秒无效, 年为负数时表示长期有效);End time;
        ('bIsEndless', C_BOOL),  # 是否长期有效;Is end time unlimited;
        ('szSnapFaceURL', c_char * 128),  # 人脸图片保存地址;Face picture URL;
        ('szCitizenPictureURL', c_char * 128),  # 证件图片保存地址;Citizen picture URL;
        ('szCitizenIDNo', c_char * 20),  # 证件号码;Citizen card number;
        ('emSex', C_ENUM),  # 性别 Refer: NET_ACCESSCTLCARD_SEX;sex Refer: NET_ACCESSCTLCARD_SEX;
        ('szRole', c_char * 32),  # 角色;role;
        ('szProjectNo', c_char * 32),  # 项目ID;project No.;
        ('szProjectName', c_char * 64),  # 项目名称;project name;
        ('szBuilderName', c_char * 64),  # 施工单位全称;builder name;
        ('szBuilderID', c_char * 32),  # 施工单位ID;builder ID;
        ('szBuilderType', c_char * 32),  # 施工单位类型;builder type;
        ('szBuilderTypeID', c_char * 8),  # 施工单位类别ID;builder type ID;
        ('szPictureID', c_char * 64),  # 人员照片ID;picture ID;
        ('szContractID', c_char * 16),  # 原合同系统合同编号;contract ID in original contract system;
        ('szWorkerTypeID', c_char * 8),  # 工种ID;worker type ID;
        ('szWorkerTypeName', c_char * 32),  # 工种名称;worker type name;
        ('bPersonStatus', C_BOOL),  # 人员状态, TRUE:启用, FALSE:禁用;person status, TRUE:enable, FALSE:forbidden;
        ('emHatStyle', C_ENUM),  # 帽子类型 Refer: EM_HAT_STYLE;hat style Refer: EM_HAT_STYLE;
        ('emHatColor', C_ENUM),  # 帽子颜色 Refer: EM_UNIFIED_COLOR_TYPE;hat color Refer: EM_UNIFIED_COLOR_TYPE;
        ('stuManTemperatureInfo', NET_MAN_TEMPERATURE_INFO),  # 人员温度信息;human temperature info;
        ('nCompanionInfo', c_int),  # 陪同人员 stuCompanionInfo 个数;stuCompanionInfo's count;
        ('stuCompanionInfo', NET_COMPANION_INFO * 12),  # 陪同人员信息：姓名、卡号字段有效;companion info:name and card valid;
        ('emMask', C_ENUM),  # 口罩状态（EM_MASK_STATE_UNKNOWN、EM_MASK_STATE_NOMASK、EM_MASK_STATE_WEAR 有效） Refer: EM_MASK_STATE_TYPE;mask ( EM_MASK_STATE_UNKNOWN,EM_MASK_STATE_NOMASK,EM_MASK_STATE_WEAR is valid ) Refer: EM_MASK_STATE_TYPE;
        ('nFaceIndex', C_UINT),  # 一人多脸的人脸序号;face index;
        ('nScore', c_int),  # 人脸质量评分;Face quality score;
        ('nLiftNo', c_int),  # 电梯编号;Elevator number;
        ('szQRCode', c_char * 512),  # 二维码;QRCode;
        ('emFaceCheck', C_ENUM),  # 刷卡开门时，门禁后台校验人脸是否是同一个人 Refer: EM_FACE_CHECK; when swiping the card to open the door, the access control background checks whether the face is the same person Refer: EM_FACE_CHECK;
        ('emQRCodeIsExpired', C_ENUM),  # 
        ('emQRCodeState', C_ENUM),  # 
        ('stuQRCodeValidTo', NET_TIME),  # 二维码截止日期;QR code deadline;
        ('emLiftCallerType', C_ENUM),  # 梯控方式触发者 Refer: EM_LIFT_CALLER_TYPE;Ladder control trigger Refer: EM_LIFT_CALLER_TYPE;
        ('nBlockId', C_UINT),  # 上报事件数据序列号从1开始自增;The serial number of the reported event data increases from 1;
        ('szSection', c_char * 64),  # 部门名称;Department name;
        ('szWorkClass', c_char * 256),  # 工作班级;Work class;
        ('emTestItems', C_ENUM),  # 测试项目 Refer: EM_TEST_ITEMS;Test items Refer: EM_TEST_ITEMS;
        ('stuTestResult', NET_TEST_RESULT),  # ESD阻值测试结果;ESD resistance test result;
        ('bUseCardNameEx', C_BOOL),  # 是否使用卡命名扩展;Whether to use the card name extension;
        ('szCardNameEx', c_char * 128),  # 卡命名扩展;Card name extension;
        ('nHSJCResult', c_int),  # 核酸检测报告结果;Nucleic acid test report result;
        ('nVaccinateFlag', c_int),  # 是否已接种新冠疫苗（0:否，1:是）;Have you been vaccinated against the new crown vaccine, 0: No, 1: Yes;
        ('szVaccineName', c_char * 128),  # 新冠疫苗名称;New crown vaccine name;
        ('nDateCount', c_int),  # 历史接种日期有效数;Valid number of historical vaccination dates;
        ('szVaccinateDate', c_char * 256),  # 历史接种日期  历史接种日期 (yyyy-MM-dd)。 ”0000-00-00”，表示已接种，但无具体日期。;Historical vaccination date(yyyy-MM-dd). If you cannot provide the time, fill in "0000-00-00", which means that you have been vaccinated;
        ('emTravelCodeColor', C_ENUM),  # 返回行程码状态信息 Refer: EM_TRAVEL_CODE_COLOR;Travel Code Color Refer: EM_TRAVEL_CODE_COLOR;
        ('nCityCount', c_int),  # 最近14天经过的城市名有效数;Number of cities passed in the last 14 days;
        ('szPassingCity', c_char * 2048),  # 最近14天经过的城市名（按照时间顺序排列）最早经过的城市放第一个。;The names of the cities that have passed in the last 14 days. In chronological order, the earliest passing city is placed first;
        ('szTrafficPlate', c_char * 32),  # 车牌;TrafficPlate;
        ('szRecordLocalUrl', c_char * 128),  # 刷卡录像的地址;Record Url;
        ('szHSJCReportDate', c_char * 32),  # 核酸检测报告日期(格式: yyyy-MM-dd);Date of nucleic acid test report (format: yyyy-MM-dd);
        ('nHSJCExpiresIn', c_int),  # 核酸检测报告有效期(单位:天);Validity period of nucleic acid test report (unit: day);
        ('szAntigenReportDate', c_char * 32),  # 抗原检测报告日期(格式: yyyy-MM-dd);Antigen test report date (format: yyyy-MM-dd);
        ('nAntigenStatus', c_int),  # 抗原检测报告结果:
        ('nAntigenExpiresIn', c_int),  # 抗原检测报告有效期(单位:天);Validity period of antigen test report (unit: day);
        ('szCheckOutType', c_char * 32),  # 签出类型;Check Out Type;
        ('szCheckOutCause', c_char * 512),  # 签出原因;Check out Reason;
        ('nCreateTimeRealUTC', C_UINT),  # 刷卡时间，真实UTC时间戳;Swipe time, real UTC time;
        ('szReserved', c_char * 20),  # 字节对齐;Reserved;
        ('szLocationName', c_char * 256),  # 场所码名称;Location Name;
        ('szLocationAddress', c_char * 256),  # 场所码详细地址;Location Address;
        ('szLocationType', c_char * 256),  # 场所码类型;Location Type;
    ]

class NET_IN_SNAP_MNG_SHOT(Structure):
    """
    即时抓图(又名手动抓图)入参, 对应命令DH_CTRL_SNAP_MNG_SNAP_SHOT
    realtime snapshot (manual snapshot) input parameter, corresponding command DH_CTRL_SNAP_MNG_SNAP_SHOT
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 该结构体大小;the structure size;
        ('nChannel', c_int),  # 通道号;channel number;
        ('nTime', c_int),  # 连拍次数, 0表示停止抓拍,正数表示连续抓拍的张数;continuous snapshot times, 0 means stopping snapshot, positive number means the number of continuous snapshot;
    ]

class NET_OUT_SNAP_MNG_SHOT(Structure):
    """
    即时抓图(又名手动抓图)出参, 对应命令DH_CTRL_SNAP_MNG_SNAP_SHOT
    realtime snapshot (manual snapshot) output parameter, corresponding command DH_CTRL_SNAP_MNG_SNAP_SHOT
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 该结构体大小;the structure size;
    ]

class NET_EVENT_MANUALSNAP_CUSTOM_DATA(Structure):
    """
    手动抓拍专用上报内容
    manual-snap data
    """
    _fields_ = [
        ('stuWeighInfo', EVENT_CUSTOM_WEIGHT_INFO),  # 称重信息; weight info;
        ('byReserved', C_BYTE * 472),  # 保留字节;Reserved;
    ]

class NET_A_EVENT_MANUALSNAP_PARKING_INFO(Structure):
    """
    停车位数据信息
    parking space data information
    """
    _fields_ = [
        ('nChannel', C_UINT),  # 通道号，从0开始, -1表示未知通道;Channel number, starting from 0. -1 indicates an unknown channel;
        ('nStatus', C_UINT),  # 车位是否有车标记：0：未知 1：有车 2：无车;Whether there is a car in the parking space: 0: unknown 1: there is a car 2: no car;
        ('szPlateNumber', c_char * 64),  # 车牌号码;plate number;
        ('szParkingNo', c_char * 32),  # 车牌号码;plate number;
        ('szReserved', c_char * 128),  # 保留字节;Save bytes;
    ]

class NET_DEV_EVENT_TRAFFIC_MANUALSNAP_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_MANUALSNAP(交通手动抓拍事件)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFIC_MANUALSNAP's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('nLane', c_int),  # 对应车道号;lane number;
        ('szManualSnapNo', C_BYTE * 64),  # 手动抓拍序号;manual snap number;
        ('stuObject', SDK_MSG_OBJECT),  # 检测到的物体;have being detected object;
        ('stuVehicle', SDK_MSG_OBJECT),  # 检测到的车身信息;have being detected vehicle;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 表示交通车辆的数据库记录;TrafficCar info;
        ('stuFileInfo', SDK_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byOpenStrobeState', C_BYTE),  # 开闸状态, 具体请见 EM_OPEN_STROBE_STATE;Open status, see EM_OPEN_STROBE_STATE;
        ('byReserved', C_BYTE * 1),
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', SDK_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('bReserved', C_BYTE * 504),  # 保留字节,留待扩展.;
        ('stuCustom', NET_EVENT_MANUALSNAP_CUSTOM_DATA),  # 手动抓拍专用上报内容;Custom data;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('stuParkingInfo', NET_A_EVENT_MANUALSNAP_PARKING_INFO * 32),  # 停车位数据信息;Parking space data information;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;The event public extension field structure;
    ]

class NET_CTRL_OPEN_STROBE(Structure):
    """
    开启道闸参数(对应CTRL_OPEN_STROBE命令)
    open gateway parameter(corresponding to CTRL_OPEN_STROBE command)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannelId', c_int),  # 通道号, nChannelId为-1时表示未使用通道号, 表示单通道设备;channel no., when nChannelId is -1,denotes unused channel no. and single channel device;
        ('szPlateNumber', c_char * 64),  # 车牌号码;plate no.;
        ('emOpenType', C_ENUM),  # 开闸类型 Refer: EM_OPEN_STROBE_TYPE;open strobe type Refer: EM_OPEN_STROBE_TYPE;
        ('nLocation', c_int),  # 开闸车道号;Location
        ('szCustomParkNo', c_char * 32),  # 自定义车道号，优先使用自定义车道号，自定义车道号为空，则使用location;Custom lane number, priority given to using custom lane number. If the custom lane number is empty, use location
    ]

class NET_CTRL_CLOSE_STROBE(Structure):
    """
    关闭道闸参数(对应CTRL_CLOSE_STROBE命令)
    close gateway parameter(corresponding to CTRL_CLOSE_STROBE command)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannelId', c_int),  # 通道号;channel no.;
        ('nLocation', c_int),  # 关闸车道号;Location.;
    ]

class NET_A_COMM_STATE(Structure):
    """
    串口状态
    Serial port status
    """
    _fields_ = [
        ('uBeOpened', C_UINT),
        ('uBaudRate', C_UINT),
        ('uDataBites', C_UINT),
        ('uStopBits', C_UINT),
        ('uParity', C_UINT),
        ('bReserved', C_BYTE * 32),
    ]

class NET_SMARTDETECT_HUMAN_OBJECT(Structure):
    """
    智能动检(人)对象信息
    object info of smart motion detection about human
    """
    _fields_ = [
        ('nHumanID', C_UINT),  # 人动检ID;object ID about human;
        ('stuRect', NET_RECT),  # 人的位置;rect of human;
        ('bReserved', C_BYTE * 508),  # 保留字节;reserved;
    ]

class NET_A_DEV_EVENT_SMARTMOTION_HUMAN_INFO(Structure):
    """
    事件类型EVENT_ALARM_SMARTMOTION_HUMAN(智能视频移动侦测事件(人))对应的数据块描述信息
    Corresponding to data block description of event type EVENT_ALARM_SMARTMOTION_HUMAN(smart video motion detection event about human)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('nAction', c_int),  # 1:开始 2:停止;event action, 0:pulse, 1:start, 2:stop;;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS;
        ('UTC', NET_TIME_EX),  # 事件发生的时间;UTC;
        ('nEventID', C_UINT),  # 事件ID;event ID;
        ('stuSmartRegion', NET_MOTIONDETECT_REGION_INFO * 32),  # 智能动检区域信息;region info of smart motion detection;
        ('nSmartRegionNum', C_UINT),  # 智能动检区域个数;count of smart motion detection region;
        ('nHumanObjectNum', C_UINT),  # 智能动检(人)对象个数;count of smart motion detection objects about human;
        ('stuHumanObject', NET_SMARTDETECT_HUMAN_OBJECT * 64),  # 智能动检(人)对象信息;object info of smart motion detection about human;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;The event public extension field structure;
        ('bReserved', C_BYTE * 1024),  # 保留字节;reserved;
    ]

class MANUAL_SNAP_PARAMETER(Structure):
    """
    智能交通, 手动抓拍 (对应结构体 MANUAL_SNAP_PARAMETER)
    manual snap (struct MANUAL_SNAP_PARAMETER)
    """
    _fields_ = [
        ('nChannel', c_int),  # 通道号;snap channel,start with 0
        ('bySequence', C_BYTE * 64),  # 抓图序列号字符串;snap sequence string
        ('byReserved', C_BYTE * 60), # 保留字段;reserved
    ]

class NET_OUT_ADD_ANALYSE_TASK(Structure):
    """
    CLIENT_AddAnalyseTask 接口输出参数
    output parameter of CLIENT_AddAnalyseTask
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nTaskID', C_UINT),  # 任务ID;task ID;
        ('nVirtualChannel', C_UINT),  # 任务对应的虚拟通道号;virtual channel;
        ('szUrl', c_char * 256),  # 智能码流rtsp地址;RTSP address of intelligent stream;
    ]

class NET_PUSH_PICFILE_BYRULE_INFO(Structure):
    """
    推送远程图片文件，添加任务时无规则和图片信息，通过推送图片接口，每张图片中带有不同的规则信息（目前能源场景中使用）
    Push remote picture file, add task without rules and picture information, through the push picture interface, each picture has different rule information (currently used in the energy scene)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
        ('emStartRule', C_ENUM),  # 智能任务启动规则 Refer: EM_ANALYSE_TASK_START_RULE;Analyse tesk start rule Refer: EM_ANALYSE_TASK_START_RULE;
        ('szTaskUserData', c_char * 256),  # 任务数据;Task user data;
    ]

class NET_IN_FIND_ANALYSE_TASK(Structure):
    """
    CLIENT_FindAnalyseTask 接口输入参数
    input parameter of CLIENT_FindAnalyseTask
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_ANALYSE_TASKS_INFO(Structure):
    """
    智能分析任务信息
    info of analyse task
    """
    _fields_ = [
        ('nTaskID', C_UINT),  # 任务ID;task ID;
        ('emAnalyseState', C_ENUM),  # 分析状态 Refer: EM_ANALYSE_STATE;analyse state Refer: EM_ANALYSE_STATE;
        ('emErrorCode', C_ENUM),  # 错误码 Refer: EM_ANALYSE_TASK_ERROR;error code Refer: EM_ANALYSE_TASK_ERROR;
        ('byReserved1', C_BYTE * 4),  # 字节对齐;byte alignment;
        ('szTaskUserData', c_char * 256),  # 任务数据;task user date;
        ('nVideoAnalysisProcess', c_int),  # 录像分析进度，当任务添加接口CLIENT_AddAnalyseTask emDataSourceType参数为录像分析"EM_DATA_SOURCE_REMOTE_PICTURE_FILE"时有效 范围1~100，100表示分析完成;Video analysis progress, is is valid when task add interface CLIENT_AddAnalyseTask's parameter emDataSourceType is "EM_DATA_SOURCE_REMOTE_PICTURE_FILE", the valid range is 1 ~ 100100, indicating that the analysis is completed;
        ('szUrl', c_char * 256),  # 智能流rtsp地址，实时流时才填写;RTSP address of intelligent stream, which can be filled in only when real-time flow;
        ('emClassType', C_ENUM),  # 智能大类类型 Refer: EM_SCENE_CLASS_TYPE;Class type Refer: EM_SCENE_CLASS_TYPE;
        ('emSourceType', C_ENUM),  # 数据源类型 Refer: EM_DATA_SOURCE_TYPE;Source type Refer: EM_DATA_SOURCE_TYPE;
        ('nChipId', c_int),  # 任务使用的分析子卡ID.-1表示无效子卡，大于等于0的值表示子卡ID号emErrorCode为EM_ANALYSE_TASK_ERROR_ANALYZER_OFF_LINE或EM_ANALYSE_TASK_ERROR_ANALYZER_ON_LINE时此字段有效;The analysis sub card ID used by the task. - 1 represents the invalid sub card, and a value greater than or equal to 0 represents the sub card ID numberThis field is valid when the emErrorCode is EM_ANALYSE_TASK_ERROR_ANALYZER_OFF_LINE or EM_ANALYSE_TASK_ERROR_ANALYZER_ON_LINE;
        ('byReserved', C_BYTE * 428),  # 保留字节;reserved bytes;
    ]

class NET_OUT_FIND_ANALYSE_TASK(Structure):
    """
    CLIENT_FindAnalyseTask 接口输出参数
    out parameter of CLIENT_FindAnalyseTask
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nTaskNum', C_UINT),  # 智能分析任务个数;number of analyse tasks;
        ('stuTaskInfos', NET_ANALYSE_TASKS_INFO * 256),  # 智能分析任务信息;info of analyse tasks;
    ]

class NET_IN_REMOVE_ANALYSE_TASK(Structure):
    """
    CLIENT_RemoveAnalyseTask 接口输入参数
    input parameter of CLIENT_RemoveAnalyseTask
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nTaskID', C_UINT),  # 任务ID;task ID;
    ]

class NET_OUT_REMOVE_ANALYSE_TASK(Structure):
    """
    CLIENT_RemoveAnalyseTask 接口输出参数
    output parameter of CLIENT_RemoveAnalyseTask
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_ANALYSE_RULE_INFO(Structure):
    """
    智能分析规则信息
    info of analyse rule
    """
    _fields_ = [
        ('emClassType', C_ENUM),  # 分析大类类型 Refer: EM_SCENE_CLASS_TYPE;class type Refer: EM_SCENE_CLASS_TYPE;
        ('dwRuleType', C_DWORD),  # 规则类型, 详见dhnetsdk.h中"智能分析事件类型"
        ('pReserved', c_void_p),  # 规则配置, 具体结构体类型根据dwRuleType来确定, 具体信息见dwRuleType的注释;rule config, the rule config struct is determined by dwRuleType, see the comments of dwRuleType;
        ('nObjectTypeNum', C_UINT),  # 检测物体类型个数, 为0 表示不指定物体类型;count of object types, 0 means no types;
        ('emObjectTypes', C_ENUM * 16),  # 检测物体类型列表 Refer: EM_ANALYSE_OBJECT_TYPE;object types Refer: EM_ANALYSE_OBJECT_TYPE;
        ('szRuleName', c_char * 128),  # 规则名称，不带预置点的设备规则名称不能重名，带预置点的设备，同一预置点内规则名称不能重名，不同预置点之间规则名称可以重名;rule name;
        ('byReserved', C_BYTE * 828),  # 保留字节;reserved bytes;
    ]

class NET_ANALYSE_RULE(Structure):
    """
    智能分析规则
    analyse rule
    """
    _fields_ = [
        ('stuRuleInfos', NET_ANALYSE_RULE_INFO * 32),  # 分析规则信息;info of analyse rules;
        ('nRuleCount', C_UINT),  # 分析规则条数;number of analyse rules;
        ('byReserved', C_BYTE * 1028),  # 保留字节;reserved bytes;
    ]

class NET_REMOTE_STREAM_INFO(Structure):
    """
    远程实时视频源信息("analyseTaskManager.analysePushPictureFileByRule"协议使用)
    Remote real-time video source information (used in protocol "analyseTaskManager.analysePushPictureFileByRule")
    """
    _fields_ = [
        ('emStreamProtocolType', C_ENUM),  # 视频流协议类型 Refer: EM_STREAM_PROTOCOL_TYPE;Stream protocol type Refer: EM_STREAM_PROTOCOL_TYPE;
        ('byReserved1', C_BYTE * 4),  # 用于字节对齐;Used for byte alignment;
        ('szPath', c_char * 256),  # 视频流地址;Video streaming path;
        ('szIp', c_char * 64),  # IP 地址;IP;
        ('wPort', c_uint16),  # 端口号;port;
        ('szUser', c_char * 64),  # 用户名;user;
        ('szPwd', c_char * 64),  # 密码;password;
        ('nChannelID', c_int),  # 通道号;ChannelID;;
        ('nStreamType', C_UINT),  # 码流类型, 0:主码流; 1:辅1码流; 2:辅2码流;;Stream type, 0-main stream, 1-extra stream 1, 2-extra stream 2;
        ('byReserved', c_char * 1024),  # 保留字节;Reserved;
    ]

class NET_PUSH_PICTURE_BYRULE_INFO(Structure):
    """
    智能分析图片信息
    Intelligent analysis of picture information
    """
    _fields_ = [
        ('szFileID', c_char * 128),  # 文件ID;File ID;
        ('nOffset', C_UINT),  # 文件数据在二进制数据中的偏移, 单位:字节 (URL和Offset/Length应该是两者有且只有一个);The Offset of the file data in binary data, in bytes (RemoteStreamInfo and Offset/Length should be both and only one).;
        ('nLength', C_UINT),  # 文件数据长度, 单位:字节 (URL和Offset/Length应该是两者有且只有一个);Length of file data, in bytes;
        ('stuRuleInfo', NET_ANALYSE_RULE),  # 分析规则信息;Analyze rule information;
        ('szUserDefineData', c_char * 512),  # 用户定义数据，通过client.notifyTaskResult回调中”UserDefineData”字段带回;User-defined data;
        ('szModelUrl', c_char * 512),  # 模型远程文件url地址，目前支持http方式下载;Model remote file URL address, currently support HTTP download;
        ('stuRemoteStreamInfo', NET_REMOTE_STREAM_INFO),  # 远程实时视频流信息;Remote real-time video streaming information;
        ('nDetectType', C_UINT),  # 能源SDT仪器仪表使用;0：深度学习 1：建模方式;Energy SDT instrument use; 0: Deep learning 1: modeling approach;
        ('nPicUrlNum', c_int),  # 图片远程文件url地址个数;Number of URL addresses of remote image files;
        ('szPicUrl', c_char * 64 * 512),    # 图片远程文件url地址,目前支持http方式下载;The URL address of the remote image file. At present, it supports HTTP download;
        ('byReserved', C_BYTE * 256),       # 保留字节;Reserved;
    ]

class NET_IN_PUSH_ANALYSE_PICTURE_FILE_BYRULE(Structure):
    """
    CLIENT_PushAnalysePictureFileByRule 接口输入参数
    CLIENT_PushAnalysePictureFileByRule input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
        ('nTaskID', C_UINT),  # 任务ID;TaskID;
        ('pstuPushPicByRuleInfos', POINTER(NET_PUSH_PICTURE_BYRULE_INFO)),  # 推送图片信息，文件列表支持url路径和二进制数据两种方式，但是每次只能选择一种方式，即URL和Offset/Length应该是两者有且只有一个用户自定义空间;Push picture information, file list support URL path and binary data two ways, but can only choose one way at a timeUsers apply for their own memory;
        ('nPicNum', C_UINT),  # 推送图片数量,用户定义;Number of images to push, user-defined;
        ('nBinBufLen', C_UINT),  # 数据缓冲区长度, 单位:字节;BufLen;
        ('pBinBuf', POINTER(c_char)),  # 数据缓冲区, 由用户申请和释放,选择nOffset/nLength方式，需要传送图片数据;Data buffers, applied and released by the user;
    ]

class NET_OUT_PUSH_ANALYSE_PICTURE_FILE_BYRULE(Structure):
    """
    CLIENT_PushAnalysePictureFileByRule 接口输出参数
    CLIENT_PushAnalysePictureFileByRule output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
    ]

class NET_IMAGE_INFO(Structure):
    """
    图片信息
    Image info
    """
    _fields_ = [
        ('emPicType', C_ENUM),  # 图片类型 Refer: EM_PIC_TYPE;Picture type Refer: EM_PIC_TYPE;
        ('nOffset', C_UINT),  # 在二进制数据块中的偏移;Offset in binary data;
        ('nLength', C_UINT),  # 图片大小,单位:字节;Length,Unit:Byte;
        ('szFilePath', c_char * 256),  # 图片路径;File path;
        ('byReserved', C_BYTE * 1024),  # 预留字节;Reserved;
    ]

class NET_A_DEV_EVENT_DIALRECOGNITION_INFO(Structure):
    """
    仪表检测事件, 对应事件类型 EVENT_IVS_DIALRECOGNITION
    Instrument detection event, corresponding event type EVENT_IVS_DIALRECOGNITION
    """
    _fields_ = [
        ('nChannelID', C_UINT),  # 视频通道号,从0开始;ChannelID;
        ('nPresetID', C_UINT),  # 预置点ID,如果普通IPC则为0;PresetID,If normal IPC is 0;
        ('szTaskID', c_char * 64),  # 任务ID.添加时设备端生成;Task ID. Device generated;
        ('emType', C_ENUM),  # 仪表类型 Refer: EM_INSTRUMENT_TYPE;The instrument type Refer: EM_INSTRUMENT_TYPE;
        ('nRetImageInfoNum', c_int),  # 返回的图片信息个数;Number of image Info returned;
        ('stuImgaeInfo', NET_IMAGE_INFO * 8),  # 图片信息;Image info;
        ('szDialResult', c_char * 2048),  # 检测结果，根据Type的不同，格式也不同;Dial result;
        ('nOriginalImageOffset', c_int),  # 原始图片在二进制数据块中的偏移;The offset of the original image in the binary data block;
        ('nOriginalImageLength', c_int),  # 原始图片大小,单位：字节;Original image size, unit: bytes;
        ('nAlarmType', C_UINT),         # 告警类型：0-该字段无效;1-数值异常;2-定时上报; 3-高阀值报警; 4-低阀值报警;Alarm type: 0-this field is invalid; 1-value is abnormal; 2-periodic report; 3-High threshold alarm; 4-Low threshold alarm;
        ('szDialSubType', c_char * 32),  # 仪表检测具体子类型;Dial Detection Subtype;
        ('fUpperThreshold', c_float),   # 报警上限阈值;Upper alarm threshold;
        ('fLowerThreshold', c_float),   # 报警下限阈值;Lower alarm threshold;
        ('stuBoundingBox', NET_RECT * 128),  # 包围盒;bounding box;
        ('nRetBoundingBoxNum', c_int),  # 包围盒个数;bounding box count;
        ('szReserved', c_char * 968),  # 预留字节;Reserved;
    ]

class NET_A_POINTCOORDINATE(Structure):
    """
    景物点位置
    scenery position
    """
    _fields_ = [
        ('nX', c_int),  # 第一个元素表示景物点的x坐标(0~8191);X coordinate range: [0,8191];
        ('nY', c_int),  # 第二个元素表示景物点的y坐标(0~8191);Y coordinate range: [0,8191];
    ]

class NET_CFG_CALIBRATEBOX_INFO(Structure):
    """
    校准框信息
    Calibrate box info
    """
    _fields_ = [
        ('stuCenterPoint', NET_A_POINTCOORDINATE),  # 校准框中心点坐标(点的坐标归一化到[0,8191]区间);Calibrate box center point. range: [0,8191];
        ('fRatio', c_float),  # 相对基准校准框的比率(比如1表示基准框大小，0.5表示基准框大小的一半);The relative ratio of the calibrate box(such as 1 means the calibrate box,0.5 means the half size of the calibrate box);
    ]

class NET_CFG_SIZE(Structure):
    """
    物体尺寸
    Size
    """
    _fields_ = [
        ('nWidthOrnArea', c_float),  # 宽或面积;Width Or Area;
        ('nHeight', c_float),  # 高;Height;
    ]

class NET_CFG_SIZEFILTER_INFO(Structure):
    """
    尺寸过滤器
    Size filter
    """
    _fields_ = [
        ('nCalibrateBoxNum', c_int),  # 校准框个数;Calibration pane number;
        ('stuCalibrateBoxs', NET_CFG_CALIBRATEBOX_INFO * 10),  # 校准框(远端近端标定模式下有效);Calibration box (far and near-end calibration mode only);
        ('bMeasureModeEnable', c_bool),  # 计量方式参数是否有效;Measurement mode enabled or not;
        ('bMeasureMode', C_BYTE),  # 计量方式,0-像素，不需要远端、近端标定, 1-实际长度，单位：米, 2-远端近端标定后的像素;Measurement mode, 0-pixel, far and near-end calibration not necessary, 1- real length, unit: meter, 2- pixel after far and near-end calibration;
        ('bFilterTypeEnable', c_bool),  # 过滤类型参数是否有效;Filter type enabled or notByArea,ByRatio as compatible only, with independent ByArea and ByRatio alternatives as substitute 2012/03/06;
        ('bFilterType', C_BYTE),  # 过滤类型:0:"ByLength",1:"ByArea", 2"ByWidthHeight";Filter type:0:"ByLength",1:"ByArea", 2"ByWidthHeight";
        ('bFilterMinSizeEnable', c_bool),  # 物体最小尺寸参数是否有效;Min object size parameter is valid or not;
        ('bFilterMaxSizeEnable', c_bool),  # 物体最大尺寸参数是否有效;Max object size parameter is valid or not;
        ('abByArea', c_bool),
        ('abMinArea', c_bool),
        ('abMaxArea', c_bool),
        ('abMinAreaSize', c_bool),
        ('abMaxAreaSize', c_bool),
        ('bByArea', c_bool),  # 是否按面积过滤 通过能力ComplexSizeFilter判断是否可用;Filter by area or not. You can use ComplexSizeFilter to see it works or not.;
        ('stuFilterMinSize', NET_CFG_SIZE),  # 物体最小尺寸 "ByLength"模式下表示宽高的尺寸，"ByArea"模式下宽表示面积，高无效(远端近端标定模式下表示基准框的宽高尺寸)。;Min object size      size of length ratio under "ByLength" Mode,size of area under "ByArea" mode, invalid height (size of standard box lengths under far and near-end calibration mode);
        ('stuFilterMaxSize', NET_CFG_SIZE),  # 物体最大尺寸 "ByLength"模式下表示宽高的尺寸，"ByArea"模式下宽表示面积，高无效(远端近端标定模式下表示基准框的宽高尺寸)。;Max object size size of length ratio under "ByLength" mode, size of area under "ByArea" mode", invalid height (size of standard box lengths under far and near-end calibration mode);
        ('nMinArea', c_float),  # 最小面积;Min area;
        ('nMaxArea', c_float),  # 最大面积;Max area;
        ('stuMinAreaSize', NET_CFG_SIZE),  # 最小面积矩形框尺寸 "计量方式"为"像素"时，表示最小面积矩形框的宽高尺寸；"计量方式"为"远端近端标定模式"时，表示基准框的最小宽高尺寸；;Min area rectangle box.   When  "measurement method" is "pixel", it represents its sizes of lengths; when "measurement method" is "far and near-end calibration mode", it represents the min sizes of lengths of standard box;
        ('stuMaxAreaSize', NET_CFG_SIZE),  # 最大面积矩形框尺寸, 同上;Max area rectangle box, same as above;
        ('abByRatio', c_bool),
        ('abMinRatio', c_bool),
        ('abMaxRatio', c_bool),
        ('abMinRatioSize', c_bool),
        ('abMaxRatioSize', c_bool),
        ('bByRatio', c_bool),  # 是否按宽高比过滤 通过能力ComplexSizeFilter判断是否可用;Filter by length ratio or not   . You can use ComplexSizeFilter to see it works or not.;
        ('bReserved1', c_bool * 2),
        ('dMinRatio', c_double),  # 最小宽高比;Min W/H ratio;
        ('dMaxRatio', c_double),  # 最大宽高比;Max W/H ratio;
        ('stuMinRatioSize', NET_CFG_SIZE),  # 最小宽高比矩形框尺寸，最小宽高比对应矩形框的宽高尺寸。;Min W/H ratio rectangle box size, min W/H ratio corresponding to sizes of lengths of rectangle box;
        ('stuMaxRatioSize', NET_CFG_SIZE),  # 最大宽高比矩形框尺寸，同上;Max W/H ratio rectangle box size. See above information.;
        ('nAreaCalibrateBoxNum', c_int),  # 面积校准框个数;Area calibration box number;
        ('stuAreaCalibrateBoxs', NET_CFG_CALIBRATEBOX_INFO * 10),  # 面积校准框;Area calibration box;
        ('nRatioCalibrateBoxs', c_int),  # 宽高校准框个数;W/H calibration box number;
        ('stuRatioCalibrateBoxs', NET_CFG_CALIBRATEBOX_INFO * 10),  # 宽高校准框;W/H calibration box number;
        ('abBySize', c_bool),  # 长宽过滤使能参数是否有效;Valid filter by L/H ration parameter enabled or not;
        ('bBySize', c_bool),  # 长宽过滤使能;L/W filter enabled;
        ('bReserved', C_BYTE * 518),  # 保留字段;Reserved;
    ]

class NET_IVS_DIALRECOGNITION_RULE_INFO(Structure):
    """
    EVENT_IVS_DIALRECOGNITION(仪表检测事件)对应的规则配置
    Rule type : EVENT_IVS_DIALRECOGNITION(Dial recogntion) configuration
    """
    _fields_ = [
        ('emType', C_ENUM),  # 仪表类型 Refer: EM_DIALDETECT_TYPE;Instrument type Refer: EM_DIALDETECT_TYPE;
        ('bSizeFileter', C_BOOL),  # 规则特定的尺寸过滤器是否有效;Whether the stuSizeFileter is valid;
        ('stuSizeFileter', NET_CFG_SIZEFILTER_INFO),  # 规则特定的尺寸过滤器;Rule-specific size filter;
        ('stuDetectRegion', NET_A_POINTCOORDINATE * 20),  # 检测区域;Detect Region;
        ('nDetectRegionNum', c_int),  # 检测区域顶点数;Num of Detect Region;
        ('nKinfeOpenAngleThreshold', c_int),  # 敞开式隔离开关有效,分夹角阈值, 单位度,取值范围0~90, 建议20;The open-type isolating switch is valid, the sub-angle threshold value, unit degree, the value range is 0~90, 20 is recommended;
        ('nKinfeClossAngleThreshold', c_int),  # 敞开式隔离开关有效,合夹角阈值, 单位度,取值范围0~90, 建议10;Open-type isolating switch is valid, closing angle threshold, unit degree, value range 0~90, recommended 10;
        ('bReserved', c_char * 2044),  # 保留字节;Reserved;
    ]

class NET_AIRBORNE_DETECT(Structure):
    """
    挂空悬浮物检测异常输出结果
    Airborne Detect info
    """
    _fields_ = [
        ('emAirborneType', C_ENUM),  # 挂空悬浮物具体类型 Refer: EM_AIRBORNE_TYPE;Airborne type Refer: EM_AIRBORNE_TYPE;
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_NEST_DETECT(Structure):
    """
    鸟巢检测结果
    Nest Detect info
    """
    _fields_ = [
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_DIAL_DETECT(Structure):
    """
    表盘检测结果
    Dial Detect info
    """
    _fields_ = [
        ('emDialState', C_ENUM),  # 表盘状态 Refer: EM_DIAL_STATE;dial state Refer: EM_DIAL_STATE;
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_LEAKAGE_DETECT(Structure):
    """
    渗漏检测结果
    Nest Detect info
    """
    _fields_ = [
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_DOOR_DETECT(Structure):
    """
    箱门检测结果
    Door Detect info
    """
    _fields_ = [
        ('emDoorState', C_ENUM),  # 箱门状态 Refer: EM_DOOR_STATE;door state Refer: EM_DOOR_STATE;
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_RESPIRATOR_DETECT(Structure):
    """
    呼吸器检测结果
    Respirator Detect info
    """
    _fields_ = [
        ('emRespiratorState', C_ENUM),  # 呼吸器状态 Refer: EM_RESPIRATOR_STATE;Respirator state Refer: EM_RESPIRATOR_STATE;
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_SMOKING_DETECT(Structure):
    """
    吸烟检测结果
    Smoking detect info
    """
    _fields_ = [
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_INSULATOR_DETECT(Structure):
    """
    绝缘子检测结果
    Insulator detect info
    """
    _fields_ = [
        ('emInsulatorState', C_ENUM),  # 绝缘子状态 Refer: EM_INSULATOR_STATE;insulator state Refer: EM_INSULATOR_STATE;
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_COVER_PLATE_DETECT(Structure):
    """
    盖板检测结果
    Cover plate detect info
    """
    _fields_ = [
        ('emCoverPlateState', C_ENUM),  # 盖板状态 Refer: EM_COVER_PLATE_STATE;cover plate state Refer: EM_COVER_PLATE_STATE;
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_PRESSING_PLATE_DETECT(Structure):
    """
    压板检测结果
    Pressing plate detect info
    """
    _fields_ = [
        ('emPressingPlateState', C_ENUM),  # 压板状态 Refer: EM_PRESSING_PLATE_STATE;pressing plate state Refer: EM_PRESSING_PLATE_STATE;
        ('stuBoundingBox', NET_RECT),  # 包围盒;bounding box;
    ]

class NET_METAL_CORROSION(Structure):
    """
    金属锈蚀结果
    The result of metal corrosion
    """
    _fields_ = [
        ('stuBoundingBox', NET_RECT),  # 包围盒;Bounding box;
        ('bReserved', c_char * 128),  # 预留字段;Reserved;
    ]

class NET_A_DEV_EVENT_ELECTRICFAULTDETECT_INFO(Structure):
    """
    仪表类缺陷检测事件
    Electric fault detection
    """
    _fields_ = [
        ('emClassType', C_ENUM),  # 智能事件所属大类 Refer: EM_CLASS_TYPE;class type Refer: EM_CLASS_TYPE;
        ('nChannel', C_UINT),  # 视频通道号;channel id;
        ('nRuleID', C_UINT),  # 智能事件规则编号，用于标示哪个规则触发的事件;Rule id;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS;
        ('UTC', NET_TIME_EX),  # 事件发生的时间;PTS;
        ('nPresetID', C_UINT),  # 预置点ID;preset ID;
        ('nUTCMS', C_UINT),  # 事件时间毫秒数;UTCMS;
        ('emEnableRules', C_ENUM * 16),  # 对应设备所使能的检测规则 Refer: EM_A_ELECTRIC_FAULT_ENABLE_RULES;enable rules Refer: EM_A_ELECTRIC_FAULT_ENABLE_RULES;
        ('nEnableRulesNum', c_int),  # 设备所使能的检测规则个数;enable rules number;
        ('nAirborneDetectNum', c_int),  # 挂空悬浮物检测异常输出结果个数;Airborne Detect number;
        ('stuAirborneDetectInfo', NET_AIRBORNE_DETECT * 8),  # 挂空悬浮物检测异常输出结果;Airborne Detect info;
        ('stuNestDetectInfo', NET_NEST_DETECT * 8),  # 鸟巢检测结果;Nest Detect info;
        ('nNestDetectNum', c_int),  # 鸟巢检测结果个数;Nest Detect number;
        ('nDialDetectNum', c_int),  # 表盘检测结果个数;Dial Detect number;
        ('stuDialDetectInfo', NET_DIAL_DETECT * 8),  # 表盘检测结果;Dial Detect info;
        ('stuLeakageDetectInfo', NET_LEAKAGE_DETECT * 8),  # 渗漏检测结果;Leakage Detect info;
        ('nLeakageDetectNum', c_int),  # 渗漏检测结果个数;Leakage Detect number;
        ('nDoorDetectNum', c_int),  # 箱门检测结果个数;Door Detect number;
        ('stuDoorDetectInfo', NET_DOOR_DETECT * 8),  # 箱门检测结果;Door Detect info;
        ('stuRespiratorDetectInfo', NET_RESPIRATOR_DETECT * 8),  # 呼吸器检测结果;Respirator Detect info;
        ('nRespiratorDetectNum', c_int),  # 呼吸器检测个数;Respirator Detect number;
        ('nSmokingDetectNum', c_int),  # 吸烟检测结果个数;Smoking detect number;
        ('stuSmokingDetectInfo', NET_SMOKING_DETECT * 8),  # 吸烟检测结果;Smoking detect info;
        ('stuSceneImageInfo', SCENE_IMAGE_INFO),  # 大图;Scene image info;
        ('stuInsulatorDetectInfo', NET_INSULATOR_DETECT * 8),  # 绝缘子检测结果;Insulator detect info;
        ('nInsulatorDetectNum', c_int),  # 绝缘子检测结果个数;Insulator detect number;
        ('nCoverPlateDetectNum', c_int),  # 盖板检测结果个数;Cover plate detect number;
        ('stuCoverPlateDetectInfo', NET_COVER_PLATE_DETECT * 8),  # 盖板检测结果;Cover plate detect info;
        ('stuPressingPlateDetectInfo', NET_PRESSING_PLATE_DETECT * 8),  # 压板检测结果;Pressing plate detect info;
        ('nPressingPlateDetectNum', c_int),  # 压板检测结果个数;Pressing plate detect number;
        ('nMetalCorrosionNum', c_int),  # 金属锈蚀结果个数;Metal corrosion detect number;
        ('stuMetalCorrosionInfo', NET_METAL_CORROSION * 8),  # 金属锈蚀结果;Metal Corrosion detect Info;
        ('bReserved', C_BYTE * 1024),  # 预留字段;Reserved;
    ]

class NET_IVS_ELECTRICFAULT_DETECT_RULE_INFO(Structure):
    """
    EVENT_IVS_ELECTRICFAULT_DETECT(仪表类缺陷检测事件)对应的规则配置
    Rule type : EVENT_IVS_ELECTRICFAULT_DETECT(Electric fault detect)configuration
    """
    _fields_ = [
        ('bAirborneDetectEnable', C_BOOL),  # 挂空悬浮物检测使能;AirborneDetect enable;
        ('bNestDetectEnable', C_BOOL),  # 鸟巢检测使能;Nest detect enable;
        ('bDialDetectEnable', C_BOOL),  # 表盘检测(表盘模糊)使能;Dial detect enable;
        ('bLeakageDetectEnable', C_BOOL),  # 渗漏检测使能;Leakage detect enable;
        ('bDoorDetectEnable', C_BOOL),  # 箱门检测使能;Door detect enable;
        ('bRespiratorDetectEnable', C_BOOL),  # 呼吸器检测使能;Respirator detect enable;
        ('bSmokingDetectEnable', C_BOOL),  # 吸烟检测使能;Smoking detect enable;
        ('bInsulatorDetectEnable', C_BOOL),  # 绝缘子检测使能;Insulator detect enable;
        ('bCoverPlateDetectEnable', C_BOOL),  # 盖板检测使能;Cover plate detect enable;
        ('bPressingPlateDetectEnable', C_BOOL),  # 压板开合检测使能;Pressing plate detect enable;
        ('bMetalCorrosionEnable', C_BOOL),  # 金属锈蚀检测使能;Metal corrosion enable;
        ('bSizeFileter', C_BOOL),  # 规则特定的尺寸过滤器是否有效;Whether the stuSizeFileter is valid;
        ('stuSizeFileter', NET_CFG_SIZEFILTER_INFO),  # 规则特定的尺寸过滤器;Rule-specific size filter;
        ('stuDetectRegion', NET_A_POINTCOORDINATE * 20),  # 检测区域;Detect Region;
        ('nDetectRegionNum', c_int),  # 检测区域顶点数;Num of Detect Region;
        ('bReserved', c_char * 2048),  # 保留字节;Reserved;
    ]

class NET_CB_ANALYSE_TASK_STATE_INFO(Structure):
    """
    智能分析任务状态回调信息
    callback info of attach analyse state
    """
    _fields_ = [
        ('stuTaskInfos', NET_ANALYSE_TASKS_INFO * 64),  # 智能分析任务信息;info of analyse task;
        ('nTaskNum', C_UINT),  # 任务个数;number of task;
        ('byReserved', C_BYTE * 1024),  # 保留字节;reserved bytes;
    ]

class NET_IN_ATTACH_ANALYSE_TASK_STATE(Structure):
    """
    CLIENT_AttachAnalyseTaskState 接口输入参数
    input parameter of CLIENT_AttachAnalyseTaskState
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nTaskIDs', C_UINT * 64),  # 智能分析任务ID;task IDs;
        ('nTaskIdNum', C_UINT),  # 智能分析任务个数, 0表示订阅全部任务;number of analyse task, 0 is means attach all;
        ('cbAnalyseTaskState', CB_FUNCTYPE(c_int, C_LLONG, POINTER(NET_CB_ANALYSE_TASK_STATE_INFO), C_LDWORD)),  # 智能分析任务状态订阅函数;callback function of attach analyse state;
        ('dwUser', C_LDWORD),  # 用户数据;user data;
    ]

class NET_ANALYSE_RESULT_FILTER(Structure):
    """
    智能分析结果订阅的过滤条件
    filter condition of attach analyse result
    """
    _fields_ = [
        ('dwAlarmTypes', C_DWORD * 64),  # 过滤事件, 详见dhnetsdk.h中"智能分析事件类型";event types, see "intelligent analyse event type" in dhnetsdk.h;
        ('nEventNum', C_UINT),  # 过滤事件数量;number of events which are used as filter condition;
        ('nImageDataFlag', c_int),  # 是否包含图片, 0-包含,  1-不包含;need image, 0-need, 1-no;
        ('byReserved1', C_BYTE * 4),  # 对齐;alignment;
        ('nImageTypeNum', c_int),  # pImageType有效个数;pImageType valid num;
        ('pImageType', POINTER(C_ENUM)),  # 过滤上报的图片类型 Refer: EM_FILTER_IMAGE_TYPE;image data type Refer: EM_FILTER_IMAGE_TYPE;
        ('byReserved', C_BYTE * 1004),  # 保留字节;reserved bytes;
    ]

class NET_SECONDARY_ANALYSE_EVENT_INFO(Structure):
    """
    二次录像分析事件信息
    the event info of secondary record analysis
    """
    _fields_ = [
        ('emEventType', C_ENUM),  # 事件类型 Refer: EM_ANALYSE_EVENT_TYPE;event type Refer: EM_ANALYSE_EVENT_TYPE;
        ('byReserved1', C_BYTE * 4),  # 字节对齐;byte alignment;
        ('pstEventInfo', c_void_p),  # 事件信息, 根据emEventType确定不同的结构体;event info, determine the specific struct according to emEventType;
        ('byReserved', C_BYTE * 1024),  # 保留字节;reserved;
    ]

class NET_TASK_CUSTOM_DATA(Structure):
    """
    任务自定义数据
    Custorm data for task
    """
    _fields_ = [
        ('szClientIP', c_char * 128),  # 客户端IP;Client IP;
        ('szDeviceID', c_char * 128),  # 设备ID;Device ID;
        ('byReserved', C_BYTE * 256),  # 保留字节;Reserved;
    ]

class NET_ANALYSE_TASK_RESULT(Structure):
    """
    智能分析任务结果信息
    result of analyse task
    """
    _fields_ = [
        ('nTaskID', C_UINT),  # 任务ID;task ID;
        ('szFileID', c_char * 128),  # 文件ID, 分析文件时有效;file ID, used for file analyse;
        ('emFileAnalyseState', C_ENUM),  # 文件分析状态 Refer: EM_FILE_ANALYSE_STATE;file analyse state Refer: EM_FILE_ANALYSE_STATE;
        ('szFileAnalyseMsg', c_char * 256),  # 文件分析额外信息, 一般都是分析失败的原因;additional info about file analyse, usually it is failure info.;
        ('stuEventInfos', NET_SECONDARY_ANALYSE_EVENT_INFO * 8),  # 事件信息;info of events;
        ('nEventCount', c_int),  # 实际的事件个数;number of events;
        ('stuCustomData', NET_TASK_CUSTOM_DATA),  # 自定义数据;custorm data for task;
        ('szUserData', c_char * 64),  # 频源数据，标示视频源信息，对应addPollingTask中UserData字段。;user data.;
        ('szTaskUserData', c_char * 256),  # 任务数据;task user data;
        ('pstuEventInfosEx', POINTER(NET_SECONDARY_ANALYSE_EVENT_INFO)),  # 扩展事件信息;Extended event information;
        ('nRetEventInfoExNum', c_int),  # 返回扩展事件信息个数;Number of extended event information returned;
        ('szUserDefineData', c_char * 512),  # 用户定义数据，对应analyseTaskManager.analysePushPictureFileByRule中UserDefineData字段;User-defined data;
        ('byReserved', C_BYTE * 184),  # 保留字节;Reserved bytes;
    ]

class NET_CB_ANALYSE_TASK_RESULT_INFO(Structure):
    """
    智能分析任务结果回调信息
    callback info of analyse result
    """
    _fields_ = [
        ('stuTaskResultInfos', NET_ANALYSE_TASK_RESULT * 64),  # 智能分析任务结果信息;result of analyse tasks;
        ('nTaskResultNum', C_UINT),  # 任务个数;numbet of tasks;
        ('byReserved', C_BYTE * 1028),  # 保留字节;reserved bytes;
    ]

class NET_IN_ATTACH_ANALYSE_RESULT(Structure):
    """
    CLIENT_AttachAnalyseTaskResult 接口输入参数
    input parameter of CLIENT_AttachAnalyseTaskResult
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nTaskIDs', C_UINT * 64),  # 智能分析任务ID;task IDs;
        ('nTaskIdNum', C_UINT),  # 智能分析任务个数, 0表示订阅全部任务;number of tasks, 0 is means attach all;
        ('stuFilter', NET_ANALYSE_RESULT_FILTER),  # 过滤条件;filter confition;
        ('byReserved', C_BYTE * 4),  # 对齐;for alignment;
        ('cbAnalyseTaskResult', CB_FUNCTYPE(c_int, C_LLONG, POINTER(NET_CB_ANALYSE_TASK_RESULT_INFO), POINTER(c_char), C_DWORD, C_LDWORD)),  # 智能分析任务结果订阅函数;callback function of attach analyse result;
        ('dwUser', C_LDWORD),  # 用户数据;user data;
    ]

class NET_A_ALARM_EVENT_CROSSLINE_INFO(Structure):
    """
    警戒线事件(对应事件 EVENT_CROSSLINE_DETECTION)
    Warning line event (Corresponding to event  EVENT_CROSSLINE_DETECTION)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannelID', c_int),  # 通道号;Channel No.;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Time stamp (Unit is ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occurrence time;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('nEventAction', c_int),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event operation. 0=pulse event.1=continious event begin. 2=continuous event stop;
        ('emCrossDirection', C_ENUM),  # 入侵方向 Refer: EM_A_NET_CROSSLINE_DIRECTION_INFO;Intrusion direction Refer: EM_A_NET_CROSSLINE_DIRECTION_INFO;
        ('nOccurrenceCount', c_int),  # 规则被触发生次数;Triggered amount;
        ('nLevel', c_int),  # 事件级别,GB30147需求项;Event type;
        ('bIsObjectInfo', C_BOOL),  # 是否检测到物体信息;Target information detection enablement;
        ('stuObject', SDK_MSG_OBJECT),  # 检测到的物体信息;Object information detected;
        ('nRetObjectNum', c_int),  # 实际返回多个检测到的物体信息;Actually returns multiple detected object information;
        ('stuObjects', SDK_MSG_OBJECT * 100),  # 多个检测到的物体信息;Multiple detected object information;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_ALARM_EVENT_CROSSREGION_INFO(Structure):
    """
    警戒区事件(对应事件 EVENT_CROSSREGION_DETECTION)
    Warning zone event( Corresponding to event EVENT_CROSSREGION_DETECTION)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannelID', c_int),  # 通道号;Channel No.;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Time stamp (Unit is ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occurrence time;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('nEventAction', c_int),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event operation. 0=pulse event.1=continues event begin. 2=continuous event stop;
        ('emDirection', C_ENUM),  # 警戒区入侵方向 Refer: EM_A_NET_CROSSREGION_DIRECTION_INFO;Warning zone intrusion direction Refer: EM_A_NET_CROSSREGION_DIRECTION_INFO;
        ('emActionType', C_ENUM),  # 警戒区检测动作类型 Refer: EM_A_NET_CROSSREGION_ACTION_INFO;Detected types in the warning zone Refer: EM_A_NET_CROSSREGION_ACTION_INFO;
        ('nOccurrenceCount', c_int),  # 规则被触发生次数;Rule triggered amount;
        ('nLevel', c_int),  # 事件级别,GB30147需求项;Event type;
        ('szName', c_char * 128),  # 名称;name;
        ('bIsObjectInfo', C_BOOL),  # 是否检测到物体信息;Target information detection enablement;
        ('stuObject', SDK_MSG_OBJECT),  # 检测到的物体信息;Object information detected;
        ('nRetObjectNum', c_int),  # 实际返回多个检测到的物体信息;Actually returns multiple detected object information;
        ('stuObjects', SDK_MSG_OBJECT * 100),  # 多个检测到的物体信息;Multiple detected object information;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('szMac', c_char * 32),  # 事件触发源的Mac地址;Trigger type - 1: unknown 0: vehicle detector 1: radar 2: video;
        ('szReserved', c_char * 1024),  # 预留字节;Reserved;
    ]

class NET_A_ALARM_LOGIN_FAILIUR_INFO(Structure):
    """
    登陆失败事件
    login failed event
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nAction', c_int),  # 0:开始 1:停止;0:start 1:stop;
        ('nSequence', C_UINT),  # 序号;no.;
        ('szName', c_char * 128),  # 事件名,填用户名称;event name, fill in user name;
        ('szType', c_char * 128),  # 登录类型;login type;
        ('szAddr', c_char * 128),  # 来源IP地址;source IP address;
        ('nError', c_int),  # 用户登陆失败错误码;user login failed error code;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_IN_MATRIX_GET_CAMERAS(Structure):
    """
    CLIENT_MatrixGetCameras接口的输入参数
    CLIENT_MatrixGetCameras's interface input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),
    ]

class NET_SOURCE_STREAM_ENCRYPT(Structure):
    """
    显示源码流加密方式
    The encrypt of stream info
    """
    _fields_ = [
        ('emEncryptLevel', C_ENUM),  # 加密等级 Refer: EM_ENCRYPT_LEVEL;Encrypt level Refer: EM_ENCRYPT_LEVEL;
        ('emAlgorithm', C_ENUM),  # 加密算法 Refer: EM_ENCRYPT_ALGORITHM_TYPE;The type of stream encrypt algorithm Refer: EM_ENCRYPT_ALGORITHM_TYPE;
        ('emExchange', C_ENUM),  # 密钥交换方式 Refer: EM_KEY_EXCHANGE_TYPE;The type of exchange key Refer: EM_KEY_EXCHANGE_TYPE;
        ('bUnvarnished', C_BOOL),  # MTS使用场景,true为交互MIKEY后让数据不进行加/解密;MTS using scene,true is interacting with MIKEY and than donot encrypt data;
        ('szPSK', c_char * 1032),  # 密钥;key;
        ('byReserved', C_BYTE * 1024),  # 保留字节;Revered;
    ]

class NET_A_VIDEO_INPUTS(Structure):
    """
    视频输入通道信息
    channel info of video input
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szChnName', c_char * 64),  # 通道名称;channel name;
        ('bEnable', C_BOOL),  # 使能;enable;
        ('szControlID', c_char * 128),  # 控制ID;control ID;
        ('szMainStreamUrl', c_char * 260),  # 主码流url地址;main stream url;
        ('szExtraStreamUrl', c_char * 260),  # 辅码流url地址;extra stream url;
        ('nOptionalMainUrlCount', c_int),  # 备用主码流地址数量;spare main stream address quantity;
        ('szOptionalMainUrls', c_char * 2080),  # 备用主码流地址列表;spare main stream address list;
        ('nOptionalExtraUrlCount', c_int),  # 备用辅码流地址数量;spare sub stream address quantity;
        ('szOptionalExtraUrls', c_char * 2080),  # 备用辅码流地址列表;spare substream address list;
        ('szCaption', c_char * 32),  # 通道备注;caption;
        ('emServiceType', C_ENUM),  # 指码流传输的服务类型 Refer: EM_STREAM_TRANSMISSION_SERVICE_TYPE;service type Refer: EM_STREAM_TRANSMISSION_SERVICE_TYPE;
        ('stuSourceStreamEncrypt', NET_SOURCE_STREAM_ENCRYPT),  # 码流加密方式;The encrypt of stream info;
    ]

class NET_REMOTE_DEVICE_EX(Structure):
    """
    远程设备信息扩展
    info of remote device extend
    """
    _fields_ = [
        ('szPwdEx2', c_char * 128),  # 密码;password;
        ('bUsePwdEx2', C_BOOL),  # 是否使用szPwdEx2密码;use szPwdEx2 password;
        ('szIpEx', c_char * 64),  # IP;IP;
        ('bUseIpEx', C_BOOL),  # 是否使用szIpEx IP;use szIpEx IP;
        ('szReserved', c_char * 952),  # 保留字节;reserved;
    ]

class NET_A_REMOTE_DEVICE(Structure):
    """
    远程设备信息
    info of remote device
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('bEnable', C_BOOL),  # 使能;enable;
        ('szIp', c_char * 16),  # IP;IP;
        ('szUser', c_char * 8),  # 用户名,建议使用szUserEx;username;
        ('szPwd', c_char * 8),  # 密码,建议使用szPwdEx;password;
        ('nPort', c_int),  # 端口;port;
        ('nDefinition', c_int),  # 清晰度, 0-标清, 1-高清;definition. 0-standard definition, 1-high definition;
        ('emProtocol', C_ENUM),  # 协议类型 Refer: EM_A_DEVICE_PROTOCOL;protocol type Refer: EM_A_DEVICE_PROTOCOL;
        ('szDevName', c_char * 64),  # 设备名称;device name;
        ('nVideoInputChannels', c_int),  # 视频输入通道数;count channel of video input;
        ('nAudioInputChannels', c_int),  # 音频输入通道数;count channel of audio input;
        ('szDevClass', c_char * 32),  # 设备类型, 如IPC, DVR, NVR等;device type, such as IPC, DVR, NVR;
        ('szDevType', c_char * 32),  # 设备具体型号, 如IPC-HF3300;device type, such as IPC-HF3300;
        ('nHttpPort', c_int),  # Http端口;Http port;
        ('nMaxVideoInputCount', c_int),  # 视频输入通道最大数;max count of video input;
        ('nRetVideoInputCount', c_int),  # 返回实际通道个数;return count;
        ('pstuVideoInputs', POINTER(NET_A_VIDEO_INPUTS)),  # 视频输入通道信息,由用户申请内存，大小为sizeof(VIDEO_INPUTS)*nMaxVideoInputCount;max count of audion input, user malloc the memory,apply to sizeof(VIDEO_INPUTS)*nMaxVideoInputCount;
        ('szMachineAddress', c_char * 256),  # 设备部署地;machine address;
        ('szSerialNo', c_char * 48),  # 设备序列号;serial no.;
        ('nRtspPort', c_int),  # Rtsp端口;Rtsp Port;
        ('szUserEx', c_char * 32),  # 用户名;username;
        ('szPwdEx', c_char * 32),  # 密码，szPwdEx只支持31位密码长度，当密码需要大于等于32位时，使用pstuRemoteDevEx里的szPwdEx2;password,When the password needs to be greater than or equal to 32 bits, use szpwdex2 in pstuRemoteDevEx;
        ('szVendorAbbr', c_char * 32),  # 厂商缩写;vendor abbreviation;
        ('szSoftwareVersion', c_char * 64),  # 设备软件版本;software version;
        ('stuActivationTime', NET_TIME),  # 启动时间;activation time;
        ('szMac', c_char * 20),  # MAC地址;MAC;
        ('nHttpsPort', c_int),  # HttpsPort;HttpsPort;
        ('byReserved', C_BYTE * 4),  # 保留字段;Reserved;
        ('pstuRemoteDevEx', POINTER(NET_REMOTE_DEVICE_EX)),  # 用于REMOTE_DEVICE新增字段扩展,由用户申请内存，大小为sizeof(NET_REMOTE_DEVICE_EX);REMOTE_DEVICE extend,user malloc the memory,apply to sizeof(NET_REMOTE_DEVICE_EX);
    ]

class NET_A_MATRIX_CAMERA_INFO(Structure):
    """
    可用的显示源信息
    available according to the source of information
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szName', c_char * 128),  # 名称;name;
        ('szDevID', c_char * 128),  # 设备ID;device ID;
        ('szControlID', c_char * 128),  # 控制ID;control ID;
        ('nChannelID', c_int),  # 通道号, DeviceID设备内唯一;channel ID, DeviceID is unique;
        ('nUniqueChannel', c_int),  # 设备内统一编号的唯一通道号;unique channel;
        ('bRemoteDevice', C_BOOL),  # 是否远程设备;support remote device or not;
        ('stuRemoteDevice', NET_A_REMOTE_DEVICE),  # 远程设备信息;info of remote device;
        ('emStreamType', C_ENUM),  # 视频码流类型 Refer: EM_A_NET_STREAM_TYPE;stream type Refer: EM_A_NET_STREAM_TYPE;
        ('emChannelType', C_ENUM),  # 通道类型 Refer: EM_A_NET_LOGIC_CHN_TYPE;Channel Types Refer: EM_A_NET_LOGIC_CHN_TYPE;
        ('bEnable', C_BOOL),  # 仅在使用DeviceID添加/删除设备时的使能，通过DeviceInfo操作不要使用;Enable only when using DeviceID to add/remove a device, do not use it through DeviceInfo operation;
        ('emVideoStream', C_ENUM),  # 视频码流 Refer: EM_VIDEO_STREAM;Video stream Refer: EM_VIDEO_STREAM;
    ]

class NET_A_OUT_MATRIX_GET_CAMERAS(Structure):
    """
    CLIENT_MatrixGetCameras接口的输出参数
    CLIENT_MatrixGetCameras's interface output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('pstuCameras', POINTER(NET_A_MATRIX_CAMERA_INFO)),  # 显示源信息数组, 用户分配内存,大小为sizeof(MATRIX_CAMERA_INFO)*nMaxCameraCount;array;
        ('nMaxCameraCount', c_int),  # 显示源数组大小;size of source array,the space application by the user,apply to sizeof(MATRIX_CAMERA_INFO)*nMaxCameraCount;
        ('nRetCameraCount', c_int),  # 返回的显示源数量;return count;
    ]

class NET_CB_RTMP_MANAGER_INFO(Structure):
    """
    推送的数据内容
    Pushed data content
    """
    _fields_ = [
        ('nPushId', C_UINT),  # 推流ID;Push ID;
        ('emStatus', C_ENUM),  # 状态变化 Refer: EM_A_NET_EM_RTMP_MANAGER_STATUS;State change Refer: EM_A_NET_EM_RTMP_MANAGER_STATUS;
        ('emErrCode', C_ENUM),  # 错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;Error code Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;
        ('bReserved', C_BYTE * 256),  # 保留字段;Reserved;
    ]

class NET_CB_RTMP_STATUS_INFO(Structure):
    """
    回调函数RTMP状态信息
    Callback function RTMP status information
    """
    _fields_ = [
        ('nSID', C_UINT),  # 订阅id号;Subscription ID number;
        ('stuInfo', NET_CB_RTMP_MANAGER_INFO),  # 推送的数据内容;Pushed data content;
        ('bReserved', C_BYTE * 1024),  # 保留字段;Reserved;
    ]

class NET_IN_RTMP_MANAGER_ATTACH_STATUS(Structure):
    """
    CLIENT_AttachStatusRTMPManager入参
    CLIENT_AttachStatusRTMPManager Input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 要订阅的推流ID;Push ID;
        ('cbRTMPAttachStatusCallBack', CB_FUNCTYPE(c_int, C_LLONG, POINTER(NET_CB_RTMP_STATUS_INFO), C_LDWORD)),  # 入参回调函数;Parameter callback function;
        ('dwUser', C_LDWORD),  # 用户自定义参数;User defined parameters;
    ]

class NET_OUT_RTMP_MANAGER_ATTACH_STATUS(Structure):
    """
    CLIENT_AttachStatusRTMPManager出参
    CLIENT_AttachStatusRTMPManager Output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nSID', C_UINT),  # 订阅id号;Subscription ID number;
        ('emErrCode', C_ENUM),  # 错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;Error code Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;
    ]

class NET_IN_RTMP_MANAGER_DETACH_STATUS(Structure):
    """
    CLIENT_DetachStatusRTMPManager 入参
    CLIENT_DetachStatusRTMPManager Input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 要取消订阅的推流ID;Push ID;
    ]

class NET_OUT_RTMP_MANAGER_DETACH_STATUS(Structure):
    """
    CLIENT_DetachStatusRTMPManager出参
    CLIENT_DetachStatusRTMPManager Output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
    ]

class NET_IN_RTMP_MANAGER_GETPUSHINFOS(Structure):
    """
    CLIENT_GetPushInfosRTMPManager 接口入参
    CLIENT_GetPushInfosRTMPManager Interface input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
    ]

class NET_RTMP_MANAGER_PUSHINFOS(Structure):
    """
    已创建推流任务的信息
    Information of created streaming task
    """
    _fields_ = [
        ('nPushId', C_UINT),  # 推流ID;Push flow ID;
        ('emType', C_ENUM),  # 推流地址类型 Refer: EM_A_NET_EM_RTMP_MANAGER_ADD_TYPE;Streaming address type Refer: EM_A_NET_EM_RTMP_MANAGER_ADD_TYPE;
        ('emStatus', C_ENUM),  # 推流状态 Refer: EM_A_NET_EM_RTMP_MANAGER_STATUS;Push flow state Refer: EM_A_NET_EM_RTMP_MANAGER_STATUS;
        ('szReserved', c_char * 1028),  # 预留字节;Reserved;
    ]

class NET_OUT_RTMP_MANAGER_GETPUSHINFOS(Structure):
    """
    CLIENT_GetPushInfosRTMPManager 接口出参
    CLIENT_GetPushInfosRTMPManager Interface output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushInfosNum', c_int),  # 已创建推流任务的信息个数;Number of information created for streaming task;
        ('stuPushInfos', NET_RTMP_MANAGER_PUSHINFOS * 32),  # 已创建推流任务的信息;Information of created streaming task;
    ]

class NET_IN_MANUAL_SNAP(Structure):
    """
    CLIENT_ManualSnap 接口输入参数
    Input param of CLIENT_ManualSnap
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Struct size;
        ('nChannel', C_UINT),  # 抓图通道号;Capture channel number;
        ('nCmdSerial', C_UINT),  # 请求序列号;Serial number;
        ('szFilePath', c_char * 260),  # 抓图保存路径;Capture save path;
    ]

class NET_OUT_MANUAL_SNAP(Structure):
    """
    CLIENT_ManualSnap 接口输出参数
    Output param of CLIENT_ManualSnap
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Struct size;
        ('nMaxBufLen', C_UINT),  # pRcvBuf的长度,由用户指定;The length of pRcvBuf. Its value is specified by the user;
        ('pRcvBuf', POINTER(c_char)),  # 接收图片缓冲, 用于存放抓图数据, 空间由用户申请和释放, 申请大小为nMaxBufLen;Buffer of capture, It is Used to store snapshot data.The space is applied and released by the user, and the application size is nmaxbuflen.;
        ('nRetBufLen', C_UINT),  # 实际接收到的图片大小;Actual received picture size;
        ('emEncodeType', C_ENUM),  # 图片编码格式 Refer: EM_SNAP_ENCODE_TYPE;Picture encoding format Refer: EM_SNAP_ENCODE_TYPE;
        ('nCmdSerial', C_UINT),  # 请求序列号;Serial number;
        ('bReserved', C_BYTE * 4),  # 字节对齐;Byte alignment;
    ]

class NET_A_OPR_RIGHT_EX(Structure):
    """
    权限信息
    Right information
    """
    _fields_ = [
        ('dwID', C_DWORD),
        ('name', c_char * 32),
        ('memo', c_char * 32),
    ]

class NET_A_USER_GROUP_INFO_EX(Structure):
    """
    用户组信息
    User group information
    """
    _fields_ = [
        ('dwID', C_DWORD),
        ('name', c_char * 16),
        ('dwRightNum', C_DWORD),
        ('rights', C_DWORD * 100),
        ('memo', c_char * 32),
    ]

class NET_A_USER_INFO_EX(Structure):
    """
    用户信息
    User information
    """
    _fields_ = [
        ('dwID', C_DWORD),
        ('dwGroupID', C_DWORD),
        ('name', c_char * 16),
        ('passWord', c_char * 16),
        ('dwRightNum', C_DWORD),
        ('rights', C_DWORD * 100),
        ('memo', c_char * 32),
        ('dwFouctionMask', C_DWORD),  # 掩码,0x00000001 - 支持用户复用;Subnet mask,0x00000001 - support reuse;
        ('byReserve', C_BYTE * 32),
    ]

class NET_A_USER_MANAGE_INFO_EX(Structure):
    """
    用户信息表
    User information sheet
    """
    _fields_ = [
        ('dwRightNum', C_DWORD),  # 权限信息;Right information;
        ('rightList', NET_A_OPR_RIGHT_EX * 100),
        ('dwGroupNum', C_DWORD),  # 用户组信息;User group information;
        ('groupList', NET_A_USER_GROUP_INFO_EX * 20),
        ('dwUserNum', C_DWORD),  # 用户信息;User information;
        ('userList', NET_A_USER_INFO_EX * 200),
        ('dwFouctionMask', C_DWORD),  # 掩码；0x00000001 - 支持用户复用,0x00000002 - 密码修改需要校验;Subnet mask;0x00000001 - support reuse, 0x00000002 - Password has been modified , it needs to be verified.;
        ('byNameMaxLength', C_BYTE),  # 支持的用户名最大长度;The supported user name max length;
        ('byPSWMaxLength', C_BYTE),  # 支持的密码最大长度;The supported password max length;
        ('byReserve', C_BYTE * 254),
    ]

class NET_IN_ADD_ONVIF_USER_INFO(Structure):
    """
    添加Onvif用户，CLIENT_AddOnvifUser 入参
    Add Onvif User, CLIENT_AddOnvifUser Input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('szName', c_char * 128),  # 用户名;UserName;
        ('szPassword', c_char * 128),  # 密码;Password;
        ('emGroupType', C_ENUM),  # 用户所在的组 Refer: EM_GROUP_TYPE;User Group Refer: EM_GROUP_TYPE;
    ]

class NET_OUT_ADD_ONVIF_USER_INFO(Structure):
    """
    添加Onvif用户，CLIENT_AddOnvifUser 出参
    Add Onvif User, CLIENT_AddOnvifUser Output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_ONVIF_USER_INFO(Structure):
    """
    Onvif 新用户信息
    Onvif New user information
    """
    _fields_ = [
        ('szName', c_char * 128),  # 用户名;User name;
        ('szPassword', c_char * 128),  # 密码;password;
        ('stuPasswordModifiedTime', NET_TIME),  # 最近修改密码的时间;Recently modified password time;
        ('emGroupType', C_ENUM),  # 用户所在的组 Refer: EM_GROUP_TYPE;User Group Refer: EM_GROUP_TYPE;
        ('bReserved', C_BOOL),  # 用户是否为保留用户，保留用户不可删除;if the user keeps the user, the user must not be deleted;
        ('byReserved', C_BYTE * 512),  # 保留字节;reserved;
    ]

class NET_IN_MODIFYONVIF_USER_INFO(Structure):
    """
    修改 Onvif用户，CLIENT_ModifyOnvifUser 入参
    Modify onvif user, CLIENT_ModifyOnvifUser Entry parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('szName', c_char * 128),  # 需要修改的用户名称;User name that needs to be modified;
        ('stUserInfo', NET_ONVIF_USER_INFO),  # 新用户信息;New user information;
    ]

class NET_OUT_MODIFYONVIF_USER_INFO(Structure):
    """
    修改 Onvif用户，CLIENT_ModifyOnvifUser 出参
    Modify onvif user, CLIENT_ModifyOnvifUser Output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_IN_GETONVIF_USERINFO_ALL_INFO(Structure):
    """
    获取所有 Onvif 用户信息，CLIENT_GetOnvifUserInfoAll 入参
    Get all onvif user information, CLIENT_GetOnvifUserInfoAll Enter parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_OUT_GETONVIF_USERINFO_ALL_INFO(Structure):
    """
    获取所有 Onvif 用户信息， CLIENT_GetOnvifUserInfoAll 出参
    Get all onvif user information, CLIENT_GetOnvifUserInfoAll Output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nRetUserInfoNumber', c_int),  # 本次已查询到的个数;The number of this query;
        ('stuUserInfo', NET_ONVIF_USER_INFO * 20),  # 用户信息列表(无法获取到密码信息);User information list(unable to get password information);
    ]

class NET_IN_MODIFYONVIF_PASSWORD_INFO(Structure):
    """
    修改 Onvif 用户密码， CLIENT_ModifyOnvifUserPassword 入参
    Modify the Onvif user password, CLIENT_ModifyOnvifUserPassword Enter parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('szName', c_char * 128),  # 用户名称;User name;
        ('szPwd', c_char * 128),  # 用户密码;User password;
        ('szPwdOld', c_char * 128),  # 旧密码;old password;
    ]

class NET_OUT_MODIFYONVIF_PASSWORD_INFO(Structure):
    """
    修改 Onvif 用户密码，CLIENT_ModifyOnvifUserPassword 出参
    Modify the Onvif user password, CLIENT_ModifyOnvifUserPassword Output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_IN_RTMP_MANAGER_GETCAPS(Structure):
    """
    获取设备RTMP推流能力入参
    Get the RTMP streaming capability input parameter of the device
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
    ]

class NET_OUT_RTMP_MANAGER_GETCAPS(Structure):
    """
    获取设备RTMP推流能力出参
    Get the RTMP streaming capability input parameter of the device
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nMaxLive', C_UINT),  # 最大实时流推流通道数;Maximum number of real-time streaming channels;
        ('nMaxRecord', C_UINT),  # 最大录像流推流通道数;Maximum number of video streaming channels;
    ]

class NET_RTMP_MANAGER_LIVE_STREAM(Structure):
    """
    Type为0表示实时流时，需要填写
    If the type is 0, it means real-time flow, which needs to be filled in
    """
    _fields_ = [
        ('nChannel', c_int),  # 通道号;channel id;
        ('emStreamType', C_ENUM),  # 码流类型 Refer: EM_A_NET_EM_RTMP_MANAGER_STREAM_TYPE;stream type Refer: EM_A_NET_EM_RTMP_MANAGER_STREAM_TYPE;
        ('byReserved', C_BYTE * 1024),  # 预留字节;reserved;
    ]

class NET_RTMP_MANAGER_RECORD_STREAM(Structure):
    """
    Type为1表示回放流时，需要填写
    When type is 1, it means that it is required to fill in when playing back the stream
    """
    _fields_ = [
        ('szFilePath', c_char * 260),  # 录像文件路径;Video file path;
        ('szStartTime', c_char * 20),  # 录像开始时间;video start time;
        ('szEndTime', c_char * 20),  # 录像结束时间;video stop time;
        ('nChannel', c_int),  # 通道号;channel id;
        ('emStreamType', C_ENUM),  # 码流类型，默认为主码流 Refer: EM_A_NET_EM_RTMP_MANAGER_STREAM_TYPE;Code stream type. It is the main code stream by default Refer: EM_A_NET_EM_RTMP_MANAGER_STREAM_TYPE;
        ('byReserved', C_BYTE * 1024),  # 预留字节;reserved;
    ]

class NET_IN_RTMP_MANAGER_ADD(Structure):
    """
    添加推流地址入参
    Add streaming address input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('emType', C_ENUM),  # 添加推流地址类型 Refer: EM_A_NET_EM_RTMP_MANAGER_ADD_TYPE;Add streaming address type Refer: EM_A_NET_EM_RTMP_MANAGER_ADD_TYPE;
        ('stuLiveStream', NET_RTMP_MANAGER_LIVE_STREAM),  # Type为0表示实时流时，需要填写;If the type is 0, it means Live stream, which needs to be filled in;
        ('stuRecordStream', NET_RTMP_MANAGER_RECORD_STREAM),  # Type为1表示回放流时，需要填写;If the type is 1, it means Record stream, which needs to be filled in;
        ('szUrl', c_char * 512),  # 添加推流地址;Add streaming address;
    ]

class NET_OUT_RTMP_MANAGER_ADD(Structure):
    """
    添加推流地址出参
    Add streaming address output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 添加成功返回推流ID，失败时填0;The push stream ID is returned after adding successfully, and 0 is filled in if it fails;
        ('emErrCode', C_ENUM),  # Add 表示错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ADD_ERRCODE;Add Indicates the error code Refer: EM_A_NET_EM_RTMP_MANAGER_ADD_ERRCODE;
    ]

class NET_IN_RTMP_MANAGER_REMOVE(Structure):
    """
    删除推流地址入参
    Delete streaming address input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 要删除的推流ID;Push ID;
    ]

class NET_OUT_RTMP_MANAGER_REMOVE(Structure):
    """
    删除推流地址出参
    Delete streaming address output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('emErrCode', C_ENUM),  # 错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;Error code Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;
    ]

class NET_IN_RTMP_MANAGER_START(Structure):
    """
    启动推流入参
    Start push in parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 要启动的推流ID;Push ID;
    ]

class NET_OUT_RTMP_MANAGER_START(Structure):
    """
    启动推流出参
    Start push out parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('emErrCode', C_ENUM),  # 错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;Error code Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;
    ]

class NET_IN_RTMP_MANAGER_STOP(Structure):
    """
    停止推流入参
    Stop pushing input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 要停止的推流ID;Push ID;
    ]

class NET_OUT_RTMP_MANAGER_STOP(Structure):
    """
    停止推流出参
    Stop pushing out parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('emErrCode', C_ENUM),  # 错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;Error code Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;
    ]

class NET_IN_RTMP_MANAGER_PAUSE(Structure):
    """
    暂停推流入参
    Pause push in parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 要暂停的推流ID;Push ID;
    ]

class NET_OUT_RTMP_MANAGER_PAUSE(Structure):
    """
    暂停推流出参
    Pause pushing out parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('emErrCode', C_ENUM),  # 错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;Error code Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;
    ]

class NET_IN_RTMP_MANAGER_RESUME(Structure):
    """
    恢复推流入参
    Resume push in parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 要恢复的推流ID;Push ID;
    ]

class NET_OUT_RTMP_MANAGER_RESUME(Structure):
    """
    恢复推流出参
    Resume push out parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('emErrCode', C_ENUM),  # 错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;Error code Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;
    ]

class NET_IN_RTMP_MANAGER_SET_SPEED(Structure):
    """
    设置倍速推流入参
    Set the double speed push parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nPushId', C_UINT),  # 要恢复的推流ID;Push ID;
        ('dbSpeed', c_double),  # 播放速度，正数表示正向播放，负数表示反向播放，数据表示倍数;Playback speed: >0:indicates forward playback, <0:indicates reverse playback,data indicates multiple;
    ]

class NET_OUT_RTMP_MANAGER_SET_SPEED(Structure):
    """
    设置倍速推流出参
    Set double speed push out parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('emErrCode', C_ENUM),  # 错误码 Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;Error code Refer: EM_A_NET_EM_RTMP_MANAGER_ERRCODE;
    ]

class NET_SCREEN_SHOW_INFO(Structure):
    """
    屏幕信息
    Screen information
    """
    _fields_ = [
        ('nScreenNo', C_UINT),  # 屏幕编号;Screen no;
        ('szText', c_char * 256),  # 显示文本(文本类型为EM_SCREEN_TEXT_TYPE_LOCAL_TIME时的时间格式,%Y 年%M 月%D 日%H 时(24小时机制)%h 时(12小时)%m 分%S 秒%W 星期%T 显示上午或下午%X 表示显示普通文本内容;
                              # Display text (time format for text type EM_SCREEN_TEXT_TYPE_LOCAL_TIME,%Y Year%M months%D day%H 24-hour mechanism%h 12 hours%m min%S seconds%W week%T  shows morning or afternoon%X means to display normal text content;
        ('emTextType', C_ENUM),  # 文本类型 Refer: EM_SCREEN_TEXT_TYPE;Text type Refer: EM_SCREEN_TEXT_TYPE;
        ('emTextColor', C_ENUM),  # 文本颜色 Refer: EM_SCREEN_TEXT_COLOR;Text color Refer: EM_SCREEN_TEXT_COLOR;
        ('emTextRollMode', C_ENUM),  # 文本滚动模式 Refer: EM_SCREEN_TEXT_ROLL_MODE;Text roll mode Refer: EM_SCREEN_TEXT_ROLL_MODE;
        ('nRollSpeed', C_UINT),  # 文本滚动速度由慢到快分为1~5;Text scrolling speed is divided into 1 ~ 5 from slow to fast;
        ('byReserved', C_BYTE * 252),  # 保留字节;Reserved;
    ]

class NET_BROADCAST_INFO(Structure):
    """
    播报信息
    Broadcast information
    """
    _fields_ = [
        ('szText', c_char * 256),  # 语音文本;Voice text;
        ('emTextType', C_ENUM),  # 文本类型 Refer: EM_BROADCAST_TEXT_TYPE;Text type Refer: EM_BROADCAST_TEXT_TYPE;
        ('byReserved', C_BYTE * 252),  # 保留字节;Reserved;
    ]

class NET_IN_SET_PARK_CONTROL_INFO(Structure):
    """
    设置停车控制信息(点阵屏和语音播报的控制) CLIENT_ControlDeviceEx入参(对应 CTRL_SET_PARK_CONTROL_INFO )
    Set parking control information(Control of dot matrix screen and voice broadcast) CLIENT_ControlDeviceEx in parameters (corresponding to CTRL_SET_PARK_CONTROL_INFO )
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Struct size;
        ('nScreenShowInfoNum', c_int),  # 屏幕信息个数;Number of screen control information;
        ('stuScreenShowInfo', NET_SCREEN_SHOW_INFO * 16),  # 屏幕信息;Screen control information;
        ('byReserved', C_BYTE * 4),  # 字节补齐;Byte completion;
        ('nBroadcastInfoNum', c_int),  # 播报信息个数;Number of broadcast control information;
        ('stuBroadcastInfo', NET_BROADCAST_INFO * 16),  # 播报信息;Broadcast control information;
    ]

class NET_OUT_SET_PARK_CONTROL_INFO(Structure):
    """
    设置停车控制信息(点阵屏和语音播报的控制) CLIENT_ControlDeviceEx出参(对应 CTRL_SET_PARK_CONTROL_INFO)
    Set parking control information(Control of dot matrix screen and voice broadcast) CLIENT_ControlDeviceEx out parameters (corresponding to CTRL_SET_PARK_CONTROL_INFO )
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Struct size;
    ]

class NET_CTRL_SET_PARK_INFO(Structure):
    """
    设置停车信息,对应CTRL_SET_PARK_INFO命令参数
    Set park info, corresponding CTRL_SET_PARK_INFO command parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szPlateNumber', c_char * 64),  # 车牌号码;Plate number;
        ('nParkTime', C_UINT),  # 停车时长,单位:分钟;park time,Unit:minute;
        ('szMasterofCar', c_char * 32),  # 车主姓名;Main of car;
        ('szUserType', c_char * 32),  # 用户类型,非通用,用于出入口抓拍一体机monthlyCardUser表示月卡用户,yearlyCardUser表示年卡用户,longTimeUser表示长期用户,casualUser表示临时用户/Visitor;User type,not general,Used in entrance capture machinemonthlyCardUser means monthly card user,yearlyCardUser means yearly card user,longTimeUser means long time user,casualUser means casual user/Visitor;
        ('nRemainDay', C_UINT),  # 到期天数;Remain day;
        ('szParkCharge', c_char * 32),  # 停车费;Park charge;
        ('nRemainSpace', C_UINT),  # 停车库余位数;Remain space;
        ('nPassEnable', C_UINT),  # 0:不允许车辆通过 1:允许车辆通过;0:car is not allowed to pass,1:car is allowed to pass;
        ('stuInTime', NET_TIME),  # 车辆入场时间;car in time;
        ('stuOutTime', NET_TIME),  # 车辆出场时间;car out time;
        ('emCarStatus', C_ENUM),  # 过车状态 Refer: EM_CARPASS_STATUS;car pass status Refer: EM_CARPASS_STATUS;
        ('szCustom', c_char * 128),  # 自定义显示字段，默认空;custom field,default:null;
        ('szSubUserType', c_char * 64),  # 用户类型（szUserType字段）的子类型;Sub user type of szUserType;
        ('szRemarks', c_char * 64),  # 备注信息;Remarks info;
        ('szResource', c_char * 64),  # 资源文件（视频或图片）视频支持:mp4格式; 图片支持:BMP/jpg/JPG/jpeg/JPEG/png/PNG格式;Resource file(video or picture) video support:mp4; picture support:BMP/jpg/JPG/jpeg/JPEG/png/PNG;
        ('nParkTimeout', C_UINT),  # 停车超时时间，单位分钟。为0表示未超时，不为0表示超时时间。;Parking timeout, in minutes. A value of 0 means no timeout, and a value of not 0 means timeout.;
    ]

class NET_A_OPR_RIGHT_NEW(Structure):
    """
    权限信息
    Rights info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('dwID', C_DWORD),
        ('name', c_char * 32),
        ('memo', c_char * 32),
    ]

class NET_A_USER_GROUP_INFO_NEW(Structure):
    """
    用户组信息
    User group info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('dwID', C_DWORD),
        ('name', c_char * 16),
        ('dwRightNum', C_DWORD),
        ('rights', C_DWORD * 1024),
        ('memo', c_char * 32),
    ]

class NET_A_USER_INFO_NEW(Structure):
    """
    用户信息
    User info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('dwID', C_DWORD),
        ('dwGroupID', C_DWORD),
        ('name', c_char * 128),
        ('passWord', c_char * 128),
        ('dwRightNum', C_DWORD),
        ('rights', C_DWORD * 1024),
        ('memo', c_char * 32),
        ('dwFouctionMask', C_DWORD),  # 掩码,0x00000001 - 支持用户复用;Sub mask,0x00000001 - Support account reusable;
        ('stuTime', NET_TIME),  # 最后修改时间;Last Revise Time;
        ('byIsAnonymous', C_BYTE),  # 是否可以匿名登录, 0:不可匿名登录, 1: 可以匿名登录;Whether Can Be Anonymous Login,0=Can't Be Anonymous Login,1=Can be Anonymous Login;
        ('byReserve', C_BYTE * 7),
    ]

class NET_A_USER_GROUP_INFO_EX2(Structure):
    """
    用户组信息扩展,用户组名加长
    user group information expand,user group lengthen
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('dwID', C_DWORD),
        ('name', c_char * 128),
        ('dwRightNum', C_DWORD),
        ('rights', C_DWORD * 1024),
        ('memo', c_char * 32),
    ]

class NET_A_USER_MANAGE_INFO_NEW(Structure):
    """
    用户信息表
    User info list
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('dwRightNum', C_DWORD),  # 权限信息;Rights info;
        ('rightList', NET_A_OPR_RIGHT_NEW * 1024),
        ('dwGroupNum', C_DWORD),  # 用户组数;User group info;
        ('groupList', NET_A_USER_GROUP_INFO_NEW * 20),  # 用户组信息,此参数废弃,请使用groupListEx;
        ('dwUserNum', C_DWORD),  # 用户信息;User info;
        ('userList', NET_A_USER_INFO_NEW * 200),
        ('dwFouctionMask', C_DWORD),  # 掩码；0x00000001 - 支持用户复用,0x00000002 - 密码修改需要校验;Sub mask; 0x00000001 - Support account reusable,0x00000002 - Verification needed when change password;
        ('byNameMaxLength', C_BYTE),  # 支持的用户名最大长度;Max user name length supported;
        ('byPSWMaxLength', C_BYTE),  # 支持的密码最大长度;Max password length supported;
        ('byReserve', C_BYTE * 254),
        ('groupListEx', NET_A_USER_GROUP_INFO_EX2 * 20),  # 用户组信息扩展;User Group Information Expand;
    ]

class NET_ALARM_SAFETY_ABNORMAL_INFO(Structure):
    """
    安全报警事件(对应 ALARM_SAFETY_ABNORMAL)
    Safety Abnormal alarm info(corresponding to ALARM_SAFETY_ABNORMAL)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('nAction', c_int),  # 事件动作, 0: 脉冲;Event Action 0:Pulse;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间;The time when the event occurred;
        ('emExceptionType', C_ENUM),  # 异常事件类型 Refer: EM_EXCEPTION_TYPE;Exception Type Refer: EM_EXCEPTION_TYPE;
        ('szAddress', c_char * 64),  # 来源IP地址;Source IP address;
        ('stuAbnormalTime', NET_TIME),  # 发生异常时间;Abnormal time;
        ('szUser', c_char * 128),  # 发生的用户名;User;
        ('szReserved', c_char * 1024),  # 保留字节;Reserved bytes;
    ]

class NET_CTRL_RECORDSET_INSERT_IN(Structure):
    """
    记录集新增操作(insert)输入参数
    New Record Set Operation(Insert)Parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('emType', C_ENUM),  # 记录集信息类型 Refer: EM_NET_RECORD_TYPE;Record Information Type Refer: EM_NET_RECORD_TYPE;
        ('pBuf', c_void_p),  # 记录集信息缓存,详见EM_NET_RECORD_TYPE注释，由用户申请内存.;Record Information Cache,The EM_NET_RECORD_TYPE Note is Details,the space application by the user;
        ('nBufLen', c_int),  # 记录集信息缓存大小,大小参照记录集信息类型对应的结构体;Record Information Cache Size,please refer to the structure of EM_NET_RECORD_TYPE;
    ]

class NET_CTRL_RECORDSET_INSERT_OUT(Structure):
    """
    记录集新增操作(insert)输出参数
    Record New Operation(Insert) Parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nRecNo', c_int),  # 记录编号(新增insert时设备返回);Record Number(The Device Come Back When New Insert );
    ]

class NET_CTRL_RECORDSET_INSERT_PARAM(Structure):
    """
    记录集新增操作(insert)参数
    Record New Operation (Insert)Parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('stuCtrlRecordSetInfo', NET_CTRL_RECORDSET_INSERT_IN),  # 记录集信息(用户填写);Record Information(User Write);
        ('stuCtrlRecordSetResult', NET_CTRL_RECORDSET_INSERT_OUT),  # 记录集信息(设备返回);Record Information(the Device Come Back);
    ]

class NET_A_FIND_RECORD_ACCESSCTLCARD_CONDITION(Structure):
    """
    门禁卡记录查询条件
    Entrance Card Record Query Conditions
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szCardNo', c_char * 32),  # 卡号;Card Number;
        ('szUserID', c_char * 32),  # 用户ID;User ID;
        ('bIsValid', C_BOOL),  # 是否有效, TRUE:有效,FALSE:无效;Whether effective, TRUE: effective, FALSE: invalid;
        ('abCardNo', C_BOOL),  # 卡号查询条件是否有效,针对成员 szCardNo;Card inquire condition effects or not, for member szCardNo;
        ('abUserID', C_BOOL),  # 用户ID查询条件是否有效,针对成员 szUserID;User ID inquire condition effects or not, for member  szUserID;
        ('abIsValid', C_BOOL),  # IsValid查询条件是否有效,针对成员 bIsValid;IsValid inquire condition effects or not, for member  bIsValid;
    ]

class NET_ACCESSCTLCARD_FINGERPRINT_PACKET(Structure):
    """
    数据，只用于下发信息
    data, for sending only
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nLength', c_int),  # 单个数据包长度,单位字节;length of a finger print packet, unit: byte;
        ('nCount', c_int),  # 包个数;packet number;
        ('pPacketData', POINTER(c_char)),  # 所有数据包，用户申请内存并填充，长度为 nLength*nCount;all packet in a single buffer, allocated and filled by user, nLength*nCount bytes;
    ]

class NET_ACCESSCTLCARD_FINGERPRINT_PACKET_EX(Structure):
    """
    数据扩展，可用于下发和获取信息
    data, for sending and receiving
    """
    _fields_ = [
        ('nLength', c_int),  # 单个数据包长度,单位字节;length of a finger print packet, unit: byte;
        ('nCount', c_int),  # 包个数;packet number;
        ('pPacketData', POINTER(c_char)),  # 所有数据包, 用户申请内存,大小至少为nLength * nCount;all packet in a single buffer, allocated by user,the space application is over nLength * nCount;
        ('nPacketLen', c_int),  # pPacketData 指向内存区的大小，用户填写;pPacketData buffer length, set by user;
        ('nRealPacketLen', c_int),  # 返回给用户实际总大小;The actual size returned to the user, equal to nLength*nCount;
        ('nDuressIndex', c_int),  # 胁迫序号，范围1~nCount;duress index of group, range: 1~nCount;
        ('byReverseed', C_BYTE * 1020),  # 保留大小;Reserved size;
    ]

class NET_FLOORS_INFO(Structure):
    """
    楼层号
    Floor number (elevator control requirements)
    """
    _fields_ = [
        ('nFloorNumEx2', c_int),  # 有效的楼层数量再次扩展;The number of effective floors expanded again;
        ('szFloorEx', c_char * 2048),  # 楼层号,最多不超过256个，楼层号不超过999;Floor numbers, no more than 256, floor numbers no more than 999;
        ('byReserved', C_BYTE * 512),  # 保留字节;Reserved byte;
    ]

class NET_RECORDSET_ACCESS_CTL_CARD(Structure):
    """
    门禁卡记录集信息
    Access Control Card Info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nRecNo', c_int),  # 记录集编号,只读;Record Number,Read-Only;
        ('stuCreateTime', NET_TIME),  # 创建时间;Creat Time;
        ('szCardNo', c_char * 32),  # 卡号;Card number;
        ('szUserID', c_char * 32),  # 用户ID, 设备暂不支持;User's ID;
        ('emStatus', C_ENUM),  # 卡状态 Refer: EM_A_NET_ACCESSCTLCARD_STATE;Card Stetue Refer: EM_A_NET_ACCESSCTLCARD_STATE;
        ('emType', C_ENUM),  # 卡类型 Refer: EM_A_NET_ACCESSCTLCARD_TYPE;Card Type Refer: EM_A_NET_ACCESSCTLCARD_TYPE;
        ('szPsw', c_char * 64),  # 卡密码;Card Password;
        ('nDoorNum', c_int),  # 有效的门数目;;Valid Door Number;;
        ('sznDoors', c_int * 32),  # 有权限的门序号,即CFG_CMD_ACCESS_EVENT配置的数组下标;Privileged Door Number,That is CFG_CMD_ACCESS_EVENT Configure Array Subscript;
        ('nTimeSectionNum', c_int),  # 有效的的开门时间段数目;the Number of Effective Open Time;
        ('sznTimeSectionNo', c_int * 32),  # 开门时间段索引,即CFG_ACCESS_TIMESCHEDULE_INFO的数组下标;Open Time Segment Index,That is CFG_ACCESS_TIMESCHEDULE_INFO Array subscript;
        ('nUserTime', c_int),  # 使用次数,仅当来宾卡时有效;Frequency of Use;
        ('stuValidStartTime', NET_TIME),  # 开始有效期, 设备暂不支持时分秒;Valid Start Time;
        ('stuValidEndTime', NET_TIME),  # 结束有效期, 设备暂不支持时分秒;Valid End Time;
        ('bIsValid', C_BOOL),  # 是否有效,TRUE有效;FALSE无效;Wether Valid,True =Valid,False=Invalid;
        ('stuFingerPrintInfo', NET_ACCESSCTLCARD_FINGERPRINT_PACKET),  # 下发数据信息，仅为兼容性保留，请使用 stuFingerPrintInfoEx;data info (send only), DEPRECATED! use stuFingerPrintInfoEx instead;
        ('bFirstEnter', C_BOOL),  # 是否拥有首卡权限;has first card or not;
        ('szCardName', c_char * 64),  # 卡命名;card naming;
        ('szVTOPosition', c_char * 64),  # 门口机关联位置;VTO link position;
        ('bHandicap', C_BOOL),  # 是否为残障人士卡;Card for handicap, TRUE:yes, FALSE:no;
        ('bEnableExtended', C_BOOL),  # 启用成员 stuFingerPrintInfoEx;Enabled member stuFingerPrintInfoEx;
        ('stuFingerPrintInfoEx', NET_ACCESSCTLCARD_FINGERPRINT_PACKET_EX),  # 数据信息; data info structure;
        ('nFaceDataNum', c_int),  # 人脸数据个数不超过20;face detection data number,can not > 20;
        ('szFaceData', c_char * 40960),  # 人脸模版数据;face detection data;
        ('szDynamicCheckCode', c_char * 16),  # 动态校验码。VTO等设备会保存此校验码，以后每次刷卡都以一定的算法生成新校验码并写入IC卡中，同时更新VTO设备的校验码，只有卡号和此校验码同时验证通过时才可开门。缺点：目前方案只支持一卡刷一个设备。;dynamic check code;
        ('nRepeatEnterRouteNum', c_int),  # 反潜路径个数;repeat enter route num;
        ('arRepeatEnterRoute', c_int * 12),  # 反潜路径;repeat enter route;
        ('nRepeatEnterRouteTimeout', c_int),  # 反潜超时时间;repeat enter route timeout;
        ('bNewDoor', C_BOOL),  # 是否启动新开门授权字段，TRUE表示使用nNewDoorNum和nNewDoors字段下发开门权限;enable to new field, TRUE: user nNewDoorNum,nNewDoors;
        ('nNewDoorNum', c_int),  # 有效的门数目;;Valid Door Number;;
        ('nNewDoors', c_int * 128),  # 有权限的门序号,即CFG_CMD_ACCESS_EVENT配置的数组下标;Privileged Door Number, That is CFG_CMD_ACCESS_EVENT Configure Array Subscript;
        ('nNewTimeSectionNum', c_int),  # 有效的的开门时间段数目;the Number of Effective Open Time;
        ('nNewTimeSectionNo', c_int * 128),  # 开门时间段索引,即CFG_ACCESS_TIMESCHEDULE_INFO的数组下标;Open Time Segment Index,That is CFG_ACCESS_TIMESCHEDULE_INFO Array subscript;
        ('szCitizenIDNo', c_char * 32),  # 证件号码;ID card no;
        ('nSpecialDaysScheduleNum', c_int),  # 假日计划表示数量;SpecialDaysSchedule Number;
        ('arSpecialDaysSchedule', c_int * 128),  # 假日计划标识;SpecialDaysSchedule Identification;
        ('nUserType', C_UINT),  # 用户类型, 0 普通用户, 1 禁止名单用户;user type, 0:common, 1:blocklist;
        ('nFloorNum', c_int),  # 有效的楼层数量;floor number;
        ('szFloorNo', c_char * 256),  # 楼层号;floor;
        ('szSection', c_char * 64),  # 部门名称;Section name;
        ('nScore', c_int),  # 信用积分;credit score;
        ('szCompanyName', c_char * 200),  # 单位名称;company name;
        ('nSectionID', C_UINT),  # 部门ID;Section ID;
        ('emSex', C_ENUM),  # 性别 Refer: EM_A_NET_ACCESSCTLCARD_SEX;sex Refer: EM_A_NET_ACCESSCTLCARD_SEX;
        ('szRole', c_char * 32),  # 角色;Role;
        ('szProjectNo', c_char * 32),  # 项目ID;project No.;
        ('szProjectName', c_char * 64),  # 项目名称;project name;
        ('szBuilderName', c_char * 64),  # 施工单位全称;builder name;
        ('szBuilderID', c_char * 32),  # 施工单位ID;builder ID;
        ('szBuilderType', c_char * 32),  # 施工单位类型;builder type;
        ('szBuilderTypeID', c_char * 8),  # 施工单位类别ID;builder type ID;
        ('szPictureID', c_char * 64),  # 人员照片ID;picture ID;
        ('szContractID', c_char * 16),  # 原合同系统合同编号;contract ID in original contract system;
        ('szWorkerTypeID', c_char * 8),  # 工种ID;worker type ID;
        ('szWorkerTypeName', c_char * 32),  # 工种名称;worker type name;
        ('bPersonStatus', C_BOOL),  # 人员状态, TRUE:启用, FALSE:禁用;person status, TRUE:enable, FALSE:forbidden;
        ('emAuthority', C_ENUM),  # 用户权限 Refer: EM_A_NET_ACCESSCTLCARD_AUTHORITY;user authority Refer: EM_A_NET_ACCESSCTLCARD_AUTHORITY;
        ('szCompanionName', c_char * 120),  # 陪同人姓名;name of companion;
        ('szCompanionCompany', c_char * 200),  # 陪同人单位;company of companion;
        ('stuTmpAuthBeginTime', NET_TIME),  # 临时授权开始时间,当该时间和其他时间同时生效时，以此时间为最高优先级;temporary auth begin Time,high priority;
        ('stuTmpAuthEndTime', NET_TIME),  # 临时授权结束时间,当该时间和其他时间同时生效时，以此时间为最高优先级;temporary auth end Time,high priority;
        ('bFloorNoExValid', C_BOOL),  # 楼层号扩展 szFloorNoEx 是否有效;is szFloorNoEx valid, TRUE:valid, else invalid;
        ('nFloorNumEx', c_int),  # 有效的楼层数量扩展;floor number extended;
        ('szFloorNoEx', c_char * 2048),  # 楼层号扩展;floor info;
        ('szSubUserID', c_char * 32),  # 用户ID;sub user id;
        ('szPhoneNumber', c_char * 32),  # 人员电话号码;phone number;
        ('szPhotoPath', c_char * 256),  # 人员照片对应在ftp上的路径;photo path;
        ('szCause', c_char * 64),  # 来访原因;cause for visit;
        ('szCompanionCard', c_char * 32),  # 陪同人员证件号;companion card;
        ('szCitizenAddress', c_char * 128),  # 证件地址;citizen address;
        ('stuBirthDay', NET_TIME),  # 出生日期（年月日有效）;birth day (year month day are valid);
        ('bFloorNoEx2Valid', C_BOOL),  # stuFloors2 是否有效;Is stuFloorsEx2 valid;
        ('pstuFloorsEx2', POINTER(NET_FLOORS_INFO)),  # 楼层号（再次扩展）;Floor number (extended again);
        ('szDefaultFloor', c_char * 8),  # 默认楼层号;Default floor number;
        ('nUserTimeSectionNum', c_int),  # 用户时间段有效个数;Number of valid user time periods;
        ('szUserTimeSections', c_char * 120),  # 针对用户自身的开门时间段校验，最多支持6个时间段;Check the user's own door opening time zone, supporting up to 6 time zones;
        ('szWorkClass', c_char * 256),  # 工作班别;Work class;
        ('stuStartTimeInPeriodOfValidity', NET_TIME),  # 有效时间段内启动时间;Start time in valid time period;
        ('emTestItems', C_ENUM),  # 测试项目 Refer: EM_TEST_ITEMS;Test items Refer: EM_TEST_ITEMS;
        ('nAuthOverdueTime', C_UINT),  # 授权时间、过期时间，时间单位: 小时;Authorization time, expiration time, time unit: hour;
        ('emGreenCNHealthStatus', C_ENUM),  # 人员健康状态 Refer: EM_GREENCNHEALTH_STATUS;Staff health status Refer: EM_GREENCNHEALTH_STATUS;
        ('emAllowPermitFlag', C_ENUM),  # 电子通行证状态 Refer: EM_ALLOW_PERMIT_FLAG;E-pass status Refer: EM_ALLOW_PERMIT_FLAG;
        ('emRentState', C_ENUM),  # 对接第三方平台数据 Refer: EM_RENT_STATE;Connect to third-party platform data, Refer: EM_RENT_STATE;
        ('nConsumptionTimeSectionsNum', c_int),  # 用户消费时间段;User consumption period;
        ('szConsumptionTimeSections', c_char * 42 * 34),    # 消费时间段.每天最多6个时间段，每6个元素对应一天。一共7天;每个时段格式为"星期 时:分:秒-时:分:秒 消费类型 可消费次数 可消费金额";Consumption period There are up to 6 time periods per day, and every 6 elements correspond to one day. 7 days in total;The format of each period is "week hour: minute: second hour: minute: second consumption type consumable times consumable amount";
    ]

class NET_A_ALARM_ACCESS_CTL_EVENT_INFO(Structure):
    """
    门禁事件
    access control event
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nDoor', c_int),  # 门通道号;Door Channel Number;
        ('szDoorName', c_char * 128),  # 门禁名称;Entrance Guard Name;
        ('stuTime', NET_TIME),  # 报警事件发生的时间;Alarm Event Triggered Time;
        ('emEventType', C_ENUM),  # 门禁事件类型 Refer: EM_A_NET_ACCESS_CTL_EVENT_TYPE;Entrance Guard Event Type Refer: EM_A_NET_ACCESS_CTL_EVENT_TYPE;
        ('bStatus', C_BOOL),  # 刷卡结果,TRUE表示成功,FALSE表示失败;Swing Card Result,True is Success,False is Fail;
        ('emCardType', C_ENUM),  # 卡类型 Refer: EM_A_NET_ACCESSCTLCARD_TYPE;Card Type Refer: EM_A_NET_ACCESSCTLCARD_TYPE;
        ('emOpenMethod', C_ENUM),  # 开门方式 Refer: EM_A_NET_ACCESS_DOOROPEN_METHOD;Open The Door Method Refer: EM_A_NET_ACCESS_DOOROPEN_METHOD;
        ('szCardNo', c_char * 32),  # 卡号;Card Number;
        ('szPwd', c_char * 64),  # 密码;Password;
        ('szReaderID', c_char * 32),  # 门读卡器ID;Reader ID;
        ('szUserID', c_char * 64),  # 开门用户;unlock user;
        ('szSnapURL', c_char * 256),  # 抓拍照片存储地址;snapshot picture storage address;
        ('nErrorCode', c_int),  # 开门操作码，配合 bStatus 使用0x00 没有错误0x10 未授权0x11 卡挂失或注销0x12 没有该门权限0x13 开门模式错误0x14 有效期错误0x15 防反潜模式0x16 胁迫报警未打开0x17 门常闭状态0x18 AB互锁状态0x19 巡逻卡0x1A 设备处于闯入报警状态0x20 时间段错误0x21 假期内开门时间段错误0x23 卡逾期0x30 需要先验证有首卡权限的卡片0x40 卡片正确,输入密码错误0x41 卡片正确,输入密码超时0x42 卡片正确,输入错误0x43 卡片正确,输入超时0x44 正确,输入密码错误0x45 正确,输入密码超时0x50 组合开门顺序错误0x51 组合开门需要继续验证0x60 验证通过,控制台未授权0x61 卡片正确,人脸错误0x62 卡片正确,人脸超时0x63 重复进入0x64 未授权,需要后端平台识别0x65 温度过高0x66 未戴口罩0x67 健康码获取失败0x68 黄码禁止通行0x69 红码禁止通行0x6a 健康码无效0x6b 绿码验证通过0x6e 绿码,行程码非绿码0x6f 绿码 获取健康码信息0x71 校验证件信息（平台下发对应证件号的校验结果）0xA8 未佩戴安全帽 0xB1 授权信息不足，待补充;
                              # Open door operate code, use with bStatus0x00 no error0x10 unauthorized0x11 card lost or cancelled0x12 no door right0x13 unlock mode error0x14 valid period error0x15 anti sneak into mode0x16 forced alarm not unlocked0x17 door NC status0x18 AB lock status0x19 patrol card0x1A device is under intrusion alarm status0x20 period error0x21 unlock period error in holiday period0x23 Card is overdue0x30 first card right check required0x40 card correct, input password error0x41 card correct, input password timed out0x42 card correct, input error0x43 card correct, input timed out0x44 correct, input password error0x45 correct, input password timed out0x50 group unlock sequence error0x51 test required for group unlock0x60 test passed, control unauthorized0x61 card correct, face error0x62 card correct,face timeout0x63 repeat enter0x64 unauthorized, requiring back-end platform identification0x65 high body temperature0x66 no mask0x67 get health code fail0x68 No Entry because of yellow code0x69 No Entry because of red code0x6a health code is invalid0x6b entry because of green code0x6e Green code, travel code not green code0x6f Green code, get health code info0x71 verify citizenId (platform issues the verification result of the corresponding citizenId)0xA8 not wear safety helmet (customized)0xB1 insufficient authorization information, to be supplemented;
        ('nPunchingRecNo', c_int),  # 刷卡记录集中的记录编号;punching record number;
        ('nNumbers', c_int),  # 抓图张数;pic Numbers;
        ('emStatus', C_ENUM),  # 卡状态 Refer: EM_A_NET_ACCESSCTLCARD_STATE;Card Status Refer: EM_A_NET_ACCESSCTLCARD_STATE;
        ('szSN', c_char * 32),  # 智能锁序列号;wireless deivce serial number;
        ('emAttendanceState', C_ENUM),  # 考勤状态 Refer: EM_A_NET_ATTENDANCESTATE;attend state Refer: EM_A_NET_ATTENDANCESTATE;
        ('szQRCode', c_char * 512),  # 二维码;QRcode;
        ('szCallLiftFloor', c_char * 16),  # 呼梯楼层号;Floor of Call Lift;
        ('emCardState', C_ENUM),  # 是否为采集卡片 Refer: EM_CARD_STATE;Collect as card or not Refer: EM_CARD_STATE;
        ('szCitizenIDNo', c_char * 20),  # 证件号;Citizen card ID;
        ('szCompanionCards', c_char * 192),  # 陪同者卡号信息;The companion cards list;
        ('nCompanionCardCount', c_int),  # 陪同者卡号个数;The number of companion cards;
        ('emHatStyle', C_ENUM),  # 帽子类型 Refer: EM_HAT_STYLE;hat style Refer: EM_HAT_STYLE;
        ('emHatColor', C_ENUM),  # 帽子颜色 Refer: EM_UNIFIED_COLOR_TYPE;hat color Refer: EM_UNIFIED_COLOR_TYPE;
        ('emLiftCallerType', C_ENUM),  # 梯控方式触发者 Refer: EM_LIFT_CALLER_TYPE;lift caller type Refer: EM_LIFT_CALLER_TYPE;
        ('bManTemperature', C_BOOL),  # 人员温度信息是否有效;Whether the information of human body temperature is valid;
        ('stuManTemperatureInfo', NET_MAN_TEMPERATURE_INFO),  # 人员温度信息, bManTemperature 为TRUE 时有效;Information of human body temperature, It is valid whne bManTemperature is TURE;
        ('szCitizenName', c_char * 256),  # 证件姓名;citizen name;
        ('emMask', C_ENUM),  # 口罩状态（EM_MASK_STATE_UNKNOWN、EM_MASK_STATE_NOMASK、EM_MASK_STATE_WEAR 有效） Refer: EM_MASK_STATE_TYPE;mask ( EM_MASK_STATE_UNKNOWN,EM_MASK_STATE_NOMASK,EM_MASK_STATE_WEAR is valid ) Refer: EM_MASK_STATE_TYPE;
        ('szCardName', c_char * 64),  # 卡命名;card name;
        ('nFaceIndex', C_UINT),  # 一人脸时的人脸序号;face index;
        ('emUserType', C_ENUM),  # 用户类型( EM_USER_TYPE ) ;user type( from EM_USER_TYPE)
        ('bRealUTC', C_BOOL),  # RealUTC 是否有效，bRealUTC 为 TRUE 时，用 RealUTC，否则用 stuTime 字段;whether RealUTC is valid. when bRealUTC is TRUE, use RealUTC, otherwise use stuTime;
        ('RealUTC', NET_TIME_EX),  # 事件发生的时间（标准UTC）;event occur time;
        ('szCompanyName', c_char * 200),  # 公司名称;Company Address;
        ('nScore', c_int),  # 人脸质量评分;Face Quality;
        ('nLiftNo', c_int),  # 电梯编号;Elevator number;
        ('emQRCodeIsExpired', C_ENUM),  # 
        ('emQRCodeState', C_ENUM),  # 
        ('stuQRCodeValidTo', NET_TIME),  # 二维码截止日期;QR code deadline;
        ('szDynPWD', c_char * 32),  # 平台通过密码校验权限。用于动态密码校验，动态密码由手机APP生成，设备仅透传给平台;The platform verifies permissions by password. Used for dynamic password verification. The dynamic password is generated by the mobile APP, and the device is only transparently transmitted to the platform;
        ('nBlockId', C_UINT),  # 上报事件数据序列号从1开始自增;The serial number of the reported event data increases from 1;
        ('szSection', c_char * 64),  # 部门名称;Department name;
        ('szWorkClass', c_char * 256),  # 工作班级;Work class;
        ('emTestItems', C_ENUM),  # 测试项目 Refer: EM_TEST_ITEMS;Test items Refer: EM_TEST_ITEMS;
        ('stuTestResult', NET_TEST_RESULT),  # ESD阻值测试结果;ESD resistance test result;
        ('szDeviceID', c_char * 128),  # 门禁设备编号;Access control equipment number;
        ('szUserUniqueID', c_char * 128),  # 用户唯一表示ID;User unique ID;
        ('bUseCardNameEx', C_BOOL),  # 是否使用卡命名扩展;Whether to use the card name extension;
        ('szCardNameEx', c_char * 128),  # 卡命名扩展;Card name extension;
        ('szTempPassword', c_char * 64),  # 临时密码;tmp passwd;
        ('szNote', c_char * 512),  # 摘要信息;Note;
        ('nHSJCResult', c_int),  # 核酸检测报告结果 
        ('stuVaccineInfo', NET_VACCINE_INFO),  # 新冠疫苗接种信息;New crown vaccination information;
        ('stuTravelInfo', NET_TRAVEL_INFO),  # 行程码信息;Trip code information;
        ('szQRCodeEx', c_char * 2048),  # 用来上传大二维码内容; used to upload large QR code content;
        ('stuHSJCInfo', NET_HSJC_INFO),  # 核酸信息;Nucleic acid detection information;
        ('stuAntigenInfo', NET_ANTIGEN_INFO),  # 抗原检测信息;Antigen Test Information;
        ('szHealthGreenStatus', c_char * 20),   # 个人健康状态 绿码:"Green" 红码:"Red" 黄码:"Yellow" 橙:"Orange" 未知:"None";Personal health status Green Code:"Green" Red code:"Red" Yellow code:"Yellow" Orange code:"Orange" unknown:"None";
        ('nAge', c_int),  # 年龄;Age;
        ('szReserved', c_char * 2044),  # 预留字节;Reserved;
    ]

class NET_CTRL_ACCESS_OPEN(Structure):
    """
    CLIENT_ControlDevice接口的 CTRL_ACCESS_OPEN 命令参数
    CLIENT_ControlDevice's param: CTRL_ACCESS_OPEN
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannelID', c_int),  # 通道号(0开始);Channel ID (start from 0);
        ('szTargetID', POINTER(c_char)),  # 转发目标设备ID,为NULL表示不转发;Target ID, NULL equals to not transmit;
        ('szUserID', c_char * 32),  # 远程用户ID;remote user id;
        ('emOpenDoorType', C_ENUM),  # 开门方式 Refer: EM_OPEN_DOOR_TYPE;open door type Refer: EM_OPEN_DOOR_TYPE;
        ('emOpenDoorDirection', C_ENUM),  # 开门方向 Refer: EM_OPEN_DOOR_DIRECTION;open door direction Refer: EM_OPEN_DOOR_DIRECTION;
        ('emRemoteCheckCode', C_ENUM),  # 远程权限验证结果 Refer: EM_REMOTE_CHECK_CODE;remote check code Refer: EM_REMOTE_CHECK_CODE;
        ('szShortNumber', c_char * 16),  # 兼容字段;Compatible fields;
    ]

class NET_CTRL_ACCESS_CLOSE(Structure):
    """
    CLIENT_ControlDevice接口的 CTRL_ACCESS_CLOSE 命令参数
    CLIENT_ControlDevice's param: CTRL_ACCESS_CLOSE
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nChannelID', c_int),  # 通道号(0开始);Channel ID (start from 0);
    ]

class NET_ACCESS_USER_INFO_EX(Structure):
    """
    用户信息
    User Info extension
    """
    _fields_ = [
        ('szConsumptionTimeSections', c_char * 1428),  # 消费时间段每天最多6个时间段，每6个元素对应一天。一共7天。每个时段格式为"星期 时:分:秒-时:分:秒 消费类型 可消费次数 可消费金额"，星期从0开始，表示周日，前6个时段前面都是0，表示周日的6个时段，剩下依次周一，周二... 一共42个时段。消费类型包括：0为定额消费，1为非定额消费；可消费次数最大上限200次；可消费金额最高999900，也就是9999元;
                              # Consumption TimeSectionsevery day has six TimeSectionsthe TimeSection format is: "DayNo hour:minute:second-hour:minute:second type times amount"DayNo starts with 0, 0 means Sunday, the DayNo of the the first six TimeSections is 0type is the Consumption type, 0 means quota, 1 means nonquotatimes is the Consumable times, the max is 200amount is the Consumable amount, the max is 999900 cents;
        ('byReserved', C_BYTE * 1024),  # 保留字节;Reserved;
    ]

class NET_ACCESS_USER_INFO(Structure):
    """
    用户信息
    User Info
    """
    _fields_ = [
        ('szUserID', c_char * 32),  # 用户ID;user ID;
        ('szName', c_char * 32),  # 人员名称;user name;
        ('emUserType', C_ENUM),  # 用户类型 Refer: EM_A_NET_ENUM_USER_TYPE;user type Refer: EM_A_NET_ENUM_USER_TYPE;
        ('nUserStatus', C_UINT),  # 用户状态, 0 正常, 1 冻结;user status, 0 normal, 1 freeze;
        ('nUserTime', c_int),  # 来宾卡的通行次数;user times of guest;
        ('szCitizenIDNo', c_char * 32),  # 证件号码;CitizenID no;
        ('szPsw', c_char * 64),  # UserID+密码开门时密码;UserID+password;
        ('nDoorNum', c_int),  # 有效的门数目;;door number;;
        ('nDoors', c_int * 32),  # 有权限的门序号,即 CFG_CMD_ACCESS_EVENT 配置的数组下标;Privileged Door Number,That is CFG_CMD_ACCESS_EVENT Configure Array Subscript;
        ('nTimeSectionNum', c_int),  # 有效的的开门时间段数目;the Number of Effective Open Time;
        ('nTimeSectionNo', c_int * 32),  # 开门时间段索引,即 CFG_ACCESS_TIMESCHEDULE_INFO 的数组下标;Open Time Segment Index,That is CFG_ACCESS_TIMESCHEDULE_INFO Array subscript;
        ('nSpecialDaysScheduleNum', c_int),  # 假日计划表示数量;the number of specialday;
        ('nSpecialDaysSchedule', c_int * 128),  # 假日计划标识, 即 NET_EM_CFG_ACCESSCTL_SPECIALDAYS_SCHEDULE 配置的下标;Open specialday index, That is NET_EM_CFG_ACCESSCTL_SPECIALDAYS_SCHEDULE Array subscript;
        ('stuValidBeginTime', NET_TIME),  # 开始有效期;Valid Begin Time;
        ('stuValidEndTime', NET_TIME),  # 结束有效期;Valid End Time;
        ('bFirstEnter', C_BOOL),  # 是否拥有首卡权限;has first card or not;
        ('nFirstEnterDoorsNum', c_int),  # 拥有首用户权限的门数量;has first card door number;
        ('nFirstEnterDoors', c_int * 32),  # 拥有首用户权限的门序号，bFirstEnter为TRUE时有效,-1表示全通道;has first card door No,FirstEnter-1 means all channels;
        ('emAuthority', C_ENUM),  # 用户权限，可选 Refer: EM_A_NET_ATTENDANCE_AUTHORITY;user authority Refer: EM_A_NET_ATTENDANCE_AUTHORITY;
        ('nRepeatEnterRouteTimeout', c_int),  # 反潜超时时间;repeatenter timeout time;
        ('nFloorNum', c_int),  # 有效的楼层数量;floor number;
        ('szFloorNo', c_char * 1024),  # 楼层号;floor;
        ('nRoom', c_int),  # 房间个数;room number;
        ('szRoomNo', c_char * 512),  # 房间号列表;room;
        ('bFloorNoExValid', C_BOOL),  # szFloorNoEx 是否有效;if szFloorNoEx is valid, TRUE:valid, else invalid;
        ('nFloorNumEx', c_int),  # 有效的楼层数量扩展;floor number extended;
        ('szFloorNoEx', c_char * 1024),  # 楼层号扩展;floor info;
        ('szClassInfo', c_char * 256),  # 班级信息;class info;
        ('szStudentNo', c_char * 64),  # 学号;student num;
        ('szCitizenAddress', c_char * 128),  # 证件地址;citizen address;
        ('stuBirthDay', NET_TIME),  # 出生日期（年月日有效）;birth day (year month day are valid);
        ('emSex', C_ENUM),  # 性别 Refer: EM_A_NET_ACCESSCTLCARD_SEX;sex Refer: EM_A_NET_ACCESSCTLCARD_SEX;
        ('szDepartment', c_char * 128),  # 部门;department;
        ('szSiteCode', c_char * 32),  # 站点码;site cod;
        ('szPhoneNumber', c_char * 32),  # 手机号码;PhoneNumber;
        ('szDefaultFloor', c_char * 8),  # 默认楼层号;Default floor number (elevator control requirements);
        ('bFloorNoEx2Valid', C_BOOL),  # 是否使用扩展结构体;stuFloorsEx2 wheather valid;
        ('pstuFloorsEx2', POINTER(NET_FLOORS_INFO)),  # 楼层号（再次扩展）;Floor number (extended again);
        ('bHealthStatus', C_BOOL),  # 人员健康状态;Personnel health status;
        ('nUserTimeSectionsNum', c_int),  # 用户自身的开门时间段校验有效个数;The number of valid verifications for the user's own door opening time;
        ('szUserTimeSections', c_char * 120),  # 针对用户自身的开门时间段校验;Check the user's own door opening time period;
        ('szECType', c_char * 64),  # 民族;Nation;
        ('emTypeOfCertificate', C_ENUM),  # 证件类型 Refer: EM_TYPE_OF_CERTIFICATE;type of certificate Refer: EM_TYPE_OF_CERTIFICATE;
        ('szCountryOrAreaCode', c_char * 8),  # 国籍或所在地区代码，符合GB/T 2659-2000的规范;Nationality or area code, in line with GB/T 2659-2000;
        ('szCountryOrAreaName', c_char * 64),  # 国籍或所在地区名称，符合GB/T 2659-2000的规范;Nationality or area name, in line with GB/T 2659-2000;
        ('szCertificateVersionNumber', c_char * 64),  # 永久居住证的证件版本号;The version number of the permanent residence permit;
        ('szApplicationAgencyCode', c_char * 64),  # 申请受理机关代码;Application acceptance agency code;
        ('szIssuingAuthority', c_char * 64),  # 签发机关;issuing authority;
        ('szStartTimeOfCertificateValidity', c_char * 64),  # 证件有效开始时间;Start time of certificate validity;
        ('szEndTimeOfCertificateValidity', c_char * 64),  # 证件有效结束时间;End time of certificate validity;
        ('nSignNum', c_int),  # 证件签发次数;Number of certificates issued;
        ('szActualResidentialAddr', c_char * 108),  # 实际家庭住址;Actual home address;
        ('szWorkClass', c_char * 256),  # 工作班别;Work class;
        ('stuStartTimeInPeriodOfValidity', NET_TIME),  # 有效时间段内启动时间;Start time within valid time period;
        ('emTestItems', C_ENUM),  # 测试项目 Refer: EM_TEST_ITEMS;Test items Refer: EM_TEST_ITEMS;
        ('bUseNameEx', C_BOOL),  # szNameEx 是否有效，为TRUE时，使用szNameEx字段;Whether to use the szNameEx field;
        ('szNameEx', c_char * 128),  # 人员名称扩展;Name extension;
        ('bUserInfoExValid', C_BOOL),  # 是否使用用户信息结构体;pstuUserInfoEx wheather valid;
        ('pstuUserInfoEx', POINTER(NET_ACCESS_USER_INFO_EX)),  # 扩展用户信息;User Info (extended);
        ('nAuthOverdueTime', C_UINT),  # 授权时间、过期时间，时间单位: 小时;Authorization time, expiration time, time unit: hour;
        ('emGreenCNHealthStatus', C_ENUM),  # 人员健康状态 Refer: EM_GREENCNHEALTH_STATUS;Staff health status Refer: EM_GREENCNHEALTH_STATUS;
        ('emAllowPermitFlag', C_ENUM),  # 电子通行证状态） Refer: EM_ALLOW_PERMIT_FLAG;E-pass status Refer: EM_ALLOW_PERMIT_FLAG;
        ('nHolidayGroupIndex', c_int),  # 假日组HolidayGroup索引值; holiday group HolidayGroup index value;
        ('stuUpdateTime', NET_TIME),  # 信息更新时间,UTC时间;Info UpdateTime,UTC time;
        ('szValidFroms', c_char * 192),  # 用户的门通道起始有效期,每个通道设置一个有效期,数组元素与门通道一一对应;The initial validity period of the user's door channel, each channel is set to a validity period, and the array elements correspond to the door channels one-to-one;
        ('nValidFromsNum', c_int),  # 用户的门通道起始有效期有效个数, 最大值为8;The valid number of the user's door channel starting valid, the maximum value is 8;
        ('nValidTosNum', c_int),  # 用户的门通道截止有效期有效个数, 最大值为8;User's gate channel expiration valid number, the maximum value is 8;
        ('szValidTos', c_char * 192),  # 用户的门通道截止有效期,每个通道设置一个有效期,数组元素与门通道一一对应;The user's door channel expires valid period, each channel is set to a valid period, and the array elements correspond to the door channel one-to-one;
        ('byReserved', C_BYTE * (880 - sizeof(c_void_p))),  # 保留字节;Reserved;
    ]

class NET_IN_ACCESS_USER_SERVICE_INSERT(Structure):
    """
    新增或更新用户信息入参
    input of insert or update user
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nInfoNum', c_int),  # 用户信息数量;user number;
        ('pUserInfo', POINTER(NET_ACCESS_USER_INFO)),  # 用户信息,内存由用户申请释放，申请大小不小于nInfoNum*sizeof(NET_ACCESS_USER_INFO);;user info;
    ]

class NET_OUT_ACCESS_USER_SERVICE_INSERT(Structure):
    """
    新增或更新用户信息出参
    output param of insert or update user
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nMaxRetNum', c_int),  # 申请的最大返回的错误信息数量,不小于NET_IN_ACCESS_USER_SERVICE_INSERT中nInfoNum;max return number, nInfoNum of NET_IN_ACCESS_USER_SERVICE_INSERT plus;
        ('pFailCode', POINTER(C_ENUM)),  # 用户分配释放内存,插入失败时，对应插入的每一项的结果,返回个数同NET_IN_ACCESS_USER_SERVICE_INSERT中nInfoNum Refer: EM_A_NET_EM_FAILCODE;errorcode when insert failed,return number is nInfoNum of NET_IN_ACCESS_USER_SERVICE_INSERT Refer: EM_A_NET_EM_FAILCODE;
    ]

class NET_IN_ACCESS_USER_SERVICE_GET(Structure):
    """
    获取用户信息入参
    input param of Get user
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nUserNum', c_int),  # 查询的数量;Get number;
        ('szUserID', c_char * 3200),  # 用户ID;user id;
        ('szUserIDEx', c_char * 100 * 128), # 用户ID扩展，当前只支持32位有效值下发;User ID extension, currently only 32-bit valid values are supported;
        ('bUserIDEx', C_BOOL),  # szUserIDEx 是否有效，为TRUE时，使用szUserIDEx字段;Whether szUserIDEx is valid. If true, use the szUserIDEx field;
    ]

class NET_OUT_ACCESS_USER_SERVICE_GET(Structure):
    """
    获取用户信息出参
    output param of Get user
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nMaxRetNum', c_int),  # 查询返回的最大数量;max number of return;
        ('pUserInfo', POINTER(NET_ACCESS_USER_INFO)),  # 用户信息,内存由用户申请释放，申请大小不小于 nUserNum*sizeof(NET_ACCESS_USER_INFO)                                                                            返回个数同NET_IN_ACCESS_USER_SERVICE_GET中nUserNum;user info,larger than nUserNum*sizeof(NET_ACCESS_USER_INFO);
        ('pFailCode', POINTER(C_ENUM)),  # 查询失败时，内存由用户申请释放,对应查询的每一项的结果，返回个数同NET_IN_ACCESS_USER_SERVICE_GET中nUserNum Refer: EM_A_NET_EM_FAILCODE;errorcode when failed,return number is nUserNum in NET_IN_ACCESS_USER_SERVICE_GET Refer: EM_A_NET_EM_FAILCODE;
    ]

class NET_IN_ACCESS_USER_SERVICE_REMOVE(Structure):
    """
    删除指定ID人员信息入参
    input of  remove user
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nUserNum', c_int),  # 删除的数量;remove number;
        ('szUserID', c_char * 3200),  # 用户ID;user ID;
        ('szUserIDEx', c_char * 100 * 128), # 用户ID扩展，当前只支持32位有效值下发;User ID extension, currently only 32-bit valid values are supported;
        ('bUserIDEx', C_BOOL),  # szUserIDEx 是否有效，为TRUE时，使用szUserIDEx字段;Whether szUserIDEx is valid. If true, use the szUserIDEx field;
    ]

class NET_OUT_ACCESS_USER_SERVICE_REMOVE(Structure):
    """
    删除指定ID人员信息出参
    output of remove user
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nMaxRetNum', c_int),  # 返回的最大数量,不小于 NET_IN_ACCESS_USER_SERVICE_REMOVE中nUserNum;max return number,nUserNum in NET_IN_ACCESS_USER_SERVICE_REMOVE;
        ('pFailCode', POINTER(C_ENUM)),  # 插入失败时，内存由用户申请释放,对应插入的每一项的结果,返回个数同NET_IN_ACCESS_USER_SERVICE_REMOVE中nUserNum Refer: EM_A_NET_EM_FAILCODE;errorcode when failed,return number is nUserNum in NET_IN_ACCESS_USER_SERVICE_REMOVE Refer: EM_A_NET_EM_FAILCODE;
    ]

class NET_IN_ACCESS_USER_SERVICE_CLEAR(Structure):
    """
    删除所有人员信息入参
    input of clear user
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_OUT_ACCESS_USER_SERVICE_CLEAR(Structure):
    """
    删除所有人员信息出参
    output of clear user
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_ACCESS_FACE_INFO(Structure):
    """
    人脸信息
    face info
    """
    _fields_ = [
        ('szUserID', c_char * 32),  # 用户ID;user ID;
        ('nFaceData', c_int),  # 人脸模板数据个数,最大20;count of face data,the max number is 20;
        ('szFaceData', c_char * 40960),  # 人脸模板数据;face data;
        ('nFaceDataLen', c_int * 20),  # 人脸模版数据大小;face data length;
        ('nFacePhoto', c_int),  # 人脸照片个数,不超过5个;count of face photo,max size: 5;
        ('nInFacePhotoLen', c_int * 5),  # 用户申请的每张图片的大小;the size of each photo used by the user;
        ('nOutFacePhotoLen', c_int * 5),  # 每张图片实际的大小;the actual size of each photo;
        ('pFacePhoto', c_void_p * 5),  # 人脸照片数据,大小不超过200K;face photo data,max size: 120K;
        ('bFaceDataExEnable', C_BOOL),  # 是否使用扩展人脸模板数据;Whether to use extended face template data;
        ('nMaxFaceDataLen', c_int * 20),  # 用户申请的扩展人脸模板数据大小;Data size of the extended face template requested by the user;
        ('nRetFaceDataLen', c_int * 20),  # 实际人脸模板数据大小;Actual face template data size;
        ('pFaceDataEx', POINTER(c_char) * 20),  # 人脸模板数据扩展字段 当bFaceDataExEnable有效时，建议使用扩展字段pFaceDataEx;Face template data extension field,When bFaceDataExEnable is valid, it is recommended to use the extension field pFaceDataEx;
        ('stuUpdateTime', NET_TIME),  # 人脸信息更新时间,UTC时间;Info UpdateTime,UTC time;
        ('byReserved', C_BYTE * 1776),  # 保留字节;reserved;
    ]

class NET_IN_ACCESS_FACE_SERVICE_INSERT(Structure):
    """
    添加人脸记录信息输入参数(NET_EM_ACCESS_CTL_FACE_SERVICE_INSERT)
    the input param of adding face data(NET_EM_ACCESS_CTL_FACE_SERVICE_INSERT)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
        ('nFaceInfoNum', c_int),  # 人脸信息数量;face info number;
        ('pFaceInfo', POINTER(NET_ACCESS_FACE_INFO)),  # 人脸数据,用户自行分配数据;face info,user allocates memory;
    ]

class NET_OUT_ACCESS_FACE_SERVICE_INSERT(Structure):
    """
    添加人脸记录信息输出参数(NET_EM_ACCESS_CTL_FACE_SERVICE_INSERT)
    the output param of adding face data(NET_EM_ACCESS_CTL_FACE_SERVICE_INSERT)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
        ('nMaxRetNum', c_int),  # 最大返回数量,不小于 NET_IN_ACCESS_FACE_SERVICE_INSERT 中的nFaceInfoNum;the max return number,not less than nFaceInfoNum in NET_IN_ACCESS_FACE_SERVICE_INSERT;
        ('pFailCode', POINTER(C_ENUM)),  # 用户分配内存,添加失败时,对应插入的每一项的结果,返回个数同NET_IN_ACCESS_FACE_SERVICE_INSERT中的nFaceInfoNum Refer: EM_A_NET_EM_FAILCODE;user allocates memory.when insert failed,the result of each item inserted,count is nFaceInfoNum in NET_IN_ACCESS_FACE_SERVICE_INSERT Refer: EM_A_NET_EM_FAILCODE;
    ]

class NET_IN_ACCESS_FACE_SERVICE_GET(Structure):
    """
    批量获取多用户多个人脸输入参数(NET_EM_ACCESS_CTL_FACE_SERVICE_GET)
    the input param of getting face data(NET_EM_ACCESS_CTL_FACE_SERVICE_GET)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
        ('nUserNum', c_int),  # 用户ID数量,最大100;user ID number,the max number is 100;
        ('szUserID', c_char * 3200),  # 用户ID;user ID;
        ('szUserIDEx', c_char * 100 * 128), # 用户ID扩展，当前只支持32位有效值下发;User ID extension, currently only 32-bit valid values are supported;
        ('bUserIDEx', C_BOOL),  # szUserIDEx 是否有效，为TRUE时，使用szUserIDEx字段;Whether szUserIDEx is valid. If true, use the szUserIDEx field;
    ]

class NET_OUT_ACCESS_FACE_SERVICE_GET(Structure):
    """
    批量获取多用户多个人脸输出参数(NET_EM_ACCESS_CTL_FACE_SERVICE_GET)
    the out param of getting face data(NET_EM_ACCESS_CTL_FACE_SERVICE_GET)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
        ('nMaxRetNum', c_int),  # 最大返回数量,不小于 NET_IN_ACCESS_FACE_SERVICE_GET 中的 nUserNum;the max return number,not less than nUserNum in NET_IN_ACCESS_FACE_SERVICE_GET;
        ('pFaceInfo', POINTER(NET_ACCESS_FACE_INFO)),  # 人脸数据,用户分配内存,返回个数同NET_IN_ACCESS_FACE_SERVICE_GET中的nUserNum,只返回的人脸模版数据;face data,user allocates memory.count is nUserNum in NET_IN_ACCESS_FACE_SERVICE_GET,only return face data;
        ('pFailCode', POINTER(C_ENUM)),  # 用户分配内存,获取失败时,对应获取的每一项的结果,返回个数同NET_IN_ACCESS_FACE_SERVICE_GET中的nUserNum Refer: EM_A_NET_EM_FAILCODE;user allocates memory.when get failed,the result of each item get,count is nUserNum in NET_IN_ACCESS_FACE_SERVICE_GET Refer: EM_A_NET_EM_FAILCODE;
    ]

class NET_IN_ACCESS_FACE_SERVICE_UPDATE(Structure):
    """
    更新多用户多个人脸记录信息输入参数(NET_EM_ACCESS_CTL_FACE_SERVICE_UPDATE)
    the input param to update face data(NET_EM_ACCESS_CTL_FACE_SERVICE_UPDATE)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
        ('nFaceInfoNum', c_int),  # 人脸信息数量;face info number;
        ('pFaceInfo', POINTER(NET_ACCESS_FACE_INFO)),  # 人脸数据,用户分配内存;face data,user allocates memory;
    ]

class NET_OUT_ACCESS_FACE_SERVICE_UPDATE(Structure):
    """
    更新多用户多个人脸记录信息输出参数(NET_EM_ACCESS_CTL_FACE_SERVICE_UPDATE)
    the output param to update face data(NET_EM_ACCESS_CTL_FACE_SERVICE_UPDATE)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
        ('nMaxRetNum', c_int),  # 最大返回数量,不小于 NET_IN_ACCESS_FACE_SERVICE_UPDATE中的nFaceInfoNum;the max return number,not less than nFaceInfoNum in NET_IN_ACCESS_FACE_SERVICE_UPDATE;
        ('pFailCode', POINTER(C_ENUM)),  # 用户分配内存.更新失败时,对应更新的每一项的结果,返回个数同NET_IN_ACCESS_FACE_SERVICE_UPDATE中的nFaceInfoNum Refer: EM_A_NET_EM_FAILCODE;user allocates memory.when update failed,the result of each item updated,count is nFaceInfoNum in NET_IN_ACCESS_FACE_SERVICE_UPDATE Refer: EM_A_NET_EM_FAILCODE;
    ]

class NET_IN_ACCESS_FACE_SERVICE_REMOVE(Structure):
    """
    删除多用户的多个人脸信息输入参数(NET_EM_ACCESS_CTL_FACE_SERVICE_REMOVE)
    the input param of removing face data(NET_EM_ACCESS_CTL_FACE_SERVICE_REMOVE)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
        ('nUserNum', c_int),  # 用户ID数量,最大100;user ID number,the max number is 100;
        ('szUserID', c_char * 3200),  # 用户ID;user ID;
        ('szUserIDEx', c_char * 100 * 128), # 用户ID扩展，当前只支持32位有效值下发;User ID extension, currently only 32-bit valid values are supported;
        ('bUserIDEx', C_BOOL),  # szUserIDEx 是否有效，为TRUE时，使用szUserIDEx字段;Whether szUserIDEx is valid. If true, use the szUserIDEx field;
    ]

class NET_OUT_ACCESS_FACE_SERVICE_REMOVE(Structure):
    """
    删除多用户的多个人脸信息输出参数(NET_EM_ACCESS_CTL_FACE_SERVICE_REMOVE)
    the output param of removing face data(NET_EM_ACCESS_CTL_FACE_SERVICE_REMOVE)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
        ('nMaxRetNum', c_int),  # 最大返回数量,不小于 NET_IN_ACCESS_FACE_SERVICE_REMOVE中的nUserNum;the max return number,not less than nUserNum in NET_IN_ACCESS_FACE_SERVICE_REMOVE;
        ('pFailCode', POINTER(C_ENUM)),  # 用户分配内存.删除失败时,对应删除的每一项的结果,返回个数同NET_IN_ACCESS_FACE_SERVICE_REMOVE中的nUserNum Refer: EM_A_NET_EM_FAILCODE;user allocates memory.when remove failed,the result of each item removed,count is nUserNum in NET_IN_ACCESS_FACE_SERVICE_REMOVE Refer: EM_A_NET_EM_FAILCODE;
    ]

class NET_IN_ACCESS_FACE_SERVICE_CLEAR(Structure):
    """
    清空所有人脸记录信息输入参数(NET_EM_ACCESS_CTL_FACE_SERVICE_CLEAR)
    the input param of clear face data(NET_EM_ACCESS_CTL_FACE_SERVICE_CLEAR)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
    ]

class NET_OUT_ACCESS_FACE_SERVICE_CLEAR(Structure):
    """
    清空所有人脸记录信息输出参数(NET_EM_ACCESS_CTL_FACE_SERVICE_CLEAR)
    the output param of clear face data(NET_EM_ACCESS_CTL_FACE_SERVICE_CLEAR)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
    ]

class NET_ACCESS_CARD_INFO(Structure):
    """
    卡片信息
    card info
    """
    _fields_ = [
        ('szCardNo', c_char * 32),  # 卡号;card number;
        ('szUserID', c_char * 32),  # 用户ID;user id;
        ('emType', C_ENUM),  # 卡类型,只支持一般卡、胁迫卡和母卡 Refer: NET_ACCESSCTLCARD_TYPE;card type,only support General,Corce,Mother card Refer: NET_ACCESSCTLCARD_TYPE;
        ('szDynamicCheckCode', c_char * 16),  # 动态校验码;dynamic check code;
        ('stuUpdateTime', NET_TIME),  # 信息更新时间,UTC时间;Info UpdateTime,UTC time;
        ('byReserved', C_BYTE * 4072),  # 保留字节;reserve;
    ]

class NET_IN_ACCESS_CARD_SERVICE_INSERT(Structure):
    """
    新增卡片信息入参
    input of insert card
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nInfoNum', c_int),  # 用户信息数量;card number;
        ('pCardInfo', POINTER(NET_ACCESS_CARD_INFO)),  # 卡片信息,用户分配释放内存,大小为sizeof(NET_ACCESS_CARD_INFO)*nInfoNum;card info;
    ]

class NET_OUT_ACCESS_CARD_SERVICE_INSERT(Structure):
    """
    新增卡片信息出参
    output of insert card
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nMaxRetNum', c_int),  # 最大返回的用户信息数量,不小于NET_IN_ACCESS_CARD_SERVICE_INSERT中nInfoNum;return number ,greater than nInfoNum in NET_IN_ACCESS_CARD_SERVICE_INSERT;
        ('pFailCode', POINTER(C_ENUM)),  # 用户分配释放内存,插入失败时,对应插入的每一项的结果,返回个数同NET_IN_ACCESS_CARD_SERVICE_INSERT中nInfoNum Refer: EM_A_NET_EM_FAILCODE;error code,return number is nInfoNum in NET_IN_ACCESS_CARD_SERVICE_INSERT Refer: EM_A_NET_EM_FAILCODE;
        ('byReserved', C_BYTE * 4),
    ]

class NET_IN_ACCESS_CARD_SERVICE_GET(Structure):
    """
    获取卡片信息入参
    input of get card info
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nCardNum', c_int),  # 查询的数量;get number;
        ('szCardNo', c_char * 3200),  # 卡号;card No;
    ]

class NET_OUT_ACCESS_CARD_SERVICE_GET(Structure):
    """
    获取卡片信息出参
    output of get card info
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nMaxRetNum', c_int),  # 查询返回的最大数量;max return number;
        ('pCardInfo', POINTER(NET_ACCESS_CARD_INFO)),  # 卡片信息,内存由用户申请释放，申请大小不小于nCardNum*sizeof(NET_ACCESS_CARD_INFO);                                                                            返回个数同NET_IN_ACCESS_CARD_SERVICE_GET中nCardNum;card info;
        ('pFailCode', POINTER(C_ENUM)),  # 查询失败时，对应查询的每一项的结果,返回个数同NET_IN_ACCESS_CARD_SERVICE_GET中nCardNum Refer: EM_A_NET_EM_FAILCODE;error code,return number is nCardNum in NET_IN_ACCESS_CARD_SERVICE_GET Refer: EM_A_NET_EM_FAILCODE;
    ]

class NET_IN_ACCESS_CARD_SERVICE_UPDATE(Structure):
    """
    更新卡片信息入参
    input of update card info
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nInfoNum', c_int),  # 用户信息数量;card number;
        ('pCardInfo', POINTER(NET_ACCESS_CARD_INFO)),  # 卡片信息,用户分配释放内存,大小为sizeof(NET_ACCESS_CARD_INFO)*nInfoNum;card info;
    ]

class NET_OUT_ACCESS_CARD_SERVICE_UPDATE(Structure):
    """
    更新卡片信息出参
    output of update card info
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nMaxRetNum', c_int),  # 最大返回的用户信息数量,不小于NET_IN_ACCESS_CARD_SERVICE_UPDATE中nInfoNum;max return number,greater than nInfoNum in NET_IN_ACCESS_CARD_SERVICE_UPDATE;
        ('pFailCode', POINTER(C_ENUM)),  # 用户分配释放内存,插入失败时，对应插入的每一项的结果,返回个数同NET_IN_ACCESS_CARD_SERVICE_UPDATE中nInfoNum Refer: EM_A_NET_EM_FAILCODE;error code,return number is nInfoNum in NET_IN_ACCESS_CARD_SERVICE_UPDATE Refer: EM_A_NET_EM_FAILCODE;
        ('byReserved', C_BYTE * 4),  # reserved;
    ]

class NET_IN_ACCESS_CARD_SERVICE_REMOVE(Structure):
    """
    删除指定卡号信息入参
    input of remove card info
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nCardNum', c_int),  # 删除的数量;remove number;
        ('szCardNo', c_char * 3200),  # 卡号;card no;
    ]

class NET_OUT_ACCESS_CARD_SERVICE_REMOVE(Structure):
    """
    删除指定卡号信息出参
    output of remove card
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nMaxRetNum', c_int),  # 最大返回信息数量,不小于 NET_IN_ACCESS_CARD_SERVICE_REMOVE中nCardNum;max retrun number,great than nCardNum in NET_IN_ACCESS_CARD_SERVICE_REMOVE;
        ('pFailCode', POINTER(C_ENUM)),  # 用户分配释放内存,插入失败时,对应删除的每一项的结果,返回个数同NET_IN_ACCESS_CARD_SERVICE_REMOVE中nCardNum Refer: EM_A_NET_EM_FAILCODE;error code,return number is nCardNum in NET_IN_ACCESS_CARD_SERVICE_REMOVE Refer: EM_A_NET_EM_FAILCODE;
        ('byReserved', C_BYTE * 4),  # reserved;
    ]

class NET_IN_ACCESS_CARD_SERVICE_CLEAR(Structure):
    """
    删除所有卡片信息入参
    inout of clear card
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_OUT_ACCESS_CARD_SERVICE_CLEAR(Structure):
    """
    删除所有卡片信息出参
    output of clear card
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_A_ALARM_VIDEO_LOSS_INFO(Structure):
    """
    事件类型ALARM_VIDEO_LOSS (视频丢失事件)对应的数据块描述信息
    alarm of driver video loss, (Corresponding to event ALARM_VIDEO_LOSS)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作,1表示持续性事件开始,2表示持续性事件结束;;Event operation. 1=start. 2=stop;
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('dbPTS', c_double),  # 时间戳(单位是毫秒);Time stamp (Unit is ms);
        ('byReserved1', C_BYTE * 4),  # 字节对齐;alagin;
        ('stuTime', NET_TIME_EX),  # 事件发生的时间;Event occurrence time;
        ('stuStartTime', NET_TIME_EX),  # 开始时间,nAction为2时上报此字段;Start time,it is Reported when nAction is 2;
        ('stuGPS', NET_GPS_STATUS_INFO),  # GPS信息;GPS information;
        ('emViFormat', C_ENUM),  # 采集源分辨率 Refer: EM_NET_VIFORMAT_TYPE;Vi format Refer: EM_NET_VIFORMAT_TYPE;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('byReserved', C_BYTE * 1020),  # 保留字节;Reserved;
    ]

class NET_FURTHEST_RECORD_TIME(Structure):
    """
    最早录像时间
    The first recording time
    """
    _fields_ = [
        ('nChnCount', c_int),  # 通道数目;Channel amount;
        ('stuFurthestTime', NET_TIME * 16),  # 最早录像时间,有效值为前面0 到 (nChnCount-1)个.如果某通道没有录象的话,最早录象时间全为0;The first recording time, valid value is 0 to (nChnCount-1).If there is no video, the first recording time is 0.;
        ('dwFurthestTimeAllSize', C_DWORD),  # 当通道个数大于16时,使用。表示下面pStuFurthestTimeAll这块内存大小。;when channel >16,use this field.means pStuFurthestTimeAll memory size.;
        ('pStuFurthestTimeAll', POINTER(NET_TIME)),  # 当通道个数大于16时,使用。此部分内存需要用户申请,申请大小为(通道个数*sizeof(NET_TIME))。;when channel >16,use this field.need user apply, memory size(nChnCount*sizeof(NET_TIME)).;
        ('bReserved', C_BYTE * 376),  # 保留字段;Reserved words;
    ]

class NET_IN_GET_BOUND_TIMEEX(Structure):
    """
    CLIENT_GetStorageBoundTimeEx 入参
    CLIENT_GetStorageBoundTimeEx input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nDiskCount', c_int),  # 磁盘数量;disk count;
        ('nDiskList', c_int * 1024),  # 磁盘号列表;disk list;
    ]

class NET_BOUND_TIME_INFO(Structure):
    """
    硬盘录像时间信息
    disk bound time info
    """
    _fields_ = [
        ('nDiskNO', C_UINT),  # 磁盘号;disk NO;
        ('stuStartTime', NET_TIME_EX),  # 开始时间;Start Time;
        ('stuEndTime', NET_TIME_EX),  # 结束时间;End Time;
        ('byReserved', C_BYTE * 1024),  # 保留字节;reserved;
    ]

class NET_OUT_GET_BOUND_TIMEEX(Structure):
    """
    CLIENT_GetStorageBoundTimeEx 出参
    CLIENT_GetStorageBoundTimeEx output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nRetDiskCount', c_int),  # 返回的磁盘数量;return disk count;
        ('stuBoundTime', NET_BOUND_TIME_INFO * 1024),  # 硬盘录像时间信息;disk bound time info;
    ]

class NET_A_PTZ_LINK(Structure):
    """
    云台联动
    PTZ Activation
    """
    _fields_ = [
        ('iType', c_int),  # 0-None,1-Preset,2-Tour,3-Pattern;0-None,1-Preset,2-Tour,3-Pattern;
        ('iValue', c_int),
    ]

class NET_A_MSG_HANDLE_EX(Structure):
    """
    报警联动扩展结构体
    Alarm relay structure
    """
    _fields_ = [
        ('dwActionMask', C_DWORD),  # 当前报警所支持的处理方式,按位掩码表示;Current alarm supporting methods, shown by bit mask;
        ('dwActionFlag', C_DWORD),  # 触发动作,按位掩码表示,具体动作所需要的参数在各自的配置中体现;Triggering action,shown by bit mask,concrete action parameter is shows in the configuration;
        ('byRelAlarmOut', C_BYTE * 32),  # 报警触发的输出通道,报警触发的输出,为1表示触发该输出;
        ('dwDuration', C_DWORD),  # 报警持续时间;Alarm lasting period;
        ('byRecordChannel', C_BYTE * 32),  # 报警触发的录象通道,为1表示触发该通道;Record channel triggered by alarm,1 means triggering this channel;
        ('dwRecLatch', C_DWORD),  # 录象持续时间;Recording period;
        ('bySnap', C_BYTE * 32),  # 抓图通道;
        ('byTour', C_BYTE * 32),  # 轮巡通道 0-31路;
        ('struPtzLink', NET_A_PTZ_LINK * 32),
        ('dwEventLatch', C_DWORD),  # 联动开始延时时间,s为单位,范围是0~15,默认值是0;Event delay time, s for unit,range is 0~15,default is 0;
        ('byRelWIAlarmOut', C_BYTE * 32),  # 报警触发的无线输出通道,报警触发的输出,为1表示触发该输出;
        ('bMessageToNet', C_BYTE),
        ('bMMSEn', C_BYTE),  # 短信报警使能;Message triggering alarm enabling;
        ('bySnapshotTimes', C_BYTE),  # 短信发送抓图张数;the number of sheets of drawings;
        ('bMatrixEn', C_BYTE),  # 矩阵使能;Matrix output enable;
        ('dwMatrix', C_DWORD),  # 矩阵掩码;Matrix mask;
        ('bLog', C_BYTE),  # 日志使能,目前只有在WTN动态检测中使用;Log enable,only used in WTN motion detection;
        ('bSnapshotPeriod', C_BYTE),  # 抓图帧间隔,每隔多少帧抓一张图片,一定时间内抓拍的张数还与抓图帧率有关。0表示不隔帧,连续抓拍;Snapshot frame interval. System can snapshot regularly at the interval you specify here. The snapshot amount in a period of time also has relationship with the snapshot frame rate. 0 means there is no interval, system just snapshot continuously.;
        ('byTour2', C_BYTE * 32),  # 轮巡通道 32-63路*/;Tour channel 32-63;
        ('byEmailType', C_BYTE),  # 0,图片附件,1,录像附件>;0,picture,1,record>;
        ('byEmailMaxLength', C_BYTE),  # 附件录像时的最大长度,单位MB>;max record length,unit:MB>;
        ('byEmailMaxTime', C_BYTE),  # 附件是录像时最大时间长度,单位秒>;max time length, unit:second>;
        ('byReserved', C_BYTE * 475),
    ]

class NET_A_ALARM_ALARM_INFO_EX2(Structure):
    """
    本地报警事件(对ALARM_ALARM_EX升级)
    Local Alarm Event (ALARM_ALARM_EX Update
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('nAction', c_int),  # 0:开始 1:停止;0=Start 1=Stop;
        ('stuTime', NET_TIME),  # 报警事件发生的时间;Alarm Event Begin Time;
        ('emSenseType', C_ENUM),  # 传感器类型 Refer: EM_A_NET_SENSE_METHOD;The Sensor's Type Refer: EM_A_NET_SENSE_METHOD;
        ('stuEventHandler', NET_A_MSG_HANDLE_EX),  # 联动信息;Handle method;
        ('emDefenceAreaType', C_ENUM),  # 防区类型 Refer: EM_NET_DEFENCE_AREA_TYPE;protection area type, refer to EM_NET_DEFENCE_AREA_TYPE Refer: EM_NET_DEFENCE_AREA_TYPE;
        ('nEventID', C_UINT),  # 事件ID;event id;
        ('szName', c_char * 32),  # 通道名称;Channel Name;
        ('nCount', c_int),  # 事件发生次数;evnet count;
        ('stuGPS', NET_GPS_STATUS_INFO),  # GPS信息;GPS information;
        ('szUserID', c_char * 32),  # 本地报警时登陆的用户ID;User ID logged in at local alarm;
        ('szUserName', c_char * 128),  # 本地报警时登陆的用户名;User name logged in at local alarm;
        ('szSN', c_char * 32),  # 设备序列号;Device serial number;
        ('bExAlarmIn', C_BOOL),  # 外部输入报警;External input alarm;
        ('nAreaNums', c_int),  # 报警通道所属区域的个数;Number of areas to which the alarm channel belongs;
        ('nAreas', c_int * 64),  # 报警通道所属的区域;The area to which the alarm channel belongs;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('byReserved', C_BYTE * 568),  # 保留字节;Reserved;
    ]

class NET_A_ALARM_IPC_INFO(Structure):
    """
    IPC报警,IPC通过DVR或NVR上报的本地报警(对应事件 ALARM_IPC)
    IPC alarm,local alarm IPC send out by DVR or NVR(Corresponding to event  ALARM_IPC)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannelID', c_int),  # 通道号;Channel No.;
        ('nEventAction', c_int),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event operation. 0=pulse event.1=continues event begin. 2=continuous event stop;
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occurrence time;
        ('szName', c_char * 64),  # 报警通道名称;Alarm channel name;
        ('nAlarmChannel', c_int),  # 报警输入通道号，从0开始。没有该字段表示无法区分报警通道号。;Alarm input channel number, starting from 0. The absence of this field means that the alarm channel number cannot be distinguished.;
    ]

class NET_IN_MODIFY_IP(Structure):
    """
    修改IP入参
    input of CLIENT_ModifyDeviceEx
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('stuDevNetInfo', DEVICE_NET_INFO_EX2),  # 设备信息结构体;device net info;
    ]

class NET_OUT_MODIFY_IP(Structure):
    """
    修改IP出参
    output of CLIENT_ModifyDeviceEx
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_A_ETHERNET_EX(Structure):
    """
    以太网扩展配置
    Ethernet extended Configuration
    """
    _fields_ = [
        ('sDevIPAddr', c_char * 16),  # DVR IP 地址;DVR IP  address;
        ('sDevIPMask', c_char * 16),  # DVR IP 地址掩码;DVR IP subnet mask;
        ('sGatewayIP', c_char * 16),  # 网关地址为了扩展将DWORD拆成四个;Gateway addressDivide DWORD into four to future development;
        ('dwNetInterface', C_BYTE),  # NSP;NSP;
        ('bTranMedia', C_BYTE),  # 0：有线,1：无线;0:cable,1:wireless;
        ('bValid', C_BYTE),  # 按位表示,第一位：1：有效 0：无效；第二位：0：DHCP关闭 1：DHCP使能；第三位：0：不支持DHCP 1：支持DHCP;Use bit to represent, The first bit:1:valid 0:invalid;The second bit:0:unable DHCP 1:Enable DHCP;The third bit:0:Do not support DHCP 1:Support DHCP;
        ('bDefaultEth', C_BYTE),  # 是否作为默认的网卡 1：默认 0：非默认;To be the default network card or not.  1: default 0:non-default;
        ('byMACAddr', c_char * 40),  # MAC地址,只读;MAC address , read-only.;
        ('bMode', C_BYTE),  # 网卡所处模式, 0:绑定模式, 1:负载均衡模式, 2:多址模式, 3:容错模式;mode, 1:balance, 2:multi, 3:fault-toerant;
        ('bReserved1', C_BYTE * 3),  # 字节对齐;reserved;
        ('szEthernetName', c_char * 16),  # 网卡名,只读;Card name, read only;
        ('bReserved', C_BYTE * 12),  # 保留字节;reserved;
    ]

class NET_A_REMOTE_HOST(Structure):
    """
    远程主机配置
    Remote host setup
    """
    _fields_ = [
        ('byEnable', C_BYTE),  # 连接使能;Enable connection;
        ('byAssistant', C_BYTE),  # 目前只对于PPPoE服务器有用,0：在有线网卡拨号；1：在无线网卡上拨号;Only for PPPoE server,0:on the cabled network; 1:on the wireless network;
        ('wHostPort', c_uint16),  # 远程主机 端口;Remote host Port;
        ('sHostIPAddr', c_char * 16),  # 远程主机 IP 地址;Remote host IP address;
        ('sHostUser', c_char * 64),  # 远程主机 用户名;Remote host User name;
        ('sHostPassword', c_char * 32),  # 远程主机 密码;Remote host Password;
    ]

class NET_A_MAIL_CFG(Structure):
    """
    邮件配置
    Mail setup
    """
    _fields_ = [
        ('sMailIPAddr', c_char * 16),  # 邮件服务器IP地址;Email server IP;
        ('wMailPort', c_uint16),  # 邮件服务器端口;Email server port;
        ('wReserved', c_uint16),  # 保留;Reserved;
        ('sSenderAddr', c_char * 128),  # 发送地址;Send out address;
        ('sUserName', c_char * 16),  # 用户名;User name;
        ('sUserPsw', c_char * 16),  # 用户密码;User password;
        ('sDestAddr', c_char * 128),  # 目的地址;Destination address;
        ('sCcAddr', c_char * 128),  # 抄送地址;CC address;
        ('sBccAddr', c_char * 128),  # 暗抄地址;BCC address;
        ('sSubject', c_char * 64),  # 标题;Subject;
    ]

class NET_A_DEV_NET_CFG_EX(Structure):
    """
    扩展网络配置结构体
    Network extended configuration structure
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('sDevName', c_char * 16),  # 设备主机名;Device host name;
        ('wTcpMaxConnectNum', c_uint16),  # TCP最大连接数;TCP max connection amount;
        ('wTcpPort', c_uint16),  # TCP帧听端口;TCP listening port;
        ('wUdpPort', c_uint16),  # UDP侦听端口;UDP listening port;
        ('wHttpPort', c_uint16),  # HTTP端口号;HTTP port number;
        ('wHttpsPort', c_uint16),  # HTTPS端口号;HTTPS port number;
        ('wSslPort', c_uint16),  # SSL端口号;SSL port number;
        ('nEtherNetNum', c_int),  # 以太网口数;Ethernet port number;
        ('stEtherNet', NET_A_ETHERNET_EX * 10),  # 以太网口;Ethernet info;
        ('struAlarmHost', NET_A_REMOTE_HOST),  # 报警服务器;Alarm server;
        ('struLogHost', NET_A_REMOTE_HOST),  # 日志服务器;Log server;
        ('struSmtpHost', NET_A_REMOTE_HOST),  # SMTP服务器;SMTP server;
        ('struMultiCast', NET_A_REMOTE_HOST),  # 多播组;Multiple-cast group;
        ('struNfs', NET_A_REMOTE_HOST),  # NFS服务器;NFS server;
        ('struPppoe', NET_A_REMOTE_HOST),  # PPPoE服务器;PPPoE server;
        ('sPppoeIP', c_char * 16),  # PPPoE注册返回的IP;returned IP after PPPoE registration;
        ('struDdns', NET_A_REMOTE_HOST),  # DDNS服务器;DDNS server;
        ('sDdnsHostName', c_char * 64),  # DDNS主机名;DDNS host name;
        ('struDns', NET_A_REMOTE_HOST),  # DNS服务器;DNS server;
        ('struMail', NET_A_MAIL_CFG),  # 邮件配置;Email setup;
        ('bReserved', C_BYTE * 128),  # 保留字节;reserved;
    ]

class NET_A_ALARM_WIRELESSDEV_POWERLESS_INFO(Structure):
    """
    探测器主电丢失事件(对应ALARM_WIRELESSDEV_POWERLESS)
    wireless device powerless event(corresponding to ALARM_WIRELESSDEV_POWERLESS)
    """
    _fields_ = [
        ('nAction', c_int),  # 0:脉冲  1:开始 2:停止;0:pulse  1:start 2:stop;
        ('nIndex', c_int),  # 探测器地址;device index;
        ('stuLoacalTime', NET_TIME_EX),  # 事件发生的时间;Time of event;
        ('szModel', c_char * 32),  # 探测器类型;device type;
        ('szName', c_char * 32),  # 探测器名称;device name;
        ('szSN', c_char * 32),  # 探测器序列号;device serial-number;
        ('szAreaName', c_char * 32),  # 探测器所属区域名称;Area name;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('szReserverd', c_char * 128),  # 保留字节;Reserved byte;
    ]

class NET_A_ALARM_WIRELESS_DEVBATTERY_LOSS_INFO(Structure):
    """
    事件类型ALARM_WIRELESS_DEVBATTERY_LOSS (探测器电池丢失事件)对应的数据块描述信息
    The description information of the data block corresponding to the event type ALARM_WIRELESS_DEVBATTERY_LOSS (detector battery loss event)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作,1表示持续性事件开始,2表示持续性事件结束;;event action, 1 means the start of the persistent event, 2 means the end of the persistent event;;
        ('nChannelID', c_int),  # 通道号;channel number;
        ('stuTime', NET_TIME_EX),  # 事件发生的时间;Time when the event occurred;
        ('szAreaName', c_char * 32),  # 探测器所属区域名称;The name of the area to which the detector belongs;
        ('szModel', c_char * 32),  # 探测器类型;detector type;
        ('szName', c_char * 32),  # 探测器名称;detector name;
        ('szSN', c_char * 32),  # 探测器序列号;detector serial number;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('szReserved', c_char * 1024),  # 保留字节;reserved bytes;
    ]

class NET_A_ALARM_WIRELESSDEV_LOWPOWER_INFO(Structure):
    """
    无线设备低电量报警事件结构体
    report event of lowpower wireless
    """
    _fields_ = [
        ('emResult', C_ENUM),  # 是否为低电量true低电量,false 电量正常,unknown未知 Refer: NET_THREE_STATUS_BOOL;lowpower event:true lowpower,false narmal, unknown Unknown Refer: NET_THREE_STATUS_BOOL;
        ('stuTime', NET_TIME),  # 事件发生的时间;event time;
        ('nId', c_int),  # 无线设备ID 此字段协议上已废弃;Wireless device ID This field is obsolete on the protocol;
        ('emType', C_ENUM),  # 无线设备类型 Refer: EM_A_NET_WIRELESSDEV_LOWPOWER_TYPE;wirelessdevice type Refer: EM_A_NET_WIRELESSDEV_LOWPOWER_TYPE;
        ('szSN', c_char * 32),  # 无线配件序列号;wirelessdevice Serial Number;
        ('fPercent', c_float),  # 电量百分比;battery percentage;
        ('nIndex', c_int),  # 通道号或探测器地址;channel;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('reserved', C_BYTE * 984),  # 预留;reserved;
    ]

class NET_A_ALARM_MODULE_LOST_INFO(Structure):
    """
    扩展模块掉线事件 对应事件类型 ALARM_MODULE_LOST
    expansion module offline event  corresponding to event type ALARM_MODULE_LOST
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('stuTime', NET_TIME),  # 事件上报时间;event report time;
        ('nSequence', c_int),  # 扩展模块接的总线的序号(从0开始);expansion module BUS no.(from 0);
        ('emBusType', C_ENUM),  # 总线类型 Refer: EM_A_NET_BUS_TYPE;BUS type Refer: EM_A_NET_BUS_TYPE;
        ('nAddr', c_int),  # 掉线的扩展模块数目;offline expansion module quantity;
        ('anAddr', c_int * 256),  # 掉线的扩展模块的序号(从0开始);offline expansionmodule no.(from 0);
        ('szDevType', c_char * 64),  # 设备类型 "SmartLock",是级联设备;当设备类型"AlarmDefence"接口序号为报警序号"LiftController":梯控设备;device type "SmartLock"when type of"AlarmDefence"Index address is Alarm number"LiftController":lift controller;
        ('bOnline', C_BOOL),  # 在线情况,默认FALSE. false:不在线；true:在线;Online status. The default setup is false. False=offline, true=online;
        ('szSN', c_char * 32),  # 无线配件序列号;wirelessdevice Serial Number;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_ALARM_SENSOR_ABNORMAL_INFO(Structure):
    """
    事件类型(ALARM_SENSOR_ABNORMAL) 探测器状态异常报警
    event type (ALARM_SENSOR_ABNORMAL)
    """
    _fields_ = [
        ('nAction', c_int),  # 0:开始 1:停止;0:start 1:stop;
        ('nChannelID', c_int),  # 视频通道号;channel id;
        ('stuTime', NET_TIME_EX),  # 事件发生的时间;UTC time;
        ('emStatus', C_ENUM),  # 探测器状态 Refer: EM_SENSOR_ABNORMAL_STATUS;sensor status Refer: EM_SENSOR_ABNORMAL_STATUS;
        ('emSenseMethod', C_ENUM),  # SenseMethod, 感应方式,参见具体枚举定义 Refer: EM_A_NET_SENSE_METHOD;SenseMethod, refer to the specific enumeration definition. Refer: EM_A_NET_SENSE_METHOD;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('byReserved', C_BYTE * 124),  # 预留字段;Reserved;
    ]

class NET_A_ALARM_INPUT_SOURCE_SIGNAL_INFO(Structure):
    """
    报警输入源事件详情(只要有输入就会产生改事件,不论防区当前的模式,无法屏蔽)
    Alarm Input Source Event Details(As Long As There Will Have to Change The Input Event, Regardless of the Current Mode of The Defence Zone Can not be Shielded)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('nAction', c_int),  # 0:开始 1:停止;0=Start 1=Stop;
        ('stuTime', NET_TIME),  # 报警事件发生的时间;Alarm Event Begin Time;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_ALARM_ARMMODE_CHANGE_INFO(Structure):
    """
    布撤防状态变化事件的信息
    Protect Transformate Event's Information
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('stuTime', NET_TIME),  # 报警事件发生的时间;Alarm Event Begin Time;
        ('bArm', C_ENUM),  # 变化后的状态 Refer: EM_A_NET_ALARM_MODE;Statue of Transformated Refer: EM_A_NET_ALARM_MODE;
        ('emSceneMode', C_ENUM),  # 情景模式 Refer: EM_A_NET_SCENE_MODE;ContextualMode Refer: EM_A_NET_SCENE_MODE;
        ('dwID', C_DWORD),  # ID号, 遥控器编号或键盘地址, emTriggerMode为NET_EM_TRIGGER_MODE_NET类型时为0;ID number, remote control number or keypad address, emTriggerMode=0 when  belong to NET_EM_TRIGGER_MODE_NET;
        ('emTriggerMode', C_ENUM),  # 触发方式 Refer: EM_A_NET_EM_TRIGGER_MODE;trigger mode Refer: EM_A_NET_EM_TRIGGER_MODE;
        ('szNetClientAddr', c_char * 64),  # 网络用户IP地址或网络地址;Net user IP or IP address;
        ('nUserCode', C_UINT),  # 用户ID，0:管理员，1~20：普通用户，21：安装员，22：挟持用户;User ID, 0:administrator, 1~20:ordinary user, 21:setter, 22:hijacked user;
    ]

class NET_A_ALARM_AREAARM_MODECHANGE_INFO(Structure):
    """
    区域防区模式改变事件(对应事件 ALARM_AREAARM_MODECHANGE)
    alarm of area arm mode change(Corresponding to ALARM_AREAARM_MODECHANGE)
    """
    _fields_ = [
        ('nAreaIndex', c_int),  # 区域编号;Area ID;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occurrence time;
        ('emTriggerMode', C_ENUM),  # 操作方式 Refer: EM_AREAARM_TRIGGERMODE;Trigger mode Refer: EM_AREAARM_TRIGGERMODE;
        ('emUser', C_ENUM),  # 操作用户，仅emTriggerMode = EM_AREAARM_USER_USER时有效 Refer: EM_AREAARM_USER;user,useful when emTriggerMode = EM_AREAARM_USER_USER Refer: EM_AREAARM_USER;
        ('nID', C_UINT),  # ID号,emTriggerMode = EM_AREAARM_TRIGGERMODE_KEYPAD表示键盘地址;emTriggerMode =EM_AREAARM_TRIGGERMODE_REMOTECONTROL时表示遥控器编号;ID,emTriggerMode = EM_AREAARM_TRIGGERMODE_KEYPADkeypad address;emTriggerMode =EM_AREAARM_TRIGGERMODE_REMOTECONTROL remote control ID;
        ('emArmState', C_ENUM),  # 布撤防状态 Refer: EM_ARM_STATE;arm state Refer: EM_ARM_STATE;
        ('byReserved', C_BYTE * 1024),  # 保留扩展字节;Reserved Byte;
    ]

class NET_A_ALARM_RCEMERGENCY_CALL_INFO(Structure):
    """
    紧急救助事件详情
    Emergency Help Event Details
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nAction', c_int),  # -1:未知 0:开始 1:停止;0:start 1:stop;
        ('emType', C_ENUM),  # 紧急类型 Refer: EM_RCEMERGENCY_CALL_TYPE;emergency type Refer: EM_RCEMERGENCY_CALL_TYPE;
        ('stuTime', NET_TIME),  # 事件发生时间;event time;
        ('emMode', C_ENUM),  # 报警方式 Refer: EM_RCEMERGENCY_MODE_TYPE;alarm method Refer: EM_RCEMERGENCY_MODE_TYPE;
        ('dwID', C_DWORD),  # 用于标示不同的紧急事件(只有emMode是遥控器类型时有效, 表示遥控器的编号, 0表示无效ID);for different emergency events (only emMode is remote control type, it is valid , means remote control no. , 0 means invalid ID);
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('szDelayUploadSeq', c_char * 128),  # 延时上传序号;Delay Upload Seq;
        ('szResvered', c_char * 1020),  # 保留字节;Reserved Byte;
    ]

class NET_A_ALARM_POWERFAULT_INFO(Structure):
    """
    电源故障事件
    Power Fault Event
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('emPowerType', C_ENUM),  # 电源类型 Refer: EM_POWER_TYPE;Power Type Refer: EM_POWER_TYPE;
        ('emPowerFaultEvent', C_ENUM),  # 电源故障事件 Refer: EM_POWERFAULT_EVENT_TYPE;Power Fault Event Refer: EM_POWERFAULT_EVENT_TYPE;
        ('stuTime', NET_TIME),  # 报警事件发生的时间;Alarm Event Begin Time;
        ('nAction', c_int),  # 0:开始 1:停止;0=Start 1=Stop;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_ALARM_BATTERYLOWPOWER_INFO(Structure):
    """
    电池电压过低报警
    battery low power alarm info
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nAction', c_int),  # 0:开始 1:停止;0:start 1:stop;
        ('nBatteryLeft', c_int),  # 剩余电量百分比,单位%;battery left, unit:%;
        ('stTime', NET_TIME),  # 事件发生时间;event happen time;
        ('nChannelID', c_int),  # 通道号, 标识子设备电池, 从0开始;channel no. Mark sub-device battery. Begins with 0.;
        ('stGPSStatus', NET_GPS_STATUS_INFO),  # GPS信息;GPS info;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_ALARM_CHASSISINTRUDED_INFO(Structure):
    """
    防拆报警事件
    Tamper Alarm Event
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nAction', c_int),  # 0:开始 1:停止;0=Start 1=Stop;
        ('stuTime', NET_TIME),  # 报警事件发生的时间;Alarm Event Begin Time;
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('szReaderID', c_char * 32),  # 读卡器ID;Reader ID;
        ('nEventID', C_UINT),  # 事件ID;event id;
        ('szSN', c_char * 32),  # 无线设备序列号;wireless device serial number;
        ('bRealUTC', C_BOOL),  # RealUTC 是否有效，bRealUTC 为 TRUE 时，用 RealUTC，否则用 stuTime 字段;whether RealUTC is valid. when bRealUTC is TRUE, use RealUTC, otherwise use stuTime;
        ('RealUTC', NET_TIME_EX),  # 事件发生的时间（标准UTC）;Event occur time;
        ('emDevType', C_ENUM),  # 设备类型 Refer: EM_ALARM_CHASSISINTRUDED_DEV_TYPE;Equipment type Refer: EM_ALARM_CHASSISINTRUDED_DEV_TYPE;
    ]

class NET_A_ALARM_PSTN_BREAK_LINE_INFO(Structure):
    """
    PSTN掉线事件
    PSTN offline event
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannelID', c_int),  # 电话线序号(从0开始);tel wire no.(from 0);
        ('nAction', c_int),  # 0:开始 1:停止;0:start  1:stop;
        ('stuTime', NET_TIME),  # 事件发生的时间;event time;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_ALARM_NOGSMFIELD_INFO(Structure):
    """
    事件类型ALARM_NOGSMFIELD(通信模块掉线或者sim没插事件)对应数据块描述信息
    Alarm of Comunicating module offline or no sim card(Corresponding to ALARM_NOGSMFIELD)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作,1表示持续性事件开始,2表示持续性事件结束;;Event operation,1:Start 2:Stop;
        ('UTC', NET_TIME_EX),  # 事件发生时间;Event occurrence time;
        ('emFaultType', C_ENUM),  # 通讯错误类型 Refer: EM_A_GSMFIELD_FAULT_TYPE;Fault type Refer: EM_A_GSMFIELD_FAULT_TYPE;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_ALARM_SIREN_TAMPER_INFO(Structure):
    """
    事件类型ALARM_SIREN_TAMPER (警号防拆事件)对应的数据块描述信息
    The description information of the data block corresponding to the event type ALARM_SIREN_TAMPER (alarm tamper event)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作,1表示持续性事件开始,2表示持续性事件结束;;Event action, 1 means the continuous event starts, 2 means the continuous event ends;
        ('nChannelID', c_int),  # 通道号;Channel number;
        ('stuTime', NET_TIME_EX),  # 事件发生的时间;Time when the event occurred;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('szReserved', c_char * 1024),  # 保留字节;reserved bytes;
    ]

class NET_A_ALARM_KEYPAD_TAMPER_INFO(Structure):
    """
    事件类型ALARM_KEYPAD_TAMPER (键盘防拆事件)对应的数据块描述信息
    The description of the data block corresponding to the event type ALARM_KEYPAD_TAMPER (keyboard tampering event)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作,1表示持续性事件开始,2表示持续性事件结束;;Event action, 1 means the continuous event starts, 2 means the continuous event ends;;
        ('nChannelID', c_int),  # 通道号;Channel number;
        ('stuTime', NET_TIME_EX),  # 事件发生的时间;Time when the event occurred;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('szReserved', c_char * 1024),  # 保留字节;reserved bytes;
    ]

class NET_A_ALARM_KEYPAD_LOCK_INFO(Structure):
    """
    事件类型ALARM_KEYPAD_LOCK (键盘锁定事件)对应的数据块描述信息
    The description information of the data block corresponding to the event type ALARM_KEYPAD_LOCK (keyboard lock event)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作,1表示持续性事件开始,2表示持续性事件结束;;Event action, 1 means the continuous event starts, 2 means the continuous event ends;
        ('nChannelID', c_int),  # 通道号;Channel number;
        ('stuTime', NET_TIME_EX),  # 事件发生的时间;Time when the event occurred;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('szReserved', c_char * 1024),  # 保留字节;reserved bytes;
    ]

class NET_A_ALARM_KEYPAD_FAILURE_INFO(Structure):
    """
    事件类型ALARM_KEYPAD_FAILURE (键盘掉线事件)对应的数据块描述信息
    The description information of the data block corresponding to the event type ALARM_KEYPAD_FAILURE (keyboard failure event)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作,1表示持续性事件开始,2表示持续性事件结束;;Event action, 1 means the continuous event starts, 2 means the continuous event ends;;
        ('nChannelID', c_int),  # 通道号;Channel number;
        ('stuTime', NET_TIME_EX),  # 事件发生的时间;Time when the event occurred;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('szReserved', c_char * 1024),  # 保留字节;reserved bytes;
    ]

class NET_ARM_OPTIONS(Structure):
    """
    布撤防详细信息
    Arming and disarming details
    """
    _fields_ = [
        ('emSceneMode', C_ENUM),  # 情景模式 Refer: EM_A_NET_EM_SCENE_MODE;Scene mode Refer: EM_A_NET_EM_SCENE_MODE;
        ('emAreaarmTriggerMode', C_ENUM),  # 触发方式 Refer: EM_AREAARM_TRIGGERMODE;Trigger method Refer: EM_AREAARM_TRIGGERMODE;
        ('nId', c_int),  # 触发者编号，如用户编号、键盘地址、遥控器编号、定时器编号或key类型防区号;Trigger number, such as user number, keyboard address, remote control number, timer number or key type zone number;
        ('szName', c_char * 64),  # 触发者名称，如用户名称，键盘名称等;Trigger name, such as user name, keyboard name, etc.;
        ('szClientAddress', c_char * 64),  # 网络用户IP地址或网络地址，对于TriggerMode为Remote时，需要填写此项;The IP address or network address of the network user, when TriggerMode is Remote, this field is required;
        ('bReserved', C_BYTE * 132),  # 预留字节;Reserved byte;
    ]

class NET_DETAIL_INFO(Structure):
    """
    执行布撤防时的附加信息
    Additional information when performing arming and disarming
    """
    _fields_ = [
        ('stuArmOption', NET_ARM_OPTIONS),  # 布撤防详细信息;Arming and disarming details;
        ('byReserved', C_BYTE * 128),  # 预留字节;Reserved byte;
    ]

class NET_IN_SET_ALARMMODE(Structure):
    """
    设置布防模式 输入参数。此时CLIENT_SetAlarmRegionInfo的emType参数为NET_EM_SET_ALARMREGION_INFO_ARMMODE
    CLIENT_SetAlarmRegionInfo NET_EM_SET_ALARMREGION_INFO_ARMMODE input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('emArmType', C_ENUM),  # 布撤防类型 Refer: EM_ARM_TYPE;arm type Refer: EM_ARM_TYPE;
        ('szPwd', c_char * 256),  # 密码;password;
        ('nAreaNum', c_int),  # 区域的个数;area number;
        ('arrAreas', c_int * 8),  # 区域号;area id;
        ('stuDetail', NET_DETAIL_INFO),  # 执行布撤防时的附加信息;Additional information when performing arming and disarming;
        ('nAreaNumEx', c_int),  # 区域的扩展个数;Number of areas to expand;
        ('arrAreasEx', c_int * 64),  # 区域号扩展 个数超过8个使用这个字段;Use this field if the number of area number extension exceeds 8;
    ]

class NET_A_ARM_FAILED_DETAIL(Structure):
    """
    布防失败细节
    failed detail
    """
    _fields_ = [
        ('nArea', c_int),  # 布防失败的区域号;failed area id;
        ('nAlarmSourceRet', c_int),  # 报警源输入返回个数;alarm source return number;
        ('arrAlarmSource', c_int * 72),  # 区域下包含的有源输入的防区;alarm source number;
        ('byReserved', C_BYTE * 1024),  # 保留字节;reserved;
    ]

class NET_ZONE_ABNORMAL_INFO(Structure):
    """
    异常防区信息
    Abnormal zone information
    """
    _fields_ = [
        ('nIndex', c_int),  # 防区号;Zone code;
        ('szName', c_char * 32),  # 防区名称;Zoom name;
        ('szReason', c_char * 32),  # 异常原因，异常原因，平台直接取值做显示即可;Exception reason, exception reason, the platform can directly display the value;
        ('byReserved', C_BYTE * 188),  # 保留字节;reserved;
    ]

class NET_A_ARM_FAILED_DETAIL_EX(Structure):
    """
    布防失败细节扩展字段
    Armed failure details extended field
    """
    _fields_ = [
        ('nArea', c_int),  # 布防失败的区域号;Number of the area that failed to arm;
        ('nAlarmSourceRetEx', c_int),  # 报警源输入返回个数;Number of alarm source input returns;
        ('arrAlarmSourceEx', c_int * 256),  # 区域下包含的有源输入的防区;The active input defense zone contained under the zone;
        ('nZoneAbnormalNum', c_int),  # 异常防区信息个数;Number of abnormal zone information;
        ('stuZoneAbnormal', NET_ZONE_ABNORMAL_INFO * 1024),  # 异常防区信息，最大有1024个;Abnormal zone information, maximum 1024;
    ]

class NET_DEVICE_FAULT_INFO(Structure):
    """
    设备异常信息
    Equipment exception information
    """
    _fields_ = [
        ('szName', c_char * 32),  # 设备名称;Device Name;
        ('szReason', c_char * 32),  # 异常原因，平台直接取值做显示即可;The reason for the exception, the platform can directly display the value;
        ('byReserved', C_BYTE * 512),  # 保留字节;reserved;
    ]

class NET_OUT_SET_ALARMMODE(Structure):
    """
    设置布防模式 输出参数。此时CLIENT_SetAlarmRegionInfo的emType参数为NET_EM_SET_ALARMREGION_INFO_ARMMODE
    CLIENT_SetAlarmRegionInfo NET_EM_SET_ALARMREGION_INFO_ARMMODE output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nArmResult', c_int),  # 布防结果 0:成功 1:失败;result 0:succeed 1:failed;
        ('nFailedAreaRet', c_int),  # 布防失败的区域个数;failed area number;
        ('stuFailedDetail', NET_A_ARM_FAILED_DETAIL * 8),  # 布防失败的细节;failed detail;
        ('nFailedDetailNum', c_int),  # 布防失败个数, 最大值为64;The number of failed deployments, the maximum is 64;
        ('pstuFailedDetailEx', POINTER(NET_A_ARM_FAILED_DETAIL_EX)),  # 布防失败的细节扩展字段 布防个数大于8个使用此字段;Expansion field for details of failed deployment;
        ('nDeviceFaultNum', c_int),  # 异常设备信息个数;Number of abnormal device information;
        ('stuDeviceFault', NET_DEVICE_FAULT_INFO * 256),  # 设备异常信息，最大支持256个;Device abnormal information, maximum support 256;
    ]

class NET_IN_SET_BYPASSMODE(Structure):
    """
    设置旁路状态 输入参数。此时CLIENT_SetAlarmRegionInfo的emType参数为NET_EM_SET_ALARMREGION_INFO_BYPASSMODE
    CLIENT_SetAlarmRegionInfo NET_EM_SET_ALARMREGION_INFO_BYPASSMODE input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('szPwd', c_char * 256),  # 密码;password;
        ('emType', C_ENUM),  # 旁路模式 Refer: EM_BYPASSMODE_TYPE;bypass mode Refer: EM_BYPASSMODE_TYPE;
        ('nZoneNum', c_int),  # 防区个数;zone number;
        ('arrZones', c_int * 72),  # 防区号;zone id;
        ('nZoneNumEx', c_int),  # 防区个数扩展;zone number extend;
        ('arrZonesEx', c_int * 256),  # 防区号扩展，超过72时使用此字段;Zone code extension, use this field when it exceeds 72;
    ]

class NET_OUT_SET_BYPASSMODE(Structure):
    """
    设置旁路状态 输出参数，此时CLIENT_SetAlarmRegionInfo的emType参数为NET_EM_SET_ALARMREGION_INFO_BYPASSMODE
    CLIENT_SetAlarmRegionInfo NET_EM_SET_ALARMREGION_INFO_BYPASSMODE output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_IN_SET_OUTPUT_STATE(Structure):
    """
    设置输出状态 输入参数。此时CLIENT_SetAlarmRegionInfo的emType参数为NET_EM_SET_ALARMREGION_INFO_OUTPUTSTATE
    CLIENT_SetAlarmRegionInfo NET_EM_SET_ALARMREGION_INFO_OUTPUTSTATE input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('emType', C_ENUM),  # 输出类型 Refer: EM_OUTPUT_TYPE;output type Refer: EM_OUTPUT_TYPE;
        ('nChannel', c_int),  # emType= EM_OUTPUT_TYPE_SIREN时表示警号号emType= EM_OUTPUT_TYPE_ALARMOUT时表示通道号;emType= EM_OUTPUT_TYPE_SIREN: sirenemType= EM_OUTPUT_TYPE_ALARMOUT: channel id;
        ('action', c_bool),  # 输出动作false:关闭true:打开;output action false:close true:open;
        ('byReserved', C_BYTE * 3),  # 字节对齐;reserved;
    ]

class NET_OUT_SET_OUTPUT_STATE(Structure):
    """
    设置输出状态输出参数。此时CLIENT_SetAlarmRegionInfo的emType参数为NET_EM_SET_ALARMREGION_INFO_OUTPUTSTATE
    CLIENT_SetAlarmRegionInfo NET_EM_SET_ALARMREGION_INFO_OUTPUTSTATE output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_IN_GET_ALARMCAPS(Structure):
    """
    获取能力 输入参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_ALARMCAPS
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_ALARMCAPS input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct;
    ]

class NET_PARTIAL_ARM(Structure):
    """
    Partial Arm的配置信息
    Partial Arm's config information
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 是否支持Partial Arm。当bSupportArmProfile不使能时，才支持显示Partial布防。;Whether partial arm is supported. When supportarmprofile is not enabled, partial deployment is supported.;
        ('nIndex', c_int),  # 指示Partial N布防，比如Index为1时，支持Partial1布防;Indicates partial n deployment. For example, when index is 1, partial1 deployment is supported;
        ('byReserved', C_BYTE * 64),  # 预留字节;Reserved bytes;
    ]

class NET_AREA_ARM_MODE(Structure):
    """
    布撤防模式信息
    Deployment and withdrawal mode information
    """
    _fields_ = [
        ('bOutDoor', C_BOOL),  # 是否支持显示外出布防，当bSupportArmProfile使能时，才支持显示外出布防。执行setArmMode接口的布防模式参数为"T";Whether to support the display of out of office deployment. Only when bSupportarmprofile is enabled can it be displayed. The deployment mode parameter of executing setarmmode interface is "t";
        ('bAtHome', C_BOOL),  # 是否支持显示留守布防,当bSupportArmProfile使能时，才支持显示留守布防。执行setArmMode接口的布防模式参数为"p1";Whether to support display stay arming, when bSupportArmProfile is enabled, display stay arming is supported. The arming mode parameter of the setArmMode interface is "p1";
        ('bTotalArm', C_BOOL),  # 是否支持Total布防。当bSupportArmProfile不使能时，才支持显示Total布防。;Whether to support Total arming. When bSupportArmProfile is not enabled, Total Arming is supported.;
        ('nPartialArmNum', c_int),  # 是否支持Partial Arm的个数;Whether to support the number of Partial Arm;
        ('stuPartialArm', NET_PARTIAL_ARM * 4),  # 是否支持Partial Arm，最多支持4个;Whether to support Partial Arm, up to 4;
        ('bDisArm', C_BOOL),  # 是否支持撤防。一般默认都需要显示撤防;Whether to support disarming. Generally, it is necessary to display disarm by default;
        ('byReserved', C_BYTE * 516),  # 预留字节;Reserved bytes;
    ]

class NET_SUPPORT_MULITSIM_CARDS(Structure):
    """
    支持的SIM卡信息
    Supported SIM card information
    """
    _fields_ = [
        ('nIndex', c_int),  # sim卡标识;sim card identification;
        ('bEnable', C_BOOL),  # 是否启用;Whether to enable;
        ('bReserved', C_BYTE * 64),  # 预留字节;Reserved byte;
    ]

class NET_OUT_GET_ALARMCAPS(Structure):
    """
    获取能力 输出参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_ALARMCAPS
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_ALARMCAPS output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nSiren', c_int),  # 支持的警号数量;supported siren number;
        ('nAlarmIn', c_int),  # 支持的报警输入数量;supported input alarm number;
        ('nAlarmOut', c_int),  # 支持的报警输出数量, 最多82个;supported output alarm number, max:82;
        ('nRemoteControl', c_int),  # 支持的遥控器数量;supported remotecontrol number;
        ('nICCard', c_int),  # 支持的IC卡数量;Number of IC cards supported;
        ('nKeypad', c_int),  # 支持的键盘数量;Number of keyboards supported;
        ('nTelephoneNumber', c_int),  # 支持的电话号码数量;Number of phone numbers supported;
        ('nKeypadUserCount', c_int),  # 支持的键盘用户数量;Number of keyboard users supported;
        ('nAlarmAreas', c_int),  # 支持的Area（也可称为子系统）数量;Number of areas (also called subsystems) supported;
        ('bSupportOneClickArmMode', C_BOOL),  # 是否支持主机一键布撤防;Whether to support one-key arming and disarming of the host;
        ('bSupportDefenceArmMode', C_BOOL),  # 是否支持单防区布撤防;Whether to support single zone arming and disarming;
        ('bSupportArmProfile', C_BOOL),  # 是否启用布防的情景模式;Whether to enable the armed scene mode;
        ('stuAreaArmMode', NET_AREA_ARM_MODE),  # 布撤防模式;Arming and disarming mode;
        ('nZoomNum', c_int),  # 防区工作模式个数;Number of working modes of defense zone;
        ('emZoomMode', C_ENUM * 16),  # 支持的防区工作模式 Refer: EM_BYPASSMODE_TYPE;Supported zone working mode Refer: EM_BYPASSMODE_TYPE;
        ('bSupportAlarmClear', C_BOOL),  # 是否支持消警命令;Whether to support the alarm command;
        ('nNetworkUserCount', c_int),  # 支持的网络用户数量;Number of network users supported;
        ('nSupportMultiSIMCardsNum', c_int),  # 支持的SIM个数;Number of SIMs supported;
        ('stuSupportMultiSIMCards', NET_SUPPORT_MULITSIM_CARDS * 8),  # 支持的SIM卡信息;Supported SIM card information;
    ]

class NET_IN_GET_ALARMMODE(Structure):
    """
    获取布防模式 输入参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_ARMMODE
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_ARMMODE input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_ARMMODE_INFO(Structure):
    """
    布撤防信息
    armmode information
    """
    _fields_ = [
        ('emArmState', C_ENUM),  # 布撤防状态 Refer: EM_ARM_STATE;arm state Refer: EM_ARM_STATE;
        ('byReserved', C_BYTE * 1024),  # 保留字节;reserved;
    ]

class NET_OUT_GET_ALARMMODE(Structure):
    """
    获取布防模式 输出参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_ARMMODE
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_ARMMODE output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nArmModeRet', c_int),  # 布撤防状态个数;arm state number;
        ('stuArmMode', NET_ARMMODE_INFO * 8),  # 布撤防信息;arm mode information;
        ('nArmModeRetEx', c_int),  # 布撤防状态个数扩展 超过8个请使用这个字段;The number of arming and disarming states is expanded. If more than 8, please use this field.;
        ('stuArmModeEx', NET_ARMMODE_INFO * 64),  # 布撤防信息;Arming and disarming information;
    ]

class NET_IN_GET_BYPASSMODE(Structure):
    """
    获取旁路状态 输入参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_BYPASSMODE
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_BYPASSMODE input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nZoneNum', c_int),  # 防区个数;zone number;
        ('arrZones', c_int * 72),  # 防区号;zone id;
        ('nZoneNumEx', c_int),  # 防区个数扩展;zone number extend;
        ('arrZonesEx', c_int * 256),  # 防区号扩展  超过72使用这个字段;Zone code extension, use this field when it exceeds 72;
    ]

class NET_OUT_GET_BYPASSMODE(Structure):
    """
    获取旁路状态 输出参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_BYPASSMODE
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_BYPASSMODE output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nZoneRet', c_int),  # 防区个数;zone number;
        ('arrModes', C_ENUM * 72),  # 防区工作模式 Refer: EM_BYPASSMODE_TYPE;bypass mode Refer: EM_BYPASSMODE_TYPE;
        ('nZoneRetEx', c_int),  # 防区个数扩展;Number of defense zones expanded;
        ('arrModesEx', C_ENUM * 256),  # 防区号扩展  超过72使用这个字段 Refer: EM_BYPASSMODE_TYPE;Zone code extension Use this field for more than 72 Refer: EM_BYPASSMODE_TYPE;
    ]

class NET_IN_GET_AREAZONES(Structure):
    """
    获取区域防区信息 输入参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_AREAZONES
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_AREAZONES input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nAreaNum', c_int),  # 区域个数;area number;
        ('arrArea', c_int * 8),  # 区域号;area id;
        ('nAreaNumEx', c_int),  # 区域个数;area number extend;
        ('arrAreaEx', c_int * 64),  # 区域号扩展 区域个数超过8使用这个字段;Area number extension Use this field if the number of areas exceeds 8;
    ]

class NET_AREA_INFO(Structure):
    """
    区域信息
    area information
    """
    _fields_ = [
        ('nArea', c_int),  # 区域号;arae id;
        ('nZoneRet', c_int),  # 区域下的防区个数;zone number;
        ('arrZones', c_int * 72),  # 区域下的防区号;zone id;
        ('byReserved', C_BYTE * 1024),  # 保留字段;reserved;
    ]

class NET_AREA_INFO_EX(Structure):
    """
    区域信息扩展字段
    area information extend
    """
    _fields_ = [
        ('nArea', c_int),  # 区域号;arae id;
        ('nZoneRetEx', c_int),  # 区域下的防区个数扩展;zone number extend;
        ('arrZonesEx', c_int * 256),  # 区域下的防区号;zone id;
        ('byReserved', C_BYTE * 1024),  # 保留字段;reserved;
    ]

class NET_ZONES_INFO(Structure):
    """
    防区信息
    Sector information
    """
    _fields_ = [
        ('nIndex', c_int),  # 防区号;Zone code;
        ('szName', c_char * 128),  # 防区名称;Zone Name;
        ('nSupPartial', C_UINT),  # 第0位为1，表示支持Partial1 第1位为1，表示支持Partial2;Bit 0 is 1, which means partial1 is supported, and bit 1 is 1, which means partial2 is supported;
        ('byReserved', C_BYTE * 512),  # 保留字段;reserved;
    ]

class NET_AREA_INFO_EX_SUPPLEMENT(Structure):
    """
    区域信息扩展字段补充字段 与 NET_AREA_INFO_EX 的合集表示区域信息
    Area information extension supplementary field  The set with NET_AREA_INFO_EX represents region information
    """
    _fields_ = [
        ('stuZonesInfo', NET_ZONES_INFO * 256),  # 防区信息;Sector information;
        ('szAreaName', c_char * 128),  # 区域名称;Area name;
        ('byReserved', C_BYTE * 1024),  # 保留字段;reserved;
    ]

class NET_OUT_GET_AREAZONES(Structure):
    """
    获取区域防区信息 输出参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_AREAZONES
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_AREAZONES output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nAreaRet', c_int),  # 区域个数;area number;
        ('stuAreaInfo', NET_AREA_INFO * 8),  # 区域信息;area information;
        ('nAreaRetEx', c_int),  # 区域个数;area number extend;
        ('stuAreaInfoEx', NET_AREA_INFO_EX * 64),  # 区域信息扩展 超过8个防区使用此字段;Area information expansion More than 8 zones use this field;
        ('stuAreaInfoExSupplement', NET_AREA_INFO_EX_SUPPLEMENT * 64),  # 区域信息扩展补充字段;Area information extension supplementary field;
    ]

class NET_IN_GET_ALLINSLOTS(Structure):
    """
    获取所有报警防区 输入参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_ALLINSLOTS
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_ALLINSLOTS input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_OUT_GET_ALLINSLOTS(Structure):
    """
    获取所有报警防区 输出参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_ALLINSLOTS
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_ALLINSLOTS output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nLocol', c_int),  # 本地防区数量, 最多8个;local zone number, max:8;
        ('nWired', c_int),  # 有线防区数量, 最多64个;wired zone number, max:64;
        ('nWireless', c_int),  # 无线防区数量, 最多64个;wireless zone number, max:64;
    ]

class NET_IN_GET_ALLOUTSLOTS(Structure):
    """
    获取所有报警输出 输入参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_ALLOUTSLOTS
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_ALLOUTSLOTS input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_OUT_GET_ALLOUTSLOTS(Structure):
    """
    获取所有报警输出 输出参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_ALLOUTSLOTS
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_ALLOUTSLOTS output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nLocol', c_int),  # 本地报警输出数量, 最多2个;local alarm output number, max:2;
        ('nWired', c_int),  # 扩展有线报警输出数量, 最多80个;wired alarm output number, max:80;
        ('nWireless', c_int),  # 扩展无线报警输出数量, 最多80个;wired alarm output number, max:80;
    ]

class NET_IN_GET_CONNECTIONSTATUS(Structure):
    """
    获取防区练连接状态 输入参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_ZONECONNECTIONSSTATUS
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_ZONECONNECTIONSSTATUS input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_OUT_GET_CONNECTIONSTATUS(Structure):
    """
    获取防区连接状态 输出参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_ZONECONNECTIONSSTATUS
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_ZONECONNECTIONSSTATUS output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nZoneRet', c_int),  # 防区个数;zone number;
        ('arrZoneStates', c_bool * 72),  # 防区在线状态false:离线 true:在线;zone state false:offline true:online;
        ('nZoonRetEx', c_int),  # 防区个数扩展;Number of defense zones expanded;
        ('arrZoneStatesEx', C_BOOL * 256),  # 防区在线状态扩展FALSE:离线 TRUE:在线，防区个数超过72使用这个字段;Defense zone online status extension FALSE: Offline TRUE: Online, use this field if the number of defense zones exceeds 72;
    ]

class NET_IN_GET_AREAS_STATUS(Structure):
    """
    获取区域状态 输入参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_AREASTATUS
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_AREASTATUS input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('emType', C_ENUM),  # 获取异常防区类型 Refer: EM_GET_AREASSTATUS_TYPE;get area status type Refer: EM_GET_AREASSTATUS_TYPE;
    ]

class NET_ZONE_STATUS(Structure):
    """
    防区异常信息
    zone status
    """
    _fields_ = [
        ('nIndex', c_int),  # 防区号;zone id;
        ('emStatus', C_ENUM),  # 防区异常状态 Refer: EM_ZONE_STATUS;zone statu Refer: EM_ZONE_STATUS;
        ('byReserved', C_BYTE * 1024),  # 保留字节;reserved;
    ]

class NET_AREA_STATUS(Structure):
    """
    区域异常防区信息
    area status
    """
    _fields_ = [
        ('nArea', c_int),  # 区域号;area id;
        ('nZoneRet', c_int),  # 防区个数;zone number;
        ('stuZoneStatus', NET_ZONE_STATUS * 72),  # 防区异常状态;zone status;
        ('byReserved', C_BYTE * 1024),  # 保留字节;reserved;
    ]

class NET_AREA_STATUS_EX(Structure):
    """
    区域异常防区信息扩展
    Area abnormal defense zone information expansion
    """
    _fields_ = [
        ('nArea', c_int),  # 区域号;rea id;
        ('nZoneRetEx', c_int),  # 防区个数扩展;zone number extend;
        ('stuZoneStatusEx', NET_ZONE_STATUS * 256),  # 防区异常状态;zone status;
        ('byReserved', C_BYTE * 1024),  # 保留字节;reserved;
    ]

class NET_OUT_GET_AREAS_STATUS(Structure):
    """
    获取区域状态 输出参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_AREASTATUS
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_AREASTATUS output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nAreaRet', c_int),  # 区域个数;area size;
        ('stuAreaStatus', NET_AREA_STATUS * 8),  # 区域防区异常状态信息;area status;
        ('nAreaRetEx', c_int),  # 区域个数扩展;area size extend;
        ('stuAreaStatusEx', NET_AREA_STATUS_EX * 64),  # 区域防区异常状态信息扩展，区域个数超过8个使用这个字段;The abnormal status information of the area defense zone is expanded. Use this field for more than 8 areas;
    ]

class NET_IN_GET_OUTPUT_STATE(Structure):
    """
    获取输出状态 输入参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_OUTPUTSTATE
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_OUTPUTSTATE input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('emType', C_ENUM),  # 通道类型 Refer: EM_OUTPUT_TYPE;channel type Refer: EM_OUTPUT_TYPE;
    ]

class NET_OUT_GET_OUTPUT_STATE(Structure):
    """
    获取输出状态 输出参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_OUTPUTSTATE
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_OUTPUTSTATE output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nStateRet', c_int),  # 状态个数;state number;
        ('arrStates', c_bool * 82),  # 状态false:关闭true打开;state false:close  true:open;
        ('byReserved', C_BYTE * 6),  # 对齐;align;
        ('nStateRetEx', c_int),  # 状态个数扩展 超过82个使用这个字段;The number of states is expanded to more than 82 use this field;
        ('arrStatesEx', C_BOOL * 256),  # 状态FLASE:关闭TRUE打开;Status FLASE: closed TRUE open;
        ('byReserved1', C_BYTE * 4),  # 对齐;align;
    ]

class NET_IN_GET_ZONES_TROUBLE(Structure):
    """
    获取防区故障 输入参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_ZONESTROUBLE
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_ZONESTROUBLE input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_ZONE_TROUBLE_INFO(Structure):
    """
    防区故障信息
    trouble information
    """
    _fields_ = [
        ('nIndex', c_int),  # 防区号;zone id;
        ('emTroubleType', C_ENUM),  # 故障类型 Refer: EM_ZONE_TROUBLE_TYPE;trouble type Refer: EM_ZONE_TROUBLE_TYPE;
        ('byReserved', C_BYTE * 1024),  # 保留字节;reserved;
    ]

class NET_OUT_GET_ZONES_TROUBLE(Structure):
    """
    获取防区故障 输出参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_ZONESTROUBLE
    CLIENT_GetAlarmRegionInfo NET_EM_GET_ALARMREGION_INFO_ZONESTROUBLE output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nZoneRet', c_int),  # 故障防区个数;zone number;
        ('stuTroubleInfo', NET_ZONE_TROUBLE_INFO * 72),  # 防区故障信息;trouble information;
        ('nZoneRetEx', c_int),  # 故障防区个数扩展;zone number extend;
        ('stuTroubleInfoEx', NET_ZONE_TROUBLE_INFO * 256),  # 防区故障信息扩展个数超过72使用这字段;Use this field if the number of zone fault information extension exceeds 72;
    ]

class NET_CHANNELS_STATE_CONDITION(Structure):
    """
    获取通道状态查询条件
    query conditions for get channel status
    """
    _fields_ = [
        ('emType', C_ENUM),  # 通道类型 Refer: EM_CHANNELS_STATE_TYPE;type Refer: EM_CHANNELS_STATE_TYPE;
        ('byReserved', C_BYTE * 1020),  # 保留字节;Reserved;
    ]

class NET_IN_GET_CHANNELS_STATE(Structure):
    """
    获取通道状态 输入参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_CHANNELSSTATE
    CLIENT_GetAlarmRegionInfo InParam. emType is NET_EM_GET_ALARMREGION_INFO_CHANNELSSTATE
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('stuCondition', NET_CHANNELS_STATE_CONDITION),  # 获取通道状态查询条件;query conditions for get channel status;
    ]

class NET_SENSOR_STATE(Structure):
    """
    探测器状态信息
    Sensor State info
    """
    _fields_ = [
        ('nExPowerState', c_int),  # 外接电源连接状态 : 0:正常, 1:未连接;External power connection status: 0: normal, 1: not connected;
        ('nTamper', c_int),  # 配件防拆状态 : 0:正常, 1:打开;Accessory Tamper Status: 0: Normal, 1: Open;
        ('nLowPowerState', c_int),  # 电池电量状态 : 0:正常, 1:低电量, 2:掉电;Battery power status: 0: normal, 1: low power, 2: power down;
        ('szReserved', c_char * 244),  # 保留字节;reserved bytes;
    ]

class NET_CHANNELS_STATE(Structure):
    """
    通道状态
    channels state
    """
    _fields_ = [
        ('emType', C_ENUM),  # 通道类型 Refer: EM_CHANNELS_STATE_TYPE;Type Refer: EM_CHANNELS_STATE_TYPE;
        ('nIndex', C_UINT),  # 通道号;Index for channels;
        ('emOnlineState', C_ENUM),  # 在线状态 Refer: EM_DEV_STATUS;Online state Refer: EM_DEV_STATUS;
        ('emAlarmState', C_ENUM),  # 报警状态，当emType为EM_CHANNELS_STATE_TYPE_ALARMIN时有效 Refer: EM_ZONE_STATUS;Alarm state, valid when emType is EM_CHANNELS_STATE_TYPE_ALARMIN Refer: EM_ZONE_STATUS;
        ('emOutputState', C_ENUM),  # 输出状态，当emType为EM_CHANNELS_STATE_TYPE_ALARMOUT,EM_CHANNELS_STATE_TYPE_SIREN时有效 Refer: EM_OUTPUT_STATE;Output state, valid when emType is EM_CHANNELS_STATE_TYPE_ALARMOUT, EM_CHANNELS_STATE_TYPE_SIREN Refer: EM_OUTPUT_STATE;
        ('szName', c_char * 64),  # 通道对应名称;channel name;
        ('szSN', c_char * 32),  # 通道对应SN号;channel SN;
        ('stuSensorState', NET_SENSOR_STATE),  # 探测器状态信息;Sensor State info;
        ('byReserved', C_BYTE * 60),  # 保留字节;Reserved;
    ]

class NET_OUT_GET_CHANNELS_STATE(Structure):
    """
    获取通道状态 输出参数。此时CLIENT_GetAlarmRegionInfo的emType参数为NET_EM_GET_ALARMREGION_INFO_CHANNELSSTATE
    CLIENT_GetAlarmRegionInfo OutParam. emType is NET_EM_GET_ALARMREGION_INFO_CHANNELSSTATE
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nChannelsStatesCount', C_UINT),  # 通道状态个数;Count of channel states;
        ('stuChannelsStates', NET_CHANNELS_STATE * 1024),  # 通道状态;Channel state;
    ]

class NET_A_DEV_NTP_CFG(Structure):
    """
    NTP配置
    NTP setup
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 是否启用;Enable or not;
        ('nHostPort', c_int),  # NTP服务器默认端口为123;NTP  server default port is 123;
        ('szHostIp', c_char * 32),  # 主机IP;Host IP;
        ('szDomainName', c_char * 128),  # 域名;Domain name;
        ('nType', c_int),  # 不可设置,0：表示IP,1：表示域名,2：表示IP和域名;Read only ,0:IP,1:domain name ,2:IP and domain name;
        ('nUpdateInterval', c_int),  # 更新时间(分钟);Update time(minute);
        ('nTimeZone', c_int),  # 见TIME_ZONE_TYPE;Please refer to TIME_ZONE_TYPE;
        ('reserved', c_char * 128),
    ]

class NET_RELATING_VIDEO_INFO(Structure):
    """
    违章关联的多个视频信息
    Multiple video information related to violation
    """
    _fields_ = [
        ('szVideoPath', c_char * 256),  # 违章关联视频FTP上传路径;FTP upload path of violation related video;
        ('szReserved', c_char * 128),  # 保留字节;reserved bytes;
    ]

class NET_A_DEV_EVENT_TIREDPHYSIOLOGICAL_INFO(Structure):
    """
    事件类型EVENT_IVS_TIREDPHYSIOLOGICAL(生理疲劳驾驶事件)对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_TRAFFIC_TIREDPHYSIOLOGICAL(physiological fatigue driving events)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('bReserved1', c_char * 4),  # 字节对齐;Byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Timestamp (in milliseconds);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Time for the event occurred;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('nAction', c_int),  # 0:脉冲 1:开始 2:停止;event action, 0: Pulse, 1: Start, 2: Stop;
        ('stuGPSStatus', NET_GPS_STATUS_INFO),  # GPS信息;GPS info;
        ('szDriverID', c_char * 32),  # 司机ID;Driver ID;
        ('szVideoPath', c_char * 256),  # 违章关联视频FTP上传路径;ftp path for assocated video;
        ('nRelatingVideoInfoNum', c_int),  # 违章关联的多个视频信息个数;Number of multiple video information associated with violation;
        ('stuRelatingVideoInfo', NET_RELATING_VIDEO_INFO * 16),  # 违章关联的多个视频信息数组，最多支持16个视频;Multiple video information arrays associated with violations, supporting up to 16 videos;
        ('bReserved', C_BYTE * 736),  # 保留字节,留待扩展.;Reserved;
    ]

class NET_A_DEV_EVENT_DRIVERYAWN_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_DRIVERYAWN (开车打哈欠事件) 对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_TRAFFIC_DRIVERYAWN (Event of driver yawn)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('szReserved1', c_char * 4),  # 字节对齐;Byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Timestamp (in milliseconds);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Time for the event occurred;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('stuGPSStatus', NET_GPS_STATUS_INFO),  # GPS信息;GPS info;
        ('szDriverID', c_char * 32),  # 司机ID;Driver ID;
        ('szVideoPath', c_char * 256),  # 违章关联视频FTP上传路径;ftp path for assocated video;
        ('nRelatingVideoInfoNum', c_int),  # 违章关联的多个视频信息个数;Number of multiple video information associated with violation;
        ('stuRelatingVideoInfo', NET_RELATING_VIDEO_INFO * 16),  # 违章关联的多个视频信息数组，最多支持16个视频;Multiple video information arrays associated with violations, supporting up to 16 videos;
        ('byReserved', C_BYTE * 736),  # 保留字节,留待扩展.;Reserved;
    ]

class NET_A_DEV_EVENT_TRAFFIC_DRIVER_SMOKING(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_DRIVER_SMOKING (驾驶员抽烟事件)对应的数据块描述信息
    event type EVENT_IVS_TRAFFIC_DRIVER_SMOKING (driver smoke event )corresponding to data block description info
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel no.;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('nTriggerType', c_int),  # TriggerType:触发类型,0车检器,1雷达,2视频;TriggerType: trigger type , 0 vehicle detector, 1 radar, 2 video;
        ('PTS', C_DWORD),  # 时间戳(单位是毫秒);time stamp(unit is ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;event occurred time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;means snapshot no.,  as 3,2,1,1 means snapshot end,0 means abnormal end;
        ('byEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;    BYTE                    byReserved1[2];;event  motion , 0 means pulse  event ,1 means  continuity  event  start ,2 means  continuity  event end;  BYTE          byReserved1[2];;
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;picture no., same time(accurate to second) may be multiple pictures , start from 0;
        ('byReserved1', C_BYTE * 2),
        ('stuFileInfo', SDK_EVENT_FILE_INFO),  # 事件对应文件信息;event corresponding to file info;
        ('nLane', c_int),  # 对应车道号;corresponding to lane no.;
        ('nMark', c_int),  # 底层产生的触发抓拍帧标记;bottom occurred trigger snapshot mark;
        ('nFrameSequence', c_int),  # 视频分析帧序号;video analysis frame no.;
        ('nSource', c_int),  # 视频分析的数据源地址;video analysis data source address;
        ('stuObject', SDK_MSG_OBJECT),  # 检测到的物体;detection received object;
        ('stuVehicle', SDK_MSG_OBJECT),  # 车身信息;body info;
        ('stuTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('nSpeed', c_int),  # 车辆实际速度,Km/h;car actual speed,Km/h;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;snapshot mark(by bit), see NET_RESERVED_COMMON;
        ('stuResolution', SDK_RESOLUTION_INFO),  # 对应图片的分辨率;corresponding to picture resolution;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息 车载;GPS info ,use in mobile DVR/NVR;
        ('szDriverID', c_char * 32),  # 司机ID;driver ID;
        ('nRelatingVideoInfoNum', c_int),  # 违章关联的多个视频信息个数;Number of multiple video information associated with violation;
        ('stuRelatingVideoInfo', NET_RELATING_VIDEO_INFO * 16),  # 违章关联的多个视频信息数组，最多支持16个视频;Multiple video information arrays associated with violations, supporting up to 16 videos;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('byReserved', C_BYTE * 952),  # 保留字节;reserve text;
    ]

class NET_A_DEV_EVENT_TRAFFIC_DRIVER_CALLING(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_DRIVER_CALLING(驾驶员打电话事件)对应的数据块描述信息
    event type EVENT_IVS_TRAFFIC_DRIVER_CALLING(driver call event )corresponding to data block description info
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel no.;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('nTriggerType', c_int),  # TriggerType:触发类型,0车检器,1雷达,2视频;TriggerType: trigger type , 0 vehicle detector, 1 radar, 2 video;
        ('PTS', C_DWORD),  # 时间戳(单位是毫秒);time stamp(unit is ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;event occurred time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;means snapshot no., as 3,2,1,1 means snapshot end,0 means abnormal end;
        ('byEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;    BYTE                    byReserved1[2];;event  motion , 0 means pulse  event ,1 means  continuity  event  start ,2 means  continuity  event end;  BYTE          byReserved1[2];;
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;picture no., same time (accurate to second) maybe multiple picture , start from 0;
        ('byReserved1', C_BYTE * 2),
        ('stuFileInfo', SDK_EVENT_FILE_INFO),  # 事件对应文件信息;event corresponding to file info;
        ('nLane', c_int),  # 对应车道号;corresponding to lane no.;
        ('nMark', c_int),  # 底层产生的触发抓拍帧标记;bottom trigger snapshot frame mark;
        ('nFrameSequence', c_int),  # 视频分析帧序号;video analysis frame no.;
        ('nSource', c_int),  # 视频分析的数据源地址;video analysis data source address;
        ('stuObject', SDK_MSG_OBJECT),  # 检测到的物体;detection received object;
        ('stuVehicle', SDK_MSG_OBJECT),  # 车身信息;body info;
        ('stuTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('nSpeed', c_int),  # 车辆实际速度,Km/h;vehicle actual speed,Km/h;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;snapshot mark(by bit), see NET_RESERVED_COMMON;
        ('stuResolution', SDK_RESOLUTION_INFO),  # 对应图片的分辨率;corresponding to picture resolution;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息 车载;GPS info ,use in mobile DVR/NVR;
        ('szDriverID', c_char * 32),  # 司机ID;driver ID;
        ('nRelatingVideoInfoNum', c_int),  # 违章关联的多个视频信息个数;Number of multiple video information associated with violation;
        ('stuRelatingVideoInfo', NET_RELATING_VIDEO_INFO * 16),  # 违章关联的多个视频信息数组，最多支持16个视频;Multiple video information arrays associated with violations, supporting up to 16 videos;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('byReserved', C_BYTE * 952),  # 保留字节;reserve text;
    ]

class NET_A_DEV_EVENT_DRIVERLOOKAROUND_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_DRIVERLOOKAROUND(开车左顾右盼报警事件)对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_TRAFFIC_DRIVERLOOKAROUND(Event of driver look around)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('bReserved1', c_char * 4),  # 字节对齐;Byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Timestamp (in milliseconds);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Time for the event occurred;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('stuGPSStatus', NET_GPS_STATUS_INFO),  # GPS信息;GPS info;
        ('szDriverID', c_char * 32),  # 司机ID;Driver ID;
        ('szVideoPath', c_char * 256),  # 违章关联视频FTP上传路径;ftp path for assocated video;
        ('nRelatingVideoInfoNum', c_int),  # 违章关联的多个视频信息个数;Number of multiple video information associated with violation;
        ('stuRelatingVideoInfo', NET_RELATING_VIDEO_INFO * 16),  # 违章关联的多个视频信息数组，最多支持16个视频;Multiple video information arrays associated with violations, supporting up to 16 videos;
        ('bReserved', C_BYTE * 736),  # 保留字节,留待扩展.;Reserved;
    ]

class NET_A_DEV_EVENT_TIREDLOWERHEAD_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_TIREDLOWERHEAD(开车低头报警事件)对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_TRAFFIC_TIREDLOWERHEAD(Event of driver lower head)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('bReserved1', c_char * 4),  # 字节对齐;Byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Timestamp (in milliseconds);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Time for the event occurred;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('stuGPSStatus', NET_GPS_STATUS_INFO),  # GPS信息;GPS info;
        ('szDriverID', c_char * 32),  # 司机ID;Driver ID;
        ('szVideoPath', c_char * 256),  # 违章关联视频FTP上传路径;ftp path for assocated video;
        ('nRelatingVideoInfoNum', c_int),  # 违章关联的多个视频信息个数;Number of multiple video information associated with violation;
        ('stuRelatingVideoInfo', NET_RELATING_VIDEO_INFO * 16),  # 违章关联的多个视频信息数组，最多支持16个视频;Multiple video information arrays associated with violations, supporting up to 16 videos;
        ('bReserved', C_BYTE * 736),  # 保留字节,留待扩展.;Reserved;
    ]

class NET_IMAGE_INFO_EX(Structure):
    """
    图片信息扩展
    Picture information extension
    """
    _fields_ = [
        ('nIndexInData', C_UINT),  # 在上传图片数据中的图片序号;The serial number of the picture in the uploaded picture data;
        ('nOffset', C_UINT),  # 在二进制数据块中的偏移;Offset in the binary data block;
        ('nLength', C_UINT),  # 图片大小,单位:字节;Picture size, unit: byte;
        ('emType', C_ENUM),  # 图片类型 Refer: EM_IMAGE_TYPE;Picture type Refer: EM_IMAGE_TYPE;
    ]

class NET_A_DEV_EVENT_ALARM_VIDEOBLIND(Structure):
    """
    报警事件类型 EVENT_ALARM_VIDEOBLIND(视频遮挡报警)
    the describe of EVENT_ALARM_VIDEOBLIND's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel id;
        ('szName', c_char * 128),  # 事件名称;evnent name;
        ('Reserved', c_char * 4),  # 保留字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;evnet ID;
        ('stuTime', NET_TIME_EX),  # 事件发生的时间, (设备时间, 不一定是utc时间);Action happens time,accurate to seconds;
        ('szDriverID', c_char * 32),  # 司机ID;driver ID;
        ('stuGPSStatus', NET_GPS_STATUS_INFO),  # GPS信息;GPS;
        ('szVideoPath', c_char * 256),  # 违章关联视频FTP上传路径;ftp path for assocated video;
        ('stuImageInfo', NET_IMAGE_INFO_EX * 6),  # 图片信息扩展;Picture information extension;
        ('nImageInfo', c_int),  # 图片信息扩展的个数;The number of image information extensions;
        ('stuImageInfoEx2', NET_IMAGE_INFO_EX2 * 32),  # 图片信息数组;image information array;
        ('nImageInfoEx2Num', c_int),  # 图片信息个数;Number of image information;
        ('nRelatingVideoInfoNum', c_int),  # 违章关联的多个视频信息个数;Number of multiple video information associated with violation;
        ('stuRelatingVideoInfo', NET_RELATING_VIDEO_INFO * 16),  # 违章关联的多个视频信息数组，最多支持16个视频;Multiple video information arrays associated with violations, supporting up to 16 videos;
        ('byReserved', c_char * 1024),  # 保留字节;reserved bytes;
    ]

class NET_A_DEV_EVENT_DRIVERLEAVEPOST_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_DRIVERLEAVEPOST(开车离岗报警事件)对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_TRAFFIC_DRIVERLEAVEPOST(Event of driver leave post)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('bReserved1', c_char * 4),  # 字节对齐;Byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Timestamp (in milliseconds);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Time for the event occurred;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('stuGPSStatus', NET_GPS_STATUS_INFO),  # GPS信息;GPS info;
        ('szDriverID', c_char * 32),  # 司机ID;Driver ID;
        ('szVideoPath', c_char * 256),  # 违章关联视频FTP上传路径;ftp path for assocated video;
        ('nRelatingVideoInfoNum', c_int),  # 违章关联的多个视频信息个数;Number of multiple video information associated with violation;
        ('stuRelatingVideoInfo', NET_RELATING_VIDEO_INFO * 16),  # 违章关联的多个视频信息数组，最多支持16个视频;Multiple video information arrays associated with violations, supporting up to 16 videos;
        ('bReserved', C_BYTE * 736),  # 保留字节,留待扩展.;Reserved;
    ]

class NET_A_GPS_POINT(Structure):
    """
    电子围栏区域信息
    rect point info
    """
    _fields_ = [
        ('dwLongitude', C_DWORD),  # 经度(单位是百万分之度,范围0-360度)如东经120.178274度表示为300178274;longitude;
        ('dwLatidude', C_DWORD),  # 纬度(单位是百万分之度,范围0-180度)如北纬30.183382度表示为120183382经纬度的具体转换方式可以参考结构体 NET_WIFI_GPS_INFO 中的注释;latidude;
    ]

class NET_FIRING_GPS_INFO(Structure):
    """
    着火点的GPS坐标
    Firing GPS info
    """
    _fields_ = [
        ('dwLongitude', C_DWORD),  # 经度(单位是百万分之度,范围0-360度)如东经120.178274度表示为300178274;Longitude, unit:1/1000000 degree;
        ('dwLatidude', C_DWORD),  # 纬度(单位是百万分之度,范围0-180度)如北纬30.183382度表示为120183382;Latitude, unit:1/1000000 degree;
        ('dbAltitude', c_double),  # 高度, 单位为米;Altitude, unit : m;
        ('szReserve', c_char * 32),  # 预留32字节;Reserved;
    ]

class NET_FIREWARNING_INFO(Structure):
    """
    热成像火情报警信息
    firewarning info
    """
    _fields_ = [
        ('nPresetId', c_int),  # 预置点编号 从测温规则配置CFG_RADIOMETRY_RULE_INFO中选择;preset number is selected from the Temperature Monitoring rule config refer to CFG_RADIOMETRY_RULE_INFO;
        ('stuBoundingBox', NET_RECT),  # 着火点矩形框;kindling point rectangular box;
        ('nTemperatureUnit', c_int),  # 温度单位(当前配置的温度单位),见 NET_TEMPERATURE_UNIT;temperature unit (currently configured temperature unit), refer to NET_TEMPERATURE_UNIT;
        ('fTemperature', c_float),  # 最高点温度值 同帧检测和差分检测提供;max spot temperature value provided by same frame detection and differential detection;
        ('nDistance', C_UINT),  # 着火点距离,单位米 0表示无效;kindling point distance, unit is meter, 0 means invalid;
        ('stuGpsPoint', NET_A_GPS_POINT),  # 着火点经纬度;kindling point longitude and latitude;
        ('stuPTZPosition', PTZ_SPACE_UNIT),  # 云台运行信息;PTZ Info;
        ('fAltitude', c_float),  # 高度(单位：米);Altitude(unit: metre);
        ('nThermoHFOV', C_UINT),  # Uint32 热成像横向视角;Uint32 Thermo horizontal visual;
        ('nThermoVFOV', C_UINT),  # Uint32 热成像纵向视角;Uint32 Thermo vertical visual;
        ('nFSID', C_UINT),  # Uint32 火情编号ID;Uint32 Fire status id;
        ('stuFiringGPS', NET_FIRING_GPS_INFO),  # 着火点的GPS坐标;Firing GPS info;
        ('emFireType', C_ENUM),  # 报警框所属位置 Refer: EM_FIRE_TYPE;The location of the alarm frame Refer: EM_FIRE_TYPE;
        ('reserved', C_BYTE * 144),
    ]

class NET_A_ALARM_FIREWARNING_INFO_DETAIL(Structure):
    """
    热成像火情报警信息上报事件
    firewarning event info
    """
    _fields_ = [
        ('nChannel', c_int),  # 对应视频通道号;channel id;
        ('nWarningInfoCount', c_int),  # 报警信息个数;warning info count;
        ('stuFireWarningInfo', NET_FIREWARNING_INFO * 4),  # 具体报警信息;warning info;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('reserved', C_BYTE * 256),
    ]

class NET_RADAR_ALARMPOINT_INFO(Structure):
    """
    单个雷达报警点信息
    single radar alarm point info
    """
    _fields_ = [
        ('emPointType', C_ENUM),  # 点类型的掩码,该字段废弃,请不要使用,请使用nPointType Refer: EM_RADAR_POINTTYPE;point type,the field is abandoned.please do not use, use nPointType Refer: EM_RADAR_POINTTYPE;
        ('nPointType', c_int),  # 点类型的掩码bit0：无效bit1：当前点是消失的轨迹点bit2：当前点是正在被联动监控的点bit3：当前点是报警区的报警点备注：点的状态可能有多个，例如值为0xC时，表示当前的点既是正在被联动监控的点，又是报警区的报警点;
                              # point typebit0:invalidbit1:disappear track pointbit2:points being monitored by linkagebit3:alarm point of alarm area;
        ('nRegionNumber', c_int),  # 当前点所属的防区编号,范围[0,10]([1,10]为防区编号,0表示当前点不属于任何一个防区);region number, range[0,10]([1,10] is defense area number,0 indicates that it does not belong to any defense area);
        ('emObjectType', C_ENUM),  # 点所指对象的类型的掩码 Refer: EM_RADAR_OBJECTTYPE;radar object type Refer: EM_RADAR_OBJECTTYPE;
        ('nTrackID', c_int),  # 点所属的轨迹号,范围[0,63];track ID, range[0,63];
        ('nDistance', c_int),  # 当前点像素极坐标值-距离，实际长度扩大100倍的结果,单位米;distance, the result of expand 100 times, unit:m;
        ('nAngle', c_int),  # 当前点像素极坐标值-角度，实际角度扩大100倍的结果，单位度;angle, the result of expand 100 times, unit:degree;
        ('nSpeed', c_int),  # 当前点速度，扩大100倍的结果，单位米/秒;point speed, the result of expand 100 times, unit:s;
        ('nLongitude', c_int),  # 经度, 用整型传输, 放大1000000倍, 小数点后6位有效, 不足6位用0补齐, 例如120125400代表120.1254;Longitude, transmitted by integer, magnified by 1000000 times, 6 digits after the decimal point are valid, and less than 6 digits are filled with 0, for example, 120125400 represents 120.1254;
        ('nLatitude', c_int),  # 纬度, 用整型传输, 放大1000000倍, 小数点后6位有效, 不足6位用0补齐, 例如120125400代表120.1254;Latitude, transmitted by integer, magnified by 1000000 times, 6 digits after the decimal point are valid, if less than 6 digits are filled with 0, for example, 120125400 represents 120.1254;
        ('szTrackerIP', c_char * 16),  # 正在跟踪目标的球机的IP地址;The dome camera is tracking the target, 0 is an invalid value;
        ('byReserved', C_BYTE * 488),  # 保留字节;Reserved;
    ]

class NET_RADAR_RULE_INFO(Structure):
    """
    雷达规则信息
    Radar rule information
    """
    _fields_ = [
        ('nRuleID', c_int),  # 规则编号;Rule ID;
        ('nPointNumber', c_int),  # 规则内轨迹数量;Number of tracks in the rule;
        ('nTrackerIP', C_UINT),  # 正在跟踪目标的球机, 0 为无效值;The dome camera is tracking the target, 0 is an invalid value;
        ('byReserved', c_char * 60),  # 保留字节;Reserved;
    ]

class NET_RADAR_NOTIFY_ALARMPOINTINFO(Structure):
    """
    上报的雷达报警点信息
    notify radar alarm point info
    """
    _fields_ = [
        ('nNumAlarmPoint', c_int),  # 雷达报警点的数量;radar alarm point number;
        ('stuAlarmPoint', NET_RADAR_ALARMPOINT_INFO * 64),  # 雷达报警点信息;radar alarm point info;
        ('nChannel', c_int),  # 通道号;channel;
        ('nRuleNum', C_UINT),  # 规则数量;rule number;
        ('stuRuleInfo', NET_RADAR_RULE_INFO * 10),  # 雷达规则信息;radar regulation information;
        ('byReserved', C_BYTE * 296),  # 保留字节;reserved;
    ]

class NET_IN_RADAR_ALARMPOINTINFO(Structure):
    """
    订阅雷达的报警点信息入参(对应接口 CLIENT_AttachRadarAlarmPointInfo)
    attach radar alarm point info input param(corresponding to CLIENT_AttachRadarAlarmPointInfo)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
        ('cbAlarmPointInfo', CB_FUNCTYPE(None, C_LLONG, C_LLONG, POINTER(NET_RADAR_NOTIFY_ALARMPOINTINFO), C_DWORD, c_void_p, C_LDWORD)),  # 雷达报警点信息回调;radar alarm point info callback;
        ('dwUser', C_LDWORD),  # 用户数据;user data;
        ('nChannel', c_int),  # 通道号;channel;
    ]

class NET_OUT_RADAR_ALARMPOINTINFO(Structure):
    """
    订阅雷达的报警点信息出参(对应接口 CLIENT_AttachRadarAlarmPointInfo)
    attach radar alarm point info output param(corresponding to CLIENT_AttachRadarAlarmPointInfo)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;structure size;
    ]

class NET_RADAR_DETECT_OBJECT(Structure):
    """
    雷达检测对象
    Radar detect object
    """
    _fields_ = [
        ('nObjectID', c_int),  # 物体ID;Object ID;
        ('emObjectType', C_ENUM),  # 物体类型 Refer: EM_RADAR_DETECT_OBJECT_TYPE;Object type Refer: EM_RADAR_DETECT_OBJECT_TYPE;
        ('byReserved', C_BYTE * 1024),  # 预留字节;Reserved;
    ]

class NET_RADAR_REGIONDETECTION_RFIDCARD_INFO(Structure):
    """
    雷达区域检测事件的RFID卡片信息
    RFID card information
    """
    _fields_ = [
        ('szCardID', c_char * 24),  # 卡片ID;Card ID;
        ('byReserved', c_char * 256),  # 保留字节;reserved bytes;
    ]

class NET_A_ALARM_RADAR_REGIONDETECTION_INFO(Structure):
    """
    雷达区域检测事件(对应 ALARM_RADAR_REGIONDETECTION)
    radar region detection event(corresponding to ALARM_RADAR_REGIONDETECTION)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作1:Start 2:Stop;event action 1:Start 2:Stop;
        ('stuTime', NET_TIME_EX),  # 事件发生的时间;event occur time;
        ('nChannelID', c_int),  # 通道号;Channel id;
        ('nObjectNum', c_int),  # 检测到的对象个数;Number of detected objects;
        ('stuObjects', NET_RADAR_DETECT_OBJECT * 100),  # 雷达检测对象列表;List of radar detection objects;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('nPresetID', c_int),  # 事件触发的预置点号;Preset point number triggered by the event;
        ('nDetectRegionNum', c_int),  # 检测区域顶点数;The number of vertices in the detection area;
        ('stuDetectRegion', SDK_POINT * 20),  # 检测区域,[0,8191];Detection area,[0,8191];
        ('emAlarmType', C_ENUM),  # 报警类型 Refer: EM_RADAR_ALARM_TYPE;alarm type Refer: EM_RADAR_ALARM_TYPE;
        ('nLongitude', c_int),  # 经度，扩大1000000倍，小数点后6位有效，不足6位用0补齐，例如120125400代表120.1254;Longitude, expanded by 1000000 times, 6 digits after the decimal point are valid, if less than 6 digits are filled with 0, for example, 120125400 represents 120.1254;
        ('nLatitude', c_int),  # 纬度，扩大1000000倍，小数点后6位有效，不足6位用0补齐，例如120125400代表120.1254;Latitude, expanded by 1000000 times, 6 digits after the decimal point are valid, if less than 6 digits are less than 6 digits, use 0 to fill in, for example, 120125400 represents 120.1254;
        ('nRuleID', C_UINT),  # 智能事件规则编号，用于表示哪个规则触发的事件。;Smart event rule number, used to indicate which rule triggered the event.;
        ('nCardNum', c_int),  # RFID卡片数量;RFID card number;
        ('stuCardInfo', NET_RADAR_REGIONDETECTION_RFIDCARD_INFO * 256),  # RFID卡片信息;RFID card information;
        ('nAlarmLevel', C_UINT),  # 报警等级，0 表示未知， 1表示预警警告，2表示报警;alarm level, 0 means unknown, 1 means warning, 2 means alarm The 2nd bit indicates whether the line is prohibited, and the 3rd bit indicates whether it is retrograde;
        ('nAlarmFlag', c_int),  # 报警标志位，bit0表示是否超速，bit1表示是否AIS匹配 第2bit位表示是否禁行 第3bit位表示是否逆行;Alarm flag bit, bit0 indicates whether overspeed, Bit1 indicates whether AIS matches;
        ('nAlarmChannel', c_int),  # 报警输入通道号;Alarm input channel number;
        ('nEventID', C_UINT),  # 事件编号，用来唯一标志一个事件;Event number, used to uniquely mark an event;
        ('nSpeed', c_int),  # 触发事件目标的速度，用整型传输，扩大100倍 单位m/s;The speed of the trigger event target, transmitted by integer, expanded by 100 times, unit m/s;
        ('nTrackID', c_int),  # 触发事件目标的id,范围[0,63];id of trigger event target, range [0,63];
        ('nObjectType', c_int),  # 触发事件目标的类型的掩码: 0x00未识别目标 0x01目标为人 0x02目标为交通工具 0x03目标为树 0x04目标为建筑物 0x05目标为屏幕 0x06目标为动物 0x07目标为大船 0x08目标为中船 0x09目标为小船;Mask of the type of trigger event target: 0x00 unidentified target, 0x01 target is human, 0x02 target is vehicle, 0x03 target is tree, 0x04 target is building, 0x05 target is screen, 0x06 target is animal, 0x07 targets large ships, 0x08 targets medium ships, and 0x09 targets small ships;
        ('nUpDownGoing', c_int),  # 车道/航道方向 -1:未知 0:无效 1:上行 2:下行;Lane / channel direction - 1: unknown 0: invalid 1: up 2: down;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('nDistance', c_int),   # 当前触发事件目标的像素极坐标值--距离，扩大100倍的结果,单位米;Pixel polar coordinate value of current trigger event target -- distance, result of 100 times expansion, unit: meter;
        ('nAngle', c_int),  # 当前触发事件目标的极坐标值--角度，扩大100倍的结果，单位度;Polar coordinate value of current trigger event target -- angle, result of 100 times expansion, unit:degree;
        ('szTargetUUID', c_char * 32),  #  报警目标唯一id;Alarm target unique ID
        ('byReserved', c_char * 960),  # 预留字节;Reserved;
    ]

class NET_A_ALARM_RADAR_LINEDETECTION_INFO(Structure):
    """
    雷达警戒线/绊线检测事件(对应事件ALARM_RADAR_LINEDETECTION)
    Radar cordon/trip line detection event(corresponding to ALARM_RADAR_LINEDETECTION)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel id;
        ('nAction', c_int),  # 事件动作1:Start 2:Stop;event action 1:Start 2:Stop;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('stuTime', NET_TIME_EX),  # 事件发生的时间;Time when the event occurred;
        ('nObjectNum', c_int),  # 检测到的对象个数;Number of detected objects;
        ('stuObjects', NET_RADAR_DETECT_OBJECT * 100),  # 雷达检测对象列表;List of radar detection objects;
        ('nPresetID', c_int),  # 事件触发的预置点号;Preset point number triggered by the event;
        ('nDetectRegionNum', c_int),  # 检测区域顶点数;The number of vertices in the detection area;
        ('stuDetectRegion', SDK_POINT * 20),  # 检测区域,[0,8191];Detection area,[0,8191];
        ('nLongitude', c_int),  # 经度，扩大1000000倍，小数点后6位有效，不足6位用0补齐，例如120125400代表120.1254;Longitude, expanded by 1000000 times, 6 digits after the decimal point are valid, if less than 6 digits are filled with 0, for example, 120125400 represents 120.1254;
        ('nLatitude', c_int),  # 纬度，扩大1000000倍，小数点后6位有效，不足6位用0补齐，例如120125400代表120.1254;Latitude, expanded by 1000000 times, 6 digits after the decimal point are valid, if less than 6 digits are less than 6 digits, use 0 to fill in, for example, 120125400 represents 120.1254;
        ('nAlarmLevel', C_UINT),  # 报警等级，0 表示未知， 1表示预警警告，2表示报警;alarm level, 0 means unkonwn, 1 means warning, 2 means alarm;
        ('nAlarmFlag', c_int),  # 报警标志位，bit0表示是否超速，bit1表示是否AIS匹配;Alarm flag bit, bit0 indicates whether overspeed, Bit1 indicates whether AIS matches;
        ('emAlarmType', C_ENUM),  # 报警类型 Refer: EM_RADAR_ALARM_TYPE;Alarm type Refer: EM_RADAR_ALARM_TYPE;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('byReserved', c_char * 1012),  # 预留字节;reserved byte;
    ]

class NET_VEHICLE_OBJECT(Structure):
    """
    车辆信息
    Vehicle object type
    """
    _fields_ = [
        ('nObjectID', C_UINT),  # 物体ID;Object ID;
        ('nSpeed', C_UINT),  # 车速，单位km/h;Speed unit km/h;
        ('szObjectType', c_char * 16),  # 物体类型 Vehicle NonMotor Plate;Object type Vehicle NonMotor Plate;
        ('emSubObject', C_ENUM),  # 物体类型中的子类别 Refer: EM_CATEGORY_TYPE;Object subtype Refer: EM_CATEGORY_TYPE;
        ('nLane', C_UINT),  # 物理车道号;Lane;
        ('nRoadwayNumber', C_UINT),  # 自定义车道号;Custom lane number;
        ('emSensorType', C_ENUM),  # 探测物体的传感器类型 Refer: EM_DETECT_SENSOR_TYPE;Sensor type for detecting objects Refer: EM_DETECT_SENSOR_TYPE;
        ('nObjectRVID', C_UINT),  # 物体雷达和视频融合ID;Object radar and video fusion ID;
        ('nObjectRID', C_UINT),  # 物体的雷达ID;The radar ID of the object;
        ('szDrivingDirection', c_char * 96),  # 行驶方向"Approach"-上行,即车辆离设备部署点越来越近; "Leave"-下行,即车辆离设备部署点越来越远,第二和第三个参数分别代表上行和下行的两个地点,UTF-8编码;DrivingDirection "Approach" means driving direction,where the car is more near;"Leave"-means where if mor far to the car,the scend and third param means the location of the driving direction;
        ('szPlateNumber', c_char * 32),  # 车牌号码;Platenumber;
        ('szPlateColor', c_char * 16),  # 车牌颜色;PlateColor;
        ('dbLongitude', c_double),  # 车辆经度;Longitude;
        ('dbLatitude', c_double),  # 车辆纬度;Latitude;
        ('szCarColor', c_char * 16),  # 车身颜色;Vehicle color;
        ('emCarType', C_ENUM),  # 车辆类型 Refer: EM_VEHICLEINOUT_CAR_TYPE;Vehicle type Refer: EM_VEHICLEINOUT_CAR_TYPE;
        ('emVirtualCoilDirection', C_ENUM),  # 车辆驶入驶出虚拟线圈的状态 Refer: NET_FLOWSTAT_DIRECTION;The state of the vehicle driving in and out of the virtual coil Refer: NET_FLOWSTAT_DIRECTION;
        ('dbDistanceToStop', c_double),  # 距离停车线距离;Distance from stop line;
        ('dbCarX', c_double),  # 车辆与所有车道的中心点(中心点在设备所处位置，且垂直于车道方向的直线上)，X轴方向(垂直于车道方向)的距离;X-axis direction;
        ('dbCarY', c_double),  # 车辆与所有车道的中心点(中心点在设备所处位置，且垂直于车道方向的直线上)，Y轴方向(平行于车道方向)的距离;Y-axis direction;
        ('dbCarAngle', c_double),  # 车辆与所有车道的中心点(中心点在设备所处位置且垂直于车道方向的直线上)的角度；;Angle.;
        ('nObjectInVideoLane', C_UINT),  # 物体是否在视频车道内, 0:未知, 1:物体不在视频车道内, 2:物体在视频车道内;Whether the object is in the video lane, 0: unknown, 1: the object is not in the video lane, 2: the object is in the video lane;
        ('nDirection', c_int),  # 目标物体实际行驶方向 0-未知，1-直行，2-左转，3-右转，4-掉头;Actual running direction of target object, 0-unknown 1-straight 2-left 3-right 4-u-turn;
        ('fSpeedX', c_float),  # 目标横向运动速度;Target lateral motion speed;
        ('fSpeedY', c_float),  # 目标纵向运动速度;Target longitudinal motion speed;
        ('dbHeadingAngle', c_double),  # 航向角;Heading angle;
        ('stuCarBoundingBox', NET_RECT),  # 车身坐标，包围盒0~8191相对坐标;Car Bounding box;
        ('byReserverd', C_BYTE * 216),  # 保留字节;Reserved;
    ]

class NET_TRAFFIC_FLOW_STAT(Structure):
    """
    车道流量统计
    Lane flow statistics
    """
    _fields_ = [
        ('nLane', C_UINT),  # 物理车道号;Physical lane number;
        ('nRoadwayNumber', C_UINT),  # 自定义车道号;Custom lane number;
        ('emStatus', C_ENUM),  # 流量状态 Refer: EM_TRAFFIC_FLOW_STATUS;Flow status Refer: EM_TRAFFIC_FLOW_STATUS;
        ('emHeadCoil', C_ENUM),  # 车头虚拟线圈状态, 即车进线圈 Refer: EM_VIRTUAL_COIL_OCCUPANCY_STATUS;The virtual coil state of the front of the car, that is, the car enters the coil Refer: EM_VIRTUAL_COIL_OCCUPANCY_STATUS;
        ('emTailCoil', C_ENUM),  # 车尾虚拟线圈状态, 即车出线圈 Refer: EM_VIRTUAL_COIL_OCCUPANCY_STATUS;The state of the virtual coil at the rear of the car Refer: EM_VIRTUAL_COIL_OCCUPANCY_STATUS;
        ('nSpeed', C_UINT),  # 车道平均速度(单位：km/h);Average lane speed (unit: km/h);
        ('nQueueLen', C_UINT),  # 排队长度(单位：cm);Queue length (unit: cm);
        ('nCarsInQueue', C_UINT),  # 排队车辆数;Number of queued vehicles;
        ('emSensorType', C_ENUM),  # 探测物体的传感器类型 Refer: EM_DETECT_SENSOR_TYPE;Sensor type for detecting objects Refer: EM_DETECT_SENSOR_TYPE;
        ('dbSpaceHeadway', c_double),  # 车头间距，相邻车辆之间的距离，单位米/辆;Headway, distance between adjacent vehicles, unit: M / vehicle;
        ('dbTimeHeadWay', c_double),  # 车头时距，单位秒/辆;Headway, unit: S / vehicle;
        ('dbSpaceOccRatio', c_double),  # 空间占有率，即按百分率计量的车辆长度总和除以时间间隔内车辆平均行驶距离;Space occupancy, which is the sum of vehicle lengths as a percentage divided by the average distance traveled by the vehicle during the time interval;
        ('nCarVehicles', C_UINT),  # 车道中的所有车辆的数量，即车流量;The number of all vehicles in the lane, i.e. traffic flow;
        ('byReserverd', C_BYTE * 228),  # 保留字节;Reserved;
    ]

class NET_A_ALARM_VEHICLE_INOUT_INFO(Structure):
    """
    事件类型 ALARM_VEHICLE_INOUT （车辆出入事件）对应的数据块描述信息
    Event type ALARM_VEHICLEINOUT (vehicle entry and exit event) corresponding to the data block description information
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作,0表示脉冲事件;Event action, 0 means pulse event;
        ('nChannel', c_int),  # 通道号;Channel;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Time of event;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('pstObjets', POINTER(NET_VEHICLE_OBJECT)),  # 物体列表;Object list;
        ('nObjectNum', c_int),  # 物体有效个数;Effective number of objects;
        ('nStatNum', c_int),  # 统计有效个数;Count the effective number;
        ('stuStats', NET_TRAFFIC_FLOW_STAT * 8),  # 各个车道实时交通流量统计信息, 最大支持8车道;Real-time traffic flow statistics of each lane, up to 8 lanes;
        ('dbRadarInstallAngle', c_double),  # 雷达安装角度（雷达坐标系Y轴与正北方向的逆时针夹角）单位：度 (0 ~ 360);Radar installation angle (the counterclockwise included angle between the Y-axis of the radar coordinate system and the true north direction) Unit: degree (0 ~ 360);
        ('byReserverd', C_BYTE * 1016),  # 保留字节;Reserved byte;
    ]

class NET_A_COILS_INFO(Structure):
    """
    线圈信息（主要是里面的车辆信息）
    Lane coil information(mainly vehicle information inside the coil)
    """
    _fields_ = [
        ('nCarId', C_UINT),  # 车辆Id（不是车牌号，ID是设备检测到物体记录的编号);Vehicle ID(not license plate number, ID is the number of the record of the object detected by the device);
        ('PlateNum', c_char * 64),  # 车牌号;Plate number;
        ('emCarType', C_ENUM),  # 车辆类型 Refer: EM_NET_CARTYPE;Car Type Refer: EM_NET_CARTYPE;
        ('nDirection', C_UINT),  # 算法识别的车辆行驶方向，0-未知，1-左转，2-直行，3-右转，4-掉头;The driving direction of the vehicle identified by the algorithm, 0-unknown, 1-turn left, 2-go straight, 3-turn right, 4-turn;
        ('byReserved', C_BYTE * 1020),  # 预留字节;Reserved;
    ]

class NET_A_LANE_INFO(Structure):
    """
    车道信息
    Line Info
    """
    _fields_ = [
        ('nLane', C_UINT),  # 物理车道号（范围0~4）;Physical Lane Number (Range 0~4);
        ('nLaneType', c_int),  # 车道类型，虚线车道：0， 实线车道：1;Lane type,dashed lane:0, solid lane:1;
        ('dbLaneOcc', c_double),  # 车道空间占有率,范围[0.0~1.0];Lane space occupancy,Range[0.0~1.0];
        ('nRoadwayNumber', C_UINT),  # 自定义车道号（范围0~128）;Custom Lane Number(Range:0~128);
        ('nCurrentLaneVehicleNum', c_int),  # 当前车道车的数量;Number of Current Lane Vehicles;
        ('nVehicleNum', c_int),  # 从上次统计结束到现在，通过车的辆数(设备0.5秒下发一次);From the end of the last statistics to the present,the number of passing cars(equipment 0.5 seconds down);
        ('nCarId', C_UINT),  # 保留最近有效过车的ID（不是车牌号），CarId是设备检测到物体记录的编号;Keep the ID of the most recent valid passing(not the license plate number), and the CarID is number of the record ofthe object detected by the device;
        ('dbCarEnterTime', c_double),  # 编号CarId车辆进入虚线车道的时间;Number Carld Vehicle Entry Damaged Lane Time;
        ('dbCarLeaveTime', c_double),  # 编号CarId车辆离开实线车道的时间;Time for Carld Vehicle Number to Leave Solid Lane;
        ('nCarDistance', C_UINT),  # 编号CarId车辆行驶的距离，单位：米;Number CarID Vehicle Distance, Unit:M;
        ('nQueueLen', c_int),  # 车辆等待时的排队长度，单位：米;The distance between the vehicle at the rear of the lane and the parking line, in meters;
        ('dbCarSpeed', c_double),  # 编号CarId车辆平均车速，单位：米/秒;Number CarId Vehicle Average Vehicle Speed, Unit:m/s;
        ('nCoilsInfoNum', c_int),  # 实际返回线圈信息个数;Number of actual return coil information;
        ('stuCoilsInfo', NET_A_COILS_INFO * 140),  # 线圈信息（主要是线圈内的车辆信息）;Lane coil information(mainly vehicle information in the coil);
        ('nRetSolidLanNum', c_int),  # 实际返回虚线车道个数;Number of actual return dashed lanes;
        ('nSolidLaneNum', c_int * 6),  # 虚线车道对应的实线车道自定义车道号;Custom Lane Number of Solid Lane Corresponding to Damaged Lane;
        ('nVehicleNumByTypeNum', c_int),  # 实际返回车辆类型统计个数;Statistical Number of Real Return Vehicle Types;
        ('nVehicleNumByType', C_UINT * 64),  # 类型车辆统计,数组下标对应不同车型（车型参考 EM_NET_CARTYPE），下标值对应车辆类型统计的数量;Lane type statistics, array subscripts  correspond to differernt vehicle types(model reference EM_NET_VEHICLE_TYPE), subscripts correspond to the number of vehicle type statistics;
        ('nEndLen', c_int),  # 车辆运行时，尾部车辆位置距离停车线的距离 ，单位：米;When a vehicle is running, the distance between the rear vehicle position and the parking line is in meters, Unit:M;
        ('byReserved', C_BYTE * 1024),  # 预留字节;Reserved;
    ]

class NET_A_ALARM_TRAFFIC_XINKONG_INFO(Structure):
    """
    交通态势事件（ALARM_TRAFFIC_XINKONG）
    alarm of TrafficXinKong(ALARM_TRAFFIC_XINKONG)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('nAction', c_int),  # 只有一个事件动作0，表示脉冲事件;There is only one event action 0, which represents a pulse event;
        ('dbPTS', c_double),  # 时间戳(单位是毫秒);Time stamp (Unit:ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occurrence time;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('byReserved1', C_BYTE * 4),  # 字节对齐;byte alignment;
        ('nLaneInfoNum', c_int),  # 实际上报多少车道信息;Number of Actual Return Lane Information;
        ('stuLaneInfo', NET_A_LANE_INFO * 6),  # 车道信息;Lane information;
        ('nVirtualCoilHeight', C_UINT),  # 单个虚拟线圈的的表征的高度，默认1米，范围: [1, 20];Characterization height of single virtual coil, default is 1 meter, range [1, 20];
        ('nVirtualCoilNumber', C_UINT),  # 虚拟线圈的数量;Number of virtual coils;
        ('nRangeTime', c_int),  # 统计周期内机动车从开始断面到结束断面的平均时间（单位ms）;The average time of the motor vehicle from the start section to the end section in the statistical period (unit ms);
        ('nCurrentAllVehicleNum', c_int),  # 此时刻检测框内的车辆数;The number of vehicles in the detection frame at this moment;
        ('nPedestrationNum', c_int),  # 此时刻行人区域内的人数;The number of people in the pedestrian area at this moment;
        ('nNonMotorNum', c_int),  # 此时刻非机动车区域内非机动车数;The number of non-motor vehicles in the non-motor vehicle area at this time;
        ('byReserved', C_BYTE * 1000),  # 预留字节;Reserved;
    ]

class NET_CAR_PASSING_INFO(Structure):
    """
    车辆进出信息
    Vehicle entry and exit information
    """
    _fields_ = [
        ('nCarId', C_UINT),  # 车辆物体ID;Car ID;
        ('nLane', C_UINT),  # 车道号;Lane;
        ('szPlateNumber', c_char * 32),  # 车牌号码;PlateNumber;
        ('szPlateColor', c_char * 32),  # 车牌颜色;PlateColor;
        ('nSpeed', c_int),  # 车速，单位:km/h，255表示无测速;Vehicle speed, unit: km/h, 255 means no speed measurement;
        ('nCarSize', C_UINT),  # 大小车类型, 0大车 1小车;Large and small car type, 0 large car 1 small car;
        ('emMoveState', C_ENUM),  # 物体进入还是离开 Refer: EM_CAR_PASSING_MOVE_STATE;whether the object enters or leaves Refer: EM_CAR_PASSING_MOVE_STATE;
        ('stuTime', NET_TIME_EX),  # 车辆进出时间，设备本地时间;Vehicle entry and exit time, device local time;
        ('nRoadwayNumber', C_UINT),  # 自定义车道号;Roadway Number;
        ('nCoilID', C_UINT),  # 线圈编号，范围：0-65535;Coil number, range: 0-65535;
        ('dbCarX', c_double),  # 车辆与所有车道的中心点(中心点在设备所处位置，且垂直于车道方向的直线上)，X轴方向(垂直于车道方向)的距离;The distance between the vehicle and the center point of all lanes (the center point is at the position of the device and on a straight line perpendicular to the direction of the lane), the X-axis direction (perpendicular to the direction of the lane);
        ('dbCarY', c_double),  # 车辆与所有车道的中心点(中心点在设备所处位置，且垂直于车道方向的直线上)，Y轴方向(平行于车道方向)的距离;The distance between the vehicle and the center point of all lanes (the center point is at the position of the device and on a line perpendicular to the direction of the lane), in the Y-axis direction (parallel to the direction of the lane);
        ('dbCarAngle', c_double),  # 车辆与所有车道的中心点(中心点在设备所处位置且垂直于车道方向的直线上)的角度;The angle between the vehicle and the center point of all lanes (the center point is on the line where the device is located and perpendicular to the direction of the lane);
        ('szReserved', c_char * 128),  # 保留字节;Reserved byte;
    ]

class NET_A_ALARM_TRAFFIC_CAR_PASSING_INFO(Structure):
    """
    车辆进出虚拟线圈状态事件 (对应 ALARM_TRAFFIC_CAR_PASSING)
    Traffic Car Passing Alarm (correspond to ALARM_TRAFFIC_CAR_PASSING)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作 0:脉冲;Event Action 0: Pulse;
        ('nChannel', c_int),  # 通道号;Channel;
        ('szName', c_char * 128),  # 事件名称;Event Name;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间，设备本地时间;Time of event, device local time;
        ('nUTCMS', C_UINT),  # 事件发生时间，表示毫秒;The time when the event occurred, in milliseconds;
        ('nTimeZone', C_UINT),  # 时区索引，参见时区列表TIME_ZONE_TYPE;TimeZone, See TIME_ZONE_TYPE;
        ('nFrameSequence', C_UINT),  # 视频分析帧序号;Frame Sequence;
        ('nCarPassingCount', c_int),  # 车辆进出个数;Car Passing Count;
        ('stuCarPassing', NET_CAR_PASSING_INFO * 16),  # 车辆进出信息;Car Passing Info;
        ('szReserved', c_char * 1024),  # 保留字节;Reserved byte;
    ]

class NET_IN_PTZBASE_GET_FOCUS_VALUE(Structure):
    """
    CLIENT_QueryDevInfo NET_QUERY_PTZBASE_GET_FOCUS_VALUE 类型接口输入参数
    CLIENT_QueryDevInfo NET_QUERY_PTZBASE_GET_FOCUS_VALUE Type interface input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nChannel', c_int),  # 通道号从0开始;The channel number starts from 0;
        ('fZoom', c_float),  # 镜头变倍值,归一化到0~1;Lens zoom value, normalized to 0~1;
    ]

class NET_OUT_PTZBASE_GET_FOCUS_VALUE(Structure):
    """
    CLIENT_QueryDevInfo NET_QUERY_PTZBASE_GET_FOCUS_VALUE 类型接口输出参数
    CLIENT_QueryDevInfo NET_QUERY_PTZBASE_GET_FOCUS_VALUE Type interface output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nValue', c_int),  # 对应倍率焦距值 单位0.01mm, 扩大100倍表示;Corresponding magnification focal length value, the unit is 0.01 degrees, and it is expressed by 100 times;
        ('nMinValue', c_int),  # 镜头最小焦距值,单位同nValue;Minimum focal length of lens, the unit is the same as nValue;
        ('nMaxValue', c_int),  # 镜头最大焦距值,单位同nValue;Maximum focal length of lens, the unit is the same as nValue;
    ]


class NET_IN_TRAFFIC_RADAR_GET_OBJECT_EX_INFO(Structure):
    """
    CLIENT_QueryDevInfo NET_QUERY_TRAFFIC_RADAR_GET_OBJECT_EX 类型接口输入参数
    CLIENT_QueryDevInfo NET_QUERY_TRAFFIC_RADAR_GET_OBJECT_EX enumeration type oinput parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Struct size;
        ('nChannel', C_UINT),  # 通道号;Channel;
    ]

class NET_RADAR_OBJECT_EX_INFO(Structure):
    """
    目标雷达信息
    Radar Object information
    """
    _fields_ = [
        ('nID', C_UINT),  # 物体ID;Object ID;
        ('nBelongId', C_UINT),  # 属主id，无属主则为0;BelongId;
        ('emObjectType', C_ENUM),  # 物体类型 Refer: EM_A_EMUM_VIDEO_ANALYSE_OBJECT_TYPE;bjectType Refer: EM_A_EMUM_VIDEO_ANALYSE_OBJECT_TYPE;
        ('nRadarObjAtt', C_UINT),  # 雷达目标属性, emObjectType为EMUM_VIDEO_ANALYSE_OBJECT_TYPE_RADARDETECT时有效, 0:表示雷达目标是虚拟目标; 1:表示是真实(有效)目标;Radar target attribute, valid when emObjectType is EMUM_VIDEO_ANALYSE_OBJECT_TYPE_RADARDETECT, 0: indicates that the radar target is a virtual target; 1: indicates that it is a real (valid) target;
        ('nRadarObjSource', C_UINT),  # 雷达目标产生源, 当nRadarObjAtt为1时有效, 0:表示从融合物体信息中获取 1:表示直接从雷达裸数据中获取;Radar target generation source, valid when nRadarObjAtt is 1, 0: Obtained from the fusion object information 1: Obtained directly from the radar naked data;
        ('nVideoObjAtt', C_UINT),  # 视频目标属性, emObjectType为EMUM_VIDEO_ANALYSE_OBJECT_TYPE_VEHICLE/EMUM_VIDEO_ANALYSE_OBJECT_TYPE_NONMOTOR/EMUM_VIDEO_ANALYSE_OBJECT_TYPE_HUMAN时有效, 0:表示视频目标是融合目标; 1:表示视频目标是虚拟目标;Video target attribute, valid when emObjectType is EMUM_VIDEO_ANALYSE_OBJECT_TYPE_VEHICLE/EMUM_VIDEO_ANALYSE_OBJECT_TYPE_NONMOTOR/EMUM_VIDEO_ANALYSE_OBJECT_TYPE_HUMAN, 0: indicates that the video target is a fusion target; 1: indicates that the video target is a virtual target;
        ('nVerticalPos', C_UINT),  # 物体在道路方向上的坐标, 雷达为坐标原点 单位:cm;The coordinates of the object in the direction of the road, the radar is the origin of the coordinates Unit: cm;
        ('nHorizontalPos', C_UINT),  # 物体在垂直道路方向上的坐标, 雷达为坐标原点 单位:cm;The coordinates of the object in the vertical direction of the road, the radar is the origin of the coordinates Unit: cm;
        ('nObjectLen', C_UINT),  # 物体长度 单位:cm;Object Length Unit: cm;
        ('dbSpeedX', c_double),  # 目标横向运动速度, 单位:m/s, 精确到小数点后一位 设备视角: 右手方向为x正向;Target lateral movement speed, unit: m/s, accurate to one decimal place;
        ('dbSpeedY', c_double),  # 目标纵向运动速度, 单位:m/s, 精确到小数点后一位 设备视角: 正前方为y正向;Target longitudinal movement speed, unit: m/s, accurate to one decimal place;
        ('szReserved', c_char * 972),  # 保留字节;Reserved;
    ]

class NET_OUT_TRAFFIC_RADAR_GET_OBJECT_EX_INFO(Structure):
    """
    CLIENT_QueryDevInfo NET_QUERY_TRAFFIC_RADAR_GET_OBJECT_EX 类型接口输出参数
    CLIENT_QueryDevInfo NET_QUERY_TRAFFIC_RADAR_GET_OBJECT_EX enumeration type output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Struct size;
        ('nObjectNum', c_int),  # 有效目标个数;number of valid targets;
        ('nMaxObjectNum', C_UINT),  # 用户申请目标最大个数;The maximum number of user application targets;
        ('nObjectCount', c_int),  # 获取到目标的个数;Get the number of targets;
        ('pstuObjectInfo', POINTER(NET_RADAR_OBJECT_EX_INFO)),  # 目标信息内存由用户申请;The target information, memory is requested by the user;
    ]

class NET_A_ALARM_AREAALARM_INFO(Structure):
    """
    区域报警事件(对应事件 ALARM_AREAALARM)
    alarm of area alarm(Corresponding to ALARM_AREAALARM)
    """
    _fields_ = [
        ('nAreaIndex', c_int),  # 区域号;Area ID;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occurrence time;
        ('szName', c_char * 128),  # 名称;Name;
        ('emDefenceAreaType', C_ENUM),  # 防区类型 Refer: EM_DEFENCE_AREA_TYPE;Defence area type Refer: EM_DEFENCE_AREA_TYPE;
        ('nIndex', c_int),  # 触发的通道号;Channel ID;
        ('emTrigerType', C_ENUM),  # 触发类型 Refer: EM_AREAALARM_TRIGGER_TYPE;trigger type Refer: EM_AREAALARM_TRIGGER_TYPE;
        ('byReserved', C_BYTE * 1024),  # 保留扩展字节;Reserved Byte;
    ]

class NET_ALARM_RF_JAMMING_INFO(Structure):
    """
    RF干扰上报事件 (对应 ALARM_RF_JAMMING)
    RF interference alarm reporting event(corresponding to ALARM_RF_JAMMING)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作 0:脉冲;Event action 0: pulse;
        ('nChannel', c_int),  # 通道号;channel;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间,标准的（不带时区偏差的）UTC时间;the event happen time;
        ('szDeviceName', c_char * 256),  # 设备名称;device name;
        ('szReserved', c_char * 1024),  # 保留字节;Reserved;
    ]

class NET_ALARM_ARMING_FAILURE_INFO(Structure):
    """
    布防失败上报事件 (对应 ALARM_ARMING_FAILURE)
    reporting event of deployment failure (corresponding to ALARM_ARMING_FAILURE)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作 0:脉冲;Event action 0: pulse;
        ('nChannel', c_int),  # 通道号;channel;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间,标准的（不带时区偏差的）UTC时间;the event happen time;
        ('emMode', C_ENUM),  # 布撤防模式 Refer: EM_ARM_TYPE;Deployment and removal mode Refer: EM_ARM_TYPE;
        ('szReserved', c_char * 1024),  # 保留字节;Reserved;
    ]

class NET_ALARM_USER_MODIFIED_INFO(Structure):
    """
    用户信息被修改(增加、删除、修改)上报事件 (对应 ALARM_USER_MODIFIED)
    reporting event when user information is modified (added, deleted, modified) (corresponding to ALARM_USER_MODIFIED)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作 0:脉冲;Event action 0: pulse;
        ('nChannel', c_int),  # 通道号;channel;
        ('szUser', c_char * 128),  # 用户名称;username;
        ('emOpType', C_ENUM),  # 操作类型 Refer: EM_A_NET_EVENT_OPERATE_TYPE;Operation type Refer: EM_A_NET_EVENT_OPERATE_TYPE;
        ('emUserType', C_ENUM),  # 用户类型 Refer: EM_A_NET_EVENT_USER_TYPE;user type Refer: EM_A_NET_EVENT_USER_TYPE;
        ('szReserved', c_char * 1024),  # 保留字节;Reserved;
    ]

class NET_ALARM_MANUAL_TEST_INFO(Structure):
    """
    手动测试上报事件 (对应 ALARM_MANUAL_TEST)
    Manually test alarm reporting events (corresponding to ALARM_MANUAL_TEST)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作 0:脉冲;Event action 0: pulse;
        ('nChannel', c_int),  # 通道号;channel;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间,标准的（不带时区偏差的）UTC时间;the event happen time;
        ('szSN', c_char * 32),  # 配件序列号;Accessory serial number;
        ('szName', c_char * 32),  # 配件名称;Accessory name;
        ('szAreaName', c_char * 128),  # 配件所属区域名称;Name of the area to which the accessories belong;
        ('szReserved', c_char * 1024),  # 保留字节;Reserved;
    ]

class NET_ALARM_DEVICE_MODIFIED_INFO(Structure):
    """
    设备设息修改(增加、删除、修改)上报事件 (对应 ALARM_DEVICE_MODIFIED)
    reporting events for equipment setting modification (addition, deletion, modification) (corresponding to ALARM_DEVICE_MODIFIED)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作 0:脉冲;Event action 0: pulse;
        ('nChannel', c_int),  # 通道号;channel;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间,标准的（不带时区偏差的）UTC时间;the event happen time;
        ('szUser', c_char * 32),  # 用户名称;username;
        ('emOpType', C_ENUM),  # 操作类型 Refer: EM_A_NET_EVENT_OPERATE_TYPE;Operation type Refer: EM_A_NET_EVENT_OPERATE_TYPE;
        ('emDeviceType', C_ENUM),  # 设备类型 Refer: EM_A_NET_EVENT_DEVICE_TYPE;device type Refer: EM_A_NET_EVENT_DEVICE_TYPE;
        ('szReserved', c_char * 1024),  # 保留字节;Reserved;
    ]

class NET_ALARM_ATS_FAULT_INFO(Structure):
    """
    报警传输系统故障上报事件 (对应 ALARM_ATS_FAULT)
    transmission system fault  reporting event (corresponding to ALARM_ATS_FAULT)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作, 1:开始 2:停止;Event action 1:start 2:stop;
        ('nChannel', c_int),  # 通道号;channel;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间,标准的（不带时区偏差的）UTC时间;the event happen time;
        ('szReserved', c_char * 1024),  # 保留字节;Reserved;
    ]

class NET_ALARM_ARC_OFFLINE_INFO(Structure):
    """
    报警接收中心离线上报事件 (对应 ALARM_ARC_OFFLINE)
    receiving center offline  reporting event (corresponding to ALARM_ARC_OFFLINE)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作, 1:开始 2:停止;Event action 1:start 2:stop;
        ('nChannel', c_int),  # 通道号;channel;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间,标准的（不带时区偏差的）UTC时间;the event happen time;
        ('szDetail', c_char * 128),  # ARC通讯异常描述信息;ARC communication exception description information;
        ('szReserved', c_char * 1024),  # 保留字节;Reserved;
    ]

class NET_EVENT_AREAR_INFO(Structure):
    """
    所属区域信息结构体
    Region information struct
    """
    _fields_ = [
        ('szName', c_char * 128),  # 所属区域名称;Area name;
        ('nIndex', c_int),  # 所属区域编号;Area number;
        ('szRsd', c_char * 64),  # 保留字节;Reserved;
    ]

class NET_ALARM_WIFI_FAILURE_INFO(Structure):
    """
    wifi故障上报事件 (对应 ALARM_WIFI_FAILURE)
    WiFi fault  reporting event (corresponding to ALARM_WIFI_FAILURE)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作, 1:开始 2:停止;Event action 1:start 2:stop;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间,标准的（不带时区偏差的）UTC时间;the event happen time;
        ('szSN', c_char * 32),  # 配件序列号;Accessory serial number;
        ('szName', c_char * 64),  # 配件名称;Accessory name;
        ('nErrorCode', c_int),  # wifi故障错误码 1:未知错误;2:无效的网络名称;3:无效的网络口令;4:网络故障;WiFi fault error code 1: unknown error; 2: Invalid network name; 3: Invalid network password; 4: Network failure;
        ('nAreaInfoNum', c_int),  # 所属区域信息个数;Region information number;
        ('stuAreaInfo', NET_EVENT_AREAR_INFO * 64),  # 所属区域信息;Region information;
        ('szReserved', c_char * 1024),  # 保留字节;Reserved;
    ]

class NET_ALARM_OVER_TEMPERATURE_INFO(Structure):
    """
    超温上报事件 (对应 ALARM_OVER_TEMPERATURE)
    Over temperature  reporting event (corresponding to ALARM_OVER_TEMPERATURE)
    """
    _fields_ = [
        ('nAction', c_int),  # 事件动作 0:脉冲;Event action 0: pulse;
        ('nChannel', c_int),  # 通道号;channel;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间,标准的（不带时区偏差的）UTC时间;the event happen time;
        ('szSN', c_char * 32),  # 配件序列号;Accessory serial number;
        ('szName', c_char * 64),  # 配件名称;Accessory name;
        ('nTemperatureType', c_int),  # 超温类型 0:温度恢复正常;1:温度超过下限;2:温度超过上限;Overtemperature type 0: the temperature returns to normal;1: The temperature exceeds the lower limit; 2: Temperature exceeds upper limit;
        ('nAreaInfoNum', c_int),  # 所属区域信息个数;Region information number;
        ('stuAreaInfo', NET_EVENT_AREAR_INFO * 64),  # 所属区域信息;Region information;
        ('szReserved', c_char * 1024),  # 保留字节;Reserved;
    ]

class NET_IMAGE_COMPARE_INFO(Structure):
    """
    人脸图片比较信息
    face image compare info
    """
    _fields_ = [
        ('dwoffset', C_DWORD),  # 在二进制数据块中的偏移,单位:字节;offset in binary data,unit:byte;
        ('dwLength', C_DWORD),  # 图片大小,单位:字节;Image length,unit:byte;
        ('dwWidth', C_DWORD),  # 图片宽度;image width;
        ('dwHeight', C_DWORD),  # 图片高度;image height;
        ('byReserved', C_BYTE * 128),  # 保留字节;Reserved;
    ]

class NET_MATCH_TWO_FACE_IN(Structure):
    """
    CLIENT_MatchTwoFace 输入参数
    CLIENT_MatchTwoFace input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('stuOriginalImage', NET_IMAGE_COMPARE_INFO),  # 原图;original image;
        ('stuCompareImage', NET_IMAGE_COMPARE_INFO),  # 比较图;compare image;
        ('pSendBuf', POINTER(c_char)),  # 两张人脸图片数据;two face image data;
        ('dwSendBufLen', C_DWORD),  # 数据大小;data length;
    ]

class NET_MATCH_TWO_FACE_OUT(Structure):
    """
    CLIENT_MatchTwoFace 输出参数
    CLIENT_MatchTwoFace output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nSimilarity', c_int),  # 两张图片的相似度,范围0~100;Similarity ( expressed as a percentage, from 1 to 100);
    ]

class NET_DEVICE_ID_STRING(Structure):
    """
    登录模式为主动注册时使用
    Used when the login mode is active registration
    """
    _fields_ = [
        ('ID', c_char * 64)
    ]

class NET_IN_WATERDATA_STAT_SERVER_GETCAPS_INFO(Structure):
    """
    CLIENT_GetWaterDataStatServerCaps 输入参数
    CLIENT_GetWaterDataStatServerCaps input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小,必须赋值;The size of this structure must be assigned;
    ]

class NET_OUT_WATERDATA_STAT_SERVER_GETCAPS_INFO(Structure):
    """
    CLIENT_GetWaterDataStatServerCaps 输出参数
    CLIENT_GetWaterDataStatServerCaps Output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小,必须赋值;The size of this structure must be assigned;
        ('emSupport', C_ENUM),  # 当前是否具备水质检测功能 Refer: EM_WATERDATA_STAT_SERVER_SUPPORT;Does it have water quality detection function at present Refer: EM_WATERDATA_STAT_SERVER_SUPPORT;
        ('emSupportLocalDataStore', C_ENUM),  # 是否支持本地存储 Refer: EM_SUPPORT_LOCALDATA_STORE;Does it support local storage Refer: EM_SUPPORT_LOCALDATA_STORE;
    ]

class NET_IN_WATERDATA_STAT_SERVER_GETDATA_INFO(Structure):
    """
    CLIENT_GetWaterDataStatServerWaterData 输入参数
    CLIENT_GetWaterDataStatServerWaterData input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小,必须赋值;The size of this structure must be assigned;
        ('nTypeNum', c_int),  # 检测类型个数;Number of detection types;
        ('emType', C_ENUM * 32),  # 检测类型 Refer: EM_WATER_DETECTION_ALARM_TYPE;Detection type Refer: EM_WATER_DETECTION_ALARM_TYPE;
    ]

class NET_WATER_DETECTION_UPLOAD_INFO(Structure):
    """
    水质检测上报数据信息
    Water quality test report data information
    """
    _fields_ = [
        ('fPH', c_float),  # PH值 范围(1-14);PH value range (1-14);
        ('fNTU', c_float),  # 浊度值 范围(0-500NTU);Turbidity value range (0-500ntu);
        ('fNH3_N', c_float),  # 氨氮值 范围(0-50mg/l);Ammonia nitrogen value range (0-50mg / L);
        ('fTN', c_float),  # 总氮值 范围(0-50mg/l);Total nitrogen value range (0-50mg / L);
        ('fSD', c_float),  # 透明度值 范围(0-30 m);Transparency value range (0-30 m);
        ('fCOD', c_float),  # 化学需氧量 范围(0-100mg/l);Cod range (0-100mg / L);
        ('fNN', c_float),  # 亚硝酸盐氮 范围(0-500mg/l);Nitrite nitrogen range (0-500mg / L);
        ('fDO', c_float),  # 溶解氧 范围(0-10 mg/l);Dissolved oxygen range (0-10 mg / L);
        ('fChl_a', c_float),  # 叶绿素a 范围(0-300 ug/l);Chlorophyll a range (0-300 UG / L);
        ('fTP', c_float),  # 总磷 范围0-5mg/L;Total phosphorus range: 0-5mg / L;
        ('fCODMn', c_float),  # 高锰酸盐指数范围(0-100mg/l);Permanganate index range (0-100mg / L);
        ('fSS', c_float),  # 悬浮物 范围(0-1000mg/l);Suspended solids range (0-1000mg / L);
        ('fBOD_5', c_float),  # 五日生化需氧量 范围(0-50mg/l);Five day biochemical oxygen demand range (0-50mg / L);
        ('fNO3_N', c_float),  # 硝酸盐 范围(0-500mg/l);Nitrate range (0-500mg / L);
        ('fTSI', c_float),  # 富营养状况指数 范围无;Range of eutrophication index: None;
        ('emSmellyLevel', C_ENUM),  # 黑臭等级 Refer: EM_SMELLY_LEVEL;Black odor grade Refer: EM_SMELLY_LEVEL;
        ('szReserved', c_char * 512),  # 预留字节;Reserved;
    ]

class NET_OUT_WATERDATA_STAT_SERVER_GETDATA_INFO(Structure):
    """
    CLIENT_GetWaterDataStatServerWaterData 输出参数
    CLIENT_GetWaterDataStatServerWaterData Output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小,必须赋值;The size of this structure must be assigned;
        ('emQuality', C_ENUM),  # 水质类别，越小越好 Refer: EM_WATER_QUALITY;Water quality category, the smaller the better Refer: EM_WATER_QUALITY;
        ('stuUploadInfo', NET_WATER_DETECTION_UPLOAD_INFO),  # 水质检测上报数据信息;Water quality test report data information;
        ('nFlunkTypeNum', c_int),  # 参数超过阈值类型个数;Number of parameter types exceeding threshold;
        ('emFlunkType', C_ENUM * 32),  # 参数超过阈值类型 Refer: EM_WATER_DETECTION_ALARM_TYPE;Parameter exceeds threshold type Refer: EM_WATER_DETECTION_ALARM_TYPE;
    ]

class NET_START_FIND_WATERDATA_CONDITION(Structure):
    """
    水质检测数据查询条件
    Query conditions of water quality test data
    """
    _fields_ = [
        ('stuStartTime', NET_TIME_EX),  # 开始时间;Start time;
        ('emType', C_ENUM * 32),  # 检测类型 Refer: EM_WATER_DETECTION_ALARM_TYPE;Detection type Refer: EM_WATER_DETECTION_ALARM_TYPE;
        ('nTypeNum', c_int),  # 检测类型个数;Number of detection types;
        ('nPresetIDNum', c_int),  # 预置点个数;Number of preset points;
        ('nPresetID', c_int * 32),  # 预置点;Preset;
        ('stuEndTime', NET_TIME_EX),  # 结束时间;End time;
        ('szReserved', c_char * 256),  # 预留字节;Reserved byte;
    ]

class NET_IN_START_FIND_WATERDATA_STAT_SERVER_INFO(Structure):
    """
    CLIENT_StartFindWaterDataStatServer 输入参数
    CLIENT_StartFindWaterDataStatServer input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小,必须赋值;The size of this structure must be assigned;
        ('stuCondition', NET_START_FIND_WATERDATA_CONDITION),  # 水质检测数据查询条件;Query conditions of water quality test data;
    ]

class NET_OUT_START_FIND_WATERDATA_STAT_SERVER_INFO(Structure):
    """
    CLIENT_StartFindWaterDataStatServer 输出参数
    CLIENT_StartFindWaterDataStatServer Output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小,必须赋值;The size of this structure must be assigned;
        ('nToken', C_UINT),  # 取到的查询令牌;Retrieved query token;
        ('nTotalCount', C_UINT),  # 符合此次查询条件的结果总条数;Total number of results that meet the query criteria;
    ]

class NET_IN_DO_FIND_WATERDATA_STAT_SERVER_INFO(Structure):
    """
    CLIENT_DoFindWaterDataStatServer 输入参数
    CLIENT_DoFindWaterDataStatServer input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小,必须赋值;The size of this structure must be assigned;
        ('nToken', C_UINT),  # 查询令牌;Query token;
        ('nBeginNumber', C_UINT),  # 查询起始序号, 表示从beginNumber条记录开始,取count条记录返回;Query the start sequence number, which means that it starts from beginnumber records and returns count records;
        ('nCount', c_int),  # 每次查询的流量统计条数;Number of traffic statistics per query;
    ]

class NET_WATERDATA_STAT_SERVER_INFO(Structure):
    """
    流量统计信息
    Traffic statistics
    """
    _fields_ = [
        ('stuStartTime', NET_TIME_EX),  # 开始时间;Start time;
        ('emQuality', C_ENUM),  # 水质类别 Refer: EM_WATER_QUALITY;Water quality category Refer: EM_WATER_QUALITY;
        ('stuUploadInfo', NET_WATER_DETECTION_UPLOAD_INFO),  # 水质检测上报数据信息;Water quality test report data information;
        ('szReserved', c_char * 256),  # 预留字节;Reserved;
    ]

class NET_OUT_DO_FIND_WATERDATA_STAT_SERVER_INFO(Structure):
    """
    CLIENT_DoFindWaterDataStatServer 输出参数
    CLIENT_DoFindWaterDataStatServer Output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小,必须赋值;The size of this structure must be assigned;
        ('nFound', C_UINT),  # 查询到的条数;Number of queries;
        ('nInfoNum', c_int),  # 流量统计信息个数;Number of traffic statistics;
        ('stuInfo', NET_WATERDATA_STAT_SERVER_INFO * 64),  # 流量统计信息;Traffic statistics;
    ]

class NET_IN_STOP_FIND_WATERDATA_STAT_SERVER_INFO(Structure):
    """
    CLIENT_StopFindWaterDataStatServer 输入参数
    CLIENT_StopFindWaterDataStatServer input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小,必须赋值;The size of this structure must be assigned;
        ('nToken', C_UINT),  # 查询令牌;Query token;
    ]

class NET_OUT_STOP_FIND_WATERDATA_STAT_SERVER_INFO(Structure):
    """
    CLIENT_StopFindWaterDataStatServer 输出参数
    CLIENT_StopFindWaterDataStatServer Output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小,必须赋值;The size of this structure must be assigned;
    ]

class NET_FACE_RECORD_INFO(Structure):
    """
    人脸信息
    the info of fae
    """
    _fields_ = [
        ('szUserName', c_char * 128),  # 用户名;user name;
        ('nRoom', c_int),  # 房间个数;count of rooms;
        ('szRoomNo', c_char * 32 * 16),  # 房间号列表;list of rooms;
        ('nFaceData', c_int),  # 人脸模板数据个数;count of face data;
        ('szFaceData', c_char * 20 * 2048),  # 人脸模板数据;face data;
        ('nFaceDataLen', c_int * 20),  # 人脸模版数据大小;face data len;
        ('nFacePhoto', c_int),  # 人脸照片个数;count of face photo;
        ('nFacePhotoLen', c_int * 5),  # 每张图片的大小;face photo data len;
        ('pszFacePhoto', POINTER(c_char) * 5),  # 人脸照片数据,大小不超过120K;face photo data,max size: 120K;
        ('bValidDate', C_BOOL),  # 是否设置人脸有效时间;face photo date of validity;
        ('stuValidDateStart', NET_TIME),  # 人脸有效开始时间;face photo start date of validity;
        ('stuValidDateEnd', NET_TIME),  # 人脸有效结束时间;face photo end date of validity;
        ('nValidCounts', c_int),  # 刷脸有效次数：小于0表示不限次数， 等于0刷脸次数已用完;Valid count(nValidCounts < 0 : unlimited count, nValidCounts == 0 : can't open door);
        ('bValidCountsEnable', C_BOOL),  # 次数字段使能;Valid Count Enable;
        ('bFaceDataExEnable', C_BOOL),  # 人脸模板数据扩展使能;face data extension enable;
        ('pszFaceDataEx', POINTER(c_char) * 20),  # 人脸模板数据扩展, 由用户申请释放, 每张照片最大为8K;face data extension, it is applied and released by user, each photo max size: 8K;
        ('byReserved', C_BYTE * 240),  # 保留字节;reserved bytes;
    ]

class NET_IN_UPDATE_FACE_INFO(Structure):
    """
    更新人脸记录信息输入参数
    the input param to updata face data
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szUserID', c_char * 32),  # 用户ID;user ID;
        ('stuFaceInfo', NET_FACE_RECORD_INFO),  # 人脸数据;the info of face;
    ]

class NET_OUT_UPDATE_FACE_INFO(Structure):
    """
    更新人脸记录信息输出参数
    the output param to updata face data
    """
    _fields_ = [
        ('dwSize', C_DWORD),
    ]

class NET_IN_GET_FACE_INFO(Structure):
    """
    获取人脸记录信息输入参数
    the input param of getting face data
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szUserID', c_char * 32),  # 用户ID;user ID;
    ]

class NET_OUT_GET_FACE_INFO(Structure):
    """
    获取人脸记录信息输出参数
    the out param of getting face data
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nFaceData', c_int),  # 人脸模板数据个数;count of face data;
        ('szFaceData', c_char * 20 * 2048),  # 人脸模板数据;face data;
        ('nPhotoData', c_int),  # 白光人脸照片数据个数, 最大个数：5;the number of photo data, max number: 5;
        ('nInPhotoDataLen', c_int * 5),  # 用户申请的每张白光人脸照片大小;the length of each photo data applied by user;
        ('nOutPhotoDataLen', c_int * 5),  # 每张白光人脸照片实际的大小;the actual length of each photo data;
        ('pPhotoData', POINTER(c_char) * 5),  # 白光人脸照片数据, 由用户申请释放, 每张照片最大为200K;photo data, it is applied and released by user, each photo max size: 200K;
    ]

class NET_IN_ADD_FACE_INFO(Structure):
    """
    添加人脸记录信息输入参数
    the input param of adding face data
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szUserID', c_char * 32),  # 用户ID;user ID;
        ('stuFaceInfo', NET_FACE_RECORD_INFO),  # 人脸数据;face data;
    ]

class NET_OUT_ADD_FACE_INFO(Structure):
    """
    添加人脸记录信息输出参数
    the output param of adding face data
    """
    _fields_ = [
        ('dwSize', C_DWORD),
    ]

class NET_IN_GETFACEEIGEN_INFO(Structure):
    """
    获取人脸特征值信息输入参数
    the input param of get face eigen
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nPhotoDataLen', c_int),  # 人脸照片数据大小;photo data len;
        ('pszPhotoData', POINTER(c_char)),  # 人脸照片数据, 由用户申请释放, 每张照片最大为200K;photo data, it is applied and released by user, each photo max size: 200K;
    ]

class NET_OUT_GETFACEEIGEN_INFO(Structure):
    """
    获取人脸特征值信息输出参数
    the output param of get face eigen
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nInFaceEigenLen', c_int),  # 用户申请的人脸特征值数据大小;the length of face eigen applied by user;
        ('nOutFaceEigenLen', c_int),  # 人脸特征值数据实际的大小;the actual length of face eigen;
        ('pszFaceEigen', POINTER(c_char)),  # 人脸特征值数据, 由用户申请释放, 每张照片最大为8K;face eigen data, it is applied and released by user, each photo max size: 8K;
    ]

class NET_IN_CLEAR_FACE_INFO(Structure):
    """
    清除人脸记录信息输入参数
    the input param of clear face data
    """
    _fields_ = [
        ('dwSize', C_DWORD),
    ]

class NET_OUT_CLEAR_FACE_INFO(Structure):
    """
    清除人脸记录信息输出参数
    the output param of clear face data
    """
    _fields_ = [
        ('dwSize', C_DWORD),
    ]

class NET_IN_REMOVE_FACE_INFO(Structure):
    """
    删除人脸记录信息输入参数
    the input param of removing face data
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szUserID', c_char * 32),  # 用户ID;user ID;
    ]

class NET_OUT_REMOVE_FACE_INFO(Structure):
    """
    删除人脸记录信息输出参数
    the output param of removing face data
    """
    _fields_ = [
        ('dwSize', C_DWORD),
    ]

class NET_A_DEV_VERSION_INFO(Structure):
    """
    设备软件版本信息,对应CLIENT_QueryDevState接口
    Device software version information. Corresponding to CLIENT_QueryDevState
    """
    _fields_ = [
        ('szDevSerialNo', c_char * 48),  # 序列号;Serial number;
        ('byDevType', c_char),  # 设备类型,见枚举NET_DEVICE_TYPE;Device type, please refer to NET_DEVICE_TYPE;
        ('szDevType', c_char * 32),  # 设备详细型号,字符串格式,可能为空;Device detailed type. String format. It may be null.;
        ('nProtocalVer', c_int),  # 协议版本号;Protocol version number;
        ('szSoftWareVersion', c_char * 128),
        ('dwSoftwareBuildDate', C_DWORD),
        ('szPeripheralSoftwareVersion', c_char * 128),  # 从片版本信息,字符串格式,可能为空;From the Slice Version Information, The String Format, May Be Empty;
        ('dwPeripheralSoftwareBuildDate', C_DWORD),
        ('szGeographySoftwareVersion', c_char * 128),  # 地理信息定位芯片版本信息,字符串格式,可能为空;Geographical Iinformation Positioning Chip Version Information, The String Format, May Be empty;
        ('dwGeographySoftwareBuildDate', C_DWORD),
        ('szHardwareVersion', c_char * 128),
        ('dwHardwareDate', C_DWORD),
        ('szWebVersion', c_char * 128),
        ('dwWebBuildDate', C_DWORD),
        ('szDetailType', c_char * 64),  # 设备详细型号,字符串格式,可能为空;Device detailed type. String format. It may be null.;
        ('reserved', c_char * 192),
    ]

class NET_IN_GET_DEVICETYPE_INFO(Structure):
    """
    CLIENT_GetDeviceType 入参
    CLIENT_GetDeviceType input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_OUT_GET_DEVICETYPE_INFO(Structure):
    """
    CLIENT_GetDeviceType 出参
    CLIENT_GetDeviceType output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('szType', c_char * 32),  # 设备类型,该字段被废弃;Device Type, the field is discarded;
        ('szTypeEx', c_char * 256),  # 设备类型, 扩展设备类型建议使用此字段;Device Type, extending device type suggests using the field;
    ]

class NET_OSD_CHANNEL_TITLE(Structure):
    """
    编码物件-通道标题
    Encode widget-channel title
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('emOsdBlendType', C_ENUM),  # 叠加类型，不管是获取还是设置都要设置该字段 Refer: EM_A_NET_EM_OSD_BLEND_TYPE;Overlay Type, should set the value whether getting config or setting config Refer: EM_A_NET_EM_OSD_BLEND_TYPE;
        ('bEncodeBlend', C_BOOL),  # 是否叠加;Overlay or not;
        ('stuFrontColor', NET_COLOR_RGBA),  # 前景色;Foreground color;
        ('stuBackColor', NET_COLOR_RGBA),  # 背景色;Background color;
        ('stuRect', NET_RECT),  # 区域, 坐标取值[0~8191], 仅使用left和top值, 点(left,top)应和(right,bottom)设置成同样的点;Zone. The coordinates value ranges from 0 to 8191. Only use left value and top value.The point (left,top) shall be the same as the point(right,bottom).;
        ('emTextAlign', C_ENUM),  # 文本对齐方式 Refer: EM_TITLE_TEXT_ALIGNTYPE;Text alignment Refer: EM_TITLE_TEXT_ALIGNTYPE;
    ]

class NET_OSD_TIME_TITLE(Structure):
    """
    编码物件-时间标题
    Encode widget-Time title
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('emOsdBlendType', C_ENUM),  # 叠加类型，不管是获取还是设置都要设置该字段 Refer: EM_A_NET_EM_OSD_BLEND_TYPE;Overlay Type, should set the value whether getting config or setting config Refer: EM_A_NET_EM_OSD_BLEND_TYPE;
        ('bEncodeBlend', C_BOOL),  # 是否叠加;Overlay or not;
        ('stuFrontColor', NET_COLOR_RGBA),  # 前景色;Foreground color;
        ('stuBackColor', NET_COLOR_RGBA),  # 背景色;Background color;
        ('stuRect', NET_RECT),  # 区域, 坐标取值[0~8191], 仅使用left和top值, 点(left,top)应和(right,bottom)设置成同样的点;Zone. The coordinates value ranges from 0 to 8191. Only use left value and top value.The point (left,top) shall be the same as the point(right,bottom).;
        ('bShowWeek', C_BOOL),  # 是否显示星期;Display week or not;
    ]

class NET_CUSTOM_TITLE_INFO(Structure):
    """
    编码物件-自定义标题信息
    Encode widget-User-defined title information
    """
    _fields_ = [
        ('bEncodeBlend', C_BOOL),  # 是否叠加;Overlay or not;
        ('stuFrontColor', NET_COLOR_RGBA),  # 前景色;Foreground color;
        ('stuBackColor', NET_COLOR_RGBA),  # 背景色;Background color;
        ('stuRect', NET_RECT),  # 区域, 坐标取值[0~8191], 仅使用left和top值, 点(left,top)应和(right,bottom)设置成同样的点;Zone. The coordinates value ranges from 0 to 8191. Only use left value and top value.The point (left,top) shall be the same as the point(right,bottom).;
        ('szText', c_char * 1024),  # 标题内容;Title contents;
        ('emTitleType', C_ENUM),  # 叠加标题用途 Refer: EM_A_NET_EM_TITLE_TYPE;Overlapping heading purpose Refer: EM_A_NET_EM_TITLE_TYPE;
        ('emTextAlign', C_ENUM),  # 文本对齐方式 Refer: EM_TITLE_TEXT_ALIGNTYPE;Text alignment Refer: EM_TITLE_TEXT_ALIGNTYPE;
        ('byReserved', C_BYTE * 504),  # 保留字节;reserved;
    ]

class NET_OSD_CUSTOM_TITLE(Structure):
    """
    编码物件-自定义标题
    Encode widget-User-defined title
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('emOsdBlendType', C_ENUM),  # 叠加类型，不管是获取还是设置都要设置该字段 Refer: EM_A_NET_EM_OSD_BLEND_TYPE;Overlay Type, should set the value whether getting config or setting config Refer: EM_A_NET_EM_OSD_BLEND_TYPE;
        ('nCustomTitleNum', c_int),  # 自定义标题数量;User-defined title amount;
        ('stuCustomTitle', NET_CUSTOM_TITLE_INFO * 8),  # 自定义标题;User-defined title;
    ]

class NET_USER_DEF_TITLE_INFO(Structure):
    """
    用户自定义OSD-自定义标题信息
    UserTitle widget-User-defined title information
    """
    _fields_ = [
        ('szText', c_char * 1024),  # 标题内容;Title contents;
        ('bEncodeBlend', C_BOOL),  # 是否叠加;Overlay or not;
        ('bPreviewBlend', C_BOOL),  # 叠加到预览视频使能;Overlay Preview;
        ('stuRect', NET_RECT), # 区域, 坐标取值[0~8191], 仅使用left和top值, 点(left,top)应和(right,bottom)设置成同样的点;Zone. The coordinates value ranges from 0 to 8191. Only use left value and top value.The point (left,top) shall be the same as the point(right,bottom).;
        ('stuFrontColor', NET_COLOR_RGBA),  # 前景色;Foreground color;
        ('stuBackColor', NET_COLOR_RGBA),  # 背景色;Background color;
        ('emTextAlign', C_ENUM),  # 文本对齐方式 Refer: EM_TITLE_TEXT_ALIGNTYPE;Text alignment Refer: EM_TITLE_TEXT_ALIGNTYPE;
        ('byReserved', C_BYTE * 516),  # 保留字节;reserved;
    ]

class NET_OSD_USER_DEF_TITLE(Structure):
    """
    用户自定义OSD标题
    UserTitle widget-User-defined title
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nUserDefTitleNum', c_int),  # 自定义标题数量
        ('stuUserDefTitle', NET_USER_DEF_TITLE_INFO * 16),  # 自定义标题;User-defined title;
    ]

class NET_IN_GET_DEVICE_AII_INFO(Structure):
    """
    CLIENT_GetDeviceAllInfo 输入结构体
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 赋值为结构体大小;
    ]

class NET_STORAGE_PARTITION_INFO(Structure):
    """
    设备存储分区信息
    """
    _fields_ = [
        ('bError', C_BOOL),  # 分区是否异常;
        ('emType', C_ENUM),  # 分区属性类型 Refer: EM_PARTITION_TYPE;
        ('dTotalBytes', c_double),  # 分区总空间，单位字节;
        ('dUsedBytes', c_double),  # 分区使用空间;
        ('szPath', c_char * 128),  # 分区名字;
        ('byReserved', C_BYTE * 128),  # 保留字节;
    ]

class NET_DEVICE_STORAGE_INFO(Structure):
    """
    设备存储信息
    """
    _fields_ = [
        ('szNmae', c_char * 32),  # 设备名称;
        ('bSupportHotPlug', C_BOOL),  # 存储设备能否热插拔;
        ('fLifePercent', c_float),  # 寿命长度标识;
        ('emLockState', C_ENUM),  # SD卡加锁状态 Refer: EM_SD_LOCK_STATE;
        ('emSDEncryptFlag', C_ENUM),  # SD卡加密功能标识 Refer: EM_SD_ENCRYPT_FLAG;
        ('emHealthType', C_ENUM),  # 健康状态标识 Refer: EM_STORAGE_HEALTH_TYPE;
        ('emState', C_ENUM),  # 存储设备状态 Refer: EM_STORAGE_DEVICE_STATUS;
        ('stuPartitionInfo', NET_STORAGE_PARTITION_INFO * 12),  # 分区的具体信息;
        ('nPartition', c_int),  # 分区数量;
        ('byReserved', C_BYTE * 516),  # 保留字节;
    ]

class NET_OUT_GET_DEVICE_AII_INFO(Structure):
    """
    CLIENT_GetDeviceAllInfo 输出结构体
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 赋值为结构体大小;
        ('nInfoCount', c_int),  # 信息的个数;
        ('stuStorageInfo', NET_DEVICE_STORAGE_INFO * 8),  # 设备存储信息;
    ]

class NET_WPAN_RELAY_INFO(Structure):
    """
    中继状态
    Relay status
    """
    _fields_ = [
        ('emEnable', C_ENUM),  # 是否启用中继转发 Refer: EM_RELAY_TYPE;enable relay Refer: EM_RELAY_TYPE;
        ('nRelayIndex', c_int),  # 使用中继地址;index of relay;
        ('byReserved', C_BYTE * 32),  # 预留字段;reserved;
    ]

class NET_WPAN_HEARTBEAT_INFO(Structure):
    """
    心跳信息
    Heartbeat infomation
    """
    _fields_ = [
        ('nInterval', C_UINT),  # 心跳间隔，单位：秒;heartbeat interval, unit: s;
        ('nOfflineTimes', C_UINT),  # 离线次数;offline times;
        ('byReserved', C_BYTE * 32),  # 预留字段;reserved;
    ]

class NET_WPAN_ACCESSORY_CAPS_INFO(Structure):
    """
    配件能力集
    Accessory capability set
    """
    _fields_ = [
        ('bSupportAlarmTone', C_BOOL),  # 是否支持报警声音设置;whether alarm sound setting is supported;
        ('bSupportCardReader', C_BOOL),  # 是否支持读卡器;whether the card reader is supported;
        ('bSupportChime', C_BOOL),  # 是否支持门铃模式;whether the doorbell mode is supported;
        ('bSupportOverTemperatureAlarm', C_BOOL),  # 是否支持超温报警;whether over temperature alarm is supported;
        ('bSupportExternalWifi', C_BOOL),  # 是否支持外部wifi设置;whether external WiFi settings are supported;
        ('bSupportWifiInfo', C_BOOL),  # 是否支持wifi信息设置;whether WiFi information setting is supported;
        ('byreserve', C_BYTE * 32),  # 预留字段;reserved;
    ]

class NET_WPAN_ACCESSORY_LOCK_INFO(Structure):
    """
    登录失败的锁定信息
    Lock information of login failure
    """
    _fields_ = [
        ('bLockLoginEnable', C_BOOL),  # 登录锁定使能;login lock enable;
        ('nLoginFailLockTime', C_UINT),  # 登录失败锁定时间，单位：秒;login failure locking time, unit: s;
        ('byLockLoginTimes', C_BYTE),  # 登录失败可尝试次数;number of attempts after login failure;
        ('byReserved', C_BYTE * 31),  # 预留字段;reserved;
    ]

class NET_WPAN_CARD_READER_INFO(Structure):
    """
    读卡器配置
    Card reader configuration
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 读卡器使能;card reader enable;
        ('byEncryption', C_BYTE),  # 发卡时是否加密卡片，1：加密(软加密)；2：不加密;whether to encrypt the card when issuing, 1: encryption (soft encryption); 2: do not encrypt;
        ('byReserved', C_BYTE * 31),  # 预留字段;reserved;
    ]

class NET_WPAN_ACCESSORY_IMAGE_INFO(Structure):
    """
    图片信息
    Image information
    """
    _fields_ = [
        ('emResolution', C_ENUM),  # 分辨率 Refer: EM_A_CAPTURE_SIZE;resolution Refer: EM_A_CAPTURE_SIZE;
        ('nSnapshotNumber', c_int),  # 抓图数量;number of snapshots;
        ('nSnapshotTimes', c_int),  # 抓图次数;times of snapshots;
        ('byReserved', C_BYTE * 32),  # 预留字段;reserved;
    ]

class NET_WPAN_EXTERNAL_WIFI_INFO(Structure):
    """
    外部wifi信息
    External WiFi information
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 外部wifi使能;external WiFi enable;
        ('emPriority', C_ENUM),  # 外部wifi优先级 Refer: EM_EXTERNAL_WIFI_PRIORITY;external WiFi priority Refer: EM_EXTERNAL_WIFI_PRIORITY;
        ('byReserved', C_BYTE * 32),  # 预留字段;reserved;
    ]

class NET_WPAN_WIFI_INFO(Structure):
    """
    wifi信息
    WIFI information
    """
    _fields_ = [
        ('bSyncEnable', C_BOOL),  # Wi-Fi参数信息同步使能;wifi parameter information synchronization enable;
        ('szSSID', c_char * 128),  # wifi名称;wifi name;
        ('szPassword', c_char * 64),  # wifi密码;wifi password;
        ('byReserved', C_BYTE * 32),  # 预留字段;reserved;
    ]

class NET_WPAN_OVER_TEMPERATURE_ALARM_INFO(Structure):
    """
    超温报警
    Overtemperature alarm
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 超温报警使能开关;overtemperature alarm enable switch;
        ('dbLowerLimit', c_double),  # 超温报警下限温度值;over temperature alarm lower limit temperature value;
        ('dbUpperLimit', c_double),  # 超温报警上限温度值;over temperature alarm upper limit temperature value;
        ('byReserved', C_BYTE * 32),  # 预留字段;reserved;
    ]

class NET_WPAN_ARMING_INFO(Structure):
    """
    布防信息
    Arming infomation
    """
    _fields_ = [
        ('emType', C_ENUM),  # 布防模式 Refer: EM_ARMING_TYPE;arming type Refer: EM_ARMING_TYPE;
        ('bEnable', C_BOOL),  # 布防开关：布防时候是否使能该探测器;whether the detector is enabled during arming;
        ('bDelayEnable', C_BOOL),  # 延时使能：布防时候是否使用进入退出延时;whether to use the entry and exit during arming;
        ('byReserved', C_BYTE * 32),  # 预留字段;reserved;
    ]

class NET_WPAN_ACCESSORY_BUTTON_INFO(Structure):
    """
    按钮信息
    Button information
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 按键使能;key enable;
        ('emType', C_ENUM),  # 报警类型 Refer: EM_BUTTON_ALARM_TYPE;alarm type Refer: EM_BUTTON_ALARM_TYPE;
        ('nSirenLinkageNum', C_UINT),  # 警号联动个数;number of siren linkage;
        ('nSirenLinkage', c_int * 64),  # 警号联动;siren linkage;
        ('byReserved', C_BYTE * 32),  # 预留字段;reserved;
    ]

class NET_WPAN_ACCESSORY_INFO(Structure):
    """
    返回的配件信息
    Accessory information
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('bRecordEnable', C_BOOL),  # 录像使能，必须同时有RecordChannels;record enable, and recordchannels must be available at the same time;
        ('bExternalAlarmEnable', C_BOOL),  # 外部告警使能;external alarm enable;
        ('bArmingWithoutPassword', C_BOOL),  # 无密码布防使能;enable arming without password;
        ('byAlarmLedIndication', C_BYTE),  # 报警Led灯指示，0：关闭；1：打开;alarm LED indicator, 0: off, 1: Open;
        ('byExPowerCheck', C_BYTE),  # 控制检测外接电源状态的开关，0：关闭；1：打开;the switch for detecting the state of external power supply, 0: off, 1: Open;
        ('byTamper', C_BYTE),  # 配件防拆状态，0：关；1：开;anti disassembly status of accessory, 0: off, 1: Open;
        ('by24HDefenceStatus', C_BYTE),  # 24H防区状态，0：关；1：开;24h defense zone status, 0: off, 1: Open;
        ('byAlarmStatus', C_BYTE),  # 告警状态，0：正常；1：报警;alarm status, 0: normal, 1: Alarm;
        ('byExternalAlarmStatus', C_BYTE),  # 外部告警状态，0：正常；1：报警;external alarm status, 0: normal, 1: Alarm;
        ('byLedIndication', C_BYTE),  # Led灯指示，0：关；1：开;LED indicator, 0: off, 1: Open;
        ('byBeepIndication', C_BYTE),  # 布撤防以及进入退出延时是否有BEEP声音，0：无；1：有;whether there is beep sound during arming/disarming and entering/exiting delay, 0: none, 1: have;
        ('bySosStatus', C_BYTE),  # 紧急按钮状态，0：关；1：开;emergency button status, 0: off, 1: Open;
        ('byViaTrace', C_BYTE),  # 配件上报方式，0：直连；1：中继上报;accessory reporting method: 0: direct connection, 1: Relay Report;
        ('bySensorType', C_BYTE),  # 传感器类型，0：常闭；1：常开;sensor type, 0: normally closed, 1: normally open;
        ('byLockState', C_BYTE),  # 锁定状态，1：非锁定；2：锁定;locked state, 1: unlocked, 2: lock;
        ('bySensorFailure', C_BYTE),  # 传感器故障状态，0：正常；1：故障;sensor fault status, 0: normal, 1: malfunction;
        ('bySignalStrengthTest', C_BYTE),  # 信号强度测试，0：关；1：开;signal strength test, 0: off, 1: Open;
        ('bySensitivityTest', C_BYTE),  # 灵敏度测试，0：关；1：开;sensitivity test, 0: off, 1: Open;
        ('byVolumeTest', C_BYTE),  # 音量测试，0：关；1：开;volume test, 0: off, 1: Open;
        ('bySnapshotTest', C_BYTE),  # 抓图测试，0：关；1：开;snapshot test, 0: off; 1: Open;
        ('byWifiTest', C_BYTE),  # wifi测试，0：关；1：开;wifi test, 0: off; 1: Open;
        ('byBlockState', C_BYTE),  # 传感器屏蔽状态, 1:关闭屏蔽；2：开启屏蔽;sensor shielding status, 1: turn off shielding; 2: turn on shielding;
        ('nShortAddr', C_UINT),  # 配件短地址，从1开始;accessory short address, starting from 1;
        ('nPercent', C_UINT),  # 电池电量百分比：0~100;battery power percentage: 0 ~ 100;
        ('nSignalLevel', C_UINT),  # 无线信号强度等级;wireless signal strength level;
        ('nEntryDelay', C_UINT),  # 进入延时，单位：秒;entry delay, unit:s;
        ('nExitDelay', C_UINT),  # 退出延时，单位：秒;exit delay, unit:s;
        ('nAlarmDuring', C_UINT),  # 报警持续时间，单位：秒;alarm duration, unit:s;
        ('nTriggerAlarmInterval', c_int),  # 触发报警间隔时间，单位：秒;trigger alarm interval time, unit:S;
        ('emState', C_ENUM),  # 探测器状态 Refer: EM_DETECTOR_STATUS_TYPE;detector status Refer: EM_DETECTOR_STATUS_TYPE;
        ('emBeepVolume', C_ENUM),  # 设备布防时音量 Refer: EM_ACCESSORY_VOLUME;volume during arming Refer: EM_ACCESSORY_VOLUME;
        ('emSensentivity', C_ENUM),  # 灵敏度 Refer: EM_ACCESSORY_SENSITIVITY;sensitivity Refer: EM_ACCESSORY_SENSITIVITY;
        ('emPowerRegulation', C_ENUM),  # 功率调节 Refer: EM_POWER_REGULATION_TYPE;power regulation Refer: EM_POWER_REGULATION_TYPE;
        ('emOnline', C_ENUM),  # 在线状态 Refer: EM_ONLINE_STATUS;online status Refer: EM_ONLINE_STATUS;
        ('emAlarmType', C_ENUM),  # 报警类型 Refer: EM_ACCESSORY_ALARM_TYPE;alarm type Refer: EM_ACCESSORY_ALARM_TYPE;
        ('emInputType', C_ENUM),  # 输入类型 Refer: EM_ACCESSORY_INPUT_TYPE;input type Refer: EM_ACCESSORY_INPUT_TYPE;
        ('emLedBrightnessLevel', C_ENUM),  # LED亮度 Refer: EM_LED_BRIGHTNESS_LEVEL;LED brightness Refer: EM_LED_BRIGHTNESS_LEVEL;
        ('emOperationMode', C_ENUM),  # 操作模式 Refer: EM_OPERATION_MODE;operating mode Refer: EM_OPERATION_MODE;
        ('emAntiMispress', C_ENUM),  # 防误按模式 Refer: EM_ANTI_MISPRESS_TYPE;anti mispress mode Refer: EM_ANTI_MISPRESS_TYPE;
        ('emExPowerState', C_ENUM),  # 外部电源状态，若未开启检测外接电源状态则为未知 Refer: EM_EXPOWER_STATE;external power status(if the external power is not turned on, the status is unknown) Refer: EM_EXPOWER_STATE;
        ('emVolume', C_ENUM),  # 设备报警音量 Refer: EM_ACCESSORY_VOLUME;device alarm volume Refer: EM_ACCESSORY_VOLUME;
        ('fAmbientTemperature', c_float),  # 环境温度，单位：摄氏度;ambient temperature in degrees Celsius;
        ('szSN', c_char * 32),  # 配件序列号;accessory serial number;
        ('szName', c_char * 64),  # 配件名称;accessory name;
        ('szVersion', c_char * 64),  # 配件版本;accessory version;
        ('szModel', c_char * 64),  # 配件型号;accessory model;
        ('szAlarmTone', c_char * 128),  # 报警提示音;alarm tone;
        ('stuRelayTran', NET_WPAN_RELAY_INFO),  # 中继状态;relay status;
        ('emType', C_ENUM),  # 传感器感应方式 Refer: EM_A_NET_SENSE_METHOD;sensor sensing mode Refer: EM_A_NET_SENSE_METHOD;
        ('stuHeartbeat', NET_WPAN_HEARTBEAT_INFO),  # 心跳信息;heartbeat;
        ('stuCaps', NET_WPAN_ACCESSORY_CAPS_INFO),  # 配件能力集;accessory Capability Set;
        ('stuLockInfo', NET_WPAN_ACCESSORY_LOCK_INFO),  # 登录失败的锁定信息;lock information of login failure;
        ('stuCardReader', NET_WPAN_CARD_READER_INFO),  # 读卡器配置;card reader configuration;
        ('stuImageInfo', NET_WPAN_ACCESSORY_IMAGE_INFO),  # 图片信息;image information;
        ('stuExternalWifi', NET_WPAN_EXTERNAL_WIFI_INFO),  # 外部wifi信息;external WiFi information;
        ('stuWifiInfo', NET_WPAN_WIFI_INFO),  # Wi-Fi信息;wifi information;
        ('stuOverTemperatureAlarm', NET_WPAN_OVER_TEMPERATURE_ALARM_INFO),  # 超温报警;overtemperature alarm;
        ('nAreaNumberCnt', C_UINT),  # 所属区域个数;number of regions;
        ('nAreaNumber', c_int * 64),  # 所属区域编号，整形数组从1开始;region number, starting from 1;
        ('nControlAreaNumCnt', C_UINT),  # 控制区域个数;number of control areas;
        ('nControlAreaNum', c_int * 64),  # 控制区域编号：所属区域编号，从1开始；-1：全局，0：关闭;control area number, starting from 1(-1:global; 0:off);
        ('nRecordChannelsNum', C_UINT),  # 录像通道号个数;number of video channel numbers;
        ('nRecordChannels', c_int * 256),  # 录像通道号列表，一维数组，每个成员表示对应的通道需要执行录像，通道号从0开始;recording channel number list, one-dimensional array, each member indicates that the corresponding channel needs to perform recording, and the channel number starts from 0;
        ('nSirenLinkageNum', C_UINT),  # 警号联动个数;number of siren linkage;
        ('nSirenLinkage', c_int * 256),  # 警号联动;siren linkage;
        ('nArmingInfoNum', C_UINT),  # 布防信息个数;number of arming information;
        ('stuArmingInfo', NET_WPAN_ARMING_INFO * 4),  # 布防信息，最大4组;arming information, up to 4 groups;
        ('nButtonNum', C_UINT),  # 按键个数;number of button;
        ('stuButton', NET_WPAN_ACCESSORY_BUTTON_INFO * 16),  # 按键信息;key information;
    ]

class NET_GET_ACCESSORY_INFO(Structure):
    """
    获取配件信息(对应DEVSTATE_GET_ACCESSORY_INFO)
    Get accessory information(corresponding to DEVSTATE_GET_ACCESSORY_INFO)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nSNNum', C_UINT),  # 配件序列号数组个数（当个数为0时,返回主机下所有配件状态）;number of accessory serial number array (when the number is 0, the status of all accessories under the host is returned);
        ('szSN', c_char * 56 * 32),  # 配件序列号数组;accessory serial number array;
        ('nMaxInfoNum', C_UINT),  # 申请的配件个数;number of accessory applied;
        ('pstuInfo', POINTER(NET_WPAN_ACCESSORY_INFO)),  # 配件信息指针,由调用者分配内存,分配的大小为 nMaxInfoNum*sizeof(NET_WPAN_ACCESSORY_INFO);pointer fo tag array, user malloc the memory, the size is nMaxInfoNum*sizeof(NET_WPAN_ACCESSORY_INFO);
        ('nInfoNum', C_UINT),  # 返回的配件数;number of accessory returned;
    ]

class NET_IN_CTRL_LOWRATEWPAN_ACCESSORY_PARAM(Structure):
    """
    设置配件信息入参(对应CTRL_LOWRATEWPAN_SET_ACCESSORY_PARAM)
    Set accessory information(corresponding to CTRL_LOWRATEWPAN_SET_ACCESSORY_PARAM)
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # struct size;
        ('stuInfo', NET_WPAN_ACCESSORY_INFO),  # 配件信息;accessory information;
    ]

class NET_IN_UNIFIEDINFOCOLLECT_GET_DEVSTATUS(Structure):
    """
    获取设备状态入参
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;
    ]

class NET_DEVSTATUS_POWER_INFO(Structure):
    """
    电源电池相关信息
    """
    _fields_ = [
        ('nBatteryPercent', C_UINT),  # 电池电量百分比,0~100;
        ('emPowerType', C_ENUM),  # 供电类型 Refer: EM_A_NET_EM_POWER_TYPE;
    ]

class NET_DEVSTATUS_SIM_INFO(Structure):
    """
    sim卡状态信息
    """
    _fields_ = [
        ('emStatus', C_ENUM),  # SIM卡状态 Refer: EM_A_NET_EM_SIM_STATE;
        ('byIndex', C_BYTE),  # SIM卡编号;
        ('byReserved', C_BYTE * 31),  # 预留字段;
    ]

class NET_DEVSTATUS_NET_INFO(Structure):
    """
    网络相关信息
    """
    _fields_ = [
        ('nWifiIntensity', C_UINT),  # wifi信号强度等级，0~5，0表示没有信号;
        ('nWifiSignal', C_UINT),  # wifi信号强度，单位dbm, 0~100,0表示没有信号;
        ('nCellulSignal', C_UINT),  # 2g/3g/4g信号强度,单位dbm. 0~100, 0表示没有信号;
        ('nCellulIntensity', C_UINT),  # 2g/3g/4g信号强度等级,0~5, 0表示没有信号;
        ('emEthState', C_ENUM),  # 有线网连接状态 Refer: EM_A_NET_EM_ETH_STATE;
        ('n3Gflux', C_UINT),  # 蜂窝网络实际使用流量，单位：MB;
        ('n3GfluxByTime', C_UINT),  # 网络实际使用时长，单位：分钟;
        ('emWifiState', C_ENUM),  # 网络连接状态 Refer: EM_A_NET_EM_ETH_STATE;
        ('emCellularstate', C_ENUM),  # 蜂窝网络连接状态 Refer: EM_A_NET_EM_ETH_STATE;
        ('nSimNum', C_UINT),  # SIM卡数量;
        ('stuSimInfo', NET_DEVSTATUS_SIM_INFO * 8),  # SIM卡状态信息;
    ]

class NET_OUT_UNIFIEDINFOCOLLECT_GET_DEVSTATUS(Structure):
    """
    获取设备状态出参
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;
        ('stuPowerInfo', NET_DEVSTATUS_POWER_INFO),  # 电源电池相关信息;
        ('stuNetInfo', NET_DEVSTATUS_NET_INFO),  # 网络相关信息;
        ('szVersion', c_char * 32),  # 主机软件版本;
        ('emTamperState', C_ENUM),  # 主机防拆状态 Refer: EM_A_NET_EM_TAMPER_STATE;
    ]

class NET_RFID_CARD_INFO(Structure):
    """
    RFID卡片信息
    RFID Card information
    """
    _fields_ = [
        ('szCardId', c_char * 24),  # RFID卡片ID;RFID ID;
        ('byReserved', c_char * 128),  # 预留字节;Reserved;
    ]

class NET_A_DEV_EVENT_RADAR_REGION_DETECTION_INFO(Structure):
    """
    事件类型EVENT_IVS_RADAR_REGION_DETECTION(雷达警戒区检测事件)对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_RADAR_REGION_DETECTION
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('nAction', c_int),  # 0:脉冲 1:开始 2:停止;Event action, 0: Pulse, 1: Start, 2: Stop;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Timestamp (in milliseconds);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Time for the event occurred;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('nRuleID', C_UINT),  # 智能事件规则编号，用于标示哪个规则触发的事件;Rule ID,used to indicate which rule triggers;
        ('emClassType', C_ENUM),  # 智能事件所属大类 Refer: EM_CLASS_TYPE;Event class Refer: EM_CLASS_TYPE;
        ('stuFileInfo', SDK_EVENT_FILE_INFO),  # 事件对应文件信息;Event file info;
        ('nObjectNum', c_int),  # 检测到的对象个数;The number of object;
        ('stuObjects', NET_RADAR_DETECT_OBJECT * 100),  # 雷达检测对象列表;The list of objects which was detected;
        ('nPresetID', c_int),  # 事件触发的预置点号;PresetID;
        ('nDetectRegionNum', c_int),  # 检测区域顶点数;The number of stuDetectRegion;
        ('stuDetectRegion', SDK_POINT * 20),  # 检测区域,[0,8191];The region of alarm occur, [0,8191];
        ('stuSceneImage', SCENE_IMAGE_INFO_EX),  # 全景广角图（当图片超过1张时 使用stuSceneImageEx）;Scene image(UsestuSceneImageEx when there is more than one image);
        ('emAlarmType', C_ENUM),  # 报警类型 Refer: EM_RADAR_ALARM_TYPE;AlarmType Refer: EM_RADAR_ALARM_TYPE;
        ('szAlarmLevel', c_char * 16),  # 报警等级;Alarm level;
        ('nAlarmChannel', c_int),  # 报警输入通道号;Alarm input channel number;
        ('nRFIDCardIdNum', c_int),  # RFID卡片信息个数;RFID Number of card information;
        ('stuRFIDCardId', NET_RFID_CARD_INFO * 256),  # RFID卡片信息，最多支持256张卡片信息;RFID Card information, Up to 256 card information is supported;
        ('stuSceneImageEx', SCENE_IMAGE_INFO_EX * 10),  # 全景广角图（扩展为10张）;Panoramic wide-angle view (expanded to 10);
        ('nstuSceneImageExNum', c_int),  # 全景广角图个数;Number of panoramic wide-angle images;
        ('nSpeed', c_int),  # 触发事件目标的速度，用整型传输，扩大100倍 单位m/s;The speed of the trigger event target, transmitted by integer, expanded by 100 times, unit m/s;
        ('nTrackID', c_int),  # 触发事件目标的id,范围[0,63];id of trigger event target, range [0,63];
        ('nObjectType', c_int),  # 触发事件目标的类型的掩码: 0x00未识别目标 0x01目标为人 0x02目标为交通工具 0x03目标为树 0x04目标为建筑物 0x05目标为屏幕 0x06目标为动物 0x07目标为大船 0x08目标为中船 0x09目标为小船;Mask of the type of trigger event target: 0x00 unidentified target, 0x01 target is human, 0x02 target is vehicle, 0x03 target is tree, 0x04 target is building, 0x05 target is screen, 0x06 target is animal, 0x07 targets large ships, 0x08 targets medium ships, and 0x09 targets small ships;
        ('nAlarmFlag', c_int),  # 报警标志位，第0bit位表示是否超速，第1bit位表示是否AIS匹配 第2bit位表示是否禁行 第3bit位表示是否逆行;Alarm flag bit, the 0th bit indicates whether it is overspeeding, and the 1st bit indicates whether the AIS matches The 2nd bit indicates whether the line is prohibited, and the 3rd bit indicates whether it is retrograde;
        ('nLongitude', c_int),  # 经度，用整型传输，1000000倍，小数点后6位有效，不足6位用0补齐;longitude,Use integer transmission, 1000000 times, valid for 6 digits after the decimal point, and make up for less than 6 digits with 0;
        ('nLatitude', c_int),  # 纬度，用整型传输，1000000倍，小数点后6位有效，不足6位用0补齐;Latitude Use integer transmission, 1000000 times, valid for 6 digits after the decimal point, and make up for less than 6 digits with 0;
        ('nUpDownGoing', c_int),  # 车道/航道方向 -1:未知 0:无效 1:上行 2:下行;Lane / channel direction - 1: unknown 0: invalid 1: up 2: down;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('nDistance', c_int),  # 当前触发事件目标的像素极坐标值--距离，扩大100倍的结果,单位米;Pixel polar coordinate value of current trigger event target -- distance, result of 100 times expansion, unit: meter;
        ('nAngle', c_int),  # 当前触发事件目标的极坐标值--角度，扩大100倍的结果，单位度;Polar coordinate value of current trigger event target -- angle, result of 100 times expansion, unit:degree;
        ('byReserved', C_BYTE * 988),  # 预留字节;Reserved;
    ]

class NET_IN_FINDNUMBERSTAT(Structure):
    """
    接口(CLIENT_StartFindNumberStat)输入参数
    interface(CLIENT_StartFindNumberStat)'s input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小;size;
        ('nChannelID', c_int),  # 要进行查询的通道号;channel ID;
        ('stStartTime', NET_TIME),  # 开始时间 暂时精确到小时;start time;
        ('stEndTime', NET_TIME),  # 结束时间 暂时精确到小时;end time;
        ('nGranularityType', c_int),  # 查询粒度0:分钟,1:小时,2:日,3:周,4:月,5:季,6:年,7:即时, 8:人员 (7和8只在emRuleType为EM_RULE_MAN_NUM_DETECTION时有效);granularity type, 0:minute,1:hour,2:day,3:week,4:month,5:quarter,6:year7:instant, 8:person(7 and 8 are valid only when the emRuleType is EM_RULE_MAN_NUM_DETECTION);
        ('nWaittime', c_int),  # 等待接收数据的超时时间;wait time;
        ('nPlanID', C_UINT),  # 计划ID,仅球机有效,从1开始;Plan ID,Speed Dome use,start from 1;
        ('emRuleType', C_ENUM),  # 规则类型 Refer: EM_RULE_TYPE;rule type Refer: EM_RULE_TYPE;
        ('nMinStayTime', c_int),  # 区域人数查询最小滞留时间，不填默认为0，返回滞留时长大于等于该时间的人数信息NumberStat时不需要此参数;the minimum stay time,default value is 0; return the number of persons, the stay time of these persons are greater or equal to this timethis parameter is not required when the find type is NumberStat;
        ('nAreaIDNum', c_int),  # 区域ID个数;area id num;
        ('nAreaID', C_UINT * 20),  # 区域ID(一个预置点可以对应多个区域ID);Area ID(a preset point can correspond to multiple area IDs);
        ('emOtherRule', C_ENUM),  # 其他规则 Refer: EM_OTHER_RULE_TYPE;other rule Refer: EM_OTHER_RULE_TYPE;
        ('nGranularityExt', c_int),  # 当查询粒度为分钟时，用以细化具体粒度 不填默认5分钟粒度;When the query granularity is minutes, it is used to refine the specific granularity, default value is 5;
    ]

class NET_OUT_FINDNUMBERSTAT(Structure):
    """
    接口(CLIENT_StartFindNumberStat)输出参数
    CLIENT_StartFindNumberStat's output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小;
        ('dwTotalCount', C_DWORD),  # 符合此次查询条件的结果总条数;total count;
    ]

class NET_IN_DOFINDNUMBERSTAT(Structure):
    """
    接口(CLIENT_DoFindNumberStat)输入参数
    CLIENT_DoFindNumberStat's input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小;
        ('nBeginNumber', C_UINT),  # [0, totalCount-1], 查询起始序号,表示从beginNumber条记录开始,取count条记录返回;;[0, totalCount-1];
        ('nCount', C_UINT),  # 每次查询的流量统计条数;count;
        ('nWaittime', c_int),  # 等待接收数据的超时时间;wait time;
    ]

class NET_TEMPERATURE_STATISTICS_INFO(Structure):
    """
    温度统计信息
    Temperature statistics info
    """
    _fields_ = [
        ('nTotalCount', C_UINT),  # 总人数;total count;
        ('nHighTempCount', C_UINT),  # 
        ('nLowTempCount', C_UINT),  # 
        ('nNormalTempCount', C_UINT),  # 温度正常次数;normal temperature count;
        ('nNoMaskCount', C_UINT),  # 未带口罩总人数;no mask count;
        ('nTimeKey', C_UINT),  # 记录编号;time key;
        ('byReserved', C_BYTE * 1024),  # 预留字段;reserved;
    ]

class NET_A_NUMBERSTAT(Structure):
    """
    返回的人数统计信息
    the space application yb the user, the length unit is the dwsize of NUMBERSTAT
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nChannelID', c_int),  # 统计通道号;channel id;
        ('szRuleName', c_char * 32),  # 规则名称;rule name;
        ('stuStartTime', NET_TIME),  # 开始时间;start time;
        ('stuEndTime', NET_TIME),  # 结束时间;end time;
        ('nEnteredSubTotal', c_int),  # 进入人数小计;entered total;
        ('nExitedSubtotal', c_int),  # 出去人数小计;entered total;
        ('nAvgInside', c_int),  # 平均保有人数(除去零值);average number inside;
        ('nMaxInside', c_int),  # 最大保有人数;max number inside;
        ('nEnteredWithHelmet', c_int),  # 戴安全帽进入人数小计;people enter with helmet count;
        ('nEnteredWithoutHelmet', c_int),  # 不戴安全帽进入人数小计;people enter without helmet count;
        ('nExitedWithHelmet', c_int),  # 戴安全帽出去人数小计;people exit with helmet count;
        ('nExitedWithoutHelmet', c_int),  # 不戴安全帽出去人数小计;people exit without helmet count;
        ('nInsideSubtotal', c_int),  # 在区域内人数小计;the count of peoples in the region;
        ('nPlanID', C_UINT),  # 计划ID,仅球机有效,从1开始;Plan ID,Speed Dome use,start from 1;
        ('nAreaID', C_UINT),  # 区域ID(一个预置点可以对应多个区域ID);Area ID(a preset point can correspond to multiple area IDs);
        ('nAverageStayTime', C_UINT),  # 区域内平均滞留时间;Average Stay Time;
        ('stuTempInfo', NET_TEMPERATURE_STATISTICS_INFO),  # 温度统计信息(NET_IN_FINDNUMBERSTAT 字段 emRuleType 取值为 EM_RULE_ANATOMYTEMP_DETECT 时有效);Temperature statistics info ( valid when emRuleType in NET_IN_FINDNUMBERSTAT is EM_RULE_ANATOMYTEMP_DETECT );
        ('nPassedSubtotal', c_int),  # 经过人数小计;Passed Subtotaled;
        ('nEnteredDupSubtotal', C_UINT),  # 进入重复人数小计;Subtotal of duplicate entries;
        ('nExitedDupSubtotal', C_UINT),  # 出去重复人数小计;Subtotal of duplicate number of people going out;
        ('nEnteredNoDupSubtotal', C_UINT),  # 去重后的进入人数小计;Subtotal of entry numbers after weight removal;
        ('nExitedNoDupSubtotal', C_UINT),  # 去重后的出去人数小计;Subtotal of number of people going out after weight removal;
        ('nClusterAreaID', c_int),  # 多通道融合区域ID;Cluster area ID;
        ('nBatchTotal', c_int),  # 批次数小计;Subtotal of batch times;
    ]

class NET_OUT_DOFINDNUMBERSTAT(Structure):
    """
    接口(CLIENT_DoFindNumberStat)输出参数
    CLIENT_DoFindNumberStat's ouput param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小;
        ('nCount', c_int),  # 查询返回的人数统计信息个数;count;
        ('pstuNumberStat', POINTER(NET_A_NUMBERSTAT)),  # 返回的人数统计信息数组由用户申请内存，大小为nBufferLen;state array, the space application by the user;
        ('nBufferLen', c_int),  # 用户申请的内存大小,以NUMBERSTAT中的dwsize大小为单位;the space application yb the user, the length unit is the dwsize of NUMBERSTAT;
        ('nMinStayTime', c_int),  # 区域人数查询时指定的最小滞留时间;the minimum stay time when the find type is ManNumDetection;
    ]

class NET_IN_GET_DEVICE_LIST_INFO(Structure):
    """
    CLIENT_GetDeviceInfo 接口输入参数
    input parameter of interface CLIENT_GetDeviceInfo
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nCount', c_int),  # 设备个数;device num;
        ('szDeviceIDs', c_char * 1024 * 128),  # 设备信息列表;device id list;
    ]

class NET_GET_DEVICE_INFO(Structure):
    """
    已添加设备的结果信息
    the result information of added device
    """
    _fields_ = [
        ('szDeviceID', c_char * 128),  # 设备ID;device ID;
        ('szUrl', c_char * 512),  # url;url;
        ('szSerialNo', c_char * 32),  # 设备序列号;serial number;
        ('szDeviceType', c_char * 64),  # 设备类型;device type;
        ('szDeviceClass', c_char * 16),  # 设备大类;device class;
        ('nMacCount', c_int),  # 设备mac个数;device mac num;
        ('szMacs', c_char * 8 * 40),  # 设备mac地址组;device mac list;
        ('szDevSoftVersion', c_char * 128),  # 设备软件版本号;device software version;
        ('szDeviceName', c_char * 128),  # 设备名称;device name;
        ('szDetail', c_char * 512),  # 设备详细信息;device detail;
        ('nVideoInputCh', C_UINT),  # 视频输入通道数;video input channels num;
        ('nVideoOutputCh', C_UINT),  # 视频输出通道数;video output channels num;
        ('nAudioInputCh', C_UINT),  # 音频输入通道数;audio input channels num;
        ('nAudioOutputCh', C_UINT),  # 音频输出通道数;audio output channels num;
        ('nAlarmInputCh', C_UINT),  # 报警输入通道数;alarm input channels num;
        ('nAlarmOutputCh', C_UINT),  # 报警输出通道数;alarm output channels num;
        ('nErrorCode', C_UINT),  # 设备离线错误码;device off-line error code;
        ('nVtoDoors', C_UINT),  # 门禁设备可控制的门的总数;entrance guard vto door total num;
        ('byOnline', C_BYTE),  # 设备是否在线 0:离线 1：在线;whether the device is online 0:off-line 1:online;
        ('byReserved', C_BYTE * 511),  # 保留字节;reserved;
    ]

class NET_OUT_GET_DEVICE_LIST_INFO(Structure):
    """
    CLIENT_GetDeviceInfo 接口输出参数
    output parameter of interface CLIENT_GetDeviceInfo
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nMaxCount', c_int),  # 用户申请的设备个数;the count of the device in the user application;
        ('nRetCount', c_int),  # 实际返回的设备个数;return count from device;
        ('pstuDeviceInfo', POINTER(NET_GET_DEVICE_INFO)),  # 设备信息列表, 由用户申请和释放内存, 申请大小为sizeof(NET_GET_DEVICE_INFO)*nMaxCount;device info list, user malloc and free the memory,apply to sizeof(NET_GET_DEVICE_INFO)*nMaxCount;
    ]

class NET_IN_GET_CHANNEL_INFO(Structure):
    """
    CLIENT_GetChannelInfo 接口输入参数
    input parameter of interface CLIENT_GetChannelInfo
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szDeviceID', c_char * 128),  # 设备ID;device ID;
    ]

class NET_GET_CHANNEL_INFO(Structure):
    """
    获取设备通道信息结果信息
    the result information of device channel
    """
    _fields_ = [
        ('nRemoteChannel', C_UINT),  # 远程通道号;remote channel;
        ('nLogicChannel', c_int),  # 分配的逻辑通道,-1表示未分配;logic channel, -1 means not allocation;
        ('szName', c_char * 128),  # 名称;name;
        ('szDetail', c_char * 512),  # 设备详细信息;device detail;
        ('szDeviceType', c_char * 64),  # 设备类型;device type;
        ('szDeviceClass', c_char * 16),  # 设备大类;device class;
        ('szIP', c_char * 16),  # ip地址;ip;
        ('szMac', c_char * 40),  # 设备mac地址;device mac address;
        ('szSerialNo', c_char * 48),  # 设备序列号;serial number;
        ('szDevSoftVersion', c_char * 128),  # 设备软件版本号;device software version;
        ('nVideoInputCh', C_UINT),  # 视频输入通道数;video input channels num;
        ('nVideoOutputCh', C_UINT),  # 视频输出通道数;video output channels num;
        ('nAudioInputCh', C_UINT),  # 音频输入通道数;audio input channels num;
        ('nAudioOutputCh', C_UINT),  # 音频输出通道数;audio output channels num;
        ('nAlarmInputCh', C_UINT),  # 报警输入通道数;alarm input channels num;
        ('nAlarmOutputCh', C_UINT),  # 报警输出通道数;alarm output channels num;
        ('byOnline', C_BYTE),  # 通道是否在线0:离线 1：在线;whether the channel is online 0:off-line 1:online;
        ('byUsed', C_BYTE),  # 该通道是否被本地设备使用 0：未使用 1：使用;whether the channel is used by local device 0:unuse 1:used;
        ('byReserved', C_BYTE * 510),  # 保留字节;reserved;
    ]

class NET_OUT_GET_CHANNEL_INFO(Structure):
    """
    CLIENT_GetChannelInfo 接口输出参数
    output parameter of interface CLIENT_GetChannelInfo
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nMaxCount', c_int),  # 用户申请的通道个数;the count of the channel in the user application;
        ('nRetCount', c_int),  # 实际返回的通道个数;return channel count from device;
        ('pstuChannelInfo', POINTER(NET_GET_CHANNEL_INFO)),  # 通道信息列表, 由用户申请和释放内存, 申请大小为sizeof(NET_GET_CHANNEL_INFO)*nMaxCount;channel info list, user malloc and free the memory,apply to sizeof(NET_GET_CHANNEL_INFO)*nMaxCount;
    ]

class NET_MULTI_APPEND_EXTENDED_INFO(Structure):
    """
    扩展信息
    Extended Information
    """
    _fields_ = [
        ('nToken', C_UINT),  # 该次人脸导入的token值;The token value of this face import;
        ('emState', C_ENUM),  # 人脸导入状态 Refer: EM_FACE_APPEND_STATE;Face append state Refer: EM_FACE_APPEND_STATE;
        ('szResvered', c_char * 248),  # 保留字节;reserved bytes;
    ]

class NET_IN_BATCH_APPEND_FACERECONGNITION(Structure):
    """
    CLIENT_BatchAppendFaceRecognition 接口输入参数
    Input param of CLIENT_BatchAppendFaceRecognition
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nPersonNum', C_UINT),  # 需要添加的人员数量;the number of persons which are appended to the face DB;
        ('pstPersonInfo', POINTER(FACERECOGNITION_PERSON_INFOEX)),  # 人员信息，内存由用户申请，大小为nPersonNum * sizeof(FACERECOGNITION_PERSON_INFOEX);person info,memory is requested by user,and the size is nPersonNum * sizeof(FACERECOGNITION_PERSON_INFOEX);
        ('pBuffer', c_char_p),  # 缓冲地址;picture buffer;
        ('nBufferLen', C_UINT),  # 缓冲数据长度;length of picture buffer;
        ('bReserved', C_BYTE * 4),  # 字节对齐;alignment;
        ('stuInfo', NET_MULTI_APPEND_EXTENDED_INFO),  # 扩展信息;Extended Information;
    ]

class NET_BATCH_APPEND_PERSON_RESULT(Structure):
    """
    批量添加人员结果信息
    result of batch append persons
    """
    _fields_ = [
        ('nUID', C_UINT),  # 人员UID;UID;
        ('dwErrorCode', C_DWORD),  # 错误码信息;error code;
        ('szUID2', c_char * 64),  # 添加人员UID, 根据UIDType指定UID使用字段;Add personnel UID, specify UID field according to UIDType;
        ('bReserved', C_BYTE * 448),  # 保留字段;reserved;
    ]

class NET_OUT_BATCH_APPEND_FACERECONGNITION(Structure):
    """
    CLIENT_BatchAppendFaceRecognition 接口输出参数
    output param of CLIENT_BatchAppendFaceRecognition
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nResultNum', C_UINT),  # 批量添加结果个数，由用户指定，数值与NET_IN_BATCH_APPEND_FACERECONGNITION中的nPersonNum一致;number of result,it is set by user. The value is same with the nPersonNum in ET_IN_MULTI_APPEND_FACERECONGNITION;
        ('pstResultInfo', POINTER(NET_BATCH_APPEND_PERSON_RESULT)),  # 批量添加结果信息;result of batch append persons;
        ('nUIDType', C_UINT),  # 指定NET_BATCH_APPEND_PERSON_RESULT中的UID使用字段，不存在本字段或值为0则使用UID字段，若值为1则使用UID2字段;Specify the UID field in NET_BATCH_APPEND_PERSON_RESULT. If this field does not exist or the value is 0, the UID field will be used. If the value is 1, the UID2 field will be used.;
    ]

class NET_DISPOSITION_CHANNEL_INFO(Structure):
    """
    布控的视频通道信息
    info of disposition channel
    """
    _fields_ = [
        ('nChannelID', c_int),  # 视频通道号;channel ID;
        ('nSimilary', c_int),  # 相似度阈值, 0-100;similary, 0-100;
        ('bReserved', C_BYTE * 256),  # 保留;Reserved;
    ]

class NET_IN_FACE_RECOGNITION_PUT_DISPOSITION_INFO(Structure):
    """
    CLIENT_FaceRecognitionPutDisposition 接口输入参数
    input parameter of CLIENT_FaceRecognitionPutDisposition
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szGroupId', c_char * 64),  # 人员组ID;group ID;
        ('nDispositionChnNum', c_int),  # 布控视频通道个数;count of disposition channels;
        ('stuDispositionChnInfo', NET_DISPOSITION_CHANNEL_INFO * 1024),  # 布控视频通道信息;info of disposition channels;
    ]

class NET_OUT_FACE_RECOGNITION_PUT_DISPOSITION_INFO(Structure):
    """
    CLIENT_FaceRecognitionPutDisposition 接口输出参数
    output parameter of CLIENT_FaceRecognitionPutDisposition
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nReportCnt', c_int),  # 通道布控结果个数;the result count;
        ('bReport', C_BOOL * 1024),  # 通道布控结果, TRUE追加成功, FALSE追加失败;the result, TRUE-success, FALSE-failed;
    ]

class NET_IN_FACE_RECOGNITION_DEL_DISPOSITION_INFO(Structure):
    """
    CLIENT_FaceRecognitionDelDisposition 接口输入参数
    input parameter of CLIENT_FaceRecognitionDelDisposition
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # the size of this struct;
        ('szGroupId', c_char * 64),  # 人员组ID;group ID;
        ('nDispositionChnNum', c_int),  # 撤控视频通道个数;the count of disposition channels;
        ('nDispositionChn', c_int * 1024),  # 撤控视频通道列表;the list of disposition channels;
    ]

class NET_OUT_FACE_RECOGNITION_DEL_DISPOSITION_INFO(Structure):
    """
    CLIENT_FaceRecognitionDelDisposition 接口输出参数
    output parameter of CLIENT_FaceRecognitionDelDisposition
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # the size of this struct;
        ('nReportCnt', c_int),  # 通道布控结果个数;the result count;
        ('bReport', C_BOOL * 1024),  # 通道布控结果, TRUE删除成功, FALSE删除失败;the result, TRUE-success, FALSE-falied;
    ]

class NET_CB_ADDFILESTATE(Structure):
    """
    fAddFileStateCB 参数
    fAddFileStateCB param
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szFileName', POINTER(c_char)),  # 文件名称;file name;
        ('szState', POINTER(c_char)),  # 文件分析状态, "Successed",成功; "Failed",失败；;analyse file's state, "Successed" ; "Failed" ;;
    ]

class NET_IN_ADDFILE_STATE(Structure):
    """
    CLIENT_AttacAddFileState()接口输入参数
    CLIENT_AttacAddFileState()interface input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('cbAttachState', CB_FUNCTYPE(None, C_LLONG, C_LLONG, POINTER(NET_CB_ADDFILESTATE), c_int, C_LDWORD)),  # 订阅增加文件状态回调;listenint to increase callback file state;
        ('dwUser', C_LDWORD),  # 用户数据;user's data;
    ]

class NET_OUT_ADDFILE_STATE(Structure):
    """
    CLIENT_AttacAddFileState()接口输入参数
    CLIENT_AttacAddFileState()interface input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),
    ]

class NET_SMALL_PIC_INFO(Structure):
    """
    大图中小图的信息
    the small image info in the large image
    """
    _fields_ = [
        ('nSmallPicId', c_int),  # 小图ID;small image ID;
        ('stuRect', NET_RECT),  # 小图在大图中的位置;the postion of the small image in the large image;
        ('emDetectObjType', C_ENUM),  # 目标类型 Refer: EM_OBJECT_TYPE;bject type Refer: EM_OBJECT_TYPE;
        ('bReserved', C_BYTE * 124),  # 保留字节;Reserved;
    ]

class NET_IMAGE_RELATION(Structure):
    """
    一张大图检测到小图的结果
    the result of detection small image from the large image
    """
    _fields_ = [
        ('nBigPicId', c_int),  # 大图ID;large image ID;
        ('nSmallPicNum', c_int),  # 大图中小图张数;the number of small image in the large image;
        ('stuSmallPicInfo', NET_SMALL_PIC_INFO * 32),  # 大图中小图的信息;the info of small image in the large image;
        ('emDetectErrCode', C_ENUM),  # 大图检测小图结果错误码 Refer: EM_MULTIFACE_DETECT_ERRCODE;Error code of multi detect in scene image Refer: EM_MULTIFACE_DETECT_ERRCODE;
        ('bReserved', C_BYTE * 124),  # 保留字节;Reserved;
    ]

class NET_CB_MULTIFACE_DETECT_STATE(Structure):
    """
    订阅大图检测小图进度回调结构体
    the callback struct of detection small image from the large image
    """
    _fields_ = [
        ('nProgress', c_int),  # 检测进度;the progress of detection;
        ('stuImageRelation', NET_IMAGE_RELATION),  # 大图检测小图的检测结果;the result of detection small image from the large image;
        ('byReserved', C_BYTE * 512),  # 保留字节;Reserved;
    ]

class NET_A_HUMAN_ATTRIBUTES_INFO(Structure):
    """
    人体属性信息
    Human attributes info
    """
    _fields_ = [
        ('emCoatColor', C_ENUM),  # 上衣颜色 Refer: EM_CLOTHES_COLOR;Coat color Refer: EM_CLOTHES_COLOR;
        ('emCoatType', C_ENUM),  # 上衣类型 Refer: EM_COAT_TYPE;Coat type Refer: EM_COAT_TYPE;
        ('emTrousersColor', C_ENUM),  # 裤子颜色 Refer: EM_CLOTHES_COLOR;Trousers color Refer: EM_CLOTHES_COLOR;
        ('emTrousersType', C_ENUM),  # 裤子类型 Refer: EM_TROUSERS_TYPE;Trousers type Refer: EM_TROUSERS_TYPE;
        ('emHasHat', C_ENUM),  # 是否戴帽子 Refer: EM_HAS_HAT;whether has hat Refer: EM_HAS_HAT;
        ('emHasBag', C_ENUM),  # 是否带包 Refer: EM_HAS_BAG;whether has bag Refer: EM_HAS_BAG;
        ('stuBoundingBox', NET_RECT),  # 包围盒(8192坐标系);BoundingBox(8192 coordinates);
        ('nAge', c_int),  # 年龄;Age;
        ('emSex', C_ENUM),  # 性别 Refer: EM_SEX_TYPE;Six Refer: EM_SEX_TYPE;
        ('emAngle', C_ENUM),  # 角度 Refer: EM_ANGLE_TYPE;Angle Refer: EM_ANGLE_TYPE;
        ('emHasUmbrella', C_ENUM),  # 是否打伞 Refer: EM_HAS_UMBRELLA;Umbrella state Refer: EM_HAS_UMBRELLA;
        ('emBag', C_ENUM),  # 包类型 Refer: EM_BAG_TYPE;Bag type Refer: EM_BAG_TYPE;
        ('emUpperPattern', C_ENUM),  # 上半身衣服图案 Refer: EM_CLOTHES_PATTERN;Upper Pattern Refer: EM_CLOTHES_PATTERN;
        ('emHairStyle', C_ENUM),  # 头发样式 Refer: EM_HAIR_STYLE;Hair style Refer: EM_HAIR_STYLE;
        ('emCap', C_ENUM),  # 帽类型 Refer: EM_CAP_TYPE;Cap type Refer: EM_CAP_TYPE;
        ('stuHumanCenter', SDK_POINT),  # 人体型心(不是包围盒中心), 0-8191相对坐标, 相对于大图;Center of human(not center of bounding box), 0-8191 relative coordinates, relative to large graph;
        ('emHasVest', C_ENUM),  # 是否有反光背心; Refer: EM_HAS_VEST;Is there a reflective vest Refer: EM_HAS_VEST;
        ('emHasBadge', C_ENUM),  # 是否佩戴工牌 Refer: EM_HAS_BADGE;Whether to wear a badge Refer: EM_HAS_BADGE;
        ('emHasBabyCarriage', C_ENUM),  # 是否推婴儿车 Refer: EM_HAS_BABYCARRIAGE;Whether to push a baby carriage Refer: EM_HAS_BABYCARRIAGE;
        ('emIsErrorDetect', C_ENUM),  # 是否虚检（背景误检，仅头，仅下半身都会判定为虚检） Refer: EM_IS_ERRORDETECT;Whether is error detect or not Refer: EM_IS_ERRORDETECT;
        ('emHasHead', C_ENUM),  # 人体部位是否有头 Refer: EM_HAS_HEAD;Whether has head Refer: EM_HAS_HEAD;
        ('emHasDownBody', C_ENUM),  # 人体部位是否有下半身 Refer: EM_HAS_DOWNBODY;Whether has down body Refer: EM_HAS_DOWNBODY;
        ('nAngleConf', C_UINT),  # 姿态置信度，质量评估总分0到100;degree of confidence about Angle, range is [0,100];
        ('nUpColorConf', C_UINT),  # 上衣颜色置信度，质量评估总分0到100;degree of confidence about UpColor, range is [0,100];
        ('nDownColorConf', C_UINT),  # 下衣颜色置信度，质量评估总分0到100;degree of confidence about DownColor, range is [0,100];
        ('nGenderConf', C_UINT),  # 性别置信度，质量评估总分0到100;degree of confidence about Gender, range is [0,100];
        ('nAgeConf', C_UINT),  # 年龄段置信度，质量评估总分0到100;degree of confidence about Age, range is [0,100];
        ('nHatTypeConf', C_UINT),  # 帽子类型置信度，质量评估总分0到100;degree of confidence about HatType, range is [0,100];
        ('nUpTypeConf', C_UINT),  # 上衣种类置信度，质量评估总分0到100;degree of confidence about UpType, range is [0,100];
        ('nDownTypeConf', C_UINT),  # 下衣种类置信度，质量评估总分0到100;degree of confidence about DownType, range is [0,100];
        ('nHairTypeConf', C_UINT),  # 发型种类置信度，质量评估总分0到100;degree of confidence about Hair, range is [0,100];
        ('nHasHeadConf', C_UINT),  # 人体部位是否有头的置信度，质量评估总分0到100;degree of confidence about HasHead, range is [0,100];
        ('nHasDownBodyConf', C_UINT),  # 人体部位是否有下半身置信度，质量评估总分0到100;degree of confidence about HasDownBody, range is [0,100];
        ('nUniformStyleConf', C_UINT),  # 制服类型置信度，质量评估总分0到100;degree of confidence about UniformStyle, range is [0,100];
        ('nCoatType', c_char),  # 上衣类型，emCoatType实现和协议不一致，兼容处理，0:未知 1:长袖 2:短袖 3:长款大衣 4:夹克及牛仔服 5:T恤；6:运动装 7:羽绒服 8:衬衫 9:连衣裙 10:西装 11:毛衣 12:无袖 13:背心;Coat type, emCoatType implementation is inconsistent with the protocol0:Unknown 1:Long sleeve 2:Short sleeve 3:Long coat 4:Jacket and jeans 5: T-shirt6:Sportswear 7:Down-filled coat 8:shirt 9:Dress 10:suit 11:sweater 12:Sleeveless 13:vest;
        ('byReserved', C_BYTE * 3),  # 预留字节;Reserved;
    ]

class NET_PIC_INFO_EX(Structure):
    """
    图片信息(目前仅用于机动车和非机动车)
    Image information (currently only for motor vehicles and non-motor vehicles)
    """
    _fields_ = [
        ('nLength', C_UINT),  # 图片大小,单位:字节;Image size, unit: bytes;
        ('nWidth', C_UINT),  # 图片宽度;Image width;
        ('nHeight', C_UINT),  # 图片高度;Image height;
        ('byReserverd', c_char * 4),  # 用于字节对齐;for byte alignment;
        ('szFilePath', c_char * 256),  # 图片路径;image path;
        ('szReserverd', c_char * 256),  # 保留字节;reserved bytes;
    ]

class NET_HISTORY_TRAFFIC_CAR_INFO(Structure):
    """
    机动车信息
    Vehicle Information
    """
    _fields_ = [
        ('szUID', c_char * 64),  # 非机动车唯一标识符;non-motor vehicle unique identifier;
        ('stuBoundingBox', NET_RECT),  # 包围盒(8192坐标系);Bounding box (8192 coordinate system);
        ('szPlateNumber', c_char * 32),  # 车牌号码;license plate number;
        ('szPlateType', c_char * 32),  # 车牌类型;license plate type;
        ('szPlateColor', c_char * 32),  # 车牌颜色;license plate color;
        ('szVehicleColor', c_char * 32),  # 车身颜色;body color;
        ('szCategory', c_char * 32),  # 车辆类型;vehicle type;
        ('szSpecialCar', c_char * 32),  # 特种车辆;special vehicle;
        ('szVehicleSign', c_char * 64),  # 车辆标识;vehicle sign;
        ('nSubBrand', C_UINT),  # 车辆子品牌;vehicle sub-brand;
        ('nBrandYear', C_UINT),  # 车辆年款;Vehicle year;
        ('nFurnitureCount', C_UINT),  # 摆件数量;number of ornaments;
        ('nPendantCount', C_UINT),  # 挂件数量;number of pendants;
        ('nAnnualInspectionCount', C_UINT),  # 年检标数量;Number of annual inspections;
        ('nAnnualInspectionShape', c_int),  # 年检标顺序, 0: 未知 1: 乱排 2: 横排 3: 竖排;annual inspection order, 0: unknown 1: random 2: horizontal 3: vertical;
        ('emSunShade', C_ENUM),  # 主驾驶遮阳板状态 Refer: EM_A_NET_SUNSHADE_STATE;main driver sunshade state Refer: EM_A_NET_SUNSHADE_STATE;
        ('emSubSeatSunShade', C_ENUM),  # 副驾驶遮阳板状态 Refer: EM_A_NET_SUNSHADE_STATE;copilot sunshade state Refer: EM_A_NET_SUNSHADE_STATE;
        ('nCardCount', C_UINT),  # 卡片数量;number of cards;
        ('emSafeBelt', C_ENUM),  # 主驾驶安全带 Refer: EM_A_NET_SAFEBELT_STATE;main driver's seat belt Refer: EM_A_NET_SAFEBELT_STATE;
        ('nCalling', c_int),  # 是否在打电话, 0: 未知 1: 否 2: 是;is calling, 0: unknown 1: no 2: yes;
        ('nPlayPhone', c_int),  # 是否在玩手机, 0: 未知 1: 否 2: 是;Whether the phone is playing, 0: unknown 1: no 2: yes;
        ('nSmoking', c_int),  # 是否在抽烟, 0: 未知 1: 否 2: 是;smoking, 0: unknown 1: no 2: yes;
        ('nSubSeatPeople', c_int),  # 副驾驶是否有人, 0: 未知 1: 否 2: 是;Is there anyone in the co-pilot, 0: unknown 1: no 2: yes;
        ('emSubSeatSafeBelt', C_ENUM),  # 副驾驶安全带 Refer: EM_A_NET_SAFEBELT_STATE;passenger seat belt Refer: EM_A_NET_SAFEBELT_STATE;
        ('nHoldBaby', c_int),  # 是否抱小孩, 0: 未知 1: 否 2: 是;whether to hold the baby, 0: unknown 1: no 2: yes;
        ('nSunroof', c_int),  # 是否有天窗, 0: 未知 1: 否 2: 是;whether there is a sunroof, 0: unknown 1: no 2: yes;
        ('nLuggageRack', c_int),  # 是否有行李架, 0: 未知 1: 否 2: 是;whether there is a luggage rack, 0: unknown 1: no 2: yes;
        ('nVehicleCollision', c_int),  # 是否有车辆撞损, 0: 未知 1: 否 2: 是;whether there is a vehicle crash, 0: unknown 1: no 2: yes;
        ('nVehiclePrint', c_int),  # 是否有喷绘, 0: 未知 1: 否 2: 是;whether there is a print, 0: unknown 1: no 2: yes;
        ('nBackupTire', c_int),  # 是否有备胎, 0: 未知 1: 否 2: 是;whether there is a spare tire, 0: unknown 1: no 2: yes;
        ('nTrunk', c_int),  # 后备箱状态, 0: 未知 1: 关闭 2: 打开;trunk status, 0: unknown 1: closed 2: open;
        ('nPlateAttribute', c_int),  # 车牌污损状态, 0: 未知 1: 正常 2: 无牌 3: 部分遮挡/污损 4: 完全遮挡/污损;license plate defacement status, 0: unknown 1: normal 2: no plate 3: partially occluded/defaced 4: fully occluded/defaced;
        ('nMuskHide', c_int),  # 渣土车遮盖状态, 0: 未知 1: 有遮盖 2: 无遮盖空载 3: 无遮盖满载;Muck cover status, 0: Unknown 1: Covered 2: Uncovered empty 3: Uncovered full;
        ('stuImage', NET_PIC_INFO_EX),  # 机动车图片信息;Motor vehicle picture information;
        ('nPressParkingStatus', c_int),  # 车辆停车是否压线, 0: 未知 1: 未压线停车 2: 压线停车;Whether the vehicle is parked and pressed, 0: Unknown 1: Parking without pressing the wire 2: Parking when the wire is pressed;
        ('szReserved', c_char * 256),  # 保留字节;reserved bytes;
    ]

class NET_IMAGE_RELATION_LIST(Structure):
    """
    一张大图检测结果列表
    A list of test results for a large image
    """
    _fields_ = [
        ('pszFeature', POINTER(c_char)),  # base64特征值;base64 feature data;
        ('nFeatureLen', c_int),  # base64特征值长度;base64 feature data length;
        ('szFeatureID', c_char * 64),  # 特征ID;Feature ID;
        ('stuFaceData', NET_FACE_DATA),  # 人脸数据;Face data;
        ('stuHumanAttributes', NET_A_HUMAN_ATTRIBUTES_INFO),  # 人体属性;Human attribute;
        ('stuNonMotor', VA_OBJECT_NONMOTOR),  # 非机动车信息;Nonmotor info;
        ('szAlgorithmVersion', c_char * 32),  # 特征版本号;The version of algorithm;
        ('szVendor', c_char * 32),  # 厂商;Vendor;
        ('emObjectType', C_ENUM),  # 目标类型 Refer: EM_OBJECT_TYPE;Object type Refer: EM_OBJECT_TYPE;
        ('stuRectPoint', SDK_POINT * 2),  # 矩形区域;Rectangular area;
        ('stuHistoryTrafficCar', NET_HISTORY_TRAFFIC_CAR_INFO),  # 机动车属性;History Traffic Car;
        ('bReserved', C_BYTE * 1024),  # 保留字节;Reserved;
    ]

class NET_IMAGE_RELATION_EX_IMAGEINFO(Structure):
    """
    小图信息
    Thumbnail information
    """
    _fields_ = [
        ('nOffset', c_int),  # 在二进制数据块中的偏移;Offset in binary data block;
        ('nLength', c_int),  # 图片大小,单位字节;Picture size,Unit byte;
        ('szReserved', c_char * 16),  # 预留字节;Reserved;
    ]

class NET_IMAGE_RELATION_EX(Structure):
    """
    一张大图检测到小图的结果
    A small image is detected in a large image
    """
    _fields_ = [
        ('szRequestID', c_char * 64),  # 图片的请求ID;Request ID;
        ('nBigPicId', c_int),  # 大图ID;Large image ID;
        ('nSmallPicNum', c_int),  # 大图中小图张数;Number of small pictures in large picture;
        ('stuSmallPicInfo', NET_SMALL_PIC_INFO * 32),  # 大图中小图的信息;Info of small pictures in large picture;
        ('emDetectErrCode', C_ENUM),  # 大图检测小图结果错误码 Refer: EM_MULTIFACE_DETECT_ERRCODE;Error code of small image result detected by large image Refer: EM_MULTIFACE_DETECT_ERRCODE;
        ('stuImageRelation', NET_IMAGE_RELATION_LIST * 32),  # 大图检测结果列表;List of test results for a large image;
        ('nstuImageRelationNum', c_int),  # 大图检测结果列表个数;Number of test results for a large image;
        ('nToken', C_UINT),  # 查询令牌;Token;
        ('stuImageInfo', NET_IMAGE_RELATION_EX_IMAGEINFO * 32),  # 小图信息;Thumbnail information;
        ('nImageNum', c_int),  # 小图信息个数;Thumbnail information number;
        ('pData', POINTER(c_char)),  # 小图图片数据;Picture data;
        ('bReserved', C_BYTE * 248),  # 保留字节;Reserved;
    ]

class NET_CB_MULTIFACE_DETECT_STATE_EX(Structure):
    """
    订阅大图检测小图进度回调结构体
    Attach to large image to detect small image progress callback info
    """
    _fields_ = [
        ('nProgress', c_int),  # 检测进度;Inspection progress;
        ('stuImageRelation', NET_IMAGE_RELATION_EX),  # 大图检测小图的检测结果;Test results of large image and small image;
        ('byReserved', C_BYTE * 512),  # 保留字节;Reserved;
    ]

class NET_IN_MULTIFACE_DETECT_STATE(Structure):
    """
    CLIENT_AttachDetectMultiFaceState 接口输入参数
    the input parameter of interface CLIENT_AttachDetectMultiFaceState
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小;the size of this struct;
        ('bReserved', C_BYTE * 4),  # 用于字节对齐;for byte alignment;
        ('cbMultiFaceDetectState', CB_FUNCTYPE(None, C_LLONG, POINTER(NET_CB_MULTIFACE_DETECT_STATE), C_LDWORD)),  # 回调函数;callback function;
        ('dwUser', C_LDWORD),  # 用户数据;user data;
        ('cbMultiFaceDetectStateEx', CB_FUNCTYPE(None, C_LLONG, POINTER(NET_CB_MULTIFACE_DETECT_STATE_EX), C_LDWORD)),  # 回调函数扩展（推荐使用）;Callback function extension (recommended);
        ('nTokens', C_UINT * 10),  # 查询令牌;Tokens;
        ('nTokensNum', c_int),  # 查询令牌个数, 若为0，则默认订阅token为0的检测, 若为-1表示订阅全部token;Number of tokens, 0 means subscribe to all;
    ]

class NET_OUT_MULTIFACE_DETECT_STATE(Structure):
    """
    CLIENT_AttachDetectMultiFaceState 接口输出参数
    the output parameter of interface CLIENT_AttachDetectMultiFaceState
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小;the size of this struct;
    ]

class NET_DETECT_BIG_PIC_INFO(Structure):
    """
    大图信息(大图抠小图功能)
    large image info (the function of detect small image from large image)
    """
    _fields_ = [
        ('nPicID', c_int),  # 大图ID;large image ID;
        ('dwOffSet', C_DWORD),  # 文件在二进制数据块中的偏移位置, 单位:字节;the offset position of the large image in the binary data, unit:bytes;
        ('dwFileLenth', C_DWORD),  # 文件大小, 单位:字节;the length of the file, unit:bytes;
        ('dwWidth', C_DWORD),  # 图片宽度, 单位:像素;the width of this image, unit:pixel;
        ('dwHeight', C_DWORD),  # 图片高度, 单位:像素;the height of this image, unit:pixel;
        ('nDetectRegionNum', c_int),  # 规则检测区域顶点数;Points number of detect region;
        ('stuDetectRegion', SDK_POINT * 20),  # 规则检测区域;Detect region;
        ('bReserved', C_BYTE * 44),  # 保留字节;Reserved;
    ]

class NET_DETECT_BIG_PIC_INFO_EX(Structure):
    """
    大图信息(大图抠小图功能)
    Large image info (the function of detect small image from large image)
    """
    _fields_ = [
        ('nPicID', c_int),  # 大图ID;Large image ID;
        ('dwOffSet', C_DWORD),  # 文件在二进制数据块中的偏移位置, 单位:字节;The offset position of the large image in the binary data, unit:bytes;
        ('dwFileLenth', C_DWORD),  # 文件大小, 单位:字节;The length of the file, unit:bytes;
        ('dwWidth', C_DWORD),  # 图片宽度, 单位:像素;The width of this image, unit:pixel;
        ('dwHeight', C_DWORD),  # 图片高度, 单位:像素;The height of this image, unit:pixel;
        ('nDetectRegionNum', c_int),  # 规则检测区域顶点数;Points number of detect region;
        ('stuDetectRegion', SDK_POINT * 20),  # 规则检测区域;Detect region;
        ('szRequestID', c_char * 64),  # 请求图片ID;Request ID;
        ('szPath', c_char * 256),  # 通过URL下载图片;URL address about image;
        ('emCoordinateType', C_ENUM),  # 坐标系类型 Refer: EM_COORDINATE_TYPE;Coordinate type Refer: EM_COORDINATE_TYPE;
        ('emObjectType', C_ENUM),  # 目标类型 Refer: EM_DETECT_OBJECT_TYPE;Detect object type Refer: EM_DETECT_OBJECT_TYPE;
        ('nTargetType', C_UINT),  # 按位组合，全1表示全检测,1表示人脸，2表示人体，4表示机动车，8表示非机动整体, 16表示非机动车;By bit combination, all 1 means full detection, 1 means face, 2 means human body, 4 means motor vehicle, 8 means non motor vehicle, 16 means non motor vehicle;
        ('nProcessTypeNum', c_int),  # 处理类型个数;Count of process type;
        ('emProcessType', C_ENUM * 8),  # 处理类型 Refer: EM_DETECT_PROCESS_TYPE;Process type Refer: EM_DETECT_PROCESS_TYPE;
        ('szData', POINTER(c_char)),  # 全景大图数据，经过Base64后的字符串 无该字段或该字段为空则使用二进制图片数据;Scene image data, if the string after Base64 does not have this field or the field is empty, binary image data will be used;
        ('nDataLen', c_int),  # 全景大图数据长度;Scene image length;
        ('bReserved', C_BYTE * 1016),  # 保留字节;Reserved;
    ]

class NET_IN_FACE_RECOGNITION_DETECT_MULTI_FACE_INFO(Structure):
    """
    CLIENT_FaceRecognitionDetectMultiFace 接口输入参数
    the input parameter of interface CLIENT_FaceRecognitionDetectMultiFace
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体的大小;the size of this struct;
        ('nBigPicNum', c_int),  # 大图张数;the number of large image;
        ('stuBigPicInfo', NET_DETECT_BIG_PIC_INFO * 50),  # 大图信息（推荐使用stuBigPicInfoEx）;the info of large image(stuBigPicInfoEx is recommended);
        ('pBuffer', c_char_p),  # 缓冲地址;the buffer of the image;
        ('nBufferLen', c_int),  # 缓冲数据长度;the length of th buffer;
        ('emDetectObjType', C_ENUM),  # 目标类型 Refer: EM_OBJECT_TYPE;Object type Refer: EM_OBJECT_TYPE;
        ('bBigPicInfoExEnable', C_BOOL),  # stuBigPicInfoEx是否有效;Whether stuBigPicInfoEx is valid;
        ('nBigPicNumEx', c_int),  # 大图张数;Number of big picture;
        ('stuBigPicInfoEx', NET_DETECT_BIG_PIC_INFO_EX * 50),  # 大图信息(扩展);Big picture information (Extended);
        ('nToken', C_UINT),  # 查询令牌,没有则为0;Token(If no, it is 0);
    ]

class NET_OUT_FACE_RECOGNITION_DETECT_MULTI_FACE_INFO(Structure):
    """
    CLIENT_FaceRecognitionDetectMultiFace 接口输出参数
    the output parameter of interface CLIENT_FaceRecognitionDetectMultiFace
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体的大小;the size of this struct;
    ]

class NET_TRAFFIC_CAR_ATTRIBUTE_INFO(Structure):
    """
    车辆以图搜图时可选择的属性过滤条件
    The attribute filter conditions that can be selected when searching for pictures by vehicle
    """
    _fields_ = [
        ('nVehicleColorArrayNums', c_int),  # 车身颜色的个数,最大值是32;The number of body colors, the maximum value is 32;
        ('emVehicleColorArray', C_ENUM * 32),  # 车身颜色 Refer: EM_OBJECT_COLOR_TYPE;body color Refer: EM_OBJECT_COLOR_TYPE;
        ('nCategoryArrayNums', c_int),  # 车辆类型的个数,最大值是32;The number of vehicle types, the maximum value is 32;
        ('emCategoryArray', C_ENUM * 32),  # 车辆类型 Refer: EM_NET_VEHICLE_TYPE;vehicle type Refer: EM_NET_VEHICLE_TYPE;
        ('szVehicleSign', c_char * 64),  # 车标;vehicle sign;
        ('nSubBrand', C_UINT),  # 车辆子品牌 需要通过映射表得到真正的子品牌 映射表详见开发手册;Vehicle sub-brand The real sub-brand needs to be obtained through the mapping table. Please refer to the development manual for the mapping table;
        ('nBrandYear', C_UINT),  # 车辆年款 需要通过映射表得到真正的年款 映射表详见开发手册;Vehicle year model The real model year needs to be obtained through the mapping table. Please refer to the development manual for the mapping table;
        ('nFurniture', c_int),  # 是否有摆件, 0: 不限 1: 无 2: 有;Whether there are ornaments, 0: no limit 1: no 2: yes;
        ('nPendant', c_int),  # 是否有挂件, 0: 不限 1: 无 2: 有;Whether there is a pendant, 0: no limit 1: no 2: yes;
        ('nAnnualInspection', c_int),  # 是否有年检标, 0: 不限 1: 无 2: 有;Whether there is an annual inspection mark, 0: no limit 1: no 2: yes;
        ('nSunShade', c_int),  # 是否有遮阳板, 0: 不限 1: 无 2: 有;whether there is a sunshade, 0: no limit 1: no 2: yes;
        ('byReserved', c_char * 256),  # 保留字节;reserved bytes;
    ]

class NET_FACERECOGNITION_PERSON_INFOEX2(Structure):
    """
    目标信息，包括以图搜图的图片数据和属性等
    Target information, including image data and attributes for image search
    """
    _fields_ = [
        ('bPersonExEnable', C_BOOL),  # 人员信息查询条件字段stPersonInfoEx是否有效, 并使用人员信息扩展结构体;Whether the personnel information query condition field stPersonInfoEx is valid, and expand the structure with personnel information;
        ('stPersonInfoEx', FACERECOGNITION_PERSON_INFOEX),  # 人员信息扩展;Person information extension;
        ('nFacePicNumEx', c_int),  # 目标图片数据信息的个数, 最大值为48;The number of target picture data information, the maximum value is 48;
        ('stuFacePicInfoEx', NET_FACE_PIC_INFO * 48),  # 目标图片数据信息;target picture data information;
        ('nBoundingBoxNum', c_int),  # 目标区域信息的个数, 最大值为48;The number of target area information, the maximum value is 48;
        ('stuBoundingBox', NET_RECT * 48),  # 目标区域信息, 若字段不存在或均为0则表示为全图区域, 若有该字段则与stuFacePicInfoEx[48]通过数组下标匹配;Target area information, if the field does not exist or both are 0, it means the full image area, if there is this field, it is matched with stuFacePicInfoEx[48] through the array subscript;
        ('nTrafficCarAttributeNum', c_int),  # 车辆以图搜图时可选择的属性过滤条件的个数, 最大值为48;The number of attribute filter conditions that can be selected when searching for a vehicle by image, the maximum value is 48;
        ('stuTrafficCarAttribute', NET_TRAFFIC_CAR_ATTRIBUTE_INFO * 48),  # 车辆以图搜图时可选择的属性过滤条件, 若有该字段则与stuFacePicInfoEx[48]通过数组下标匹配;The attribute filter condition that can be selected when the vehicle searches for images by image, if there is this field, it will be matched with stuFacePicInfoEx[48] through the array subscript;
        ('szReserved', c_char * 1024),  # 保留字节;reserved bytes;
    ]

class NET_IN_STARTMULTIFIND_FACERECONGNITION_EX(Structure):
    """
    CLIENT_StartMultiFindFaceRecognitionEx 接口输入参数
    CLIENT_StartMultiFindFaceRecognitionEx interface input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('pChannelID', POINTER(c_int)),  # 通道号;channel number;
        ('nChannelCount', c_int),  # 通道申请个数;number of channel applications;
        ('emObjectType', C_ENUM),  # 搜索的目标类型 Refer: EM_OBJECT_TYPE;searched object type Refer: EM_OBJECT_TYPE;
        ('stMatchOptions', NET_FACE_MATCH_OPTIONS),  # 人脸匹配选项;face matching options;
        ('stFilterInfo', NET_FACE_FILTER_CONDTION),  # 查询过滤条件;query filter conditions;
        ('pBuffer', POINTER(c_char)),  # 缓冲地址;buffer address;
        ('nBufferLen', c_int),  # 缓冲数据长度;buffer data length;
        ('bPersonEx2Enable', C_BOOL),  # 目标信息是否有效, 并使用目标信息结构体;Whether the target information is valid, and use the target information structure;
        ('stPersonInfoEx2', NET_FACERECOGNITION_PERSON_INFOEX2),  # 目标信息, 包括以图搜图的图片数据和属性等;Target information, including image data and attributes for image search;
    ]

class NET_COUNT_DETAIL_INFO(Structure):
    """
    结果详细信息
    result details
    """
    _fields_ = [
        ('nPictureID', C_UINT),  # 图片的编号(0开始);The number of the picture (0 starts);
        ('nCount', C_UINT),  # 该图片的结果数量;the number of results for this image;
        ('szReserved', c_char * 256),  # 保留字节;reserved bytes;
    ]

class NET_OUT_STARTMULTIFIND_FACERECONGNITION_EX(Structure):
    """
    CLIENT_StartMultiFindFaceRecognitionEx 接口输出参数
    CLIENT_StartMultiFindFaceRecognitionEx interface output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nTotalCount', c_int),  # 返回的符合查询条件的记录个数-1表示总条数未生成,要推迟获取使用CLIENT_AttachFaceFindState接口状态;The number of returned records that meet the query conditions-1 means that the total number of records has not been generated, and the acquisition should be postponedUse CLIENT_AttachFaceFindState interface state;
        ('lFindHandle', C_LLONG),  # 查询句柄;query handle;
        ('nToken', c_int),  # 获取到的查询令牌;obtained query token;
        ('nCountDetailNum', c_int),  # 结果详细信息的个数, 最大值为64;the number of result details, the maximum value is 64;
        ('stuCountDetail', NET_COUNT_DETAIL_INFO * 64),  # 结果详细信息;result details;
    ]

class NET_IN_DOFIND_FACERECONGNITION_EX(Structure):
    """
    CLIENT_DoFindFaceRecognitionEx 接口输入参数
    CLIENT_DoFindFaceRecognitionEx interface input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('lFindHandle', C_LLONG),  # 查询句柄;query handle;
        ('nBeginNum', c_int),  # 查询起始序号;Query the starting serial number;
        ('nCount', c_int),  # 当前想查询的记录条数;the current number of records to query;
        ('emDataType', C_ENUM),  # 指定查询结果返回图片的格式 Refer: EM_NEEDED_PIC_RETURN_TYPE;Specify the format of the picture returned by the query result Refer: EM_NEEDED_PIC_RETURN_TYPE;
        ('bPictureIDEnable', C_BOOL),  # 图片的编号是否有效TRUE : nPictureID字段有效且下发该字段, 表示只查单张图片的结果FALSE : nPictureID字段无效且不下发该字段, 表示查所有图片的结果;Whether the picture number is validTRUE : The nPictureID field is valid and this field is sent, indicating that only the result of checking a single pictureFALSE : The nPictureID field is invalid and this field is not issued, indicating the result of checking all pictures;
        ('nPictureID', C_UINT),  # 图片的编号(0开始);The number of the picture (0 starts);
    ]

class NET_HISTORY_NON_MOTOR_INFO(Structure):
    """
    非机动车信息
    Non-motor vehicle information
    """
    _fields_ = [
        ('szUID', c_char * 64),  # 非机动车唯一标识符;non-motor vehicle unique identifier;
        ('stuBoundingBox', NET_RECT),  # 包围盒(8192坐标系);Bounding box (8192 coordinate system);
        ('nHelmet', C_UINT),  # 车上人员头盔状态 0-未知 1-没有 2-有;Helmet status of the person on board 0-unknown 1-no 2-yes;
        ('szCapColor', c_char * 16),  # 帽子颜色;cap color;
        ('szCategory', c_char * 32),  # 非机动车子类型;non-motor vehicle subtype;
        ('szColor', c_char * 16),  # 非机动车颜色;non-motor vehicle color;
        ('nBasket', C_UINT),  # 非机动车车篮 0-未知 1-否 2-有;non-motor vehicle basket 0-unknown 1-no 2-yes;
        ('nStoragebox', C_UINT),  # 非机动车后备箱 0: 未知 1: 无后备箱 2: 非机动车自带箱 3: 非机动车自装箱 4: 非机动车自带自装箱都有;Non-motor vehicle trunk 0: Unknown 1: No trunk 2: Non-motor vehicle self-packing box 3: Non-motor vehicle self-packing box 4: Non-motor vehicle self-packing box;
        ('nNumOfCycling', C_UINT),  # 骑车人数, 0xff表示未知;number of cyclists, 0xff means unknown;
        ('stuImage', NET_PIC_INFO_EX),  # 非机动车图片信息;Non-motor vehicle picture information;
        ('szReserved', c_char * 256),  # 保留字节;reserved bytes;
    ]

class NET_CANDIDATE_INFOEX2(Structure):
    """
    候选人员信息列表
    candidate information list
    """
    _fields_ = [
        ('stuCandidatesEx', CANDIDATE_INFOEX),  # 当前人脸匹配到的候选对象信息扩展;Expansion of candidate object information matched by the current face;
        ('nSimilarity2', C_UINT),  # 以图搜图业务,输入图片的相似度,万分比 1~10000;Search image business by image, input the similarity of the image, 1~10000;
        ('nTaskID', c_int),  # 任务流ID, 任务流以图搜图时, 表示候选人来自哪个分析任务;task flow ID, when the task flow is searched by graph, it indicates which analysis task the candidate comes from;
        ('stuHistoryNonMotorInfo', NET_HISTORY_NON_MOTOR_INFO),  # 非机动车信息, 非机动车以图搜图时返回的非机动车属性;Non-motorized vehicle information, the non-motorized vehicle attribute returned when the non-motorized vehicle is searched by image;
        ('stuHistoryTrafficCarInfo', NET_HISTORY_TRAFFIC_CAR_INFO),  # 机动车信息, 机动车以图搜图时返回的机动车属性;Motor vehicle information, the motor vehicle attribute returned when the motor vehicle is searched by image;
        ('szReserved', c_char * 256),  # 保留字节;reserved bytes;
    ]

class NET_OUT_DOFIND_FACERECONGNITION_EX(Structure):
    """
    CLIENT_DoFindFaceRecognitionEx接口输出参数
    CLIENT_DoFindFaceRecognitionEx interface output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('pBuffer', POINTER(c_char)),  # 缓冲地址;buffer address;
        ('nBufferLen', c_int),  # 缓冲数据长度;buffer data length;
        ('nRetCadidateEx2Num', c_int),  # 设备实际返回的候选信息结构体个数, 最大值是50, nRetCadidateEx2Num必须要小于等于nCadidateEx2Num;The number of candidate information structures actually returned by the device, the maximum value is 50, nRetCadidateEx2Num must be less than or equal to nCadidateEx2Num;
        ('nCadidateEx2Num', c_int),  # 需要用户输入的候选信息结构体个数, 最大值是50;The number of candidate information structures that require user input, the maximum value is 50;
        ('pstuCandidatesEx2', POINTER(NET_CANDIDATE_INFOEX2)),  # 候选人员信息列表, 需要用户进行申请和释放，申请内存大小为: sizeof(NET_CANDIDATE_INFOEX2) * nCadidateEx2Num;Candidate information list, which needs to be applied and released by the user, the application memory size is: sizeof(NET_CANDIDATE_INFOEX2) * nCadidateEx2Num;
    ]

class NET_IN_FACERSERVER_GETDETEVTTOKEN(Structure):
    """
    CLIENT_FaceRServerGetDetectToken 接口输入参数
    CLIENT_FaceRServerGetDetectToken input parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
    ]

class NET_OUT_FACERSERVER_GETDETEVTTOKEN(Structure):
    """
    CLIENT_FaceRServerGetDetectToken 接口输出参数
    CLIENT_FaceRServerGetDetectToken output parameters
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Structure size;
        ('nToken', C_UINT),  # 获取到的查询令牌;token;
    ]

class NET_A_CFG_THERMOMETRY_INFO(Structure):
    """
    热成像测温全局配置
    thermal imaging Temperature Monitoring global config
    """
    _fields_ = [
        ('nRelativeHumidity', c_int),  # 相对湿度;relative humidity;
        ('fAtmosphericTemperature', c_float),  # 大气温度;atmospheric temperature;
        ('fObjectEmissivity', c_float),  # 物体辐射系数;object radiation coefficient;
        ('nObjectDistance', c_int),  # 物体距离;object distance;
        ('fReflectedTemperature', c_float),  # 物体反射温度;object reflection temperature;
        ('nTemperatureUnit', c_int),  # 温度单位，见 TEMPERATURE_UNIT;temperature unit, see TEMPERATURE_UNIT;
        ('bIsothermEnable', C_BOOL),  # 色标功能使能;color batch enable;
        ('nMinLimitTemp', c_int),  # 等温线下限温度值;isotherm minimum temperature value;
        ('nMediumTemp', c_int),  # 等温线中位温度值;isotherm median temperature value;
        ('nMaxLimitTemp', c_int),  # 等温线上限温度值;isotherm upper limit temperature;
        ('nSaturationTemp', c_int),  # 等温线饱和温度值;isotherm Saturated temperature;
        ('stIsothermRect', CFG_RECT),  # 色温条矩形区域（OSD 位置），使用相对坐标体系，取值均为0-8191;Color temperature rectangular area (OSD position), use the relative coordinates system, the value are 0-8191;
        ('bColorBarDisplay', C_BOOL),  # 是否显示色标条（OSD 叠加）;whether to display the color batch (OSD overlay);
        ('bHotSpotFollow', C_BOOL),  # 是否开启热点探测追踪使能;whether enable hotspot detector tracking or not;
        ('bTemperEnable', C_BOOL),  # 测温开关;color temperature switch;
        ('stHighCTMakerColor', CFG_RGBA),  # 高色温标注颜色;high color temperature color;
        ('stLowCTMakerColor', CFG_RGBA),  # 低色温标注颜色;low temperature mark color;
    ]

class NET_CFG_ACCESS_FUNCTION_INFO(Structure):
    """
    接入功能配置(对应枚举 NET_EM_CFG_ACCESS_FUNCTION)
    Access function config(corresponding to NET_EM_CFG_ACCESS_FUNCTION)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('bGb28181ClientEnable', C_BOOL),  # 是否允许接入国标前端设备;access to Gb28181 Client Enable;
        ('bGb28181ServerEnable', C_BOOL),  # 是否能接入国标平台;access to Gb28181 Server Enable;
        ('bONVIFClientEnable', C_BOOL),  # 是否允许接入ONVIF前端;access to ONVIF Client Enable;
        ('bONVIFServerEnable', C_BOOL),  # 是否支持onvifserver;access to ONVIF Server Enable;
        ('bRTSPEnable', C_BOOL),  # 是否支持rtsp被拉流;support RTSP Enable;
    ]

class NET_CFG_DISABLE_LINKAGE(Structure):
    """
    一键撤防配置(对应枚举 CFG_DISABLE_LINKAGE)
    Disable linkage configuration(corresponding to CFG_DISABLE_LINKAGE)
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('bEnable', C_BOOL),  # 撤防联动项功能总开关;unable linkage switch
    ]

class NET_ENCODE_SNAP_INFO(Structure):
    """
    抓图配置
    the snap info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('emSnapType', C_ENUM),  # 抓图类型 Refer: EM_A_NET_EM_SNAP_TYPE;snap type Refer: EM_A_NET_EM_SNAP_TYPE;
        ('bSnapEnable', C_BOOL),  # 定时抓图使能;enable;
        ('emCompression', C_ENUM),  # 视频压缩格式 Refer: EM_A_NET_EM_VIDEO_COMPRESSION;the video compression Refer: EM_A_NET_EM_VIDEO_COMPRESSION;
        ('nWidth', c_int),  # 视频宽度;the width of image;
        ('nHeight', c_int),  # 视频高度;the height of image;
        ('nFrameRate', c_float),  # 视频帧率;frame rate;
        ('nQualityRange', c_int),  # 图像质量取值范围;the range of image quality;
        ('emImageQuality', C_ENUM),  # 图像质量 Refer: EM_CFG_IMAGE_QUALITY;image quality Refer: EM_CFG_IMAGE_QUALITY;
    ]

class NET_ENCODE_SNAP_TIME_INFO(Structure):
    """
    抓图时间配置
    snap time info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('shPicTimeInterval', c_short),  # 定时抓图时间间隔,单位为秒,目前设备支持最大的抓图时间间隔为30分钟;the time interval of snap, unit:second;
        ('bPicIntervalHour', C_BYTE),  # 定时抓图时间间隔小时数;the time interval of snap, unit:hour;
        ('dwTrigPicIntervalSecond', C_DWORD),  # 报警触发后每次抓图时间间隔时间 单位秒;the time interval of snap after alarm, unit:second;
    ]

class NET_ENCODE_VIDEO_INFO(Structure):
    """
    主(辅)码流视频格式(f6/f5/bin)
    the video info of main(extra) stream
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('emFormatType', C_ENUM),  # 码流类型,设置和获取时都需要设置值 Refer: EM_A_NET_EM_FORMAT_TYPE;stream type, you need to set this value when get or set config Refer: EM_A_NET_EM_FORMAT_TYPE;
        ('bVideoEnable', C_BOOL),  # 视频使能;enable;
        ('emCompression', C_ENUM),  # 视频压缩格式 Refer: CFG_VIDEO_COMPRESSION;the type of video compression Refer: CFG_VIDEO_COMPRESSION;
        ('nWidth', c_int),  # 视频宽度;the wigth of video;
        ('nHeight', c_int),  # 视频高度;the height of video;
        ('emBitRateControl', C_ENUM),  # 码流控制模式 Refer: EM_A_NET_EM_BITRATE_CONTROL;the type of BitRateControl Refer: EM_A_NET_EM_BITRATE_CONTROL;
        ('nBitRate', c_int),  # 视频码流(kbps);Video bit rate (kbps);
        ('nFrameRate', c_float),  # 视频帧率;Frame Rate;
        ('nIFrameInterval', c_int),  # I帧间隔(1-100)，比如50表示每49个B帧或P帧，设置一个I帧。;I frame interval(1-100). For example, 50 means there is I frame in each 49 B frame or P frame.;
        ('emImageQuality', C_ENUM),  # 图像质量 Refer: EM_A_NET_EM_IMAGE_QUALITY;image quality Refer: EM_A_NET_EM_IMAGE_QUALITY;
    ]

class NET_A_CFG_PTZ_LINK(Structure):
    """
    联动云台信息
    PTZ activation information
    """
    _fields_ = [
        ('emType', C_ENUM),  # 联动类型 Refer: EM_A_CFG_LINK_TYPE;Activation type Refer: EM_A_CFG_LINK_TYPE;
        ('nValue', c_int),  # 联动取值分别对应预置点号，巡航号等等;The activation value is the corresponding preset number, tour number and etc.;
    ]

class NET_A_CFG_PTZ_LINK_EX(Structure):
    """
    联动云台信息扩展
    PTZ activation extend information
    """
    _fields_ = [
        ('emType', C_ENUM),  # 联动类型 Refer: EM_A_CFG_LINK_TYPE;Activation type Refer: EM_A_CFG_LINK_TYPE;
        ('nParam1', c_int),  # 联动参数1;Activation parameter1;
        ('nParam2', c_int),  # 联动参数2;Activation parameter2;
        ('nParam3', c_int),  # 联动参数3;Activation parameter3;
        ('nChannelID', c_int),  # 所联动云台通道;Activation channel;
    ]

class NET_A_CFG_EVENT_TITLE(Structure):
    """
    事件标题内容结构体
    Event title
    """
    _fields_ = [
        ('szText', c_char * 64),
        ('stuPoint', CFG_POLYGON),  # 标题左上角坐标, 采用0-8191相对坐标系;Title on the upper left corner coordinates, using the 0-8191 to sitting;
        ('stuSize', NET_CFG_SIZE),  # 标题的宽度和高度,采用0-8191相对坐标系，某项或者两项为0表示按照字体自适应宽高;The height and width of title, using 0-8191 relative coordinnate system, the item or two adaptive width 0 said according to the font;
        ('stuFrontColor', CFG_RGBA),  # 前景颜色;Front color;
        ('stuBackColor', CFG_RGBA),  # 背景颜色;Back color;
    ]

class NET_A_CFG_MAIL_DETAIL(Structure):
    """
    邮件详细内容
    Mail detail
    """
    _fields_ = [
        ('emAttachType', C_ENUM),  # 附件类型 Refer: EM_A_CFG_ATTACHMENT_TYPE;Attachment type Refer: EM_A_CFG_ATTACHMENT_TYPE;
        ('nMaxSize', c_int),  # 文件大小上限，单位kB;The max size for file, unit kB;
        ('nMaxTimeLength', c_int),  # 最大录像时间长度，单位秒，对video有效;Max time length, unit sec, effective for video;
    ]

class NET_A_CFG_TOURLINK(Structure):
    """
    轮巡联动配置
    Tour link configuration
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 轮巡使能;Tour enable;
        ('emSplitMode', C_ENUM),  # 轮巡时的分割模式 Refer: EM_A_CFG_SPLITMODE;Touring, split mode Refer: EM_A_CFG_SPLITMODE;
        ('nChannels', c_int * 256),  # 轮巡通道号列表;Touring,video channel;
        ('nChannelCount', c_int),  # 轮巡通道数量;Touring,channel count;
    ]

class NET_A_CFG_TALKBACK_INFO(Structure):
    """
    语音呼叫联动信息
    Voice Call Linkage Information
    """
    _fields_ = [
        ('bCallEnable', C_BOOL),  # 语音呼叫使能;Voice Call Enable;
        ('emCallerType', C_ENUM),  # 语音呼叫发起方 Refer: EM_CALLER_TYPE;Voice Calls Originating Refer: EM_CALLER_TYPE;
        ('emCallerProtocol', C_ENUM),  # 语音呼叫协议 Refer: EM_CALLER_PROTOCOL_TYPE;Voice Call Protocol Refer: EM_CALLER_PROTOCOL_TYPE;
    ]

class NET_A_CFG_PSTN_ALARM_SERVER(Structure):
    """
    电话报警中心联动信息
    Telephone Alarm Center Linkage Information
    """
    _fields_ = [
        ('bNeedReport', C_BOOL),  # 是否上报至电话报警中心;Whether to Report to the Call Center;
        ('nServerCount', c_int),  # 电话报警服务器个数;The Number of Telephone Alarm Server;
        ('byDestination', C_BYTE * 8),  # 上报的报警中心下标,详见配置CFG_PSTN_ALARM_CENTER_INFO;Report to the Alarm Center Subscript,See the Configuration CFG_PSTN_ALARM_CENTER_INFO;
    ]

class NET_A_CFG_TIME_SECTION(Structure):
    """
    时间段信息
    Period information
    """
    _fields_ = [
        ('dwRecordMask', C_DWORD),  # 录像掩码，按位分别为Bit0-动态检测录像、Bit1-报警录像、Bit2-定时录像、Bit3-动检和报警同时触发时才录像、Bit4-卡号录像、Bit5-智能录像、Bit6-POS录像、Bit7~Bit15保留;Record subnet mask. Bit0-motion detection recording, Bit1-alarm recording, Bit2-timing recording, Bit3-motion detection and alarm triggered simultaneously, Bit4-card number recording, Bit5-smart recording, Bit6-POS recording, Bit7~Bit15 reserved;
        ('nBeginHour', c_int),
        ('nBeginMin', c_int),
        ('nBeginSec', c_int),
        ('nEndHour', c_int),
        ('nEndMin', c_int),
        ('nEndSec', c_int),
    ]

class NET_A_CFG_TIME_SCHEDULE(Structure):
    """
    时间表信息
    Schedule Information
    """
    _fields_ = [
        ('bEnableHoliday', C_BOOL),  # 是否支持节假日配置，默认为不支持，除非获取配置后返回为TRUE，不要使能假日配置;whether holiday config is enabled, default value is FALSE, DO NOT enable it unless you get TRUE after get config;
        ('stuTimeSection', NET_A_CFG_TIME_SECTION * 8 * 6),  # 第一维前7个元素对应每周7天，第8个元素对应节假日，每天最多6个时间段;The First Dimension Before the 7 Elements Corresponding 7 Days a week, Eighth Elements Corresponding Holiday, Up to Six Time Periods Per Day;
    ]

class NET_PTZ_LINK(Structure):
    """
    云台联动项
    pos ptz link
    """
    _fields_ = [
        ('emType', C_ENUM),  # 云台联动类型 Refer: EM_PTZ_LINK_TYPE;ptz link type Refer: EM_PTZ_LINK_TYPE;
        ('nParam1', c_int),  # 联动参数1;link param 1;
        ('nParam2', c_int),  # 联动参数2;link param 2;
        ('nParam3', c_int),  # 联动参数3;link param 3;
        ('nChannelID', c_int),  # 所联动云台通道;ptz link channelID;
    ]

class NET_CFG_LIGHTING_LINK_INFO(Structure):
    """
    云台补光灯联动项
    PTZ supplementary light linkage item
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 使能;Enzble;
        ('emFilckerLightType', C_ENUM),  # 闪烁灯光类型 Refer: EM_A_NET_EM_FILCKERLIGHT_TYPE;Flashing light type Refer: EM_A_NET_EM_FILCKERLIGHT_TYPE;
        ('emLightlinkType', C_ENUM),  # 灯光联动方式 Refer: EM_A_NET_EM_LIGHTLINK_TYPE;Lighting linkage mode Refer: EM_A_NET_EM_LIGHTLINK_TYPE;
        ('fFilckerIntevalTime', c_float),  # 闪烁间隔时间;Filcker inteval time;
        ('nFilckerTimes', c_int),  # 闪烁可配置的次数;Filcker times;
        ('nLightDuration', C_UINT),  # 灯光闪烁或常亮持续时间,单位秒;light duration;
        ('nLightBright', C_UINT),  # 联动灯光的亮度;Brightness of linkage light;
        ('stuWhiteLightTimeSection', NET_A_CFG_TIME_SECTION * 7 * 6),  # 白光灯联动时间段;White light time section;
    ]

class NET_A_CFG_ALARM_MSG_HANDLE(Structure):
    """
    报警联动信息
    Alarm activation information
    """
    _fields_ = [
        ('abRecordMask', c_bool),
        ('abRecordEnable', c_bool),
        ('abRecordLatch', c_bool),
        ('abAlarmOutMask', c_bool),
        ('abAlarmOutEn', c_bool),
        ('abAlarmOutLatch', c_bool),
        ('abExAlarmOutMask', c_bool),
        ('abExAlarmOutEn', c_bool),
        ('abPtzLinkEn', c_bool),
        ('abTourMask', c_bool),
        ('abTourEnable', c_bool),
        ('abSnapshot', c_bool),
        ('abSnapshotEn', c_bool),
        ('abSnapshotPeriod', c_bool),
        ('abSnapshotTimes', c_bool),
        ('abTipEnable', c_bool),
        ('abMailEnable', c_bool),
        ('abMessageEnable', c_bool),
        ('abBeepEnable', c_bool),
        ('abVoiceEnable', c_bool),
        ('abMatrixMask', c_bool),
        ('abMatrixEnable', c_bool),
        ('abEventLatch', c_bool),
        ('abLogEnable', c_bool),
        ('abDelay', c_bool),
        ('abVideoMessageEn', c_bool),
        ('abMMSEnable', c_bool),
        ('abMessageToNetEn', c_bool),
        ('abTourSplit', c_bool),
        ('abSnapshotTitleEn', c_bool),
        ('abChannelCount', c_bool),
        ('abAlarmOutCount', c_bool),
        ('abPtzLinkEx', c_bool),
        ('abSnapshotTitle', c_bool),
        ('abMailDetail', c_bool),
        ('abVideoTitleEn', c_bool),
        ('abVideoTitle', c_bool),
        ('abTour', c_bool),
        ('abDBKeys', c_bool),
        ('abJpegSummary', c_bool),
        ('abFlashEn', c_bool),
        ('abFlashLatch', c_bool),
        ('byReserved1', C_BYTE * 2),  # 补齐信息;For alignInformation;
        ('nChannelCount', c_int),  # 设备的视频通道数;The video channel of the device;
        ('nAlarmOutCount', c_int),  # 设备的报警输出个数;The alarm output amount of the device;
        ('dwRecordMask', C_DWORD * 16),  # 录像通道掩码(按位);Subnet mask of the recording channel(use the bit to represent);
        ('bRecordEnable', C_BOOL),  # 录像使能;Record enable;
        ('nRecordLatch', c_int),  # 录像延时时间(秒);Record delay time(s);
        ('dwAlarmOutMask', C_DWORD * 16),  # 报警输出通道掩码;Subnet mask of alarm output channel;
        ('bAlarmOutEn', C_BOOL),  # 报警输出使能;Alarm output enable;
        ('nAlarmOutLatch', c_int),  # 报警输出延时时间(秒);Alarm output delay time (s);
        ('dwExAlarmOutMask', C_DWORD * 16),  # 扩展报警输出通道掩码;Subnet mask of extension alarm output channel;
        ('bExAlarmOutEn', C_BOOL),  # 扩展报警输出使能;Extension alarm output enable;
        ('stuPtzLink', NET_A_CFG_PTZ_LINK * 256),  # 云台联动项;PTZ activation item;
        ('bPtzLinkEn', C_BOOL),  # 云台联动使能;PTZ activation enable;
        ('dwTourMask', C_DWORD * 16),  # 轮询通道掩码;Subnet mask of tour channel;
        ('bTourEnable', C_BOOL),  # 轮询使能;Tour enable;
        ('dwSnapshot', C_DWORD * 16),  # 快照通道号掩码;Snapshot channel subnet mask;
        ('bSnapshotEn', C_BOOL),  # 快照使能;Snapshot enable;
        ('nSnapshotPeriod', c_int),  # 连拍周期(秒);Snapshot period(s);
        ('nSnapshotTimes', c_int),  # 连拍次数;Snapshot times;
        ('bTipEnable', C_BOOL),  # 本地消息框提示;Local prompt dialogue box;
        ('bMailEnable', C_BOOL),  # 发送邮件，如果有图片，作为附件;Send out emali. The image is sent out as the attachment.;
        ('bMessageEnable', C_BOOL),  # 上传到报警服务器;Upload to the alarm server;
        ('bBeepEnable', C_BOOL),  # 蜂鸣;Buzzer;
        ('bVoiceEnable', C_BOOL),  # 语音提示;Audio prompt;
        ('dwMatrixMask', C_DWORD * 16),  # 联动视频矩阵通道掩码;Subnet mask of the activated video channel;
        ('bMatrixEnable', C_BOOL),  # 联动视频矩阵;Activate the video matrix;
        ('nEventLatch', c_int),  # 联动开始延时时间(秒)，0－15;Activation delay time (s),0-15;
        ('bLogEnable', C_BOOL),  # 是否记录日志;Record log or not;
        ('nDelay', c_int),  # 设置时先延时再生效，单位为秒;Delay first and then becomes valid when set. Unit is second.;
        ('bVideoMessageEn', C_BOOL),  # 叠加提示字幕到视频。叠加的字幕包括事件类型，通道号，秒计时。;Overlay the prompt character to the video. The overlay character includes the event type, channel number. The unit is second.;
        ('bMMSEnable', C_BOOL),  # 发送彩信使能;Enable MMS;
        ('bMessageToNetEn', C_BOOL),  # 消息上传给网络使能;Send the message to the network enable;
        ('nTourSplit', c_int),  # 轮巡时的分割模式 0: 1画面; 1: 8画面;Tour split mod 0: 1tour; 1: 8tour;
        ('bSnapshotTitleEn', C_BOOL),  # 是否叠加图片标题;Enble osd;
        ('nPtzLinkExNum', c_int),  # 云台配置数;PTZ link configuration number;
        ('stuPtzLinkEx', NET_A_CFG_PTZ_LINK_EX * 256),  # 扩展云台信息;PTZ extend information;
        ('nSnapTitleNum', c_int),  # 图片标题内容数;Number of picture title;
        ('stuSnapshotTitle', NET_A_CFG_EVENT_TITLE * 256),  # 图片标题内容;Picture title content;
        ('stuMailDetail', NET_A_CFG_MAIL_DETAIL),  # 邮件详细内容;Mail detial;
        ('bVideoTitleEn', C_BOOL),  # 是否叠加视频标题，主要指主码流;Whether overlay video title, mainly refers to the main stream;
        ('nVideoTitleNum', c_int),  # 视频标题内容数目;Video title num;
        ('stuVideoTitle', NET_A_CFG_EVENT_TITLE * 256),  # 视频标题内容;Video title;
        ('nTourNum', c_int),  # 轮询联动数目;Tour num;
        ('stuTour', NET_A_CFG_TOURLINK * 256),  # 轮询联动配置;Tour configuration;
        ('nDBKeysNum', c_int),  # 指定数据库关键字的有效数;Specify the db keyword on the number of effective;
        ('szDBKeys', c_char * 64 * 64),  # 指定事件详细信息里需要写到数据库的关键字;The specify event detail information need write the BD keyword;
        ('byJpegSummary', C_BYTE * 1024),  # 叠加到JPEG图片的摘要信息;The summary information of the jpeg image;
        ('bFlashEnable', C_BOOL),  # 是否使能补光灯;Whether enable flash;
        ('nFlashLatch', c_int),  # 补光灯延时时间(秒),延时时间范围：[10,300];Flash delay time (s),the time range:[10,300];
        ('abAudioFileName', c_bool),
        ('abAlarmBellEn', c_bool),
        ('abAccessControlEn', c_bool),
        ('abAccessControl', c_bool),
        ('szAudioFileName', c_char * 260),  # 联动语音文件绝对路径;The Absolute Path to the Linkage Audio Files;
        ('bAlarmBellEn', C_BOOL),  # 警号使能;Warning Signal Enable;
        ('bAccessControlEn', C_BOOL),  # 门禁使能;Entrance Guard Enable;
        ('dwAccessControl', C_DWORD),  # 门禁组数;Class Number of Entrance Guard;
        ('emAccessControlType', C_ENUM * 8),  # 门禁联动操作信息 Refer: EM_CFG_ACCESSCONTROLTYPE;Entrance Guard Linkage Operation Information Refer: EM_CFG_ACCESSCONTROLTYPE;
        ('abTalkBack', c_bool),
        ('byReserved2', C_BYTE * 3),  # 补齐;For align;
        ('stuTalkback', NET_A_CFG_TALKBACK_INFO),  # 语音呼叫联动信息;Voice Call Linkage Information;
        ('abPSTNAlarmServer', c_bool),
        ('byReserved3', C_BYTE * 3),  # 补齐;For align;
        ('stuPSTNAlarmServer', NET_A_CFG_PSTN_ALARM_SERVER),  # 电话报警中心联动信息;Telephone Alarm Center Linkage Information;
        ('stuTimeSection', NET_A_CFG_TIME_SCHEDULE),  # 事件响应时间表;Event Response Timetable;
        ('abAlarmBellLatch', c_bool),
        ('byReserved4', C_BYTE * 3),  # 补齐;For align;
        ('nAlarmBellLatch', c_int),  # 警号输出延时时间(10-300秒);Police no. output delay time(10-300 s);
        ('abAudioPlayTimes', c_bool),
        ('abAudioLinkTime', c_bool),
        ('byReserved5', C_BYTE * 2),  # 补齐;For align;
        ('nAudioPlayTimes', C_UINT),  # 联动语音播放次数;times of linkage voice play;
        ('nAudioLinkTime', C_UINT),  # 联动语音播放的时间, 单位：秒;time of linkage voice play, uint:s;
        ('abAlarmOutTime', c_bool),  # nAlarmOutTime 是否有效;is nAlarmOutTime valid;
        ('nAlarmOutTime', c_int),  # 报警输出持续时间,单位秒, 如果无此字段，按设备原来的方式实现;alarm timeout,unit:second;
        ('abBeepTime', c_bool),  # nBeepTime 是否有效;is nBeepTime valid;
        ('nBeepTime', c_int),  # 蜂鸣时长，单位秒，最大值为3600，0代表持续蜂鸣;beep time,unit:second,max value is 3600,0 means beep continuely;
    ]

class NET_ALARM_MSG_HANDLE(Structure):
    """
    报警联动信息
    Alarm activation information
    """
    _fields_ = [
        ('abChannelCount', c_bool),  # 是否支持通道数量;Whether Support Channel Count;
        ('abAlarmOutCount', c_bool),  # 是否支持报警输出数量;Whether Support AlarmOut Count;
        ('abRecordMask', c_bool),  # 是否支持录像通道;Whether Support RecordMask;
        ('abRecordEnable', c_bool),  # 是否支持录像使能;Whether Support RecordEnable;
        ('abRecordLatch', c_bool),  # 是否支持录像延时;Whether Support RecordLatch;
        ('abAlarmOutMask', c_bool),  # 是否支持报警输出通道;Whether Support AlarmOutMask;
        ('abAlarmOutEn', c_bool),  # 是否支持报警输出使能;Whether Support AlarmOut Enable;
        ('abAlarmOutLatch', c_bool),  # 是否支持报警输出延时;Whether Support AlarmOut Latch;
        ('abExAlarmOutMask', c_bool),  # 是否支持扩展报警输出通道;Whether Support ExAlarmOut Mask;
        ('abExAlarmOutEn', c_bool),  # 是否支持扩展报警输出使能;Whether Support ExAlarmOut Enable;
        ('abPtzLinkEn', c_bool),  # 是否支持云台联动使能;Whether Support PTZ Link Enable;
        ('abTourMask', c_bool),  # 是否支持轮巡掩码;Whether Support Tour Mask;
        ('abTourEnable', c_bool),  # 是否支持轮巡使能;Whether Support Tour Enable;
        ('abSnapshot', c_bool),  # 是否支持快照;Whether Support Snapshot;
        ('abSnapshotEn', c_bool),  # 是否支持快照使能;Whether Support Snapshot Enable;
        ('abSnapshotPeriod', c_bool),# 是否支持帧间隔，每隔多少帧抓一张图片;Whether Support Snapshot Period, Snap a picture every sceond;
        ('abSnapshotTimes', c_bool),  # 是否支持连拍次数;Whether Support Snapshot Times;
        ('abTipEnable', c_bool),  # 是否支持本地消息框提示;Whether Support Local Message Box prompt;
        ('abMailEnable', c_bool),  # 是否支持发送邮件;Whether Support Send Mail Enable;
        ('abMessageEnable', c_bool),  # 是否支持上传到报警中心服务器;Whether Support Upload to the alarm center server;
        ('abBeepEnable', c_bool),  # 是否支持蜂鸣;Whether Support Beep Enable;
        ('abVoiceEnable', c_bool),  # 是否支持语音提示;Whether Support Voice Enable;
        ('abMatrixMask', c_bool),  # 是否支持联动视频矩阵掩码;Whether Support Matrix Mask;
        ('abMatrixEnable', c_bool),  # 是否支持联动视频矩阵使能;Whether Support Matrix Enable;
        ('abEventLatch', c_bool),  # 是否支持联动开始延时时间;Whether Support Event Latch;
        ('abLogEnable', c_bool),  # 是否支持日志使能;Whether Support Log Enable;
        ('abDelay', c_bool),  # 是否支持报警延时;Whether Support Delay;
        ('abVideoMessageEn', c_bool),  # 是否支持叠加提示字幕到视频;Whether Support Add Message to video;
        ('abMMSEnable', c_bool),  # 是否支持发送短消息;Whether Support Send MMS Enable;
        ('abMessageToNetEn', c_bool),  # 是否支持消息上传给网络使能;Whether Support Message to Net Enable;
        ('abTourSplit', c_bool),  # 是否支持换面分割轮巡;Whether Support TourSplit;
        ('abSnapshotTitleEn', c_bool),  # 是否支持叠加图片标题使能;Whether Support Snapshot Title Enable;
        ('abPtzLinkEx', c_bool),  # 是否支持云台联动使能;Whether Support PTZ Link Enable;
        ('abSnapshotTitle', c_bool),  # 是否支持叠加图片标题;Whether Support Add Snapshot Title;
        ('abMailDetail', c_bool),  # 是否支持邮件详情;Whether Support Mail Detail;
        ('abVideoTitleEn', c_bool),  # 是否支持叠加视频标题，主要指主码流;Whether Support Add Video Title Enable, MainStream;
        ('abVideoTitle', c_bool),  # 是否支持视频标题内容;Whether Support Video Title;
        ('abTour', c_bool),  # 是否支持轮巡;Whether Support Tour;
        ('abDBKeys', c_bool),# 是否支持指定事件详细信息里需要写到数据库的关键字;Whether Support Specifies the KeyWords that need to be Written to the DB in the event details;
        ('abJpegSummary', c_bool),  # 是否支持叠加到JPEG图片的摘要信息;Whether Support Add JPEG Summary;
        ('abFlashEn', c_bool),  # 是否支持补光灯使能;Whether Support Flash Enable;
        ('abFlashLatch', c_bool),  # 是否支持补光灯延时;Whether Support Flash Latch;
        ('abAudioFileName', c_bool),  # 是否支持联动语音文件绝对路径;Whether Support Audio File Name;
        ('abAlarmBellEn', c_bool),  # 是否支持警号使能;Whether Support AlarmBell Enable;
        ('abAccessControlEn', c_bool),  # 是否支持门禁控制使能;Whether Support Access Control Enable;
        ('abAccessControl', c_bool),  # 是否支持门禁控制;Whether Support Access Control;
        ('abTalkBack', c_bool),  # 是否支持语音呼叫;Whether Support TalkBack;
        ('abPSTNAlarmServer', c_bool),  # 是否支持电话报警中心;Whether Support PSTN Alarm Server;
        ('abAlarmBellLatch', c_bool),  # 是否支持警号输出延时;Whether Support AlarmBell Latch;
        ('abPlayTimes', c_bool),  # 是否支持联动语音播放次数;Whether Support PlayTimes;
        ('abReboot', c_bool),  # 是否支持重启使能;Whether Support Reboot enable;
        ('abBeepTime', c_bool),  # 是否支持蜂鸣时长;Whether Support BeepTime;
        ('byReserved', C_BYTE * 68),  # 能力保留字段;reserved for ability;
        ('stuTimeSection', NET_A_CFG_TIME_SCHEDULE),  # 事件响应时间表;Alarm Time Section;
        ('nChannelCount', c_int),  # 设备的视频通道数;The video channel of the device;
        ('nAlarmOutCount', c_int),  # 设备的报警输出个数;The alarm output amount of the device;
        ('dwRecordMask', C_DWORD * 16),  # 录像通道掩码(按位);Subnet mask of the recording channel(use the bit to represent);
        ('bRecordEnable', C_BOOL),  # 录像使能;Record enable;
        ('nRecordLatch', c_int),  # 录像延时时间(秒);Record delay time(s);
        ('dwAlarmOutMask', C_DWORD * 16),  # 报警输出通道掩码;ubnet mask of alarm output channel;
        ('bAlarmOutEn', C_BOOL),  # 报警输出使能;Alarm output enable;
        ('nAlarmOutLatch', c_int),  # 报警输出延时时间(秒);Alarm output delay time (s);
        ('dwExAlarmOutMask', C_DWORD * 16),  # 扩展报警输出通道掩码;Subnet mask of extension alarm output channel;
        ('bExAlarmOutEn', C_BOOL),  # 扩展报警输出使能;Extension alarm output enable;
        ('stuPtzLink', NET_A_CFG_PTZ_LINK * 256),  # 云台联动项 这个参数并没有被解析，应该是被扩展替代;PTZ activation item;
        ('bPtzLinkEn', C_BOOL),  # 云台联动使能;PTZ activation enable;
        ('dwTourMask', C_DWORD * 16),  # 轮询通道掩码;Subnet mask of tour channel;
        ('bTourEnable', C_BOOL),  # 轮询使能;Tour enable;
        ('dwSnapshot', C_DWORD * 16),  # 快照通道号掩码;Snapshot channel subnet mask;
        ('bSnapshotEn', C_BOOL),  # 快照使能;Snapshot enable;
        ('nSnapshotPeriod', c_int),  # 连拍周期(秒);Snapshot period(s);
        ('nSnapshotTimes', c_int),  # 连拍次数;Snapshot times;
        ('bTipEnable', C_BOOL),  # 本地消息框提示;Local prompt dialogue box;
        ('bMailEnable', C_BOOL),  # 发送邮件，如果有图片，作为附件;Send out emali. The image is sent out as the attachment.;
        ('bMessageEnable', C_BOOL),  # 上传到报警服务器;Upload to the alarm server;
        ('bBeepEnable', C_BOOL),  # 蜂鸣;Buzzer;
        ('bVoiceEnable', C_BOOL),  # 语音提示;Audio prompt;
        ('nPlayTimes', c_int),  # 联动语音播放次数bVoiceEnable=TRUE时生效;The Linkage Audio play times,bVoiceEnable=TRUE is effective;
        ('dwMatrixMask', C_DWORD * 16),  # 联动视频矩阵通道掩码;Subnet mask of the activated video channel;
        ('bMatrixEnable', C_BOOL),  # 联动视频矩阵;Activate the video matrix;
        ('nEventLatch', c_int),  # 联动开始延时时间(秒)，0－15;Activation delay time (s),0-15;
        ('bLogEnable', C_BOOL),  # 是否记录日志;Record log or not;
        ('nDelay', c_int),  # 设置时先延时再生效，单位为秒;Delay first and then becomes valid when set. Unit is second.;
        ('bVideoMessageEn', C_BOOL),   # 叠加提示字幕到视频。叠加的字幕包括事件类型，通道号，秒计时。;Overlay the prompt character to the video. The overlay character includes the event type, channel number. The unit is second.;
        ('bMMSEnable', C_BOOL),  # 发送彩信使能;Enable MMS;
        ('bMessageToNetEn', C_BOOL),  # 消息上传给网络使能;Send the message to the network enable;
        ('nTourSplit', c_int),  # 轮巡时的分割模式 0: 1画面; 1: 8画面;Tour split mod 0: 1tour; 1: 8tour;
        ('bSnapshotTitleEn', C_BOOL),  # 是否叠加图片标题;Enble osd;
        ('nPtzLinkExNum', c_int),  # 云台配置数;PTZ link configuration number;
        ('stuPtzLinkEx', NET_PTZ_LINK * 256),  # 扩展云台信息;PTZ extend information;
        ('nSnapTitleNum', c_int),  # 图片标题内容数;Number of picture title;
        ('stuSnapshotTitle', NET_A_CFG_EVENT_TITLE * 256),  # 图片标题内容;Picture title content;
        ('stuMailDetail', NET_A_CFG_MAIL_DETAIL),  # 邮件详细内容;Mail detial;
        ('bVideoTitleEn', C_BOOL),  # 是否叠加视频标题，主要指主码流;Whether overlay video title, mainly refers to the main stream;
        ('nVideoTitleNum', c_int),  # 视频标题内容数目;Video title num;
        ('stuVideoTitle', NET_A_CFG_EVENT_TITLE * 256),  # 视频标题内容;Video title;
        ('nTourNum', c_int),  # 轮询联动数目;Tour num;
        ('stuTour', NET_A_CFG_TOURLINK * 256),  # 轮询联动配置;Tour configuration;
        ('nDBKeysNum', c_int),  # 指定数据库关键字的有效数;Specify the db keyword on the number of effective;
        ('szDBKeys', c_char * 64 * 64),# 指定事件详细信息里需要写到数据库的关键字;The specify event detail information need write the BD keyword;
        ('byJpegSummary', C_BYTE * 1024),  # 叠加到JPEG图片的摘要信息;The summary information of the jpeg image;
        ('bFlashEnable', C_BOOL),  # 是否使能补光灯;Whether enable flash;
        ('nFlashLatch', c_int),  # 补光灯延时时间(秒),延时时间范围：[10,300];Flash delay time (s),the time range:[10,300];
        ('szAudioFileName', c_char * 260),  # 联动语音文件绝对路径;The Absolute Path to the Linkage Audio Files;
        ('bAlarmBellEn', C_BOOL),  # 警号使能;Warning Signal Enable;
        ('bAccessControlEn', C_BOOL),  # 门禁使能;Entrance Guard Enable;
        ('dwAccessControl', C_DWORD),  # 门禁组数;Class Number of Entrance Guard;
        ('emAccessControlType', C_ENUM * 8),# 门禁联动操作信息 Refer: EM_A_NET_EM_CFG_ACCESSCONTROLTYPE;Entrance Guard Linkage Operation Information Refer: EM_A_NET_EM_CFG_ACCESSCONTROLTYPE;
        ('stuTalkback', NET_A_CFG_TALKBACK_INFO),  # 语音呼叫联动信息;Voice Call Linkage Information;
        ('stuPSTNAlarmServer', NET_A_CFG_PSTN_ALARM_SERVER),  # 电话报警中心联动信息;Telephone Alarm Center Linkage Information;
        ('nAlarmBellLatch', c_int),  # 警号输出延时时间(10-300秒);Police no. output delay time(10-300 s);
        ('bReboot', C_BOOL),  # 重启使能TRUE:使能 FALSE:不使能;Rebot Enable,TRUE:enable FALSE:unenble;
        ('nBeepTime', c_int),  # 蜂鸣时长最大值为3600，0代表持续蜂鸣;The Max Beep Time:3600,0 Stand for persistent buzz;
        ('abAudioLinkTime', C_BOOL),  # 联动语音时间使能;enable of nAudioLinkTime;
        ('nAudioLinkTime', c_int),  # 联动语音播放的时间, 单位：秒;time of linkage voice play, uint:s;
        ('abAudioPlayTimes', C_BOOL),  # 联动语音播放使能;enable of nAudioPlayTimes;
        ('nAudioPlayTimes', C_UINT),  # 联动语音播放次数;times of linkage voice play;
        ('abLightingLink', C_BOOL),  # 云台补光灯联动项使能;PTZ light activation enable;
        ('stuLightingLink', NET_CFG_LIGHTING_LINK_INFO),  # 云台补光灯联动项;PTZ light activation;
        ('byReserve', C_BYTE * 828),  # 预留字节;reserved;
    ]

class NET_A_CFG_STORAGENOEXIST_INFO(Structure):
    """
    无存储设备报警配置
    No storage device alarm setup
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 使能开关;Enable;
        ('stuEventHandler', NET_A_CFG_ALARM_MSG_HANDLE),  # 报警联动;Alarm activation;
    ]

class NET_A_CFG_NETABORT_INFO(Structure):
    """
    网络断开报警配置
    Network disconnection alarm setup
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 使能开关;Enable;
        ('stuEventHandler', NET_A_CFG_ALARM_MSG_HANDLE),  # 报警联动;Alarm activation;
    ]

class NET_A_CFG_IPCONFLICT_INFO(Structure):
    """
    IP冲突报警配置
    IP conflict alarm setup
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 使能开关;Enable;
        ('stuEventHandler', NET_A_CFG_ALARM_MSG_HANDLE),  # 报警联动;Alarm activation;
    ]

class NET_A_CFG_MACCONFLICT_INFO(Structure):
    """
    MAC冲突事件报警配置
    MAC conflict event alarm config
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 使能开关;enable siwtch;
        ('stuEventHandler', NET_A_CFG_ALARM_MSG_HANDLE),  # 报警联动;alarm link;
    ]

class NET_A_CFG_LOGIN_FAILURE_ALARM(Structure):
    """
    登陆失败报警配置(对应 CFG_CMD_LOGIN_FAILURE_ALARM)
    login failure alarm(Corresponding to CFG_CMD_LOGIN_FAILURE_ALARM)
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 登陆失败报警使能开关，TRUE为打开，FALSE为关闭;Enable switch of login failure alarm,TRUE is ON,FALSE is OFF;
        ('nTryLoginTimes', c_int),  # 尝试登陆次数，若登陆密码错误次数达到尝试次数后，启动报警联动;Try login times.if times is over nTryLoginTimes, start alarm linkage.;
        ('stuEventHandler', NET_A_CFG_ALARM_MSG_HANDLE),  # 报警联动;alarm link;
    ]

class NET_A_CFG_BATTERY_LOW_POWER_INFO(Structure):
    """
    电池电压低配置 ==>CFG_CMD_BATTERY_LOW_POWER
    Battery voltage low config ==>CFG_CMD_BATTERY_LOW_POWER
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 使能;Enable;
        ('stuEventHandler', NET_A_CFG_ALARM_MSG_HANDLE),  # 报警联动;Alarm activation;
        ('emMode', C_ENUM),  # 电量报警模式 Refer: EM_BATTERY_POWER_ALARM_MODE;Alarm mode Refer: EM_BATTERY_POWER_ALARM_MODE;
        ('nPressure', c_int),  # 正常电压值 手动模式有效 单位：伏;Normal voltage value effective in manual mode Unit: Volt;
        ('nPercent', c_int),  # 百分比，当前电量百分比低于此值报警。手动模式有效;Percentage, the current battery percentage is lower than this value and alarm. Manual mode is effective;
        ('nLowSetNum', c_int),  # 细化档有效个数;The valid number of LowSet.;
        ('nLowSet', c_int * 8),  # 低于Percent以下的细化档，左例表示50以下报警, 低于30再报警，低于10再报警。手动模式有效;Alow Power alarm set. Manual mode is effective;
        ('nNotifyTimes', c_int),  # 报警上报次数, 默认1;Alarm report times, default 1;
    ]

class NET_A_SIZE(Structure):
    """
    尺寸
    Dimensions
    """
    _fields_ = [
        ('nWidth', c_int),  # 宽度;Width;
        ('nHeight', c_int),  # 高度;Height;
    ]

class NET_COLOR_RGBA(Structure):
    """
    颜色RGBA
    color RGBA
    """
    _fields_ = [
        ('nRed', c_int),  # 红;red;
        ('nGreen', c_int),  # 绿;green;
        ('nBlue', c_int),  # 蓝;blue;
        ('nAlpha', c_int),  # 透明;transparent;
    ]

class NET_CFG_SAFETYABNORMAL_INFO(Structure):
    """
    安全异常报警配置
    Security abnormal alarm configuration
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('bEnable', C_BOOL),  # 使能;Enable;
        ('nExceptionNum', c_int),  # 有效异常报警个数;Number of effective exceptions;
        ('stuExceptions', C_ENUM * 16),  # 异常报警类型 Refer: EM_EXCEPTION_TYPE;Exception type Refer: EM_EXCEPTION_TYPE;
        ('stuEventHandler', NET_ALARM_MSG_HANDLE),  # 报警联动;Alarm linkage;
    ]

class NET_A_CFG_BACKUP_LIVE_INFO(Structure):
    """
    实时抽帧配置,EVS
    Real-time frame drawing config, EVS
    Real-time frame drawing config, EVS
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 是否启动抽帧;whether to enable, start frame drawing;
        ('nBackupRate', c_int),  # 抽帧备份比率，如为0表示只保留I帧，其它情况下表示保留I帧以及紧邻其后的若干P帧单位：百分比如果GOP为50，20表示保留50*20%=10帧数据(即1个I帧和9个P帧)。如果计算结果带小数，则取整;If it is 0, only I frame will be reserved. In other cases, I frame and several P frames next to it will be reservedUnit: percentageIf GOP is 50, 20 means 50 * 20% = 10 frames of data (i.e. 1 I frame and 9 P frames) are reserved. If the calculation result is decimal, then round;
        ('stuTimeSection', NET_A_CFG_TIME_SECTION),  # 抽帧时间段;frame drawing time section;
    ]

class NET_A_CFG_RECORD_INFO(Structure):
    """
    定时录像配置信息
    Schedule record configuration information
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号(0开始);The channel number(Begins with 0);
        ('stuTimeSection', NET_A_CFG_TIME_SECTION * 7 * 6),  # 时间表;Time table;
        ('nPreRecTime', c_int),  # 预录时间，为零时表示关闭(0~300);Pre-record time.The value ranges from 0 to 300. This function is unable when the value is 0.;
        ('bRedundancyEn', C_BOOL),  # 录像冗余开关;Record redundancy enbale button;
        ('nStreamType', c_int),  # 0－主码流，1－辅码流1，2－辅码流2，3－辅码流3;0-main stream,1-extra stream 1,2-extra stream 2,3-extra stream 3;
        ('nProtocolVer', c_int),  # 协议版本号, 只读能力;Protocol Version No., read onlyCapacity;
        ('abHolidaySchedule', C_BOOL),  # 为true时有假日配置信息，bHolidayEn、stuHolTimeSection才有效;;There are Holiday Configuration Information When it is True, bHolidayEn,stuHolTimeSection is effective;;
        ('bHolidayEn', C_BOOL),  # 假日录像使能TRUE:使能,FALSE:未使能;Holiday Video Enable TRUE:Enable,FALSE:Unable;
        ('stuHolTimeSection', NET_A_CFG_TIME_SECTION * 6),  # 假日录像时间表;Holiday Video Schedule;
        ('nBackupLiveNum', c_int),  # 实时抽帧配置个数;Real-time frame drawing config number;
        ('stuBackupLiveInfo', NET_A_CFG_BACKUP_LIVE_INFO * 8),  # 实时抽帧配置,EVS;Real-time c config, EVS;
        ('bSaveVideo', C_BOOL),  # 是否录制视频帧;Record video frames;
        ('bSaveAudio', C_BOOL),  # 录像时是否保存音频数据;Whether to save audio data when recording;
    ]

class NET_A_CFG_SNAP_INFO(Structure):
    """
    抓图配置
    Grab Configuration
    """
    _fields_ = [
        ('stuTimeSchedule', NET_A_CFG_TIME_SCHEDULE),  # 时间表, 每个时间段掩码按位定义如下:Bit0-定时抓图Bit1-动态检测抓图Bit2-报警抓图Bit3-卡号抓图Bit4~Bit31-保留;
                              # Schedule, the mask bit for each time period is defined as follows:Bit0-timed shotsBit1-dynamic detection captureBit2-alarm captureBit3-card captureBit4 ~ Bit31 - remain;
    ]

class NET_MEDIA_GLOBAL_INFO(Structure):
    """
    媒体组件全局配置
    Media global config
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nPacketType', c_int),  # 0:按时间,1：按大小;0:by time,1:by size;
        ('byPacketLength', C_BYTE),  # 录像打包时间长度,单位分钟。1-255;Record packet time length. unit:minite. 1-255;
        ('byAlign', C_BYTE * 3),  # 对齐;align;
        ('dwPacketSize', C_DWORD),  # 录像打包文件长度,单位KB;Record packet file size. unit:KB;
        ('bLogRecord', C_BOOL),  # 是否记录录像日志;Is wirte record's log;
        ('bLogEncode', C_BOOL),  # 是否记录编码异常日志;Is write abnormal encode's log;
        ('emSnapFormatAs', C_ENUM),  # 抓图流编码格式参照格式；设备不支持独立配置抓图流分辨率格式时，抓图格式根据参照格式设置 Refer: EM_MEDIA_GLOBAL_SNAP_FORMAT_AS;Snap format reference; If device not support set snap format independently, snap format use reference Refer: EM_MEDIA_GLOBAL_SNAP_FORMAT_AS;
    ]

class NET_A_FORMAT_PATITION(Structure):
    """
    格式化分区信息
    format the partition information
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('pszStorageName', POINTER(c_char)),  # 存储设备名称;storage name;
        ('pszPatitionName', POINTER(c_char)),  # 分区名;partition name;
        ('pszFileSystem', POINTER(c_char)),  # 文件系统格式;file system;
    ]

class NET_A_CFG_MOTION_WINDOW(Structure):
    """
    动检支持的视频窗口配置
    Dynamic configuartion support video window
    """
    _fields_ = [
        ('nThreshold', c_int),  # 面积阀值，取值[0, 100];The area threshold,[0, 100];
        ('nSensitive', c_int),  # 灵敏度，取值[0, 100];Sensitive,[0, 100];
        ('stuWindow', CFG_RECT),  # 动检窗口区域, 坐标位置取值[0, 8192);Motion window area, coordinate range [0, 8192);
    ]

class NET_A_CFG_DETECT_REGION(Structure):
    """
    检测区域
    3rd generation motion detection zone
    """
    _fields_ = [
        ('nRegionID', c_int),  # 区域ID;Zone ID;
        ('szRegionName', c_char * 64),  # 动态窗口名称;Motion window name;
        ('nThreshold', c_int),  # 面积阀值，取值[0, 100];Area threshold, value[0, 100];
        ('nSenseLevel', c_int),  # 灵敏度1～6;Sensitivity 1-6;
        ('nMotionRow', c_int),  # 动态检测区域的行数;Motion zone row;
        ('nMotionCol', c_int),  # 动态检测区域的列数;Motion detection zone column;
        ('byRegion', C_BYTE * 32 * 32),  # 检测区域，最多32*32块区域;Detection zone, max 32*32 blocks;
    ]

class NET_A_CFG_MOTION_INFO(Structure):
    """
    动态检测报警配置
    Motion detect alarm setup
    """
    _fields_ = [
        ('nChannelID', c_int),  # 报警通道号(0开始), nVersion=1时，此字段无效;Alarm channel number (Begins with 0);
        ('bEnable', C_BOOL),  # 使能开关;Enable;
        ('nSenseLevel', c_int),  # 一代动检灵敏度1～6;Sensitivity 1~6;
        ('nMotionRow', c_int),  # 一代动态检测区域的行数;The rows of the motion detect zone;
        ('nMotionCol', c_int),  # 一代动态检测区域的列数;The columns of the motion detect zone;
        ('byRegion', C_BYTE * 32 * 32),  # 一代检测区域，最多32*32块区域;Motion detect,Max 32*32 zones;
        ('stuEventHandler', NET_A_CFG_ALARM_MSG_HANDLE),  # 报警联动;Alarm activation;
        ('stuTimeSection', NET_A_CFG_TIME_SECTION * 7 * 6),  # 事件响应时间段，时间段获取和设置以此成员为准，忽略 stuEventHandler 中的 stuTimeSection;Event responding period,if you want set and get time, take this as the standard;ignore the "stuTimeSection" filed in stuEventHandler;
        ('nVersion', c_int),  # 0, 1, 由能力集确定, 只读, 等于1时以下字段有效;0, 1, be determined by the capability set set, read only,when equal 1,the following fields;
        ('bSenseLevelEn', C_BOOL),  # 只读，决定nSenseLevel是否有效;Read only,decide nSenseLevel efficiency or not;
        ('bVRatioEn', C_BOOL),  # 只读，面积占用比使能， 决定nVolumeRatio是否有效;Read only,the area impropriate enable, decide nVolumeRatio efficiency or not;
        ('nVolumeRatio', c_int),  # 一代动检的面积占用比,1-100;The area impropriate,1-100;
        ('bSRatioEn', C_BOOL),  # 只读，灵敏度使能，决定nSubRatio值是否有效;Read only, sensitivity enable,decide nVolumeRatio efficiency or not;
        ('nSubRatio', c_int),  # 一代动检的残差阈值, 1-100;Motion inspection of residual error threshold, 1-100;
        ('abWindow', C_BOOL),  # 此字段及以下两个字段已废弃;Read only,0: nMotionRow, nMotionCol,byRegion availability, 1: the following field in the video window;
        ('nWindowCount', c_int),  # 视频窗口个数;Number of video window;
        ('stuWindows', NET_A_CFG_MOTION_WINDOW * 10),  # 视频窗口数组;Video window;
        ('abDetectRegion', C_BOOL),  # 只读，1：nRegionCount，stuRegion有效0：nMotionRow，nMotionCol，byRegion有效;Read only, 1:nRegionCount, stuRegion valid0:nMotionRow, nMotionCol, byRegion valid;
        ('nRegionCount', c_int),  # 三代动态检测区域个数;3rd generation motion detection zone quantity;
        ('stuRegion', NET_A_CFG_DETECT_REGION * 10),  # 三代动态检测区域;3rd generation motion detection zone;
        ('stuRemoteEventHandler', NET_A_CFG_ALARM_MSG_HANDLE),  # 前端动态检测联动;Remote alarm activation;
        ('stuRemoteTimeSection', NET_A_CFG_TIME_SECTION * 7 * 6),  # 前端动态检测联动, 事件响应时间段，时间段获取和设置以此成员为准，忽略 stuRemoteEventHandler 中的 stuTimeSection;Remote event responding period, if you want set and get time, take this as the standard; ignore the "stuTimeSection" filed in stuRemoteEventHandler;
    ]

class NET_SMART_MOTION_DETECT_OBJECT(Structure):
    """
    智能动态检测对象
    Intelligent dynamic detection object
    """
    _fields_ = [
        ('bHuman', C_BOOL),  # 动态检测人使能;Dynamic detection human enable;
        ('bVehicle', C_BOOL),  # 动态检测车使能;Dynamic detection vehicle enable;
        ('byReserved', C_BYTE * 1020),  # 保留字节;Reserved byte;
    ]

class NET_CFG_SMART_MOTION_DETECT(Structure):
    """
    智能动态检测配置
    Intelligent dynamic detection configuration
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Struct size;
        ('bEnable', C_BOOL),  # 动检使能，开：TRUE 关：FALSE;Dynamic inspection enable, on: TRUE, off: FALSE;
        ('emMotionDetectSensitivityLevel', C_ENUM),  # 动检敏感级别 Refer: EM_SMART_MOTION_DETECT_SENSITIVITY_LEVEL;Motion detection sensitivity level Refer: EM_SMART_MOTION_DETECT_SENSITIVITY_LEVEL;
        ('stuMotionDetectObject', NET_SMART_MOTION_DETECT_OBJECT),  # 智能动态检测对象;Intelligent dynamic detection configuration;
    ]

class NET_A_CFG_ALARMIN_INFO(Structure):
    """
    外部报警配置
    External alarm setup
    """
    _fields_ = [
        ('nChannelID', c_int),  # 报警通道号(0开始);Alarm channel number (Begins with 0);
        ('bEnable', C_BOOL),  # 使能开关;Enable;
        ('szChnName', c_char * 64),  # 报警通道名称;Alarm channel name;
        ('nAlarmType', c_int),  # 报警器类型，0：常闭，1：常开;Alarm device type,0:NC,1:NO;
        ('stuEventHandler', NET_A_CFG_ALARM_MSG_HANDLE),  # 报警联动;Alarm activation;
        ('stuTimeSection', NET_A_CFG_TIME_SECTION * 7 * 6),  # 事件响应时间段，时间段获取和设置以此成员为准，忽略 stuEventHandler 中的 stuTimeSection;Event responding period,if you want set and get time, take this as the standard;ignore the "stuTimeSection" filed in stuEventHandler;
        ('abDevID', C_BOOL),
        ('szDevID', c_char * 128),  # 设备ID;Device ID;
        ('nPole', c_int),  # 传感器触发模式, 0:高有效，1低有效；具体表现为传感器接地or电源，与nAlarmType组合使用;Sensor trigger mode, 0:high effective,1low effective;Sensor grounding or supply,with nAlarmType;
        ('emSense', C_ENUM),  # 传感器感应方式 Refer: EM_SENSE_METHOD;Inductive sensor Refer: EM_SENSE_METHOD;
        ('emCtrl', C_ENUM),  # 报警使能控制方式 Refer: EM_CTRL_ENABLE;Alarm control Refer: EM_CTRL_ENABLE;
        ('nDisDelay', c_int),  # 延时撤防时间,防区类型为"Delay"(延时防区)时才有效, 单位: 秒, 最大时间通过查询能力获得emCtrl值为EM_CTRL_NORMAL或EM_CTRL_ALWAYS_EN 时有效。;Delay time machine, unit(s),0~300,emCtrl value is EM_CTRL_NORMAL or EM_CTRL_ALWAYS_EN valid;
        ('emDefenceAreaType', C_ENUM),  # 防区类型, 具体支持的类型通过查询能力获得 Refer: EM_CFG_DEFENCEAREATYPE;DefenceArea Type , Specific Types Supported by Querying the Ability to Obtain Refer: EM_CFG_DEFENCEAREATYPE;
        ('nEnableDelay', c_int),  # 延时布防时间, 防区类型为"Delay"(延时防区)时才有效, 单位: 秒, 最大时间通过查询能力获得;Delay Protection Time, DefenceArea Type is"Delay"(Delay DefenceArea)is Effective, Unit: Second, Maximum Time by Querying the Ability to Obtain;
        ('nSlot', c_int),  # 根地址, -1表示无效, 0表示本地通道, 1表示连接在第一个串口上的扩展通道, 2、3...以此类推;Root address, -1 means invalid, 0 means local channel, 1 means connect to 1st serial extention channel, 2,3...and so on;
        ('nLevel1', c_int),  # 第一级级联地址, 表示连接在第nSlot串口上的第nLevel1个探测器或仪表, -1表示无效, 从0开始;1st level cascading address, means connection to no.nSlot serial no.nLevel 1 detector or meter, -1 means invalid, from 0;
        ('abLevel2', c_bool),  # 表示nLevel2字段是否存在;Means if nLevel2 text exists;
        ('nLevel2', c_int),  # 第二级级联地址, 表示连接在第nLevel1个的仪表上的探测器序号, -1表示无效, 从0开始;2rd level cascading address, means connected to no. nLevel1 meter's detector no., -1 means invalid, from 0;
        ('nDoorNotClosedTimeout', c_int),  # 门未关超时时间,单位为s,范围 15s-300s;The timeout of un-close the door,unit second,range is 15s-300s;
    ]

class NET_A_AV_CFG_StorageGroupChannel(Structure):
    """
    存储组通道相关配置
    Storage group channel corresponding config
    """
    _fields_ = [
        ('nStructSize', c_int),
        ('nMaxPictures', c_int),  # 每个通道文件夹图片存储上限, 超过就覆盖;Picture storage threshold of each channel folder. System overwrites once it reaches the threshold.;
        ('szPath', c_char * 32),  # 通道在命名规则里的字符串表示, %c对应的内容;The string of the channel in the Name Rule. The corresponding contents of %c.;
    ]

class NET_A_AV_CFG_StorageGroup(Structure):
    """
    存储组配置
    Storage group config
    """
    _fields_ = [
        ('nStructSize', c_int),
        ('szName', c_char * 64),  # 分组名称;Group name;
        ('szMemo', c_char * 128),  # 分组说明;Group note;
        ('nFileHoldTime', c_int),  # 文件保留时间;File save time;
        ('bOverWrite', C_BOOL),  # 存储空间满是否覆盖;Overwrite or not when the storage space is full.;
        ('szRecordPathRule', c_char * 260),  # 录像文件路径命名规则;Record file path name rule;
        ('szPicturePathRule', c_char * 260),  # 图片文件路径命名规则%y年, %M月, %d日, %h时, %m分, %s秒, %c通道路径如果年月日时分秒出现两次, 第一次表示开始时间, 第二次表示结束时间;Picture file path name rule%y=Y, %M=M, %d=D, %h=H, %m=M, %s=S, %c=Channel pathIf the Y-M-D-M-S appears twice, the first one stands for the start time and the second one stands for the end time.;
        ('stuChannels', NET_A_AV_CFG_StorageGroupChannel * 1024),  # 通道相关配置;Channel corresponding config;
        ('nChannelCount', c_int),  # 通道配置数;Channel config amount;
        ('szCustomName', c_char * 64),  # 自定义名称，若为空使用szName;custom name，if it is null use szName;
        ('szSubDevices', c_char * 16 * 64),  # 子设备列表;sub device list;
        ('nSubDevices', c_int),  # 子设备数量;sub device amount;
    ]

class NET_A_AV_CFG_RecordMode(Structure):
    """
    三代协议新增
    录像模式
    The 3rd protocol newly added contents
    Record mode
    """
    _fields_ = [
        ('nStructSize', c_int),
        ('nMode', c_int),  # 录像模式, 0-自动录像，1-手动录像，2-关闭录像;record mode, 0-schedule, 1- manual, 2- off;
        ('nModeExtra1', c_int),  # 辅码流1录像模式, 0-自动录像，1-手动录像，2-关闭录像;Sub stream1 record mode, 0-auto, 1-manual, 2-OFF;
        ('nModeExtra2', c_int),  # 辅码流2录像模式, 0-自动录像，1-手动录像，2-关闭录像;Sub stream2 record mode, 0-auto, 1-manual, 2-OFF;
    ]

class NET_A_CFG_SERVER_INFO(Structure):
    """
    服务器
    service
    """
    _fields_ = [
        ('nPort', c_int),  # 服务器端口号;service port;
        ('szAddress', c_char * 256),  # IP地址或网络名;IP address or;
    ]

class NET_A_CFG_REGISTER_SERVER_INFO(Structure):
    """
    主动注册配置
    initiative register configuration
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 主动注册使能;initiative register enable;
        ('szDeviceID', c_char * 256),  # 设备ID;device ID;
        ('nServersNum', c_int),  # 服务器个数;server num;
        ('stuServers', NET_A_CFG_SERVER_INFO * 10),  # 服务器数组;servers;
    ]

class NET_A_CFG_REGISTERSERVER_VEHICLE(Structure):
    """
    车载专用主动注册配置
    Vehicle-specific active registration configuration
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 主动注册使能;Active registration enabled;
        ('bRepeatEnable', C_BOOL),  # 是否发送相同坐标数据;Whether to send the same coordinate data;
        ('szDeviceID', c_char * 256),  # 子设备ID;Sub-device ID;
        ('nSendInterval', c_int),  # 发送间隔, 单位：秒;Sent interval, uint:s;
        ('szAddress', c_char * 256),  # IP地址或网络名;IP Addredd or network name;
        ('nPort', c_int),  # 端口号;Port;
        ('emSendPolicy', C_ENUM),  # 上传策略 Refer: EM_CFG_SENDPOLICY;Send Policy Refer: EM_CFG_SENDPOLICY;
        ('szTestAddress', c_char * 256),  # 测试IP地址或网络名;Test IP Address or network name;
        ('nTestPort', c_int),  # 测试端口号;Test port;
        ('byReserved', C_BYTE * 1024),  # 保留字节;Reserved;
    ]

class NET_A_CFG_DVRIP_INFO(Structure):
    """
    网络协议配置
    network protocol configuration
    """
    _fields_ = [
        ('nTcpPort', c_int),  # TCP服务端口,1025~65535;TCP server port,1025~65535;
        ('nSSLPort', c_int),  # SSL服务端口,1025~65535;SSL server port,1025~65535;
        ('nUDPPort', c_int),  # UDP服务端口,1025~65535;UDP server port,1025~65535;
        ('nMaxConnections', c_int),  # 最大连接数;max connections;
        ('bMCASTEnable', C_BOOL),  # 组播使能;multicast enable;
        ('nMCASTPort', c_int),  # 组播端口号;multicast port;
        ('szMCASTAddress', c_char * 256),  # 组播地址;multicast address;
        ('nRegistersNum', c_int),  # 主动注册配置个数;number of initiative register configuration;
        ('stuRegisters', NET_A_CFG_REGISTER_SERVER_INFO * 10),  # 主动注册配置;initiative register configuration;
        ('emStreamPolicy', C_ENUM),  # 带宽不足时码流策略 Refer: EM_STREAM_POLICY;Bit stream strategy when bandwitch is insufficient Refer: EM_STREAM_POLICY;
        ('stuRegisterServerVehicle', NET_A_CFG_REGISTERSERVER_VEHICLE),  # 车载专用主动注册配置;Vehicle-specific active registration configuration;
    ]

class NET_A_CFG_ALARM_SUBSYSTEM_MSG_HANDLE(Structure):
    """
    报警联动
    Alarm activation
    """
    _fields_ = [
        ('bAlarmOutEnable', C_BOOL),  # 报警输出使能;support alarm output or not;
        ('bAlarmBellEnable', C_BOOL),  # 警号输出使能;support alarm bell or not;
        ('nAlarmOutChannelNum', c_int),  # 报警输出通道号个数;Channel's count of alarm output;
        ('nAlarmOutChannels', c_int * 256),  # 报警输出通道号列表;Channel list of alarm output;
    ]

class NET_A_CFG_ALARM_SUBSYSTEM_INFO(Structure):
    """
    报警子系统配置 ==>CFG_CMD_ALARM_SUBSYSTEM
    Alarm sub system config ==>CFG_CMD_ALARM_SUBSYSTEM
    """
    _fields_ = [
        ('szName', c_char * 128),  # 名称;name;
        ('nZoneNum', c_int),  # 本地防区数目;Local zone quantity;
        ('anZone', c_int * 256),  # 本地防区号;Local zone no.;
        ('nExZoneNum', c_int),  # 扩展防区数目;Extention zone quantity;
        ('anExZone', c_int * 256),  # 扩展防区号;Extention zone no.;
        ('nDisableDelay', c_int),  # 延时撤防时间（进入延时）, 单位为秒;Delay disarm time, entry time, ,unit is s;
        ('nEnableDelay', c_int),  # 延时布防时间（退出延时）, 单位为秒;Delay arm time, exit delay, , unit is s;
        ('bIsPublic', C_BOOL),  # 是否为公共子系统;Public sub system;
        ('nPublicSubSystem', c_int),  # 公共所属的子系统数目;Public sub system quantity;
        ('anPublicSubSystem', c_int * 256),  # 公共所属的关联子系统;Public link sub system;
        ('stuEventHandler', NET_A_CFG_ALARM_SUBSYSTEM_MSG_HANDLE),  # 报警联动;Alarm activation;
        ('bEnable', C_BOOL),  # 是否启用子系统;enable the subsystem or not;
    ]

class NET_A_CFG_DATA_TIME(Structure):
    """
    日期
    data time
    """
    _fields_ = [
        ('dwYear', C_DWORD),  # 年;year;
        ('dwMonth', C_DWORD),  # 月;month;
        ('dwDay', C_DWORD),  # 日;day;
        ('dwHour', C_DWORD),  # 时;hour;
        ('dwMinute', C_DWORD),  # 分;minute;
        ('dwSecond', C_DWORD),  # 秒;second;
        ('dwReserved', C_DWORD * 2),  # 保留字段;reserved;
    ]

class NET_A_CFG_DEV_DISPOSITION_INFO(Structure):
    """
    普通配置 (CFG_CMD_DEV_GENERRAL) General
    General configuration(CFG_CMD_DEV_GENERRAL) General
    """
    _fields_ = [
        ('nLocalNo', c_int),  # 本机编号，主要用于遥控器区分不同设备 0~998;Device number,0~998;
        ('szMachineName', c_char * 256),  # 机器名称或编号;Machine name;
        ('szMachineAddress', c_char * 256),  # 机器部署地点即道路编码;Machine instal address,such as road number;
        ('szMachineGroup', c_char * 256),  # 机器分组或叫设备所属单位 默认为空，用户可以将不同的设备编为一组，便于管理，可重复。;Machine group, it instal as null,;
        ('szMachineID', c_char * 64),  # 机器编号, 联网平台内唯一;The machine serial number exclusive;
        ('nLockLoginTimes', c_int),  # 登陆失败可尝试次数;logon failed attempt times;
        ('nLoginFailLockTime', c_int),  # 登陆失败锁定时间;login failed lock time;
        ('bLockLoginEnable', C_BOOL),  # 登陆失败可尝试次数使能;logon failed attempt times enable;
        ('stuActivationTime', NET_A_CFG_DATA_TIME),  # 启动时间;activation time;
        ('bReserved', C_BYTE * 916),  # 保留字节;Reserved;
    ]

class NET_IN_GET_DEVICESERIALNO_INFO(Structure):
    """
    CLIENT_GetDeviceSerialNo 入参
    CLIENT_GetDeviceSerialNo input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
    ]

class NET_OUT_GET_DEVICESERIALNO_INFO(Structure):
    """
    CLIENT_GetDeviceSerialNo 出参
    CLIENT_GetDeviceSerialNo output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('szSN', c_char * 64),  # 序列号;serial number;
    ]

class NET_A_CFG_COMMADDR_INFO(Structure):
    """
    串口地址
    Serial address
    """
    _fields_ = [
        ('nAddressNum', c_int),  # 串口地址个数;serial address number;
        ('nAddress', c_int * 16),  # 地址描述,不同厂商地址位不同，用数组表示;address description, different manufacturer has different addresses, in group;
    ]

class NET_A_CFG_PROFILE_INFO(Structure):
    """
    情景详细信息
    Profile detail info
    """
    _fields_ = [
        ('nSceneID', c_int),  # 情景ID;Scene ID;
        ('szBrand', c_char * 64),  # 厂家名称;Device brand;
        ('emScene', C_ENUM),  # 情景模式 Refer: EM_SMARTHOME_SCENE_MODE;Scene mode Refer: EM_SMARTHOME_SCENE_MODE;
        ('stuCommAddr', NET_A_CFG_COMMADDR_INFO),  # 串口地址;Device address;
    ]

class NET_A_CFG_SCENE_MODE_INFO(Structure):
    """
    情景模式配置 (对应 CFG_CMD_SCENE_MODE)
    Profile config (corresponding to CFG_CMD_SCENE_MODE)
    """
    _fields_ = [
        ('nCurrentID', c_int),  # 当前情景模式ID号;Current profile ID;
        ('nProfileCount', c_int),  # 情景模式个数;The valid count of profile;
        ('stuProfiles', NET_A_CFG_PROFILE_INFO * 54),  # 情景模式信息;The profile;
    ]

class NET_MEMBERS_INFO(Structure):
    """
    联系人信息
    Contact member info
    """
    _fields_ = [
        ('szName', c_char * 32),  # 联系人姓名;contact member name;
        ('szMobile', c_char * 16),  # 设备描述;device description;
        ('szEmail', c_char * 32),  # 电子邮箱;E-mail;
        ('szOrganization', c_char * 64),  # 组织;organization;
    ]

class NET_NOTIFY_INFO(Structure):
    """
    用户组关联通知信息
    User group association notify information
    """
    _fields_ = [
        ('emType', C_ENUM),  # 通知类型 Refer: EM_A_NET_NOTIFY_TYPE;notify type Refer: EM_A_NET_NOTIFY_TYPE;
        ('bAlarmEvents', C_BOOL),  # 是否接受报警事件的推送;accept alarm event notify or not;
        ('bSystemEvents', C_BOOL),  # 是否接受故障事件的推送;accept system fault event notify or not;
        ('bOperationEvents', C_BOOL),  # 是否接受操作事件的推送;accept operation event or not;
    ]

class NET_NETAPP_COMMUNICATION_LIST(Structure):
    """
    通讯录配置列表
    communication config list
    """
    _fields_ = [
        ('szGroupName', c_char * 16),  # 自定义组名,不可重复命名;custom group name,Non-repeatable naming;
        ('nMembersNum', c_int),  # 联系人个数;num of member;
        ('arrMembers', NET_MEMBERS_INFO * 32),  # 联系人信息;contact member info;
        ('stuNotifyInfo', NET_NOTIFY_INFO),  # 用户组关联通知信息;user group association notify info;
    ]

class NET_NETAPP_COMMUNICATION_LIST_CFG(Structure):
    """
    通讯录配置
    CommunicationList config
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;struct size;
        ('nConmmunicationListNum', c_int),  # 实际的通讯录配置个数;num of communication list config;
        ('stuCommunication', NET_NETAPP_COMMUNICATION_LIST * 10),  # 通讯录配置数组;communication config array;
    ]

class NET_A_CFG_CHASSISINTRUSION_INFO(Structure):
    """
    机箱入侵报警(防拆报警)配置
    Chassis intrusion alarm (tamper alarm) configuration
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 使能开关;Enable switch;
        ('stuEventHandler', NET_A_CFG_ALARM_MSG_HANDLE),  # 报警联动;alarmLinkage;
    ]

class NET_A_QUERY_DEVICE_LOG_PARAM(Structure):
    """
    查询记录数条件
    search record filter
    """
    _fields_ = [
        ('emLogType', C_ENUM),  # 查询日志类型 Refer: EM_A_LOG_QUERY_TYPE;Searched log type Refer: EM_A_LOG_QUERY_TYPE;
        ('stuStartTime', NET_TIME),  # 查询日志的开始时间;The searched log start time;
        ('stuEndTime', NET_TIME),  # 查询日志的结束时间;The searched log end time.;
        ('nStartNum', c_int),  # 在时间段中从第几条日志开始查询,开始第一次查询可设为0;The search begins from which log in one period. It shall begin with 0 if it is the first time search.;
        ('nEndNum', c_int),  # 一次查询中到第几条日志结束,日志返回条数的最大值为1024;The ended log serial number in one search,the max returning number is 1024;
        ('nLogStuType', C_BYTE),  # 日志数据结构体类型,0:表示NET_A_DEVICE_LOG_ITEM；1:表示NET_A_DEVICE_LOG_ITEM_EX;log struct type,0:NET_A_DEVICE_LOG_ITEM;1:NET_A_DEVICE_LOG_ITEM_EX;
        ('reserved', C_BYTE * 3),  # 保留 对齐;Reserved;
        ('nChannelID', C_UINT),  # 通道号,0:兼容之前表示所有通道号,所以通道号从1开始; 1:第一个通道;Channel no. 0:Compatible with previous all channel numbers. The channel No. begins with 1.1: The first channel.;
        ('bReserved', C_BYTE * 40),
    ]

class NET_A_CFG_WLAN_EAP(Structure):
    """
    单个WLAN配置EAP
    EAP of one WLAN
    """
    _fields_ = [
        ('emMethod', C_ENUM),  # EAP方法 Refer: EM_CFG_EAP_METHOD;EAP method Refer: EM_CFG_EAP_METHOD;
        ('emAuthType', C_ENUM),  # EAP身份验证方法 Refer: EM_CFG_EAP_AUTH_TYPE;EAP auth Refer: EM_CFG_EAP_AUTH_TYPE;
        ('szIdentity', c_char * 64),  # 身份;Identity;
        ('szAnonymousID', c_char * 64),  # 匿名身份;AnonymousID;
        ('szPassword', c_char * 64),  # 密码;Password;
        ('szCaCert', c_char * 512),  # CA证书;CA;
        ('szUserCert', c_char * 512),  # 用户证书;User Cert;
    ]

class NET_A_CFG_WLAN_NETWORK(Structure):
    """
    单个WLAN配置Network
    Network of one WLAN
    """
    _fields_ = [
        ('szIPAddress', c_char * 40),  # IP;IP;
        ('szSubnetMask', c_char * 40),  # 子网掩码;subnet mask;
        ('szDefaultGateway', c_char * 40),  # 网关;gateway;
        ('bDhcpEnable', C_BOOL),  # 是否开启DHCP;DHCP enable;
        ('szDnsServers', c_char * 2 * 40),  # DNS服务器;DNS servers;
    ]

class NET_A_CFG_WLAN_INFO(Structure):
    """
    单个WLAN配置
    WLAN configure
    """
    _fields_ = [
        ('szWlanName', c_char * 32),  # Wlan名称, 只能获取不能修改;Wlan name, read only;
        ('bEnable', C_BOOL),  # WIFI网卡使能开关, TRUE打开, FALSE关闭;WIFI interface enable;
        ('szSSID', c_char * 36),  # 网络名称(SSID);SSID;
        ('bConnectEnable', C_BOOL),  # 手动连接开关, TRUE手动连接, FALSE手动断开;manual connect to WLAN, TRUE: connect, FALSE: disconnect;
        ('bLinkEnable', C_BOOL),  # 自动连接开关, TRUE不自动连接, FALSE自动连接, IPC无意义;auto connect to WALN, TRUE: no, FALSE: yes, no scene for IPC;
        ('nLinkMode', c_int),  # 连接模式, 0: auto, 1: adhoc, 2: Infrastructure;link mode, 0: auto, 1: adhoc, 2: Infrastructure;
        ('nEncryption', c_int),  # 加密模式, 0: off, 1: on, 2: WEP64, 3: WEP128, 4: WPA-PSK-TKIP, 5: WPA-PSK-AES, 6: WPA2-PSK-TKIP, 7: WPA2-PSK-AES, 8: WPA-TKIP, 9: WPA-AES,10: WPA2-TKIP, 11: WPA2-AES, 12: AUTO;Encryption, 0: off, 1: on, 2: WEP-OPEN, 3: WEP-SHARED, 4: WPA-TKIP, 5: WPA-PSK-TKIP, 6: WPA2-TKIP, 7: WPA2-PSK-TKIP, 8: WPA-AES, 9: WPA-PSK-AES, 10: WPA2-AES, 11: WPA2-PSK-AES, 12: Auto;
        ('emAuthentication', C_ENUM),  # 认证方式, 暂时没用 Refer: EM_CFG_WIRELESS_AUTHENTICATION;Authentication, unused Refer: EM_CFG_WIRELESS_AUTHENTICATION;
        ('emDataEncryption', C_ENUM),  # 数据加密方式, 暂时没用 Refer: EM_CFG_WIRELESS_DATA_ENCRYPT;Data Encryption, unused Refer: EM_CFG_WIRELESS_DATA_ENCRYPT;
        ('nKeyType', c_int),  # 密码类型, 0: Hex, 1: ASCII;Key Type, 0: Hex, 1: ASCII;
        ('nKeyID', c_int),  # 秘钥索引, 取值0~3;Key index, range of 0~3;
        ('szKeys', c_char * 4 * 128),  # 四组密码;four keys;
        ('bKeyFlag', C_BOOL),  # 密码是否已经设置;is key set or not;
        ('stuEap', NET_A_CFG_WLAN_EAP),  # EAP;EAP;
        ('stuNetwork', NET_A_CFG_WLAN_NETWORK),  # Network;Network;
    ]

class NET_A_CFG_NETAPP_WLAN(Structure):
    """
    WLAN配置(对应 CFG_CMD_WLAN)
    all WLAN configure(corresponding to CFG_CMD_WLAN)
    """
    _fields_ = [
        ('nNum', c_int),  # stuWlanInfo有效的WLAN配置个数;valid WLAN info in stuWlanInfo;
        ('stuWlanInfo', NET_A_CFG_WLAN_INFO * 8),  # WLAN配置信息;WLAN info;
    ]

class NET_IN_WLAN_ACCESSPOINT(Structure):
    """
    CLIENT_QueryDevInfo , NET_QUERY_WLAN_ACCESSPOINT 命令输入参数
    CLIENT_QueryDevInfo , NET_QUERY_WLAN_ACCESSPOINT input
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('szSSID', c_char * 36),  # 需要获取信息的无线网络名称,为空时搜索所有网络;SSID of wireless network whose info you want to query. if null, query all wireless network;
        ('szName', c_char * 32),  # 网卡名称, 为空时, 默认为eth2;Network Name, default is eth2;
    ]

class NET_WLAN_ACCESSPOINT_INFO(Structure):
    """
    接入点信息
    info for each network
    """
    _fields_ = [
        ('szSSID', c_char * 36),  # 无线网络名称;SSID (name of wireless network);
        ('nStrength', c_int),  # 信号强度 范围0-100;signal strength, range: 0-100;
        ('nAuthMode', c_int),  # 认证模式0:OPEN;1:SHARED;2:WPA;3:WPA-PSK;4:WPA2;5:WPA2-PSK;6:WPA-NONE(用在adhoc网络模式),7-11是混合模式,选择其中任何一种都可以进行连接7:WPA-PSK | WPA2-PSK; 8:WPA | WPA2; 9:WPA | WPA-PSK;10:WPA2 | WPA2-PSK; 11:WPA | WPA-PSK |WPA2 |WPA2-PSK 12: UnKnown;attestation mod:0:OPEN;1:SHARED;2:WPA;3:WPA-PSK;4:WPA2;5:WPA2-PSK;6:WPA-NONE(only use in Adhoc mode),7-11 are mix mode,choose one of them can to be connected7:WPA-PSK | WPA2-PSK; 8:WPA | WPA2; 9:WPA | WPA-PSK;10:WPA2 | WPA2-PSK; 11:WPA | WPA-PSK |WPA2 |WPA2-PSK 12: UnKnown;
        ('nEncrAlgr', c_int),  # 0:NONE, 1:WEP, 2:TKIP, 3:AES(CCMP), 4:TKIP+AES( mix Mode), 5:UnKnown;0:NONE, 1:WEP, 2:TKIP, 3:AES(CCMP), 4:TKIP+AES( mix Mode), 5:UnKnown;
        ('reserved', c_char * 1016),
    ]

class NET_OUT_WLAN_ACCESSPOINT(Structure):
    """
    CLIENT_QueryDevInfo , NET_QUERY_WLAN_ACCESSPOINT 命令输出参数
    CLIENT_QueryDevInfo , NET_QUERY_WLAN_ACCESSPOINT output
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nCount', c_int),  # 无线网络接入点个数;wireless network count;
        ('stuInfo', NET_WLAN_ACCESSPOINT_INFO * 128),  # 接入点信息;info for each network;
    ]

class NET_A_CFG_WIRELESS_INFO(Structure):
    """
    无线网络连接设置
    Wi-Fi Settings
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 2G网络使能;2G Network Enables;
        ('nKeepAlive', c_int),  # 保活时间, 单位为秒，0表示一直连接，不自动断开;Keep-alive time, in seconds, 0 means always connected, does not automatically disconnect;
        ('emAPN', C_ENUM),  # 接入的2G网络名称 Refer: EM_CFG_APN;the name of the 2G network access Refer: EM_CFG_APN;
        ('szUseName', c_char * 64),  # 用户名;User Name;
        ('szPassword', c_char * 64),  # 密码;Password;
        ('emDay3GFluxTactic', C_ENUM),  # 每日流量控制策略 Refer: EM_CFG_DAY3GFLUXTACTIC;Daily Traffic Control Strategy Refer: EM_CFG_DAY3GFLUXTACTIC;
        ('dwDay3GFluxUp', C_DWORD),  # 每日流量使用上限, MB或者分钟;Daily Traffic Usage Limit, MB or minute;
        ('dwDay3GFluxUse', C_DWORD),  # 当日的已用流量, MB或者分钟;Used Traffic Day, MB or minute;
        ('emDay3GFluxAction', C_ENUM),  # 流量报警策略 Refer: EM_CFG_DAY3GFLUXACTION;Traffic police tactics Refer: EM_CFG_DAY3GFLUXACTION;
        ('stuTimeSection', NET_A_CFG_TIME_SECTION * 7 * 6),  # 拨号时间段;Time sections;
        ('emAuthMode', C_ENUM),  # 鉴权模式 Refer: EM_CFG_AUTHMODE;Authentication mode Refer: EM_CFG_AUTHMODE;
        ('szAPNName', c_char * 32),  # 接入网络名;APN name;
        ('n3GFlux', C_UINT),  # 实际使用流量, [0,65535]MB或者分钟;The actual use of flux, [0,65535]MB or minute;
        ('em3GFluxTactic', C_ENUM),  # 流量使用策略 Refer: EM_CFG_3GFLUXTACTIC;flux usage policy Refer: EM_CFG_3GFLUXTACTIC;
        ('n3GFluxUp', C_UINT),  # 流量使用上限;Flux usage up limit;
        ('emWorkMode', C_ENUM),  # 工作模式选择 Refer: EM_CFG_WORKMODE;working mode selection Refer: EM_CFG_WORKMODE;
        ('szDailNumber', c_char * 32),  # 拨号号码;Dail number;
        ('bActivate', C_BOOL),  # 是否已经被语音或短信激活;Whether it has been activated by voice or SMS;
    ]

class NET_CODEID_INFO(Structure):
    """
    对码信息
    Code info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nWirelessId', C_TP_U64),  # 无线ID号;Wireless ID no.;
        ('emType', C_ENUM),  # 无线设备类型 Refer: EM_A_NET_WIRELESS_DEVICE_TYPE;Wireless device type Refer: EM_A_NET_WIRELESS_DEVICE_TYPE;
        ('szName', c_char * 8),  # 用户名;Username;
        ('bEnable', C_BOOL),  # 是否启用了此设备;Enable this device;
        ('szCustomName', c_char * 64),  # 自定义名称;Custom Name;
        ('nChannel', c_int),  # 无线防区的alarm通道号,Alarm配置的下标,只有Type为Defence时此字段才有效。;It only to be valid when emType is NET_WIRELESS_DEVICE_TYPE_DEFENCE;
        ('emMode', C_ENUM),  # 无线设备工作模式 Refer: EM_WIRELESS_DEVICE_MODE;Wireless Device Mode. Refer: EM_WIRELESS_DEVICE_MODE;
        ('emSenseMethod', C_ENUM),  # 传感器方式 Refer: EM_CODEID_SENSE_METHOD_TYPE;The sense method Refer: EM_CODEID_SENSE_METHOD_TYPE;
        ('szSerialNumber', c_char * 32),  # 无线设备序列号;Wireless Device SN;
        ('nTaskID', C_UINT),  # 任务ID;Task ID;
        ('szRoomNo', c_char * 64),  # 智能锁房间号;Room number of intelligent lock;
        ('nMaxFingerprints', C_DWORD),  # 信息数量:为0时表示不支持信息;information number: 0 indicates unsupported informations;
        ('nMaxCards', C_DWORD),  # 卡片数量:为0时表示不支持卡片;cards number: 0 indicates unsupported cards;
        ('nMaxPwd', C_DWORD),  # 密码数量:为0时表示不支持密码;password number: 0 indicates unsupported password;
        ('szRandSalt', c_char * 128),  # 智能门锁复杂盐值;Salt Value;
    ]

class NET_CTRL_LOWRATEWPAN_ADD(Structure):
    """
    增加对码信息
    add code info
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('stuCodeIDInfo', NET_CODEID_INFO),  # 对码数据;code info data;
    ]

class NET_CTRL_LOWRATEWPAN_REMOVE(Structure):
    """
    删除指定无线设备
    CLIENT_ControlDevice 接口的 CTRL_LOWRATEWPAN_REMOVE命令参数
    Delete specific wireless device
    CLIENT_ControlDevice port CTRL_LOWRATEWPAN_REMOVE command parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('nWirelessId', C_TP_U64),  # 无线设备ID;Wireless device ID;
        ('szSerialNumber', c_char * 32),  # 无线设备序列号 无线对码后续采用序列号的方式;Wireless device SN;
    ]

class NET_CTRL_LOWRATEWPAN_REMOVEALL(Structure):
    """
    删除全部无线设备
    CLIENT_ControlDevice接口的 CTRL_LOWRATEWPAN_REMOVEALL命令参数
    Delete all wireless device
    CLIENT_ControlDevice port CTRL_LOWRATEWPAN_REMOVEALL command parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),
    ]

class NET_IN_ATTACH_LOWRATEWPAN(Structure):
    """
    CLIENT_AttachLowRateWPAN()输入参数
    CLIENT_AttachLowRateWPAN() input parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),
        ('cbAttachLowRateWPANCB', CB_FUNCTYPE(None, C_LLONG, C_LLONG, POINTER(NET_CODEID_INFO), C_ENUM, C_LDWORD)),  # 对码数据回调;Code data call;
        ('dwUser', C_LDWORD),  # 用户数据;User Data;
    ]

class NET_OUT_ATTACH_LOWRATEWPAN(Structure):
    """
    CLIENT_AttachLowRateWPAN()输出参数
    CLIENT_AttachLowRateWPAN() output parameter
    """
    _fields_ = [
        ('dwSize', C_DWORD),
    ]

class NET_CFG_DISABLE_BEEP_LINKAGE_INFO(Structure):
    """
    防蜂鸣联动项使能配置信息, 对应 NET_EM_CFG_DISABLE_BEEP_LINKAGE
    Enable configuration information of beep linkage item, corresponding to NET_EM_CFG_DISABLE_BEEP_LINKAGE
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwsize;
        ('bEnable', C_BOOL),  # 开启撤防联动项功能总开关（DisableLinkage）后，是否撤防蜂鸣联动项;Whether to disarm beep linkage;
        ('szName', c_char * 32),  # 联动项配置名;Linkage item configuration name;
    ]

class NET_IN_TRANSMIT_CMD(Structure):
    """
    CLIENT_TransmitCmd 接口输入参数
    CLIENT_TransmitCmd input params
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
        ('nChannel', c_int),  # 通道号, 范围 0~设备通道数;Channel;
        ('nHannel', c_int),  # 协议类型，0 : 整形数组;Protocol type, 0: integer array;
        ('bReply', C_BOOL),  # 此命令需要接收回复;This command needs to receive a reply;
        ('nMessageCount', c_int),  # 命令字节数量;Command Count;
        ('pMessage', POINTER(c_int)),  # 具体命令，是一个数组，每个元素为每个字节的整形值，使用DVR同前端交互协议,需要用户分配内存空间;The specific command is an array, each element is an integer value of each byte, and the user needs to allocate memory space;
    ]

class NET_OUT_TRANSMIT_CMD(Structure):
    """
    CLIENT_TransmitCmd 接口输出参数
    CLIENT_TransmitCmd output params
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
        ('nChannel', c_int),  # 通道号, 范围 0~设备通道数;Channel;
        ('nHannel', c_int),  # 协议类型，0 : 整形数组;Protocol type, 0: integer array;
        ('nRetMessageCount', c_int),  # 返回命令长度;Return command length;
        ('nMaxMessageCount', c_int),  # 用户填写,为pMessage指针所指的数组元素数量;The number of array elements indicated by the pMessage pointer filled by the user;
        ('pMessage', POINTER(c_int)),  # 返回值，是一个数组，每个元素为每个字节的整形值，需要用户分配内存空间;The return value is an array. Each element is an integer value of each byte. The user needs to allocate memory space;
    ]

class NET_AREAS_INFO(Structure):
    """
    Area状态信息
    Areas status infomation
    """
    _fields_ = [
        ('szMode', c_char * 32),  # 子系统当前的布撤防模式"T" : Total布防/外出布防模式"p1" : Partial1布防/在家布防模式"p2" : Partial2布防/自定义模式"P" : Partial1+2布防"t" : 强制布防"D" : 撤防;
                              # Current deployment and removal mode of the subsystem"T": Total deployment/outbound deployment mode"P1": Partial1 defense/home defense mode"P2": Partial2 deployment/custom mode"P": Partial1+2 defense"T": forced deployment"D": defense withdrawal;
        ('szReserved', c_char * 32),  # 保留字节;Reserved;
    ]

class NET_PREVENTION_OF_ARMING_INFO(Structure):
    """
    禁止布防的条件，当其中一个或多个状态且对应项的值为true时，报警主机应能禁止布防
    Conditions for Prohibiting Deployment
    """
    _fields_ = [
        ('bIntrusionDetectorActivated', C_BOOL),  # 入侵探测器处于激活状态;Intrusion detector activated;
        ('bHoldupDeviceActivated', C_BOOL),  # 紧急报警装置处于激活状态;Holdup device activated;
        ('bMovementDetectorMasked', C_BOOL),  # 移动目标探测器被遮挡;Movement detector masked;
        ('bMovementDetectorRangeReduction', C_BOOL),  # 移动目标探测器的探测距离明显减小;Movement detector range reduction;
        ('bIntrusionDetectorFault', C_BOOL),  # 入侵探测器故障;Intrusion detector fault;
        ('bTamperCondition', C_BOOL),  # 防拆报警;Tamper condition;
        ('bInterconnectionFaults', C_BOOL),  # 互连通信故障;Interconnection faults;
        ('bPrimePowerSourceFault', C_BOOL),  # 主电源故障;Prime power source fault;
        ('bAlternativePowerSourceFault', C_BOOL),  # 备用电源故障;Alternative power source fault;
        ('bAlarmTransmissionSystemFault', C_BOOL),  # 报警传输系统故障;Alarm transmission systemFault;
        ('bWarningDeviceFault', C_BOOL),  # 告警装置故障;Warning device fault;
        ('szReserved', c_char * 252),  # 保留字节;Reserved;
    ]

class NET_SYSTEM_STATUS_CHECK_INFO(Structure):
    """
    系统检测状态
    System status check
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 检测使能;Enable;
        ('stuPreventionOfArming', NET_PREVENTION_OF_ARMING_INFO),  # 禁止布防的条件，当其中一个或多个状态且对应项的值为true时，报警主机应能禁止布防;Conditions for Prohibiting Deployment;
        ('szReserved', c_char * 512),  # 保留字节;Reserved;
    ]

class NET_CFG_AREA_ARM_MODE_INFO(Structure):
    """
    Area布撤防配置, 对应 NET_EM_CFG_AREA_ARM_MODE
    Area deployment and removal configuration, corresponding toNET_EM_CFG_AREA_ARM_MODE
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
        ('nAreasNum', c_int),  # Area状态信息数量，数组最大64个;number of Areas status infomation list;
        ('stuAreas', NET_AREAS_INFO * 64),  # Area状态信息数组;Areas status infomation list;
        ('stuSystemStatusCheck', NET_SYSTEM_STATUS_CHECK_INFO),  # 系统检测状态;System status check;
    ]

class NET_IN_MANUAL_TEST(Structure):
    """
    CLIENT_ManualTest 接口输入参数
    CLIENT_ManualTest input params
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
        ('dwTestID', C_DWORD),  # 测试ID，每次下发的测试ID不一样;TestID,the test ID issued each time is different;
        ('nChannel', C_UINT),  # 测试的通道号，可以对应某一个要测试的SIA服务器;Channel ID;
    ]

class NET_OUT_MANUAL_TEST(Structure):
    """
    CLIENT_ManualTest 接口输出参数
    CLIENT_ManualTest output params
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
        ('nTestResult', c_int),  # 结果 1：测试成功，结果同步返回 2：发送测试请求成功，结果异步返回 3：测试失败;Result 1: The test is successful, the result is returned synchronously 2: The test request is sent successfully, the result is returned asynchronously 3: The test failed;
    ]

class NET_ALARM_USER_ONECLICKARMING(Structure):
    """
    一键布防配置
    One-key deployment configuration
    """
    _fields_ = [
        ('bEnable', C_BOOL),  # 一键布防使能;One key arming enable;
        ('emFunction', C_ENUM),  # 布防功能 Refer: EM_ALARM_ONECLICKARMING_FUNCTION;Arming function Refer: EM_ALARM_ONECLICKARMING_FUNCTION;
        ('emTriggerOption', C_ENUM),  # 触发类型 Refer: EM_ALARM_ONECLICKARMING_TRIGGEROPTION;trigger type Refer: EM_ALARM_ONECLICKARMING_TRIGGEROPTION;
        ('emArmProfile', C_ENUM),  # 一键布防类型 Refer: EM_A_NET_EM_SCENE_MODE;Deployment scenario mode Refer: EM_A_NET_EM_SCENE_MODE;
        ('emArmMode', C_ENUM),  # 布撤防模式 Refer: EM_ARM_TYPE;arm type Refer: EM_ARM_TYPE;
        ('byReserved', C_BYTE * 256),  # 保留字节;reserved;
    ]

class NET_ALARM_USER_EXTERN(Structure):
    """
    报警产品本地用户扩展信息
    Alarm product local user extension information
    """
    _fields_ = [
        ('szDuressPassword', c_char * 64),  # 胁迫密码;Duress password;
        ('szCard', c_char * 64 * 32),  # 关联卡片;Associated card;
        ('nCardNum', c_int),  # 关联卡片数量;number of associated card;
        ('szReserved', c_char * 1020),  # 保留字节;Reserved;
    ]

class NET_ALARM_USER(Structure):
    """
    报警产品本地用户信息
    Local user information of alarm product
    """
    _fields_ = [
        ('szID', c_char * 32),  # 用户编号;User ID;
        ('emUserStatus', C_ENUM),  # 用户状态 Refer: EM_GETUSERINFOBYCONDITION_USER_STATUS;User status Refer: EM_GETUSERINFOBYCONDITION_USER_STATUS;
        ('szName', c_char * 64),  # 用户名;username;
        ('szPassword', c_char * 64),  # 密码;password;
        ('nAuthorityListNum', c_int),  # 用户的权限列表个数;The number of user authorization lists;
        ('emAuthorityList', C_ENUM * 32),  # 用户的权限列表 Refer: EM_ALARM_USERAUTHORITY;User's authorization list Refer: EM_ALARM_USERAUTHORITY;
        ('emGroup', C_ENUM),  # 用户所在组 Refer: EM_ALARM_USER_GROUP;user's group Refer: EM_ALARM_USER_GROUP;
        ('bReserved', C_BOOL),  # 是否为保留用户，保留用户不可删除;Whether it is a reserved user, the reserved user cannot be deleted;
        ('emUserType', C_ENUM),  # 用户类型 Refer: EM_GETUSERINFOBYCONDITION_USER_TYPE;User type Refer: EM_GETUSERINFOBYCONDITION_USER_TYPE;
        ('nInterval', C_UINT),  # 相同短信时间间隔，间隔时间内若有连续相同的报告触发，则不上传。（当用户类型为Key时有效）单位：秒;The same message time interval, if the same report is triggered continuously within the interval, it will not be uploaded. (Valid when the user type is Key) Unit: seconds;
        ('stuAccessAllowTimeStart', NET_TIME),  # 允许访问的时间 开始时间;Allowed access time Start time;
        ('stuAccessAllowTimeEnd', NET_TIME),  # 允许访问的时间 结束时间;Allowed access time End time;
        ('szMemo', c_char * 32),  # 用户备注信息;User remarks information;
        ('nSubSystemNum', c_int),  # 关联的子系统对应子系统号的个数;The number of associated subsystem corresponding to the subsystem number;
        ('nSubSystems', c_int * 64),  # 关联的子系统，对应子系统号，用户只能操作其关联的子系统;Associated subsystem, corresponding to the subsystem number, the user can only operate its associated subsystem;
        ('nZoneNum', c_int),  # 关联防区的个数;Number of associated zone;
        ('nZones', c_int * 256),  # 关联防区，当emUserType=EM_GETUSERINFOBYCONDITION_USER_TYPE_KEY时用来关联Key防区。不同的Key防区可以关联不同的Key用户。;Associate the zone, when emUserType=EM_GETUSERINFOBYCONDITION_USER_TYPE_KEY, it is used to associate the Key zone. Different Key defense zones can be associated with different Key users.;
        ('stuOneClickArming', NET_ALARM_USER_ONECLICKARMING),  # 一键布防配置;One-click arming configuration;
        ('pstuAlarmUserExtern', POINTER(NET_ALARM_USER_EXTERN)),  # 用户信息扩展数据，需要用户申请内存;User information extended data requires user to apply for memory;
        ('byReserved', C_BYTE * (256-sizeof(c_void_p))),  # 保留字节;reserved;
    ]

class NET_IN_ADD_ALARM_USER(Structure):
    """
    CLIENT_AddAlarmUser 接口输入参数
    CLIENT_AddAlarmUser input params
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
        ('stuAlarmUser', NET_ALARM_USER),  # 添加的用户信息;User information;
    ]

class NET_OUT_ADD_ALARM_USER(Structure):
    """
    CLIENT_AddAlarmUser 接口输出参数
    CLIENT_AddAlarmUser output params
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
    ]

class NET_IN_MODIFY_ALARM_USER(Structure):
    """
    CLIENT_ModifyAlarmUser 接口输入参数
    CLIENT_ModifyAlarmUser input params
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
        ('szUserID', c_char * 64),  # 用户ID，用户唯一标识;User ID;
        ('stuAlarmUser', NET_ALARM_USER),  # 修改的用户信息;User information;
    ]

class NET_OUT_MODIFY_ALARM_USER(Structure):
    """
    CLIENT_ModifyAlarmUser 接口输出参数
    CLIENT_ModifyAlarmUser output params
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
    ]

class NET_IN_MODIFY_ALARM_USER_PASSWORD(Structure):
    """
    CLIENT_ModifyAlarmUserPassword 接口输入参数
    CLIENT_ModifyAlarmUserPassword input params
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
        ('szUserID', c_char * 64),  # 用户ID，用户唯一标识;User ID;
        ('szOldPassword', c_char * 64),  # 旧密码;Old password;
        ('szNewPassword', c_char * 64),  # 新密码;New password;
    ]

class NET_OUT_MODIFY_ALARM_USER_PASSWORD(Structure):
    """
    CLIENT_ModifyAlarmUserPassword 接口输出参数
    CLIENT_ModifyAlarmUserPassword output params
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
    ]

class NET_IN_DELETE_ALARM_USER(Structure):
    """
    CLIENT_DeleteAlarmUser 接口输入参数
    CLIENT_DeleteAlarmUser input params
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
        ('szUserID', c_char * 64),  # 用户ID，用户唯一标识;User ID;
    ]

class NET_OUT_DELETE_ALARM_USER(Structure):
    """
    CLIENT_DeleteAlarmUser 接口输出参数
    CLIENT_DeleteAlarmUser output params
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;dwSize;
    ]

class NET_A_DEVTIME(Structure):
    """
    日志信息里的时间定义
    The time definition in the log information
    """
    _fields_ = [
        ('date', C_DWORD),
    ]

class NET_A_DEVICE_LOG_ITEM(Structure):
    """
    日志信息,对应接口CLIENT_QueryDeviceLog接口
    Log information. Corresponding to CLIENT_QueryDeviceLog
    """
    _fields_ = [
        ('nLogType', c_int),  # 日志类型;Log type;
        ('stuOperateTime', NET_A_DEVTIME),  # 日期;Date;
        ('szOperator', c_char * 16),  # 操作者;Operator;
        ('bReserved', C_BYTE * 3),
        ('bUnionType', C_BYTE),  # union结构类型,0:szLogContext;1:stuOldLog;union structure type,0:szLogContext;1:stuOldLog;
        ('szLogContext', c_char * 64),  # 日志备注信息;Log content;
        ('reserved', c_char * 16),
    ]

class NET_A_DEVICE_LOG_ITEM_EX(Structure):
    """
    新日志信息结构,对应接口CLIENT_QueryDeviceLog接口
    new Log information. Corresponding to CLIENT_QueryDeviceLog
    """
    _fields_ = [
        ('nLogType', c_int),  # 日志类型;Log type;
        ('stuOperateTime', NET_A_DEVTIME),  # 日期;Date;
        ('szOperator', c_char * 16),  # 操作者;Operator;
        ('bReserved', C_BYTE * 3),
        ('bUnionType', C_BYTE),  # union结构类型,0:szLogContext;1:stuOldLog;union structure type,0:szLogContext;1:stuOldLog;
        ('szLogContext', c_char * 64),  # 日志备注信息;Log content;
        ('szOperation', c_char * 32),  # 具体的操作内容;Detail operation;
        ('szDetailContext', c_char * 4096),  # 详细日志信息描述;DetailContext;
    ]

class NET_A_DEV_EVENT_CLASSROOM_BEHAVIOR_INFO(Structure):
    """
    事件类型 CLASSROOM_BEHAVIOR (课堂行为分析事件) 对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_CLASSROOM_BEHAVIOR (classroom dehavior detect)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('nAction', c_int),  # 0:脉冲 1:开始 2:停止;Event action, 0: Pulse, 1: Start, 2: Stop;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Timestamp (in milliseconds);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Time for the event occurred;
        ('nEventID', C_UINT),  # 事件ID;Event ID;
        ('stuFileInfo', SDK_EVENT_FILE_INFO),  # 事件对应文件信息;Event corresponding to file information;
        ('emClassType', C_ENUM),  # 智能事件所属大类 Refer: EM_CLASS_TYPE;Class type Refer: EM_CLASS_TYPE;
        ('nRuleID', C_UINT),  # 智能事件规则编号，用于标示哪个规则触发的事件;Rule ID;
        ('nObjectID', C_UINT),  # 物体ID;Object ID;
        ('nSequence', C_UINT),  # 帧序号;Sequence;
        ('emClassroomAction', C_ENUM),  # 课堂行为动作 Refer: EM_CLASSROOM_ACTION;Classroom action Refer: EM_CLASSROOM_ACTION;
        ('stuDetectRegion', SDK_POINT * 20),  # 规则检测区域;The point list of rule detect region;
        ('nDetectRegionNum', c_int),  # 规则检测区域顶点数;The point number of rule detect region;
        ('nPresetID', C_UINT),  # 事件触发的预置点号;Preset ID;
        ('szPresetName', c_char * 64),  # 事件触发的预置点名称;Preset name;
        ('szSerialUUID', c_char * 22),  # 智能物体全局唯一物体标识格式如下：前2位%d%d:01-视频片段,02-图片,03-文件,99-其他;中间14位YYYYMMDDhhmmss:年月日时分秒;后5位%u%u%u%u%u：物体ID，如00001;Serial UUIDThe format is as follows:Front 2:%d%d:01-video,02-picture,03-file,99-other;Middle 14:YYYYMMDDhhmmss:year,month,day,hour,minute,second;Last 5:%u%u%u%u%u:object ID,as 00001;
        ('byReserved1', C_BYTE * 2),  # 用于字节对齐;For align;
        ('stuBoundingBox', SDK_RECT),  # 包围盒;Bounding box;
        ('stuSceneImage', NET_INTELLIGENCE_IMAGE_INFO),  # 底图信息;Scene image;
        ('stuFaceImage', NET_INTELLIGENCE_IMAGE_INFO),  # 小图信息;image;
        ('stuFaceAttributes', NET_FACE_ATTRIBUTE_EX),  # 属性;attributes;
        ('stuImageInfo', NET_IMAGE_INFO_EX2 * 32),  # 图片信息数组;image information array;
        ('nImageInfoNum', c_int),  # 图片信息个数;Number of image information;
        ('byReserved', c_char * 1024),  # 预留字节;Reserved;
    ]

class NET_USERMANAGER_IMAGE_INFO(Structure):
    """
    用户信息图片信息
    usermanager image info
    """
    _fields_ = [
        ('nOffset', C_UINT),  # 在二进制数据块中的偏移,单位:字节;offset in binary data,unit:byte;
        ('nLength', C_UINT),  # 图片大小,单位:字节;Image length,unit:byte;
        ('nWidth', c_uint16),  # 图片宽度;image width;
        ('nHeight', c_uint16),  # 图片高度;image height;
        ('emImageType', C_ENUM),  # 图片类型 Refer: EM_USERMANAGER_IMAGE_TYPE;image type Refer: EM_USERMANAGER_IMAGE_TYPE;
        ('szReserved', c_char * 64),  # 保留字节;reserved bytes;
    ]

class NET_DEV_EVENT_USERMANAGER_FOR_TWSDK_INFO(Structure):
    """
    事件类型 EVENT_IVS_USERMANAGER_FOR_TWSDK (用户信息上报事件)对应的数据块描述信息
    EVENT_IVS_USERMANAGER_FOR_TWSDK Specifies the description of the data block corresponding to User information reporting event
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;ChannelID;
        ('nAction', c_int),  # 0:脉冲;0: pulse;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间;The time of the event;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 扩展协议字段;Extended protocol field;
        ('szUserID', c_char * 9),  # 用户ID;UserID;
        ('szReserved1', c_char * 7),  # 字节对齐;byte alignment;
        ('szUserName', c_char * 64),  # 用户名;UserName;
        ('nUserType', c_int),  # 用户类型;Byte aligned user type;
        ('nUseTime', c_int),  # 使用次数;Use time;
        ('nAuthority', c_int),  # 用户权限 0:未知 1: 管理员 2: 普通用户;User permission 0: unknown 1: administrator 2: ordinary user;
        ('nTimeSectionNum', c_int),  # 有效的的时间段数目;Number of nTimeSections;
        ('nTimeSections', C_UINT * 64),  # 时段;TimeSections;
        ('stuValidTo', NET_TIME),  # 有效期;term of validity;
        ('nSpecialDaysSchedule', C_UINT * 64),  # 假日计划;Special Days Schedule;
        ('nSpecialDaysScheduleNum', c_int),  # 假日计划表示数量;Number of Special Days Schedule;
        ('nType', c_int),  # 消息类型 0: 未知 1: 人员新增消息 2: 人员修改消息 3:人员删除消息（删除时仅UserID有效）;Message type 0: Unknown 1: New message for personnel 2: Modify message for personnel 3: Delete message for personnel (only UserID is valid when deleting);
        ('szPassword', c_char * 9),  # 密码;Password;
        ('szReserved2', c_char * 7),  # 字节对齐;byte alignment;
        ('szFaceList', c_char * 5 * 2048),  # 特征值;target list;
        ('nFaceListNum', c_int),  # 特征值数量;Number of target list;
        ('nCardListNum', c_int),  # 卡片数量;Number of cardlist;
        ('szCardList', c_char * 5 * 32),  # 卡片;cardlist;
        ('szFingerList', c_char * 5 * 256),  # 信息;FingerList;
        ('nFingerListNum', c_int),  # 信息数量;Number of fingerlist;
        ('bDelAllUser', C_BOOL),  # 是否删除所有用户（true:删除所有用户数据，其余字段无效）;Whether to delete all users (true: delete all user data, other fields are invalid);
        ('stuValidFrom', NET_TIME),  # 有效期开始时间;Valid from;
        ('szSN', c_char * 32),  # 设备序列号;sn;
        ('nUserCount', C_UINT),  # 用户总数量;user count;
        ('nFingerCount', C_UINT),  # 信息总数量;finger count;
        ('nFaceCount', C_UINT),  # 目标总数量;target count;
        ('nCardCount', C_UINT),  # 卡片总数量;card count;
        ('stuImageInfo', NET_USERMANAGER_IMAGE_INFO * 5),  # 用户信息图片信息;user image info;
        ('nImageInfoCount', c_int),  # 用户信息图片信息个数;user image info count;
        ('szReserved', c_char * 572),  # 预留字节;Reserved;
    ]


class NET_DEV_EVENT_TIMECHANGE_FOR_TWSDK_INFO(Structure):
    """
    事件类型 EVENT_IVS_TIMECHANGE_FOR_TWSDK (系统时间被修改报警事件)对应的数据块描述信息
    Description of the data block corresponding to the event EVENT_IVS_TIMECHANGE_FOR_TWSDK (System time modified alarm event)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('nAction', c_int),  # 0:脉冲,1:开始, 2:停止;0: pulse,1: start, 2: stop;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 扩展协议字段;Extend the protocol field;
        ('stuBeforeModifyTime', NET_TIME),  # 修改前时间;Before Modify Time;
        ('stuModifiedTime', NET_TIME),  # 修改后时间;Modified Time;
        ('szSN', c_char * 32),  # 设备序列号;Device serial number;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间;Time of the event;
        ('szReserved', c_char * 1020),  # 预留字节;Reserved bytes;
    ]

class NET_IN_GET_VERSION(Structure):
    """
    CLIENT_IntervideoManagerGetVersion接口入参
    CLIENT_IntervideoManagerGetVersion interface input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Struct size;
        ('emProtocolName', C_ENUM),  # 协议名称 Refer: EM_PROTOCOL_NAME;Protocol name Refer: EM_PROTOCOL_NAME;
    ]

class NET_OUT_GET_VERSION(Structure):
    """
    CLIENT_IntervideoManagerGetVersion接口出参
    CLIENT_IntervideoManagerGetVersion interface output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 结构体大小;Struct size;
        ('szGB28181Version', c_char * 16),  # GB28181协议版本;GB28181 version;
    ]

class NET_A_EVENT_FILE_INFO(Structure):
    """
    事件对应文件信息
    event file info
    """
    _fields_ = [
        ('bCount', C_BYTE),  # 当前文件所在文件组中的文件总数;the file count in the current file's group;
        ('bIndex', C_BYTE),  # 当前文件在文件组中的文件编号(编号1开始);the index of the file in the group;
        ('bFileTag', C_BYTE),  # 文件标签, EM_EVENT_FILETAG;file tag, see the enum struct EM_EVENT_FILETAG;
        ('bFileType', C_BYTE),  # 文件类型,0-普通 1-合成 2-抠图;file type,0-normal 1-compose 2-cut picture;
        ('stuFileTime', NET_TIME_EX),  # 文件时间;file time;
        ('nGroupId', C_DWORD),  # 同一组抓拍文件的唯一标识;the only id of one group file;
    ]

class NET_A_RESOLUTION_INFO(Structure):
    """
    图片分辨率
    pic resolution
    """
    _fields_ = [
        ('snWidth', c_uint16),  # 宽;width;
        ('snHight', c_uint16),  # 高;hight;
    ]

class NET_A_EVENT_INTELLI_COMM_INFO(Structure):
    """
    智能报警事件公共信息
    intelli event comm info
    """
    _fields_ = [
        ('emClassType', C_ENUM),  # 智能事件所属大类 Refer: EM_CLASS_TYPE;class type Refer: EM_CLASS_TYPE;
        ('nPresetID', c_int),  # 该事件触发的预置点，取值范围为0~255，大于0表示在此预置点时有效。;Preset ID, value range is 0~255 and when the value is greater than 0 is valied;
        ('bReserved', C_BYTE * 124),  # 保留字节,留待扩展.;reserved;
    ]

class NET_A_SIG_CARWAY_INFO_EX(Structure):
    """
    车检器冗余信息
    Vehicle detector redundancy info
    """
    _fields_ = [
        ('byRedundance', C_BYTE * 8),  # 由车检器产生抓拍信号冗余信息;The vehicle detector generates the snap signal redundancy info;
        ('bReserved', C_BYTE * 120),  # 保留字段;Reserved field;
    ]

class NET_A_DEV_EVENT_TRAFFIC_PARKING_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_PARKING(交通违章停车事件)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFIC_PARKING's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('nRuleID', C_UINT),  # 规则编号,用于标示哪个规则触发的事件，缺省时默认为0;Rule ID, used to indicate which rule triggers the event. The default value is 0;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;have being detected object;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('nLane', c_int),  # 对应车道号;Corresponding Lane number;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('reserved', C_BYTE * 2),  # 保留字节;Reserved bytes;
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('stuStartParkingTime', NET_TIME_EX),  # 开始停车时间;the time of starting parking;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束(bEventAction=2时此参数有效);snap index: such as 3,2,1,1 means the last one,0 means there has some exception and snap stop(this param work when bEventAction=2);
        ('nAlarmIntervalTime', c_int),  # 报警时间间隔,单位:秒。(此事件为连续性事件,在收到第一个此事件之后,若在超过间隔时间后未收到此事件的后续事件,则认为此事件异常结束了);interval time of alarm(s) (this is a continuous event,if the interval time of recieving next event go beyond this param, we can judge that this event is over with exception);
        ('nParkingAllowedTime', c_int),  # 允许停车时长,单位：秒。;the time of legal parking;
        ('nDetectRegionNum', c_int),  # 规则检测区域顶点数;detect region point number;
        ('DetectRegion', NET_POINT * 20),  # 规则检测区域;detect region point number;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESEED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('bIsExistAlarmRecord', C_BOOL),  # rue:有对应的报警录像; false:无对应的报警录像;true:corresponding alarm recording; false: no corresponding alarm recording;
        ('dwAlarmRecordSize', C_DWORD),  # 录像大小;Video size;
        ('szAlarmRecordPath', c_char * 256),  # 录像路径;Video Path;
        ('szFTPPath', c_char * 256),  # FTP路径;FTP path;
        ('stuIntelliCommInfo', NET_A_EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info;
        ('byPreAlarm', C_BYTE),  # 是否为违章预警图片,0 违章停车事件1 预警事件(预警触发后一定时间，车辆还没有离开，才判定为违章)由于此字段会导致事件含义改变，必须和在平台识别预警事件后，才能有此字段,;weather is PreAlarm event,0 :traffic parking event,1 :preAlarm event;
        ('bReserved2', C_BYTE * 3),  # 保留字节,留待扩展.;Reserved;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息;GPS info ,use in mobile DVR/NVR;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX2)),  # 图片信息数组;Image information array;
        ('nImageInfoNum', c_int),  # 图片信息个数;Number of picture information;
        ('nPresetID', c_int),  # 预置点编号,从1开始;Preset point number, starting from 1;
        ('szSN', c_char * 32),  # 设备SN号;Device SN number;
        ('emViolationSnapSource', C_ENUM),  # 抓拍触发源: EM_VIOLATION_SNAP_SOURCE;Snap trigger source: EM_VIOLATION_SNAP_SOURCE;
        ('bReserved', C_BYTE * 180),  # 保留字节,留待扩展.;Reserved;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('stuNonMotor', VA_OBJECT_NONMOTOR),  # 非机动车对象;NonMotor information;
        ('bHasNonMotor', C_BOOL),  # 是否有非机动车对象;has NonMotor information?;
        ('nParkingDuration', C_UINT),  # 违停持续时间，单位：秒, 0表示无意义;Parking Duration;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_EVENT_TRAFFIC_CAR_PART_INFO(Structure):
    """
    交通车辆部分信息
    part of traffic car info
    """
    _fields_ = [
        ('szMachineName', c_char * 128),  # 本地或远程设备名称 来源于普通配置General.MachineName;Local or remote device name;
        ('szRoadwayNo', c_char * 32),  # 道路编号;road way number;
        ('szPlateNumber', c_char * 32),  # 车牌号码;plate number;
        ('szCategory', c_char * 32),  # 车辆子类型;category;
        ('bReserved', C_BYTE * 288),  # 保留字节;reserved;
    ]

class NET_A_EVENT_VEHICLE_INFO(Structure):
    """
    行人信息
    Pedestrain info
    """
    _fields_ = [
        ('szCategory', c_char * 64),  # 物体类型，Passerby表示行人;Object type,Passerby mean pedestrain;
        ('byReserved', C_BYTE * 64),  # 预留字节;Reserved;
    ]

    
class NET_A_DEV_EVENT_TRAFFIC_PEDESTRAIN_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_PEDESTRAIN(交通行人事件)对应数据块描述信息
    Event type EVENT_IVS_TRAFFIC_PEDESTRAIN(pedestrain)corresponding data block description info
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 8),  # 字节对齐;byte alignment;
        ('PTS', C_DWORD),  # 时间戳(单位是毫秒);Time stamp(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occurred time;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;The corresponding file info of the event;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),0位:"*",1位:"Timing",2位:"Manual",3位:"Marked",4位:"Event",5位:"Mosaic",6位:"Cutout";Snap flag(by bit)0 bit:"*",1 bit:"Timing",2 bit:"Manual",3 bit:"Marked",4 bit:"Event",5 bit:"Mosaic",6 bit:"Cutout";
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event operation.0=pulse event,1=begin of the durative event,2=end of the durative event;;
        ('bReserved2', C_BYTE * 2),  
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('nLane', c_int),  # 对应车道号;Corresponding lane No.;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;Detected object;
        ('stuIntelliCommInfo', NET_A_EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info;
        ('stuTrafficCarPartInfo', NET_A_EVENT_TRAFFIC_CAR_PART_INFO),  # 交通车辆部分信息;part of traffic car info;
        ('stuVehicle', NET_A_EVENT_VEHICLE_INFO),  # 行人信息;pedestrain info;
        ('bReserved', C_BYTE * 252),  # 保留字节;reserved;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
    ]

class NET_A_DEV_EVENT_TRAFFIC_NONMOTOR_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_NONMOTOR (交通非机动车事件检测)对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_TRAFFIC_NONMOTOR
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel;
        ('nAction', c_int),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action 0:pulse 1:start 2:stop;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('PTS', c_double),  # 时间戳(单位:毫秒);Time stamp(unit:ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occur time;
        ('nEventID', C_UINT),  # 事件ID;Event ID;
        ('nRuleId', C_UINT),  # 智能事件规则编号;Event RuleID;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;FileInfo;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的车牌信息;Plate number info;
        ('emTriggerType', C_ENUM),  # 触发类型 Refer: EM_TRIGGER_TYPE;TriggerType Refer: EM_TRIGGER_TYPE;
        ('stuCommInfo', EVENT_COMM_INFO),  # 公共信息;Common Info;
        ('bNonMotorInfo', C_BOOL),  # 是否有非机动车信息;stuNonMotor if valid;
        ('stuNonMotor', VA_OBJECT_NONMOTOR),  # 非机动车信息;NonMotor info;
        ('bReserved', C_BYTE * 1024),  # 保留字节;Reserved;
    ]

class NET_A_DEV_EVENT_TRAFFICJAM_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFICJAM(交通拥堵事件)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFICJAM's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('nLane', c_int),  # 对应车道号;Corresponding Lane number;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('bJamLenght', C_BYTE),  # 表示拥堵长度(总车道长度百分比）0-100;Mean congestion length (percentage of total lane length) 0-100;
        ('reserved', C_BYTE),  # 保留字节;reserved;
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('stuStartJamTime', NET_TIME_EX),  # 开始停车时间;the time of starting jam;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束(bEventAction=2时此参数有效);snap index: such as 3,2,1,1 means the last one,0 means there has some exception and snap stop(this param work when bEventAction=2);
        ('nAlarmIntervalTime', c_int),  # 报警时间间隔,单位:秒。(此事件为连续性事件,在收到第一个此事件之后,若在超过间隔时间后未收到此事件的后续事件,则认为此事件异常结束了);interval time of alarm(s).(this is a continuous event,if the interval time of recieving next event go beyond this param, we can judge that this event is over with exception);
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('nJamRealLength', c_int),  # 表实际的拥堵长度,单位米;means actual jam length, unit is meter;
        ('stuExtensionInfo', NET_EXTENSION_INFO),  # 扩展信息;Extension info;
        ('bJamRegionFlagValid', C_BOOL),  # 区域拥堵标志是否有效;Whether the zone congestion sign is effective;
        ('nJamRegionFlag', C_UINT),  # 区域拥堵标志 0-车道拥堵 1-区域拥堵;Zone congestion sign 0- Lane congestion 1- Zone congestion;
        ('bReserved', C_BYTE * 868),  # 保留字节,留待扩展.;Reserved;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
    ]

class NET_A_DEV_EVENT_TRAFFIC_CROSSLANE_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_CROSSLANE(交通违章-违章变道)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFIC_CROSSLANE's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;have being detected object;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('nLane', c_int),  # 对应车道号;Corresponding Lane number;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),  
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('nSpeed', c_int),  # 车辆实际速度,km/h;speed,km/h;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('stuIntelliCommInfo', NET_A_EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息;GPS info ,use in mobile DVR/NVR;
        ('bReserved', C_BYTE * 836),  # 保留字节,留待扩展.留待扩展.;Reserved bytes.;
        ('stuTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;traffic vehicle info;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_DEV_EVENT_TRAFFIC_RETROGRADE_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_RETROGRADE(交通-逆行事件)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFIC_RETROGRADE's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('nRuleID', C_UINT),  # 规则编号,用于标示哪个规则触发的事件，缺省时默认为0;Rule ID, used to indicate which rule triggers the event. The default value is 0;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('nLane', c_int),  # 对应车道号;Corresponding Lane number;
        ('stuObject', NET_A_MSG_OBJECT),  # 车牌信息;have being detected object;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;snap index: such as 3,2,1,1 means the last one,0 means there has some exception and snap stop;
        ('nSpeed', c_int),  # 车辆实际速度,Km/h;speed, km/h;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),  
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('bIsExistAlarmRecord', C_BOOL),  # rue:有对应的报警录像; false:无对应的报警录像;a corresponding alarm recording; false: no corresponding alarm recording;
        ('dwAlarmRecordSize', C_DWORD),  # 录像大小;Video size;
        ('szAlarmRecordPath', c_char * 256),  # 录像路径;Video Path;
        ('stuIntelliCommInfo', NET_A_EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息;GPS info ,use in mobile DVR/NVR;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX3)),  # 图片信息数组;Picture information;
        ('nImageInfoNum', c_int),  # 图片信息个数;Picture number;
        ('bReserved', C_BYTE * (480-sizeof(c_void_p))),  # 保留字节;Reserved bytes;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('nDetectNum', c_int),  # 规则检测区域顶点数;Acme amount of the rule detect zone;
        ('DetectRegion', NET_POINT * 20),  # 规则检测区域;Rule detect zone;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('bHasNonMotor', C_BOOL),  # 是否有非机动车对象;has NonMotor information?;
        ('stuNonMotor', VA_OBJECT_NONMOTOR),  # 非机动车对象;NonMotor information;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_DEV_EVENT_IVS_TRAFFIC_BACKING_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_BACKING(违章倒车事件)对应的数据块描述信息
    Event type EVENT_IVS_TRAFFIC_BACKING(traffic backing)corresponding data block description info
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Time stamp(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occurred time;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;Detected object;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;Vehicle body info;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;The corresponding file info of the event;
        ('nLane', c_int),  # 对应车道号;Corresponding lane No.;
        ('nSequence', c_int),  # 抓拍序号,如3-2-1/0,1表示抓拍正常结束,0表示抓拍异常结束;snap index: such as 3,2,1,1 means the last one,0 means there has some exception and snap stop;
        ('nSpeed', c_int),  # 车速,km/h;speed km/h;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event operation.0=pulse event,1=begin of the durative event,2=end of the durative event;;
        ('byReserved', C_BYTE * 2),  
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;Snap flag(by bit),please refer to NET_RESERVED_COMMON;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 表示交通车辆的数据库记录;The record of the database of the traffic vehicle;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('stuIntelliCommInfo', NET_A_EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息;GPS info ,use in mobile DVR/NVR;
        ('bReserved', C_BYTE * 848),  # 保留字节,留待扩展.;reserved;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
    ]

class NET_A_DEV_EVENT_TRAFFIC_OVERLINE_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_OVERLINE(交通-压线事件)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFIC_OVERLINE's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('nLane', c_int),  # 对应车道号;Corresponding Lane number;
        ('stuObject', NET_A_MSG_OBJECT),  # 车牌信息;have being detected object;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;snap index,such as 3,2,1,1 means the last one,0 means there has some exception and snap stop;
        ('nSpeed', c_int),  # 车辆实际速度,Km/h;speed,km/h;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),  
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息;GPS info ,use in mobile DVR/NVR;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX3)),  # 图片信息数组;Picture information;
        ('nImageInfoNum', c_int),  # 图片信息个数;Picture number;
        ('bReserved', C_BYTE * (964-sizeof(c_void_p))),  # 保留字节;Reserved;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_REGION_INFO(Structure):
    """
    区间测速信息
    Interval speed information
    """
    _fields_ = [
        ('stuDriveInTime', NET_TIME),  # 驶入时间;Drive in time;
        ('stuDriveOutTime', NET_TIME),  # 驶出时间;Drive Out time;
        ('bReserved', C_BYTE * 1024),  # 保留字节;Reserved;
    ]

class NET_A_DEV_EVENT_TRAFFIC_OVERSPEED_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_OVERSPEED(交通超速事件)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFIC_OVERSPEED's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('nLane', c_int),  # 对应车道号;Corresponding Lane number;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;have being detected object;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('nSpeed', c_int),  # 车辆实际速度Km/h;vehicle speed Unit:Km/h;
        ('nSpeedUpperLimit', c_int),  # 速度上限 单位：km/h;Speed Up limit Unit:km/h;
        ('nSpeedLowerLimit', c_int),  # 速度下限 单位：km/h;Speed Low limit Unit:km/h;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;snap index:such as 3,2,1,1 means the last one,0 means there has some exception and snap stop;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2 means continuous event's end;;
        ('byReserved', C_BYTE * 2),  
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('szFilePath', c_char * 260),  # 文件路径;Faile path;
        ('stuIntelliCommInfo', NET_A_EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息;GPS info ,use in mobile DVR/NVR;
        ('nSpeedingPercentage', c_int),  # 超速百分比;over speed percentage;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX3)),  # 图片信息数组;Picture information;
        ('nImageInfoNum', c_int),  # 图片信息个数;Picture number;
        ('bReserved', C_BYTE * (568-sizeof(c_void_p))),  # 保留字节;Reserved;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('stRegionInfo', NET_REGION_INFO),  # 区间测速信息;Interval speed information;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('stuNonMotor', VA_OBJECT_NONMOTOR),  # 非机动车信息;The information of Non-motor;
        ('bHasNonMotor', C_BOOL),  # 是否有非机动车对象;has NonMotor information;
    ]

class NET_A_DEV_EVENT_TRAFFIC_UNDERSPEED_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_UNDERSPEED(交通欠速事件)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFIC_UNDERSPEED's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved2', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('nLane', c_int),  # 对应车道号;Corresponding Lane number;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;have being detected object;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('nSpeed', c_int),  # 车辆实际速度Km/h;vehicle speed Unit:Km/h;
        ('nSpeedUpperLimit', c_int),  # 速度上限 单位：km/h;Speed Up limit Unit:km/h;
        ('nSpeedLowerLimit', c_int),  # 速度下限 单位：km/h;Speed Low limit Unit:km/h;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;snap index: such as 3,2,1,1 means the last one,0 means there has some exception and snap stop;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('bReserved1', C_BYTE * 2),  # 对齐;reserved;
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('nUnderSpeedingPercentage', c_int),  # 欠速百分比;under speed percentage;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('stuIntelliCommInfo', NET_A_EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelligence common information;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息;GPS info ,use in mobile DVR/NVR;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX3)),  # 图片信息数组;Picture information;
        ('nImageInfoNum', c_int),  # 图片信息个数;Picture number;
        ('bReserved', C_BYTE * (828-sizeof(c_void_p))),  # 保留字节;Reserved;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_DEV_EVENT_TRAFFIC_ROAD_CONSTRUCTION_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_ROAD_CONSTRUCTION (交通道路施工检测事件) 对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_TRAFFIC_ROAD_CONSTRUCTION (traffic road block construction)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('nAction', c_int),  # 事件动作, 0表示脉冲事件, 1表示持续性事件开始, 2表示持续性事件结束;Event action, 0: Pulse, 1: Start, 2: Stop;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Timestamp (in milliseconds);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Time for the event occurred;
        ('nEventID', C_UINT),  # 事件ID;Event ID;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;Event file info;
        ('stuBoundingBox', NET_RECT),  # 物体包围盒;Bounding box;
        ('nLane', C_UINT),  # 车道号;Lane number;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;Common info;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX2)),  # 图片信息数组;Number of picture information;
        ('nImageInfoNum', c_int),  # 图片信息个数;Number of picture information;
        ('bReserved', C_BYTE * (4088 - sizeof(c_void_p))),  # 预留字节;reserved;
    ]

class NET_A_DEV_EVENT_TRAFFIC_ROAD_BLOCK_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_ROAD_BLOCK (交通路障检测事件) 对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_TRAFFIC_ROAD_BLOCK (traffic road block detection)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('nAction', c_int),  # 事件动作, 0表示脉冲事件, 1表示持续性事件开始, 2表示持续性事件结束;Event action, 0: Pulse, 1: Start, 2: Stop;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Timestamp (in milliseconds);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Time for the event occurred;
        ('nEventID', C_UINT),  # 事件ID;Event ID;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;Event file info;
        ('stuBoundingBox', NET_RECT),  # 物体包围盒;Bounding box;
        ('nLane', C_UINT),  # 车道号;Lane number;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;Common info;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX2)),  # 图片信息数组;Picture information array;
        ('nImageInfoNum', c_int),  # 图片信息个数;Number of picture information;
        ('bReserved', C_BYTE * (4088 - sizeof(c_void_p))),  # 预留字节;reserved;
    ]

class NET_A_DEV_EVENT_TRAFFICACCIDENT_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFICACCIDENT(交通事故事件)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFICACCIDENT's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;ChannelId;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('nObjectNum', c_int),  # 检测到的物体个数;have being detected object number;
        ('stuObjectIDs', NET_A_MSG_OBJECT * 16),  # 检测到的物体列表;have being detected object list;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),  
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuTrafficCarPartInfo', NET_A_EVENT_TRAFFIC_CAR_PART_INFO),  # 交通车辆部分信息;part of traffic car info;
        ('nLane', C_UINT),  # 车道号;Lane num;
        ('bReserved', C_BYTE * 460),  # 保留字节,留待扩展.;reserved;
    ]

class NET_A_DEV_EVENT_TRAFFIC_VISIBILITY_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_VISIBILITY (交通能见度事件检测)对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_TRAFFIC_VISIBILITY
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel;
        ('nAction', c_int),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action 0:pulse 1:start 2:stop;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('PTS', c_double),  # 时间戳(单位:毫秒);Time stamp(unit:ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occur time;
        ('nEventID', C_UINT),  # 事件ID;Event ID;
        ('nRuleId', C_UINT),  # 智能事件规则编号;Event RuleID;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;FileInfo;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的车牌信息;Plate number info;
        ('emTriggerType', C_ENUM),  # 触发类型 Refer: EM_TRIGGER_TYPE;Trigger Type Refer: EM_TRIGGER_TYPE;
        ('stuCommInfo', EVENT_COMM_INFO),  # 公共信息;Common Info;
        ('nVisibility', C_UINT),  # 能见程度（表示距离范围）单位：米;Visibility distance unit:m;
        ('bReserved', C_BYTE * 1020),  # 保留字节;Reserved;
    ]

class NET_A_DEV_EVENT_TRAFFIC_THROW_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_THROW(交通抛洒物品事件)对应数据块描述信息
    Event type EVENT_IVS_TRAFFIC_THROW(throw)corresponding data block description info
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 8),  # 字节对齐;byte alignment;
        ('PTS', C_DWORD),  # 时间戳(单位是毫秒);Time stamp(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occurred time;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;The corresponding file info of the event;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),0位:"*",1位:"Timing",2位:"Manual",3位:"Marked",4位:"Event",5位:"Mosaic",6位:"Cutout";Snap flag(by bit)0 bit:"*",1 bit:"Timing",2 bit:"Manual",3 bit:"Marked",4 bit:"Event",5 bit:"Mosaic",6 bit:"Cutout";
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event operation.0=pulse event,1=begin of the durative event,2=end of the durative event;;
        ('bReserved2', C_BYTE * 2),  
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('nLane', c_int),  # 对应车道号;Corresponding lane No.;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;Detected object;
        ('stuIntelliCommInfo', NET_A_EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelligent things info;
        ('stuTrafficCarPartInfo', NET_A_EVENT_TRAFFIC_CAR_PART_INFO),  # 交通车辆部分信息;part of traffic car info;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息;GPS info ,use in mobile DVR/NVR;
        ('bReserved', C_BYTE * 340),  # 保留字节;reserved;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
    ]

class NET_GPS_INFO_EX(Structure):
    """
    GPS信息
    GPS info
    """
    _fields_ = [
        ('nLongitude', c_int),  # 经度(单位是百万分之一度)西经：0 - 180000000 实际值应为: 180*1000000 – dwLongitude东经：180000000 - 360000000 实际值应为: dwLongitude – 180*1000000如: 300168866应为（300168866 - 180*1000000）/1000000 即东经120.168866度;Longitude(Unit: one millionth of a degree);
        ('nLatidude', c_int),  # 纬度(单位是百万分之一度)南纬：0 - 90000000 实际值应为: 90*1000000 – dwLatidude北纬：90000000 – 180000000 实际值应为: dwLatidude – 90*1000000如: 120186268应为 (120186268 - 90*1000000)/1000000 即北纬30. 186268度;Latidude(Unit: one millionth of a degree);
        ('nAltitude', c_double),  # 高度,单位为米;Altitude, unit : meters;
        ('szReserved', c_char * 48),  # 保留字段;Reserved byte;
    ]

class NET_A_DEV_EVENT_SMOKE_INFO(Structure):
    """
    事件类型EVENT_IVS_SMOKEDETECTION(烟雾报警事件)对应的数据块描述信息
    the describe of EVENT_IVS_SMOKEDETECTION's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;ChannelId;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('nRuleID', C_UINT),  # 规则编号,用于标示哪个规则触发的事件，缺省时默认为0;Rule ID, used to indicate which rule triggers the event. The default value is 0;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;have being detected object;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),  
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('nOccurrenceCount', C_UINT),  # 事件触发累计次数;event trigger accumilated times;
        ('stuIntelliCommInfo', NET_A_EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info;
        ('stuPtzPosition', PTZ_SPACE_UNIT),  # 云台的坐标和放大倍数;ptz coordinate and zoom;
        ('bSceneImage', C_BOOL),  # stuSceneImage 是否有效;Whether stuSceneImage is valid;
        ('stuSceneImage', SCENE_IMAGE_INFO_EX),  # 全景广角图;Global scene iamge;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('emTriggerType', C_ENUM),  # 触发类型 Refer: EM_TRIGGER_TYPE;Trigger type Refer: EM_TRIGGER_TYPE;
        ('nMark', c_int),  # 标记抓拍帧;Used to mark capture frames;
        ('nSource', c_int),  # 视频分析的数据源地址;Data source address of the video analysis;
        ('nFrameSequence', c_int),  # 视频分析帧序号;Video analysis frame number;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('stuCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('emCaptureProcess', C_ENUM),  # 抓拍过程 Refer: EM_CAPTURE_PROCESS_END_TYPE;Capture process Refer: EM_CAPTURE_PROCESS_END_TYPE;
        ('nCurChannelHFOV', C_UINT),  # 当前报警通道的横向视场角,单位：度，实际角度乘以100;The lateral field of view angle of the current alarm channel, unit: degree, the actual angle is multiplied by 100;
        ('nCurChannelVFOV', C_UINT),  # 当前报警通道的垂直视场角,单位：度，实际角度乘以100;The vertical field of view angle of the current alarm channel, unit: degree, the actual angle is multiplied by 100;
        ('stuGPS', NET_GPS_INFO_EX),  # 设备的GPS坐标;GPS Info;
        ('nObjectCount', c_int),  # 烟雾检测点个数;Number of smoke detection points;
        ('stuObjects', NET_A_MSG_OBJECT_EX2 * 16),  # 烟雾检测点信息;Smoke detection point information;
        ('emSmokeColor', C_ENUM * 16),  # 烟雾颜色 Refer: EM_SMOKE_COLOR;smoke color Refer: EM_SMOKE_COLOR;
        ('nSmokeColorNum', c_int),  # 烟雾颜色有效个数;smoke color number;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX2)),  # 图片信息数组;Image information array;
        ('nImageInfoNum', c_int),  # 图片信息个数;Number of picture information;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('szReserved', c_char * 944),  # 保留字段;Reserved byte;
    ]

class NET_A_DEV_EVENT_FIRE_INFO(Structure):
    """
    事件类型EVENT_IVS_FIREDETECTION(火警事件)对应的数据块描述信息
    the describe of EVENT_IVS_FIREDETECTION's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;ChannelId;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;have being detected object;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),  # 保留字节;
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('nDetectRegionNum', c_int),  # 规则检测区域顶点数;detect region point;
        ('DetectRegion', NET_POINT * 20),  # 规则检测区域;detect region;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见 NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('nSourceIndex', c_int),  # 事件源设备上的index,-1表示数据无效;the source device's index,-1 means data in invalid;
        ('szSourceDevice', c_char * 260),  # 事件源设备唯一标识,字段不存在或者为空表示本地设备;the source device's sign(exclusive),field said local device does not exist or is empty;
        ('nOccurrenceCount', C_UINT),  # 事件触发累计次数;event trigger accumilated times;
        ('stuIntelliCommInfo', NET_A_EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info;
        ('bSceneImage', C_BOOL),  # stuSceneImage 是否有效;Whether stuSceneImage is valid;
        ('stuSceneImage', SCENE_IMAGE_INFO_EX),  # 全景广角图;Global scene iamge;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('emTriggerType', C_ENUM),  # 触发类型 Refer: EM_TRIGGER_TYPE;Trigger type Refer: EM_TRIGGER_TYPE;
        ('emCaptureProcess', C_ENUM),  # 抓拍过程 Refer: EM_CAPTURE_PROCESS_END_TYPE;Capture process Refer: EM_CAPTURE_PROCESS_END_TYPE;
        ('nMark', c_int),  # 标记抓拍帧;Used to mark capture frames;
        ('nSource', c_int),  # 视频分析的数据源地址;Data source address of the video analysis;
        ('nFrameSequence', c_int),  # 视频分析帧序号;Video analysis frame number;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('stuCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX2)),  # 图片信息数组;Image information array;
        ('nImageInfoNum', c_int),  # 图片信息个数;Number of picture information;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_DREGS_UNCOVERED_VEHICLE_INFO(Structure):
    """
    车辆信息
    Vehicle info
    """
    _fields_ = [
        ('szPlateNumber', c_char * 64),  # 车牌号码;Plate number;
        ('stuBoundingBox', NET_RECT),  # 包围盒;Bounding box;
        ('byReserved', C_BYTE * 512),  # 预留字节;Reserved;
    ]

class NET_A_DEV_EVENT_DREGS_UNCOVERED_INFO(Structure):
    """
    事件类型 EVENT_IVS_DREGS_UNCOVERED(渣土车未遮盖载货检测事件)对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_DREGS_UNCOVERED(Loading test event not covered by muck truck)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel ID;
        ('nAction', c_int),  # 0:脉冲;Event action,0 pause;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Timestamp (in milliseconds);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Time for the event occurred;
        ('nEventID', C_UINT),  # 事件ID;Event ID;
        ('emClassType', C_ENUM),  # 智能事件所属大类 Refer: EM_CLASS_TYPE;Event class Refer: EM_CLASS_TYPE;
        ('nDetectRegionNum', c_int),  # 检测区域顶点数;The number of stuDetectRegion;
        ('stuDetectRegion', NET_POINT * 20),  # 检测区域,[0,8191];The region of alarm occur, [0,8191];
        ('stuVehicleInfo', NET_A_DREGS_UNCOVERED_VEHICLE_INFO),  # 车辆信息;Vehicle info;
        ('stuSceneImage', SCENE_IMAGE_INFO),  # 全景广角图;Panoramic wide-angle map;
        ('byReserved', C_BYTE * 952),  # 预留字节;Reserved;
    ]

class NET_A_DEV_EVENT_TRAFFIC_BOARD_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_BOARD (交通违章上下客事件检测)对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_TRAFFIC_BOARD
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel;
        ('nAction', c_int),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action 0:pulse 1:start 2:stop;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('PTS', c_double),  # 时间戳(单位:毫秒);Time stamp(unit:ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occur time;
        ('nEventID', C_UINT),  # 事件ID;Event ID;
        ('nRuleId', C_UINT),  # 智能事件规则编号;Event RuleID;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;FileInfo;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的车牌信息;Plate number info;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 检测到的车辆信息;Detected vehicle info;
        ('emTriggerType', C_ENUM),  # 触发类型 Refer: EM_TRIGGER_TYPE;TriggerType Refer: EM_TRIGGER_TYPE;
        ('stuCommInfo', EVENT_COMM_INFO),  # 公共信息;Common Info;
        ('bReserved', C_BYTE * 1020),  # 保留字节;Reserved;
    ]

class NET_A_DEV_EVENT_TRAFFIC_VEHICLE_CLEANLINESS_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_VEHICLE_CLEANLINESS (交通车辆清洁度检测事件检测)对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_TRAFFIC_VEHICLE_CLEANLINESS
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel;
        ('nAction', c_int),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action 0:pulse 1:start 2:stop;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('PTS', c_double),  # 时间戳(单位:毫秒);Time stamp(unit:ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occur time;
        ('nEventID', C_UINT),  # 事件ID;Event ID;
        ('nRuleId', C_UINT),  # 智能事件规则编号;Event RuleID;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;FileInfo;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的车牌信息;Plate number info;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 检测到的车辆信息;Detected vehicle info;
        ('emTriggerType', C_ENUM),  # 触发类型 Refer: EM_TRIGGER_TYPE;Trigger Type Refer: EM_TRIGGER_TYPE;
        ('stuCommInfo', EVENT_COMM_INFO),  # 公共信息;Common Info;
        ('nCleanValue', c_int),  # 清洁度阀值;clean value;
        ('bReserved', C_BYTE * 1024),  # 保留字节;Reserved;
    ]

class NET_A_DEV_EVENT_TRAFFIC_SPEED_CHANGE_DETECTION_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_SPEED_CHANGE_DETECTION 变速检测事件 对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_TRAFFIC_SPEED_CHANGE_DETECTION
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel;
        ('nAction', c_int),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action 0:pulse 1:start 2:stop;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('PTS', c_double),  # 时间戳(单位:毫秒);Time stamp(unit:ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occur time;
        ('nEventID', C_UINT),  # 事件ID;Event ID;
        ('nRuleId', C_UINT),  # 智能事件规则编号;Rule ID;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;Event file info;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的车牌信息;Plate number info;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 检测到的车辆信息;Detected vehicle info;
        ('emTriggerType', C_ENUM),  # 触发类型 Refer: EM_TRIGGER_TYPE;Trigger Type Refer: EM_TRIGGER_TYPE;
        ('nLane', c_int),  # 对应车道号;Lane;
        ('nSpeedNew', c_int),  # 当前车速, 单位: km/h;Current speed, unit: km/h;
        ('nSpeedOld', c_int),  # 变化前车速, 单位: km/h;Vehicle speed before change, unit: km/h;
        ('byReserved', C_BYTE * 1024),  # 保留字节;Reserved;
    ]

class NET_A_DEV_EVENT_TRAFFIC_OVERYELLOWLINE_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_OVERYELLOWLINE(交通违章-压黄线)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFIC_OVERYELLOWLINE's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;have being detected object;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('nLane', c_int),  # 对应车道号;Corresponding Lane number;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),  
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('nSpeed', c_int),  # 车辆实际速度,km/h;speed,km/h;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('bIsExistAlarmRecord', C_BOOL),  # rue:有对应的报警录像; false:无对应的报警录像;true:corresponding alarm recording; false: no corresponding alarm recording;
        ('dwAlarmRecordSize', C_DWORD),  # 录像大小;Video size;
        ('szAlarmRecordPath', c_char * 256),  # 录像路径;Video Path;
        ('stuIntelliCommInfo', NET_A_EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX3)),  # 图片信息数组;Picture information;
        ('nImageInfoNum', c_int),  # 图片信息个数;Picture number;
        ('bReserved', C_BYTE * (528-sizeof(c_void_p))),  # 保留字节,留待扩展.;reserved;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('nDetectNum', c_int),  # 规则检测区域顶点数;Acme amount of the rule detect zone;
        ('DetectRegion', NET_POINT * 20),  # 规则检测区域;Rule detect zone;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_DEV_EVENT_TRAFFIC_VEHICLE_IN_EMERGENCY_LANE_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_VEHICLE_IN_EMERGENCY_LANE (占用应急车道事件)对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_TRAFFIC_VEHICLE_IN_EMERGENCY_LANE
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel id;
        ('nAction', c_int),  # 0:脉冲事件;0:pulse;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('PTS', C_DWORD),  # 时间戳(单位是毫秒);Time stamp(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occurred time;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('nLane', c_int),  # 对应车道号;lane;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;object info;
        ('byReserved1', C_BYTE * 4),  # 字节对齐;byte alignment;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('stuTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;traffic car info;
        ('byReserved2', C_BYTE * 4),  # 字节对齐;byte alignment;
        ('stuNonMotor', VA_OBJECT_NONMOTOR),  # 非机动车对象;non motor info;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;Sequence;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;file info;
        ('stuCommInfo', EVENT_COMM_INFO),  # 公共信息;common info;
        ('byReserved', C_BYTE * 1024),  # 预留字段;reserved;
    ]

class NET_A_DEV_EVENT_TRAFFIC_TRUCK_OCCUPIED_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_TRUCK_OCCUPIED (大车占道事件)对应的数据块描述信息
    The description information of the data block corresponding to the event type EVENT_IVS_TRAFFIC_TRUCK_OCCUPIED (Truck occupation event)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel number;
        ('nAction', c_int),  # 0:脉冲,1:开始, 2:停止;Action, 0:pulse,1:start, 2:stop;
        ('szName', c_char * 128),  # 事件名称;Event Name;
        ('szClass', c_char * 16),  # 智能事件所属大类;Category of intelligent events;
        ('nGroupID', c_int),  # GroupID事件组ID，同一物体抓拍过程内GroupID相同;group ID, which is the same in the process of capturing the same object;
        ('nCountInGroup', c_int),  # CountInGroup一个事件组内的抓拍张数;CountInGroup Number of snapshots in an event group;
        ('nIndexInGroup', c_int),  # IndexInGroup一个事件组内的抓拍序号，从1开始;IndexInGroup Capture sequence number in an event group,Start with 1;
        ('nUTCMS', C_UINT),  # 事件时间毫秒数;Time of occurrence in milliseconds;
        ('dbPTS', c_double),  # 相对事件时间戳,(单位是毫秒);Relative event timestamp in milliseconds;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间;Time of occurrence;
        ('nEventID', C_UINT),  # 事件ID;Event ID;
        ('nLane', c_int),  # 对应车道号;Corresponding lane number;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;Indicates the capture sequence number. For example, 3,2,1,1 indicates the end of capture, and 0 indicates the abnormal end;
        ('szReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('stuObject', NET_A_MSG_OBJECT),  # 车牌信息;License plate information;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;Body information;
        ('stuTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle information;
        ('stuCommInfo', EVENT_COMM_INFO),  # 公共信息;Public information;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;Event corresponding file information;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;Capture flag (bitwise), see NET_RESERVED_COMMON for details;
        ('szReserved', c_char * 1024),  # 预留字节;Reserved;
    ]

class NET_A_DEV_EVENT_TRAFFIC_SPECIAL_VEHICLE_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_SPECIAL_VEHICLE_DETECT (特殊车辆检测)对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_TRAFFIC_SPECIAL_VEHICLE_DETECT
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel;
        ('nAction', c_int),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action 0:pulse 1:start 2:stop;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('PTS', c_double),  # 时间戳(单位:毫秒);Time stamp(unit:ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occur time;
        ('nEventID', C_UINT),  # 事件ID;Event ID;
        ('nRuleId', C_UINT),  # 智能事件规则编号;Event RuleID;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;FileInfo;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的车牌信息;Plate number info;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 检测到的车辆信息;Detected vehicle info;
        ('emTriggerType', C_ENUM),  # 触发类型 Refer: EM_TRIGGER_TYPE;Trigger Type Refer: EM_TRIGGER_TYPE;
        ('stuCommInfo', EVENT_COMM_INFO),  # 公共信息;Common Info;
        ('bReserved', C_BYTE * 1020),  # 保留字节;Reserved;
    ]

class NET_A_DEV_EVENT_TRAFFICCONTROL_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFICCONTROL(交通管理事件)对应的数据块描述信息
    Event type EVENT_IVS_TRAFFICCONTROL(traffic control)corresponding data block description info
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;ChannelId;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;have being detected object;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息;GPS info ,use in mobile DVR/NVR;
        ('bReserved', C_BYTE * 932),  # 保留字节,留待扩展.;Reserved field. For extension use.;
    ]

class NET_A_DEV_EVENT_TRAFFICGATE_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFICGATE(交通卡口老规则事件/线圈电警上的交通卡口老规则事件)对应的数据块描述信息
    由于历史原因,如果要处理卡口事件,DEV_EVENT_TRAFFICJUNCTION_INFO和EVENT_IVS_TRAFFICGATE要一起处理,以防止有视频电警和线圈电警同时接入平台的情况发生
    另外EVENT_IVS_TRAFFIC_TOLLGATE只支持新卡口事件的配置
    the describe of EVENT_IVS_TRAFFICGATE's data
    owing to history, if you want to deal with TRAFFICGATE,DEV_EVENT_TRAFFICJUNCTION_INFO/EVENT_IVS_TRAFFICGATE must be handle together;
    in addition: EVENT_IVS_TRAFFIC_TOLLGATE only support new tollgate event configuration
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;ChannelId;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('byOpenStrobeState', C_BYTE),  # 开闸状态,具体请见EM_OPEN_STROBE_STATE;Open gateway status, see EM_OPEN_STROBE_STATE;
        ('bReserved1', c_char * 3),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体，车标;have being detected object;
        ('nLane', c_int),  # 对应车道号;road number;
        ('nSpeed', c_int),  # 车辆实际速度Km/h;the car's actual rate(Km/h);
        ('nSpeedUpperLimit', c_int),  # 速度上限 单位：km/h;rate upper limit(km/h);
        ('nSpeedLowerLimit', c_int),  # 速度下限 单位：km/h;rate lower limit(km/h);
        ('dwBreakingRule', C_DWORD),  # 违反规则掩码,第一位:逆行;第二位:压线行驶; 第三位:超速行驶;第四位：欠速行驶; 第五位:闯红灯;第六位:穿过路口(卡口事件)第七位: 压黄线; 第八位: 有车占道; 第九位: 黄牌占道;否则默认为:交通卡口事件;BreakingRule's mask,first byte: Retrograde;second byte:Overline; the third byte:Overspeed;the forth byte:UnderSpeed;the five byte: crash red light;the six byte:passing(trafficgate)the seven byte: OverYellowLine; the eight byte: WrongRunningRoute; the nine byte: YellowVehicleInRoute; default: trafficgate;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息，有存放车牌信息;vehicle info;
        ('szManualSnapNo', C_BYTE * 64),  # 手动抓拍序号;manual snap sequence string;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;snap index,such as 3,2,1,1 means the last one,0 means there has some exception and snap stop;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 3),  # 保留字节;reserved;
        ('szSnapFlag', C_BYTE * 16),  # 设备产生的抓拍标识;snap flag from device;
        ('bySnapMode', C_BYTE),  # 抓拍方式,0-未分类 1-全景 2-近景 4-同向抓拍 8-反向抓拍 16-号牌图像;snap mode,0-normal 1-globle 2-near 4-snap on the same side 8-snap on the reverse side 16-plant picture;
        ('byOverSpeedPercentage', C_BYTE),  # 超速百分比;over speed percentage;
        ('byUnderSpeedingPercentage', C_BYTE),  # 欠速百分比;under speed percentage;
        ('byRedLightMargin', C_BYTE),  # 红灯容许间隔时间,单位：秒;red light margin, s;
        ('byDriveDirection', C_BYTE),  # 行驶方向,0-上行(即车辆离设备部署点越来越近),1-下行(即车辆离设备部署点越来越远);drive direction,0-"Approach",where the car is more near,1-"Leave",means where if mor far to the car;
        ('szRoadwayNo', c_char * 32),  # 道路编号;road way number;
        ('szViolationCode', c_char * 16),  # 违章代码;violation code;
        ('szViolationDesc', c_char * 128),  # 违章描述;violation desc;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('szVehicleType', c_char * 32),  # 车辆大小类型 Minisize"微型车,"Light-duty"小型车,"Medium"中型车,"Oversize"大型车,"Huge"超大车,"Largesize"长车 "Unknown"未知;car type,"Motor", "Light-duty", "Medium", "Oversize", "Huge", "Other";
        ('byVehicleLenth', C_BYTE),  # 车辆长度, 单位米;car length, m;
        ('byLightState', C_BYTE),  # LightState表示红绿灯状态:0 未知,1 绿灯,2 红灯,3 黄灯;LightState means red light status:0 unknown,1 green,2 red,3 yellow;
        ('byReserved1', C_BYTE),  # 保留字节,留待扩展;reserved;
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('nOverSpeedMargin', c_int),  # 限高速宽限值 单位：km/h;over speed margin, km/h;
        ('nUnderSpeedMargin', c_int),  # 限低速宽限值 单位：km/h;under speed margin, km/h;
        ('szDrivingDirection', c_char * 3 * 256),  # "DrivingDirection" ,行驶方向"Approach"-上行,即车辆离设备部署点越来越近；"Leave"-下行,即车辆离设备部署点越来越远,第二和第三个参数分别代表上行和下行的两个地点,UTF-8编码;"DrivingDirection""Approach" means driving direction,where the car is more near;"Leave"-means where if mor far to the carthe second and third param means the location of the driving direction;
        ('szMachineName', c_char * 256),  # 本地或远程设备名称;machine name;
        ('szMachineAddress', c_char * 256),  # 机器部署地点、道路编码;machine address;
        ('szMachineGroup', c_char * 256),  # 机器分组、设备所属单位;machine group;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuSigInfo', NET_A_SIG_CARWAY_INFO_EX),  # 由车检器产生抓拍信号冗余信息;The vehicle detector generates the snap signal redundancy info;
        ('szFilePath', c_char * 260),  # 文件路径;File path;
        ('RedLightUTC', NET_TIME_EX),  # 红灯开始UTC时间;the begin time of red light;
        ('szDeviceAddress', POINTER(c_char)),  # 设备地址,OSD叠加到图片上的,来源于配置TrafficSnapshot.DeviceAddress,'\0'结束;device address,OSD superimposed onto the image,from TrafficSnapshot.DeviceAddress,'\0'means end.;
        ('fActualShutter', c_float),  # 当前图片曝光时间,单位为毫秒;Current picture exposure time, in milliseconds;
        ('byActualGain', C_BYTE),  # 当前图片增益,范围为0~100;Current picture gain, ranging from 0 to 1000;
        ('byDirection', C_BYTE),  # 0-南向北 1-西南向东北 2-西向东 3-西北向东南 4-北向南 5-东北向西南 6-东向西 7-东南向西北 8-未知;0-S to N 1-SW to NE 2-W to E 3-NW to SE 4-N to S 5-NE to SW 6-E to W 7-SE to NW 8-Unknown;
        ('bReserve', C_BYTE),  # 保留字节, 字节对齐;Reserved bytes, byte alignment;
        ('bRetCardNumber', C_BYTE),  # 卡片个数;Card Number;
        ('stuCardInfo', EVENT_CARD_INFO * 16),  # 卡片信息;Card information;
        ('szDefendCode', c_char * 64),  # 图片防伪码;Waterproof;
        ('nTrafficBlackListID', c_int),  # 关联禁止名单数据库记录默认主键ID, 0,无效；> 0,禁止名单数据记录;Link to blocklist main keyID, 0, invalid, > 0, blocklist data record;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('emVehicleDirection', C_ENUM),  # 抓拍方向 Refer: EM_VEHICLE_DIRECTION;Vehicle Direction Refer: EM_VEHICLE_DIRECTION;
        ('bReserved', C_BYTE * 448),  # 保留字节,留待扩展.;Reserved bytes, leave extended;
    ]

class NET_A_SIG_CARWAY_INFO(Structure):
    """
    抓拍信息
    snapshot info
    """
    _fields_ = [
        ('snSpeed', c_short),  # 当前车的速度,km/h;current car speed,km/h;
        ('snCarLength', c_short),  # 当前车长,分米为单位;current car length, dm;
        ('fRedTime', c_float),  # 当前车道红灯时间,秒.毫秒;current red light time, s.ms;
        ('fCapTime', c_float),  # 当前车道抓拍时间,秒.毫秒;current car way snapshot time, s.ms;
        ('bSigSequence', C_BYTE),  # 当前抓拍序号;current snapshot Sequence;
        ('bType', C_BYTE),  # 当前车道的抓拍类型0: 雷达高限速;1: 雷达低限速;2: 车检器高限速;3:车检器低限速4: 逆向;5: 闯红灯;6: 红灯亮;7: 红灯灭;8: 全部抓拍或者卡口;current snapshot type0: radar up speed limit;1: radar low speed limit;2: car detector up speed limit;3:car detector low speed limit4: reverse;5: break red light;6: red light on;7: red light off;8: snapshot or traffic gate;
        ('bDirection', C_BYTE),  # 闯红灯类型:01:左转红灯;02:直行红灯;03:右转红灯;breaking type :01:left turn;02:straight;03:right;
        ('bLightColor', C_BYTE),  # 当前车道的红绿灯状态,0: 绿灯, 1: 红灯, 2: 黄灯;current car way traffic light state,0: green, 1: red, 2: yellow;
        ('bSnapFlag', C_BYTE * 16),  # 设备产生的抓拍标识;snap flag from device;
    ]

class NET_A_CARWAY_INFO(Structure):
    """
    每个车道的相关信息
    car way info
    """
    _fields_ = [
        ('bCarWayID', C_BYTE),  # 当前车道号;current car way id;
        ('bReserve', C_BYTE * 2),  # 保留字段;reserved;
        ('bSigCount', C_BYTE),  # 被触发抓拍的个数;being snapshotted;
        ('stuSigInfo', NET_A_SIG_CARWAY_INFO * 3),  # 当前车道上,被触发抓拍对应的抓拍信息;the snapshot info;
        ('bReserved', C_BYTE * 12),  # 保留字段;reserved;
    ]

class NET_A_DEV_EVENT_TRAFFICSNAPSHOT_INFO(Structure):
    """
    事件类型EVENT_TRAFFICSNAPSHOT(交通抓拍事件)对应的数据块描述信息
    the describe of EVENT_TRAFFICSNAPSHOT's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;ChannelId;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('bReserv', C_BYTE * 3),  # 保留字节;reserved;
        ('bCarWayCount', C_BYTE),  # 触发抓拍的车道个数;car way number being snapshotting;
        ('stuCarWayInfo', NET_A_CARWAY_INFO * 8),  # 触发抓拍的车道相关信息;car way info being snapshotting;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('bReserved', C_BYTE * 344),  # 保留字节,留待扩展;Reserved;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
    ]

class NET_A_DEV_EVENT_TRAFFIC_NONMOTORINMOTORROUTE_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_NONMOTORINMOTORROUTE (非机动车占用机动车道)对应的数据块描述信息
    Event Type EVENT_IVS_TRAFFIC_NONMOTORINMOTORROUTE (Non-motor vehicles occupy the lanes)corresponding to the description of the data block,
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;ChannelId;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('bReserved1', C_BYTE * 3),  # 保留字节.;Reserved bytes.;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;have being detected object;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('szRecordFile', c_char * 128),  # 报警对应的原始录像文件信息;Alarm corresponding original video file information;
        ('nLane', c_int),  # 对应车道号;road number;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;snap index,such as 3,2,1,1 means the last one,0 means there has some exception and snap stop;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('bHasNonMotor', C_BOOL),  # 是否有非机动车对象;has NonMotor information?;
        ('stuNonMotor', VA_OBJECT_NONMOTOR),  # 非机动车对象;NonMotor information;
        ('bReserved', C_BYTE * 4096),  # 保留字节,留待扩展.;Reserved bytes, leave extended_.;
    ]

class NET_A_DEV_EVENT_TRAFFIC_RUNREDLIGHT_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_RUNREDLIGHT(交通-闯红灯事件)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFIC_RUNREDLIGHT's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('nLane', c_int),  # 对应车道号;Corresponding Lane number;
        ('stuObject', NET_A_MSG_OBJECT),  # 车牌信息;have being detected object;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('nLightState', c_int),  # 红绿灯状态 0:未知 1：绿灯 2:红灯 3:黄灯;state of traffic light 0:unknown 1:green 2:red 3:yellow;
        ('nSpeed', c_int),  # 车速,km/h;speed,km/h;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;snap index,such as 3,2,1,1 means the last one,0 means there has some exception and snap stop;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stRedLightUTC', NET_TIME_EX),  # 红灯开始时间;time of red light starting;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('byRedLightMargin', C_BYTE),  # 红灯容许间隔时间,单位：秒;red light margin, s;
        ('byAlignment', C_BYTE * 3),  # 字节对齐;Align string;
        ('nRedLightPeriod', c_int),  # 表示红灯周期时间,单位毫秒;Red light period. The unit is ms.;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息;GPS info ,use in mobile DVR/NVR;
        ('nDirectionCount', c_int),  # 闯红灯方向个数;Number of red light running directions;
        ('emDirection', C_ENUM * 8),  # 闯红灯方向 Refer: EM_RED_LIGHT_DIRECTION;Directions of running the red light Refer: EM_RED_LIGHT_DIRECTION;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX3)),  # 图片信息数组;Picture information;
        ('nImageInfoNum', c_int),  # 图片信息个数;Picture number;
        ('bReserved', C_BYTE * (888-sizeof(c_void_p))),  # 保留字节;Reserved string;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('bHasNonMotor', C_BOOL),  # 是否有非机动车对象;has NonMotor information?;
        ('stuNonMotor', VA_OBJECT_NONMOTOR),  # 非机动车对象;NonMotor information;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_DEV_EVENT_TRAFFIC_TURNLEFT_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_TURNLEFT(交通-违章左转)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFIC_TURNLEFT's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('nLane', c_int),  # 对应车道号;Corresponding Lane number;
        ('stuObject', NET_A_MSG_OBJECT),  # 车牌信息;have being detected object;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;snap index: such as 3,2,1,1 means the last one,0 means there has some exception and snap stop;
        ('nSpeed', c_int),  # 车辆实际速度,Km/h;speed,km/h;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息;GPS info ,use in mobile DVR/NVR;
        ('bReserved', C_BYTE * 968),  # 保留字节;Reserved;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('stuNonMotor', VA_OBJECT_NONMOTOR),  # 非机动车信息;The information of Non-motor;
        ('bHasNonMotor', C_BOOL),  # 是否有非机动车对象;whether stuNonMotor is valid;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]


class NET_A_DEV_EVENT_TRAFFIC_TURNRIGHT_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_TURNRIGHT (交通-违章右转)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFIC_TURNRIGHT's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('nLane', c_int),  # 对应车道号;Corresponding Lane number;
        ('stuObject', NET_A_MSG_OBJECT),  # 车牌信息;have being detected object;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;snap index: such as 3,2,1,1 means the last one,0 means there has some exception and snap stop;
        ('nSpeed', c_int),  # 车辆实际速度,Km/h;speed,km/h;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息;GPS info ,use in mobile DVR/NVR;
        ('bReserved', C_BYTE * 968),  # 保留字节;Reserved;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('stuNonMotor', VA_OBJECT_NONMOTOR),  # 非机动车信息;The information of Non-motor;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_DEV_EVENT_TRAFFIC_UTURN_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_UTURN(违章调头事件)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFIC_UTURN's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('nLane', c_int),  # 对应车道号;Corresponding Lane number;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;have being detected object;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;snap index: such as 3,2,1,1 means the last one,0 means there has some exception and snap stop;
        ('nSpeed', c_int),  # 车辆实际速度,Km/h;speed,km/h;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息;GPS info ,use in mobile DVR/NVR;
        ('bReserved', C_BYTE * 968),  # 保留字节;Reserved;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('stuNonMotor', VA_OBJECT_NONMOTOR),  # 非机动车信息;The information of Non-motor;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_DEV_EVENT_TRAFFIC_WRONGROUTE_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_WRONGROUTE(交通违章-不按车道行驶)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFIC_WRONGROUTE's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;have being detected object;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('nLane', c_int),  # 对应车道号;Corresponding Lane number;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('nSpeed', c_int),  # 车辆实际速度,km/h;speed,km/h;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息;GPS info ,use in mobile DVR/NVR;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX3)),  # 图片信息数组;Picture information;
        ('nImageInfoNum', c_int),  # 图片信息个数;Picture number;
        ('bReserved', C_BYTE * (968-sizeof(c_void_p))),  # 保留字节,留待扩展.;Reserved;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
    ]

class NET_A_DEV_EVENT_TRAFFIC_DRIVINGONSHOULDER_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_DRIVINGONSHOULDER(交通违章-路肩行驶事件)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFIC_DRIVINGONSHOULDER's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;have being detected object;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('nLane', c_int),  # 对应车道号;Corresponding Lane number;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('nSpeed', c_int),  # 车辆实际速度,km/h;speed,km/h;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;traffic car information;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
    ]

class NET_A_DEV_EVENT_TRAFFIC_YELLOWPLATEINLANE_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_YELLOWPLATEINLANE(交通违章-黄牌车占道事件)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFIC_YELLOWPLATEINLANE's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;have being detected object;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;vehicle info;
        ('nLane', c_int),  # 对应车道号;Corresponding Lane number;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('nSpeed', c_int),  # 车辆实际速度,km/h;speed,km/h;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('bReserved', C_BYTE * 1016),  # 保留字节,留待扩展.;Reserved;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle info;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
    ]

class NET_A_DEV_EVENT_TRAFFIC_PEDESTRAINPRIORITY_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_PEDESTRAINPRIORITY(斑马线行人优先事件)对应的数据块描述信息
    Event type EVENT_IVS_TRAFFIC_PEDESTRAINPRIORITY(Pedestal has higher priority at the crosswalk) corresponding data block description info
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel No.;
        ('szName', c_char * 128),  # 事件名称;Event name;
        ('bReserved1', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Time stamp(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occurred time;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;Detected object;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;Vehicle body info;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;The corresponding file info of the event;
        ('nLane', c_int),  # 对应车道号;Corresponding lane No.;
        ('dInitialUTC', c_double),  # 事件初始UTC时间 UTC为事件的UTC (1970-1-1 00:00:00)秒数。;Event initial UTC time UTC is the second of the event UTC (1970-1-1 00:00:00);
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event operation.0=pulse event,1=begin of the durative event,2=end of the durative event;;
        ('byReserved', C_BYTE * 2),
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;Snap flag(by bit),please refer to NET_RESERVED_COMMON;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 表示交通车辆的数据库记录;The record of the database of the traffic vehicle;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息;GPS info ,use in mobile DVR/NVR;
        ('bReserved', C_BYTE * 984),  # 保留字节,留待扩展.;Reserved field for future extension.;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
    ]

class NET_A_DEV_EVENT_TRAFFIC_NOPASSING_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_NOPASSING(交通违章-禁止通行事件)对应的数据块描述信息
    the describe of EVENT_IVS_TRAFFIC_NOPASSING's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('nTriggerType', c_int),  # TriggerType:触发类型,0车检器,1雷达,2视频;Trigger Type, 0 vehicle inspection device, 1 radar, 2 video;
        ('PTS', C_DWORD),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('UTCMS', c_int),
        ('nMark', c_int),  # 底层产生的触发抓拍帧标记;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;snap index: such as 3,2,1,1 means the last one,0 means there has some exception and snap stop;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;TrafficCar info;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;picture resolution;
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('byReserved1', C_BYTE * 3),
        ('nLane', c_int),  # 对应车道号;Corresponding lane number;
        ('stuObject', NET_A_MSG_OBJECT),  # 检测到的物体;Object to be detected;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;car body information;
        ('nFrameSequence', c_int),  # 视频分析帧序号;Video analysis frame number;
        ('nSource', c_int),  # 视频分析的数据源地址;Data source address of the video analysis;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息;GPS info ,use in mobile DVR/NVR;
        ('byReserved', C_BYTE * 984),  # 保留字节;Reserved bytes;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
    ]

class NET_A_DEV_EVENT_TRAFFIC_QUEUEJUMP_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_QUEUEJUMP (车辆加塞事件)对应的数据块描述信息
    EVENT_IVS_TRAFFIC_QUEUEJUMP (car jump a queue) corresponding data block description info
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('Reserved', c_char * 4),  # 保留字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Time stamp(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occurred time;
        ('nEventID', C_DWORD),  # 事件ID;Event ID;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;Event corresponding to file information;
        ('stuObject', NET_A_MSG_OBJECT),  # 车牌信息;plate info;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;car body info;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 车辆信息;Traffic car info;
        ('nLane', c_int),  # 对应车道号;Corresponding lane number;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;snap index,such as 3,2,1,1 means the last one,0 means there has some exception and snap stop;
        ('byEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action, 0 represents the pulse event, 1 means persistent event starts, 2 means persistent event ends;
        ('byImageIndex', C_BYTE),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;(Serial chip, the same time (accurate to seconds) may have multiple images, starting from 0);
        ('byReserved1', C_BYTE * 2),
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;(Grab flag (bit), see specific NET_RESERVED_COMMON);
        ('stuResolution', NET_A_RESOLUTION_INFO),  # 对应图片的分辨率;(the resolution of relative picture);
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('nEventType', C_UINT),  # 事件类型掩码，bit0表示报警事件，bit1表示违章事件。若bit0和bit1都置位则既是报警事件又是违章事件，默认bit0置位，报警事件;Event type mask, bit0 indicates alarm event, bit1 indicates violation event. If both bit0 and bit1 are set, it is both an alarm event and a violation event. By default, bit0 is set, and an alarm event occurs.;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # 事件公共扩展字段结构体;Event public extension field structure;
        ('byReserved', C_BYTE * 1020),  # 保留字节;Reserved;
    ]

class NET_A_DEV_EVENT_SPILLEDMATERIAL_DETECTION_INFO(Structure):
    """
    事件类型 EVENT_IVS_SPILLEDMATERIAL_DETECTION (抛洒物检测事件)对应数据块描述信息
    EVENT_IVS_SPILLEDMATERIAL_DETECTION Event info data
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;ChannelId;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('bReserved', c_char * 4),  # 字节对齐;byte alignment;
        ('PTS', c_double),  # 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # 事件ID;event ID;
        ('stuObjects', SDK_MSG_OBJECT_EX * 100),  # 检测到的物体;Objects;
        ('nObjectNum', c_int),  # 检测到的物体数量;The number of objects;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('stuDetectLine', NET_POINT * 20),  # 规则检测线;rule detect line;
        ('nDetectLineNum', c_int),  # 规则检测线顶点数;rule detect line's point number;
        ('stuTrackLine', NET_POINT * 20),  # 物体运动轨迹;object moveing track;
        ('nTrackLineNum', c_int),  # 物体运动轨迹顶点数;object moveing track's point number;
        ('bEventAction', C_BYTE),  # 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;event action,0 pulse,1 durable events begin, 2 durable events end;
        ('bReserved1', C_BYTE * 3),  # 保留字节;reserved;
        ('emDirection', C_ENUM),  # 表示入侵方向,（nObjectNum > 0时此字段无效，由stuObjects格式下emPersonDirection字段代替） Refer: EM_A_NET_CROSSLINE_DIRECTION_INFO;Direction,( if nObjectNum > 0 please use emPersonDirection which in stuObjects ) Refer: EM_A_NET_CROSSLINE_DIRECTION_INFO;
        ('nImageIndex', c_int),  # 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('nSourceIndex', c_int),  # 事件源设备上的index,-1表示数据无效,-1表示数据无效;the source device's index,-1 means data in invalid;
        ('szSourceDevice', c_char * 260),  # 事件源设备唯一标识,字段不存在或者为空表示本地设备;the source device's sign(exclusive),field said local device does not exist or is empty;
        ('nOccurrenceCount', C_UINT),  # 事件触发累计次数;event trigger accumulated times;
        ('stuIntelliCommInfo', EVENT_INTELLI_COMM_INFO),  # 智能事件公共信息;intelli comm info;
        ('stuExtensionInfo', NET_EXTENSION_INFO),  # 扩展信息;Extension info;
        ('byReserved', C_BYTE * 1028),  # 保留字节,留待扩展.;reserved;
    ]

class NET_A_DEV_EVENT_TRAFFIC_SERPENTINE_CHANGE_LANE_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_SERPENTINE_CHANGE_LANE (蛇形变道事件)对应的数据块描述信息
    The description information of the data block corresponding to the event type EVENT_IVS_TRAFFIC_SERPENTINE_CHANGE_LANE (Traffic Serpentine Change Lane event)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel number;
        ('nAction', c_int),  # 事件动作 0:脉冲;Action, 0:pulse,1:start, 2:stop;
        ('szName', c_char * 128),  # 事件名称;Event Name;
        ('nGroupID', c_int),  # GroupID事件组ID，同一物体抓拍过程内GroupID相同;group ID, which is the same in the process of capturing the same object;
        ('nCountInGroup', c_int),  # CountInGroup一个事件组内的抓拍张数;CountInGroup Number of snapshots in an event group;
        ('nIndexInGroup', c_int),  # IndexInGroup一个事件组内的抓拍序号，从1开始;IndexInGroup Capture sequence number in an event group,Start with 1;
        ('nUTCMS', C_UINT),  # 事件时间毫秒数;Time of occurrence in milliseconds;
        ('dbPTS', c_double),  # 相对事件时间戳,(单位是毫秒);Relative event timestamp in milliseconds;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间;Time of occurrence;
        ('nEventID', C_UINT),  # 事件ID;Event ID;
        ('nEventType', C_UINT),  # 事件类型掩码，bit0表示报警事件，bit1表示违章事件。若bit0和bit1都置位则既是报警事件又是违章事件，默认bit0置位，报警事件;Event type mask, bit0 represents an alarm event, and bit1 represents a violation event. If both bit0 and bit1 are set, it is both an alarm event and a violation event, By default bit0 is set, alarm event;
        ('emTriggerType', C_ENUM),  # 触发类型 Refer: EM_TRIGGER_TYPE;Trigger type Refer: EM_TRIGGER_TYPE;
        ('nMark', c_int),  # 用于标记抓拍帧;Used to mark capture frames;
        ('nSource', c_int),  # 视频分析的数据源地址;Data source address of video analysis;
        ('nFrameSequence', c_int),  # 视频分析帧序号;Sequence number of video analysis frame;
        ('nLane', c_int),  # 对应车道号;Corresponding lane number;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;Indicates the capture sequence number. For example, 3,2,1,1 indicates the end of capture, and 0 indicates the abnormal end;
        ('nSpeed', c_int),  # 车速，单位km/h;Vehicle speed in km / h;
        ('stuObject', NET_A_MSG_OBJECT),  # 车牌信息;License plate information;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;Body information;
        ('stuTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle information;
        ('stuCommInfo', EVENT_COMM_INFO),  # 公共信息;Public information;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS位置信息;GPS information;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;Event corresponding file information;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;Capture flag (bitwise), see NET_RESERVED_COMMON for details;
        ('szReserved', c_char * 1024),  # 预留字节;Reserved;
    ]

class NET_A_DEV_EVENT_TRAFFIC_CHANGE_LANE_CONTINUES_INFO(Structure):
    """
    事件类型EVENT_IVS_TRAFFIC_CHANGE_LANE_CONTINUES (机动车连续变道违法事件)对应的数据块描述信息
    The description of the data block corresponding to the event type EVENT_IVS_TRAFFIC_CHANGE_LANE_CONTINUES
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel ID;
        ('nAction', c_int),  # 0:脉冲;Action, 0:pulse,1:start, 2:stop;
        ('szName', c_char * 128),  # 事件名称;Event Name;
        ('dbPTS', c_double),  # 时间戳(单位是毫秒);PTS;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间;UTC;
        ('nEventID', c_int),  # 事件ID;EventID;
        ('nGroupID', c_int),  # nGroupID事件组ID,同一物体抓拍过程内nGroupID相同;Group ID;
        ('nCountInGroup', c_int),  # nCountInGroup一个事件组内的抓拍张数;Count In Group;
        ('nIndexInGroup', c_int),  # IndexInGroup一个事件组内的抓拍序号;Index In Group;
        ('nEventType', C_UINT),  # 事件类型掩码, bit0表示报警事件, bit1表示违章事件. 若bit0和bit1都置位则既是报警事件又是违章事件, 无该字段默认该事件是报警事件;EventType, Bit0 indicates an alarm event, bit1 indicates a violation event. If both bit0 and bit1 are set, it is both an alarm event and a violation event. Without this field, the event is an alarm event by default;
        ('stuObject', NET_A_MSG_OBJECT),  # 车牌信息;License plate information;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;Body information;
        ('emTriggerType', C_ENUM),  # TriggerType:触发类型,0车检器,1雷达,2视频 Refer: EM_TRIGGER_TYPE;TriggerType:0 vehicle detector, 1 radar, 2 video Refer: EM_TRIGGER_TYPE;
        ('nMark', c_int),  # 底层产生的触发抓拍帧标记;Mark;
        ('nSource', c_int),  # 视频分析的数据源地址;Source;
        ('nFrameSequence', c_int),  # 视频分析帧序号;Frame Sequence;
        ('nLane', c_int),  # 对应车道号;Line;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;Sequence;
        ('nSpeed', c_int),  # 车速，单位km/h;Speed,unit:km/h;
        ('stuTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle information;
        ('stuCommInfo', EVENT_COMM_INFO),  # 公共信息;Common Info;
        ('stuGPSInfo', NET_GPS_INFO),  # GPS信息;GPS Info;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;Event corresponding file information;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;Capture flag (bitwise), see NET_RESERVED_COMMON for details;
        ('szReserved', c_char * 1024),  # 保留字节,留待扩展;Reserved;
    ]

class NET_A_DEV_EVENT_TRAFFIC_ROAD_ALERT_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_ROAD_ALERT(道路安全预警)对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_TRAFFIC_ROAD_ALERT
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;channel id;
        ('nAction', c_int),  # 0:脉冲;0:pulse;
        ('szName', c_char * 128),  # 事件名称;event name;
        ('PTS', c_double),  # 时间戳(单位是毫秒);Time stamp(ms);
        ('UTC', NET_TIME_EX),  # 事件发生的时间;Event occurred time;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('stuObject', NET_A_MSG_OBJECT),  # 车牌信息;plate info;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;car body info;
        ('stTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic car info;
        ('nGroupID', c_int),  # 事件组ID，同一辆车抓拍过程内GroupID相同;Event group ID;
        ('nCountInGroup', c_int),  # 一个事件组内的抓拍张数;snap amount of one event group;
        ('nIndexInGroup', c_int),  # 一个事件组内的抓拍序号;snap index of one event group;
        ('nLane', c_int),  # 对应车道号;Corresponding lane number;
        ('stCommInfo', EVENT_COMM_INFO),  # 公共信息;public info;
        ('stFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;event file info;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1. 1表示抓拍结束,0表示异常结束;snap index,such as 3,2,1, 1 means the last one,0 means there has some exception and snap stop;
        ('byReserved', C_BYTE * 1020),  # 预留字段;reserved;
    ]

class NET_A_DEV_EVENT_TRAFFIC_LARGECAR_NO_STOP_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_LARGECAR_NO_STOP (大车右转不停车事件)对应的数据块描述信息
    The description information of the data block corresponding to the event type EVENT_IVS_TRAFFIC_LARGECAR_NO_STOP (Event of crane turning right without stopping)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel number;
        ('nAction', c_int),  # 0:脉冲,1:开始, 2:停止;Action, 0:pulse,1:start, 2:stop;
        ('szName', c_char * 128),  # 事件名称;Event Name;
        ('szClass', c_char * 16),  # 智能事件所属大类;Category of intelligent events;
        ('nGroupID', c_int),  # GroupID事件组ID，同一物体抓拍过程内GroupID相同;group ID, which is the same in the process of capturing the same object;
        ('nCountInGroup', c_int),  # CountInGroup一个事件组内的抓拍张数;CountInGroup Number of snapshots in an event group;
        ('nIndexInGroup', c_int),  # IndexInGroup一个事件组内的抓拍序号，从1开始;IndexInGroup Capture sequence number in an event group,Start with 1;
        ('nUTCMS', C_UINT),  # 事件时间毫秒数;Time of occurrence in milliseconds;
        ('dbPTS', c_double),  # 相对事件时间戳,(单位是毫秒);Relative event timestamp in milliseconds;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间;Time of occurrence;
        ('nEventID', C_UINT),  # 事件ID;Event ID;
        ('emTriggerType', C_ENUM),  # 触发类型 Refer: EM_TRIGGER_TYPE;Trigger type Refer: EM_TRIGGER_TYPE;
        ('nMark', c_int),  # 用于标记抓拍帧;Used to mark capture frames;
        ('nSource', c_int),  # 视频分析的数据源地址;Data source address of video analysis;
        ('nFrameSequence', c_int),  # 视频分析帧序号;Sequence number of video analysis frame;
        ('nLane', c_int),  # 对应车道号;Corresponding lane number;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;Indicates the capture sequence number. For example, 3,2,1,1 indicates the end of capture, and 0 indicates the abnormal end;
        ('nSpeed', c_int),  # 车速，单位km/h;Vehicle speed in km / h;
        ('stuObject', NET_A_MSG_OBJECT),  # 车牌信息;License plate information;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;Body information;
        ('stuTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle information;
        ('stuCommInfo', EVENT_COMM_INFO),  # 公共信息;Public information;
        ('stuGPSStatus', NET_GPS_STATUS_INFO),  # GPS状态;GPS status;
        ('szReserved', c_char * 1024),  # 预留字节;Reserved;
    ]

class NET_A_DEV_EVENT_TRAFFIC_CROSSING_SPEEDY_INFO(Structure):
    """
    事件类型 EVENT_IVS_TRAFFIC_CROSSING_SPEEDY (斑马线不减速事件)对应的数据块描述信息
    The description information of the data block corresponding to the event type EVENT_IVS_TRAFFIC_CROSSING_SPEEDY (Zebra crossing non deceleration event)
    """
    _fields_ = [
        ('nChannelID', c_int),  # 通道号;Channel number;
        ('nAction', c_int),  # 0:脉冲,1:开始, 2:停止;Action, 0:pulse,1:start, 2:stop;
        ('szName', c_char * 128),  # 事件名称;Event Name;
        ('szClass', c_char * 16),  # 智能事件所属大类;Category of intelligent events;
        ('nGroupID', c_int),  # GroupID事件组ID，同一物体抓拍过程内GroupID相同;group ID, which is the same in the process of capturing the same object;
        ('nCountInGroup', c_int),  # CountInGroup一个事件组内的抓拍张数;CountInGroup Number of snapshots in an event group;
        ('nIndexInGroup', c_int),  # IndexInGroup一个事件组内的抓拍序号，从1开始;IndexInGroup Capture sequence number in an event group,Start with 1;
        ('nUTCMS', C_UINT),  # 事件时间毫秒数;Time of occurrence in milliseconds;
        ('dbPTS', c_double),  # 相对事件时间戳,(单位是毫秒);Relative event timestamp in milliseconds;
        ('stuUTC', NET_TIME_EX),  # 事件发生的时间;Time of occurrence;
        ('nEventID', C_UINT),  # 事件ID;Event ID;
        ('emTriggerType', C_ENUM),  # 触发类型 Refer: EM_TRIGGER_TYPE;Trigger type Refer: EM_TRIGGER_TYPE;
        ('nMark', c_int),  # 用于标记抓拍帧;Used to mark capture frames;
        ('nSource', c_int),  # 视频分析的数据源地址;Data source address of video analysis;
        ('nFrameSequence', c_int),  # 视频分析帧序号;Sequence number of video analysis frame;
        ('nLane', c_int),  # 对应车道号;Corresponding lane number;
        ('nSequence', c_int),  # 表示抓拍序号,如3,2,1,1表示抓拍结束,0表示异常结束;Indicates the capture sequence number. For example, 3,2,1,1 indicates the end of capture, and 0 indicates the abnormal end;
        ('nSpeed', c_int),  # 车速，单位km/h;Vehicle speed in km / h;
        ('stuObject', NET_A_MSG_OBJECT),  # 车牌信息;License plate information;
        ('stuVehicle', NET_A_MSG_OBJECT),  # 车身信息;Body information;
        ('stuTrafficCar', DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO),  # 交通车辆信息;Traffic vehicle information;
        ('stuCommInfo', EVENT_COMM_INFO),  # 公共信息;Public information;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # 事件对应文件信息;Event corresponding file information;
        ('dwSnapFlagMask', C_DWORD),  # 抓图标志(按位),具体见NET_RESERVED_COMMON;Capture flag (bitwise), see NET_RESERVED_COMMON for details;
        ('szReserved', c_char * 1024),  # 预留字节;Reserved;
    ]

class NET_IN_TRAFFICFLUXSTAT(Structure):
    """
    接口(CLIENT_StartTrafficFluxStat)输入参数
    CLIENT_StartTrafficFluxStat's input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小;structure size;
        ('cbData', CB_FUNCTYPE(c_int, C_LLONG, C_DWORD, c_void_p, POINTER(C_BYTE), C_DWORD, C_LDWORD, c_int, c_void_p)),  # 回调函数指针;callback function pointer;
        ('dwUser', C_LDWORD),  # 用户数据;user data;
    ]

class NET_OUT_TRAFFICFLUXSTAT(Structure):
    """
    接口(CLIENT_StartTrafficFluxStat)输出参数
    CLIENT_StartTrafficFluxStat's output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小;structure size;
    ]

class NET_A_ALARM_ACCESS_CTL_STATUS_INFO(Structure):
    """
    门禁状态事件
    Access control status event
    """
    _fields_ = [
        ('dwSize', C_DWORD),  
        ('nDoor', c_int),  # 门通道号;Door channel no.;
        ('stuTime', NET_TIME),  # 事件发生的时间;Event time;
        ('emStatus', C_ENUM),  # 门禁状态 Refer: EM_A_NET_ACCESS_CTL_STATUS_TYPE;Access control status Refer: EM_A_NET_ACCESS_CTL_STATUS_TYPE;
        ('szSerialNumber', c_char * 256),  # 无线设备序列号(智能锁);wireless device serial number(Intelligent lock);
        ('bRealUTC', C_BOOL),  # RealUTC 是否有效，bRealUTC 为 TRUE 时，用 RealUTC，否则用 stuTime 字段;whether RealUTC is valid. when bRealUTC is TRUE, use RealUTC, otherwise use stuTime;
        ('RealUTC', NET_TIME_EX),  # 事件发生的时间（标准UTC）;event occur time;
    ]

class NET_VEHICLE_INOUT_ANALYSE_PROC(Structure):
    """
    智能分析结果的信息
    Real time traffic flow information
    """
    _fields_ = [
        ('szName', c_char * 128),  # 事件名称;Event Name;
        ('dbPTS', c_double),  # 时间戳(单位是毫秒);Timestamp (in milliseconds);
        ('stuUTC', NET_TIME_EX),  # 发生的时间;Time of occurrence;
        ('nEventID', c_int),  # 事件ID;Event ID;
        ('nSequence', C_UINT),  # 包序号,用于校验是否丢包;Sequence;
        ('nFrameSequence', c_int),  # 视频分析帧序号;Frame Sequence;
        ('pstuObjets', POINTER(NET_VEHICLE_OBJECT)),  # 物体列表;Object Info;
        ('nObjectNum', c_int),  # 物体有效个数;Object Number;
        ('nStatNum', c_int),  # 统计有效个数;Stat Num;
        ('stuStats', NET_TRAFFIC_FLOW_STAT * 8),  # 各个车道实时交通流量统计信息, 最大支持8车道;Real-time traffic flow statistics for each lane, supporting a maximum of 8 lanes;
        ('dbRadarInstallAngle', c_double),  # 雷达安装角度（雷达坐标系Y轴与正北方向的逆时针夹角）单位：度 (0 ~ 360);Radar installation angle (counterclockwise included angle between the Y-axis of the radar coordinate system and the due north direction) Unit: degrees (0~360);
        ('szReserved', c_char * 2048),  # 保留字节;Reserved Byte;
    ]

class NET_IN_ATTACH_TRAFFIC_FLOW_STAT_REAL_FLOW(Structure):
    """
    CLIENT_AttachTrafficFlowStatRealFlow 输入参数
    CLIENT_AttachTrafficFlowStatRealFlow input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小,必须赋值;The size of this structure must be assigned a value;
        ('szReserved', c_char * 4),  # 字节对齐;Byte alignment;
        ('cbVehicleInOutAnalyseProc', CB_FUNCTYPE(None, C_LLONG, POINTER(NET_VEHICLE_INOUT_ANALYSE_PROC), C_LDWORD)),  # 回调函数;Callback func;
        ('dwUser', C_LDWORD),  # 用户信息;User Info;
    ]

class NET_OUT_ATTACH_TRAFFIC_FLOW_STAT_REAL_FLOW(Structure):
    """
    CLIENT_AttachTrafficFlowStatRealFlow 输出参数
    CLIENT_AttachTrafficFlowStatRealFlow output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小,必须赋值;The size of this structure must be assigned a value;
    ]

class NET_REGION_PEOPLE_STAT_INFO(Structure):
    """
    检测区区域人数统计信息
    Statistical information of the number of people in the testing area
    """
    _fields_ = [
        ('nRegionID', C_UINT),  # 区域ID;area ID;
        ('szRegionName', c_char * 128),  # 区域名称;area name;
        ('nRegionPointNum', C_UINT),  # 区域顶点个数;Number of regional vertices
        ('stuRegionPoint', NET_POINT * 20),  # 区域顶点坐标;Regional vertex coordinates;
        ('nPeopleNum', C_UINT), # 区域内人数;Number of people in the area;
        ('byReserved', c_char * 1024),  # 保留字节;Reserved Byte;
    ]
class NET_CROWD_STAT_DATA(Structure):
    """
    检测区统计信息
    Statistical information of detection area
    """
    _fields_ = [
        ('nChannelID', C_UINT),  # 通道号;channel ID;
        ('nGloabalPeopleNum', C_UINT),  # 检测区内总人数;Total number of people in the testing area;
        ('nRegionNum', C_UINT),  # 检测区内区域个数;Number of areas within the detection area;
        ('stuRegionPeople', NET_REGION_PEOPLE_STAT_INFO * 8),  # 检测区内区域人数统计信息;Statistical information of the number of people in the detection area;
        ('byReserved', c_char * 1024),  # 保留字节;Reserved Byte;
    ]

class NET_CB_CROWD_DISTRI_STREAM_INFO(Structure):
    """
    订阅人群分布图实时统回调信息
    Crowd Distri Map callback information
    """
    _fields_ = [
        ('nCrowStatNum', C_UINT),  # 检测区个数;Number of detection areas;
        ('stuCrowdStatData', NET_CROWD_STAT_DATA * 8),  # 检测区统计信息;Statistical information of detection area;
        ('byReserved', c_char * 2048),  # 保留字节;Reserved Byte;
    ]

class NET_IN_ATTACH_CROWDDISTRI_MAP_INFO(Structure):
    """
    CLIENT_AttachCrowdDistriMap 输入参数
    CLIENT_AttachCrowdDistriMap input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小,必须赋值;The size of this structure must be assigned a value;
        ('nChannelID', c_char * 4),  # 通道号;channel ID;
        ('cbCrowdDistriStream', CB_FUNCTYPE(None, C_LLONG, POINTER(NET_CB_CROWD_DISTRI_STREAM_INFO), C_LDWORD)),  # 回调函数;Callback func;
        ('dwUser', C_LDWORD),  # 用户信息;User Info;
    ]

class NET_OUT_ATTACH_CROWDDISTRI_MAP_INFO(Structure):
    """
    CLIENT_AttachCrowdDistriMap 输出参数
    CLIENT_AttachCrowdDistriMap output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # 此结构体大小,必须赋值;The size of this structure must be assigned a value;
    ]

class NET_A_DEV_EVENT_TUMBLE_DETECTION_INFO(Structure):
    """
    事件类型 EVENT_IVS_TUMBLE_DETECTION(倒地报警事件)对应数据块描述信息
    tumble detection event (command:EVENT_IVS_TUMBLE_DETECTION)
    """
    _fields_ = [
        ('nChannelID', c_int),  # / 通道号;channel ID;
        ('szName', c_char * 128),  # / 事件名称;event name;
        ('nAction', c_int),  # / 事件动作,1表示持续性事件开始,2表示持续性事件结束;;Event operation. 1: Start, 2: Stop;
        ('PTS', c_double),  # / 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # / 事件发生的时间;time of occurrence;
        ('nEventID', c_int),  # / 事件ID;event ID;
        ('UTCMS', c_int),  # / UTC时间对应的毫秒数;millseconds;
        ('emClassType', C_ENUM),  # / 智能事件所属大类 Refer: EM_CLASS_TYPE;class type Refer: EM_CLASS_TYPE;
        ('nObjectID', c_int),  # / 目标ID;Object ID;
        ('szObjectType', c_char * 16),  # / 物体类型,支持以下:/"Unknown", "Human", "Vehicle", "Fire", "Smoke", "Plate", "HumanFace",/ "Container", "Animal", "TrafficLight", "PastePaper", "HumanHead", "BulletHole", "Entity";Object Type, support for the following:"Unknown", "Human", "Vehicle","Fire", "Smoke", "Plate", "HumanFace","Container", "Animal", "TrafficLight", "PastePaper", "HumanHead", "BulletHole", "Entity";
        ('stuBoundingBox', NET_RECT),  # / 物体包围盒;Bounding Box;
        ('szSerialUUID', c_char * 22),  # / 智能物体全局唯一物体标识/ 有效数据位21位，包含’\0’/ 前2位%d%d:01-视频片段, 02-图片, 03-文件, 99-其他/ 中间14位YYYYMMDDhhmmss:年月日时分秒/ 后5位%u%u%u%u%u：物体ID，如00001;Intelligent object global unique object identificationValid data bits are 21 bits, including '\0'Top 2 bits %d%d: 01-video clip, 02-picture, 03-file, 99-otherMiddle 14 bit yyyymmddhhmmssLast 5 bits %U%U%U%U%U: object ID, such as 00001;
        ('stuSceneImage', SCENE_IMAGE_INFO),  # / 全景广角图;Panoramic wide-angle map;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX2)),  # / 图片信息数组;Image information array;
        ('nImageInfoNum', c_int),  # / 图片信息个数;Number of picture information;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # / 事件公共扩展字段结构体;Event public extension field structure;
        ('nDetectRegionNum', c_int),  # / 检测区个数;The number of vertices in the detection area;
        ('stuDetectRegion', NET_POINT * 20),  # / 检测区;Detection area,[0,8191];
        ('bReserved', C_BYTE * 834),  # / 保留字节;reserved;
    ]

class NET_A_HUMAN_IMAGE_INFO(Structure):
    """
    人体图片信息
    Human image info
    """
    _fields_ = [
        ('nOffSet', C_UINT),  # / 偏移;Offset;
        ('nLength', C_UINT),  # / 图片大小,单位字节;image length,Unit:byte;
        ('nWidth', C_UINT),  # / 图片宽度;Width;
        ('nHeight', C_UINT),  # / 图片高度;Height;
        ('nIndexInData', C_UINT),  # / 在上传图片数据中的图片序号;The serial number of the picture in the uploaded picture data;
        ('byReserved', C_BYTE * 52),  # / 预留字节;Reserved;
    ]

class NET_HELMET_ATTRIBUTE(Structure):
    """
    安全帽属性
    Attribute of helmet
    """
    _fields_ = [
        ('emHelmetState', C_ENUM),  # / 安全帽佩戴状态 Refer: EM_WORK_HELMET_STATE;The state of helmet Refer: EM_WORK_HELMET_STATE;
        ('emHelmetColor', C_ENUM),  # / 安全帽颜色 Refer: EM_CLOTHES_COLOR;Color of helmet Refer: EM_CLOTHES_COLOR;
        ('nHelmetFlag', C_UINT),  # / 报警类型: 0:未知, 1:达到触发速度的报警, 2:达到上报速度的报警, 3:两者同时达到;Helmet Flag: 0: unknown, 1: alarm reaching trigger speed, 2: alarm reaching report speed, 3: both;
        ('nReportFlag', c_int),  # / 报警上传标识 -1: 未知, 0: 未报警, 1: 报警,;Report Flag: -1: Unknown, 0: no alarm, 1: alarm,;
        ('nHasLegalHat', c_int),  # / 安全帽检测结果, 0-合规 1-不合规 2-未知;Helmet test results, 0-compliant 1-nonconforming 2-unknown;
        ('byReserved', C_BYTE * 1012),  # / 预留字节;Reserved;
    ]

class NET_LINK_GROUP_INFO(Structure):
    """
    联动报警的工装库信息
    Tool warehouse information for linkage alarm
    """
    _fields_ = [
        ('szGroupID', c_char * 128),  # / 联动报警的工装库ID;Group ID;
        ('szFeatureName', c_char * 128),  # / 联动报警特征名称;Feature Name;
        ('nSimilarity', C_UINT),  # / 联动报警库相似度;Similarity;
        ('nSampleAttributes', C_UINT),  # / 样本属性, 0: 未知, 1: 正样本 2: 负样本;Sampl Attributes, 0: Unknown, 1: Positive sample 2: Negative sample;
        ('szGroupName', c_char * 128),  # / 联动报警的工装库名称;Group Name;
        ('szReserved', c_char * 512),  # / 预留字节;Reserved byte;
    ]

class NET_WORKCLOTHES_ATTRIBUTE(Structure):
    """
    工作服属性
    Attribute of work clothes
    """
    _fields_ = [
        ('emWorkClothesState', C_ENUM),  # / 工作服穿戴状态 Refer: EM_WORKCLOTHES_STATE;The state of work clothes Refer: EM_WORKCLOTHES_STATE;
        ('emWorkClothColor', C_ENUM),  # / 工作服颜色 Refer: EM_CLOTHES_COLOR;Color of work clothes Refer: EM_CLOTHES_COLOR;
        ('emWorkClothesLegalState', C_ENUM),  # / 工作服合法状态 Refer: EM_CLOTHES_LEGAL_STATE;Work clothes legal state Refer: EM_CLOTHES_LEGAL_STATE;
        ('nLinkGroupInfoNum', c_int),  # / 联动报警的工装库信息个数;Number of Link Group Info;
        ('pstuLinkGroupInfo', POINTER(NET_LINK_GROUP_INFO)),  # / 联动报警的工装库信息;Link Group Info;
        ('emTrousersColor', C_ENUM),  # / 工作服裤子颜色 Refer: EM_CLOTHES_COLOR;Trousers Color Refer: EM_CLOTHES_COLOR;
        ('szReserved1', c_char * 4),  # / 字节对齐;byte alignment;
        ('nCutoutPolicy', C_UINT),  # / 优选方案, 0:未知,1:全身,2:上半身;Preferred solution, 0: Unknown, 1: Full body, 2: Upper body;
        ('byReserved', C_BYTE * (1004-sizeof(c_void_p))),  # / 预留字节;Reserved;
    ]

class NET_WORKPANTS_ATTRIBUTE(Structure):
    """
    工作裤属性
    Work pants attribute
    """
    _fields_ = [
        ('emWorkPantsState', C_ENUM),  # / 工作裤穿戴状态 Refer: EM_WORKPANTS_STATE;work pants state Refer: EM_WORKPANTS_STATE;
        ('emWorkPantsColor', C_ENUM),  # / 工作裤颜色 Refer: EM_CLOTHES_COLOR;work pants color Refer: EM_CLOTHES_COLOR;
        ('byReserved', C_BYTE * 1024),  # / 预留字节;reserved;
    ]

class NET_NORMALHAT_ATTRIBUTE(Structure):
    """
    普通帽子相关属性状态信息
    Normal hat related attribute status information
    """
    _fields_ = [
        ('emHasHat', C_ENUM),  # / 是否有戴普通帽 Refer: EM_WEARING_STATE;Whether a normal hat is worn Refer: EM_WEARING_STATE;
        ('emHasLegalHat', C_ENUM),  # / 帽子检测结果 Refer: EM_COMPLIANCE_STATE;hat detection result Refer: EM_COMPLIANCE_STATE;
    ]

class NET_MASK_ATTRIBUTE(Structure):
    """
    口罩相关属性状态信息
    Mask related attribute status information
    """
    _fields_ = [
        ('emHasMask', C_ENUM),  # / 是否有戴口罩 Refer: EM_WEARING_STATE;Whether there is a mask Refer: EM_WEARING_STATE;
        ('emHasLegalMask', C_ENUM),  # / 口罩检测结果 Refer: EM_COMPLIANCE_STATE;Mask detection result Refer: EM_COMPLIANCE_STATE;
    ]

class NET_APRON_ATTRIBUTE(Structure):
    """
    围裙相关属性状态信息
    Apron related property status information
    """
    _fields_ = [
        ('emHasApron', C_ENUM),  # / 是否有穿围裙 Refer: EM_WEARING_STATE;Whether you are wearing an apron Refer: EM_WEARING_STATE;
        ('emHasLegalApron', C_ENUM),  # / 围裙检测结果 Refer: EM_COMPLIANCE_STATE;apron detection result Refer: EM_COMPLIANCE_STATE;
    ]

class NET_GLOVE_ATTRIBUTE(Structure):
    """
    手套相关属性状态信息
    Glove related attribute status information
    """
    _fields_ = [
        ('emHasGlove', C_ENUM),  # / 是否有戴手套 Refer: EM_WEARING_STATE;Whether you are wearing gloves Refer: EM_WEARING_STATE;
        ('emHasLegalGlove', C_ENUM),  # / 手套检测结果 Refer: EM_COMPLIANCE_STATE;Glove test result Refer: EM_COMPLIANCE_STATE;
    ]

class NET_BOOT_ATTRIBUTE(Structure):
    """
    靴子相关属性状态信息
    Boot related property status information
    """
    _fields_ = [
        ('emHasBoot', C_ENUM),  # / 是否有穿靴子 Refer: EM_WEARING_STATE;Whether there are boots Refer: EM_WEARING_STATE;
        ('emHasLegalBoot', C_ENUM),  # / 靴子检测结果 Refer: EM_COMPLIANCE_STATE;Boot detection result Refer: EM_COMPLIANCE_STATE;
    ]

class NET_SHOESCOVER_ATTRIBUTE(Structure):
    """
    鞋套相关属性状态信息
    Shoe cover related attribute status information
    """
    _fields_ = [
        ('emHasCover', C_ENUM),  # / 是否有穿鞋套 Refer: EM_WEARING_STATE;Whether there is a shoe cover Refer: EM_WEARING_STATE;
        ('emHasLegalCover', C_ENUM),  # / 鞋套检测结果 Refer: EM_COMPLIANCE_STATE;shoe cover detection result Refer: EM_COMPLIANCE_STATE;
    ]

class NET_NOHAT_ATTRIBUTE(Structure):
    """
    无帽子相关属性状态信息
    No hat related property status information
    """
    _fields_ = [
        ('emHasHat', C_ENUM),  # / 是否有戴帽子 Refer: EM_WEARING_STATE;Whether there is a hat Refer: EM_WEARING_STATE;
        ('emHasLegalHat', C_ENUM),  # / 帽子检测结果 Refer: EM_COMPLIANCE_STATE;hat detection result Refer: EM_COMPLIANCE_STATE;
    ]

class NET_PROHELMET_ATTRIBUTE(Structure):
    """
    防护面罩相关属性状态信息
    Relevant attribute status information of protective mask
    """
    _fields_ = [
        ('emHasHat', C_ENUM),  # / 是否有戴防护面罩 Refer: EM_WEARING_STATE;Are you wearing a protective mask Refer: EM_WEARING_STATE;
        ('emHatColor', C_ENUM),  # / 帽子颜色 Refer: EM_CLOTHES_COLOR;Hat color Refer: EM_CLOTHES_COLOR;
        ('szReserved', c_char * 128),  # / 预留字节;Reserved;
    ]

class NET_FIREPROOF_CLOTHES(Structure):
    """
    防火衣相关属性状态信息
    Relevant attribute status information of fireproof clothing
    """
    _fields_ = [
        ('emHasFireProofClothes', C_ENUM),  # / 是否穿着防火衣 Refer: EM_FIREPROOF_CLOTHES_STATE;Whether there is a FireProofClothes Refer: EM_FIREPROOF_CLOTHES_STATE;
        ('emFireProofClothesColor', C_ENUM),  # / 防火衣颜色 Refer: EM_CLOTHES_COLOR;FireProofClothes color Refer: EM_CLOTHES_COLOR;
        ('szReserved', c_char * 128),  # / 预留字节;Reserved;
    ]

class NET_GLASSES_RELATED_INFO(Structure):
    """
    眼镜相关属性状态信息
    Indicates the status of glasses related properties
    """
    _fields_ = [
        ('emGlassesType', C_ENUM),  # / 眼镜检测规则中报警类型 Refer: EM_GLASSES_RULE_TYPE;Alarm type in glasses detection rules Refer: EM_GLASSES_RULE_TYPE;
        ('nGlassesLegalMask', c_int),  # / 眼镜检测结果, 0-合规 1-不合规 2-未知;Glasses test result: 0- compliant 1- non-compliant 2- unknown;
        ('szReserved', c_char * 64),  # / 预留字节;Reserve bytes;
    ]

class NET_BREATHING_MASK_INFO(Structure):
    """
    呼吸面罩相关属性状态信息
    Indicates the status of glasses related properties
    """
    _fields_ = [
        ('nHasLegalBreathingMask', c_int),  # / 呼吸面罩检测结果, 0:未知，1:不合规，2:合规;Respirator test results, 0: unknown, 1: non compliant, 2: compliant;
        ('nHasBreathingMask', c_int),  # / 是否有穿着呼吸面罩, 0: 未知 1: 没有 2: 有;Whether wearing a breathing mask, 0: unknown 1: no 2: yes;
        ('byReserved', c_char * 56),  # / 预留字节;Reserve bytes;
    ]

class NET_PROTECTIVE_SUIT_INFO(Structure):
    """
    防护服相关属性状态信息
    Relevant attribute status information of protective clothing
    """
    _fields_ = [
        ('nHasProtectiveSuit', c_int),  # / 是否有穿着防护服, 0: 未知, 1: 没有, 2: 有, 3:不存在指定颜色的防护服;Whether wearing protective Suit, 0: Unknown, 1: None, 2: Yes, 3: No protective clothing of the specified color exists;
        ('emProtectiveSuitColor', C_ENUM),  # / 防护服颜色 Refer: EM_CLOTHES_COLOR;Protective Suit Color Refer: EM_CLOTHES_COLOR;
        ('szReserved', c_char * 24),  # / 预留字节;Reserved byte;
    ]

class NET_UNIFORM_INFO(Structure):
    """
    制服相关属性状态信息
    Status information of uniform related attributes
    """
    _fields_ = [
        ('nHasUniform', c_int),  # / 是否有穿着制服, 0: 未知, 1: 没有, 2: 有, 3:不存在指定颜色制服;Whether wearing uniform, 0: Unknown, 1: None, 2: Yes, 3: No uniform of the specified color exists;
        ('emUniformColor', C_ENUM),  # / 制服颜色 Refer: EM_CLOTHES_COLOR;Uniform Color Refer: EM_CLOTHES_COLOR;
        ('szReserved', c_char * 24),  # / 预留字节;Reserved byte;
    ]

class NET_SAFETY_ROPE_INFO(Structure):
    """
    安全绳相关属性状态信息
    Status information of relevant properties of safety ropes
    """
    _fields_ = [
        ('nCompliantType', c_int),  # / 佩戴带安全绳是否合规, 0-不合规 1-合规 2-未知;Whether the safety rope is in compliance, 0 - non-compliance 1 - compliance 2 - unknown;
        ('szReserved', c_char * 28),  # / 预留字节;Reserved byte;
    ]

class NET_SAFE_BELT_INFO(Structure):
    """
    安全带相关属性状态信息
    Safety belt related attribute status information
    """
    _fields_ = [
        ('nHasSafeBelt', c_int),  # / 是否穿安全带 , 0:未知，1:未穿安全带，2:穿了安全带;Whether to wear safety belt, 0: unknown, 1: not wearing safety belt, 2: wearing safety belt;
        ('nHasLegalSafeBelt', c_int),  # / 安全带检测结果, 0-合规 1-不合规 2-未知;Safety belt test result, 0-compliant 1-noncompliant 2-unknown;
        ('szReserved', c_char * 24),  # / 预留字节;Reserved byte;
    ]

class NET_VEST_INFO(Structure):
    """
    反光背心相关属性状态信息
    Reflective vest related attribute status information
    """
    _fields_ = [
        ('nHasVest', c_int),  # / 是否穿反光背心, 0:未知，1:未穿反光背心，2:穿了反光背心;Whether to wear reflective vest, 0: unknown, 1: no reflective vest, 2: reflective vest;
        ('nHasLegalVest', c_int),  # / 反光背心检测结果, 0-合规 1-不合规 2-未知;Reflective vest test result, 0-compliant 1-nonconforming 2-unknown;
        ('szReserved', c_char * 24),  # / 预留字节;Reserved byte;
    ]

class NET_SAFETY_SHOES_INFO(Structure):
    """
    劳保鞋相关属性状态信息
    Attribute status information about labor protection shoes
    """
    _fields_ = [
        ('nHasSafetyShoes', c_int),  # / 是否穿劳保鞋, 0:未知，1:未穿劳保鞋，2:穿了劳保鞋;Whether to wear labor protection shoes, 0: unknown, 1: no labor protection shoes, 2: wear labor protection shoes;
        ('nHasLegalSafetyShoes', c_int),  # / 劳保鞋检测结果 , 0-合规 1-不合规 2-未知;Test result of labor protection shoes, 0- compliance 1- non-compliance 2- unknown;
        ('szReserved', c_char * 24),  # / 预留字节;Reserve bytes;
    ]

class NET_WRIST_GUARD_INFO(Structure):
    """
    防割护腕相关属性状态信息
    Attribute status information about the anti-cutting wrist guard
    """
    _fields_ = [
        ('nHasWristGuard', c_int),  # / 是否穿防割护腕, 0:未知，1:未穿防割护腕，2:穿了防割护腕;0: unknown, 1: not worn, and 2: Yes;
        ('nHasLegalWristGuard', c_int),  # / 防割护腕检测结果 , 0-合规 1-不合规 2-未知;Test result of anti-cutting wrist guard: 0- compliant 1- non-compliant 2- unknown;
        ('szReserved', c_char * 24),  # / 预留字节;Reserve bytes;
    ]

class NET_A_DEV_EVENT_WORKCLOTHES_DETECT_INFO(Structure):
    """
    事件类型EVENT_IVS_WORKCLOTHES_DETECT(工装(安全帽/工作服等)检测事件)对应的数据块描述信息
    Corresponding to data block description of event type EVENT_IVS_WORKCLOTHES_DETECT (work clothes(helmet/clothes)detection)
    """
    _fields_ = [
        ('nChannelID', c_int),  # / 通道号;Channel ID;
        ('nAction', c_int),  # / 0:脉冲 1:开始 2:停止;Event action, 0: Pulse, 1: Start, 2: Stop;
        ('szName', c_char * 128),  # / 事件名称;Event name;
        ('PTS', c_double),  # / 时间戳(单位是毫秒);Timestamp (in milliseconds);
        ('UTC', NET_TIME_EX),  # / 事件发生的时间;Time for the event occurred;
        ('nEventID', C_UINT),  # / 事件ID;Event ID;
        ('emClassType', C_ENUM),  # / 智能事件所属大类 Refer: EM_CLASS_TYPE;Class type Refer: EM_CLASS_TYPE;
        ('nRuleID', C_UINT),  # / 智能事件规则编号，用于标示哪个规则触发的事件;Rule ID;
        ('nObjectID', C_UINT),  # / 物体ID;Object ID;
        ('nGroupID', C_UINT),  # / 事件组ID，一次检测的多个nGroupID相同;Event group ID,A detection of multiple workclothes detectionat the same nGroupID;
        ('nCountInGroup', C_UINT),  # / 一个事件组内的抓拍张数,一次检测的多个nCountInGroup相同;the captured workclothes number within an event group,A detection of multiple workclothes detection at the same nCountInGroup;
        ('nIndexInGroup', C_UINT),  # / 一个事件组内的抓拍序号，从1开始;capture Index of an event group,starting from 1;
        ('stuSceneImage', SCENE_IMAGE_INFO),  # / 全景大图信息;Scene image info;
        ('stuHumanImage', NET_A_HUMAN_IMAGE_INFO),  # / 小图信息;image info;
        ('stuHelmetAttribute', NET_HELMET_ATTRIBUTE),  # / 安全帽属性;Helmet attribute;
        ('stuWorkClothesAttribute', NET_WORKCLOTHES_ATTRIBUTE),  # / 工作服属性;Work clothes attribute;
        ('stuWorkPantsAttribute', NET_WORKPANTS_ATTRIBUTE),  # / 工作裤颜色;Work pants attribute;
        ('nAlarmType', c_int),  # / 不规范报警类型 0-未知 1-防护服不规范 2: 工作服不规范3:安全帽不规范4:安全帽和工作服不规范;Unstandard alarm type 0-unknown 1-Protective clothing no standard 2: Work clothes no standard 3:Helmet no standard 4:Work clothes and Helmet no standard;
        ('szSourceID', c_char * 32),  # / 事件关联ID。应用场景是同一个物体或者同一张图片做不同分析，产生的多个事件的SourceID相同/ 格式：类型+时间+序列号，其中类型2位，时间14位，序列号5位/ 类型：02-图像 时间：YYYYMMDDhhmmss 序列号：00001;Event source ID. When the same object or the same image is analyzed differently, the source ID of multiple events generated is the sameFormat: type + time + serial number, type 2, time 14, serial number 5Type: 02 image time: yyyymmddhhmmss serial number: 00001;
        ('emRuleType', C_ENUM),  # / 报警规则类型 Refer: EM_EVENT_WORKCLOTHES_RULE_TYPE;Rule type of work clothes(helmet/clothes)detection Refer: EM_EVENT_WORKCLOTHES_RULE_TYPE;
        ('stuImageInfo', NET_IMAGE_INFO_EX2 * 32),  # / 图片信息数组;image information array;
        ('nImageInfoNum', c_int),  # / 图片信息个数;Number of image information;
        ('stuNormalHat', NET_NORMALHAT_ATTRIBUTE),  # / 普通帽子相关属性状态信息;Normal hat related attribute status information;
        ('stuMask', NET_MASK_ATTRIBUTE),  # / 口罩相关属性状态信息;Mask related attribute status information;
        ('stuApron', NET_APRON_ATTRIBUTE),  # / 围裙相关属性状态信息;Apron related attribute status information;
        ('stuGlove', NET_GLOVE_ATTRIBUTE),  # / 手套相关属性状态信息;Glove related attribute status information;
        ('stuBoot', NET_BOOT_ATTRIBUTE),  # / 靴子相关属性状态信息;Boot related attribute status information;
        ('stuShoesCover', NET_SHOESCOVER_ATTRIBUTE),  # / 鞋套相关属性状态信息;Shoe cover related attribute status information;
        ('stuNoHat', NET_NOHAT_ATTRIBUTE),  # / 无帽子相关属性状态信息;No hat related attribute status information;
        ('stuProhelmet', NET_PROHELMET_ATTRIBUTE),  # / 防护面罩相关属性状态信息;Relevant attribute status information of protective mask;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # / 事件公共扩展字段结构体;Event public extension field structure;
        ('stuFireProofClothes', NET_FIREPROOF_CLOTHES),  # / 防火衣相关属性状态信息;Relevant attribute status information of fireproof clothing;
        ('pstObjectInfo', POINTER(NET_A_MSG_OBJECT_EX2)),  # / 物体信息数据;object info data;
        ('nObjectNum', C_UINT),  # / 物体信息数;object info number;
        ('stuGlassesInfo', NET_GLASSES_RELATED_INFO),  # / 眼镜相关属性状态信息;Glasses info;
        ('stuBreathingMaskInfo', NET_BREATHING_MASK_INFO),  # / 呼吸面罩相关属性状态信息;Status information of respiratory mask related attributes;
        ('stuProtectiveSuitInfo', NET_PROTECTIVE_SUIT_INFO),  # / 防护服相关属性状态信息;Relevant attribute status information of protective clothing;
        ('stuUniformInfo', NET_UNIFORM_INFO),  # / 制服相关属性状态信息;Status information of uniform related attributes;
        ('stuSafetyRopeInfo', NET_SAFETY_ROPE_INFO),  # / 安全绳相关属性状态信息;Status information of relevant properties of safety ropes;
        ('stuSafeBeltInfo', NET_SAFE_BELT_INFO),  # / 安全带相关属性状态信息;Safety belt related attribute status information;
        ('stuVestInfo', NET_VEST_INFO),  # / 反光背心相关属性状态信息;Reflective vest related attribute status information;
        ('stuSafetyShoesInfo', NET_SAFETY_SHOES_INFO),  # / 劳保鞋相关属性状态信息;Safety shoes info;
        ('stuWristGuardInfo', NET_WRIST_GUARD_INFO),  # / 防割护腕相关属性状态信息;Wrist guard info;
        ('nLegalAlarmType', C_UINT),  # / 报警方式, 0:未知, 1:有不合规项即报警 2:所有合规才报警;Legal Alarm Type, 0: Unknown, 1: Alarm if there are non compliant items, 2: Alarm only if all comply;
        ('bHelmet', c_bool),  # / 是否上报了Helmet属性;Has the Helmet attribute been reported;
        ('bClothes', c_bool),  # / 是否上报了Clothes属性;Has the Clothes attribute been reported;
        ('bWorkPants', c_bool),  # / 是否上报了WorkPants属性;Has the WorkPants attribute been reported;
        ('bNormalHat', c_bool),  # / 是否上报了NormalHat属性;Has the NormalHat attribute been reported;
        ('bMask', c_bool),  # / 是否上报了Mask属性;Has the Mask attribute been reported;
        ('bApron', c_bool),  # / 是否上报了Apron属性;Has the Apron attribute been reported;
        ('bGlove', c_bool),  # / 是否上报了Glove属性;Has the Glove attribute been reported;
        ('bBoot', c_bool),  # / 是否上报了Boot属性;Has the Boot attribute been reported;
        ('bShoesCover', c_bool),  # / 是否上报了ShoesCover属性;Has the ShoesCover attribute been reported;
        ('bNoHat', c_bool),  # / 是否上报了NoHat属性;Has the NoHat attribute been reported;
        ('bProhelmet', c_bool),  # / 是否上报了Prohelmet属性;Has the Prohelmet attribute been reported;
        ('bGlasses', c_bool),  # / 是否上报了Glasses属性;Has the Glasses attribute been reported;
        ('bFireProofClothes', c_bool),  # / 是否上报了FireProofClothes属性;Has the FireProofClothes attribute been reported;
        ('bProtectiveSuit', c_bool),  # / 是否上报了ProtectiveSuit属性;Has the ProtectiveSuit attribute been reported;
        ('bUniform', c_bool),  # / 是否上报了Uniform属性;Has the Uniform attribute been reported;
        ('bBreathingMask', c_bool),  # / 是否上报了BreathingMask属性;Has the BreathingMask attribute been reported;
        ('bSafeBelt', c_bool),  # / 是否上报了SafeBelt属性;Has the SafeBelt attribute been reported;
        ('bVest', c_bool),  # / 是否上报了Vest属性;Has the Vest attribute been reported;
        ('bSafetyShoes', c_bool),  # / 是否上报了SafetyShoes属性;Has the SafetyShoes attribute been reported;
        ('bWristGuard', c_bool),  # / 是否上报了WristGuard属性;Has the WristGuard attribute been reported;
        ('bSafetyRope', c_bool),  # / 是否上报了SafetyRope属性;Has the SafetyRope attribute been reported;
        ('szResvered1', c_char * 3),  # / 字节对齐;Byte alignment;
        ('byReserved', c_char * (304 - sizeof(c_void_p))),  # / 预留字节;Reserved;
    ]

class NET_A_DEV_EVENT_WANDER_INFO(Structure):
    """
    事件类型EVENT_IVS_WANDERDETECTION(徘徊事件)对应的数据块描述信息
    the describe of EVENT_IVS_WANDERDETECTION's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # / 通道号;ChannelId;
        ('szName', c_char * 128),  # / 事件名称;event name;
        ('bReserved1', c_char * 4),  # / 字节对齐;byte alignment;
        ('PTS', c_double),  # / 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # / 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # / 事件ID;event ID;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # / 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # / 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),  # / 保留字节;
        ('byImageIndex', C_BYTE),  # / 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('nObjectNum', c_int),  # / 检测到的物体个数;detected objects number;
        ('stuObjectIDs', NET_A_MSG_OBJECT * 16),  # / 检测到的物体;detected objects;
        ('nTrackNum', c_int),  # / 轨迹数(与检测到的物体个数对应);track number;
        ('stuTrackInfo', SDK_POLY_POINTS * 16),  # / 轨迹信息(与检测到的物体对应);track info;
        ('nDetectRegionNum', c_int),  # / 规则检测区域顶点数;detect region point number;
        ('DetectRegion', NET_POINT * 20),  # / 规则检测区域;detect region;
        ('dwSnapFlagMask', C_DWORD),  # / 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('nSourceIndex', c_int),  # / 事件源设备上的index,-1表示数据无效;the source device's index,-1 means data in invalid;
        ('szSourceDevice', c_char * 260),  # / 事件源设备唯一标识,字段不存在或者为空表示本地设备;the source device's sign(exclusive),field said local device does not exist or is empty;
        ('nOccurrenceCount', C_UINT),  # / 事件触发累计次数;event trigger accumilated times;
        ('stuIntelliCommInfo', NET_A_EVENT_INTELLI_COMM_INFO),  # / 智能事件公共信息;intelli comm info;
        ('nPreserID', c_short),  # / 事件触发的预置点号，从1开始（没有表示未知）;Event triggered preset period, starting from 1 (no unknown);
        ('szPresetName', c_char * 64),  # / 事件触发的预置名称;Preset name for event triggered;
        ('stuExtensionInfo', NET_EXTENSION_INFO),  # / 扩展信息;Extension info;
        ('stuPostion', NET_PRESET_POSITION),  # / 坐标与放大倍数;Coordinates and magnification;
        ('byReserved2', c_char * 4),  # / 字节对齐;byte alignment;
        ('nCurChannelHFOV', C_UINT),  # / 当前报警通道的横向视场角,单位：度，实际角度乘以100;The lateral field of view angle of the current alarm channel, unit: degree, the actual angle is multiplied by 100;
        ('nCurChannelVFOV', C_UINT),  # / 当前报警通道的垂直视场角,单位：度，实际角度乘以100;The vertical field of view angle of the current alarm channel, unit: degree, the actual angle is multiplied by 100;
        ('stuImageInfo', NET_IMAGE_INFO_EX2 * 32),  # / 图片信息数组;Image information array;
        ('nImageInfoNum', c_int),  # / 图片信息个数;Number of picture information;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # / 事件公共扩展字段结构体;Event public extension field structure;
        ('bSceneImage', C_BOOL),  # / pstuSceneImage是否有效;Whether stuSceneImage is valid;
        ('pstuSceneImage', POINTER(SCENE_IMAGE_INFO_EX)),  # / 全景广角图;Global scene iamge;
        ('szReserved', C_BYTE * (398 - sizeof(c_void_p))),  # / 保留字节,留待扩展.;reserved;
    ]

class NET_LINK_INFO(Structure):
    """
    联动信息，保存其他设备传输的信息
    Linkage information, save information transmitted by other devices
    """
    _fields_ = [
        ('nLinkObjectID', C_UINT),  # / 联动物体ID;Linked ObjectID;
        ('nLinkEventID', C_UINT),  # / 联动事件ID;Linked EventID;
        ('nSpeedValue', C_UINT),  # / 联动物体速度，单位米/秒，扩大100倍;Linked object speed, in m/s, expanded by 100 times;
        ('nAlarmType', C_UINT),  # / 报警类型, 第0bit位表示是否超速(1表示超速,0表示未超速), 第1bit位表示是否AIS匹配, 第2bit位表示是否禁行, 第3bit位表示是否逆行;Alarm type, the 0th bit indicates whether it is overspeeding (1 indicates overspeeding, 0 indicates not overspeeding), the 1st bit indicates whether the AIS matches, the 2nd bit indicates whether it is forbidden, and the 3rd bit indicates whether it is reversed;
        ('nLongitude', C_UINT),  # / 联动物体经度，(单位是百万分之度,范围0-360度)如东经120.178274度表示为300178274;The longitude of the linked object, (unit is millionths of degrees, range 0-360 degrees) such as east longitude 120.178274 degrees is expressed as 300178274;
        ('nLatitude', C_UINT),  # / 联动物体纬度，(单位是百万分之度,范围0-180度)如北纬30.183382度表示为120183382/ 经纬度的具体转换方式可以参考结构体 NET_WIFI_GPS_INFO 中的注释;The latitude of the linked object, (units are millionths of degrees, the range is 0-180 degrees), such as 30.183382 degrees north latitude, it is expressed as 120183382For the specific conversion method of latitude and longitude, please refer to the comments in the structure NET_WIFI_GPS_INFO;
        ('nDistance', C_UINT),  # / 联动物体距离，单位米，扩大100倍;Linked object distance, in meters, expanded by 100 times;
        ('szObjectType', c_char * 16),  # / 跟踪物体类型;Track object type;
        ('stuLinkRealUTC', NET_TIME_EX),  # / 外部设备（如雷达）识别到目标上报报警的真实UTC时间;The actual UTC time when an external device, such as radar, recognizes the target and reports the alarm;
        ('szLinkTargetUUID', c_char * 32),  # / 目标点唯一id;Unique ID of the target point;
        ('szResvered', c_char * 144),  # / 保留字节;Reserved bytes;
    ]

class NET_A_DEV_EVENT_STAY_INFO(Structure):
    """
    事件类型EVENT_IVS_STAYDETECTION(停留事件)对应的数据块描述信息
    the describe of EVENT_IVS_STAYDETECTION's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # / 通道号;ChannelId;
        ('szName', c_char * 128),  # / 事件名称;event name;
        ('bReserved1', c_char * 4),  # / 字节对齐;byte alignment;
        ('PTS', c_double),  # / 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # / 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # / 事件ID;event ID;
        ('stuObject', NET_A_MSG_OBJECT),  # / 检测到的物体;have being detected object;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # / 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # / 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('byReserved', C_BYTE * 2),
        ('byImageIndex', C_BYTE),  # / 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('nDetectRegionNum', c_int),  # / 规则检测区域顶点数;detect region point number;
        ('DetectRegion', NET_POINT * 20),  # / 规则检测区域;detect region;
        ('dwSnapFlagMask', C_DWORD),  # / 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('nSourceIndex', c_int),  # / 事件源设备上的index,-1表示数据无效;the source device's index,-1 means data in invalid;
        ('szSourceDevice', c_char * 260),  # / 事件源设备唯一标识,字段不存在或者为空表示本地设备;the source device's sign(exclusive),field said local device does not exist or is empty;
        ('nOccurrenceCount', C_UINT),  # / 事件触发累计次数;event trigger accumilated times;
        ('stuIntelliCommInfo', NET_A_EVENT_INTELLI_COMM_INFO),  # / 智能事件公共信息;intelli comm info;
        ('nObjectNum', c_int),  # / 检测到的物体个数;the count of objects;
        ('stuObjectIDs', NET_A_MSG_OBJECT * 32),  # / 检测到的物体;have being detected objects;
        ('nAreaID', C_UINT),  # / 区域ID(一个预置点可以对应多个区域ID);Area ID(a preset point can correspond to multiple area IDs);
        ('bIsCompliant', C_BOOL),  # / 该场景下是否合规;Is compliant, TRUE:yes, FALSE:no;
        ('stPosition', NET_PRESET_POSITION),  # / 预置点的坐标和放大倍数;Coordinates and magnification of preset points;
        ('nCurChannelHFOV', C_UINT),  # / 当前报警通道的横向视场角,单位：度，实际角度乘以100;The lateral field of view angle of the current alarm channel, unit: degree, the actual angle is multiplied by 100;
        ('nCurChannelVFOV', C_UINT),  # / 当前报警通道的垂直视场角,单位：度，实际角度乘以100;The vertical field of view angle of the current alarm channel, unit: degree, the actual angle is multiplied by 100;
        ('stuSceneImage', SCENE_IMAGE_INFO),  # / 全景广角图;Panoramic wide-angle map;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX2)),  # / 图片信息数组;Image information array;
        ('nImageInfoNum', c_int),  # / 图片信息个数;Number of picture information;
        ('stuLinkInfo', NET_LINK_INFO),  # / 联动信息，保存其他设备传输的信息;Linkage information, save information transmitted by other devices;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # / 事件公共扩展字段结构体;Event public extension field structure;
        ('pstuBoatObject', POINTER(NET_BOAT_OBJECT)),  # / 船只物体信息;boat object;
        ('nBoatObjectNum', c_int),  # / 船只物体信息个数;boat object number;
        ('bReserved', C_BYTE * (620 - sizeof(c_void_p))),  # / 保留字节,留待扩展.;reserved.;
    ]

class NET_A_DEV_EVENT_NUMBERSTAT_INFO(Structure):
    """
    事件类型EVENT_IVS_NUMBERSTAT(数量统计事件)对应的数据块描述信息
    the describe of EVENT_IVS_NUMBERSTAT's data
    """
    _fields_ = [
        ('nChannelID', c_int),  # / 通道号;ChannelId;
        ('szName', c_char * 128),  # / 事件名称;event name;
        ('bReserved2', c_char * 4),  # / 字节对齐;byte alignment;
        ('PTS', c_double),  # / 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # / 事件发生的时间;the event happen time;
        ('nEventID', c_int),  # / 事件ID;event ID;
        ('nNumber', c_int),  # / 区域内物体的个数;the number of object which is in the area;
        ('nUpperLimit', c_int),  # / 设置的上限;upper limit;
        ('stuFileInfo', NET_A_EVENT_FILE_INFO),  # / 事件对应文件信息;event file info;
        ('bEventAction', C_BYTE),  # / 事件动作,0表示脉冲事件,1表示持续性事件开始,2表示持续性事件结束;;Event action,0 means pulse event,1 means continuous event's begin,2means continuous event's end;;
        ('bReserved1', C_BYTE * 2),  # / 字节对齐;
        ('byImageIndex', C_BYTE),  # / 图片的序号, 同一时间内(精确到秒)可能有多张图片, 从0开始;Serial number of the picture, in the same time (accurate to seconds) may have multiple images, starting from 0;
        ('nEnteredNumber', c_int),  # / 表示进入区域或者出入口的内物体的个数;entered object number;
        ('nExitedNumber', c_int),  # / 表示出来区域或者出入口的内物体的个数;exited object number;
        ('dwSnapFlagMask', C_DWORD),  # / 抓图标志(按位),具体见NET_RESERVED_COMMON;flag(by bit),see NET_RESERVED_COMMON;
        ('nOccurrenceCount', C_UINT),  # / 事件触发累计次数;event trigger accumilated times;
        ('stuIntelliCommInfo', NET_A_EVENT_INTELLI_COMM_INFO),  # / 智能事件公共信息;intelli comm info;
        ('nAreaID', C_UINT),  # / 区域ID，一个预置点可以有多个区域ID;Area ID, a preset point can correspond to multiple area IDs;
        ('bIsCompliant', C_BOOL),  # / 该场景下是否合规;Is compliant, TRUE:yes, FALSE:no;
        ('emType', C_ENUM),  # / 表示人数越上限类型 Refer: EM_NUMBER_STAT_TYPE;Indicates that the number of people exceeds the upper limit Refer: EM_NUMBER_STAT_TYPE;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX2)),  # / 图片信息数组;Image information array;
        ('nImageInfoNum', c_int),  # / 图片信息个数;Number of picture information;
        ('nPassedNumber', c_int),  # / 经过区域物体的个数;Number of passed;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # / 事件公共扩展字段结构体;Event public extension field structure;
        ('bReserved', C_BYTE * 800),  # / 保留字节,留待扩展.;Reserved.;
    ]

class NET_A_MAN_NUM_LIST_INFO(Structure):
    """
    立体视觉区域内人数统计事件区域人员列表
    list of petsons within the region(man num)
    """
    _fields_ = [
        ('stuBoudingBox', SDK_RECT),  # / 人员包围盒,8192坐标系;personnel bounding box, 8192 coordinate system;
        ('nStature', c_int),  # / 人员身高，单位cm;persoonel height, unit cm;
        ('szReversed', c_char * 128),  # / 保留字节;reserved;
    ]

class NET_A_DEV_EVENT_MANNUM_DETECTION_INFO(Structure):
    """
    事件类型EVENT_IVS_MAN_NUM_DETECTION(立体视觉区域内人数统计事件)对应数据块描述信息
    IVS event type EVENT_IVS_MAN_NUM_DETECTION(the statistics of people in stereo vision event)data description
    """
    _fields_ = [
        ('nChannelID', c_int),  # / 通道号;channel ID;
        ('szName', c_char * 128),  # / 事件名称;event name;
        ('bReserved1', c_char * 4),  # / 字节对齐, 非保留字节;keep align, not reserved;
        ('PTS', c_double),  # / 时间戳(单位是毫秒);PTS(ms);
        ('UTC', NET_TIME_EX),  # / 事件发生的时间;time of occurrence;
        ('nEventID', c_int),  # / 事件ID;event ID;
        ('nAction', c_int),  # / 0:脉冲 1:开始 2:停止;event action, 0: Pulse, 1: Start, 2: Stop;
        ('nManListCount', c_int),  # / 区域人员列表数量;number of regional personnet list;
        ('stuManList', NET_A_MAN_NUM_LIST_INFO * 64),  # / 区域内人员列表;list of petsons within the region;
        ('stuIntelliCommInfo', NET_A_EVENT_INTELLI_COMM_INFO),  # / 智能事件公共信息;intelli comm info;
        ('nAreaID', C_UINT),  # / 区域ID(一个预置点可以对应多个区域ID);Area ID(a preset point can correspond to multiple area IDs);
        ('nPrevNumber', C_UINT),  # / 变化前人数;previous number of man;
        ('nCurrentNumber', C_UINT),  # / 当前人数;current number of man;
        ('szSourceID', c_char * 32),  # / 事件关联ID。应用场景是同一个物体或者同一张图片做不同分析，产生的多个事件的SourceID相同/ 缺省时为空字符串，表示无此信息/ 格式：类型+时间+序列号，其中类型2位，时间14位，序列号5位;Event source ID. The application scenario is different analysis of the same object or the same picture, resulting in the same sourceid of multiple eventsThe default is an empty string, indicating no such informationFormat: type + time + serial number, in which type 2 digits, time 14 digits and serial number 5 digits;
        ('szRuleName', c_char * 128),  # / 规则名称;rule name;
        ('emDetectType', C_ENUM),  # / 检测模式 Refer: EM_EVENT_DETECT_TYPE;Detection mode Refer: EM_EVENT_DETECT_TYPE;
        ('nAlertNum', C_UINT),  # / 实际触发报警的人数;Alert number;
        ('nAlarmType', c_int),  # / 报警类型. 0:未知, 1:从人数正常到人数异常, 2:从人数异常到人数正常;Alarm type. 0: unknown, 1: from normal to abnormal, 2: from abnormal to normal;
        ('pstuImageInfo', POINTER(NET_IMAGE_INFO_EX2)),  # / 图片信息数组;Image information array;
        ('nImageInfoNum', c_int),  # / 图片信息个数;Number of picture information;
        ('stuEventInfoEx', NET_EVENT_INFO_EXTEND),  # / 事件公共扩展字段结构体;Event public extension field structure;
        ('nDetectRegionNum', c_int),  # / 检测区个数;The number of vertices in the detection area;
        ('stuDetectRegion', NET_POINT * 20),  # / 检测区;Detection area,[0,8191];
        ('szReversed', c_char * 700),  # / 保留字节;reserved;
    ]

class NET_IN_TRAFFICSTARTFINDSTAT(Structure):
    """
    接口(CLIENT_StartFindFluxStat)输入参数
    CLIENT_StartFindFluxStat's input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # / 此结构体大小;structure size;
        ('stStartTime', NET_TIME),  # / 开始时间 暂时精确到小时;start time, temporarily;
        ('stEndTime', NET_TIME),  # / 结束时间 暂时精确到小时;end time, temporarily;
        ('nWaittime', c_int),  # / 等待接收数据的超时时间;the time to wait result;
        ('nChannelCount', c_int),  # / 查询的通道号个数;Query the number of channel numbers;
        ('nChannels', c_int * 256),  # / 查询的通道号;Query channel number;
        ('nLaneCount', c_int),  # / 查询的车道号个数;Query the number of lane numbers;
        ('nLanes', c_int * 16),  # / 查询的车道号;Query lane number;
        ('nClassType', c_int),  # / 数据库表类型 0表示视频结构化,1表示道路监控;Database table type 0 indicates video structure, and 1 indicates road monitoring;
        ('emGranularity', C_ENUM),  # / 查询要求返回的统计信息粒度 默认按小时 Refer: EM_GRANULARITY_STARTFIND_TYPE;Granularity of statistics returned by query request Refer: EM_GRANULARITY_STARTFIND_TYPE;
        ('emDirection', C_ENUM),  # / 统计方向查询条件 Refer: EM_STARTFIND_DIRECTION;Statistics direction query criteria Refer: EM_STARTFIND_DIRECTION;
    ]

class NET_OUT_TRAFFICSTARTFINDSTAT(Structure):
    """
    接口(CLIENT_StartFindFluxStat)输出参数
    CLIENT_StartFindFluxStat's output param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # / 此结构体大小;structure size;
        ('dwTotalCount', C_DWORD),  # / 符合此次查询条件的结果总条数;The total amount that matched current search criteria;
    ]

class NET_IN_TRAFFICDOFINDSTAT(Structure):
    """
    接口(CLIENT_DoFindFluxStat)输入参数
    CLIENT_DoFindFluxStat's input param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # / 此结构体大小;structure size;
        ('nCount', C_UINT),  # / 每次查询的流量统计条数;the number of flow Statistic for query;
        ('nWaittime', c_int),  # / 等待接收数据的超时时间;the time to wait result;
    ]

class NET_A_TRAFFICFLOWSTAT(Structure):
    """
    流量统计记录
    traffic flow state info
    """
    _fields_ = [
        ('szMachineAddress', c_char * 256),  # / 同DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO.MachineGroup;same as DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO.MachineGroup;
        ('szMachineName', c_char * 256),  # / 同DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO.MachineName;same as DEV_EVENT_TRAFFIC_TRAFFICCAR_INFO.MachineName;
        ('szDrivingDirection', c_char * 3 * 32),  # / 行驶方向"Approach"-上行,即车辆离设备部署点越来越近；"Leave"-下行,即车辆离设备部署点越来越远,第二和第三个参数分别代表上行和下行的两个地点,UTF-8编码;DrivingDirection "Approach" means driving direction,where the car is more near;"Leave"-means where if mor far to the car,the scend and third param means the location of the driving direction;
        ('nLane', c_int),  # / 车道号 使用用户配置的车道编号;lane number;
        ('UTC', NET_TIME_EX),  # / 统计时间,转换到UTC;Statistic time;
        ('nPeriod', c_int),  # / 统计周期,单位分钟;Statistic period, m;
        ('nVehicles', c_int),  # / 通过车辆总数;passed vehicle number;
        ('fAverageSpeed', c_float),  # / 平均车速,单位km/h;average speed, km/h;
        ('fAverageLength', c_float),  # / 平均车长,单位米;average length, m;
        ('fTimeOccupyRatio', c_float),  # / 时间占有率,即单位时间内通过断面的车辆所用时间的总和占单位时间的比例;time occupy ratio,;
        ('fSpaceOccupyRatio', c_float),  # / 空间占有率,即按百分率计量的车辆长度总和除以时间间隔内车辆平均行驶距离;space occupy ratio,;
        ('fSpaceHeadway', c_float),  # / 车头间距,相邻车辆之间的距离,单位米/辆;space between two cars,m;
        ('fTimeHeadway', c_float),  # / 车头时距,单位秒/辆;time between two cars, s;
        ('fDensity', c_float),  # / 车辆密度,每公里的车辆数,单位辆/km;car density, every km;
        ('nOverSpeedVehicles', c_int),  # / 超速车辆数;over speed vehicle number;
        ('nUnderSpeedVehicles', c_int),  # / 低速车辆数;under speed vehicle number;
        ('nLargeVehicles', c_int),  # / 大车数量 车辆类型判断标准参见TrafficSnapshot配置表;big car number;
        ('nMediumVehicles', c_int),  # / 中型车数量;mid car number;
        ('nSmallVehicles', c_int),  # / 小车数量;small car number;
        ('nMotoVehicles', c_int),  # / 摩托车数量;moto car number;
        ('nLongVehicles', c_int),  # / 超长车数量;long vehicle number;
        ('szChannel', c_char * 64),  # / 流量数据所属通道号;The channel number to which the traffic data belongs;
        ('szResvered', c_char * 1024),  # / 保留字段;Reserved text;
    ]

class NET_A_TRAFFICFLOWSTAT_OUT(Structure):
    """
    统计信息指针
    the statistic pointer
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # / 此结构体大小;structure size;
        ('nStatInfo', c_int),  # / 统计信息个数;the number of statistic info;
        ('pStatInfo', POINTER(NET_A_TRAFFICFLOWSTAT)),  # / 统计信息指针,由用户申请内存，大小为sizeof(TRAFFICFLOWSTAT)*nStatInfo;the statistic pointer, the space application by the user, length is sizeof(TRAFFICFLOWSTAT)*nStatInfo;
    ]

class NET_OUT_TRAFFICDOFINDSTAT(Structure):
    """
    接口(CLIENT_DoFindFluxStat)输出参数
    CLIENT_DoFindFluxStat's out param
    """
    _fields_ = [
        ('dwSize', C_DWORD),  # / 此结构体大小;structure size;
        ('stStatInfo', NET_A_TRAFFICFLOWSTAT_OUT),  # / 统计信息指针;the statistic pointer;
    ]
