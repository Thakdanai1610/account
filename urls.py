from django.conf.urls import url

from . import views

app_name = 'account'
urlpatterns = [
    url(r'^$', views.show, name='show'),
    url(r'^save/$', views.save_list, name='save_list'),
    url(r'^import/$', views.import_page, name='import_page'),
    url(r'^import/submit$', views.import_csv, name='import_csv'),
    url(r'^export/$', views.export_csv, name='export_csv'),
    url(r'^customize/$', views.custom, name='customize'),
    url(r'^customize/(?P<edit_id>[0-9]+)/edit/$', views.edit, name='edit'),
    url(r'^customize/(?P<edit_id>[0-9]+)/edit/save$', views.edit_save, name='edit_save'),
    url(r'^customize/(?P<remove_id>[0-9]+)/remove/$', views.remove, name='remove'),
    url(r'^customize/(?P<remove_id>[0-9]+)/remove/confirm$', views.remove_confirm, name='remove_confirm'),
] 
