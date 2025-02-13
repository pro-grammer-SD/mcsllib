from setuptools import setup, find_packages

setup(
    name="mcsl",  # Library name
    version="1.3-official",      # Version of your library
    packages=find_packages(),
    install_requires=["PyQt6","psutil"],  # External dependencies (if any)
    description="A developing powerful minecraft library in python to host a minecraft server.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Soumalya Das",
    author_email="dassantu8385@gmail.com",
    url="https://github.com/pro-grammer-SD/mcsl",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Python version required
)
