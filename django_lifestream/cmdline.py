#!/usr/bin/env python
import sys
import optparse
import logging
import os
import os.path
import datetime
from dateutil.tz import gettz
import time
import feedparser
from cPickle import dump, load

from django_lifestream import utils


LOGGING_FORMAT = '%(asctime)s %(levelname)s %(message)s'


def generate_dump(sources=None,dumpfile=None,tmpfile=None,sort=None):
	"""
	This function does the actual work here. It download all the source
	feeds from settings.LIFESTREAM_SOURCES, merges them and then writes
	them into the specified dumpfile
	"""
	from django.conf import settings
	# Handle timezone settings since django doesn't yet does the tzset call.
	os.environ['TZ']=settings.TIME_ZONE
	try:
	    max_days = settings.LIFESTREAM_MAXDAYS
	except:
	    max_days = None
	    
	time.tzset()
	local_timezone = gettz()
	utc_timezone = gettz('UTC')
	now = datetime.datetime.utcnow().replace(tzinfo=utc_timezone)
		
	if not sources:
		try:
			sources = settings.LIFESTREAM_SOURCES
			logging.debug('Using settings.LIFESTREAM_SOURCES')
		except:
			logging.error('settings.LIFESTREAM_SOURCES not specified!')
			raise
	if not dumpfile:
		try:
			dumpfile = settings.LIFESTREAM_DUMP
		except:
			logging.error('settings.LIFESTREAM_DUMP not specified!')
			raise
	if not tmpfile:
		tmpfile = dumpfile+".tmp"
	if not sort:
		sort = sort_entries
	
	sources = list(sources)
	utils.validate_sources(sources)
	
	entries = []
	for source in sources:
		es = feedparser.parse(source['url']).entries
		for e in es: e['_class']=source['class']
		entries+=es
	if len(entries) == 0: sys.exit(0)
	for e in entries:
		try:
			d=e.published_parsed
		except:
			d=e.updated_parsed
		d=datetime.datetime(*(d[:-2]+(utc_timezone,)))
		e['_date']=d
	if max_days:
	    entries = filter(lambda e: (now-e['_date']).days <= max_days, entries)
	# Sort according to published_parsed
	sort_entries(entries)
	output = []
	for e in entries:
		output.append(item_from_entry(e,local_timezone))
	fp = open(tmpfile,'wb+')
	try:
		dump(output,fp)
	finally:
		fp.close()
	import shutil
	shutil.move(tmpfile,dumpfile)


def sort_entries(entries):
	"""
	Sorts the given entries in place
	"""
	entries.sort(cmp=comparison,reverse=True)

def item_from_entry(entry,tz):
	"""
	Converty a preprocessed entry from feedparser (with some minimal 
	modifications) into an item dict for storage. Think "Compression" ;)
	"""
	return {
		'class':entry['_class'],
		'title':entry.title,
		'link':entry.link,
		'date':entry['_date'].astimezone(tz),
	}

def comparison(a,b):
	"""
	Compares two entries based on their parsed date.
	"""
	vala,valb=a['_date'],b['_date']
	if vala == valb: return 0
	if vala <  valb: return -1
	return 1

def run(argv=None):
	"""
	Main method that is executed when the django_lifestream.py script is used.
	It does the usual stuff like setting the debug level as well as setting
	the envvar DJANGO_SETTINGS if it is explicitly passed to the cmdline 
	script.
	"""
	if not argv: argv=sys.argv[1:]
	
	# Define the supported options and check the passed arguments
	parser = optparse.OptionParser()
	parser.add_option('-s','--settings',dest='settings_path',
		help="Path to your Django project's settings file",
		metavar='FILE',
		default=None)
	parser.add_option('-p','--pythonpath',dest='python_path',
		help='Add your project to the PYTHONPATH',
		metavar='PATH',
		default=None)
	parser.add_option('-d','--debug',dest='debug',
		action='store_true',help='Enable the debug mode')
	parser.add_option('-l','--logfile',dest='logfile',
		help='Path to the logfile',
		metavar='FILE',
		default=None)
	
	options,args = parser.parse_args(args=argv)
	logging_config = {
		'format':LOGGING_FORMAT,
		'level': logging.WARNING,
	}
	if options.debug:
		logging_config['level']=logging.DEBUG
	if options.logfile:
		logging_config['filemode']='a+'
		logging_config['filename']=options.logfile
	if options.settings_path:
		os.environ['DJANGO_SETTINGS_MODULE']=options.settings_path
	if options.python_path:
		sys.path.insert(0,options.python_path)
	logging.basicConfig(**logging_config)
	
	generate_dump()
	
	