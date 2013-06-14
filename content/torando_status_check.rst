tornado 服务监测
------------------------------

:date: 2013-06-14 10:16
:slug: tornado-status-check


概述
==================


ok , 我有在windows 下部署c9. 当前其架构大体是 nginx -> tornado(多个进程) -> proxy - application server(多个进程). 

但c9第一个版本使用的 nginx -> tornado -application server(成对出现，4个对), 使用py2exe打包

第一个版本在windows 下运行很平稳， 但以virtualenv/supervisor方式部署到ubuntu server上时，当天在上午高峰和下午高峰(日志删了，大概是上午11点多和下午3点多)， nginx 分别对tornado的一个进程报告upstream timeout.

为什么一个后端upstream timeout就会导致基本访问不能, 这是因为nginx 不会自动剔除有问题的后端, 而浏览器中的一个操作,比方说打开一个表单, 可能会有3-4个请求(如销售单通常会有请求销售单,明细, 活动,审核,工作流等5到6个请求)会发给nginx再转发给后端(这里不包括静态文件,因为静态文件直接由nginx代理)

nginx对出错后端的处理是在一个设定的时间内如果出错达到设定的次数,则在这个设定的时间内不访问该后端, 但过了这个设定的时间,则继续访问,然后就是循环, 而在c9的架构中,如果真的是zmq通讯出了问题, 其表现就是永远阻塞,最好就是直接断开此后端(当前对nginx的理解,感觉做不到这点).

nginx把这些均匀的分配给tornado后端(当前,部署了4个进程), 其中一个后端出问题了,在前台就是各种表现(比方说明细数据加载不上,或是活动数据加载不上,或是表单头部数据加载不上,或是工作流加载不上或是审核帮助加载不上), 结果就是无法操作.

当前新的架构部分, application server可以自动伸缩了, tornado部分理论上也可以自动伸缩,但是受限于nginx (在nginx.conf中,后端都是配置好的+不能自动剔除后端). 所有,tornado 端的upstream timeout问题一旦发生,就变成一个严重的问题.

当前,在windows 上尝试使用virtualenv的部署形式, 一个进程就是python app_gevent.pyc ../conf/app_gevent.json的形式, 并使用srvany做成服务.

上线当天,没有问题, 昨天, 在下午2点多, 一个tornado后端 upstream timeout, 当时没有发现此问题, 在一段时间后,重启全部tornado和application server后, 在4点多, 有一个torando 后端upstream timeout.

**这才发现,查看nginx 的error.log(c92/nginx-1.4.1/logs/error.log)是最直接的方式, 如果有一个后端upstream timeout, 就重启该后端.**

为什么tornado后端会upstream timeout
========================================

鉴于无法直接从代码上发现此问题,所以判断为什么会upstream timeout成了一个难题

nginx windows上只有一个进程, 也有1024的限制,但目前,虽然对它有怀疑,但没有充分根据.

可能的问题

1. 分发问题,打包分发不会导致此问题? 原因在什么地方? 
2. pyzmq版本问题, 当前tornado/pyzmq 均使用最新的版本, 在开发时曾多次发现py文件改变,torando autoload导致pyzmq的io loop终止? (此时理论上tornado后端就完全不能访问)
3. zmq 的req/rep违例了, 即必须请求-接受,不能请求-请求, 用户代码其实没有办法做到这点.
4. application server处理能力不足了? 扩展后能避免此问题
5. 达到1024个限制, 理论上会报错, 浏览端会收到此信息. 可以直接访问一个打印页面测试

所以

首先,再次测试打包分发, 并将application server进程启动为10个, 确认问题是否重现, 今天(6/14再测试)

然后, 以下需要在下次问题重现时验证

1. 当tornado 后端timeout时, 是完全无法连接吗? 需要验证 telnet localhost 后端端口
2. 当tornado 后端timeout时 , 一些不依赖zmq的请求工作正常吗? 需要验证,在服务器上输入 http://localhost:后端端口/application.manifest
3. 当tornado 后端timeout时, 确认是否是向proxy通讯时发生问题. 向application server(其实是通过代理)发出一个请求 localhost:后端端口/api/heart (新增加), 看看是否ok

如果经过验证, torando后端web部分正常,仅仅是向proxy通讯时发生问题, 但proxy和application server是正常的.

也就是表现为如下

1. 用户发起请求
2. nginx 将一个请求转发给其中一个tornado后端
3. 后端 不知道有没有将其转发给proxy(这需要在proxy端作日志), 反正application server应该表现为没有收到.
4. 该请求表现为阻塞,  用户端30秒后失败
5. 出错可能是该请求前面的请求
6. 后面的请求都阻塞


最好的解决方法就是重启该后端. 

如果表现确如前面所述, 出错点无法定位, 通讯可能违反了zmq 的req/rep的断言, 即发必收后再发, 但事实上, 由于tornado是单线程的, 程序代码是无法做到这点,所以还是zmq本身的问题.


监测程序
=============================

原理能简单,就是定时访问后端,查看是否超时或正常返回, 如果超时,就尝试重启服务

为了达到这个目的,特地增加了一个/api/heart , 请求该url , tornado -> proxy -> application server -> proxy -> tornado, 返回一个ok. 超时比方说30秒,就是阻塞了.


