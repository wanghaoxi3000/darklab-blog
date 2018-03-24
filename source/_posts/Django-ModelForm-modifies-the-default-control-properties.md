---
title: Django ModelForm修改默认的控件属性
date: 2017/4/9 15:53:00
categories:
- Django
toc: true
---

Django 中利用ModelForm 可以快速地利用数据库对应的Model 子类来自动创建对应表单.

例如:
```
from django.db import models
from django.forms import ModelForm


class Book(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'authors']
```

但这样默认创建的表单是很丑的, 一般需要重写字段的控件属性, 来加入各种效果. 总结下我常用的两种.

### 修改Meta的widgets属性

在Django手册的ModelForm一章中, 提供了这种方式, Book 的name 属性为CharField 如果希望它表示成一个`<textarea>` 而不是默认的`<input type="text">` 时, 可以按如下方式覆盖字段默认的Widget：

```
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'authors']
        widgets = {
            'name': Textarea(attrs={'cols': 80, 'rows': 20}),
        }
```

这种方式可以指定控件的类型及其对应的属性, 不过大部分时候, 默认的控件类型已经够用了, 只需要修改控件的属性. 可以采取另外一种更方便的方法.


### 重写`__init__`方法

通过通过重写`__init__ `方法, 遍历base_fields字段, 来快速修改控件的属性.

```
class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'authors']

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        
        for field_name in self.base_fields:
            field = self.base_fields[field_name]
            field.widget.attes.update({'cols': 80, 'rows': 20})

```
