from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = ''.join(f.readlines())

setup(
    name='OrodaelTurrim',
    version='1.2.3',
    description='Expert system based tower defense',
    long_description=long_description,
    author='Jan Horáček',
    author_email='horacj10@fit.cvut.cz',
    license='Public Domain',
    url='',
    packages=find_packages(),
    package_data={
        '': ['res/images/*.png', 'res/images/*.ui'],
    },
    entry_points={
        'console_scripts': [
        ],
    },
    classifiers=[
        'Framework :: Pytest',
        'Framework :: Sphinx',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
        'Topic :: Games/Entertainment',
        'Topic :: Games/Entertainment :: Arcade',
    ],
    install_requires=['pyqt5', 'antlr4-python3-runtime', 'click', 'multi_key_dict'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'flexmock', 'pytest-ordering'],
    test_suite="tests",
    zip_safe=True,
)
