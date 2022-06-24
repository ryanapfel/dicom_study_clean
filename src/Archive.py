import logging
import shutil
from tqdm import tqdm
import os


def archvieDirectorySubFolders(input_dir, output_dir):
    logging.info("Zipping of files has begun")
    for ith_dir in tqdm(os.listdir(input_dir)):
        path = os.path.join(input_dir, ith_dir)

        if os.path.isdir(path):
            ouput_file_name = os.path.join(output_dir, ith_dir)
            shutil.make_archive(ouput_file_name, "zip", path)

    logging.info("Zipping of files has concluded")
