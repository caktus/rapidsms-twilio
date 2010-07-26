from distribute_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

# packages = find_packages()
# packages.remove('sample_project')
setup(
    name='rtwilio',
    version='0.0.1',
    author='Caktus Consulting Group',
    author_email='solutions@caktusgroup.com',
    packages=find_packages(),
    include_package_data=True,
    exclude_package_data={
        '': ['*.sql', '*.pyc'],
    },
    url='http://github.com/caktus/rapidsms-twilio/',
    license='LICENSE.txt',
    description='RapidSMS Twilio Backend',
    long_description=open('README.rst').read(),
)
