import os
from lib.helpers import DataInfo, gen_log_messages
from mako.template import Template
from lib.generator import FileGenerator

class Models(FileGenerator):

    def __init__(self, info: DataInfo):
        super(Models, self).__init__()
        self._info  = info
        self._args  = info.get_parse_args
        __generate_validator = False

        for p in info.get_params:
            if p.lower().find('--') == -1:
                self._name = p
            elif p.lower() == '--validator':
                __generate_validator = True
        
        if not self._name:
            raise Exception('Please provide model name')

        self.load_file_path("models")
        self._fandt = [
            {
                "fname": f"{self._path}/{self._name}_model.py",
                "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/models.txt"))
            }
        ]

        if __generate_validator:
            self._fandt.append({
                "fname": f"{self.get_file_path('validators')}/{self._name}_validator.py",
                "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/validators.txt"))
            })
    