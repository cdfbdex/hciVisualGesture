from setuptools import setup, find_packages

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

setup(name='hcivisualgesture',
      version='0.1.0',
      description='HCI based on Computer Vision',
      url='',
      author='Project: Asistente Virtual (Unicatolica Lumen Gentium)',
      author_email='cdfbdex@gmail.com',
      license='BSD (3-clause)',
      packages=find_packages(),
      install_requires=parse_requirements('requirements.txt'),
      zip_safe=False)
