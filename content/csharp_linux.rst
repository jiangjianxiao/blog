尝试在ubuntu/os x上使用c#
-----------------------------------------

:date: 2015-5-9 20:34
:slug: ubuntu_os_x_c_sharp

最近微软的举动还是挺让人心动的, 但 https://github.com/dotnet/coreclr 中的dnx 部分, 除了使用mono的运行时, 使用coreclr 在os x/ubuntu 上都没有能跑起来.

最近的一个问题是cpython 的pyopenxl , 导出excel 的write_only优化, 存在着以下问题

* datavalidate list 在write_only=True时无效
* save_virtual_workbook 在write_only=True下无效

但是不启用write_only, 26000多条记录导出在有datevalidate 的情况下跑出20多秒, 无法接受

使用pypy 则会降低到7到5秒, 但目前pypy访问db的性能还是比cpython慢一倍, 无法在正式环境中接受使用它

所以, 有一个想法是想使用mono, 初步的测试是

* netmq
* aspose cells
* json.net
* dapper
* npgsql

python 通过 pyzmq 向 .net 的netmq rep发起请求, 初步测试结果如下

* 导出26000条带data validate 的excel 冷启动为2秒左右, 第二次为1.3秒左右, 文件大小为1.5 m, 比pyopenxl 的小很多
* 使用npgsql 插入26000条记录, 约26秒, 相当1秒1000条, 比cpython的约33秒也有一定的进步 


所以有个初步的设想是写个简单c#的服务端, 提供excel的导入导出服务, 两者使用zmq req/rep 协议,josn字符串传递, 二进制使用base64编码传递(cpython 2.7的字符串实际上是字节数组, 同.net 的字符串是不一样的)


几个问题
===============

* 当dapper 的command timeout 设置似乎无效, 建立连接字符串的 CommandTimeout=60;有效, 待继续排查



mono 安装
============

ubuntu 安装和更新已经非常方便了

    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF
    echo "deb http://download.mono-project.com/repo/debian wheezy main" | sudo tee /etc/apt/sources.list.d/mono-xamarin.list
    sudo apt-get update

如果是 ubuntu 12.04 tls 不敢升级

    echo "deb http://download.mono-project.com/repo/debian wheezy-libtiff-compat main" | sudo tee -a /etc/apt/sources.list.d/mono-xamarin.list
    apt-get update
    apt-get install mono-complete

mono 调试
================

sdb https://github.com/mono/sdb



nuget
==========

ubuntu 用apt-get install nuget

nuget install 安装包, 在 packages.config 所在目录安装, 并用OutputDirectory 指定packages目录 nuget install -OutputDirectory packages


重要文件

* packages.config nuget包文件
* packages nuget 包文件
* csproj/sln 项目文件
* \*.cs
* Properties/\*.cs
* packages.config/app.config
* .settings/\*.json visual studio code 配置文件

.gitignore
    
    Thumbs.db
    \*.dll
    .DS_Store
    packages
    bin
    obj
    \*.userprefs



编辑器
==========

可以使用 visual studio code和ximarin studio 

这里做的笔记是visual studio code 的

使用visual studio code 可参考这个链接 https://code.visualstudio.com/Docs/ASPnet5

* npm install -g yo grunt-cli generator-aspnet bower
* yo aspnet 生成空白项目




编译 用 shift+cmd+b
^^^^^^^^^^^^^^^^^^^^^

cmd+p, configure task runner, 实际修改的是.settings/tasks.json

将默认的任务修改成如下内容：

.. code-block:: json

    {
    "version": "0.1.0",
    "command": "xbuild",
    "args": ["ExcelService.sln"]

    }


也可以直接在项目目录下用xbuild 编译

debug
^^^^^^^^^^^^^^

cmd+p, debug:configure, 实际修改的是.settings/launch.json。

.. code-block:: json

    {
        "version": "0.1.0",
        // List of configurations. Add new configurations or edit existing ones.  
        // ONLY "node" and "mono" are supported, change "type" to switch.
        "configurations": [
            {
                // Name of configuration; appears in the launch configuration drop down menu.
                "name": "Launch ExecelService",
                // Type of configuration. Possible values: "node", "mono".
                "type": "mono",
                // Workspace relative or absolute path to the program.
                "program": "bin/Debug/ExcelService.exe", //要调试的可执行文件位置
                // Automatically stop program after launch.
                "stopOnEntry": true,
                // Command line arguments passed to the program.
                "args": [],
                // Workspace relative or absolute path to the working directory of the program being debugged. Default is the current workspace.
                "cwd": ".",
                // Workspace relative or absolute path to the runtime executable to be used. Default is the runtime executable on the PATH.
                "runtimeExecutable": null,
                // Environment variables passed to the program.
                "env": { }
            }
        ]
    }


参考
==============


http://www.cnblogs.com/dudu/p/mac-coreclr-helloworld.html

http://www.cnblogs.com/murongxiaopifu/p/4489024.html

性能评测, mono 版本比较老, 但大体性能同java差距不能说很大了

http://benchmarksgame.alioth.debian.org/u64q/benchmark.php?test=all&lang=csharp&lang2=java&data=u64q
