from setuptools import setup
from os import path

dir = path.abspath(path.dirname(__file__))
with open(path.join(dir, 'README.md'), encoding='utf-8') as file:
    long_description = file.read()


setup(name='wikibase-bot',
      version='0.1',
      description='',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/naustica/wikibase-bot',
      author='Nick Haupka',
      author_email='nick.haupka@gmail.com',
      license='MIT',
      packages=['wikibot'],
      keywords=[],
      project_urls={
        'Source': 'https://github.com/naustica/wikibase-bot',
        'Tracker': 'https://github.com/naustica/wikibase-bot/issues'
      },
      install_requires=[
        'requests',
        'pandas',
        'beautifulsoup4',
        'lxml'
      ],
      extras_require={
       'dev': ['pytest',
               'coverage',
               'pytest-cov',
               'requests-mock']
      },
      classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7'
      ],
      zip_safe=False)
