#!/usr/bin/env python
# Copyright 2020 Daisuke TONOSAKI

import os


# Constants, Enumeration
DIR_NAME_LPROJ = 'lproj'
DIR_NAME_SUFFIX = '.lproj'
SWIFT_PREFIX = '''\
import Foundation

class {class_name} {

    enum Key: String {
'''
SWIFT_SUFFIX = '''\
    }

}
'''


def write(localized_map: dict, output_path: str, strings_file_name: str, swift_file_name: str, swift_class_name: str):
    _write_strings_file(localized_map, output_path, strings_file_name)
    _write_swift_file(localized_map, output_path, swift_file_name, swift_class_name)


def _write_strings_file(localized_map: dict, output_path: str, strings_file_name: str):
    for code in localized_map.keys():
        # Create dir.
        dir = os.path.join(os.path.join(output_path, DIR_NAME_LPROJ), code + DIR_NAME_SUFFIX)
        os.makedirs(dir)
        
        
        # Create file
        file_path = os.path.join(dir, strings_file_name)
        
        try:
            with open(file_path, mode='w', encoding='utf-8') as file:
                for key, value in localized_map[code].items():
                    value_escaped = value.replace('"', '\\"')
                    
                    text = '\"{0}\"=\"{1}\";\n'.format(key, value_escaped)
                    
                    file.write(text)
            
        except Exception as e:
            raise e


def _write_swift_file(localized_map: dict, output_path: str, swift_file_name: str, swift_class_name: str):
    file_path = os.path.join(output_path, swift_file_name)
    append_keys = []
    
    try:
        with open(file_path, mode='w', encoding='utf-8') as file:
            prefix = SWIFT_PREFIX.replace('{class_name}', swift_class_name)
            file.write(prefix)
            
            for code in localized_map.keys():
                for key in localized_map[code].keys():
                    if key in append_keys:
                        continue
                    
                    append_keys.append(key)
                    
                    text = '        case {0}\n'.format(key)
                    
                    file.write(text)
                    
            file.write(SWIFT_SUFFIX)

    except Exception as e:
        raise e

