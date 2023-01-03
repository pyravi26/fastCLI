from os.path import isdir
from lib.helpers import DataInfo, gen_log_messages
from mako.template import Template
from lib.generator import FileGenerator

class Controllers(FileGenerator):

    def __init__(self, info: DataInfo):
        super(Controllers, self).__init__()
        self._info = info
        self._name = info.get_params[0]
        self._path = f"{self._info.get_source_path}/api/controllers"
        self._args = info.get_parse_args

        self._fandt = [
            {
                "fname": f"{self._path}/{self._name}_controller.py",
                "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/controllers.txt"))
            }
        ]

        