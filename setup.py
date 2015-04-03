from setuptools import setup
from setuptools.command.test import test as TestCommand
import os
import sys


VERSION = '0.0.1'
README = None
with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


class PyTest(TestCommand):

    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        try:
            from ConfigParser import ConfigParser
        except ImportError:
            from configparser import ConfigParser
        config = ConfigParser()
        config.read('pytest.ini')
        self.pytest_args = config.get('pytest', 'addopts').split(' ')

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


setup(
    name='flask-robohash',
    version=VERSION,
    packages=['flask_robohash'],
    install_requires=['Flask', 'Jinja2'],
    tests_require=['pytest', 'coverage', 'coveralls'],
    test_suite='tests',
    include_package_data=True,
    license='MIT',
    description='robohash.org avatars that you can use with the microframework Flask.',
    long_description=README,
    url='https://github.com/syndbg/flask-robohash',
    author='Anton Antonov',
    author_email='anton.synd.antonov@gmail.com',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Browsers',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
    cmdclass={'test': PyTest},
    platforms='any',
    keywords='flask robo robohash.org hash robohash avatars robots monsters microframework',
    zip_safe=True,
)
