import os, subprocess, json
from datetime import datetime
from lib.helpers import DataInfo, run_help
from mako.template import Template
from platform import python_version

class Projects():
    def __init__(self, info: DataInfo):
        self.__info          = info
        self.__args          = info.get_parse_args
        self.__name          = '-'.join(info.get_params[0].replace(r"([@_!#$%^&*()<>?/\|}{~:])", '').split(' '))
        self.__root_path     = f"{info.get_home_dir}/{self.__name}"
        self.__config_path   = f"{self.__root_path}/.fastcli.conf.json"
        self.__required      = ['fastapi', 'pydantic', 'sqlalchemy', 'psycopg2', 'uvicorn']
        self.__project_info  = {
            "name": self.__name,
            "namespace": self.__args["namespace"],
            "root_dir": self.__root_path,
            "config_file": self.__config_path,
            "required": self.__required,
            "default_files": [],
            "other_files": {
                "controllers": [],
                "routers": [],
                "models": [],
                "validators": []
            },
            "generated_by": "FastCLI: Command Line Tool",
            "fastCLI_develop_by": "omrsmeh@gmail.com, rmwork.dev@gmail.com"
        }

        if os.path.isfile(self.__config_path) is True:
            raise Exception("Project is already exists. If you want to generate new Project, leave the current path and then retry")

        if self.__args['namespace'] is None or self.__args['namespace'].strip() == '':
            raise Exception("Please provide namespace.")

        self.__templates = {
            "shell": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/executer.txt")), 
            "main": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/source.txt")),
            "connection": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/connection.txt")),
            "helper": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/helper.txt")),
            "base_controller": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/controller.txt")),
            "base_validator": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/validator.txt")),
            "initilize_route": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/initilize_route.txt"))
        }
    

    def __get_version(self) -> str:
        version = python_version().split('.')
        version.pop()
        return ".".join(version)


    def __do_installation(self, output: str):
        sp_run_args = f"cd {output} && python{self.__get_version()} -m venv {self.__name}_env && source {self.__name}_env/bin/activate && pip install {' '.join(self.__required)}"
        p = subprocess.Popen(sp_run_args, shell=True)
        p.wait()


    def gen_projects(self):
        if self.__args["output"] is not None:
            path = f"{os.path.abspath(os.path.expanduser(self.__args['output']))}/{self.__name}"
            self.__project_info["root_dir"] = path
        else:
            path = self.__root_path
        
        if os.path.exists(path) is False:
            os.makedirs(path)

            '''
                Generate Directory Structure
            '''
            for s in self.__info.get_dir_structure:
                _path = f"{path}/{s['name']}"
                if s['parent'] is not None:
                    _path = f"{path}/{s['parent']}/{s['name']}"

                os.makedirs(_path)

            __files = [
                {"name": f"{path}/{self.__args['namespace']}.sh", "template": self.__templates["shell"]},
                {"name": f"{path}/{self.__args['namespace']}_api.py", "template": self.__templates["main"]},
                {"name": f"{path}/api/database/db_connection.py", "template": self.__templates["connection"]},
                {"name": f"{path}/api/lib/core/helpers.py", "template": self.__templates["helper"]},
                {"name": f"{path}/api/lib/core/base_controller.py", "template": self.__templates["base_controller"]},
                {"name": f"{path}/api/lib/core/validators/base_validator.py", "template": self.__templates["base_validator"]},
                {"name": f"{path}/api/routers/__init__.py", "template": self.__templates["initilize_route"]}
            ]

            for f in __files:
                self.__info.get_decoder.write_file(f['name'], f['template'].render(
                    namespace=self.__args['namespace'], name=self.__name, ex_path=path, uc_name='Base',
                    blank_space=''
                ))
                self.__project_info["default_files"].append({
                    "name": f['name'].replace(path, ''),
                    "created": str(datetime.utcnow())
                })
            
            self.__info.get_decoder.write_file(self.__config_path, json.dumps(self.__project_info))
            p = subprocess.Popen(f"cd {path} && chmod +x {self.__args['namespace']}.sh", shell=True)
            p.wait()

        print("\n\nStart Installation...\n\n")
        self.__do_installation(path)
        run_help(path, self.__args['namespace'])