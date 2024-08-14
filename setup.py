from setuptools import setup, find_packages

setup(
    name="wordperchta",
    version="0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # List your dependencies here
    ],
    scripts=["scripts/setup_wordpress.py"],
)
