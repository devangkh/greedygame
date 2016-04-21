from django.conf.urls import url
from tasks.views import TaskCreate, TaskUpdate, TaskDelete, TaskList, TagCreate,\
    TagUpdate, TagDelete, TagList

urlpatterns = [
    # ...
    url(r'task/add/$', TaskCreate.as_view(), name='Task-add'),
    url(r'task/(?P<pk>[0-9]+)/$', TaskUpdate.as_view(), name='Task-update'),
    url(r'task/(?P<pk>[0-9]+)/delete/$', TaskDelete.as_view(), name='Task-delete'),
    url(r'^task/$', TaskList.as_view(), name='Task_detail'),
    url(r'tag/add/$', TagCreate.as_view(), name='Tag-add'),
    url(r'tag/(?P<pk>[0-9]+)/$', TagUpdate.as_view(), name='Tag-update'),
    url(r'tag/(?P<pk>[0-9]+)/delete/$', TagDelete.as_view(), name='Tag-delete'),
    url(r'^tag/$', TagList.as_view(), name='Tag_detail'),
    url(r'^search/$', 'tasks.views.search', name='search'),
]