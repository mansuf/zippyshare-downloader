import pathlib
from setuptools import setup
import re

HERE = pathlib.Path(__file__).parent
README_PATH = (HERE / "README.md")
README = README_PATH.read_text()

# Find version without importing it
re_version = r'__version__ = \'([0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})\''
_version = re.search(re_version, (HERE / "zippyshare_downloader/__init__.py").read_text())

if _version is None:
  raise RuntimeError("Version is not set")

version = _version.group(1)

requirements = [
  'bs4',
  'requests[socks]',
  'tqdm',
  'aiohttp',
]


extras_require = {
  'docs': [
    'sphinx',
    'furo'
  ],
  'speed': [
    'uvloop',
    'lxml'
  ]
}

packages = [
  'zippyshare_downloader',
  'zippyshare_downloader.cli'
]

setup(
  name = 'zippyshare-downloader',         
  packages = packages,   
  version = version,
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
  download_url = 'https://github.com/trollfist20/zippyshare-downloader/archive/%s.tar.gz' % (version),
  keywords = ['zippyshare', 'zippyshare-download'],
  extras_require = extras_require,
  install_requires=requirements,
  classifiers=[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10'
  ],
  python_requires='>=3.5'
)
