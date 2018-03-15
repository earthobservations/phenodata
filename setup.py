import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'requests==2.18.4',
    'requests-ftp==0.3.1',
    'docopt==0.6.2',
    'attrs==17.4.0',
    'pandas>=0.18.1,<=0.22.0',
    'tabulate==0.8.2',
    'dogpile.cache==0.6.5',
    'arrow==0.12.1',
    'tqdm==4.19.7',
    'appdirs==1.4.3',
]

test_requires = [
]

setup(name='phenodata',
    version='0.6.4',
    description='phenodata is a data acquisition and manipulation toolkit for open access phenology data',
    long_description=README,
    license="AGPL 3",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Natural Language :: English",
        "Natural Language :: German",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
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
    url='https://github.com/hiveeyes/phenodata',
    keywords='dwd usa-npn phenology phenometrics opendata bulk data download information research search',
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
    },
    dependency_links=[
    ],

    entry_points={
        'console_scripts': [
            'phenodata  = phenodata.command:run',
        ],
    },

)
