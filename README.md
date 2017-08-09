# How to run this project?

### 1. Clone the project

    git clone https://github.com/lyk2017-django/TaleTellers.git

### 2. Create a virtual enviroment in the project directory

    cd TaleTellers
    python3 -m venv .venv

### 3. Activate the virtual enviroment

    source .venv/bin/activate

### 4. Install the requirements

    (.venv) pip install -r requirements.txt

### 5. Create migrations and runserver with manage.py
    
    (.venv) cd taletellers
    (.venv) python3 manage.py migrate
    (.venv) python3 manage.py runserver
    
# Notes 

### 1. How to deactivate the virtual enviroment?

    (.venv) deactivate

### 2. How to see the SQL queries of the migrations?

    (.venv) ./manage.py sqlmigrate <app_name> <migration_number>
    (.venv) ./manage.py sqlmigrate storyboard 0001
