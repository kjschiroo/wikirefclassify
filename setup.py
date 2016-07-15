from setuptools import setup

setup(
    name='refclassifier',
    version='0.1',
    description='Classifier for wikimedia ref templates',

    author='Kevin Schiroo',
    author_email='kjschiroo@gmail.com',
    license='MIT',

    packages=['refclassifier'],
    install_requires=['mwparserfromhell',
                      'numpy',
                      'scipy',
                      'scikit-learn']
)
