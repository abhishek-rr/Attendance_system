from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('djqgrid',
    (r'query/(?P<grid_id>\w+)$', views.query),)
