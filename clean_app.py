import logging
import os
import shutil
import tempfile
import time
from argparse import ArgumentParser
from pathlib import Path

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


def main():
    args = ArgumentParser()
    args.add_argument("zipfile", help="Path to unclean python zipped project")
    args = args.parse_args()
    clean_arch(args.zipfile)


def clean_arch(file):
    with tempfile.TemporaryDirectory() as temp_dir:
        extract_file(file, temp_dir)
        track_file(temp_dir, "__init__.py")
        zip_folder(f"{Path(file).stem}_new", temp_dir)


def extract_file(file, where):
    try:
        shutil.unpack_archive(file, where)
    except shutil.ReadError:
        logger.error("error extracting file")


def track_file(path, file):
    deleted_list = []
    for dirpath, dirnames, files in os.walk(path):
        keep = False
        if os.path.basename(dirpath) == os.path.basename(path):
            continue
        for file_name in files:
            if file_name == file:
                logger.info(f"file found in {dirpath}")
                keep = True
                break
        if not keep:
            delete_dir(dirpath)
            deleted_list.append(dirpath)
    log_to_file('cleaned.txt', deleted_list)


def log_to_file(filename, dir_list):
    with open(filename, 'w') as file:
        for path in dir_list:
            file.write(path)
            file.write("\n")


def delete_dir(folder):
    try:
        logger.info(f"deleting folder {folder}")
        shutil.rmtree(folder)
    except OSError as e:
        logger.error(f'Error: {folder} : {e.strerror}')


def zip_folder(zipfile, data):
    shutil.make_archive(zipfile, 'zip', data)


if __name__ == "__main__":
    main()