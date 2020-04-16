import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Rbhctest",
    packages=['RBHC'],
    version="1.0.0-rc12",
    author="Ashwith Atluri",
    author_email="Ashwith_Atluri@intuit.com",
    description="RBHC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.intuit.com/aatluri/RBHC",
    install_requires=[
          'pandas',
          'scikit-learn',
          'numpy',
          'matplotlib',
          'jupyter'
      ]
)
