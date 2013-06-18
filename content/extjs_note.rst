extjs 备注
-----------------------------------------

:date: 2012-06-17 00:00
:slug: extjs-note

设置form所有字段只读
=========================

.. code-block:: javascript

	Ext.form.Panel.override({
	 
	  setReadOnlyForAll: function(readOnly) {
	    Ext.suspendLayouts();
	    this.getForm().getFields().each(function(field) {
	      field.setReadOnly(readOnly);
	    });
	    Ext.resumeLayouts();
	  }
	});


1. Store datachanged 对update没有效果, 仅对add/remove有效果, 4.1.1 rc2,所以可能需要同步监听datachanged和update才行

2. Store.loadData,就我个人而言应该设置isLoading返回true,但显然extjs 没有这样做

3. form对record的绑定不行,loadRecord/updateRecord需要手动调用,所以很多时候只能通过form.form.findField().setValue完成更新,设计问题

4. 调用model.destroy() 可以使用success,failure回调,参数是当前model和operation, 典型代码应该是这样

.. code-block:: javascript

	_sel.destroy({

		success:function(rec,operation){
		grid.store.remove(_sel);

	}

	});

 

5. TreeStore和Panel

如果rootVisible 为false 并且没有定义root,则会自动向TreeStore.setRootNode({expanded:true});


这个是需要注意的,因为有时你在TreeStore 中定义了root,但又在panel中设置了rootVisible,这里的建议是在总是在panel中设置root,而不在TreeStore的设置root, 不然在rootVisible=false时,自动生成的root覆盖了treestore中的root


当调用TreeStore.setRootNode时,在如下条件全部成立时自动调用load方法

1. preventLoad!=true ,此参数是setRootNode的第二个参数,通常调用setRootNode会忽略此参数,导致这个条件成立

2. root的expanded 为true 或autoLoad为true, 这里可以看到,光设置autoLoad 为false ,但expanded为true时,也会自动调用load

3. isLoaded为false

所以,建议传递loaded:true到root来达到按需加载的效果

.. code-block:: javascript

	var grid = Ext.create('Ext.tree.Panel', {
		rootVisible: false,
		root: {
			loaded: true,
			expanded: true
		},
		store: Ext.create('Ext.data.TreeStore', {

			"model": 'WorkflowAction',
			autoLoad: false,
			proxy: {
				type: 'ajax',
				url: ''
			}
		})

	});