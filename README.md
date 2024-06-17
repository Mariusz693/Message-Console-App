# Message-Console-App

Console application for sending text messages.

### Technologies:
* Argparse
* Active Record
* Psycopg2-binary

### Installation:
* Creating a virtual environment `virtualenv -p python3 env`
* Activation of the virtual environment `source env/bin/activate`
* Installation of necessary libraries `pip3 install psycopg2-binary`
* Creating a file db_settings.py wich varibles `DB_USER`, `DB_PASSWORD` and `DB_HOST`
* Database initialization `python3 db_create.py`

### Using
* List user `python3 app.py -l`
* Create user `python3 app.py -u <username> -p <password>`
* New password `python3 app.py -u <username> -p <password> -n <new_password>`
* Delete user `python3 app.py -u <username> -p <password> -d`
* Send message `python3 app.py -u <username> -p <password> -t <to_username> -s <'text message'>`
* User messages `python3 app.py -u <username> -p <password> -m`
* Help `python3 app.py`

### Contact
* [LinkedIn](https://www.linkedin.com/in/mariusz-kuleta/)