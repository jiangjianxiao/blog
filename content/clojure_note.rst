clojure 学习笔记
------------------------------------
:date: 2013-06-29 13:48
:slug: clojure-note


学习lisp 可以防止老年痴呆! 所以,我会慢慢的, 不断的反复的看clojure, 即使用不上:).

lisp的基础思想是简单的，但lisp语言是复杂的!

clojure可能是jvm中实现最好的动态语言了, groovy已经沦为java的小弟, 它很少有自己的库(gradle这样的工具不算), jython的更新迟缓, jruby一般就是兼容使用ruby的库,很少有原生为jruby开发的库. 而clojure的库,则是发挥了clojure的特点, 比方说korma 就是一个很吸引人的东西.






lisp基本点
============================

1. 当对一个列表求值时, 第一个是函数, 其他是参数, 用`阻止对列表求值
2. lisp 没有ast这样的过程. 代码就是ast


我所讨厌的东西
============================

太多了, clojure中充满了各种符号的滥用和一件事情多种做法! 我讨厌一种事情有多种做法，很多时候，它意味着总有一些方法不是最佳的，你总是需要做选择，我讨厌做选择！

各种符号的滥用解很大程度上是需要改善lisp的括号使用， 符号使用列表::

    # 的使用。 #{1 2 3 } 表示set, #"\W+" 表示正则, #(> (count %) 2) 表示匿名函数， #_宏表示忽略下一个clojure形式.
    * repl 时 *1 *2 *3 表示最近三次求值结果, *e 表示最后一个异常
    % 匿名函数时用%1, %2表示第n个参数, % 也可以表示第一个参数.
    , 逗号等于于空格, 可以用来改善可读性
    / 除了表示除法外， 还可以调用java类方法，如(Math/pow), 还可以表示有理数，如 3/5
    \ 表示字符，如\c
    . 除了小数点外， 表示调用java方法，执行对象是后一个参数 (.otherMethod otherObj 0) 或者是new, 如(java.util.ArrayList. 100)
    ->/->>宏
    {}用于 set和map. #{1 2 3}, {"name" "easynew" "url"  "http://blog.easynew.com.cn"}
    & 函数参数列表中是将后续的元素作为一个序列传给&后的变量. (defn f [arg1 arg2 & argn] (println argn)). 如果 (f 1 2 3 4 5) , argn 就是 (3 4 5), 用于解构时也是如此
    : 关键字 如{:name "easynew" :url "http://blog.easynew.com.cn"}
    :as 解构中绑定整个闭合结构到:as 后的变量. (let [[x y :as coords] [1 2 3 4 5 6]]  coords是 [1 2 3 4 5 6]
    ` 阻止对列表求值
    () 列表
    [] vector , [1 2 3]其实就是(vector 1 2 3)
    ; 注释，还可以用comment注释宏，如(comment (* 2 2)), 但comment会返回nil

讨厌的东西

* 导入有require或require+refer或use 或import 处理java导入
* 匿名函数除了用fn定义(fn [w] (> (count w) 2)), 还可以用#(> (count %) 2 ) , 用%1, %2表示第n个参数, % 也可以表示第一个参数.
* 除了false和nil, 其他求值都为true
* (->Book "title" "author ")  (Book. "title" "author"), 第二个是调用构造函数，第一个理解很费脑 ->不是将前一个作为后一个函数的参数吗？


资源
===================================

