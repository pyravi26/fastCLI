import json, datetime
from os.path import isdir
from lib.helpers import gen_log_messages

class FileGenerator(object):

    def __init__(self) -> None:
        self._info  = None
        self._path  = None
        self._name  = None
        self._data  = None
        self._fandt = [
            {"fname": None, "template": None}
        ]

    def __update_config(self, filename: str):
        cname = str(self.__class__.__name__).lower()
        fname = filename.replace(self._info.get_source_path, '')
        data  = self.__get_data()
        data["other_files"][cname].append({
            "name": fname,
            "created": str(datetime.datetime.now(datetime.timezone.utc))
        })
        self._info.get_decoder.write_file(f"{self._info.get_source_path}/.fastcli.conf.json", json.dumps(data))

    def __get_data(self):
        if self._data is None:
            self._data = json.loads(self._info.get_decoder.read_file(f"{self._info.get_source_path}/.fastcli.conf.json"))
        
        return self._data
    
    def get_file_path(self, name: str) -> str:
        return self.__get_data()['file_dirs'][name]

    def load_file_path(self, name: str):
        self._path = self.get_file_path(name)

    def generate(self):
        __name = str(self._name[0]).upper() + self._name[1:]
        if isdir(self._path) is True:
            for t in self._fandt:
                self._info.get_decoder.write_file(
                    t["fname"], 
                    t["template"].render(
                        name=self._name, uc_name=__name, 
                        table_namespace=self._info.get_table_namespace, 
                        namespace=self.__get_data()["namespace"]
                    )
                )
                self.__update_config(t["fname"])
                gen_log_messages(t["fname"])