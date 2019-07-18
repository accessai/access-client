from setuptools import find_namespace_packages
from setuptools import setup
from access_client.about import __version__, __license__

setup(
    name="access-client",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries",
    ],
    author="ConvexHull Technology Private Limited",
    author_email="support@accessai.co",
    maintainer="Majeed Khan",
    maintainer_email="majeed.khan@accessai.co",
    version=__version__,
    url="https://accessai.co/",
    keyword="face detection recognition machine learning",
    packages=find_namespace_packages(exclude=["sample", "tests"]),
    license=__license__,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    install_requires=[
        "pillow==6.0.0",
        "requests==2.22.0"
    ],
)
