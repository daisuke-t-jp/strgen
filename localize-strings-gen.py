#!/usr/bin/python
# coding: UTF-8

import sys
import os
import shutil
import enum
import csv



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

    if not initialize_csv():
        print('csv file does not open.')
        sys.exit()

    return


def initialize_check_args():
    args = sys.argv
    if len(args) < 3:
        return False
    
    if not os.path.exists(path_csv()):
         return False
    
    if not os.path.isdir(path_build_root()):
        return False
        
    return True


def iinitialize_build_dir():
    if os.path.isdir(path_build()):
        shutil.rmtree(path_build())
    
    os.makedirs(path_build())

    return


def initialize_csv():
    if not os.path.isfile(path_csv()):
        return False
    
    try:
        with open(path_csv(), mode='r') as f:
            csvFileObject = f
    except Exception as e:
        return False
    
    return True



# - - - - - - - - - - - - - - - - - - - -
# Function - Header
# - - - - - - - - - - - - - - - - - - - -
def header_process():

    header_process_enumerate_localize()
    
    header_process_create_file()
    
    return


def header_process_enumerate_localize():
    
    csvReader = csv.reader(csvFileObject)
    header = csvReader.next()
    
    for col in header[1:]:
        localizations.append(col)

    return


def header_process_create_file():
    # TODO
    return



# - - - - - - - - - - - - - - - - - - - -
# Function - Main
# - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':
    initialize()

    header_process()
