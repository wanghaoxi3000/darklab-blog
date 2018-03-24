---
title: Django 用散列隐藏数据库中主键ID
date: 2018/1/23 00:55:00
categories:
- Django
toc: true
---

最近看到了一篇讲[Django性能测试和优化](http://blog.csdn.net/dev_csdn/article/details/78782570)的文章, 文中除了提到了很多有用的优化方法, 演示程序的数据库模型写法我觉得也很值得参考, 在这单独记录下.

原文的演示代码有些问题, 我改进了下, 这里可以查看: https://github.com/wanghaoxi3000/development/tree/master/Python/Django/optimize_django

在实际项目中, 有时需要隐藏数据库中表的主键, 我之前采用的大多是为需要隐藏主键ID的表添加一个字段, 再用散列或者`UUID`等填充来唯一标识一行数据. 而上面提到的文章中则是使用了一个专门生成ID对应散列值的基类, 需要隐藏散列的表可以通过继承这个类来实现隐藏自己的主键ID.

比较特别的是此文的散列值是通过主键ID和`ContentType`的ID来一起生成的. [`ContentType`](https://docs.djangoproject.com/en/2.0/ref/contrib/contenttypes/)是Django自带的一套的框架, 在新模型安装时会自动创建新的`ContentType`实例, `ContentType` 实例具有返回它们表示的模型类的方法, 以及从这些模型查询对象的方法. 从而提供一个高层次的, 通用的接口来与模型进行交互. 

*ContentType使用说明:*
> https://docs.djangoproject.com/en/2.0/ref/contrib/contenttypes/

通过这样的机制, 解码一个散列值后就可以直接得到对应的Django ORM模型类和实例.  对于一些需要一个集中的地方对模型进行解码并对不同类的不同模型实例进行处理时会很有用.

#### Hasher 类代码
```python
from django.contrib.contenttypes.models import ContentType
import basehash


class Hasher:
    base36 = basehash.base36()

    @classmethod
    def from_model(cls, obj, klass=None):
        if obj.pk is None:
            return None
        return cls.make_hash(obj.pk, klass if klass is not None else obj)

    @classmethod
    def make_hash(cls, object_pk, klass):
        # 使用代理模型时通过 for_concrete_model=False 获取代理模型的ContentType
        content_type = ContentType.objects.get_for_model(klass, for_concrete_model=False)
        return cls.base36.hash('%(contenttype_pk)03d%(object_pk)06d' % {
            'contenttype_pk': content_type.pk,
            'object_pk': object_pk
        })

    @classmethod
    def parse_hash(cls, obj_hash):
        unhashed = '%09d' % cls.base36.unhash(obj_hash)
        contenttype_pk = int(unhashed[:-6])
        object_pk = int(unhashed[-6:])
        return contenttype_pk, object_pk

    @classmethod
    def to_object_pk(cls, obj_hash):
        return cls.parse_hash(obj_hash)[1]
```
Hasher 类主要用来完成散列值的计算和解码过程, 将`ContentType`和主键组合后进行`base36`计算, 生成一段12位的代码. 主要使用了`basehash`模块, 通过安装`gmpy2`模块可以进一步提升计算速度.

#### HashableModel 基类
```python
from django.db import models

from .utils import Hasher


class HashableModel(models.Model):
    """提供每个模型提供 Hash ID 的基类"""
    class Meta:
        abstract = True

    @property
    def hash(self):
        return Hasher.from_model(self)
```
`HashableModel` 通过在Meta元选项中设定`abstract = True`而成为Django ORM中的一个基类, 其它模型可以通过继承这个基类来具备产生对应散列的能力. 

#### 基本使用
现在, 通过一个散列值便可以编写很多通用的接口了. 例如有两张表, 都有一个`path`的字段:
```python
class TestModelOne(HashableModel):
    path = models.CharField(max_length=30)

class TestModelTwo(HashableModel):
    path = models.CharField(max_length=30)
```

通过这样一段代码, 便可以同时用来获取两张表的`path`字段了:
```
from django.contrib.contenttypes.models import ContentType

def get_path(hash_id):
    content_id, pk = Hasher.parse_hash()
    obj = ContentType.objects.get_for_id(content_id).get_object_for_this_type(pk=pk)
    return obj.path

```

*参考:*
> http://blog.csdn.net/dev_csdn/article/details/78782570
