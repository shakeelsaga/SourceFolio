from setuptools import setup, find_packages

setup(
    packages=find_packages(exclude=["tests*"]),
    py_modules=["main"],
    entry_points={
        'console_scripts': [
            'sourcefolio = main:main',
        ],
    },
)