from os import path
from setuptools import setup

pwd = path.abspath(path.dirname(__file__))
with open(path.join(pwd, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='pyusuggest',
      version='1.0.1',
      description='API to integrate Ubersuggest with Python',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/Olegario96/pyusuggest',
      author='Gustavo Olegario',
      author_email='gustavo-olegario@hotmail.com',
      license='MIT',
      packages=['pyusuggest'],
      zip_safe=False)
