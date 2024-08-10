from setuptools import setup, find_packages

setup(
    name="autorequests", 
    version="0.1.0",  # Version of your package
    description="A Python library for automating HTTP requests",  # Short description
    long_description=open("README.md").read(),  # Long description from your README file
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="mohamedhamma2003@gmail.com",
    url="https://github.com/hcn1z1/AutoRequests", 
    packages=find_packages(), 
    include_package_data=True,  # Include additional files specified in MANIFEST.in
    install_requires=[
        "requests",
        "lxml",
        "configparser"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',  # Minimum Python version required
)
