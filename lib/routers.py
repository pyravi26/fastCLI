from lib.helpers import DataInfo
from mako.template import Template
from lib.generator import FileGenerator

class Routers(FileGenerator):

    def __init__(self, info: DataInfo):
        super(Routers, self).__init__()
        self._info  = info
        self._name  = info.get_params[0]
        self._path = f"{info.get_source_path}/api/routers"

        self._fandt = [
            {
                "fname": f"{self._path}/{self._name}_router.py",
                "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/routers.txt"))
            }
        ]

