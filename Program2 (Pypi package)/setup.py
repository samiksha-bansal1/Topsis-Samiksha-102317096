from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Topsis-Samiksha-102317096",
    version="0.1.1",
    author="Samiksha",
    author_email="samikshabansal2005@example.com",  
    description="A Python package for TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution) analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/samiksha-bansal1/Topsis-Samiksha-102317096",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.18.0",
    ],
    entry_points={
        'console_scripts': [
            'topsis=topsis_samiksha_102317096.topsis:main',
        ],
    },
)