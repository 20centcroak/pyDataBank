import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyDataBank", 
    version="0.2",
    author="20centCroak",
    author_email="",
    description="module to manage a bunch of resource files using regex or dialogs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/20centcroak/pyDataBank",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)