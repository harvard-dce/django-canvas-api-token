
import os
import re
import codecs
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

def read(path):
    return codecs.open(os.path.join(here, path), 'r', 'utf-8').read()

readme = read('README.rst')
history = read('HISTORY.rst')
version_file = read('canvas_api_token/__init__.py')
version = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M).group(1)

install_requires = ["Django>=1.6","requests"]
tests_require = ['mock']

setup(
    name='django-canvas-api-token',
    version=version,
    packages=['canvas_api_token'],
    url='http://github.com/harvard_dce/django-canvas-api-token',
    license='BSD',
    author='Jay Luker',
    author_email='jay_luker@harvard.edu',
    description='Django app for generating Canvas API user oauth tokens',
    long_description=readme + "\n\n" + history,
    install_requires=install_requires,
    tests_require=tests_require,
    zip_safe=True,
    test_suite="runtests",
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Education'
    ],
)
