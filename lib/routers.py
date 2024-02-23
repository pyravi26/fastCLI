from lib.helpers import DataInfo
from mako.template import Template
from lib.generator import FileGenerator

class Routers(FileGenerator):

    def __init__(self, info: DataInfo):
        super(Routers, self).__init__()
        self._info  = info
        __generate_validator = False
        __generate_module = False

        for p in info.get_params:
            if p.lower().find('--') == -1:
                self._name = p
            elif p.lower() == '--validator':
                __generate_validator = True
            elif p.lower() == '--module':
                __generate_module = True

        self.load_file_path("routers")
        self._fandt = [
            {
                "fname": f"{self._path}/{self._name}_router.py",
                "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/routers.txt"))
            }
        ]
        if __generate_module:
            self._fandt.append({
                "fname": f"{self.get_file_path('models')}/{self._name}_model.py",
                "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/models.txt"))
            })
        if __generate_validator:
            self._fandt.append({
                "fname": f"{self.get_file_path('validators')}/{self._name}_validator.py",
                "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/validators.txt"))
            })

