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


    def __init__(self):
        self._general_input_file_path = None
        self._general_output_path = None
        
        self._google_enabled = True
        self._google_strings_file_name = self.DEFAULT_STRINGS_FILE_NAME_GOOGLE
        
        self._apple_enabled = True
        self._apple_strings_file_name = self.DEFAULT_STRINGS_FILE_NAME_APPLE
        self._apple_swift_file_name = self.DEFAULT_APPLE_SWIFT_FILE_NAME
        self._apple_swift_class_name = self.DEFAULT_APPLE_SWIFT_CLASS_NAME


    def load(self, path: str):
        # Load configuration
        yaml_data = {}
        
        try:
            with open(path, mode='r') as file:
                yaml_data = yaml.safe_load(stream=file)
        except FileNotFoundError as e:
            raise e
        
        
        self._load_general(path, yaml_data)
        self._load_google(yaml_data)
        self._load_apple(yaml_data)


    def _load_general(self, path: str, yaml_data: dict):
        data = yaml_data.get(self.YAML_KEY_GENERAL)
        if data is None:
            raise KeyError('\'general\' key no found in config file.')
        
        
        # Input file path
        self._general_input_file_path = data.get(self.YAML_KEY_INPUT_FILE_PATH)
        if self._general_input_file_path is None:
            raise KeyError('\'general\'[\'input_file_path\'] key no found in config file.')

        if not os.path.isabs(self._general_input_file_path):
            # For relative path, use config file path.
            self._general_input_file_path = os.path.join(os.path.dirname(path), self._general_input_file_path)
        
        
        # Output path
        self._general_output_path = data.get(self.YAML_KEY_OUTPUT_PATH) or os.path.dirname(path)
        if not os.path.isabs(self._general_output_path):
            # For relative path, use config file path.
            self._general_output_path = os.path.join(os.path.dirname(path), self._general_output_path)


    def _load_google(self, yaml_data: dict):
        data = yaml_data.get(self.YAML_KEY_GOOGLE)
        if data is None:
            return
        
        self._google_enabled = data.get(self.YAML_KEY_ENABLED) or True
        self._google_strings_file_name = data.get(self.YAML_KEY_STRINGS_FILE_NAME) or self.DEFAULT_STRINGS_FILE_NAME_GOOGLE


    def _load_apple(self, yaml_data: dict):
        data = yaml_data.get(self.YAML_KEY_APPLE)
        if data is None:
            return
        
        self._apple_enabled = data.get(self.YAML_KEY_ENABLED) or True
        self._apple_strings_file_name = data.get(self.YAML_KEY_STRINGS_FILE_NAME) or self.DEFAULT_STRINGS_FILE_NAME_APPLE
        self._apple_swift_file_name = data.get(self.YAML_KEY_APPLE_SWIFT_FILE_NAME) or self.DEFAULT_APPLE_SWIFT_FILE_NAME
        self._apple_swift_class_name = data.get(self.YAML_KEY_APPLE_SWIFT_CLASS_NAME) or self.DEFAULT_APPLE_SWIFT_CLASS_NAME


    @property
    def general_input_file_path(self) -> str:
        return self._general_input_file_path


    @property
    def google_enabled(self) -> bool:
        return self._google_enabled


    @property
    def google_strings_file_name(self) -> str:
        return self._google_strings_file_name


    @property
    def apple_enabled(self) -> bool:
        return self._apple_enabled


    @property
    def apple_strings_file_name(self) -> str:
        return self._apple_strings_file_name


    @property
    def apple_swift_file_name(self) -> str:
        return self._apple_swift_file_name


    @property
    def apple_swift_class_name(self) -> str:
        return self._apple_swift_class_name


    @property
    def path_output_build(self) -> str:
        return os.path.join(self._general_output_path, self.BUILD_DIR)


    @property
    def path_output_build_google(self) -> str:
        return os.path.join(self.path_output_build, self.NAME_GOOGLE)


    @property
    def path_output_build_apple(self) -> str:
        return os.path.join(self.path_output_build, self.NAME_APPLE)
