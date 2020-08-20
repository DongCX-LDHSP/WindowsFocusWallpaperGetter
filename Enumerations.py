from enum import Enum


# SettingsAnalyser
class ResetMessage(Enum):
    """
    ResetMessage:设置更新结果枚举类
    """
    success = 0             # 重置成功
    locationNotExist = 1    # 路径不存在
    fileNotFound = 2        # settings文件找不到


class StorageMethod(Enum):
    """
    StorageMethod:存储方式枚举类
    """
    textFile = 0
    database = 1
    unknown = 2


# ImageAnalyser
class ImageLayout(Enum):
    """
    ImageLayout:图片版式枚举类
    """
    horizontal = 0      # 横版图片
    vertical = 1        # 竖版图片
    unknown = 2         # 未知版式
    invalidFile = 3     # 非图片文件


class ImageFormat(Enum):
    """
    ImageFormat:图片格式枚举类
    """
    jpg = 0     # jpg/jpeg格式
    png = 1
    gif = 2
    bmp = 3
    other = 4


# Controller
class ExecuteMessage(Enum):
    success = "执行成功"
    failure = "执行失败"


class SearchMode(Enum):
    idAndNum = 0
    oldFilename = 1
