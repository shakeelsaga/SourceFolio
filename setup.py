from setuptools import setup

setup(
    packages=["fetchers", "processing"],  
    py_modules=["main"],                  
    entry_points={
        'console_scripts': [
            'sourcefolio = main:main',
        ],
    },
)