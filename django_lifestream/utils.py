import os
import os.path
from cPickle import load

def validate_sources(sources):
	"""
	Checks that all sources have the required format:
	
	{
		'link': <link to the feed>,
		'class': <class to be used for entries>,
		'content_type': <for example application/atom+xml>,
	}
	
	If a source doesn't have at least these 3 attributes, it will be removed
	from the list
	"""
	for source in sources:
		if not (source.has_key('url') and source.has_key('class') 
			and source.has_key('content_type')):
			print "removing link"
			sources.remove(source)
			
def get_default_dump():
	raise RuntimeError("get_default_dump currently doesn't work. Please specify settings.LIFESTREAM_DUMP instead!")
	s=os.path.abspath(os.environ['DJANGO_SETTINGS_MODULE'])
	return os.path.join(os.path.dirname(s),'lifestream.dump')
	
def get_dump():
	from django.conf import settings
	
	try:
		return settings.LIFESTREAM_DUMP
	except NameError:
		return get_default_path()
		
def load_entries():
	fp = open(get_dump(),'rb')
	try:
		entries = load(fp)
	except:
		entries = []
	finally:
		fp.close()
	return entries