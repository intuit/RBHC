import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="RBHC",
    packages=['RBHC'],
    version="1.0.1",
    author="Ashwith Atluri",
    author_email="ashwithatluri@gmail.com",
    description="RBHC",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/intuit/RBHC",
    install_requires=[
          'pandas',
          'scikit-learn',
          'numpy',
          'matplotlib',
          'jupyter'
      ]
)
