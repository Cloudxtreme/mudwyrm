import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'repoze.tm2',
    'zope.sqlalchemy',
    'WebError',
    'pyramid_simpleform',
    'Beaker',
    'pyramid-beaker',
    'Babel',
    ]

if sys.version_info[:3] < (2,5,0):
    requires.append('pysqlite')

setup(name='mudwyrm',
      version='0.1',
      description='mudwyrm',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='mudwyrm',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      main = mudwyrm:main
      """,
      paster_plugins=['pyramid'],
      message_extractors = {'mudwyrm': [
            ('**.py', 'python', None),
            ('templates/**.mako', 'mako', None),
            ('static/**', 'ignore', None)]}
      )

