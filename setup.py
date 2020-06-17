import os
import re
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README')).read()
CHANGES = open(os.path.join(here, 'CHANGES')).read()

with open(os.path.join(here, 'forms_api/__init__.py')) as main_file:
    pattern = re.compile(r".*__version__ = '(.*?)'", re.S)
    VERSION = pattern.match(main_file.read()).group(1)


setup(
    name='Forms-API',
    version=VERSION,
    description="Forms handling.",
    long_description=README,
    keywords='forms api',
    author='Vitalii Ponomar',
    author_email='vitalii.ponomar@gmail.com',
    url='https://github.com/ponomar/forms_api',
    license='BSD',
    zip_safe=False,
    platforms='any',
    packages=find_packages(),
    py_modules=['forms_api', 'tests'],
    install_requires=[],
    tests_require=['nose >= 1.3.7'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
)
