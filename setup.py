from setuptools import setup, find_packages

setup(
    name="arduino-serial-plotter",
    version="1.0.2",
    author="pixelistik",
    description="A graphical serial monitor",
    install_requires=['flask'],
    packages=find_packages(),
    include_package_data=True
)
