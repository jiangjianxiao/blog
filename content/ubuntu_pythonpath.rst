ubuntu 中设置 PYTHONPATH
------------------------------------------------------

:date: 2012-08-10 00:00
:slug: ubuntu-pythonpath


一开始 是通过设置环境变量来进行的，可以编辑/etc/profile或是用户目录下的.profile

增加

export PYTHONPAHT=/home/jjx/works/earrow:/home/jjx/works/c92

然后 用source /etc/profile或source .profile生效

但在sudo下无效,如 sudo python

import earrow 还是错误 ，所以 改用 pth的方式 最为简单

先查看python site-packages位置

 
.. code-block:: python

	import sys
	print sys.path

 

然后

	cd /usr/local/lib/python2.7/dist-packages
	sudo gedit my.pth

增加

	/home/jjx/works/earrow
	/home/jjx/works/c92

行之间回车 保存