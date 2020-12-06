#!/usr/bin/env python
# Copyright 2020 Daisuke TONOSAKI

import os

from strgen import util


# Constants, Enumeration
DIR_NAME_PREFIX = 'values-'
FILE_PREFIX = '''\
<?xml version="1.0" encoding="utf-8"?>
<resources>
'''
FILE_SUFFIX = '''\
</resources>
'''

def write(localized_map: dict, output_path: str, file_name: str):
    for code in localized_map.keys():
        # Create dir.
        dir = os.path.join(output_path, DIR_NAME_PREFIX + code)
        os.makedirs(dir)
        
        
        # Create file
        file_path = os.path.join(dir, file_name)
        
        try:
            with open(file_path, mode='w', encoding='utf-8') as file:
                file.write(FILE_PREFIX)
                
                for key, value in localized_map[code].items():
                    value_escaped = util.xml_escape(value)
                    
                    text = '    <string name=\"{0}\">{1}</string>\n'.format(key, value_escaped)

                    file.write(text)
                
                file.write(FILE_SUFFIX)

        except Exception as e:
            raise e
