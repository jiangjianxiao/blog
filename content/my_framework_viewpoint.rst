我的框架观点
------------------------------------------

:date: 2013-06-30 15:25
:slug: my-framework-viewpoint


我对创建能二次开发的软件一直很迷恋,最早影响我的是ms office,特别是excel.

* excel堪称完美的对象模型
* 内建的vba 开发环境和excel对象模型的完美交互.

很多年前, c3 的模型就借鉴了excel的对象模型构建.


在后来, ms 的axapta 再一次给我很大的影响. axapta 内嵌的application object tree更为完美, 语言级别的orm, 核心保密, 外围开源的模式, 完美的分布式c/s结构,方便的更新方式对我影响很大, 我花了一年左右时间创建了一个叫marsx的项目.

1. 使用delphi 开发
2. 内嵌了paxcompiler语言,允许使用paxcompiler中的pascal语言进行开发
3. 创建了application object tree, 可以ctrl+d启动开发环境
4. 代码编译后放在服务器端数据库, 用户登录时检查更新动态下载代码达到更新效果
5. 创建了activex 控件, 解决发布的问题
6. 借助remobjects dataabstract , 实现分布式数据访问.

marsx 在某些方面是成功的,他达到了我的一些目的: 达成软件即开发环境是可能的, 在开发时也有很好的效率, 特别是ui的定制上, 几乎是客户要什么现场就可以完成. 但主要的问题在paxcompiler, 这是一种编译性质的语言, 它有一些bug和缺少动态语言的灵活性, 加之在delphi这种静态语言上面,也开发不出好的orm, 虽然借助remobject dataabstract对简单的crud做了封装,但复杂数据访问还是以sql开发为主, 时间一长难以维护.

marsx 今年已经算是放弃了.

关于marsx , 大家可以看看我早期在秋毫中发的贴子 http://www.qiuhao.com/thread-12225-1-1.html



大部分小型软件开发公司, 都希望创建一个可定制的框架,然后招一些低级的程序员来工作. 以达到业务不被他人窃取,并且最小化开发成本的要求. 得确, 这也是我早年所想的. 但现在, 则是完全不同.

软件开发中人是第一要务, 思想的碰撞是很重要的, 掌握在某些人手中的思想必然要死亡的!

大而全的框架通常都是自主的,但这就是一个重复创建轮子的问题, 而且, 对于使用这些框架的程序员而言,使用你的轮子对他没有任何帮助, 留不住人. 而且, 轮子无法达到现有开源软件的高度. 比方说

* ui 框架能达到extjs 的高度吗
* orm 能达到sqlalchemy的高度吗
* webserver能达到twisted/tornado的高度吗

这些自创的轮子在一定时候必然遇到瓶颈. 所以说, 使用现有的东西往往更好,但是接下去的问题就是:对这些现有的东西做了过度的封装.甚至于无法更新到新的版本,这当然也是不行的.

所以,我的第二个观点是:封装必须是最佳实践,你对exjts的封装必须是最佳实践,你对sqlalchemy的封装必须是最佳实践....

这样, 使用你的框架的程序员是最舒服的, 他可以重用他的知识, 这也是尊重他人的一种体现.

第三: 选择好你的语言, 我现在认为,对于企业应用 客户端javascript/服务端python是最好的二次开发语言. 他们的eval机制都非常的好. python的import非常的灵活.大量优秀的库,你无法抗拒.

语言选择就像选择女朋友, 每个人心目中的女朋友是不同的. 找到你自己最喜欢的,并且寻找有类似爱好的合作伙伴.


第四: 完美的对象模型还是要追求的,特别是客户端定制. 在b/s时代, 你可以看看google apps script的是怎么构造的.

第五: 能在软件内做二次开发还是需要追求的. 我建议分以下实施(这个慢慢细谈,我也正在将桌面的经验移值到浏览器端, 当然, 我还是基于axapta的一些观点, 大家还可以参考openerp的, 但我觉的openerp是违反了我说的前两点原则的, 所以,我不会向python 开发者推荐用openerp!)

1. 应用程序的元数据存储和调用. 参考c9的菜单, 菜单项, 安全键, baseenum , tables 等机制.
2. ui的构造, 在软件中直接创建,修改界面. 参考c9的forms, querties, report
3. 脚本的创建和访问. 在软件中直接写脚本,存储并暴露给用户. 参考c9的forms, querites, reports, jobs
4. 服务端修改. 参考 c9的classes







