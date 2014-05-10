jython27 beta 3
===========================

:date: 2014-05-9 17:28
:slug: jython-27-beta3

最近 jython 发布了 2.7 beta2 ,  这里想说的是即将到来的beta3.

Jim Baker  在jython-dev上的邮件说明 beta3 主要是合并socket-reboot分支的, 这个 分支主要 是Design of a reworked implementation of socket, ssl, and select modules for Jython, using Netty 4.

并且这个版本 easy_install/pip将能重新工作在jython 2.7中

但我的尝试是运行ez_setup.py时的这个 错误 

.. code-block:: python

    open(os.devnull, 'wb')

引发 IOError, google以下, 好象有人报告这个错误, 不过同我这里还不一样  http://bugs.jython.org/issue1944, 即 LC_ALL="en_US.UTF-8" ./jython -c 'open("/dev/null", "w")'  同样还是报错, 测试了jython 2.5也是如此 

在sqlalchemy 0.86的代码 中, 包含了另外一个版本 的ez_setup 可以完成 setuptools的安装 

pip 需要使用 https://github.com/jimbaker/pip)


性能, 还是很慢, 无法忍受

看到日志提示: You don't have Javassist in your class path or you don't have enough permission to load dynamically generated classes.  Please check the configuration for better performance.

放了 Javassist.jar 在classpath ,不过这个应该对下面的db访问没有多大关系


.. code-block:: python

    #encoding=utf-8
    import sys
    import time
    if  '__pypy__' in sys.builtin_module_names:
        from psycopg2cffi import compat
        compat.register()
    from sqlalchemy.ext.declarative import declarative_base
    Base = declarative_base()


    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker, scoped_session

    if sys.platform.startswith('java'):
        db = create_engine('postgresql+zxjdbc://postgres:123456@localhost/c9')
    else:
        db = create_engine('postgresql://postgres:123456@localhost/c9')
    Session = scoped_session(sessionmaker(bind=db))
    def test():
        session = Session()
        session.execute('select * from users;').fetchall()
        session.close()

    _start = time.time()
    _count = 1000
    for i in range(_count):
        test()
    print 'timing', time.time() - _start


这段代码测试 jython/pypy/python的表现

pypy  timing 2.4122531414
python timing 1.4104578495
jython timing 14.6050000191 且不说启动脚本 用了10多秒


用类似的操作单独测试 zxjdbc, 表现也好不了多少 

timing 10.6180000305

类似的查询用groovy 跑, 2.108, 比cpython差, 说明对于依赖c 扩展(比方这里主要就是psycopg2 + libpq)的一些 操作, python的性能问题对实际表现影响不大

至于pypy只要不断的提高 查询次数 , 性能就会逐渐拉平cpython并且最终超越. 对于 对c 扩展支持不佳的pypy来说,算是不错的了

而jython 则是无法忍受, 所以不能在实际项目中写大量的jython代码, 起码同groovy持平或差一点才能考虑

