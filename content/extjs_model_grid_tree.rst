extjs model同时用于grid和tree的问题
-----------------------------------------

:date: 2012-06-04 00:00
:slug: extjs-model-with-grid-tree

当model用在tree中的,extjs会自动mixin NodeInterface ,结果destroy 是由NodeInterface执行,这导致一个问题. 

当你从grid中获取一个model,然后调用destroy时,由于NodeInterface destroy是最终是通过NodeInterface.parentNode来删除的

  parentNode.removeChild(this, destroy, suppressEvents);

但grid中的model ,不存在parent node,会导致destroy 不会向后端发送delete rest命令.

回避的方法是创建两个model,如 SubjectNode/Subject ,一个用于tree,一个用于grid

