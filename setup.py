from setuptools import setup, find_packages, find_namespace_packages

def version_dev(version):
    from setuptools_scm.version import get_local_node_and_date

    if version.dirty:
        return get_local_node_and_date(version)
    else:
        return ""

package_dir = {
  'dao_analyzer.web': 'dao_analyzer/web',
  'dao_analyzer.cache_scripts':  'cache_scripts',
  'dao_analyzer.dac': 'dao_analyzer_components/dao_analyzer_components',
}

def util_add_prefix_to_list(prefix, package_list):
    return [ '.'.join([prefix, p]) for p in package_list]

def custom_f_packages(f, *args, **kwargs):
    package_list = []
    for p, d in package_dir.items():
        package_list.append(p)
        package_list.extend(util_add_prefix_to_list(p, f(d)))
        
    return package_list

def print_packages(f):
    print(f"packages with {f.__qualname__}: {custom_f_packages(f)}")
    return custom_f_packages(f)

def main():
    setup(
        # Fix in case we need to build sdist instead
        use_scm_version={
            'local_scheme': version_dev,
            'write_to': 'dao_analyzer/web/_version.py',
        },
        setup_requires=['setuptools_scm'],
        packages = print_packages(find_packages),
        namespace_packages = ['dao_analyzer'],
        package_dir = package_dir,
    )

if __name__ == "__main__":
    main()
