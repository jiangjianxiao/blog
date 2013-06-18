C9 开放源代码计划
-----------------------------------------

:date: 2013-05-31 14:11
:slug: c9-open-source-plan
:category: c9


C9 是一个进销存系统, 当前，它主要应用在计算机批发行业. 它的前身是C3和C8. 点这个 `链接 <http://www.yuyaoe.com/static/html/intro.html>` ,可以参考更多信息

C9 计划逐步开放源代码, 当然, 开放源代码不是目的, 主要的是为了C9的体系更加结构化,更加易于扩展, 同时,通过开放源代码这种外部作用力, 使代码更规范,更安全

C9 的0.3 版本将是一个第三方扩展完备的版本, `参考版本规划 <http://www.yuyaoe.com/static/html/develop/version.html>`, 我们计划通过一个开源
的 `返修模块 <http://www.yuyaoe.com/static/html/repair/index.html>` 来验证这一点

当前
====================

* C9 的文档, 开源, `参考 <https://github.com/jiangjianxiao/c9>`_  `build <http://www.yuyaoe.com/static/html/index.html>`
* C9 返修模块, 开源,正在开发中 `参考 <https://github.com/jiangjianxiao/c9_repair>`
* C9 c proxy模块, 开源 `链接 <https://github.com/jiangjianxiao/wuproxy>`
* c9 tornado服务监控程序 `链接 <https://github.com/jiangjianxiao/servicemonitor>`

未来, 我们将逐步打碎C9, 逐步开放其销售,采购,库存,财务等模块, 最终到达全部开源的目的

从现在开始,凡是新开发的模块, 如商城接口,taobao 接口, 移动界面等,一开始就走开源的途径


C9技术堆栈
=============================

* python/pypy(在0.2版本中已支持)
* tornado/twisted/gevent 对于Web server 我们准备了三套方案,对于应用服务,我们准备了基于twisted和gevent的方案
* zeromq/pyzmq
* postgresql/psycopg2
* sqlalchemy
* memchached
* reportlab/xlwt/xhtml2pdf/xldt/python-ldap等
* socketio/socketjs 支持
* 打包方案cx_freeze
* c/cython 部分使用