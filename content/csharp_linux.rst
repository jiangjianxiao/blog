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

python 通过 zmq 向 .net 的netmq rep发起请求, 初步测试结果如下

* 导出26000条带data validate 的excel 冷启动为2秒左右, 第二次为1.3秒左右, 文件大小为1.5 m, 比pyopenxl 的小很多
* 使用npgsql 插入26000条记录, 约26秒, 相当1秒1000条, 比cpython的约33秒也有一定的进步 


所以有个初步的设想是写个简单c#的服务端, 提供excel的导入导出服务, 两者使用zmq req/rep 协议,josn字符串传递, 二进制使用base64编码传递

