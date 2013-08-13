osx 笔记
------------------------

大概6年前买过一个macbook, 用不惯, 转手卖掉后入了x61. 如今, 倒是真的喜欢上osx了.

ValueError: unknown locale: UTF-8
======================================

参考 http://patrick.arminio.info/blog/2012/02/fix-valueerror-unknown-locale-utf8/

修改.bash_profile 增加

.. code-block:: bash

	export LANG="en_US.UTF-8"
	export LC_COLLATE="en_US.UTF-8"
	export LC_CTYPE="en_US.UTF-8"
	export LC_MESSAGES="en_US.UTF-8"
	export LC_MONETARY="en_US.UTF-8"
	export LC_NUMERIC="en_US.UTF-8"
	export LC_TIME="en_US.UTF-8"
	export LC_ALL=


install pyqt
====================

1. brew install qt


2. install sip

wget http://www.riverbankcomputing.co.uk/static/Downloads/sip4/sip-4.15-snapshot-bf49a3ad5612.tar.gz
tar xvf ip-4.15-snapshot-bf49a3ad5612.tar.gz

cd sip-4.15-snapshot-bf49a3ad5612
$ python configure.py --incdir=${VIRTUAL_ENV}/include
$ make -j2
$ make install


3. install pyqt
wget http://www.riverbankcomputing.co.uk/static/Downloads/PyQt4/PyQt-mac-gpl-4.10.3-snapshot-e0e54a5ec774.tar.gz
tar xvf PyQt-mac-gpl-4.10.3-snapshot-e0e54a5ec774.tar.gz

$ cd PyQt-mac-gpl-4.10.3-snapshot-e0e54a5ec774
$ python configure.py
$ make -j2
$ make install

4. export DYLD_LIBRARY_PATH=${VIRTUAL_ENV}/lib


pkg_uninstaller
================================

https://github.com/mpapis/pkg_uninstaller

安装在~/.pkg_uninstaller目录下


有意思的命令
==================
* say
* screencapture -iW/-ic/-S
* lsbom

链接
=======================

* _`Mac OS X 平台有哪些值得推荐的常用软件？<http://www.zhihu.com/question/19550256>`
* _`macx.cn <http://www.macx.cn>`

随想
============

* 拟物 1passwd 的柜子,不过我不喜欢此类设计
* 标题栏 通常会放搜索条 登录用户等信息
* 左侧导航 右侧内容
* 两个像osx的linux发行版 elementaryos /pear linux



