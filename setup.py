import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setuptools.setup(
    name="pinout",
    version="0.0.1",
    author="John Newall",
    author_email="john@johnnewall.com",
    description="Generate graphical pinout references for electronic hardware.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/j0ono0/pinout",
    project_urls={
        "Bug Tracker": "https://github.com/j0ono0/pinout/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["Jinja2>=2.11.3"],
    data_files=[
        ('templates',['pinout/templates/group.svg','pinout/templates/image.svg','pinout/templates/pin_label.svg','pinout/templates/svg.svg']),
        ('templates/styles', ['pinout/templates/styles/pin_label_styles.css'])
    ]
)