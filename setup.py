import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'arrow>=0.12.1,<1.3',  # Verified to work on 0.17.0.
    'attrs>=17.4.0',
    'docopt>=0.6.2',
    'dogpile.cache>=0.6.5,<2',  # Verified to work on 1.1.1.
    'future',
    'pandas>=0.23.4,<2.1',
    'platformdirs<4',
    'requests>=2.18.4,<3',
    'requests-ftp>=0.3.1,<4',  # Verified to work on 0.3.1.
    'tabulate>=0.8.2,<0.10',  # Verified to work on 0.8.7.
    'tqdm>=4.60,<5',
]

test_requires = [
]

setup(name='phenodata',
    version='0.13.0',
    description='phenodata is an acquisition and processing toolkit for open access phenology data',
    long_description=README,
    license="AGPL 3, EUPL 1.2",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Natural Language :: English",
        "Natural Language :: German",
        "Natural Language :: Latin",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Topic :: Database",
        "Topic :: Education",
        "Topic :: Internet :: File Transfer Protocol (FTP)",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Software Development :: Libraries",
        "Topic :: System :: Archiving",
        "Topic :: Text Processing :: Filters",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        ],
    author='Andreas Motl',
    author_email='andreas@hiveeyes.org',
    url='https://github.com/earthobservations/phenodata',
    keywords='phenology phenology-data phenology-models phenology-modelling phenometrics '
             'opendata scientific research-data dwd gpm usa-npn',
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'phenodata': [
            'dwd/*.json',
        ],
    },
    zip_safe=False,
    test_suite='nose.collector',
    install_requires=requires,
    tests_require=test_requires,
    extras_require={
        'sql': ['duckdb>=0.3,<0.8']
    },
    dependency_links=[
    ],

    entry_points={
        'console_scripts': [
            'phenodata  = phenodata.command:run',
        ],
    },

)
