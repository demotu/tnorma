import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tnorma",
    version="0.0.1",
    author="Marcos Duarte",
    author_email="duartexyz@gmail.com",
    description="Temporal normalization (from 0 to 100% with step interval)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/demotu/tnorma",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
