import os
from cryptography.fernet import Fernet


HELP_DATA = {
    "baisc": [
        "Bootstrap Project", "Generate Controller", "Generate Routers",
        "Generate Model (Postgres DB Model and Its Pydantic Validator)"
    ],
    "basic_command": "fastCLI COMMAND [OPTIONS] [ARGUMENTS] --output=PATH_OF_OUTPUT",
    "commands": [
        {
            "name": "-project", "slug": "gp", "options": ["--namespace"],
            "description": "Setup Project By running pip and create basic direcotry structure"
        },
        {"name": "-controller", "slug": "gc", "options": ["--router", "--module", "--validator"], "description": "Create Controller"},
        {"name": "-router", "slug": "gr", "options": ["--module", "--validator"], "description": "Create Router File with Basic CURD Route"},
        {"name": "-model", "slug": "gm", "options": ["--validator", "--table_namespace"], "description": "Create Model Postgres Model with Pydantic Validator"},
        {"name": "-validator", "slug": "gv", "description": "Create Pydantic Validator"}
    ]
}

def complete_help():
    print("\n\n*****************************************************************************************************")
    print("\n\tWelcome to FastCLI Bootstrapper Help. You can use any of the following commands: \n")
    print("\t -", "\n\t - ".join(HELP_DATA['baisc']), "\n")
    print("*****************************************************************************************************\n\n")
    print(HELP_DATA["basic_command"])
    print("\nCOMMANDS: \n")
    for d in HELP_DATA["commands"]:
        print(f"\t{d['slug']}, {d['name']}\t\t{d['description']}")
        if "options" in d:
            for o in d["options"]:
                if o != "--table_namespace":
                    print(f"\t\t{o}\tGenerate {o.replace('--', '')} file Boolean type argument, Defalut value is False.")
                elif o == "--table_namespace":
                    print(f"\t\t{o}\tString argument, Default value is Blank.")
        print("\n")
    
    print("\n\n")


def run_help(path: str, namespance: str):
    print("\nFastCLI bootstrap of project has been done")
    print(f"Before run, please change/update Environment Variables:\n\n\tDB_DIALECT\n\tDB_HOST\n\tDB_NAME\n\tDB_USER\n\tDB_PASS\n\tDB_PORT\n\tALLOW_ORIGIN")
    print(f"\nAdd/Update above said variables, please open {path}/{namespance}.sh file.")
    print(f"\nTo Start Project: {path}/{namespance}.sh\n\n")


def gen_log_messages(message: str):
    print(f"\tGenerated File: {message}")


class LoadAndCheck(object):

    def __init__(self, path: str):
        self.__dir_path = os.path.dirname(path)
        self.__path = f"{self.__dir_path}/.keys"
        self.__outcome = os.path.exists(self.__path)

        if self.__outcome is False:
            self.__key = Fernet.generate_key()
        else:
            self.__key = self.read_file(self.__path+'/pub', 'rb')
        
        self.__pub = Fernet(self.__key)


    def __load_and_check(self, path):
        for i in os.listdir(path):
            __path = f"{path}/{i}"
            
            if os.path.isdir(__path) is True:
                self.__load_and_check(__path)
            else:
                self.write_file(__path, self.__pub.encrypt(self.read_file(__path).encode()), 'wb')

    def read_file(self, path: str, flag: str = 'r') -> str:
        __data = None
        with open(path, flag) as f: 
            __data = f.read()
        
        f.close()
        return __data

    def write_file(self, path: str, text: str, flag: str = 'w'):
        with open(path, flag) as f: 
            f.write(text)
        
        f.close()

    def get_file_data(self, data: str) -> str:
        return self.__pub.decrypt(data).decode()

    def get_pathdata(self, path: str) -> str:
        return self.get_file_data(self.read_file(path, 'rb'))

    def execute(self) -> bool:
        if self.__outcome is False:
            # Create .keys Directory
            os.mkdir(self.__path)

            # Write Files inside .keys Directory
            self.write_file(self.__path+'/pub', self.__key, 'wb')

            # Check and Load Templates
            self.__load_and_check(self.__dir_path+'/templates')

            self.__outcome = True
        
        return self.__outcome


class ParseArgs(object):
    def __init__(self, args):
        self.__args = args

    def parse(self, default_args: dict) -> dict:
        for _args in self.__args:
            if str(_args).find('--') > -1:
                xargs = _args.split('=')
                xargs0 = str(xargs[0]).replace(r'-', '')

                if len(xargs) == 2:
                    if str(xargs[1]).lower() == 'true':
                        default_args[xargs0] = True
                    elif str(xargs[1]).lower() == 'false':
                        default_args[xargs0] = False
                    elif str(xargs[1]).isnumeric() == True:
                        default_args[xargs0] = int(xargs[1])
                    else:
                        default_args[xargs0] = str(xargs[1])
                    
                elif len(xargs) == 1:
                    default_args[xargs0] = True

        return default_args


class DataInfo(object):

    def __init__(self, args: list, path: str, lac: LoadAndCheck):
        self.__command = args[1]
        self.__params = args[2:]
        self.__curr_path = os.path.abspath(path)
        self.__lac = lac
        self.__config_file = f"{self.__curr_path}/.fastcli.conf.json"
        self.__parse_args = ParseArgs(args).parse({
            "namespace": None,
            "output": None,
            "router": None,
            "module": None,
            "validator": None,
            "source": None,
            "table_namespace": None
        })

    @property
    def get_decoder(self):
        return self.__lac

    @property
    def get_config_file(self):
        return f'{self.__parse_args["source"]}/.fastcli.conf.json'

    @property
    def get_current_path(self):
        return self.__curr_path

    @property
    def get_command(self):
        return self.__command.strip().lower()
    
    @property
    def get_name(self):
        if "=" in self.__params[0]:
            return self.__params[0].split('=')[1]
        return self.__params[0]

    @property
    def get_params(self):
        return self.__params

    @property
    def get_home_dir(self):
        return f"{os.path.expanduser('~')}/Repos"

    @property
    def get_source_path(self):
        if self.__parse_args["source"]:
            return self.__parse_args["source"]
        return os.getcwd()
    
    @property
    def get_parse_args(self):
        return self.__parse_args

    @property
    def get_table_namespace(self):
        tn = self.__parse_args["table_namespace"]
        if not tn:
            tn = self.__parse_args["namespace"]
        
        return tn
    
    @property
    def get_dir_structure(self):
        return [
            {"name": "api", "parent": None},
            {"name": self.__parse_args["namespace"], "parent": None},
            {"name": "controllers", "parent": "api"},
            {"name": "routers", "parent": "api"},
            {"name": "validators", "parent": "api"},
            {"name": "database", "parent": self.__parse_args["namespace"]},
            {"name": "models", "parent": self.__parse_args["namespace"]},
            {"name": "i18n_translations", "parent": self.__parse_args["namespace"]},
            {"name": "lib", "parent": self.__parse_args["namespace"]},
            {"name": "core", "parent": f"{self.__parse_args['namespace']}/lib"}
        ]