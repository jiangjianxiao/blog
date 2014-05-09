jvm 互操作笔记
-----------------------------------------

:date: 2014-05-9 09:25
:slug: jvm-interactive-note
:status: draft 

当前, 使用java很多时候不可避免, 比方说以下场景

1. excel 导出需要更多的控制 ,xlwt/xlrd 无法实现类似data validation using dropdown list之类的特性, 有个包支持但格式限制在2007
2. taobao 消息通知, 目前只提供java/c# sdk
3. 大数据 

交互的手段很多 

1. 在python内部使用jpype/pyjnius 这样 的桥接工具调用 
2. 通过 jython, 然后在用消息队列或是pyro这样的支持jython/ironpython/python这样的包交互或者进程交互
3. 直接java/groovy写, 然后通过消息队列或者进程交互

目前, 尝试的工具有

* pyjnius 调用 poi
* jython + jzmq
* java + jzmq

都是可以运作的, 不过前两个选项都存在一些缺点

pyjnius 问题

1. 由于python是多进程部署, 由于java的内存占用, 这不是一个好主意, 会导致内存浪费的比较严重!　
2. 包本身问题,  比方说pyjnus 将字符串转换成byte array有问题, 不能转换大于127的字符, jython 没有问题, 参考  https://github.com/kivy/pyjnius/issues/93

jython 主要问题是性能和发展不力. 当然, 如果在这个场景, 主要用jzmq转发请求, 性能不是主要问题.  当然,  最理想的方式就是3.

下面是用jython转发taobao消息服务例子, 很简单是吗

.. code-block:: python

    from  com.taobao.api.internal.tmc import TmcClient, Message, MessageHandler, MessageStatus
    from org.zeromq import ZMQ
    import sys
    def main():
        client = TmcClient(app_key, app_secret,"default")
        context = ZMQ.context(2)
        socket = context.socket(ZMQ.PUSH)
        socket.bind("tcp://*:5555")
        class MessageHandlerImpl(MessageHandler):
            def __init__(self):
                pass
            def onMessage(self, message, status):
                try:
                    socket.send("{\"topic\": \"%s\", \"content\":%s}" % ( message.getTopic(), message.getContent()))

                except:
                    status.fail()
        client.setMessageHandler(MessageHandlerImpl())

        client.connect(uri)
        sys.stdin.readline()

    if __name__ == '__main__':
        main()    


由于定位在交互, 所以在jvm, 不会写大规模,系统的代码(同时也要避免这种情况), 同时为避免动态/静态语言转变的思维压力,降低学习成本. 使用groovy, 退化一些性能换取效率会更好. groovy的gdk能省下使用第叁方包的很多时间




pyjnius 
========================

github: https://github.com/kivy/pyjnius

windows 下编译

1. windows 下目前版本用vc编译有问题, 使用mingw编译 setup.py install --compiler=mingw32
2. 事先需要设置JAVA_HOME
3. 需要将 %JAVA_HOME%\jre\bin\client 加入到路径变量, 用server会有问题

poi

jnius.ByteArray.tostring 没有问题, 是poi workbook.getBytes()有问题, 无法获得全部数据

.. code-block:: java

    ms = ByteArrayOutputStream()
    wb.write(ms)
    ms.toByteArray() # 正确



jzmq
==========================

提示: java.lang.UnsatisfiedLinkError: java.lang.UnsatisfiedLinkError: no jzmq in java.library.path


这种方法没有用

.. code-block:: python

    from java.lang import System
    System.setProperty("java.library.path", "/usr/local/lib")
    print System.getProperty("java.library.path")

 或 -Djava.library.path="/usr/loca/lib" 
 
 或 export LD_LIBRARY_PATH=/usr/local/lib

 libjzqm.so  在/usr/local/lib,  zmq.jar 在/usr/local/share/java

