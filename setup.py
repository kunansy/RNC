import pathlib
import re
import sys

from setuptools import setup, find_packages


if sys.version_info < (3, 7):
    raise RuntimeError('Python >= 3.7 is required')

HERE = pathlib.Path(__file__).parent
txt = (HERE / 'rnc' / '__init__.py').read_text('utf-8')

try:
    version = re.findall(
        r"^__version__ = '([^']+)'\r?$", txt, re.M)[0]
except IndexError:
    raise RuntimeError('Unable to determine version.')


setup(
    name='rnc',
    version=version,
    url='https://github.com/kunansy/RNC',
    packages=find_packages(exclude='tests'),
    python_requires='>=3.7',
    license='MIT',
    install_requires=['bs4',
                      'beautifulsoup4>=4.9',
                      'aiohttp>=3.6',
                      'lxml>=4.5',
                      'aiofiles>=0.5',
                      'aiojobs>=0.3',
                      'lxml',
                      'ujson'],
    author="Kolobov Kirill",
    author_email='alniconim@gmail.com',
    description='API for Russian National Corpus',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    zip_safe=False,
)
