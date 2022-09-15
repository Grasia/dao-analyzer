import json
from setuptools import setup


with open('package.json', 'r') as f:
    package = json.load(f)

package_name = 'dao_analyzer.dac'
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
