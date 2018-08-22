from setuptools import setup, find_packages

setup(
    name='mpdScheduler',
    version='0.1',
    description='A sleep timer/alarm for MPD',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url='https://github.com/AberDerBart/mpdScheduler.git',
    author='AberDerBart',
    author_email='nonatz@web.de',
    packages=find_packages(),
    install_requires=[
        'python-mpd2',
        'parse'
    ],
    scripts=['bin/mpdScheduler'],
    zip_safe=False,
    license='GPLv3')
