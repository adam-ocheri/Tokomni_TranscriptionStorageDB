# DJANGO APP 101 - SETUP

## How-to Use This Project
#### 

## Install Library
#### Create new environment:
**$     python -m venv env**
#### Activate the environment:
**$     source env/Scripts/activate**
#### Download and install via pip:
**$     pip install django**
#### Additionaly, if you want to install postgres:
**$     pip install psycopg2**

## Create Project
#### Create new django project:
**$     django-admin startproject `new-project-name`**

## Create App
#### Create new django app:
**$     cd `new-project-name` && python manage.py startapp `new-app-name`**

## Add App to Installation
#### Once our new django app has been created, we will need to link it:
**We will need to navigate to the django-generated `settings.py` file, and add our new app's name into the `INSTALLED_APPS` array**

## Run App
#### Once our setup is complete, we can run our app like so:
**$     python manage.py runserver**

## Using Templates (Dynamic Web Pages)
#### In the django app directory, create a new folder directory called 'templates' to store `.html` files. There are 2 approaches for this:
##### Approach 1:
1. For each template you want to create, create a folder for it
2. Within the page's folder, create the html file for the template - for example, `templates/auth/index.html`

##### Approach 2:
1. Create a reusable page that uses the JINJA engine to modify html-component-blocks dynamically
2. Create a "component" like page, that `extends` the reusable html template created earlier - **To see an example, take a look at `base.html` and `home.html`**
3. Create **render** functions for rendering the template pages, in the `views.py` file, and link it with the desired template html file - **To see an example, take a look at the `home()` function that renders the `home.html`**

## Create DB Models
#### Creating models that are transformed into DB schemas is done in the `models.py` file:
- A model is a class that inherits from the `django.db.models.Model` class
- The model would have have fields that are derived from Django types: for example, `models.CharField`, `models.BooleanField`, etc
- To see an example model, look at `DBItem` in `models.py`

#### Once a model is created, it needs to be registered with Django so that it would be available in the admin panel
1. We need to import our newly created model(s) into the `admin.py` file
2. Once imported, the model(s) need to be registered via the `admin.site.register` function

#### Finally, the model would have to go through `migration` in order for it to be a part of our DB
- Everytime that we make a change to our database models (or create a new one), we would need to invoke something known as a `migration` 
- The command to make a migration is as follows: **$     python manage.py makemigrations**
- To finalize the migration and apply  data updates: **$     python manage.py migrate**

## Django Admin Panel
#### The Django admin panel allows us to look at our routes, data, users, and basically anything that we want to see regarding our backend data and services
1. First thing before you can use the Django panel of your app, you would need to have a `user`
2. To create an admin user: **$     python manage.py createsuperuser**
3. Enter the desired username and password (email is not mandatory)

#### With a super user, we can enter the admin panel and and login with our user credentials