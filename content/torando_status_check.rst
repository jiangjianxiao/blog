tornado 服务监测
------------------------------

:date: 2013-06-14 10:16
:slug: tornado-status-check

真正的原因
======================

下面的都不用看了， 真正的原因应该就是， 我在tornado处理DELETE请求时鬼马的有一行ctx.term(), 结果在并发时(同时多个DELETE请求, 如果这个前提没有，就不会有问题)， 通过该ctx的socket都接收不到异步返回，直接导致zmq违例。而tornado+pyzmq时tornado的eventloop由 pyzmq代理的。结果就是tornado后端直接无法访问。

同tornado windows下的表现应该无关，等待这几天验证

下面的就不删除了，就当作思考的过程！


概述
==================


ok , 我有在windows 下部署c9. 当前其架构大体是 nginx -> tornado(多个进程) -> proxy - application server(多个进程).  tornado部分是一个简单的restful framework, 主要就是将nginx请求转发给proxy,然后将proxy返回的结果显示给用户. tornado部分不包括任何业务逻辑. application server 是真正的业务逻辑点. proxy则是tornado和application server 之间的桥梁, 也不包括任何业务逻辑. zmq(pyzmq)是应用间通讯的主要方式.

c9第一个版本则使用是 nginx -> tornado -application server(成对出现，4个对) 结构, 并使用py2exe打包为windows service.

第一个版本在windows 下运行很平稳， 但以virtualenv/supervisor方式部署到ubuntu server上时，当天在上午高峰和下午高峰(日志删了，大概是上午11点多和下午3点多)， nginx 分别对tornado的一个进程报告upstream timeout.

为什么一个后端upstream timeout就会导致基本访问不能, 这是因为nginx 不会自动剔除有问题的后端, 而浏览器中的一个操作,比方说打开一个表单, 可能会有3-4个请求(如销售单通常会有请求销售单,明细, 活动,审核,工作流等5到6个请求)会发给nginx再转发给后端(这里不包括静态文件,因为静态文件直接由nginx代理)

nginx对出错后端的处理是在一个设定的时间内如果出错达到设定的次数,则在这个设定的时间内不访问该后端, 但过了这个设定的时间,则继续访问,然后就是循环, 而在c9的架构中,如果真的是zmq通讯出了问题, 其表现就是永远阻塞,最好就是直接断开此后端(当前对nginx的理解,感觉做不到这点).

nginx把这些请求均匀的分配给tornado后端(当前,部署了4个进程), 其中一个后端出问题了,在前台就是各种表现(比方说明细数据加载不上,或是活动数据加载不上,或是表单头部数据加载不上,或是工作流加载不上或是审核帮助加载不上), 结果就是无法操作.

当前新的架构部分, application server可以自动伸缩了, tornado部分理论上也可以自动伸缩,但是受限于nginx (在nginx.conf中,后端都是配置好的+不能自动剔除后端). 所以,tornado 端的upstream timeout问题一旦发生,就变成一个严重的问题. 即: 有业务逻辑的application server可以down, 但无业务逻辑的tornado后端却不能down.

当前,在windows 上尝试使用virtualenv的部署形式, 一个进程就是python app_gevent.pyc ../conf/app_gevent.json的形式, 并使用srvany做成服务.

上线当天,没有问题, 昨天, 在下午2点多, 一个tornado后端 upstream timeout, 当时没有发现此问题, 在一段时间后,重启全部tornado和application server后, 在4点多, 有一个tornado 后端upstream timeout.

**这才发现,查看nginx 的error.log(c92/nginx-1.4.1/logs/error.log)是最直接的方式, 如果有一个后端upstream timeout, 就重启该后端.**

为什么tornado后端会upstream timeout
========================================

鉴于无法直接从代码上发现此问题,所以判断为什么会upstream timeout成了一个难题

nginx windows上只有一个进程, 也有1024的限制,但目前,虽然对它有怀疑,但没有充分根据.

可能的问题

1. 分发问题? 打包分发不会导致此问题? **排除**
2. pyzmq版本问题? 当前tornado/pyzmq 均使用最新的版本, 在开发时曾多次发现py文件改变,tornado autoload导致pyzmq的io loop终止 (此时理论上tornado后端就完全不能访问)
3. zmq 的req/rep违例了, 即必须请求-接收,不能请求-请求, 用户代码其实没有办法做到这点. **本次已排除这点**
4. application server处理能力不足了? 扩展后能避免此问题? **无法完全避免**
5. pyzmq达到1024个限制? 理论上这样会报错, 浏览端会收到此信息. 可以直接访问一个打印页面测试. **本次排除这点**
6. proxy 没有接收到此消息, 或是没有回复此消息导致阻塞(可能性不大, 但也并非没有可能, 如果出现此问题,则重启tornado后端是最佳选择). **本次可以排除这点**

所以

.. rubric:: 2013/6/14 测试

首先,再次测试打包分发(当前使用cx_freeze打包为windows service), 并将application server进程启动为10个(最后调整到13个), 确认问题是否重现

在5点左右还是出现一个tornado进程upstream timeout, 修改nginx配置,排除该后端, 重启nginx, 在不影响访问的前提下分析这个 localhost:8000

1. 当tornado 后端timeout时, telnet localhost 后端端口, 可以telnet连接
2. 当tornado 后端timeout时 , 一些不依赖zmq的请求工作正常吗? 在服务器上输入 http://localhost:后端端口/application.manifest, 无法连接, 说明是web本身down!
3. 当tornado 后端timeout时, 确认是否是向proxy通讯时发生问题. 向application server(其实是通过代理)发出一个请求 localhost:后端端口/api/heart (新增加), 看看是否ok. 在这个例子中,由于web功能本身down!, 这个验证无需进行.

结论是端口还在监听, 但web功能丧失, proxy和application server是正常的. 同zmq也无关. 就是tornado无法正常响应请求了(当然,这对以性能著称的tornado是无法想像的).

通过分析日志，发现下午3-5点占据了50%的请求， 而4整点的请求接近10000， 超出平时高峰值1/3. 平时的高峰在6`7000之内.

.. rubric:: 结论

所以结论很明显，没有出现我担心的由于zmq req/rep出现违例而引起的阻塞(这问题如果发生了,更是头疼). 通过扩展application server进程数量, 应用服务其实是应付了这次高峰访问，由于tornado本身的品质,我倾向于windows上不支持iocp及其他支持不佳原因导致.

ps: application server的扩容,其实是增加了响应能力, 结果的可能就是导致更多的访问. 同样,如果到linux下,由于nginx等响应能力的改进,也需要提升应用服务的响应能力,否则还是会出现不匹配.


所以, 如果继续在windows 下部署

1. 通过多开两个进程分担tornado的压力, 以以往6~7000能平稳度过经验,多开两个进程就能分担多出的请求.
2. 修改nginx.conf, 通过查看tornado日志,我发现 tornado可能分担了对图标,robots文件不必要的访问
3. 迁移到linux


当然,如果tornado down了, 最好的解决方法就是快速重启该后端. 所以,tornado状态检测的程序还是有必要.


监测程序
=============================

原理能简单,就是定时访问后端,查看是否超时或正常返回, 如果超时,就尝试重启服务

为了达到这个目的,特地增加了一个/api/heart , 请求该url , tornado -> proxy -> application server -> proxy -> tornado, 返回一个ok. 超时比方说30秒,就是阻塞了. 当然,如果tornado后端本身down,也会超时.

windows 版本已经完成，参考 https://github.com/jiangjianxiao/servicemonitor

linux 兼容todo




其他: zmq rep/req的 超时控制
=============================

当前,application server借助gevent, 实现在rep端的超时控制,当前限定业务逻辑不能大于8秒,否则返回一个timeout异常,但 req端的,却没有解决方法

参考 https://github.com/zeromq/pyzmq/issues/132

但当和tornado结合时,没有办法用这个方法

继续探索....

其他: nginx 本身的设定
============================

虽然目前不可能,原因在于它只有一个fail_timeout配置, 但还是继续探索有无其他途径,比方说修改源代码, 当fail_timeout内达到max_fails时直接就是一天不能访问,相当于自动剔除这个后端, 因为少一个后端暂时不会对访问有大的影响, 而阻塞就影响访问.

