# todo 枚举变量抽离
from ImageAnalyser import ImageLayout
from datetime import datetime


class RecordLine:
    """
    RecordLine:记录行
    用于存储获取的壁纸的详细信息
    """
    def __init__(self, identity: int, num: int, old_name: str, new_name: str,
                 layout: ImageLayout, date: datetime):
        self.__id = identity
        self.__num = num
        self.__oldName = old_name
        self.__newName = new_name
        self.__layout = layout
        self.__date = date
        self.__dateStringFormat = "%Y-%m-%d %H:%M:%S"

    def return_storage_tuple(self):
        return self.__id, \
               self.__num, \
               self.__oldName, \
               self.__newName, \
               self.__layout.value, \
               self.__date.strftime(self.__dateStringFormat)

    def get_gui_string_tuple(self):
        return str(self.__id), \
               str(self.__num), \
               "横版" if self.__layout is ImageLayout.horizontal else "竖版", \
               self.__date.strftime(self.__dateStringFormat), \
               self.__oldName

    @staticmethod
    def get_from_storage(message: list):
        """
        从存储中还原对象
        1. ImageLayout需要强转
        2. 日期需要按照预定格式还原
        :param message: 预处理过的列表形式的信息
        :return: RecordLine
        """
        return RecordLine(message[0], message[1], message[2], message[3],
                          ImageLayout(message[4]),
                          datetime.strptime(message[5], "%Y-%m-%d %H:%M:%S"))

    def get_id(self):
        return self.__id

    def get_num(self):
        return self.__num

    def get_old_name(self):
        return self.__oldName

    def get_new_name(self):
        return self.__newName

    def get_layout(self):
        return self.__layout

    def get_date(self):
        return self.__date
