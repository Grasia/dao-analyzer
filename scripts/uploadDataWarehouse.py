#!/usr/bin/env python3
import os
import tempfile
from pathlib import Path
import shutil
import json

from tqdm import tqdm

DEFAULT_DATAWAREHOUSE = Path(os.getenv('DAOA_DW_PATH', 'datawarehouse'))

def getDwPaths():
    """ Returns dw paths """
    return [
        './datawarehouse/'
    ]

def archivedw(dw, tmpdir):
    import pandas as pd

    paths = []
    
    for f in dw.glob('*.txt'):
        shutil.copy(f, tmpdir)
        paths.append(f)

    for f in dw.glob('*/metadata.json'):
        newp = tmpdir / Path(f).relative_to(dw).parent
        newf = newp / Path(f).name

        newp.mkdir(exist_ok=True)
        shutil.copy(f, newf)
        paths.append(newf)
    
    for f in tqdm(list(dw.glob('**/*.arr'))):
        newp = tmpdir / Path(f).relative_to(dw).parent
        newf = newp / Path(f).with_suffix('.csv').name

        pd.read_feather(f).to_csv(newf)
        paths.append(newf)

    return paths

def uploadToZenodo(paths):
    ZENODO_DEPOSITION_ID = os.environ['ZENODO_DEPOSITION_ID']
    ZENODO_SANDBOX = bool(os.environ.get('ZENODO_SANDBOX', False))

    from zenodo_client import Zenodo

    z = Zenodo(None, sandbox=ZENODO_SANDBOX)
    z.update(ZENODO_DEPOSITION_ID, paths)

def archiveToZenodo(tmpdir):
    with tempfile.TemporaryDirectory() as zpath:
        zpath = Path(zpath)
        shutil.make_archive(zpath / 'archive', 'zip', tmpdir)
        uploadToZenodo([zpath / 'archive.zip'])

def uploadToKaggle(path, version_notes):
    from kaggle import api as k
    
    k.dataset_create_version(path, version_notes, dir_mode='zip')

def archiveToKaggle(tmpdir):
    with tempfile.TemporaryDirectory() as kpath:
        kpath = Path(kpath)
        shutil.copytree(tmpdir, kpath, dirs_exist_ok=True)

        with open(kpath / 'dataset-metadata.json', 'w') as md:
            json.dump({
                "id": "daviddavo/dao-analyzer",
            }, md)

        with open(kpath / 'update_date.txt', 'r') as ud:
            update_date = ud.readline()
        
        uploadToKaggle(kpath, update_date)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser("Update datawarehouse in Kaggle and Zenodo")

    available_repos = ['zenodo', 'kaggle']
    parser.add_argument(
        'repos',
        nargs='*',
        default='all',
        choices=[*available_repos, 'all'],
        help="Which repositories to upload the data",
    )

    args = parser.parse_args() 
    if args.repos == 'all':
        args.repos = available_repos

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        print("Archiving datawarehouse")
        archivedw(DEFAULT_DATAWAREHOUSE, tmpdir)
        if 'zenodo' in args.repos:
            print("Uploading to zenodo")
            archiveToZenodo(tmpdir)
        if 'kaggle' in args.repos:
            print("Uploading to kaggle")
            archiveToKaggle(tmpdir)
        