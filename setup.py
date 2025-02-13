from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="mcsl-lib",
    version="1.3.post3",
    packages=find_packages(),
    install_requires=requirements,
    description="A developing powerful Minecraft library in Python to host a Minecraft server.",
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
    python_requires='>=3.6',
)
