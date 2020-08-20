from FilenameManager.FilenameManager import FilenameManager
from FilenameManager.RecordLine import RecordLine

# todo 枚举变量抽离
from ImageAnalyser import ImageLayout
import pymysql


class Database(FilenameManager):
    """
    Database:继承自FilenameManager
    以数据库的方式存储文件名
    """
    def __init__(self):
        self.__host = "localhost"

        # todo 动态设置数据库用户名和密码
        self.__username = ""
        self.__password = ""

        self.__databaseName = "FilenameStorage"
        self.__tableName = "filename"
        self.__useDatabaseSql = "Use {}".format(self.__databaseName)
        self.__createDatabaseSql = "Create Database If Not Exists {}".format(self.__databaseName)
        self.__dropDatabaseSql = """Drop Database {}""".format(self.__databaseName)
        self.__createTableSql = """Create Table If Not Exists `{}` (
                                     `id` int Not Null,
                                     `num` int Not Null,
                                     `old_name` nchar(64) Not Null,
                                     `new_name` varchar(29) Not Null,
                                     `layout` int Not Null,
                                     `date` nchar(19) Not Null,
                                     Primary Key (`id`) 
                                     )
                                  """.format(self.__tableName)
        self.__searchOldFilenameSql = """Select id, num, old_name, new_name, layout, date
                                            From {} Where old_name Like "%{}%" """
        self.__searchIdNumSql = """Select id, num, old_name, new_name, layout, date 
                                      From {} Where id = {} Or num = {}"""
        # 用于在删除前获取unused_id_num
        self.__searchIdDeleteSql = """Select id, num, layout From {} Where id = {}"""
        self.__insertFilenameSql = """Insert Into {0} (id, num, old_name, new_name, layout, date) 
                                        Values ({1}, {2}, "{3}", "{4}", {5}, "{6}")
                                     """
        self.__deleteFilenameSql = """Delete From {} Where id = {}"""
        self.__selectAllSql = """Select id, num, old_name, new_name, layout, date From {}"""
        self.__connect_to_database()

    def __connect_to_database(self):
        """
        连接数据库
        1. 连接数据库
        2. 若成功则创建游标，否则跳转到3
        3. 数据库不存在，执行生成数据库及建表的方法
        :return: 暂无
        """
        try:
            self.__database = pymysql.connect(self.__host,
                                              self.__username,
                                              self.__password,
                                              self.__databaseName)
            self.__cursor = self.__database.cursor()
        except pymysql.err.InternalError:
            self.__generate_record_file()

    def __generate_record_file(self):
        self.__create_database()
        self.__create_table()

    def __create_database(self):
        """
        创建数据库
        1. 连接数据库服务器
        2. 生成游标
        3. 执行数据库创建SQL语句
        4. 执行使用该数据库的SQL语句
        :return: 暂无
        """
        self.__database = pymysql.connect(self.__host,
                                          self.__username,
                                          self.__password,
                                          charset='utf8mb4')
        self.__cursor = self.__database.cursor()
        self.__cursor.execute(self.__createDatabaseSql)
        self.__cursor.execute(self.__useDatabaseSql)

    def __create_table(self):
        """
        建数据库表
        :return: 暂无
        """
        self.__cursor.execute(self.__createTableSql)

    def is_in_old_filenames(self, filename: str):
        """
        查询数据库中是否已存在filename
        1. 执行search_by_old_name(filename)
        2. 若返回值是None则返回False，否则返回True
        :param filename: 待查询的文件名称
        :return: bool，是否已存在该文件
        """
        name = self.search_by_old_name(filename)
        if len(name) == 0:
            return False
        else:
            return True

    def search_by_id_num(self, keyword: int):
        """
        基于id和num查找记录
        :param keyword: 查找关键字
        :return: list<RecordLine>
        """
        tempRecordLines = list()
        sql = self.__searchIdNumSql.format(self.__tableName, keyword, keyword)
        self.__cursor.execute(sql)
        results = self.__cursor.fetchall()
        for result in results:
            tempRecordLines.append(RecordLine.get_from_storage(result))
        return tempRecordLines

    def search_by_old_name(self, filename: str):
        """
        查询数据库中旧文件名称是filename的项
        1. 执行Select SQL语句
        2. 获取一条记录
        3. 判断name是不是None
        4. 若是则返回None，否则返回RecordLine对象
        :param filename: 待查询的文件名称
        :return: 查询结果
        """
        tempRecordLines = list()
        sql = self.__searchOldFilenameSql.format(self.__tableName, filename)
        self.__cursor.execute(sql)
        recordLines = self.__cursor.fetchall()
        if recordLines is not ():
            for recordLine in recordLines:
                tempRecordLines.append(RecordLine.get_from_storage(recordLine))
        return tempRecordLines

    def get_all_record_lines(self):
        """
        获取RecordLine形式的列表，用于存储方式转换
        1. 执行Select SQL语句，获取所有存储内容
        2. 逐个还原成RecordLine对象并添加到临时列表中
        3. 返回临时列表
        :return: list<RecordLine>
        """
        tempRecordLine = list()
        self.__cursor.execute(self.__selectAllSql.format(self.__tableName))
        recordLines = self.__cursor.fetchall()
        for recordLine in recordLines:
            line = RecordLine.get_from_storage(recordLine)
            tempRecordLine.append(line)
        return tempRecordLine

    def append_filenames(self, record_lines: list):
        """
        向数据库中写入新增数据
        1. 逐个获取适合存储的元组
        2. 生成具体的SQL语句
        3. 执行Insert SQL语句
        4. 若成功则提交到数据库，否则跳转到5
        5. 回滚数据库
        :param record_lines: 新获取的RecordLine对象列表
        :return: 暂无
        """
        for line in record_lines:
            message_tuple = line.return_storage_tuple()
            insert_sql = self.__insertFilenameSql.format(self.__tableName,
                                                         message_tuple[0],
                                                         message_tuple[1],
                                                         message_tuple[2],
                                                         message_tuple[3],
                                                         message_tuple[4],
                                                         message_tuple[5])
            try:
                self.__cursor.execute(insert_sql)
                self.__database.commit()
            except pymysql.err.MySQLError:
                self.__database.rollback()

    def delete_filenames(self, identities: list):
        # 记录删除的数据
        unusedIdentityAndNumber = self.__generate_unused_id_num(identities)

        # 移除待删除数据
        for identity in identities:
            sql = self.__deleteFilenameSql.format(self.__tableName, identity)
            try:
                self.__cursor.execute(sql)
                self.__database.commit()
            except pymysql.err.MySQLError:
                self.__database.rollback()

        # 返回统计到的已删除的identity和number，用于后续使用
        return unusedIdentityAndNumber

    def __generate_unused_id_num(self, identities: list):
        unusedIdentityAndNumber = [[], [], []]

        # 抓取id, num, layout
        tempMessage = []
        for identity in identities:
            sql = self.__searchIdDeleteSql.format(self.__tableName, identity)
            try:
                self.__cursor.execute(sql)
                tempMessage.append(self.__cursor.fetchone())
            except pymysql.err.MySQLError:
                pass

        # 处理成unused列表
        for message in tempMessage:
            unusedIdentityAndNumber[0].append(message[0])
            if ImageLayout(message[2]) is ImageLayout.horizontal:
                unusedIdentityAndNumber[1].append(message[1])
            elif ImageLayout(message[2]) is ImageLayout.vertical:
                unusedIdentityAndNumber[2].append(message[1])
        return unusedIdentityAndNumber

    def delete_storage_file(self):
        try:
            self.__cursor.execute(self.__dropDatabaseSql)
            self.__database.commit()
        except pymysql.err.MySQLError:
            self.__database.rollback()

    def __del__(self):
        try:
            self.__database.close()
        except AttributeError:
            pass
