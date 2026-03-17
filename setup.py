import setuptools
import os

def read():
    tmp = ""
    path = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(path, 'README.md'), encoding='utf-8') as f:
        tmp = f.read()
    return tmp

setuptools.setup(
    name="quo_phone_api",
    version="1.0.0",
    author="Felix Hernandez",
    description="Simplified Python bindings for Quo Phone REST API.",
    packages=["quo_phone_api"],
    install_requires=["felog","requests"],
    url="https://github.com/basegodfelix/quo_phone_api",
    long_description = read(),
    long_description_content_type = 'text/markdown',
    license="MIT"
)