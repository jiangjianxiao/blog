extjs 4 NodeInterface destroy
----------------------------------

:date: 2013-06-16 16:02
:slug: extjs-nodeinterface-destroy


extjs 4 有一些可说是sb的设计， 比方说model的save和destroy服务端报错时不返回responseText， 或许它是一切都在success中处理, 所有访问都是http 200, 错误你自己传递给客户端。 显然这是不现实的。

当然，这个可以通过覆盖 Ext.data.proxy.Server.setException来hack::

	Ext.data.proxy.Server.override({
	  setException: function(operation, response){
	      operation.setException({
	          status: response.status,
	          statusText: response.statusText,
	          responseText: response.responseText //<--Added this line!
	      });
	  }
	});


这里要说的是tree的node的destroy, 无论服务端是否出错， 它一定会把节点给删掉， 不合理啊。 extjs论坛有人发贴 `NodeInterface destroy with callback? <http://www.sencha.com/forum/showthread.php?211235>`_，无人理睬。

当然，贴子中 model.superclass.destroy.call(model, {callback: myCallback}}); 现在也不能用了，因为它在::

 	store.fireEvent('bulkremove', store, [me], [store.indexOf(me)], false);

报错, TreeStore没有indexOf方法，所以，思路只有复制该方法，去除该行

.. code-block:: javascript

	  function node_destroy(me, options) {

	        options = Ext.apply({
	            records: [me],
	            action : 'destroy'
	        }, options);

	        var isNotPhantom = me.phantom !== true,
	            scope  = options.scope || me,
	            stores,
	            i = 0,
	            storeCount,
	            store,
	            args,
	            operation,
	            callback;

	        operation = new Ext.data.Operation(options);

	        callback = function(operation) {
	            args = [me, operation];

	            // The stores property will be mutated, so clone it first
	            stores = Ext.Array.clone(me.stores);
	            if (operation.wasSuccessful()) {
	                for (storeCount = stores.length; i < storeCount; i++) {
	                    store = stores[i];

	                    // If the store has a remove (it's not a TreeStore), then
	                    // remove this record from Store. Avoid Store handling anything by passing the "isMove" flag
	                    if (store.remove) {
	                        store.remove(me, true);
	                    }

	                    // Other parties may need to know that the record as gone
	                    // eg View SelectionModels
	                    // store.fireEvent('bulkremove', store, [me], [store.indexOf(me)], false);
	                    if (isNotPhantom) {
	                        store.fireEvent('write', store, operation);
	                    }
	                }
	                me.clearListeners();
	                Ext.callback(options.success, scope, args);
	            } else {
	                Ext.callback(options.failure, scope, args);
	            }
	            Ext.callback(options.callback, scope, args);
	        };

	        // Not a phantom, t  en we must perform this operation on the remote datasource.
	        // Record will be removed from the store in the callback upon a success response
	        if (isNotPhantom) {
	            me.getProxy().destroy(operation, callback, me);
	        }
	        // If it's a phantom, then call the callback directly with a dummy successful ResultSet
	        else {
	            operation.complete = operation.success = true;
	            operation.resultSet = me.getProxy().reader.nullResultSet;
	            callback(operation);
	        }
	        return me;
	    }
	

然后这样调用::


	node_destroy(rec, {
				success: function(record) {
					
					record.remove();
					

				},
				failure: function(record, operation) {
					Ext.MessageBox.alert('出错了', operation.error.responseText);
				}


			});


可以预见的是，如果extjs 不改变这个设计，你得跟随每个版本更新node_destroy方法！

ok, 看来我不是第一个提出此方法的人 `ExtJS 添加和删除树结点:先向服务器请求 <http://blog.csdn.net/caili314/article/details/7912124>`_