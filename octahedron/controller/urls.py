from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),

    url(r'^host_manage/check_host/$', views.check_host, name='check_host'),
    url(r"^host_manage/add_host_submit/$", views.add_host_submit, name="add_host_submit"),
    url(r"^host_manage/$", views.host_manage, name="host_manage"),
    url(r'^host_manage/remove_host/$', views.remove_host, name="remove_host"),

    url(r"^module_manage/$", views.module_manage, name="module_manage"),
    url(r"^module_manage/remove_module/$", views.remove_module, name='remove_module'),
    url(r"^module_manage/add_module_submit/$", views.add_module_submit, name="add_module_submit"),

    url(r"^save_config/$", views.save_config, name="save_config"),
    url(r"^start_task/$", views.start_task, name="start_task"),

    url(r"^HTMLEditor/$", views.HTMLEditor, name="HTMLEditor"),
    url(r"^FileEditor/$", views.FileEditor, name="FileEditor"),
    url(r"^submitFile/$", views.submitFile, name="submitFile"),
    url(r"^openfile/$", views.openfile, name="openfile"),
   # url(r"^websocket_log/$", views.websocket_log, name="websocket_log"),
    # ex: /polls/5/
    #url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    #url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    #url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),

]
