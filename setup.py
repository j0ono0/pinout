import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="pinout",
    version="0.0.15",
    author="John Newall",
    author_email="john@johnnewall.com",
    description="Generate graphical pinout references for electronic hardware.",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/j0ono0/pinout",
    project_urls={
        "Bug Tracker": "https://github.com/j0ono0/pinout/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(include=["pinout", "pinout.*"]),
    python_requires=">=3.6",
    install_requires=["Jinja2", "Pillow", "cairosvg"],
    include_package_data=True,
)
