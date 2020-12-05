#!/usr/bin/env python
# Copyright 2020 Daisuke TONOSAKI

import os

import yaml

class Config:

    # Constants, Enumeration
    BUILD_DIR = 'build'
    
    NAME_GOOGLE = 'google'
    NAME_APPLE = 'apple'
    
    YAML_KEY_GENERAL = 'general'
    YAML_KEY_INPUT_FILE_PATH = 'input_file_path'
    YAML_KEY_OUTPUT_PATH = 'output_path'
    YAML_KEY_ENABLED = 'enabled'

    YAML_KEY_GOOGLE = 'google'
    YAML_KEY_STRINGS_FILE_NAME = 'strings_file_name'

    YAML_KEY_APPLE = 'apple'
    YAML_KEY_APPLE_SWIFT_FILE_NAME = 'swift_file_name'
    YAML_KEY_APPLE_SWIFT_CLASS_NAME = 'swift_class_name'

    DEFAULT_STRINGS_FILE_NAME_GOOGLE = 'strings.xml'
    DEFAULT_STRINGS_FILE_NAME_APPLE = 'Localizable.strings'
    DEFAULT_APPLE_SWIFT_FILE_NAME = 'LocalizableStrings.swift'
    DEFAULT_APPLE_SWIFT_CLASS_NAME = 'LocalizableStrings'

    DIR_NAME_LPROJ = 'lproj'


    def __init__(self):
        self.general_input_file_path = None
        self.general_output_path = None
        
        self.google_enabled = True
        self.google_strings_file_name = self.DEFAULT_STRINGS_FILE_NAME_GOOGLE
        
        self.apple_enabled = True
        self.apple_strings_file_name = self.DEFAULT_STRINGS_FILE_NAME_APPLE
        self.apple_swift_file_name = self.DEFAULT_APPLE_SWIFT_FILE_NAME
        self.apple_swift_class_name = self.DEFAULT_APPLE_SWIFT_CLASS_NAME


    def load(self, path: str):
        # Load configuration
        try:
            with open(path, mode='r') as file:
                yaml_data = yaml.safe_load(stream=file)
                
                self._load_general(path, yaml_data)
                self._load_google(yaml_data)
                self._load_apple(yaml_data)

        except Exception as e:
            print("Can't open file {0}".format(path))
            return
        

    def _load_general(self, path: str, yaml_data: dict):
        data = yaml_data.get(self.YAML_KEY_GENERAL)
        if data is None:
            return
        
        
        # Input file path
        self.general_input_file_path = data.get(self.YAML_KEY_INPUT_FILE_PATH)
        if self.general_input_file_path is None:
            return
        
        if not os.path.isabs(self.general_input_file_path):
            # For relative path, use config file path.
            self.general_input_file_path = os.path.join(os.path.dirname(path), self.general_input_file_path)
        
        
        # Output path
        self.general_output_path = data.get(self.YAML_KEY_OUTPUT_PATH) or os.path.dirname(path)
        
        if not os.path.isabs(self.general_output_path):
            # For relative path, use config file path.
            self.general_output_path = os.path.join(os.path.dirname(path), self.general_output_path)


    def _load_google(self, yaml_data: dict):
        data = yaml_data.get(self.YAML_KEY_GOOGLE)
        if data is None:
            return
        
        self.google_enabled = data.get(self.YAML_KEY_ENABLED) or True
        self.google_strings_file_name = data.get(self.YAML_KEY_STRINGS_FILE_NAME) or self.DEFAULT_STRINGS_FILE_NAME_GOOGLE


    def _load_apple(self, yaml_data: dict):
        data = yaml_data.get(self.YAML_KEY_APPLE)
        if data is None:
            return
        
        self.apple_enabled = data.get(self.YAML_KEY_ENABLED) or True
        self.apple_strings_file_name = data.get(self.YAML_KEY_STRINGS_FILE_NAME) or self.DEFAULT_STRINGS_FILE_NAME_APPLE
        self.apple_swift_file_name = data.get(self.YAML_KEY_APPLE_SWIFT_FILE_NAME) or self.DEFAULT_APPLE_SWIFT_FILE_NAME
        self.apple_swift_class_name = data.get(self.YAML_KEY_APPLE_SWIFT_CLASS_NAME) or self.DEFAULT_APPLE_SWIFT_CLASS_NAME


    def path_output_build(self) -> str:
        return os.path.join(self.general_output_path, self.BUILD_DIR)

    def path_output_build_google(self) -> str:
        return os.path.join(self.path_output_build(), self.NAME_GOOGLE)

    def path_output_build_apple(self) -> str:
        return os.path.join(self.path_output_build(), self.NAME_APPLE)

    def path_output_build_apple_strings(self) -> str:
        return os.path.join(self.path_output_build_apple(), self.DIR_NAME_LPROJ)
