#!/usr/bin/env python

from distutils.core import setup
from pathlib import Path

repo_dir = Path(__file__).parent

long_description = (repo_dir / 'README.md').read_text()
requirements = (repo_dir / 'requirements.txt').read_text().splitlines()

setup(
      name='xrpc',
      version='1.0',
      author='maxrt',
      author_email='max.r.tkachuk@gmail.com',
      url='https://github.com/maxrt101/xrpc',
      license='MIT',
      description='RPC implementation',
      long_description=long_description,
      long_description_content_type='text/markdown',
      python_requires='>=3.10',
      packages=['xrpc'],
      install_requires=requirements,
      project_urls={
            'Source': 'https://github.com/maxrt101/xrpc',
            'Tracker': 'https://github.com/maxrt101/xrpc/issues',
      }
)