# cloud-billing-system
### Prerequisites
```
python 3.x
```
### Installing

**[Optional]** 
Before the installation, a best practise would be setting a virtualenv for the project 

```
https://virtualenv.pypa.io/
```

All the necessary libraries are in requirements.txt
```
pip install -r requirements.txt
```
### Run the project

Execute the command below

```
python manage.py runserver
```
Note: for testing purposes, we used **sqlite** as a RDBMS (relational database management system)\
In production mode, we better use an other database server to handle 
concurrency problems E.g. PostgreSQL, Microsoft SQL Server..
## Built With

* [python 3.7](https://www.python.org/) 
* [django 2.2.6](https://www.djangoproject.com/) 
* [djangorestframework](https://www.djangoproject.com/)
