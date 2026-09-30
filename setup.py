from setuptools import setup

with open("README.md", "r") as f:
    readme = f.read()  # force no build without readme

setup(
    name="KingdomsAndWarfare",
    version="0.3.0",
    description="Kingdoms, Units, Unit Traits all for MCDM's excellent expansion for D&D",
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=[
        "KingdomsAndWarfare.Traits",
        "KingdomsAndWarfare.Units",
        "KingdomsAndWarfare.Kingdoms",
    ],
    python_requires=">=3.14",
    project_urls={"Source": "https://github.com/bleehu/PyMCDMKingdomsAndWarfare"},
)
