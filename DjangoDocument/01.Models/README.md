# 模型层
模型是你的数据的唯一的、权威的信息源。它包含你所储存数据的必要字段和行为。通常，每个模型对应数据库中唯一的一张表。

基础：
* 每个模型都是django.db.models.Model 的一个Python 子类。
* 模型的每个属性都表示为数据库中的一个字段。
* Django 提供一套自动生成的用于数据库访问的API；详见执行查询。

#### 字段类型

模型中的每个字段都是 Field 子类的某个实例。Django 根据字段类的类型确定以下信息：

数据库当中的列类型 (比如: INTEGER, VARCHAR)。
渲染表单时使用的默认HTML 部件（例如，`<input type="text">`, `<select>`）。
最低限度的验证需求，它被用在 Django 管理站点和自动生成的表单中。

#### 字段选项

每个字段有一些特有的参数，详见模型字段参考。例如，CharField（和它的派生类）需要max_length 参数来指定VARCHAR 数据库字段的大小。

还有一些适用于所有字段的通用参数。 这些参数在参考中有详细定义，这里我们只简单介绍一些最常用的：

* null
如果为True，Django 将用NULL 来在数据库中存储空值。 默认值是 False.
* blank
如果为True，该字段允许为空值默认为False。

>要注意，这与 null 不同。null纯粹是数据库范畴,指数据库中字段内容是否允许为空，而 blank 是表单数据输入验证范畴的。如果一个字段的blank=True，表单的验证将允许该字段是空值。如果字段的blank=False，该字段就是必填的。

* choices
由二项元组构成的一个可迭代对象（例如，列表或元组），用来给字段提供选择项。 如果设置了choices ，默认的表单将是一个选择框而不是标准的文本框，而且这个选择框的选项就是choices 中的选项。
例如:
```python
SHIRT_SIZES = (
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    )
```
每个元组中的第一个元素，是存储在数据库中的值；第二个元素是在管理界面或 ModelChoiceField 中用作显示的内容。

* default
字段的默认值。可以是一个值或者可调用对象。如果可调用 ，每有新对象被创建它都会被调用。

* primary_key
如果为True，那么这个字段就是模型的主键。
如果你没有指定任何一个字段的primary_key=True，Django 就会自动添加一个IntegerField 字段做为主键，所以除非你想覆盖默认的主键行为，否则没必要设置任何一个字段的primary_key=True

* unique
如果该值设置为 True, 这个数据字段在整张表中必须是唯一的

### 关系
#### 多对一关系 
Django 使用 django.db.models.ForeignKey 定义多对一关系。和使用其它字段类型一样：在模型当中把它做为一个类属性包含进来。

比如，一辆汽车（Car）有一个制造商（Manufacturer） —— 但是一个制造商（Manufacturer） 生产很多汽车（Car），每一辆汽车（Car） 只能有一个制造商（Manufacturer） —— 使用下面的定义：
```python
from django.db import models

class Manufacturer(models.Model):
    # ...
    pass

class Car(models.Model):
    manufacturer = models.ForeignKey(Manufacturer)
```

#### 多对多关系
ManyToManyField 用来定义多对多关系，用法和其他Field 字段类型一样：在模型中做为一个类属性包含进来。

#### 多对多关系中的其他字段¶
处理类似搭配 pizza 和 topping 这样简单的多对多关系时，使用标准的ManyToManyField  就可以了。但是，有时你可能需要关联数据到两个模型之间的关系上。

例如，有这样一个应用，它记录音乐家所属的音乐小组。我们可以用一个ManyToManyField 表示小组和成员之间的多对多关系。但是，有时你可能想知道更多成员关系的细节，比如成员是何时加入小组的。

对于这些情况，Django 允许你指定一个中介模型来定义多对多关系。 你可以将其他字段放在中介模型里面。源模型的ManyToManyField 字段将使用through 参数指向中介模型。对于上面的音乐小组的例子，代码如
```python
from django.db import models

class Person(models.Model):
    name = models.CharField(max_length=128)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(Person, through='Membership')

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Membership(models.Model):
    person = models.ForeignKey(Person)
    group = models.ForeignKey(Group)
    date_joined = models.DateField()
    invite_reason = models.CharField(max_length=64)
```
