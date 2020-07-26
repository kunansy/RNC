import pathlib
import re
import sys

from setuptools import setup, find_packages


if sys.version_info < (3, 6):
    raise RuntimeError('Python > 3.6 required')

HERE = pathlib.Path(__file__).parent

txt = (HERE / 'rnc' / '__init__.py').read_text('utf-8')
try:
    version = re.findall(r"^__version__ = '([^']+)'\r?$",
                         txt, re.M)[0]
except IndexError:
    raise RuntimeError('Unable to determine version.')


setup(
    name='rnc',
    version=version,
    url='https://github.com/FaustGoethe/RNC',
    packages=find_packages(exclude='tests'),
    python_requires='>=3.6',
    license='MIT',
    install_requires=['bs4>=0.0.1',
                      'beautifulsoup4>=4.9.1',
                      'aiohttp>=3.6.2',
                      'lxml>=4.5.2'],
    author="Kolobov Kirill, Python beginner",
    author_email='alniconim@gmail.com',
    description='API for National Russian Corpus',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    zip_safe=False,
)