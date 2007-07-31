from distutils.core import setup
import os.path

setup(
	name='django-lifestream',
	author='Horst Gutmann',
	author_email='zerok@zerokspot.com',
	description='A simple lifestream implementation for Django',
	packages=['django_lifestream',],
   package_data={ 'django_lifestream': ['templates/django_lifestream/*.*'] },
	scripts=[os.path.join('scripts','django_lifestream'),]
)