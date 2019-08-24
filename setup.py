from setuptools import setup, find_packages

setup(name='hcivisualgesture',
      version='0.1.0',
      description='HCI based on Computer Vision',
      url='',
      author='Project: Asistente Virtual (Unicatolica Lumen Gentium)',
      author_email='cdfbdex@gmail.com',
      license='BSD (3-clause)',
      packages=find_packages(),
      install_requires=['opencv-python', 'scipy', 'scikit-learn',  'joblib', 'pandas'],
      zip_safe=False)
