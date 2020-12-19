# WindowsFocusWallpaperGetter
WallpaperGetter的面向对象和GUI版，python大作业的延续

## 所有的仓库地址

1. `Github`：[点此前往](https://github.com/DongCX-LDHSP/WindowsFocusWallpaperGetter)，可在该仓库获取`Release`版本
2. `Gitee`：[点此前往](https://gitee.com/rikdon/WindowsFocusWallpaperGetter)
3. `Gitlab`：[点此前往](https://gitlab.com/Rik-Don/windowsfocuswallpapergetter)

## 问题总结

1. 包内模块引入时，就拿FilenameManager包来说，在TextFile内引入RecordLine可选的方式有两种：第一种引入方式适合引入模块（文件）内所有对象，第二种引入方式则适合模块内只有一个单独的类：
    1. `from FilenameManager import RecordLine` # 该方式未直接将RecordLine类引入，而是引入了RecordLine文件模块，具体使用时，需要RecordLine.RecordLine
    2. `from FilenameManager.RecordLine import RecordLine` # 该方法直接将RecordLine类引入，构造时可以直接使用RecordLine()
    3. `from FilenameManager.RecordLine import *` # 该方法可以将模块内文件全部以独立的形式引入，可以直接使用而不必加模块名
    
2. 连接数据库时，如果失败，注意检查各项参数是不是传成了别的参数，比如：`username`错传成`database_name`

3. 嵌入式SQL语句中如果有字符串必须用 `""` 括起来，不然会报语法错误

4. 在`pipenv`虚拟环境下，使用`pyqt5`运行会出现提示: `This application failed to start because no QT platform plugin could be initialized. Reinstalling the application may fix this problem.`，可能的解决方案
    1. 最直接的解决办法是使用系统环境，只要正确安装应该都不会有问题（本人测试可行）
    2. 网上很多都说要复制`plugins`或`platform`文件夹中的内容拷贝到另外一个地方（本人测试无效）
    3. 再安装 `pyqt5-tools` ，这个应该是针对那些没有安装全套QT的人（但是本人测试仍然不行）
    4. 再安装 `pyqt5-stubs` ，这个咱也不知道是干嘛的，然后添加环境变量（本人测试不可行）
    
5. `python`超类不能导入子类模块，子类模块也不能互相导入，测试情况均是**一个模块占用一个文件的情况**，其他情况有待测试

6. 在 `settings.json` 增加了文件中增加了 `UnusedIdentityAndNumber` 成员后总是无法正常写入设置

    表现为：
    
    1. 第一次写入设置正常
    2. 第二次写入设置正常，但会在设置末尾多出一个 `}` 或 `]\n    }`
    3. 之后再进行设置就会异常退出
  
    原因：
    
    文件写入打开方式设置为了 `r+`，该模式下如果**部分更新设置**会出现问题
    
7. 在单元格中放入了控件，如何使控件居中
    1. 新建一个控件
    2. 新建一个布局
    3. 将欲居中的单元格控件加入布局中
    4. 设置 `1.` 中的控件的布局为 `2.` 中的布局
    5. 将 `1.` 中控件压入单元格即可

    代码如下
    ```python
    def __set_widget_style(self, widget):
        temp = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(widget)
        temp.setLayout(layout)
        temp.setFont(self.__tableOperationFont)
        return temp
    ```
    
8. 从当前遍历的列表中删除元素时，注意使用倒序遍历方式删除

9. 善用信号与槽

10. 刷新表格时，注意考虑现有表格的行数和刷新后表格的行数，否则可能会看不到刷新的效果

11. 新发现的 `python` 的特性，在类内部使用get方法，如果数据不经处理直接返回，效果类似于返回该属性的**地址**，相当于**直接暴露**了类的参数（**即使该参数是私有的**）。由于这个特性，再次被占用的未使用到的 `id` 和 `num` ，因为在 `ImageCopier` 中使用了 `pop` 方法获取元素，所以间接解决了这个更新问题。

12. 在完善了 `num` 的更新问题之后， `unused_id_num` 的更新出现了问题，这是因为如果获取图片过程中仅使用了 `unused_id_num` ，那么 `numCounter` 的值就为 `[0, 0]`，在更新 `num` 时，不会进入 `SettingsAnalyser.refresh_number` 第一个条件语句内部，没有刷新文件，所以没能正常更新 `unused_id_num`。

13. 修复了一个小 `Bug` ，是由 `Python` 的特性引发的：`Python` 函数的默认参数的值在运行时不会随着时间而改变，除非再次运行，这便是获取日期不准确的原因

14. 在实现查看全部数据倒序显示时，注意到预览壁纸的逻辑使用了被单击的单元格而不是`MyQLabel`的`row`属性，已使用`mouseReleaseEvent`重载结合自定义信号解决了该问题

15. 在数据量逐渐大了起来之后发现文件的**原始名称并不能唯一区分一张壁纸**，故可以考虑采用文件的`hash`值来区分不同的文件

## 待实现的设想特性

可以参考提交的总的文档中的两个测试类

1. 常驻后台
2. 常驻后台获取壁纸后发出通知
3. 后台模式获取通知的频率可以设置，表现为获取壁纸的数量
4. watchdog监控文件夹内容变化
5. 后台模式和前台模式表现的区别，表现为是否有主程序
6. settings.json设置项更新
7. Controller似乎不必全是静态方法，加以优化尝试
8. 尝试添加一个近期获取的壁纸旧名称，提升查询效率
9. 在长期不能获取图片时，提醒用户Windows聚焦可能出现了问题
10. 尝试记录用户不喜欢的图片，防止以后再次获取
11. 尝试通过统计新增图片的壁纸更新日期来动态更新自动获取壁纸的时间
12. 倒序显示查看记录结果
13. 尝试使用图片的hash值区分图片，需要对数据库设计进行变更
    1. 增添一个hash值的列
    2. 当检查到相同hash值的文件时，提示用户本次旧文件名称和库中已存储的旧文件名称
14. 在使用**查看记录**的功能时，使用**多线程**或者**分页加载**来提升程序的加载速度
