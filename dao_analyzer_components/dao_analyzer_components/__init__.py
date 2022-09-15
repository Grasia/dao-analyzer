from __future__ import print_function as _

import os as _os
import sys as _sys
import json

import dash as _dash

# noinspection PyUnresolvedReferences
from ._imports_ import *
from ._imports_ import __all__

if not hasattr(_dash, '__plotly_dash') and not hasattr(_dash, 'development'):
    print('Dash was not successfully imported. '
          'Make sure you don\'t have a file '
          'named \n"dash.py" in your current directory.', file=_sys.stderr)
    _sys.exit(1)

_basepath = _os.path.dirname(__file__)
_filepath = _os.path.abspath(_os.path.join(_basepath, 'package-info.json'))
with open(_filepath) as f:
    package = json.load(f)

package_name = package['name'].replace(' ', '_')
json_fname = package_name.replace('-', '_')
python_package_path = __name__.replace('.', '/')
__version__ = package['version']
namespace_name = 'dao_analyzer_components'

_current_path = _os.path.dirname(_os.path.abspath(__file__))

_this_module = _sys.modules[__name__]

async_resources = []

_js_dist = []

_js_dist.extend(
    [
        {
            "relative_package_path": "async-{}.js".format(async_resource),
            "external_url": (
                "https://unpkg.com/{0}@{2}"
                "/{1}/async-{3}.js"
            ).format(package_name, python_package_path, __version__, async_resource),
            "namespace": namespace_name,
            "async": True,
        }
        for async_resource in async_resources
    ]
)

# TODO: Figure out if unpkg link works
_js_dist.extend(
    [
        {
            "relative_package_path": "async-{}.js.map".format(async_resource),
            "external_url": (
                "https://unpkg.com/{0}@{2}"
                "/{1}/async-{3}.js.map"
            ).format(package_name, python_package_path, __version__, async_resource),
            "namespace": namespace_name,
            "dynamic": True,
        }
        for async_resource in async_resources
    ]
)

print("__name__:", __name__)
print("package_name:", package_name)
print("_this_module:", _this_module.__name__)
print("_basepath:", _basepath)
print("_filepath:", _filepath)
print("_current_path:", _current_path)
_js_dist.extend(
    [
        {
            'relative_package_path': 'dao_analyzer_components.min.js',
            'external_url': (
                f'https://unpkg.com/dao-analyzer-components@{__version__}'
                '/dao_analyzer_components.min.js'
            ),
            'namespace': namespace_name
        },
        {
            'relative_package_path': 'dao_analyzer_components.min.js.map',
            'external_url': (
                f'https://unpkg.com/dao-analzyer-components@{__version__}'
                '/dao_analyzer_components.min.js.map'
            ),
            'namespace': namespace_name,
            'dynamic': True
        }
    ]
)

_css_dist = [
    {
        'relative_package_path': 'dao_analyzer_components.css',
        'external_url': (
            f'https://unpkg.com/dao-analyzer-components@{__version__}'
            '/dao_analyzer_components.css'
        ),
        'namespace': namespace_name
    }
]


for _component_name in _imports_.__all__:
    _component = getattr(_imports_, _component_name)
    _component._js_dist = _js_dist
    _component._css_dist = _css_dist
