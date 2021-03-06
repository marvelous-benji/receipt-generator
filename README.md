# A Simple Receipt Generator

![Project Image](https://img.shields.io/badge/python-DRF-blue)


---

### Table of Contents

- [Description](#description)
- [How To Use](#how-to-use)

---

## Description

This is a simple receipt generator, where business owners,
can create account and are able to generate and issue actual receipts
or templates for goods sold to customers.

#### Technologies

- Python
- Django
- JWT

[Back To The Top](#read-me-template)

---

## How To Use

[Documentation](https://documenter.getpostman.com/view/15462060/Tzm9jumT)


[Application url](https://receipt-api-staging.herokuapp.com/)

#### Installation
```bash
git clone https://github.com/marvelous-benji/receipt-generator.git
run cd receipt-generator
setup a virtual enviroment by running python -m venv env
then run source env/bin/activate
finally run pip install -r requirements.txt
(check to see if any of these differ on windows OS)
```


#### SetUp

```python
    For Unix(that is mac or linux)
    in the project root, enter: export SECRET_KEY={your_secret_key}
    export DJANGO_SETTINGS_MODULE=config.settings.mysettings
    export DOCUMENTER_URL={{The Documentation Url}}
    python manage.py  makemigrations         
    python manage.py migrate
    Then python manage.py runserver

    To run test
    python manage.py test

    for windows OS use set instead of export

```
