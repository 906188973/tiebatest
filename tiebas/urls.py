from django.urls import path, re_path
from . import views

urlpatterns = [
    #主页
    path('', views.index, name='index'),
    #显示所有的帖子主题
    path('topics/', views.topics, name='topics'),
    #显示特定帖子
    re_path(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    #评论
    path('update_comment/', views.update_comment, name='update_comment'),
    #删除楼层
    re_path(r'^poster_del/(?P<id>\d+)/$', views.poster_del, name='poster_del'),
    #删除回复
    re_path(r'^reply_del/(?P<id>\d+)/$', views.reply_del, name='reply_del'),
]