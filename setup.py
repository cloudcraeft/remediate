from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="remediate",
    version="0.0.14",
    packages=['remediate','remediate/runbook'],
    include_package_data=True,
    install_requires=['boto3'],
    python_requires='~=3.7',
    license='MIT',
    author='cloudcraeft',
    author_email='cloudcraeft@outloook.com',
    long_description=long_description,
    url='https://github.com/cloudcraeft/remediate',
    description='integrate previously written remediation code into Demisto',
)
