from setuptools import setup

setup(
    name="scripts",
    version="0.1",
    packages=[],
    scripts=['datetime-rename', 'tree-file-count'],
    install_requires=['argparse', 'tree-format'],
    author="Martin Patz",
    author_email="mailto@martin-patz.de",
    description="A loose collection of scripts.",
    license="GNU GENERAL PUBLIC LICENSE",
    license_file="LICENSE",
)
