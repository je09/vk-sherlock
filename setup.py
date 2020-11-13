from setuptools import setup

setup(
    name='vk-sherlock',
    version='0.2',
    packages=['src', 'src.commands'],
    url='https://github.com/je09/vk-sherlock',
    license='MIT',
    author='je09',
    author_email='',
    description='',
    install_requires=[
        'click==7.1.2',
        'vk-api==11.9.0'
    ],
    entry_points={
        'console_scripts': [
            'vk-sherlock = src.main:cli'
        ]
    },
)