from setuptools import setup
import os

long_description = ''
try:
    from pypandoc import convert
    if os.path.exists('README.md'):
        long_description = convert('README.md', 'rst')
except ImportError:
    print("warning: pypandoc module not found, could not convert README.md to RST")


setup(
    name="turbotutils",
    version='0.0.1',
    description="TurbotHQ API Library",
    long_description='Python Interface into TurbotHQ\'s Interface to allow for python interaction.',
    author='Michael Osburn <michael@mosburn.com>',
    author_email="michael@mosburn.com",
    url="https://github.com/mosburn/turbot_utils",
    packages=["turbotutils"],
    install_requires=["requests", "configparser"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Application Frameworks"
    ]
)
