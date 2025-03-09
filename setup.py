from setuptools import setup, find_packages

setup(
    name="dclean",
    version="0.1.0",
    author="Ivan Statkevich",
    author_email="statkevich.ivan@gmail.com",
    description="A tool for analyzing Dockerfiles and Docker images",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/mist941/dclean",
    packages=find_packages(),
    install_requires=[
        "docker>=7.0.0,<8.0.0",
        "dockerfile-parse>=2.0.0,<3.0.0",
        "click>=8.0.0,<9.0.0",
    ],
    entry_points={"console_scripts": ["dclean=dclean.main:cli"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.10",
    keywords=[
        "docker",
        "optimization",
        "cleaning",
        "containerization",
        "security",
        "vulnerability",
        "trivy",
    ],
    project_urls={
        "Bug Reports": "https://github.com/mist941/dclean/issues",
        "Source": "https://github.com/mist941/dclean",
    },
)
