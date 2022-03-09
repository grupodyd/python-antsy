from setuptools import setup, find_packages


setup(
    name='python-antsy',
    version='0.0.1',
    license='MIT',
    author="Juan F. Duque",
    author_email='jfduque@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/grupodyd/python-antsy',
    keywords='antsy',
    install_requires=[
          'requests',
      ],

)
