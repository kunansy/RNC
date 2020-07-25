from setuptools import setup, find_packages


setup(
    name='rnc',
    vesrion='0.1',
    url='https://github.com/FaustGoethe/RNC',
    packages=find_packages(exclude='tests'),
    license='MIT',
    install_requeres=['bs4>=0.0.1',
                      'beautifulsoup4>=4.9.1',
                      'aiohttp>=3.6.2'],
    author="Kolobov Kirill, Python beginner",
    author_email='alniconim@gmail.com',
    description='API for National Russian Corpus',
    package_dir={'rnc': 'src/corpora'},
    zip_safe=False,
    long_description=open('README.md').read(),
)