import pathlib
from setuptools import setup

VERSION = 'v0.0.11.1'

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
  name = 'zippyshare-downloader',         
  packages = ['zippyshare_downloader'],   
  version = VERSION,
  license='MIT',
  description = 'Download file from zippyshare directly from python',
  long_description= README,
  long_description_content_type= 'text/markdown',
  author = 'Rahman Yusuf',              
  author_email = 'danipart4@gmail.com',
  url = 'https://github.com/trollfist20/zippyshare-downloader',  
  download_url = 'https://github.com/trollfist20/zippyshare-downloader/archive/%s.tar.gz' % (VERSION),
  keywords = ['zippyshare', 'zippyshare-download'], 
  install_requires=[           
          'requests',
          'bs4',
          'download'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',
  ],
  python_requires='>=3'
)
