import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="liwc-analysis",
    version="1.2.4",
    author="Eric Wiener",
    author_email="ericwiener3@gmail.com",
    description="Driver for LIWC2015 analysis. LIWC2015 dictionary not included.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EricWiener/liwc-analysis",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pandas',
    ],
    packages=["liwcanalysis"],
)
