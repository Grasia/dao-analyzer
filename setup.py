from setuptools import setup

def version_dev(version):
    from setuptools_scm.version import get_local_node_and_date

    if version.dirty:
        return get_local_node_and_date(version)
    else:
        return ""

def main():
    setup(
        # Fix in case we need to build sdist instead
        use_scm_version={
            'local_scheme': version_dev
        },
        setup_requires=['setuptools_scm']
    )

if __name__ == "__main__":
    main()