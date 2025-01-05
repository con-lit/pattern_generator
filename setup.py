from setuptools import setup, find_packages

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="tiles_pattern_generator",
    version="0.0.3",
    description="Generative Art",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://consta.de/",
    author="Constantin Litvak",
    author_email="clitvak@outlook.com",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent"
    ],
    packages= find_packages(include=(
        "tiles_pattern_generator",
        "tiles_pattern_generator.static",
        "tiles_pattern_generator.core",
        "tiles_pattern_generator.core.commons",
        "tiles_pattern_generator.core.fills",
    ), exclude=('test')),
    include_package_data=True,
    package_data={
        '': ['static/truchet_tiles_01/*.svg'],
    },
    install_requires=[
        "pillow",
        "pycairo",
        "cairosvg",
        "numpy",
        "perlin_noise",
        "pytest",
    ],
    python_requires='>=3.6',
)