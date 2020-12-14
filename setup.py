from setuptools import setup, find_namespace_packages

def _parse_requirements(file_path):
    with open(file_path, 'r') as stream:
        file = stream.readlines()
    return file


VERSION = "1.0"

def readme():
    with open("README.md", encoding="utf-8") as f:
        return f.read()

setup(
    name="focusdetection",
    version=VERSION,
    description="Detect in-focus areas in photos.",
    long_description=readme(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
    ],
    keywords="photography opencv",
    url="https://github.com/luismavs/FocusDetection",
    author="Luís Seabra",
    author_email="luismavseabra@gmail.com",
    install_requires=_parse_requirements("requirements.txt"),
    license="MIT",
    python_requires=">=3.7",
    zip_safe=False,
)