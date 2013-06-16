AttributeError: 'NoneType' object has no attribute '_sa_instance_state'
----------------------------------------------------------------------------

:date: 2012-08-22 00:00
:slug: no_attribute_sa_instance_state


当对sqlalchemy的一些 返回进行pickle处理时会出现如标题的错误，原因是这些返回的类型是sqlalchemy.orm.collections.InstrumentedList

简单的处理将是将其转换为列表，如

.. code-block:: python

	users = list(session.query(Role).get(1).users)
	pickle.loads(pickle.dumps(users))