from setuptools import setup, find_packages

setup(
    packages=['bts', 'fetchers', 'processing'],
    py_modules=['main'],
    entry_points={
        'console_scripts': [
            'sourcefolio = main:main',
        ],
    },
)