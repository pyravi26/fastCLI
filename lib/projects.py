import os, subprocess, json, re
from datetime import datetime, timezone
from lib.helpers import DataInfo, run_help
from mako.template import Template
from platform import python_version

class Projects():
    def __init__(self, info: DataInfo):
        self.__info          = info
        self.__args          = info.get_parse_args
        self.__name          = '-'.join(re.sub(r"[@_!#$%^&*()<>?/\|}{~:;`'\"]", "", info.get_name).split(' '))
        self.__root_path     = f"{info.get_home_dir}/{self.__name}"
        self.__config_path   = f"{self.__root_path}/.fastcli.conf.json"
        self.__required      = ['fastapi', 'pydantic', 'sqlalchemy', 'psycopg2-binary', 'uvicorn']
        self.__project_info  = {
            "name": self.__name,
            "namespace": self.__args["namespace"],
            "root_dir": self.__root_path,
            "config_file": self.__config_path,
            "file_dirs": {},
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

        self.__project_files = {
            "setup": [
                {"name": f"{self.__args['namespace']}.sh", "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/executer.txt"))},
                {"name": f"{self.__args['namespace']}_api.py", "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/source.txt"))},
                {"name": "requirements.txt", "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/requirements.txt"))},
                {"name": "Dockerfile", "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/dockerfile.txt"))},
                {"name": "docker-compose.yml", "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/dockercompose.txt"))},
            ],
            "database": {"name": "db_connection.py", "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/connection.txt"))},
            "models": {"name": "__init__.py", "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/initilize_route.txt"))},
            "core": [
                {"name": "helpers.py", "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/helper.txt"))},
                {"name": "base_controller.py", "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/controller.txt"))}
            ],
            "validators": {"name": "base_validator.py", "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/validator.txt"))},
            "routers": {"name": f"__init__.py", "template": Template(info.get_decoder.get_pathdata(f"{info.get_current_path}/templates/_gp/initilize_route.txt"))},
        }
    

    def __get_version(self) -> str:
        version = python_version().split('.')
        version.pop()
        return ".".join(version)


    def __do_installation(self, output: str):
        sp_run_args = f"cd {output} && python{self.__get_version()} -m venv {self.__name}_env && . {self.__name}_env/bin/activate && pip install {' '.join(self.__required)}"
        p = subprocess.Popen(sp_run_args, shell=True)
        p.wait()

    
    def __get_project_files(self, path: str) -> list:
        __files = []
        for pf in self.__project_files["setup"]:
            pf["name"] = f"{path}/{pf['name']}"
        
        for pf in self.__project_files:
            if isinstance(self.__project_files[pf], list):
                __files.extend(self.__project_files[pf])
            else:
                __files.append(self.__project_files[pf])
        
        return __files


    def gen_projects(self):
        if self.__args["output"] is not None:
            path = f"{os.path.abspath(os.path.expanduser(self.__args['output']))}/{self.__name}"
            self.__project_info["root_dir"] = path
            self.__config_path = f"{path}/.fastcli.conf.json"
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

                self.__project_info['file_dirs'][s['name']] = _path
                if s['name'] in self.__project_files:
                    if isinstance(self.__project_files[s['name']], list):
                        for f in self.__project_files[s['name']]:
                            f['name'] = f"{_path}/{f['name']}"
                    else:
                        self.__project_files[s['name']]['name'] = f"{_path}/{self.__project_files[s['name']]['name']}"

                os.makedirs(_path, exist_ok=True)
            
            project_files = self.__get_project_files(path)
            for f in project_files:
                self.__info.get_decoder.write_file(f['name'], f['template'].render(
                    namespace=self.__args['namespace'], name=self.__name, ex_path=path, uc_name='Base',
                    blank_space=''
                ))
                self.__project_info["default_files"].append({
                    "name": f['name'].replace(path, ''),
                    "created": str(datetime.now(timezone.utc))
                })
            
            self.__info.get_decoder.write_file(self.__config_path, json.dumps(self.__project_info))
            p = subprocess.Popen(f"cd {path} && chmod +x {self.__args['namespace']}.sh", shell=True)
            p.wait()

        print("\n\nStart Installation...\n\n")
        self.__do_installation(path)
        run_help(path, self.__args['namespace'])