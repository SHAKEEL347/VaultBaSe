from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vaultbase",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "cryptography",
        "pycryptodome"
    ],
    description="A module that protects databases using blockchain and high-level encryption, preventing unauthorized access, data breaches, and theft.",
    long_description=long_description,  
    long_description_content_type="text/markdown",  
    author="SHAKEEL",
    author_email="shakeelj33447@gmail.com",
    license="MIT",
    url="https://github.com/SHAKEEL347/VaultBaSe-",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
