from setuptools import setup

setup(
    name="regnskab",
    version="0.1.0",
    packages=["regnskab"],
    package_dir={"": "src"},
    install_requires=[
        'Click',
        "simple-term-menu",
        "pandas",
        "requests",
        "lxml",
        "beautifulsoup4",
        "html5lib",
        "fpdf",
    ],
    entry_points={
        'console_scripts': [
            'regnskab = regnskab.cli:regnskab',
        ],
    },
)
