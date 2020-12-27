from setuptools import setup, find_packages

setup(
  name='advanced-search-backend',
  version='0.0.1',
  packages=find_packages(include=['search', 'search.*']),
  url='',
  license='',
  author='Evgeny Sorokin',
  author_email='evgeniy.inpl.sorokin@gmail.com',
  description='Backend part for advanced-website-search.'
)