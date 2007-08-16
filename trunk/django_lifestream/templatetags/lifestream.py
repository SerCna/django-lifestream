from django import template
from django_lifestream import utils

register = template.Library()

def simple_lifestream(context):
	tpl = template.loader.get_template('django_lifestream/tags/simple_lifestream_entry.html')
	entries = utils.load_entries()
	compiled_entries = ''.join([tpl.render({'entry':entry}) for entry in entries])
	return {
		'entries':compiled_entries,
	}
	
register.inclusion_tag('django_lifestream/tags/simple_lifestream.html',takes_context=True)(simple_lifestream)