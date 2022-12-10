from setuptools import setup


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Yoku",
    version="1.0.1",
    packages=["yoku"],
    description="A minimal Yahoo! Auctions scraper.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "requests>=2.26.0",
        "beautifulsoup4>=4.11.1",
        "tinydb>=4.7.0",
        "lxml>=4.9.1"
    ],
    entry_points={
        "console_scripts": [
            "yoku = yoku.bot:main",
        ]
    },
)
