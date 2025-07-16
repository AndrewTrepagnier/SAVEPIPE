from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="tmin",
    version="0.1.0",
    author="Andrew Trepagnier",
    author_email="andrew.trepagnier@icloud.com",
    description="A comprehensive pipe thickness analysis tool for mechanical integrity engineering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AndrewTrepagnier/tmin",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "tmin=tmin.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "tmin": ["asmetables/*.py"],
    },
)
