################################################################################
# Author:      Finn Buchrieser
# MatNr:       11846398
# File:        config_reader.py
# Description: ... short description of the file ...
# Comments:    ... comments for the tutors ...
#              ... can be multiline ...
################################################################################

import json

class ConfigReader:
    def read_json_config(config_file):
        with open(config_file) as config_dict:
            config_dict = json.load(config_dict)
        return config_dict

