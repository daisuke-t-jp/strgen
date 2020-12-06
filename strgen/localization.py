#!/usr/bin/env python
# Copyright 2020 Daisuke TONOSAKI

import os
import csv

class Localization:
    def __init__(self):
        self._localized_map = {}
    
    
    def load(self, path: str):
        try:
            with open(path, mode='r') as file:
                # Enumerate codes.
                reader = csv.reader(file)
                header = next(reader)
                
                codes = []
                for code in header[1:]:
                    codes.append(code)
                    self._localized_map[code] = {}
                
                # Enumerate key and string.
                for row in reader:
                    key = row[0]
                                        
                    for i in range(1, len(row)):
                        code = codes[i - 1]
                        value = row[i]
                        
                        if len(value) == 0:
                            continue
                        
                        self._localized_map[code][key] = value

        except FileNotFoundError as e:
            raise e


    @property
    def localized_map(self) -> dict:
        return self._localized_map
