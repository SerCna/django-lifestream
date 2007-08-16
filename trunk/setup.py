from distutils.core import setup
import os.path

setup(
	name='django-lifestream',
	author='Horst Gutmann',
	author_email='zerok@zerokspot.com',
	description='A simple lifestream implementation for Django',
	packages=['django_lifestream','django_lifestream.templatetags'],
   package_data={ 'django_lifestream': ['templates/django_lifestream/*.*','templates/django_lifestream/tags/*.*'] },
	scripts=[os.path.join('scripts','django_lifestream'),]
)