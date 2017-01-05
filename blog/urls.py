from django.conf.urls import url, include, patterns
from blog import views

urlpatterns = [
    url(r'^$', views.view_homepage, name=''),
    url(r'about/$', views.view_aboutpage, name='about'),
    url(r'contact/$', views.view_contactpage, name='contact'),
    url(r'blog/makepost/$', views.view_makepost, name='makepost'),
    url(r'blog/(?P<slug>[\w-]+)/$', views.view_blogpost, name='post'), 
    url(r'blog/(?P<slug>[\w-]+)/updatepost/$', views.view_updatepost, name='updatepost'),
    url(r'blog/(?P<slug>[\w-]+)/deletepost/$', views.view_deletepost, name='deletepost'),
]