#!/usr/bin/python
# coding: UTF-8

import sys
import os
import shutil
import enum


# - - - - - - - - - - - - - - - - - - - -
# Const, Enum
# - - - - - - - - - - - - - - - - - - - -
BUILD_DIR = 'build'

class Target(enum.Enum):
    google  = 1
    apple  = 2

TARGET_NAME = {
    Target.google: "google",
    Target.apple: "apple",
}



# - - - - - - - - - - - - - - - - - - - -
# Statics
# - - - - - - - - - - - - - - - - - - - -
csvFileObject = None

localizations = []  # ex. ['en-US', 'ja-JP', 'zh-Hans', 'zh-Hant']

stringsFileObjects = {
    Target.google: {},
    Target.apple: {},
}

swiftFileObject = None



# - - - - - - - - - - - - - - - - - - - -
# Function - Path
# - - - - - - - - - - - - - - - - - - - -
def path_csv():
    return sys.args[1]


def path_build_root():
    return sys.args[2]


def path_build():
    return os.path.join(build_path_root(), BUILD_DIR)



# - - - - - - - - - - - - - - - - - - - -
# Function - Initialize
# - - - - - - - - - - - - - - - - - - - -
def initialize():

    if not initialize_check_args():
        print('invalid args.')
        sys.exit()
    
    iinitialize_build_dir()

    return


def initialize_check_args():
    args = sys.argv
    if len(args) < 3:
        return False
    
    if not os.path.exists(csv_path()):
         return False
    
    if not os.path.isdir(build_path_root()):
        return False
        
    return True


def iinitialize_build_dir():
    if os.path.isdir(build_path()):
        shutil.rmtree(build_path())
        return
    
    os.makedirs(build_path())

    return



# - - - - - - - - - - - - - - - - - - - -
# Function - Header
# - - - - - - - - - - - - - - - - - - - -
def header_process():
    return


def header_process_enumerate_localize():
    return




# - - - - - - - - - - - - - - - - - - - -
# Function - Main
# - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    initialize()

