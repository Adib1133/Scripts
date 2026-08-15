"""Setup script for pdf2docx production module."""

from setuptools import setup, find_packages
import os

# Read the contents of README file
def read_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="pdf2docx-production",
    version="1.0.0",
    author="PDF to DOCX Converter Team",
    author_email="noreply@example.com",
    description="Production-ready PDF to DOCX converter with OCR and fidelity checking",
    long_description=read_file("README.md") if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    url="https://github.com/example/pdf2docx-production",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Office Suites",
        "Topic :: Text Processing :: Markup",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pdf2docx>=0.5.0",
        "python-docx>=0.8.0",
        "Pillow>=6.0.0",
        "ocrmypdf>=12.0.0; platform_system!='Windows'",  # Optional on Windows
        "pymupdf>=1.24.0",
    ],
    entry_points={
        "console_scripts": [
            "pdf2docx=pdf2docx.cli:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)