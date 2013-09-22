django admin 联动
------------------------------------
:date: 2013-09-22 12:19
:slug: django-admin-linkage


在 django-admin 中实现联动，比方说 省/市下拉列表的联动有些麻烦，但还是可行的，下面说明一下大概的过程， 数据源的不同也会影响一些处理代码，请自行修改。下面的代码其实是在讲country/state的联动，但原理一致。

定义数据源
=================

简单起见， 我们在settings.py定义一个LOCATION 变量

.. code-block:: python

    LOCATION = {"浙江": ["杭州", "宁波"], "湖北": ["武汉", "xxx"]}


models.py 中的model 定义
=================================

这里没有为state定义choices 是因为state的选项是根据country的值变化的

.. code-block:: python

    from django.conf import settings
    from django.db import models

    COUNTRY = [(key, key) for key in sorted(settings.LOCATION.keys())]


    class Company(models.Model):
        country = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Country"), choices=COUNTRY)
        state = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('State'))



admin.py 的定义
==========================

.. code-block:: python

    from django import forms
    from django.contrib import admin


    class CompanyAdminForm(forms.ModelForm):
        state = forms.ChoiceField(label=_('State'), required=False)

        def locations(self):
            import json

            return json.dumps(settings.LOCATION)

        def __init__(self, *args, **kwargs):
            ins = kwargs.get('instance')
            super(CompanyAdminForm, self).__init__(*args, **kwargs)
            state = self.fields['state']

            if ins and ins.country:
                state.choices = [(item, item) for item in settings.LOCATION.get(ins.country)]

        class Meta:
            model = Company


    class CompanyAdmin(admin.ModelAdmin):
        form = CompanyAdminForm

这里， locations 函数等会将用于模板， __init__ 用来设置修改界面首次显示时 state 的选项


templates/admin/app/company/change_form.html
=====================================================

复制原 change_form.html 内容 在合适位置加入（自行写js代码 )

.. code-block:: javascript

    <script type="text/javascript">
        var LOCATION = {{ adminform.form.locations | safe }};

        var $ = django.jQuery;
        $(document).ready(function(){

            $('#id_country').change(function(){

                var country =$(this).val();
                $('#id_state').empty();
                if (country ){

                    var state = LOCATION[country];

                    var i;
                    for (i=0; i < state.length; i++){
                        var v = state[i];
                        $('#id_state').append("<option value='" + v + "'>" + v + "</option>");
                    }

                } else {

                    $('#id_state').append("<option value=''>" + "---------" + "</option>");
                }



            });



        });
    </script>