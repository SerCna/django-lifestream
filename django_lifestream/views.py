from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from django_lifestream import utils


def index(request):
	"""
	Renders the lifestream as read from settings.LIFESTREAM_DUMP
	"""
	from cPickle import load
	sources = list(settings.LIFESTREAM_SOURCES)
	utils.validate_sources(sources)
	fp = open(utils.get_dump(),'rb')
	try:
		entries = load(fp)
	except:
		entries = []
	finally:
		fp.close()
	tvars = {
		'entries':entries,
		'sources':sources,
	}
	return render_to_response('django_lifestream/lifestream.html',RequestContext(request,tvars))