from distutils.core import setup

setup(
    name = 'liveodds',
    packages = ['liveodds'],
    version='1.0',
    author="JG",
    description="A library for live horse racing odds in UK and Ireland",
    author_email="noplundy@gmail.com",
    url="https://github.com/4A47/liveodds",
    download_url = 'https://github.com/4A47/liveodds/archive/v1.0.tar.gz',
    keywords = ['Horse Racing', 'Live Odds', 'Betting'],
    install_requires=[
          'lxml',
          'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    )
