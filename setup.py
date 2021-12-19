from setuptools import setup, find_packages

setup(
    name='blexy',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'starlette',
        'pyyaml',
        'uvicorn',
        'bluepy'
    ],
    entry_points={
        'console_scripts': [
            'yourscript = yourpackage.scripts.yourscript:cli',
        ],
    },
)