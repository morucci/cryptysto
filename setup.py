from setuptools import setup
import pathlib

here = pathlib.Path(__file__).parent.resolve()

setup(
    name="cryptysto",
    version="0.0.1",
    description="A small tool to compute assets across exchanges",
    url="https://github.com/morucci/cryptysto",
    author="Fabien Boucher",
    author_email="fabien.dot.boucher@gmail.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    keywords="crypto",
    packages=["cryptysto"],
    python_requires=">=3.6, <4",
    install_requires=["dacite"],
    entry_points={
        "console_scripts": [
            "cryptysto=cryptysto.main:main",
        ],
    },
)
