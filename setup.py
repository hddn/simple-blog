from setuptools import setup, find_packages

setup(
    name = 'simple blog',
    version = '0.3',
    packages = find_packages(),
    install_requires = ['Flask', 'Pillow'],
    author = 'Andriy Kuchuk',
    description = 'Simple Blog on Flask',
    )
