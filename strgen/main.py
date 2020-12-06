#!/usr/bin/env python
# Copyright 2020 Daisuke TONOSAKI

import sys
import os
import shutil
import argparse
import csv

from strgen.config import Config
from strgen.localization import Localization
from strgen import google
from strgen import apple



# - - - - - - - - - - - - - - - - - - - -
# Constants, Enumeration
# - - - - - - - - - - - - - - - - - - - -
YAML_FILE_NAME = 'strgen.yml'



# - - - - - - - - - - - - - - - - - - - -
# Arguments
# - - - - - - - - - - - - - - - - - - - -
parser = argparse.ArgumentParser()
parser.add_argument('--config',
                        default=os.path.join(os.getcwd(), YAML_FILE_NAME),
                        type=str,
                        help='configuration yaml file path.')
args = parser.parse_args()



# - - - - - - - - - - - - - - - - - - - -
# Work
# - - - - - - - - - - - - - - - - - - - -
class Work:
    def __init__(self):
        self.config = Config()
        self.localization = Localization()

work = Work()



# - - - - - - - - - - - - - - - - - - - -
# Function - Initialize
# - - - - - - - - - - - - - - - - - - - -
def initialize():
    work.config.load(args.config)

    build_dir_initialize()
    
    work.localization.load(work.config.general_input_file_path)
    
    return



# - - - - - - - - - - - - - - - - - - - -
# Function - Build directory
# - - - - - - - - - - - - - - - - - - - -
def build_dir_initialize():
    path = work.config.path_output_build
    
    if os.path.isdir(path):
        shutil.rmtree(path)

    os.makedirs(path)

    return



# - - - - - - - - - - - - - - - - - - - -
# Function - Main
# - - - - - - - - - - - - - - - - - - - -
def main():
    initialize()

    if work.config.google_enabled:
        google.write(work.localization.localized_map,
            work.config.path_output_build_google,
            work.config.google_strings_file_name)
    
    
    if work.config.apple_enabled:
        apple.write(work.localization.localized_map,
            work.config.path_output_build_apple,
            work.config.apple_strings_file_name,
            work.config.apple_swift_file_name,
            work.config.apple_swift_class_name)


if __name__ == '__main__':
    main()
