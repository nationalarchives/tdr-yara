#! /usr/bin/python3
import yara

import os

RULES_DIR = "."


def get_rules_files():
    for root, s, files in os.walk(RULES_DIR):
        for filename in files:
            lower_filename = filename.lower()
            if lower_filename.endswith('.yar') or lower_filename.endswith('.yara'):
                yield os.path.relpath(os.path.join(root, filename), start=RULES_DIR)


yara_rules = get_rules_files()
rules_files = {relative_path: os.path.join(RULES_DIR, relative_path)
               for relative_path in yara_rules}

rules = yara.compile(filepaths=rules_files,
                     externals={'extension': '', 'filename': '', 'filepath': '', 'filetype': ''})
rules.save("/output")
