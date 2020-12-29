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
    project_urls={
        "Changelog": "https://github.com/kunansy/RNC/blob/master/CHANGELOG.md",
        "Documentation": "https://github.com/kunansy/RNC#api-for-russian-national-corpus",
    },
    keywords=["rnc", "Russian National Corpus", "Linguistics", "API"],
    python_requires='>=3.7',
    license="MIT license",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Education",
        "Topic :: Scientific/Engineering",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",

        "Natural Language :: Bulgarian",
        "Natural Language :: Chinese (Simplified)",
        "Natural Language :: Chinese (Traditional)",
        "Natural Language :: Czech",
        "Natural Language :: English",
        "Natural Language :: Finnish",
        "Natural Language :: French",
        "Natural Language :: German",
        "Natural Language :: Italian",
        "Natural Language :: Latvian",
        "Natural Language :: Lithuanian",
        "Natural Language :: Polish",
        "Natural Language :: Spanish",
        "Natural Language :: Swedish",
        "Natural Language :: Ukrainian",

        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
    ],
    install_requires=["bs4==0.0.1",
                      "beautifulsoup4==4.9.3",
                      "aiohttp==3.7.3",
                      "aiofiles==0.6.0",
                      "lxml==4.6.2",
                      "ujson==4.0.1"],
    extras_require={
      "dev": [
          "pytest",
          "twine",
          "wheel"
      ]
    },
    author="Kolobov Kirill",
    author_email="thekunansy@gmail.com",
    description='API for Russian National Corpus',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    zip_safe=False,
)
