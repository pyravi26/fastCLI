import os
from lib.helpers import DataInfo, gen_log_messages
from mako.template import Template
from lib.generator import FileGenerator

class Models(FileGenerator):

    def __init__(self, info: DataInfo):
        super(Models, self).__init__()
        self._info  = info
        self._name  = info.get_params[0]
        self._path = f"{info.get_source_path}/api/database/models"
        self._args  = info.get_parse_args

        self._fandt = [
            {
                "fname": f"{self._path}/{self._name}_model.py",
                "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/models.txt"))
            }
        ]
    