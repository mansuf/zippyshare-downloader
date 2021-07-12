import pathlib
from setuptools import setup
import re

HERE = pathlib.Path(__file__).parent

README_PATH = (HERE / "README.md")

README = README_PATH.read_text()

# Find version without importing it
REGEX_VERSION = r'v[0-9]{1}.[0-9]{1}.[0-9]{1,3}'
VERSION = re.findall(REGEX_VERSION, (HERE / "zippyshare_downloader/__init__.py").read_text())[0]

setup(
  name = 'zippyshare-downloader',         
  packages = ['zippyshare_downloader'],   
  version = VERSION,
  license='MIT',
  description = 'Download file from zippyshare directly with python',
  long_description= README,
  long_description_content_type= 'text/markdown',
  author = 'Rahman Yusuf',              
  author_email = 'danipart4@gmail.com',
  entry_points= {
    'console_scripts': [
      'zippyshare-dl=zippyshare_downloader.__main__:main',
      'zippyshare-downloader=zippyshare_downloader.__main__:main'
    ]
  },
  url = 'https://github.com/trollfist20/zippyshare-downloader',  
  download_url = 'https://github.com/trollfist20/zippyshare-downloader/archive/%s.tar.gz' % (VERSION),
  keywords = ['zippyshare', 'zippyshare-download'], 
  install_requires=[           
          'requests',
          'bs4',
          'download',
          'aiohttp'
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9'
  ],
  python_requires='>=3.5'
)
