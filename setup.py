import setuptools

setuptools.setup(
    name="flappy",
    version="0.0.1",
    author="Larkin Piner",
    author_email="",
    description="A small example package",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "pygame",
        "attrs",
        "numpy",
        "Pillow",
    ],
)