cefpython 当前的两个问题
----------------------------------------

:date: 2013-07-10 13:56
:slug: cefpython_issues


最近, 使用cefpython 写 yarder.co  的客户端, 使用的是 cefpython和 bootmetro. 主要发现这两个问题, 写下来供大家选择cefpython 时参考.

首先是 当js调用python时, python的异常不会传播到javascript. 这个问题参考 `Throw JS / Python exceptions according to execution context <https://code.google.com/p/cefpython/issues/detail?id=11>`_

所以,当前你的处理方式应该是在python内部处理异常,并返回一个是否成功的状态给js!

.. code-block:: python

	def my_method(self):

		try:

			#你的代码

			return {"success": True, "result": xxxx }
		except Exception as ex:
			# log excpeiton
			return {"success": False, "error": ex.message}



.. code-block:: javascript

	var result = my_method();
	if (result.success){
		// process result.result

	}else{

		alert(result.error);
	}



其次是 javascript 的字符串传递到python时使用的是字节码的方式,你需要显式的转换到utf-8, 就算你做已经做到了下几点

* 网页文件是 utf-8 了
* 网页已经 <meta charset="utf-8"/>
* application_settings已经传递 "string_encoding": "utf-8"
* browser_settings已经传递 "default_encoding": "utf-8" 了

此问题报告在 `Strings should be unicode by default, if bytes is required make it explicit <https://code.google.com/p/cefpython/issues/detail?id=60>`_

目前, 你可以选择将参数打包为json字符串, 然后在python端 用以下代码处理

 .. code-block:: python

 	def my_method(self, data):
 		entity = json.loads(data.decode('utf-8'))


好在这两个问题cefpython的作者都是acceptd了, 希望能很快出更新版本吧
 		

