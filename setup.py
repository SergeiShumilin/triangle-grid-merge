import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="triangular-grid-merge",
    version="1.0.0",
    author="Example Author",
    author_email="ishumili@gmail.com",
    description="Easy generate, read, merge and print tecplot triangular grids.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SergeiShumilin/triangle-grid-merge",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
)