# Bookmarks REST API
----------------------------------
REST API built using flask framework that used for managing bookmarks by individual users.

# API Consumers Note 
----------------------
This app is built using flask framework that helps this api can be cosumed both on andriod or web applications.

### API Endpoints
- POST 
    - user registration
    - bookmarks posting 
- GET 
    - user login
    - refresh token 
    - bookmarks
    - bookmark/{id}
    - bookmark/stats
    - bookmark/short_url
- PUT / PATCH 
    - bookmark/{id}
- DELETE 
    - bookmark/{id}

## Test Live API 
API have been configured and deployed using <a href="https://www.heroku.com/">Heroku.</a>

Test Live version by clicking <a href="https://bookmarks-api-rest.herokuapp.com/#/">here</a>.

### Documentation
Every Aspect of using this API is been documented using <a href="https://github.com/flasgger/flasgger">flasgger</a> which is a opensource flask extension for extracting open-api specifications which defaultly uses swagger UI to disply documentation 

## Configuring App with your Front-end
- You can refer the following files to confgure the app in your production 
```
src/config/swagger.py
src/__init__.py
```

- Currently there is no external DB used, in caseyou want to configure with any other db please do change the following env variable 
```
SQLALCHEMY_DB_URI = respective db url
```

- As there was no UI the folders templates and static are empty you can replace them with your own folders containing UI components and change the static-path in ```src/config/swagger.py```

- Currently no secret keys are configured, you can configure one during the time of deployment in your own way of choice else you can use the following commands in cmd to get random secret keys(suggested by flask).
```
import os
os.urandom(16)
```

# Developers Note 
-----
App do follow these specification 
```
- flask == 2.0+
- python == 3.7+
- flask-SQLAlchemy == 2.5+ 
```
please do follow these version specifications so that it will be ease for contributing.

## Installation Guide:
Please do clone this repo using following link or download zip.
- Clone here
    ```
    HTTPS: https://github.com/venkateshtantravahi/bookmarks-api.git
    SSH : git@github.com:venkateshtantravahi/bookmarks-api.git
    CLI: gh repo clone venkateshtantravahi/bookmarks-api
    ```
- <a href="https://github.com/venkateshtantravahi/bookmarks-api/archive/refs/heads/main.zip">Get Zip</a>

### Creating Envs
#### Using Pip
```
1. Install Virtual Environment using following command:
    pip install virtualenv
2. Open the terminal in the project directory and run:
    virtualenv env
3. run the following command to activate created venv
   .\env\Scripts\activate
4. Install the following dependencies by running:
   pip install -r requirements.txt
```

#### Using Conda
```
1. Create a new conda environment by following command:
   conda create -n <name of env>
2. Install pip in conda env by following command:
   conda install -c anaconda pip
3. Install the requirements by running:
   pip install -r requirements.txt
```

## Contribution 
Thanks that you got an eye on my repo, but before contributing please do refer the contribution guidelines <a href="https://github.com/venkateshtantravahi/bookmarks-api/contribution.md">here</a> ane make pull request to develop brach ```bm-deploy-app```.

## Issues or Bug Fixes
For anything that has some bug fix or if api consumers ran into some issues please do open a issue tagging he proper comment <a href="https://github.com/venkateshtantravahi/bookmarks-api/issues">here</a>.

## Big ShoutOut
I really appreciate :heart: both devs and consumers for trying out this api, if you do really like this work please do hit a :star: and :eye: