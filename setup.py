from setuptools import setup, find_packages

setup(
    name="autorequests", 
    version="0.1.0",  # Version of your package
    description="A Python library for automating HTTP requests",  # Short description
    long_description=open("README.md").read(),  # Long description from your README file
    long_description_content_type="text/markdown",
    author="hcn1z1",
    author_email="mohamedhamma2003@gmail.com",
    url="https://github.com/hcn1z1/AutoRequests", 
    packages=find_packages(include=['autorequests', 'autorequests.data', 'autorequests.*']),
    include_package_data=True,  # Include additional files specified in MANIFEST.in
    package_data={
        'autorequests.data': ['*.json', '*.ini'],
    },
    install_requires=[
        "requests",
        "lxml",
        "configparser"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',  # Minimum Python version required
)
