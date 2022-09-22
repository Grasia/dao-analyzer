import json
from setuptools import setup

raise NotImplementedError("Please don't install this package. Install dao-analyzer instead")

with open('package.json', 'r') as f:
    package = json.load(f)

package_name = 'dao_analyzer_components'
package_folder = package["name"].replace(" ", "_").replace("-", "_")

setup(
    name=package_name,
    version=package["version"],
    author=package['author'],
    packages=[package_name],
    package_dir={
        package_name: package_folder,
    },
    include_package_data=True,
    license=package['license'],
    description=package.get('description', package_name),
    install_requires=[],
    classifiers = [
        'Framework :: Dash',
    ],    
)
