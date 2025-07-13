from setuptools import setup, find_packages

setup(
    name='savepipe',
    version='0.1.0',
    description='Pipe Thickness Analysis & Retirement Planning for Mechanical Integrity Engineering',
    author='Andrew Trepagnier',
    author_email='andrew.trepagnier@icloud.com',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.23',
        'matplotlib>=3.5',
    ],
    entry_points={
        'console_scripts': [
            'savepipe=savepipe.cli:main',
        ],
    },
    python_requires='>=3.7',
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
