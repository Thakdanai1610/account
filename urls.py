from django.conf.urls import url

from . import views

app_name = 'account'
urlpatterns = [
    url(r'^$', views.show, name='show'),
    url(r'^save/$', views.save_list, name='save_list'),
    url(r'^customize/$', views.custom, name='customize'),
    url(r'^customize/(?P<edit_id>[0-9]+)/edit/$', views.edit, name='edit'),
    url(r'^customize/(?P<edit_id>[0-9]+)/edit/save$', views.edit_save, name='edit_save'),
    url(r'^customize/(?P<remove_id>[0-9]+)/remove/$', views.remove, name='remove'),
    url(r'^customize/(?P<remove_id>[0-9]+)/remove/confirm$', views.remove_confirm, name='remove_confirm'),
] 
