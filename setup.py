from setuptools import setup, find_packages
from pathlib import Path

from dao_analyzer import __version__

long_description_fname = Path("ABOUT.md")
if not long_description_fname.is_file():
    long_description_fname = Path("README.md")

with open(long_description_fname, "r", encoding="utf-8") as fh:
    long_description = fh.read()

def main():
    setup(
        name="dao-analyzer",
        version=__version__,
        author="David Davó",
        author_email="ddavo@ucm.es",
        description="Tool to monitor dao activity",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/Grasia/dao-analyzer",
        project_urls={
            "Bug Tracker": "https://github.com/Grasia/dao-analyzer/issues"
        },
        install_requires=[
            "dash >= 2.0.0",
            "Werkzeug < 2.1.0", # Waiting for upstream fix on dash part
            "flask >= 2.0.2",
            "gql >= 3.0.0a1 ",
            "gunicorn >= 20.1.0",
            "millify >= 0.1.1",
            "numpy >= 1.17.3",
            "pandas >= 1.3.4",
            "portalocker >= 2.3.2",
            "pyarrow >= 6.0.0",
            "requests >= 2.26.0",
            "requests-cache >= 0.8.1",
            "requests-toolbelt >= 0.9.1",
            "tqdm >= 4.62.3"
        ],
        # include_package_data=True,
        package_data= {
            'dao_analyzer': ['assets/*'],
            # Include jsons from cache_scripts
            'cache_scripts': ['*.json', '*/*.json']
        },
        # Available classifiers on https://pypi.org/classifiers/
        classifiers=[
            # How mature is this project?
            # 3 - Alpha
            # 4 - Beta
            # 5 - Production/Stable
            'Development Status :: 5 - Production/Stable',
            'Environment :: Console',
            'Environment :: Web Environment',
            'Framework :: Dash',
            'Intended Audience :: Science/Research',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Topic :: Scientific/Engineering :: Visualization',
            'Topic :: Sociology',
            'Typing :: Typed'
        ],
        package_dir={
            "dao_analyzer": "./dao_analyzer/",
            "cache_scripts": "./cache_scripts/"
        },
        packages=find_packages(where='.'),
        entry_points={
            'console_scripts': [
                'daoa-cache-scripts = cache_scripts.main:main',
                'daoa-server = dao_analyzer.app:main'
            ]
        },
        python_requires=">=3.7"
    )

if __name__ == "__main__":
    main()