# Usage Instructions<br><br>
1. Run pip install -r requirements.txt from the root directory of the folder.<br><br>
2. If there is no `log` folder create one.
3. Add your local mysql workbench data to the .env file. (Remember never to push this fille when commiting; git will automatically ignore it but just a precationary reminder).

If you do not have a .env file in the root folder directory: create a file called `.env` & add the following lines into the file (replacing the relevant info):
NB: make sure each variable (HOST, USER, etc.) is placed on a new line in your .env file.

HOST = "YOURHOSTNAME"<br>
USER = "YOURUSERNAME"<br>
PASSWD = "YOURPASSWORD"<br>
DATABASE = "YOURDATABASE --default-- = 'rating'"<br><br>
1. Execute the `create_mysql_tables.py` file.<br><br>
2. run test_app.py
