#!/usr/bin/env python3
import setuptools

setuptools.setup(
    name='discord-image-resizer',
    version='0.1',
    description='utility for resizing images before using them in discord chat (or other size restricted environments)',
    author='Nathan Fiscaletti',
    url='https://github.com/nathan-fiscaletti/discord-image-resizer',
    classifiers=[
        'Environment :: Console',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.8',
    ],
    entry_points={
        'console_scripts': [
            'discord-resize=resizer:cli_entry_point'
        ]
    },
    install_requires=[
        'pywin32',
        'pillow'
    ],
    packages=setuptools.find_packages(),
)
