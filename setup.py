import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

requires = [
    'arrow>=0.12.1,<1.5',
    'attrs>=17.4.0',
    'charset-normalizer<4',
    'docopt-ng<0.10',
    'dogpile.cache>=0.6.5,<2',
    'legacy-cgi<2.7; python_version>="3.11"',
    'pandas>=1.3,<3.1',
    'platformdirs<5',
    'requests>=2.18.4,<3',
    'requests-ftp>=0.3.1,<4',
    'setuptools<81',
    'sqlalchemy>2,<2.1',
    'tabulate>=0.8.2,<0.10',
    'tqdm>=4.60,<5',
]

test_requires = [
    'datadiff>=2.0,<3',
    'marko<3',
    'proselint==0.16.0; python_version>="3.10"',
    'pytest>=6.1.0,<10',
    'pytest-cov<8',
    'pytest-doctest-ellipsis-markers',
]

setup(name='phenodata',
    version='0.14.0',
    description='phenodata is an acquisition and processing toolkit for open access phenology data',
    long_description=README,
    long_description_content_type='text/x-rst',
    license="AGPL-3.0",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
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
    author_email='andreas.motl@panodata.org',
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
    install_requires=requires,
    extras_require={
        'sql': ['duckdb>=0.3,<1.5'],
        'test': test_requires,
    },
    entry_points={
        'console_scripts': [
            'phenodata  = phenodata.command:run',
        ],
    },

)
