from django.conf.urls.defaults import *

urlpatterns = patterns('',
	(r'^$','django_lifestream.views.index'),
)
