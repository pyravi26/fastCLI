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

- api
    - controllers
        - // controller files
    - routers
        - // route files
    - validators
        - // pydantic validator files
- PROJECT_DIRECTORY
    - database
        - db_coonection.py
    - models
        - // databse models define here
    - i18n_translations
    - lib
        - core
            - validators
                - base_validator.py
            - base_controller.py
            - helpers.py
- YOUR_NAMESPACE_api.py
- YOUR_NAMESPACE.sh


## Development Setup

### Prerequisites

- Python3.9+


### Setting Up a Project

Install the fCLI globally:

- Clone or Download fCLI form github.com

```
git clone https://github.com/pyravi26/fastCLI.git
```

- Go inside fCLI directory structure

```
cd fastCLI
```

- Run the following command

```
sudo ./setup.sh

```

This will setup the fCLI and verify the same, by showing/display the help topic/s.

- In order to create a workspace:

```
fastCLI gp --namespace=<PROJECT_NAMESPACE>
```
This will create the directory $HOME/Repos/YOUR_PROJECT_NAME. Inside this you can find **<PROJECT_NAMESPACE>.sh** file.

**ARGUMENTS**

* --namespace   Namespace of your project
* --output      Output Directory where your file will be generated


To run the application simple follow below instructions:

- Go inside your project directory by running following command:

```
cd $HOME/Repos/<PROJECT_NAME>
```

- In order to run **DOCKER Container**, you can run the following command:

```
./<PROJECT_NAMESPACE>.sh -d
```

- Without a Docker, i.e. run your project standlaone and you need to setup **Database** separately

    * Please setup your **Postgres** Database by following instructions at https://www.postgresql.org/download/

    * Before running your application you need to do some settings. In order to do settings, please go to your project directory i.e. **$HOME/Repos/YOUR_PROJECT_NAME** and open the file with name **<PROJECT_NAMESPACE>.sh**. 

    * In this file you have found multiple **export** command with **<YOUR_DATABASE_*>** tags. Please replace **<YOUR_DATABASE_*>** tags with appropriate value/s for it.

    ```
    export DB_NAME='<YOUR_DATABASE_NAME>'
    export DB_HOST='<YOUR_DATABASE_HOST>'
    export DB_PORT='<YOUR_DATABASE_PORT>'
    export DB_USER='<YOUR_DATABASE_USER_NAME>'
    export DB_PASS='<YOUR_DATABASE_PASSWORD>'
    ```

    * After this you can run your application by simply run the following command:

    ```
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

**ARGUMENTS**

* --module 
* --validator

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
