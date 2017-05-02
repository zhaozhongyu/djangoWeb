# djangoWeb
django 练手之作

## 第一部分:模型
#### 数据库的建立
编辑mysite/settings.py
> 默认数据库是sqlite, 练手之作就不修改了
> 修改TIME_ZONE为CST

```python
#注意文件顶端的INSTALLED_APPS设置。它保存这个Django实例中激活的所有的Django应用的名字。 应用可以在多个项目中使用，而且你可以将这些应用打包和分发给其他人在他们的项目中使用。

#默认情况下，INSTALLED_APPS包含下面的应用，它们都是Django 与生俱来的：

#django.contrib.admin —— 管理站点。第2部分使用到它。
#django.contrib.auth —— 认证系统。
#django.contrib.contenttypes —— 用于内容类型的框架。
#django.contrib.sessions —— 会话框架。
#django.contrib.messages —— 消息框架。
#django.contrib.staticfiles —— 管理静态文件的框架。
# 然而上面的部分应用至少需要使用一个数据库表，因此我们需要在使用它们之前先在数据库中创建相应的表
$ python manage.py migrate
#migrate查看INSTALLED_APPS设置并根据mysite/settings.py文件中的数据库设置创建任何必要的数据库表，数据库的迁移还会跟踪应用的变化
```

#### 创建模型
> 项目和应用之间有什么不同？ 应用是一个Web应用程序，它完成具体的事项 —— 比如一个博客系统、一个存储公共档案的数据库或者一个简单的投票应用。 项目是一个特定网站中相关配置和应用的集合。一个项目可以包含多个应用。一个应用可以运用到多个项目中去。

要创建应用程序, 键入`$ python manage.py startapp library`, library只是一个应用程序的示例, 它可以是名字.这将创建一个目录library，它的结构如下
```python
library/
    __init__.py
    admin.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```
编辑library/models.py文件，并让它看起来像这样：
```python
from django.db import models
from django.utils import timezone
# Create your models here.
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(null=True)
    intro = models.CharField(max_length=5000, null=True)
    def __str__(self):
        return self.first_name + " "+ self.last_name

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    group = models.CharField(max_length=100, null=True)
    web = models.URLField(null=True)
    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    author = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher)
    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, through='Bollow')
    def __str__(self):
        return self.name


class Bollow(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    bollow_date = models.DateField(default=timezone.now)
    def __str__(self):
        return self.user.name + " " + self.book.name + ' ' + str(self.bollow_date)
```
上述代码非常直观。每个模型都用一个类表示，该类继承自django.db.models.Model。每个模型都有一些类变量，在模型中每个类变量都代表了数据库中的一个字段。

每个字段通过Field类的一个实例表示 —— 例如字符字段CharField和日期字段DateTimeField。这种方法告诉Django，每个字段中保存着什么类型的数据。

某些Field 类具有必选的参数。例如，CharField要求你给它一个max_length。

现在,再次编辑mysite/settings.py文件，并修改INSTALLED_APPS设置以包含字符串`library`,让我们运行另外一个命令：
```python
$ python manage.py makemigrations library
```
通过运行makemigrations告诉Django，已经对模型做了一些更改（在这个例子中，你创建了一个新的模型）并且会将这些更改存储为迁移文件。

现在，再次运行migrate以在你的数据库中创建模型所对应的表：
```python
$ python manage.py migrate
```
migrate命令会找出所有还没有被应用的迁移文件（Django使用数据库中一个叫做django_migrations的特殊表来追踪哪些迁移文件已经被应用过），并且在你的数据库上运行它们 —— 本质上来讲，就是使你的数据库模式和你改动后的模型进行同步。

##### 探索模型
在命令行中输入`python manage.py shell`, 进入django的交互模式
现在, 在交换行中进行数据的首步添加工作
```python
#导入models
>>> from library.models import Author, Publisher, Book, User, Bollow
>>> Author.objects.all()  #查看Author当前的数据
<QuerySet []>
>>> a = Author(first_name='li',  last_name = 'goudan')
>>> a
<Author: li goudan>
>>> a.save()
>>> a = Author(first_name = 'zhang', last_name = 'tiezhu')
>>> a
<Author: zhang tiezhu>
>>> a.save()
>>> Author.objects.all()  #查看所有author
<QuerySet [<Author: li goudan>, <Author: zhang tiezhu>]>
>>> p = Publisher(name = 'tsinghua') #增加publisher
>>> p.save()
>>> p = Publisher(name = 'pku')
>>> p.save()
>>> p.name
'pku'
>>> b = Book(name='Django Web', price=100, publisher=p) #注意manytomanyfield不能在这里设置
>>> b.save()
>>> Book.objects.all()
<QuerySet [<Book: Django Web>]>
>>> a.book_set.all()
<QuerySet []>
>>> a.book_set.add(b) #只能用这种方式增加manytomanyfield数据
>>> a.book_set.all()
<QuerySet [<Book: Django Web>]>
>>> b.author.all()
<QuerySet [<Author: zhang tiezhu>]>
>>> a = Author.objects.filter(first_name = 'li') #注意filter返回的是列表
>>> a
<QuerySet [<Author: li goudan>]>
>>> a = Author.objects.get(first_name = 'li') #get返回的是单个对象,当条件中存在两个对象时,返回报错
>>> a
<Author: li goudan>
>>> a.book_set.add(b)
>>> b.author.all()
<QuerySet [<Author: zhang tiezhu>, <Author: li goudan>]>
>>> a.book_set.create(name='Python3', price=123, publisher=p) #还可以通过这种方式直接创建book对象
<Book: Python3>
>>> a.book_set.all()
<QuerySet [<Book: Django Web>, <Book: Python3>]>
>>> Book.objects.all()
<QuerySet [<Book: Django Web>, <Book: Python3>]>
>>> u = User(name='zhang san', password='zhangsan')
>>> u.save()
>>> u
<User: zhang san>
>>> bollow = Bollow(user = u, book = b) #因为设置了default date, 所以不需要date
>>> bollow.save()
>>> u.books.all()
<QuerySet [<Book: Django Web>]>

```


## 第二部分:管理站点
生成用于添加、修改和删除内容的管理性站点是一件单调乏味、缺乏创造力的工作。 为此，Django会根据你写的模型文件完全自动地生成管理界面。
#### 创建一个管理员用户
首先，我们需要创建一个能够登录管理站点的用户。 运行如下命令：
```python
$ python manage.py createsuperuser
```

#### 让library应用在管理站点中可编辑
只需要做一件事：我们需要告诉管理站点Question 对象要有一个管理界面。 要做这件事，需要打开polls/admin.py文件，把它编辑成这样：
```python
from django.contrib import admin

# Register your models here.
from .models import Author
from .models import Publisher
from .models import Book
from .models import User

admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(Book)
admin.site.register(User)
```
#### 启动开发服务器
Django的管理站点是默认启用的。 让我们启动开发服务器，然后探索它。
```python
$ python manage.py runserver 8000
```
现在，打开一个浏览器访问你本地域名中的 “/admin/” —— 例如http://127.0.0.1:8000/admin/


## 第三部分:视图和模板
#### 原理

视图是Django应用中的一“类”网页，它通常使用一个特定的函数提供服务，并且具有一个特定的模板。例如，在博客应用中，可能有以下视图：

- 博客首页 —— 显示最新发表的博客。
- 博客“详细”页面 —— 单篇博客的固定链接页面。
- 基于年份的归档页面 —— 显示某给定年份里所有月份发表过的博客。
- 基于月份的归档页面 —— 显示在给定月份中发表过博客的所有日期。
- 基于日期的归档页面 —— 显示在给定日期中发表过的所有博客名称。
- 评论 —— 对给定的博客发表评论

在Django中，网页的页面和其他内容都是由视图来传递的（视图对WEB请求进行回应）。 每个视图都是由一个简单的Python函数(或者是基于类的视图的方法)表示的。Django通过检查请求的URL（准确地说，是URL里域名之后的那部分）来选择使用哪个视图。

#### 编写你的第一个视图

让我们来编写第一个视图。 打开library/views.py文件并将以下Python代码写入：
```
# library/views.py
from django.shortcuts import render,render_to_response, get_list_or_404,get_object_or_404
from .forms import BookName
from .models import Book
# Create your views here.

def index(request):
    if not request.method=="POST":
        form = BookName() #创建forms.py中的form
        context = {"form": form}
        return render(request, 'library/index.html', context)
    else:
        form = BookName(request.POST) #使用这个方法来获得POST获取到的数据
        if form.is_valid():
            book_name = form.cleaned_data['book_name']
            books = Book.objects.filter(name__contains=book_name) #name__contains的意思是name中包含, 类似于sql中的like %book_name%
            context = {'books': books, 'book_name': book_name}
        else:
            context = {'error':form.errors}
        return render(request, 'library/results.html', context)


def detail(request, book_id):
    book = get_object_or_404(Book, pk=book_id) #get_object_or_404是获取单个对象, 当获取对象有异常时抛出404错误
    context = {'book':book}
    return render_to_response('library/detail.html', context)
```
为了在应用内部使用django提供的form能力, 需要创建一个forms.py文件
```python
from django import forms

class BookName(forms.Form):
    book_name = forms.CharField(label='book name', max_length=100) #创建一个带label的textfield
```

为了在应用目录内部创建URLconf，需要创建一个urls.py文件。

在library/urls.py文件中键入如下代码：
```
from django.conf.urls import url

from . import views

urlpatterns = [
    # like library/
    url(r'^$', views.index, name='index'),
    # like library/2
    url(r'^(?P<book_id>[0-9]+)/$', views.detail, name='detail')
]
```

下一步，让主URLconf可以链接到library.urls模块。在mysite/urls.py中插入一个include()：
```
mysite/urls.py
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^library/', include('library.urls', namespace='library')),
    url(r'^admin/', include(admin.site.urls)),
]
```

#### 模板
首先，在你的polls目录下创建一个叫做 templates的目录。Django将在这里查找模板。

你项目的TEMPLATES设置描述了Django将如何加载并渲染模板。默认的设置文件settings.py配置了一个DjangoTemplates后端，其中将APP_DIRS选项设置为True。按照惯例，DjangoTemplates在 INSTALLED_APPS所包含的每个应用的目录下查找名为"templates"子目录。因此即使我们不像教程 2.中那样去修改DIRS,Django也可以找到应用的模版。

##### 组织模板

我们可以将我们所有的模板聚在一起，放在一个大的模板目录下，且可以运行地很好。然而，我们的这个模板属于library应用，不像我们在先前教程中创建的管理站点模板，为了可重用性考虑,我们将把它们放在应用的模板目录下（library/templates）而不是项目模板目录下（templates）。

在你刚刚创建的templates目录中，创建另外一个目录library，并在其中创建一个文件index.html。换句话讲，你的模板应该位于 library/templates/library/index.html。
```html
<h1>Django Web</h1>
<body>
    <form method="post">
        {% csrf_token %}
        {{ form }}
        <input type="submit" value="Submit" />
    </form>
</body>
```
detail.html
```html
<h1>{{ book.name }}</h1>
```
results.html
```html
<h1>{{ book_name }}</h1>
<body>
    {% for book in books %}
        <li><a href="{% url 'library:detail' book.id %}">{{ book.name }}</a></li>
    {% endfor %}
</body>
```
以下分别解释下html中的各个设置.
* `{% csrf_token %}`为django提供的防范csrf攻击的函数, 只需要在每个form中填入这一行即可
* `{{ form }}`以这个格式表示的form为views函数中context字典设置的变量
* `{% for book in books %}`和`{% endfor %}`共同组成了一个for循环, books为context字典设置的变量
* `{% url 'library:detail' book.id %}`中的library为myweb/urls配置的namespace, detail为urls中配置的url, 这一行的意思就是获取到library:detail表示的url, 并将book.id作为参数传给它

通过以上步骤, 我们已经完成了一个简易的图书搜索能力, 现在执行`python manage.py runserver`, 然后打开浏览器, 查看功能是否正常吧.

## 第四部分:静态文件
除了由服务器生成的HTML文件外，网页应用一般需要提供其它必要的文件 —— 比如图片文件、JavaScript脚本和CSS样式表 —— 来为用户呈现出一个完整的网站。 在Django中，我们将这些文件称为“静态文件”。

#### 自定义你的应用的外观
首先在你的library中创建一个static目录。Django将在那里查找静态文件，这与Django在library/templates/中寻找对应的模板文件的方式是一致的。

在你刚刚创建的static目录中，创建另外一个目录library并在它下面创建一个文件style.css。换句话讲，你的样式表应该位于library/static/library/style.css。
```
li a {
    color: green;
}
```
下一步，在library/templates/library/results.html的顶端添加如下内容 ：
```
{% load staticfiles %}

<link rel="stylesheet" type="text/css" href="{% static 'library/style.css' %}" />
```
`{% load staticfiles %}` 从staticfiles模板库加载`{% static %}` 模板标签。`{% static %}`模板标签会生成静态文件的绝对URL

### End
