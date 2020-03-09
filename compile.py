#! /usr/bin/python3
import yara
import glob

rules_files = {path: path for path in glob.glob("yar/*.yar*")}
rules = yara.compile(filepaths=rules_files,
                     externals={'extension': '', 'filename': '', 'filepath': '', 'filetype': '', 'certificate': ''})
rules.save("/output")