# djangoWeb
django 练手之作
## 第一部分
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

要创建应用程序, 键入`$ python manage.py startapp polls`, polls只是一个应用程序的示例, 它可以是名字.这将创建一个目录polls，它的结构如下
```python
polls/
    __init__.py
    admin.py
    migrations/
        __init__.py
    models.py
    tests.py
    views.py
```
