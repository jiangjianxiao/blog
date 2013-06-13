ok, 这是我第一篇 pelican blog
----------------------------------

:date: 2013-06-12 04:12
:slug: first-blog 


建议你建两个同级目录，比方说就是jiangjianxiao.github.com和blog, blog用来存放pelican建立的站点, jiangjianxiao.github.com 就是pelican的原始内容

修改 pelicanconf.py, 增加::

	OUTPUT_PATH = '../jiangjianxao.github.com'



pelican-plugins 建议用submodule的方法获取

git submodule git://github.com/getpelican/pelican-plugins.git

然后在其他机器就是git submodule init/git submodule update了



我的publish.sh::

	pelican -s pelicanconf.py content -o ../jiangjinaxiao.github.com

	git add .
	git commit -m "update"
	git push origin master

	cd ../jiangjianxiao.github.com
	git add . 
	git commit -m "Update"
	git push origin master
	cd ../blog


