#!/usr/bin/python
# coding: UTF-8

import sys
import os
import shutil
import csv

import yaml



# - - - - - - - - - - - - - - - - - - - -
# Const, Enum
# - - - - - - - - - - - - - - - - - - - -
BUILD_DIR = 'build'

NAME_GOOGLE = 'google'
NAME_APPLE = 'apple'

KEY_RESULT = 'result'
KEY_MESSAGE = 'message'

DIR_NAME_PREFIX_GOOGLE = 'values-'
DIR_NAME_SUFFIX_APPLE =  '.lproj'
DIR_NAME_LPROJ = 'lproj'

YAML_FILE_NAME = 'strgen.yml'
YAML_KEY_INPUT_FILE_PATH = 'input_file_path'
YAML_KEY_OUTPUT_PATH = 'output_path'
YAML_KEY_STRINGS_FILE_NAME = 'strings_file_name'
YAML_KEY_GENERAL = 'general'
YAML_KEY_GOOGLE = 'google'
YAML_KEY_APPLE = 'apple'
YAML_KEY_APPLE_SWIFT_FILE_NAME = 'swift_file_name'
YAML_KEY_APPLE_SWIFT_CLASS_NAME = 'swift_class_name'

DEFAULT_STRINGS_FILE_NAME_GOOGLE = 'strings.xml'
DEFAULT_STRINGS_FILE_NAME_APPLE = 'Localizable.strings'
DEFAULT_APPLE_SWIFT_FILE_NAME = 'LocalizableStrings.swift'
DEFAULT_APPLE_SWIFT_CLASS_NAME = 'LocalizableStrings'



# - - - - - - - - - - - - - - - - - - - -
# Work
# - - - - - - - - - - - - - - - - - - - -
class Work:
    csv_file_object = None
    localizations = []  # ex. ['en-US', 'ja-JP', 'zh-Hans', 'zh-Hant']

    google_strings_file_map = {}
    apple_strings_file_map = {}
    apple_swift_file_object = None

    config_general_input_file_path = None
    config_general_output_path = None
    config_google_strings_file_name = None
    config_apple_strings_file_name = None
    config_apple_swift_file_name = None
    config_apple_swift_class_name = None

work = Work()



# - - - - - - - - - - - - - - - - - - - -
# Function - Initialize
# - - - - - - - - - - - - - - - - - - - -
def initialize():

    config_result = config_initialize()
    
    if not config_result[KEY_RESULT]:
        print(config_result[KEY_MESSAGE])
        sys.exit()
    
    build_dir_initialize()
    
    if not csv_initialize():
        print('csv file does not open.')
        sys.exit()
        
    localize_initialize()
    google_initialize(work.localizations)
    apple_initialize(work.localizations)
    
    return



# - - - - - - - - - - - - - - - - - - - -
# Function - Config(YAML)
# - - - - - - - - - - - - - - - - - - - -
def config_initialize():
    
    # Load file
    path = os.path.join(os.getcwd(), YAML_FILE_NAME)
    
    if len(sys.argv) > 1:
        path = sys.argv[1]
    
    try:
        file = open(path, 'r')
    except Exception as e:
        return {KEY_RESULT: False,
                KEY_MESSAGE: 'config file does not open.'}
    
    
    # Get configuration
    config = yaml.load(stream=file, Loader=yaml.SafeLoader)
    
    
    # Get general
    general = config.get(YAML_KEY_GENERAL)
    if general is None:
        return {KEY_RESULT: False,
                KEY_MESSAGE: 'config file does not have \'general\'.'}
    
    # Input file path
    work.config_general_input_file_path = general.get(YAML_KEY_INPUT_FILE_PATH)
    if work.config_general_input_file_path is None:
        return {KEY_RESULT: False,
                KEY_MESSAGE: 'config file does not have \'input_file_path\'.'}
    
    # Output path
    work.config_general_output_path = general.get(YAML_KEY_OUTPUT_PATH)
    if work.config_general_output_path is None:
        work.config_general_output_path = os.getcwd()
    
    
    # Get google
    google = config.get(YAML_KEY_GOOGLE)
    if google is None:
        return {KEY_RESULT: False,
                KEY_MESSAGE: 'config file does not have \'google\'.'}
    
    # Google strings file name
    work.config_google_strings_file_name = google.get(YAML_KEY_STRINGS_FILE_NAME)
    if work.config_google_strings_file_name is None:
        work.config_google_strings_file_name = DEFAULT_STRINGS_FILE_NAME_GOOGLE
    
    
    # Get apple
    apple = config.get(YAML_KEY_APPLE)
    if apple is None:
        return {KEY_RESULT: False,
                KEY_MESSAGE: 'config file does not have \'apple\'.'}
    
    # Apple strings file name
    work.config_apple_strings_file_name = apple.get(YAML_KEY_STRINGS_FILE_NAME)
    if work.config_apple_strings_file_name is None:
        work.config_apple_strings_file_name = DEFAULT_STRINGS_FILE_NAME_APPLE
    
    # Apple swift file name
    work.config_apple_swift_file_name = apple.get(YAML_KEY_APPLE_SWIFT_FILE_NAME)
    if work.config_apple_swift_file_name is None:
        work.config_apple_swift_file_name = DEFAULT_APPLE_SWIFT_FILE_NAME
    
    # Apple swift class name
    work.config_apple_swift_class_name = apple.get(YAML_KEY_APPLE_SWIFT_CLASS_NAME)
    if work.config_apple_swift_class_name is None:
        work.config_apple_swift_class_name = DEFAULT_APPLE_SWIFT_CLASS_NAME
    
    
    file.close()
    
    return {KEY_RESULT: True}


def config_finalize():
    # NOP
    return


def config_path_output_build():
    return os.path.join(work.config_general_output_path, BUILD_DIR)


def config_path_output_build_google():
    return os.path.join(config_path_output_build(), NAME_GOOGLE)


def config_path_output_build_apple():
    return os.path.join(config_path_output_build(), NAME_APPLE)


def config_path_output_build_apple_strings():
    return os.path.join(config_path_output_build_apple(), DIR_NAME_LPROJ)



# - - - - - - - - - - - - - - - - - - - -
# Function - Finalize
# - - - - - - - - - - - - - - - - - - - -
def finalize():
    
    config_finalize()
    csv_finalize()
    google_finalize()
    apple_finalize()
    
    return



# - - - - - - - - - - - - - - - - - - - -
# Function - Process
# - - - - - - - - - - - - - - - - - - - -
def process():

    reader = csv.reader(work.csv_file_object)
    
    for row in reader:
        
        key = row[0]
        appended_swift_file = False
        
        for i in range(1, len(row)):
            value = row[i]
            
            if len(value) == 0:
                continue
            
            code = work.localizations[i - 1]
            
            
            # Append to strings file
            google_strings_append(code, key, value)
            apple_strings_append(code, key, value)
            
            
            # Append to swift file
            if appended_swift_file:
                continue
            
            appended_swift_file = True
            apple_swift_append(key)

    return



# - - - - - - - - - - - - - - - - - - - -
# Function - Build directory
# - - - - - - - - - - - - - - - - - - - -
def build_dir_initialize():
    path = config_path_output_build()
    
    if os.path.isdir(path):
        shutil.rmtree(path)

    os.makedirs(path)

    return



# - - - - - - - - - - - - - - - - - - - -
# Function - CSV
# - - - - - - - - - - - - - - - - - - - -
def csv_initialize():
    if not os.path.isfile(work.config_general_input_file_path):
        return False
    
    try:
        work.csv_file_object = open(work.config_general_input_file_path, mode='r')
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
        localize_dir = os.path.join(config_path_output_build_google(), DIR_NAME_PREFIX_GOOGLE + elm)
        os.makedirs(localize_dir)
        
        
        # Create file
        file_path = os.path.join(localize_dir, work.config_google_strings_file_name)
        
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
    value_escaped = value
    value_escaped = value_escaped.replace('\'', "\\'")
    value_escaped = value_escaped.replace('"', '\\"')
    value_escaped = value_escaped.replace('&', '&amp;')
    value_escaped = value_escaped.replace('<', '&lt;')
    value_escaped = value_escaped.replace('>', '&gt;')
    value_escaped = value_escaped.replace('@', '\\@')
    value_escaped = value_escaped.replace('?', '\\?')

    text = '    <string name=\"{0}\">{1}</string>\n'.format(key, value_escaped)
    
    work.google_strings_file_map[code].write(text)

    return



# - - - - - - - - - - - - - - - - - - - -
# Function - Apple
# - - - - - - - - - - - - - - - - - - - -
def apple_initialize(localizations):

    for elm in localizations:
        # Create dir.
        localize_dir = os.path.join(config_path_output_build_apple_strings(), elm + DIR_NAME_SUFFIX_APPLE)
        os.makedirs(localize_dir)


        # Create file
        file_path = os.path.join(localize_dir, work.config_apple_strings_file_name)
        
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
    value_escaped = value.replace('"', '\\"')
    
    text = '\"{0}\"=\"{1}\";\n'.format(key, value_escaped)
    
    work.apple_strings_file_map[code].write(text)

    return



# - - - - - - - - - - - - - - - - - - - -
# Function - Apple swift
# - - - - - - - - - - - - - - - - - - - -
def apple_swift_initialize():

    path = os.path.join(config_path_output_build_apple(), work.config_apple_swift_file_name)

    work.apple_swift_file_object = open(path, mode='w', encoding='utf-8')

    text = '''\
import Foundation

class {class_name} {

    enum Key: String {
'''
    text = text.replace('{class_name}', work.config_apple_swift_class_name)
    
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


def apple_swift_append(key):
    text = '        case {0} = \"{1}\"\n'.format(key, key)
    
    work.apple_swift_file_object.write(text)
    
    return



# - - - - - - - - - - - - - - - - - - - -
# Function - Main
# - - - - - - - - - - - - - - - - - - - -
def main():
    initialize()
    process()
    finalize()


if __name__ == '__main__':
    main()
