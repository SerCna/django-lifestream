from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^$','django_lifestream.views.index'),
	(r'^simple_tag/$','views.simple_tag'),
)
