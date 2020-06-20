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

NAME_GOOGLE = 'google'
NAME_APPLE = 'apple'


DIR_NAME_PREFIX_GOOGLE = 'values-'
DIR_NAME_SUFFIX_APPLE =  '.lproj'
DIR_NAME_LPROJ = 'lproj'
STRINGS_FILE_NAME_GOOGLE = 'strings.xml'
STRINGS_FILE_NAME_APPLE = 'Localizable.strings'
APPLE_SWIFT_FILE_NAME = 'LocalizableStrings.swift'



# - - - - - - - - - - - - - - - - - - - -
# Work
# - - - - - - - - - - - - - - - - - - - -
class Work:
    csv_file_object = None
    localizations = []  # ex. ['en-US', 'ja-JP', 'zh-Hans', 'zh-Hant']

    google_strings_file_map = {}
    apple_strings_file_map = {}
    apple_swift_file_object = None

work = Work()



# - - - - - - - - - - - - - - - - - - - -
# Function - Path
# - - - - - - - - - - - - - - - - - - - -
def path_csv():
    return sys.argv[1]


def path_build_root():
    return sys.argv[2]


def path_build():
    return os.path.join(path_build_root(), BUILD_DIR)


def path_build_google():
    return os.path.join(path_build(), NAME_GOOGLE)


def path_build_apple():
    return os.path.join(path_build(), NAME_APPLE)

def path_build_apple_strings():
    return os.path.join(path_build_apple(), DIR_NAME_LPROJ)



# - - - - - - - - - - - - - - - - - - - -
# Function - Initialize
# - - - - - - - - - - - - - - - - - - - -
def initialize():
    if not initialize_check_args():
        print('invalid args.')
        sys.exit()
    
    build_dir_initialize()

    if not csv_initialize():
        print('csv file does not open.')
        sys.exit()
        
    localize_initialize()
    
    google_initialize(work.localizations)
    
    apple_initialize(work.localizations)
    
    return


def initialize_check_args():
    if len(sys.argv) < 3:
        return False
    
    if not os.path.exists(path_csv()):
         return False
    
    if not os.path.isdir(path_build_root()):
        return False
        
    return True



# - - - - - - - - - - - - - - - - - - - -
# Function - Finalize
# - - - - - - - - - - - - - - - - - - - -
def finalize():
    
    csv_finalize()
    google_finalize()
    apple_finalize()
    
    return



# - - - - - - - - - - - - - - - - - - - -
# Function - Process
# - - - - - - - - - - - - - - - - - - - -
def process():

    reader = csv.reader(work.csv_file_object)
    header = next(reader)   # Skip header
    
    for row in reader:
        
        key = row[0]

        for i in range(1, len(row)):
            value = row[i]
            
            if len(value) == 0:
                continue
            
            code = work.localizations[i - 1]
            
            google_strings_append(code, key, value)
            apple_strings_append(code, key, value)

    return



# - - - - - - - - - - - - - - - - - - - -
# Function - Build directory
# - - - - - - - - - - - - - - - - - - - -
def build_dir_initialize():
    if os.path.isdir(path_build()):
        shutil.rmtree(path_build())

    os.makedirs(path_build())

    return



# - - - - - - - - - - - - - - - - - - - -
# Function - CSV
# - - - - - - - - - - - - - - - - - - - -
def csv_initialize():
    if not os.path.isfile(path_csv()):
        return False
    
    try:
        work.csv_file_object = open(path_csv(), mode='r')
    except Exception as e:
        return False
    
    return True


def csv_finalize():
    work.csv_file_object.close()
    work.csv_file_object = None
    
    return



# - - - - - - - - - - - - - - - - - - - -
# Function - Localize
# - - - - - - - - - - - - - - - - - - - -
def localize_initialize():

    # Enumerate localizations.
    reader = csv.reader(work.csv_file_object)
    header = next(reader)
    
    for col in header[1:]:
        work.localizations.append(col)
    
    return



# - - - - - - - - - - - - - - - - - - - -
# Function - Google
# - - - - - - - - - - - - - - - - - - - -
def google_initialize(localizations):

    text = '''\
<?xml version="1.0" encoding="utf-8"?>
<resources>
'''

    for elm in localizations:
        # Create dir.
        localize_dir = os.path.join(path_build_google(), DIR_NAME_PREFIX_GOOGLE + elm)
        os.makedirs(localize_dir)
        
        
        # Create file
        file_path = os.path.join(localize_dir, STRINGS_FILE_NAME_GOOGLE)
        
        work.google_strings_file_map[elm] = open(file_path, mode='w', encoding='utf-8')
        work.google_strings_file_map[elm].write(text)
    
    return


def google_finalize():

    text = '''\
</resources>
'''

    for key in work.google_strings_file_map.keys():
        elm = work.google_strings_file_map[key]
        
        elm.write(text)
        elm.close()
        
        work.google_strings_file_map[key] = None
    
    return


def google_strings_append(code, key, value):
    text = '    <string name=\"{0}\">{1}</string>\n'.format(key, value)
    
    work.google_strings_file_map[code].write(text)

    return



# - - - - - - - - - - - - - - - - - - - -
# Function - Apple
# - - - - - - - - - - - - - - - - - - - -
def apple_initialize(localizations):

    for elm in localizations:
        # Create dir.
        localize_dir = os.path.join(path_build_apple_strings(), elm + DIR_NAME_SUFFIX_APPLE)
        os.makedirs(localize_dir)


        # Create file
        file_path = os.path.join(localize_dir, STRINGS_FILE_NAME_APPLE)
        
        work.apple_strings_file_map[elm] = open(file_path, mode='w', encoding='utf-8')
    
    apple_swift_initialize()
    
    return


def apple_finalize():

    for key in work.apple_strings_file_map.keys():
        elm = work.apple_strings_file_map[key]
        
        elm.close()
        
        work.apple_strings_file_map[key] = None
        
    apple_swift_finalize()
    
    return


def apple_strings_append(code, key, value):
    text = '\"{0}\"=\"{1}\";\n'.format(key, value)
    
    work.apple_strings_file_map[code].write(text)

    apple_swift_append(key, value)

    return



# - - - - - - - - - - - - - - - - - - - -
# Function - Apple swift
# - - - - - - - - - - - - - - - - - - - -
def apple_swift_initialize():

    path = os.path.join(path_build_apple(), APPLE_SWIFT_FILE_NAME)

    work.apple_swift_file_object = open(path, mode='w', encoding='utf-8')

    text = '''\
import Foundation

class LocalizableStrings {

    enum Key: String {
'''

    work.apple_swift_file_object.write(text)
    
    return


def apple_swift_finalize():

    text = '''\
    }
    
}\
'''

    work.apple_swift_file_object.write(text)

    work.apple_swift_file_object.close()
    work.apple_swift_file_object = None
    
    return


def apple_swift_append(key, value):
    text = '        case {0} = \"{1}\"\n'.format(key, value)
    
    work.apple_swift_file_object.write(text)
    
    return



# - - - - - - - - - - - - - - - - - - - -
# Function - Main
# - - - - - - - - - - - - - - - - - - - -
if __name__ == '__main__':

    initialize()
    
    process()
    
    finalize()
