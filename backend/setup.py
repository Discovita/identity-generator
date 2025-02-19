from setuptools import setup, find_packages

setup(
    name="discovita",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        line.strip()
        for line in open("requirements.txt").readlines()
        if line.strip() and not line.startswith("#")
    ],
    # Ensure pydantic v2 is installed
    dependency_links=[
        "https://pypi.org/simple/pydantic/"
    ],
    python_requires=">=3.11,<4.0",
)
