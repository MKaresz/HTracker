from setuptools import setup

setup(
    name='htracker',
    version='0.1',
    description='habit tracker app',
    author='KarolY Molnar',
    author_email='mr_karesz_molnar@gmail.com',
    packages=['htracker'],
    install_requires=["pytest", "click"]
)