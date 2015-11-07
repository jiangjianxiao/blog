Go 扔掉template method
-----------------------------------------

:date: 2015-5-14 11:43
:slug: go_discard_template_method

在支持继承的语言中, template method 是代码重用的一种常见方式, 此方法的通用模式是

* 定义一个接口 如BaseService
* 创建一个类实现该接口, 完成程序的主要骨架, 将变动的方法抽象出来, 让子类继承实现


在go中, 这种方式行不通

.. code-block:: go

    package main


    type BaseService interface{
       Invoke(request map[string]interface{})
    }


    type DefaultBaseService struct {
       
    }

    func (self *DefaultBaseService) Invoke(request map[string] interface{}){

        self.ReadId()
    }

    func (self *DefaultBaseService) ReadId() {
      
        println("DefaultBaseService");
    }


    type UserService struct {
       DefaultBaseService
    }

    func (self *UserService) ReadId(){
        println("UserService")

    }

    func main(){
        
        var user_service = &UserService{}
        user_service.Invoke(nil) // 调用的还是DefaultBaseService方法
        user_service.ReadId() // 调用的才是user_service

    }




