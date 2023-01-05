<p align="center">
    <a href="#"><img src="https://github.com/pyravi26/fastCLI/blob/main/logo_20230103.png?raw=true" alt="fastCLI" width="20%" /></a>
</p>

---

fCLI is a toolchain for FastAPI. It's basic purpose is to generate project, controllers, models, pydantic validators and routes. It support Python 3.9+ based on standard Python types, class and objects.

The key features are:

* **Easy**: It's easy to use just like <a href="https://github.com/angular/angular">Angular</a>. Designed to be easy to use and less coding time. 
* **Short**: Minimize code duplication. Multiple features from each parameter declaration. Fewer bugs.


---

## Directory Structure

YOUR_PROJECT_NAME_DIRECOTRY
- api
    - controllers
    - database
        - models
            - // databse models define here
        - validators
            - // pydantic models define here
        - db_coonection.py
    - i18n_translations
    - lib
        - core
            - validators
                - base_validator.py
            - base_controller.py
            - helpers.py
    - routers
- YOUR_NAMESPACE_api.py
- YOUR_NAMESPACE.sh


## Development Setup

### Prerequisites

- Python3.9+


### Setting Up a Project

Install the fCLI globally:

- Download fCLI form github.com
- Go inside fCLI directory structure

```
cd fastCLI
```

- Run the following command

```
./setup.sh $0

or

sh setup.sh $0
```

This will setup the fCLI and verify it by showing the help topic of this command.

- In order to create a workspace:

```
fastCLI gp <PROJECT_NAME> --namespace=<PROJECT_NAMESPACE>
```
This will create the directory $HOME/Repos/YOUR_PROJECT_NAME

- Before run application you need to do some settings. To do settings go to directory $HOME/Repos/YOUR_PROJECT_NAME and open file  <PROJECT_NAMESPACE>.sh. In this file you have found multiple **export** and **<YOUR_DATABASE_*>**. Please replace **<YOUR_DATABASE_*>** with appropriate value/s:

```
export DB_NAME='<YOUR_DATABASE_NAME>'
export DB_HOST='<YOUR_DATABASE_HOST>'
export DB_PORT='<YOUR_DATABASE_PORT>'
export DB_USER='<YOUR_DATABASE_USER_NAME>'
export DB_PASS='<YOUR_DATABASE_PASSWORD>'
```

- To run the application:

```
cd $HOME/Repos/<PROJECT_NAME>
./<PROJECT_NAMESPACE>.sh
```

### Create new Contorller

Run the following

```
fastCLI gc CONTROLLER_NAME [ARGUMENTS]

or 

fastCLI -controller CONTROLLER_NAME [ARGUMENTS]
```

**ARGUMENTS**

* --router 
* --module 
* --validator


### Create new Router

Run the following

```
fastCLI gr ROUTER_NAME [ARGUMENTS]

or 

fastCLI -router ROUTER_NAME [ARGUMENTS]
```


### Create new Module

Run the following

```
fastCLI gm MODULE_NAME [ARGUMENTS]

or 

fastCLI -module MODULE_NAME [ARGUMENTS]
```

**ARGUMENTS**

* --validator


### Create new Validator

Run the following

```
fastCLI gv VALIDATOR_NAME [ARGUMENTS]

or 

fastCLI -validator VALIDATOR_NAME [ARGUMENTS]
```


#### Argument Details

- To generate router pass argument --router or --router=True 
- To generate module pass argument --module or --module=True 
- To generate validator pass argument --validator or --validator=True 
