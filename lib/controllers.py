from os.path import isdir
from lib.helpers import DataInfo, gen_log_messages
from mako.template import Template
from lib.generator import FileGenerator

class Controllers(FileGenerator):

    def __init__(self, info: DataInfo):
        super(Controllers, self).__init__()
        self._info = info
        self._args = info.get_parse_args
        __generate_router = False
        __generate_module = False
        __generate_validator = False

        for p in info.get_params:
            if p.lower().find('--') == -1:
                self._name = p
            elif p.lower() == '--validator':
                __generate_validator = True
            elif p.lower() == '--module':
                __generate_module = True
            elif p.lower() == '--router':
                __generate_router = True
        
        if not self._name:
            raise Exception('Please provide controller name')

        self.load_file_path("controllers")
        self._fandt = [
            {
                "fname": f"{self._path}/{self._name}_controller.py",
                "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/controllers.txt"))
            }
        ]
        if __generate_validator:
            self._fandt.append({
                "fname": f"{self.get_file_path('validators')}/{self._name}_validator.py",
                "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/validators.txt"))
            })
        if __generate_module:
            self._fandt.append({
                "fname": f"{self.get_file_path('models')}/{self._name}_model.py",
                "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/models.txt"))
            })
        if __generate_router:
            self._fandt.append({
                "fname": f"{self.get_file_path('routers')}/{self._name}_router.py",
                "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/routers.txt"))
            })

        