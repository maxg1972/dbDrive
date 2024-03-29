from setuptools import setup

settings = dict()

setup(
    name='dbDrive',
    version='1.0',
    description='Utilities to facilitate INI file handling',
    long_description=open('README.md').read(),
    author='Massimo Guidi',
    author_email='maxg1972@gmail.com',
    url='https://github.com/maxg1972/dbDrive',
    py_modules=['dbDrive'],
    package_data={'': ['README.md']},
    include_package_data=True,
    install_requires=[''],
    tests_require=[],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Python License (CNRI Python License)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
